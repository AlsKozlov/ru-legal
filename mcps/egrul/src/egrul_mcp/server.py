"""MCP server для ЕГРЮЛ/ЕГРИП через api-fns.ru.

Source: api-fns.ru — коммерческая обёртка над открытыми данными ФНС.
Бесплатный тариф "СПК-старт" даёт 800 запросов суммарно — нужен ключ из личного кабинета.

Логирование строго в stderr, ключ NEVER попадает в логи или error messages.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import time
from typing import Annotated, Any

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from egrul_mcp.validators import classify_identifier, is_valid_inn

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("egrul-mcp")

API_BASE = "https://api-fns.ru/api"
REQUEST_TIMEOUT_S = 30.0
MAX_CONCURRENT_REQUESTS = 3  # api-fns.ru без задокументированного rate limit, держим консервативно
MIN_REQUEST_INTERVAL_S = 0.4  # ~300-500ms между запросами для надёжности

# Кеш для ЕГРЮЛ — TTL длиннее, чем для НПА: данные о компаниях меняются реже.
_CACHE_TTL_S = 3600.0  # 1 час
_CACHE_MAX_ENTRIES = 1000

# Batch endpoint limit (api-fns.ru multinfo/multcheck)
BATCH_MAX_SIZE = 100

mcp = FastMCP(
    name="egrul",
    instructions=(
        "Проверка российских юридических лиц и ИП по данным ЕГРЮЛ/ЕГРИП через api-fns.ru. "
        "Используй для: проверки контрагента перед сделкой (статус, дата регистрации, "
        "руководитель, учредители), поиска организаций по названию, массовой проверки "
        "списка ИНН. Требует API ключ — переменная окружения API_FNS_KEY."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None
_last_request_time = 0.0
_rate_limit_lock: asyncio.Lock | None = None

_cache: dict[str, tuple[float, Any]] = {}


def _get_api_key() -> str:
    """Читает ключ из env. Не возвращает его в logs."""
    key = os.environ.get("API_FNS_KEY", "").strip()
    if not key:
        raise ToolError(
            "Переменная окружения API_FNS_KEY не задана. "
            "Зарегистрируйся на https://api-fns.ru, подключи тариф 'СПК-старт' "
            "(бесплатно, 800 запросов), скопируй ключ и установи: "
            "export API_FNS_KEY=<ваш-ключ>"
        )
    if len(key) < 20:
        raise ToolError(
            "API_FNS_KEY выглядит слишком коротким. Ожидается ключ из api-fns.ru "
            "(обычно 40 символов). Проверь, что скопировал полностью."
        )
    return key


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": "egrul-mcp/0.1.0",
                "Accept": "application/json",
            },
            limits=httpx.Limits(max_connections=5, max_keepalive_connections=3),
            follow_redirects=True,
        )
    return _http_client


def _get_semaphore() -> asyncio.Semaphore:
    global _request_semaphore
    if _request_semaphore is None:
        _request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    return _request_semaphore


def _get_rate_lock() -> asyncio.Lock:
    global _rate_limit_lock
    if _rate_limit_lock is None:
        _rate_limit_lock = asyncio.Lock()
    return _rate_limit_lock


async def _enforce_min_interval() -> None:
    """Гарантирует MIN_REQUEST_INTERVAL_S между последовательными запросами."""
    global _last_request_time
    async with _get_rate_lock():
        elapsed = time.monotonic() - _last_request_time
        if elapsed < MIN_REQUEST_INTERVAL_S:
            await asyncio.sleep(MIN_REQUEST_INTERVAL_S - elapsed)
        _last_request_time = time.monotonic()


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


def _build_cache_key(method: str, params: dict[str, Any]) -> str:
    # Ключ для кэша — БЕЗ значения API key (он одинаков для всех запросов и не должен утечь).
    safe_params = {k: v for k, v in params.items() if k != "key"}
    serialized = json.dumps(
        sorted(safe_params.items()),
        ensure_ascii=False,
        default=str,
    )
    return f"{method} {serialized}"


async def _api_call(method: str, params: dict[str, Any]) -> Any:
    """GET вызов api-fns.ru. Скрывает ключ от логов и error messages."""
    cache_key = _build_cache_key(method, params)
    cached = _cache_get(cache_key)
    if cached is not None:
        logger.debug("cache hit: %s", cache_key)
        return cached

    # Ключ добавляется в самый последний момент, перед самим запросом.
    full_params = {**params, "key": _get_api_key()}

    client = _get_http_client()
    url = f"{API_BASE}/{method}"

    await _enforce_min_interval()
    async with _get_semaphore():
        try:
            resp = await client.get(url, params=full_params)
        except httpx.TimeoutException as e:
            logger.warning("Timeout: api-fns.ru/%s", method)
            raise ToolError(
                f"api-fns.ru не ответил за {REQUEST_TIMEOUT_S} сек. Попробуй позже."
            ) from e
        except httpx.RequestError as e:
            # Не логируем e.request.url целиком — там ключ. Только метод.
            logger.warning("Network error calling %s: %s", method, type(e).__name__)
            raise ToolError(
                f"Не удалось связаться с api-fns.ru ({type(e).__name__}). "
                "Проверь интернет-соединение."
            ) from e

    if resp.status_code in (401, 402, 403):
        logger.warning(
            "Auth/quota error from api-fns.ru/%s: HTTP %d", method, resp.status_code
        )
        raise ToolError(
            "api-fns.ru отклонил запрос (HTTP "
            f"{resp.status_code}). Скорее всего: неверный API_FNS_KEY, "
            "закончилась квота тарифа, или закрыт доступ. "
            "Проверь личный кабинет на api-fns.ru."
        )
    if resp.status_code == 404:
        # Странно для GET-метода api-fns.ru, но возможно если method опечатан
        raise ToolError(f"Endpoint api-fns.ru/{method} не найден.")
    if resp.status_code >= 500:
        raise ToolError(
            f"api-fns.ru вернул ошибку сервера (HTTP {resp.status_code}). "
            "Источник иногда нестабилен — попробуй позже."
        )
    if resp.status_code >= 400:
        # Без вывода тела — может содержать ключ если api-fns.ru его эхо.
        logger.warning(
            "4xx from api-fns.ru/%s: HTTP %d, body length %d",
            method,
            resp.status_code,
            len(resp.text),
        )
        raise ToolError(
            f"Ошибка запроса к api-fns.ru (HTTP {resp.status_code}). "
            "Проверь параметры — корректность ИНН/ОГРН и имя метода."
        )

    # api-fns.ru возвращает auth-ошибку **строкой**, не JSON-объектом.
    raw_text = resp.text.strip()
    if raw_text.startswith('"') and raw_text.endswith('"'):
        # JSON-строка — потенциально текстовая ошибка
        try:
            data = resp.json()
            if isinstance(data, str):
                logger.warning("api-fns.ru returned string response: %s", data[:80])
                if "логин" in data.lower() or "пароль" in data.lower() or "ключ" in data.lower():
                    raise ToolError(
                        "api-fns.ru: неверный API ключ. Проверь переменную "
                        "окружения API_FNS_KEY — она должна совпадать с ключом "
                        "из личного кабинета api-fns.ru."
                    )
                raise ToolError(f"api-fns.ru вернул нестандартный ответ: {data[:120]}")
        except ValueError:
            pass

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError(
            "api-fns.ru вернул не-JSON ответ. Источник может быть в degraded mode."
        ) from e

    _cache_set(cache_key, data)
    return data


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def lookup_company(
    identifier: Annotated[
        str,
        Field(
            description=(
                "ИНН (10 цифр для ЮЛ, 12 для ИП) или ОГРН (13 цифр для ЮЛ, "
                "15 для ОГРНИП). Локально проверяется контрольная цифра — "
                "при невалидном идентификаторе HTTP-запрос НЕ делается, "
                "экономится квота API."
            ),
            min_length=10,
            max_length=15,
            pattern=r"^\d+$",
        ),
    ],
) -> dict[str, Any]:
    """Получить карточку организации из ЕГРЮЛ/ЕГРИП по ИНН или ОГРН.

    Возвращает структурированные данные: статус, дата регистрации, руководитель,
    учредители, ОКВЭД, юр.адрес. Используй для проверки контрагента перед сделкой.
    """
    kind = classify_identifier(identifier)
    if kind == "invalid":
        raise ToolError(
            f"Идентификатор {identifier} не прошёл локальную проверку контрольной "
            "цифры. Проверь, что ИНН/ОГРН скопирован правильно — это частая ошибка."
        )

    logger.info("lookup_company kind=%s len=%d", kind, len(identifier))
    data = await _api_call("egr", {"req": identifier})
    return _normalize_lookup_response(data, identifier)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_companies(
    query: Annotated[
        str,
        Field(
            description=(
                "Поисковая строка — название организации, фрагмент адреса, "
                "имя руководителя. Минимум 3 символа."
            ),
            min_length=3,
            max_length=500,
        ),
    ],
    limit: Annotated[
        int,
        Field(description="Максимум результатов в ответе.", ge=1, le=50),
    ] = 10,
) -> list[dict[str, Any]]:
    """Поиск организаций в ЕГРЮЛ по названию / фрагменту реквизитов.

    Возвращает список совпадений с базовыми реквизитами. Для полной карточки —
    вызывай lookup_company(inn) на конкретной найденной организации.
    """
    logger.info("search_companies query_len=%d limit=%d", len(query), limit)
    data = await _api_call("search", {"q": query})
    items = data.get("items", []) if isinstance(data, dict) else []
    if not isinstance(items, list):
        return []
    return [_normalize_search_item(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def batch_check_problematic(
    identifiers: Annotated[
        list[str],
        Field(
            description=(
                "Список ИНН для массовой проверки (до 100). Возвращает ТОЛЬКО "
                "проблемные организации: ликвидированные, в банкротстве, "
                "реорганизуемые. Если ИНН нет в ответе — организация в порядке. "
                "Идеально для bulk-скрининга контрагентов."
            ),
            min_length=1,
            max_length=BATCH_MAX_SIZE,
        ),
    ],
) -> dict[str, Any]:
    """Массовая проверка списка ИНН на проблемный статус через multcheck.

    Возвращает {checked: N, problematic: [...]}.  Невалидные ИНН отсекаются локально
    и возвращаются в поле invalid (HTTP-запрос для них не делается).
    """
    valid: list[str] = []
    invalid: list[str] = []
    for ident in identifiers:
        if is_valid_inn(ident):
            valid.append(ident)
        else:
            invalid.append(ident)

    if not valid:
        return {
            "checked": 0,
            "problematic": [],
            "invalid": invalid,
            "note": "Все переданные идентификаторы не прошли локальную проверку контрольной цифры.",
        }

    logger.info(
        "batch_check_problematic valid=%d invalid=%d", len(valid), len(invalid)
    )
    # multcheck возвращает только проблемные — "нет в ответе = всё ок"
    data = await _api_call("multcheck", {"req": ",".join(valid)})
    items = data.get("items", []) if isinstance(data, dict) else []
    if not isinstance(items, list):
        items = []

    return {
        "checked": len(valid),
        "problematic": [_normalize_search_item(it) for it in items],
        "invalid": invalid,
    }


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def validate_identifier(
    value: Annotated[
        str,
        Field(
            description="Строка для проверки. Возвращает тип идентификатора без обращения к API.",
            min_length=1,
            max_length=20,
        ),
    ],
) -> dict[str, str | bool]:
    """Локальная валидация ИНН/ОГРН по контрольной цифре. Не делает HTTP-запросов.

    Используй когда нужно быстро проверить корректность формата, не тратя квоту API.
    Возвращает {valid: bool, kind: 'inn-ul'|'inn-fl'|'ogrn'|'ogrnip'|'invalid'}.
    """
    kind = classify_identifier(value)
    return {"valid": kind != "invalid", "kind": kind, "value": value}


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def _normalize_lookup_response(data: Any, identifier: str) -> dict[str, Any]:
    """Приводит ответ /egr к плоской предсказуемой структуре.

    api-fns.ru возвращает {"items": [{"ЮЛ": {...}}]} или {"items": [{"ИП": {...}}]}.
    """
    if not isinstance(data, dict):
        return {"found": False, "identifier": identifier, "_warning": "unexpected response"}

    items = data.get("items", [])
    if not items:
        return {"found": False, "identifier": identifier}

    entry = items[0] if isinstance(items, list) else {}
    if not isinstance(entry, dict):
        return {"found": False, "identifier": identifier}

    if "ЮЛ" in entry and isinstance(entry["ЮЛ"], dict):
        return _flatten_legal_entity(entry["ЮЛ"])
    if "ИП" in entry and isinstance(entry["ИП"], dict):
        return _flatten_sole_proprietor(entry["ИП"])

    return {"found": True, "identifier": identifier, "raw": entry}


def _flatten_legal_entity(yu: dict[str, Any]) -> dict[str, Any]:
    """Распаковывает поля ЮЛ в плоский dict с английскими именами для удобства LLM."""
    address = yu.get("Адрес") or {}
    main_activity = yu.get("ОснВидДеят") or {}
    director = yu.get("Руководитель") or {}
    capital = yu.get("УставКап") or {}

    founders_raw = yu.get("Учредители") or []
    founders: list[dict[str, Any]] = []
    if isinstance(founders_raw, list):
        for f in founders_raw:
            if not isinstance(f, dict):
                continue
            person = f.get("УчрФЛ") or {}
            entity = f.get("УчрЮЛ") or {}
            founders.append(
                {
                    "type": "individual" if person else ("entity" if entity else "other"),
                    "name": person.get("ФИОПолн") or entity.get("НаимПолнЮЛ") or "",
                    "inn": person.get("ИННФЛ") or entity.get("ИНН") or "",
                    "share_percent": f.get("Процент"),
                    "share_amount": f.get("СуммаУК"),
                }
            )

    return {
        "found": True,
        "type": "legal-entity",
        "inn": yu.get("ИНН"),
        "kpp": yu.get("КПП"),
        "ogrn": yu.get("ОГРН"),
        "name_short": yu.get("НаимСокрЮЛ"),
        "name_full": yu.get("НаимПолнЮЛ"),
        "status": yu.get("Статус"),
        "is_active": (yu.get("Статус") or "").startswith("Действ"),
        "registered_at": yu.get("ДатаРег") or yu.get("ДатаОГРН"),
        "terminated_at": yu.get("ДатаПрекр"),
        "address_full": address.get("АдресПолн") if isinstance(address, dict) else None,
        "main_activity_code": main_activity.get("Код") if isinstance(main_activity, dict) else None,
        "main_activity_name": main_activity.get("Текст") if isinstance(main_activity, dict) else None,
        "director_name": director.get("ФИОПолн") if isinstance(director, dict) else None,
        "director_inn": director.get("ИННФЛ") if isinstance(director, dict) else None,
        "director_position": director.get("Должн") if isinstance(director, dict) else None,
        "charter_capital_rub": capital.get("СумКап") if isinstance(capital, dict) else None,
        "founders": founders,
    }


def _flatten_sole_proprietor(ip: dict[str, Any]) -> dict[str, Any]:
    """Аналогично для ИП."""
    fio = ip.get("ФИОПолн") or ip.get("ФИО") or {}
    if isinstance(fio, dict):
        full_name = " ".join(
            filter(None, [fio.get("Фамилия"), fio.get("Имя"), fio.get("Отчество")])
        ).strip()
    else:
        full_name = str(fio) if fio else ""

    main_activity = ip.get("ОснВидДеят") or {}
    return {
        "found": True,
        "type": "sole-proprietor",
        "inn": ip.get("ИННФЛ") or ip.get("ИНН"),
        "ogrnip": ip.get("ОГРНИП"),
        "name_full": full_name,
        "status": ip.get("Статус"),
        "is_active": (ip.get("Статус") or "").startswith("Действ"),
        "registered_at": ip.get("ДатаРег") or ip.get("ДатаОГРН"),
        "terminated_at": ip.get("ДатаПрекр"),
        "main_activity_code": main_activity.get("Код") if isinstance(main_activity, dict) else None,
        "main_activity_name": main_activity.get("Текст") if isinstance(main_activity, dict) else None,
    }


def _normalize_search_item(item: dict[str, Any]) -> dict[str, Any]:
    """Краткая нормализация для search результата."""
    if not isinstance(item, dict):
        return {"raw": item}

    if "ЮЛ" in item and isinstance(item["ЮЛ"], dict):
        return _flatten_legal_entity(item["ЮЛ"])
    if "ИП" in item and isinstance(item["ИП"], dict):
        return _flatten_sole_proprietor(item["ИП"])

    return {
        "inn": item.get("ИНН") or item.get("ИННФЛ"),
        "ogrn": item.get("ОГРН") or item.get("ОГРНИП"),
        "name": item.get("НаимСокрЮЛ") or item.get("НаимПолнЮЛ"),
        "status": item.get("Статус"),
    }


# ---------------------------------------------------------------------------
# Resource
# ---------------------------------------------------------------------------


@mcp.resource("egrul://identifier-guide")
def identifier_guide() -> str:
    """Справка по форматам ИНН и ОГРН — полезно для LLM при объяснении пользователю."""
    return (
        "# Идентификаторы российских организаций\n\n"
        "## ИНН (Идентификационный номер налогоплательщика)\n"
        "- **10 цифр** — для юридических лиц (ЮЛ).\n"
        "- **12 цифр** — для физлиц и индивидуальных предпринимателей (ИП).\n"
        "- Последняя цифра (для ЮЛ) или последние две (для ФЛ/ИП) — контрольные.\n"
        "- Tool `validate_identifier` проверяет корректность локально.\n\n"
        "## ОГРН/ОГРНИП (Основной государственный регистрационный номер)\n"
        "- **13 цифр** — ОГРН для ЮЛ. Первая цифра — признак записи (1 — основная, 2 — измененная).\n"
        "- **15 цифр** — ОГРНИП для ИП. Первая цифра — 3 или 4.\n"
        "- Последняя цифра — контрольная.\n\n"
        "## КПП (Код причины постановки на учёт)\n"
        "- 9 цифр.\n"
        "- Только у ЮЛ. У одной компании может быть несколько КПП "
        "(для разных филиалов / по разным основаниям).\n"
        "- ИНН + КПП однозначно идентифицируют филиал.\n\n"
        "## Статусы в ЕГРЮЛ\n"
        "- `Действующее` — активная компания.\n"
        "- `Ликвидировано по 129-ФЗ` — принудительно ликвидирована ФНС.\n"
        "- `Ликвидировано по решению учредителей` — добровольная ликвидация.\n"
        "- `В стадии ликвидации` — в процессе.\n"
        "- `Реорганизация` — слияние / разделение / преобразование.\n"
        "- `Несостоятельность (банкротство)` — в процессе банкротства.\n\n"
        "## Red flags при проверке контрагента\n"
        "- Статус не `Действующее`.\n"
        "- Регистрация менее 6 месяцев назад + значительная сделка.\n"
        "- Частая смена руководителя (3+ раза за 2 года).\n"
        "- Массовый адрес регистрации (адрес у 100+ компаний).\n"
        "- Номинальный руководитель (тот же ФИО у 10+ компаний).\n"
        "- Уставной капитал минимально-возможный (10 000 руб) при больших оборотах.\n"
    )


def main() -> None:
    """Entry point для CLI запуска: uvx egrul-mcp."""
    logger.info("Starting egrul-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
