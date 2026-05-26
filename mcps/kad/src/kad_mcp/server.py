"""MCP server для kad.arbitr.ru — Картотека арбитражных дел.

kad.arbitr.ru — публичная база арбитражных дел РФ. Официального публичного API
не имеет, но есть JSON endpoints используемые сайтом (`/Kad/SearchInstances`,
`/Kad/Card`). Они нестабильны и могут потребовать сессионных cookie + anti-bot
обхода в production.

Этот MCP реализует базовый search + карточка дела через эти endpoints. Для
production volumes рекомендуется paid интеграция через СПАРК / Контур /
Casebook / kad-arbitr-parser-as-a-service.

Logging — strictly to stderr; stdout — MCP protocol only.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
from typing import Annotated, Any

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("kad-mcp")

KAD_BASE = "https://kad.arbitr.ru"
KAD_API_BASE = f"{KAD_BASE}/Kad"

REQUEST_TIMEOUT_S = 30.0
MAX_CONCURRENT_REQUESTS = 3  # kad.arbitr.ru rate-limits aggressively

mcp = FastMCP(
    name="kad",
    instructions=(
        "Поиск арбитражных дел и получение карточек дел с kad.arbitr.ru. "
        "Используй для DD контрагентов (открытые иски как ответчика / истца), "
        "tracking конкретных дел, анализа судебной практики по конкретным судам / "
        "категориям споров. Note: возвращает данные с временной задержкой; для "
        "real-time mission-critical use — paid интеграция СПАРК / Контур."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None

_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_S = 1800.0  # 30 min — kad.arbitr данные меняются медленно
_CACHE_MAX_ENTRIES = 500


def _get_http_client() -> httpx.AsyncClient:
    """HTTP client с browser-like UA + cookie jar.

    kad.arbitr.ru блокирует custom UA (HTTP 451 anti-bot).
    По умолчанию используем Chrome 120 fingerprint.
    Override через env KAD_USER_AGENT.

    Note: kad имеет Qrator/Cloudflare защиту, even с правильным UA может
    давать 451 при sustained load. Для production volumes рекомендуется
    paid feed (casebook, СПАРК).
    """
    import os
    global _http_client
    if _http_client is None:
        default_ua = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        ua = os.environ.get("KAD_USER_AGENT", default_ua)
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": ua,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://kad.arbitr.ru/",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            },
            limits=httpx.Limits(max_connections=5, max_keepalive_connections=3),
            follow_redirects=True,
            cookies=httpx.Cookies(),  # cookie jar для session
        )
    return _http_client


def _get_semaphore() -> asyncio.Semaphore:
    global _request_semaphore
    if _request_semaphore is None:
        _request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    return _request_semaphore


def _cache_get(key: str) -> Any | None:
    entry = _cache.get(key)
    if entry is None:
        return None
    ts, value = entry
    if time.monotonic() - ts > _CACHE_TTL_S:
        _cache.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: Any) -> None:
    if key not in _cache and len(_cache) >= _CACHE_MAX_ENTRIES:
        oldest_key = next(iter(_cache))
        _cache.pop(oldest_key, None)
    _cache[key] = (time.monotonic(), value)


def _build_cache_key(method: str, url: str, payload: dict[str, Any] | None) -> str:
    serialized = json.dumps(payload or {}, ensure_ascii=False, sort_keys=True, default=str)
    return f"{method} {url} {serialized}"


async def _api_post(url: str, json_payload: dict[str, Any]) -> Any:
    """POST к kad.arbitr.ru. Search endpoints используют POST с JSON."""
    cache_key = _build_cache_key("POST", url, json_payload)
    cached = _cache_get(cache_key)
    if cached is not None:
        logger.debug("cache hit: %s", cache_key)
        return cached

    client = _get_http_client()
    async with _get_semaphore():
        try:
            resp = await client.post(url, json=json_payload)
        except httpx.TimeoutException as e:
            logger.warning("Timeout: %s", url)
            raise ToolError(
                f"kad.arbitr.ru не ответил за {REQUEST_TIMEOUT_S} сек. Часто bypass через VPN помогает."
            ) from e
        except httpx.RequestError as e:
            logger.warning("Network error: %s: %s", url, e)
            raise ToolError(f"Не удалось связаться с kad.arbitr.ru: {e}") from e

    if resp.status_code == 403:
        raise ToolError(
            "kad.arbitr.ru заблокировал запрос (HTTP 403). Anti-bot protection. "
            "Для production используй paid интеграцию (СПАРК / Контур / Casebook)."
        )
    if resp.status_code == 404:
        raise ToolError("Запрашиваемый ресурс не найден на kad.arbitr.ru.")
    if resp.status_code >= 500:
        raise ToolError(
            f"kad.arbitr.ru вернул ошибку сервера (HTTP {resp.status_code}). "
            "Источник часто нестабилен — повтори позже."
        )
    if resp.status_code >= 400:
        logger.warning("HTTP %d from %s: %s", resp.status_code, url, resp.text[:500])
        raise ToolError(
            f"Ошибка запроса к kad.arbitr.ru (HTTP {resp.status_code}). "
            "Проверь параметры (номер дела в формате 'A40-1234/2025')."
        )

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError(
            "kad.arbitr.ru вернул не-JSON ответ. Возможно anti-bot challenge (captcha). "
            "Production setup требует session cookie management или paid API."
        ) from e

    _cache_set(cache_key, data)
    return data


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_cases(
    case_number: Annotated[
        str | None,
        Field(
            description=(
                "Номер дела в формате 'A40-12345/2025' (А — арбитраж, 40 — Москва, "
                "12345 — номер, 2025 — год). Регистр буквы 'А' любой. "
                "Если задан — остальные фильтры игнорируются."
            ),
            pattern=r"^[АAaа]\d{1,3}-\d+/\d{4}$",
            max_length=30,
        ),
    ] = None,
    plaintiff: Annotated[
        str | None,
        Field(
            description="Истец — полное / частичное наименование ЮЛ или ФИО.",
            max_length=300,
        ),
    ] = None,
    defendant: Annotated[
        str | None,
        Field(
            description="Ответчик — полное / частичное наименование ЮЛ или ФИО.",
            max_length=300,
        ),
    ] = None,
    plaintiff_inn: Annotated[
        str | None,
        Field(
            description="ИНН истца (10 цифр для ЮЛ, 12 для ИП).",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    defendant_inn: Annotated[
        str | None,
        Field(
            description="ИНН ответчика (10 цифр для ЮЛ, 12 для ИП).",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    court_id: Annotated[
        str | None,
        Field(
            description=(
                "Идентификатор суда (например 'А40' для АС Москвы, 'А56' для АС СПб). "
                "Получить список через list_courts."
            ),
            max_length=10,
        ),
    ] = None,
    date_from: Annotated[
        str | None,
        Field(
            description="Дата подачи иска не ранее (YYYY-MM-DD).",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    date_to: Annotated[
        str | None,
        Field(
            description="Дата подачи иска не позднее (YYYY-MM-DD).",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    sum_min: Annotated[
        float | None,
        Field(description="Сумма иска минимум (руб).", ge=0),
    ] = None,
    sum_max: Annotated[
        float | None,
        Field(description="Сумма иска максимум (руб).", ge=0),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум дел в ответе.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Поиск арбитражных дел в kad.arbitr.ru.

    Возвращает список с метаданными (номер, суд, стороны, текущая стадия, сумма иска).
    Для полной карточки + истории актов используй get_case_card(case_number).

    Use cases:
    - DD контрагента: defendant=<имя> чтобы найти все иски против него
    - Tracking своего пула дел: plaintiff_inn=<наш ИНН>
    - Анализ практики: court_id + date_from + date_to для конкретной категории
    """
    if not any([case_number, plaintiff, defendant, plaintiff_inn, defendant_inn]):
        raise ToolError(
            "Нужен хотя бы один из критериев: case_number / plaintiff / defendant / "
            "plaintiff_inn / defendant_inn. Иначе результаты будут слишком broad."
        )

    logger.info(
        "search_cases case_number=%s plaintiff=%r defendant=%r limit=%d",
        case_number, plaintiff, defendant, limit,
    )

    payload: dict[str, Any] = {
        "Page": 1,
        "Count": limit,
    }
    if case_number:
        payload["CaseNumbers"] = [case_number.upper().replace("А", "A")]
    if plaintiff:
        payload["Plaintiffs"] = [{"Name": plaintiff}]
    if defendant:
        payload["Respondents"] = [{"Name": defendant}]
    if plaintiff_inn:
        payload.setdefault("Plaintiffs", []).append({"Inn": plaintiff_inn})
    if defendant_inn:
        payload.setdefault("Respondents", []).append({"Inn": defendant_inn})
    if court_id:
        payload["Courts"] = [court_id]
    if date_from:
        payload["DateFrom"] = f"{date_from}T00:00:00"
    if date_to:
        payload["DateTo"] = f"{date_to}T23:59:59"
    if sum_min is not None:
        payload["SumFrom"] = sum_min
    if sum_max is not None:
        payload["SumTo"] = sum_max

    data = await _api_post(f"{KAD_API_BASE}/SearchInstances", payload)

    items = data.get("Result", {}).get("Items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        logger.warning("Unexpected response shape from /SearchInstances")
        return []

    return [_normalize_case_item(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_case_card(
    case_number: Annotated[
        str,
        Field(
            description="Номер дела (например 'A40-12345/2025').",
            pattern=r"^[АAaа]\d{1,3}-\d+/\d{4}$",
            max_length=30,
        ),
    ],
) -> dict[str, Any]:
    """Получает полную карточку дела с историей: стадии, акты, заседания, стороны.

    Используй после search_cases когда нужны детали по конкретному делу.

    Returns:
        Карточка с полями: case_number, court, plaintiffs, defendants, third_parties,
        judges, current_stage, sum_claim, sum_decision, hearings, judicial_acts.
    """
    logger.info("get_case_card case_number=%s", case_number)

    normalized_number = case_number.upper().replace("А", "A")
    payload = {"CaseNumbers": [normalized_number]}
    data = await _api_post(f"{KAD_API_BASE}/Card", payload)

    if not isinstance(data, dict):
        raise ToolError("Не удалось разобрать карточку дела.")

    return _normalize_case_card(data)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_case_documents(
    case_number: Annotated[
        str,
        Field(
            description="Номер дела для получения списка судебных актов.",
            pattern=r"^[АAaа]\d{1,3}-\d+/\d{4}$",
            max_length=30,
        ),
    ],
    limit: Annotated[
        int,
        Field(description="Максимум документов.", ge=1, le=200),
    ] = 50,
) -> list[dict[str, Any]]:
    """Список судебных актов (решений, определений, постановлений) по делу.

    Каждый акт содержит дату, тип, инстанцию, ссылку на PDF.
    """
    logger.info("get_case_documents case_number=%s", case_number)

    normalized_number = case_number.upper().replace("А", "A")
    payload = {"CaseNumber": normalized_number, "Count": limit}
    data = await _api_post(f"{KAD_API_BASE}/CaseDocuments", payload)

    items = data.get("Result", {}).get("Items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []

    return [_normalize_document(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def list_courts() -> list[dict[str, str]]:
    """Справочник арбитражных судов РФ — для параметра court_id в search_cases.

    Возвращает список со структурой:
    - АС субъектов РФ (первая инстанция) — `A01` (Адыгея) ... `A99` (...)
    - АС округов (кассация) — `АС МО`, `АС СЗО` и т.п.
    - 21 апелляционный АС
    - Суд по интеллектуальным правам (СИП) — для IP-споров
    - Верховный Суд РФ — экстраординарная инстанция
    """
    logger.info("list_courts")
    # Static reference — этот endpoint редко меняется; зашиваем для надёжности.
    return _STATIC_COURTS_LIST


# ----------------------------------------------------------------------------
# Normalizers — приводят response к стабильной форме для LLM consumption.
# ----------------------------------------------------------------------------

def _normalize_case_item(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item, "_warning": "unexpected response shape"}

    case_number = item.get("CaseNumber") or item.get("Number")
    return {
        "case_number": case_number,
        "court": item.get("Court", {}).get("Name") if isinstance(item.get("Court"), dict) else item.get("Court"),
        "judges": [
            j.get("Name") for j in item.get("Judges", []) if isinstance(j, dict)
        ] or None,
        "plaintiffs": _extract_parties(item.get("Plaintiffs")),
        "defendants": _extract_parties(item.get("Respondents")),
        "filed_date": item.get("FiledDate"),
        "current_stage": item.get("StageName") or item.get("Stage"),
        "sum_claim": item.get("ClaimSum"),
        "url": f"{KAD_BASE}/Card/{case_number}" if case_number else None,
    }


def _normalize_case_card(data: dict[str, Any]) -> dict[str, Any]:
    result = data.get("Result") if isinstance(data.get("Result"), dict) else data
    if not isinstance(result, dict):
        return {"raw": data, "_warning": "unexpected response shape"}

    case_number = result.get("CaseNumber") or result.get("Number")
    return {
        "case_number": case_number,
        "court": _safe_dict_field(result.get("Court"), "Name"),
        "category": result.get("Category"),
        "judges": [_safe_dict_field(j, "Name") for j in result.get("Judges") or [] if j],
        "plaintiffs": _extract_parties(result.get("Plaintiffs")),
        "defendants": _extract_parties(result.get("Respondents")),
        "third_parties": _extract_parties(result.get("ThirdParties")),
        "current_stage": result.get("StageName"),
        "filed_date": result.get("FiledDate"),
        "decision_date": result.get("DecisionDate"),
        "sum_claim": result.get("ClaimSum"),
        "sum_decision": result.get("DecisionSum"),
        "hearings": [
            {
                "date": h.get("Date"),
                "time": h.get("Time"),
                "court": _safe_dict_field(h.get("Court"), "Name"),
                "type": h.get("Type"),
            }
            for h in result.get("Hearings") or []
            if isinstance(h, dict)
        ] or None,
        "url": f"{KAD_BASE}/Card/{case_number}" if case_number else None,
    }


def _normalize_document(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item, "_warning": "unexpected response shape"}
    file_link = item.get("FileLink") or item.get("Link")
    return {
        "date": item.get("Date") or item.get("PublishDate"),
        "type": item.get("DocumentType") or item.get("Type"),
        "instance": _safe_dict_field(item.get("Court"), "Name"),
        "pdf_url": f"{KAD_BASE}{file_link}" if file_link and file_link.startswith("/") else file_link,
        "case_number": item.get("CaseNumber"),
    }


def _extract_parties(parties: Any) -> list[dict[str, Any]] | None:
    if not isinstance(parties, list):
        return None
    extracted = []
    for p in parties:
        if not isinstance(p, dict):
            continue
        extracted.append(
            {
                "name": p.get("Name"),
                "inn": p.get("Inn"),
                "ogrn": p.get("Ogrn"),
                "address": p.get("Address"),
                "type": p.get("Type"),  # ЮЛ / ИП / физ.лицо
            }
        )
    return extracted or None


def _safe_dict_field(obj: Any, field: str) -> Any:
    return obj.get(field) if isinstance(obj, dict) else None


# Static reference list of major arbitration courts.
# Reduces dependency on kad.arbitr endpoint stability for this lookup.
_STATIC_COURTS_LIST: list[dict[str, str]] = [
    {"id": "А40", "name": "Арбитражный суд города Москвы"},
    {"id": "А41", "name": "Арбитражный суд Московской области"},
    {"id": "А56", "name": "Арбитражный суд города Санкт-Петербурга и Ленинградской области"},
    {"id": "А32", "name": "Арбитражный суд Краснодарского края"},
    {"id": "А60", "name": "Арбитражный суд Свердловской области"},
    {"id": "А45", "name": "Арбитражный суд Новосибирской области"},
    {"id": "А33", "name": "Арбитражный суд Красноярского края"},
    {"id": "А50", "name": "Арбитражный суд Пермского края"},
    {"id": "А70", "name": "Арбитражный суд Тюменской области"},
    {"id": "А55", "name": "Арбитражный суд Самарской области"},
    {"id": "А12", "name": "Арбитражный суд Волгоградской области"},
    {"id": "А75", "name": "Арбитражный суд Ханты-Мансийского АО — Югры"},
    {"id": "А57", "name": "Арбитражный суд Саратовской области"},
    {"id": "А46", "name": "Арбитражный суд Омской области"},
    {"id": "А47", "name": "Арбитражный суд Оренбургской области"},
    {"id": "А76", "name": "Арбитражный суд Челябинской области"},
    {"id": "А65", "name": "Арбитражный суд Республики Татарстан"},
    {"id": "СИП", "name": "Суд по интеллектуальным правам"},
    {"id": "АС МО", "name": "Арбитражный суд Московского округа (кассация)"},
    {"id": "АС СЗО", "name": "Арбитражный суд Северо-Западного округа (кассация)"},
    {"id": "АС СКО", "name": "Арбитражный суд Северо-Кавказского округа (кассация)"},
    {"id": "АС УО", "name": "Арбитражный суд Уральского округа (кассация)"},
    {"id": "АС ВВО", "name": "Арбитражный суд Волго-Вятского округа (кассация)"},
    {"id": "АС ВСО", "name": "Арбитражный суд Восточно-Сибирского округа (кассация)"},
    {"id": "АС ДВО", "name": "Арбитражный суд Дальневосточного округа (кассация)"},
    {"id": "АС ПО", "name": "Арбитражный суд Поволжского округа (кассация)"},
    {"id": "АС ЦО", "name": "Арбитражный суд Центрального округа (кассация)"},
    {"id": "АС ЗСО", "name": "Арбитражный суд Западно-Сибирского округа (кассация)"},
    {"id": "ВС РФ", "name": "Верховный Суд Российской Федерации"},
]


@mcp.resource("kad://practice-cheatsheet")
def practice_cheatsheet() -> str:
    """Справка по работе с kad.arbitr.ru для DD / litigation tracking."""
    return (
        "# Картотека арбитражных дел (kad.arbitr.ru)\n\n"
        "## Структура номера дела\n\n"
        "`А40-12345/2025` — арбитражное дело:\n"
        "- `А` — арбитражный (от 'арбитраж')\n"
        "- `40` — код суда первой инстанции (40 = Москва)\n"
        "- `12345` — порядковый номер\n"
        "- `2025` — год регистрации\n\n"
        "## Типичные стадии\n\n"
        "- **Первая инстанция** (АС субъекта или СИП)\n"
        "- **Апелляция** (21 ААС покрывают РФ)\n"
        "- **Кассация** (10 АС округов)\n"
        "- **Надзор** (ВС РФ)\n\n"
        "## Use cases для DD\n\n"
        "1. **Открытые иски против контрагента** — `search_cases(defendant=<имя>)` "
        "+ filter по `current_stage`\n"
        "2. **Pattern сутяжничества** — high count cases как plaintiff = potentially aggressive\n"
        "3. **Финансовые проблемы** — высокая `sum_claim` против контрагента + взыскания\n"
        "4. **Бывшие проигрыши** — `current_stage` = 'Решение вступило в законную силу' "
        "по существу — материал для расчёта риска\n\n"
        "## Limitations\n\n"
        "- kad.arbitr.ru имеет anti-bot защиту — для production нужен paid feed (СПАРК / "
        "Контур.Фокус / Casebook) либо scraping infrastructure\n"
        "- Данные обновляются с задержкой 1-3 дня от actual events\n"
        "- Не все дела включают полные документы (часть только metadata)\n"
    )


def main() -> None:
    """Entry point для CLI (kad-mcp)."""
    logger.info("Starting kad-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
