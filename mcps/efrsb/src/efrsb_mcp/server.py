"""MCP server для bankrot.fedresurs.ru — ЕФРСБ (Единый федеральный реестр
сведений о банкротстве).

Источник публикуется через ФЗ-127 «О несостоятельности (банкротстве)» ст.28 + ст.213.7
для физ.лиц. Включает все опубликованные сведения: открытие производства,
назначение арбитражного управляющего, торги, отчёты, реестры требований.

ЕФРСБ имеет official JSON endpoints для search (bankrot.fedresurs.ru/Companies.aspx
через JSON XHR calls). Этот MCP wraps их в structured tools.

Logging — strictly to stderr.
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
logger = logging.getLogger("efrsb-mcp")

EFRSB_BASE = "https://bankrot.fedresurs.ru"
EFRSB_API_BASE = f"{EFRSB_BASE}/backend"

REQUEST_TIMEOUT_S = 30.0
MAX_CONCURRENT_REQUESTS = 5

mcp = FastMCP(
    name="efrsb",
    instructions=(
        "Проверка контрагентов и физ.лиц в Едином федеральном реестре сведений "
        "о банкротстве (ЕФРСБ / Федресурс). Critical для DD контрагентов перед "
        "сделкой — попадание в реестр банкротов часто означает невозможность "
        "получить оплату / выполнение обязательств. Также: tracking конкретных "
        "банкротных процедур, поиск арбитражных управляющих, мониторинг torgs."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None

_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_S = 3600.0  # 1 час — банкротные данные меняются медленно
_CACHE_MAX_ENTRIES = 500


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": "efrsb-mcp/0.1.0",
                "Accept": "application/json",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Referer": "https://bankrot.fedresurs.ru/",
            },
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
            follow_redirects=True,
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


async def _api_request(method: str, url: str, **kwargs: Any) -> Any:
    cache_key = f"{method} {url} {json.dumps(kwargs, sort_keys=True, default=str)}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    client = _get_http_client()
    async with _get_semaphore():
        try:
            resp = await client.request(method, url, **kwargs)
        except httpx.TimeoutException as e:
            raise ToolError(f"bankrot.fedresurs.ru timed out за {REQUEST_TIMEOUT_S}s.") from e
        except httpx.RequestError as e:
            raise ToolError(f"Не удалось связаться с bankrot.fedresurs.ru: {e}") from e

    if resp.status_code == 404:
        raise ToolError("Запрашиваемый ресурс не найден в ЕФРСБ.")
    if resp.status_code >= 500:
        raise ToolError(
            f"ЕФРСБ вернул ошибку сервера (HTTP {resp.status_code}). Попробуй позже."
        )
    if resp.status_code >= 400:
        logger.warning("HTTP %d from %s: %s", resp.status_code, url, resp.text[:500])
        raise ToolError(
            f"Ошибка запроса к ЕФРСБ (HTTP {resp.status_code}). Проверь параметры."
        )

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError("ЕФРСБ вернул не-JSON ответ. Источник может быть в degraded mode.") from e

    _cache_set(cache_key, data)
    return data


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def check_company_bankruptcy(
    inn: Annotated[
        str | None,
        Field(
            description="ИНН ЮЛ (10 цифр) или ИП (12 цифр) для точного поиска.",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    ogrn: Annotated[
        str | None,
        Field(
            description="ОГРН ЮЛ (13 цифр) или ОГРНИП (15 цифр).",
            pattern=r"^\d{13}$|^\d{15}$",
        ),
    ] = None,
    name: Annotated[
        str | None,
        Field(
            description="Наименование ЮЛ / ИП — для поиска (less reliable чем ИНН).",
            min_length=3,
            max_length=300,
        ),
    ] = None,
) -> dict[str, Any]:
    """Проверка ЮЛ / ИП на банкротство в ЕФРСБ.

    Returns:
        - status: 'not_found' / 'no_bankruptcy' / 'in_bankruptcy' / 'completed'
        - case_number: номер арбитражного дела (если есть)
        - stage: текущая стадия (наблюдение / финансовое оздоровление / внешнее
                управление / конкурсное производство / завершено)
        - arbitration_manager: данные арбитражного управляющего
        - dates: ключевые даты процедуры
        - publications_count: количество публикаций по делу

    Critical для DD: попадание в банкротство = high risk сделки.
    """
    if not any([inn, ogrn, name]):
        raise ToolError("Нужен хотя бы один: inn / ogrn / name.")

    logger.info("check_company_bankruptcy inn=%s ogrn=%s name=%r", inn, ogrn, name)

    params: dict[str, Any] = {}
    if inn:
        params["searchString"] = inn
    elif ogrn:
        params["searchString"] = ogrn
    elif name:
        params["searchString"] = name

    params["limit"] = 5
    data = await _api_request(
        "GET",
        f"{EFRSB_API_BASE}/companies",
        params=params,
    )

    items = data.get("pageData") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return {"status": "not_found", "query": params["searchString"]}

    # Take the best match — first result или exact ИНН match
    best = items[0]
    if inn:
        for item in items:
            if item.get("inn") == inn:
                best = item
                break

    return _normalize_company_bankruptcy(best)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def check_person_bankruptcy(
    inn: Annotated[
        str | None,
        Field(
            description="ИНН физ.лица (12 цифр).",
            pattern=r"^\d{12}$",
        ),
    ] = None,
    full_name: Annotated[
        str | None,
        Field(
            description="ФИО полностью — например 'Иванов Иван Иванович'.",
            min_length=5,
            max_length=200,
        ),
    ] = None,
    birth_date: Annotated[
        str | None,
        Field(
            description="Дата рождения (YYYY-MM-DD) — sharpens search at common names.",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
) -> dict[str, Any]:
    """Проверка физ.лица на банкротство (ФЗ-127 глава X с 2015 — потребительское банкротство).

    Returns similar structure как check_company_bankruptcy.

    Critical для personal DD (например, проверка ГД / бенефициара перед M&A).
    """
    if not any([inn, full_name]):
        raise ToolError("Нужен хотя бы один: inn / full_name.")

    logger.info("check_person_bankruptcy inn=%s full_name=%r", inn, full_name)

    search_string = inn or full_name
    params: dict[str, Any] = {"searchString": search_string, "limit": 5}
    if birth_date:
        params["birthDate"] = birth_date

    data = await _api_request(
        "GET",
        f"{EFRSB_API_BASE}/persons",
        params=params,
    )

    items = data.get("pageData") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return {"status": "not_found", "query": search_string}

    best = items[0]
    if inn:
        for item in items:
            if item.get("inn") == inn:
                best = item
                break

    return _normalize_person_bankruptcy(best)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_bankruptcy_case_publications(
    case_id: Annotated[
        str,
        Field(
            description=(
                "ID банкротного дела в ЕФРСБ (получается из check_company_bankruptcy / "
                "check_person_bankruptcy в поле 'efrsb_id')."
            ),
            min_length=1,
            max_length=100,
            pattern=r"^[A-Za-z0-9_\-]+$",
        ),
    ],
    limit: Annotated[
        int,
        Field(description="Максимум публикаций.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Получает список публикаций по конкретному банкротному делу.

    Публикации содержат:
    - Объявления о торгах (для покупки имущества debtor-а)
    - Reports арбитражного управляющего
    - Уведомления о собраниях кредиторов
    - Иные обязательные публикации (ФЗ-127 ст.28)

    Use case: tracking конкретного банкротного дела где мы кредитор / interested party.
    """
    logger.info("get_bankruptcy_case_publications case_id=%s", case_id)

    data = await _api_request(
        "GET",
        f"{EFRSB_API_BASE}/cases/{case_id}/publications",
        params={"limit": limit},
    )

    items = data.get("pageData") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []

    return [_normalize_publication(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_arbitration_manager(
    full_name: Annotated[
        str | None,
        Field(
            description="ФИО арбитражного управляющего.",
            min_length=5,
            max_length=200,
        ),
    ] = None,
    inn: Annotated[
        str | None,
        Field(
            description="ИНН арбитражного управляющего (12 цифр).",
            pattern=r"^\d{12}$",
        ),
    ] = None,
    sro: Annotated[
        str | None,
        Field(
            description="СРО арбитражных управляющих — название или часть.",
            max_length=200,
        ),
    ] = None,
) -> list[dict[str, Any]]:
    """Поиск арбитражного управляющего в реестре.

    Use case: verify статус назначенного управляющего, поиск управляющего с
    опытом в нашей сфере для potential involvement.
    """
    if not any([full_name, inn, sro]):
        raise ToolError("Нужен хотя бы один критерий поиска.")

    logger.info("search_arbitration_manager fio=%r inn=%s sro=%r", full_name, inn, sro)

    params: dict[str, Any] = {"limit": 25}
    if full_name:
        params["fullName"] = full_name
    if inn:
        params["inn"] = inn
    if sro:
        params["sroName"] = sro

    data = await _api_request(
        "GET",
        f"{EFRSB_API_BASE}/arbitrManagers",
        params=params,
    )

    items = data.get("pageData") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []

    return [_normalize_arbitration_manager(item) for item in items[:25]]


# ----------------------------------------------------------------------------
# Normalizers
# ----------------------------------------------------------------------------

# Map russian статус → English plus original.
_STATUS_MAP = {
    "Наблюдение": "monitoring",
    "Финансовое оздоровление": "financial_recovery",
    "Внешнее управление": "external_management",
    "Конкурсное производство": "liquidation",
    "Мировое соглашение": "settlement_agreement",
    "Реструктуризация долгов": "debt_restructuring",  # для физ.лиц
    "Реализация имущества": "property_sale",  # для физ.лиц
    "Завершено": "completed",
    "Прекращено": "terminated",
}


def _normalize_company_bankruptcy(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"status": "unknown", "raw": item}

    bankruptcy_data = item.get("bankruptCases") or item.get("activeCase")

    # Если bankruptCases пустой / None — компания не в банкротстве (но в реестре по
    # другим причинам, например как кредитор)
    if not bankruptcy_data:
        return {
            "status": "no_bankruptcy",
            "name": item.get("name"),
            "inn": item.get("inn"),
            "ogrn": item.get("ogrn"),
            "_note": "Компания в реестре, но активного банкротного дела нет.",
        }

    case = bankruptcy_data[0] if isinstance(bankruptcy_data, list) else bankruptcy_data
    russian_status = case.get("statusName") or case.get("category", "")
    return {
        "status": "in_bankruptcy" if "Завершено" not in russian_status else "completed",
        "stage": _STATUS_MAP.get(russian_status, russian_status),
        "stage_ru": russian_status,
        "name": item.get("name"),
        "inn": item.get("inn"),
        "ogrn": item.get("ogrn"),
        "case_number": case.get("caseNumber"),
        "court": case.get("courtName"),
        "case_started": case.get("startDate"),
        "arbitration_manager": _safe_dict_field(case.get("arbitrManager"), "fullName"),
        "arbitration_manager_inn": _safe_dict_field(case.get("arbitrManager"), "inn"),
        "efrsb_id": case.get("id") or item.get("id"),
        "url": f"{EFRSB_BASE}/bankrupt/id/{item.get('id')}" if item.get("id") else None,
    }


def _normalize_person_bankruptcy(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"status": "unknown", "raw": item}

    bankruptcy_data = item.get("bankruptCases") or item.get("activeCase")

    if not bankruptcy_data:
        return {
            "status": "no_bankruptcy",
            "name": item.get("fullName"),
            "inn": item.get("inn"),
            "birth_date": item.get("birthDate"),
        }

    case = bankruptcy_data[0] if isinstance(bankruptcy_data, list) else bankruptcy_data
    russian_status = case.get("statusName", "")
    return {
        "status": "in_bankruptcy" if "Завершено" not in russian_status else "completed",
        "stage": _STATUS_MAP.get(russian_status, russian_status),
        "stage_ru": russian_status,
        "name": item.get("fullName"),
        "inn": item.get("inn"),
        "birth_date": item.get("birthDate"),
        "case_number": case.get("caseNumber"),
        "court": case.get("courtName"),
        "arbitration_manager": _safe_dict_field(case.get("arbitrManager"), "fullName"),
        "efrsb_id": case.get("id") or item.get("id"),
        "url": f"{EFRSB_BASE}/bankrupt/id/{item.get('id')}" if item.get("id") else None,
    }


def _normalize_publication(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    return {
        "id": item.get("id"),
        "date": item.get("publishDate"),
        "type": item.get("type"),
        "type_name": item.get("typeName"),
        "subject": item.get("subject") or item.get("title"),
        "url": f"{EFRSB_BASE}/message/{item.get('id')}" if item.get("id") else None,
    }


def _normalize_arbitration_manager(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    return {
        "full_name": item.get("fullName"),
        "inn": item.get("inn"),
        "sro": _safe_dict_field(item.get("sro"), "name"),
        "registration_number": item.get("registrationNumber"),
        "active": item.get("isActive", True),
        "active_cases_count": item.get("activeCasesCount"),
        "completed_cases_count": item.get("completedCasesCount"),
    }


def _safe_dict_field(obj: Any, field: str) -> Any:
    return obj.get(field) if isinstance(obj, dict) else None


@mcp.resource("efrsb://stages-cheatsheet")
def stages_cheatsheet() -> str:
    """Справка по стадиям банкротства РФ — для interpretation статусов."""
    return (
        "# Стадии банкротства (ФЗ-127)\n\n"
        "## Для юр.лиц\n\n"
        "1. **Наблюдение** (`monitoring`) — initial stage, временный управляющий.\n"
        "   - Срок: до 7 мес.\n"
        "   - Сделки company restrictions; крупные требуют согласия управляющего.\n\n"
        "2. **Финансовое оздоровление** (`financial_recovery`) — попытка восстановить.\n"
        "   - Срок: до 2 лет.\n"
        "   - Реже применяется (требует план + обеспечение).\n\n"
        "3. **Внешнее управление** (`external_management`) — внешний управляющий ведёт business.\n"
        "   - Срок: до 18 мес + продление до 6 мес.\n"
        "   - Существенно reduces сделкоспособность.\n\n"
        "4. **Конкурсное производство** (`liquidation`) — ликвидация имущества.\n"
        "   - Срок: 6 мес + продления.\n"
        "   - Реализация активов через торги.\n"
        "   - После завершения — ликвидация ЮЛ.\n\n"
        "5. **Мировое соглашение** (`settlement_agreement`) — соглашение с кредиторами.\n"
        "   - Возможно на любой стадии.\n\n"
        "## Для физ.лиц (ФЗ-127 глава X, с 2015)\n\n"
        "1. **Реструктуризация долгов** (`debt_restructuring`) — план до 3 лет.\n"
        "2. **Реализация имущества** (`property_sale`) — конкурсное для физ.лиц.\n"
        "3. **Мировое соглашение**.\n\n"
        "## DD significance\n\n"
        "- **`in_bankruptcy` любой stage** — high risk сделки; high probability default.\n"
        "- **`completed`** — после завершения процедуры. Для ЮЛ — обычно ликвидирован.\n"
        "  Для физ.лица — освобождён от долгов (limit 5 лет до next возможности).\n"
        "- **`no_bankruptcy`** — OK with respect к ЕФРСБ. Но check также kad.arbitr.ru\n"
        "  для recent filings (могут не успеть в ЕФРСБ).\n"
    )


def main() -> None:
    """Entry point для CLI (efrsb-mcp)."""
    logger.info("Starting efrsb-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
