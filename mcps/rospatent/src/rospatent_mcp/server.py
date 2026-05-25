"""MCP server для Роспатент / ФИПС реестров (https://www1.fips.ru).

Tools:
- search_trademark — поиск товарных знаков
- get_trademark — детальная карточка ТЗ
- search_patent — поиск изобретений / полезных моделей / промобразцов
- get_patent — карточка патента
- search_software — поиск зарегистрированных программ для ЭВМ / БД
- check_patent_attorney — статус патентного поверенного

Sources:
- Открытые реестры ФИПС (fips.ru/registers-web/)
- Public search endpoints (без API ключа в большинстве случаев)

Note: ФИПС публичные search interfaces — HTML-based с JSON XHR на back-end.
Endpoints периодически меняются; этот MCP wrapping common stable interfaces.
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
logger = logging.getLogger("rospatent-mcp")

FIPS_BASE = "https://www1.fips.ru"
ROSPATENT_BASE = "https://rospatent.gov.ru"
SEARCH_API_BASE = f"{FIPS_BASE}/registers-web/api"

REQUEST_TIMEOUT_S = 30.0
MAX_CONCURRENT_REQUESTS = 5

mcp = FastMCP(
    name="rospatent",
    instructions=(
        "Поиск и проверка объектов IP в реестрах Роспатент / ФИПС — товарные "
        "знаки, патенты на изобретения / полезные модели / промобразцы, программы "
        "для ЭВМ и БД. Используй для clearance проверки перед регистрацией, FTO "
        "анализа, infringement triage, IP DD."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None

_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_S = 3600.0  # IP registry — обновляется не чаще раза в сутки
_CACHE_MAX_ENTRIES = 500


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": "rospatent-mcp/0.1.0",
                "Accept": "application/json",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Referer": "https://www1.fips.ru/",
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
        _cache.pop(next(iter(_cache)), None)
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
            raise ToolError(f"ФИПС timed out за {REQUEST_TIMEOUT_S}s.") from e
        except httpx.RequestError as e:
            raise ToolError(f"Не удалось связаться с ФИПС: {e}") from e

    if resp.status_code == 404:
        raise ToolError("Объект не найден в реестре ФИПС.")
    if resp.status_code >= 500:
        raise ToolError(f"ФИПС вернул ошибку сервера (HTTP {resp.status_code}).")
    if resp.status_code >= 400:
        logger.warning("HTTP %d from %s: %s", resp.status_code, url, resp.text[:500])
        raise ToolError(f"Ошибка запроса к ФИПС (HTTP {resp.status_code}).")

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError("ФИПС вернул не-JSON ответ. Источник может быть в degraded mode.") from e

    _cache_set(cache_key, data)
    return data


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_trademark(
    query: Annotated[
        str,
        Field(
            description=(
                "Поисковая строка — текст ТЗ (для словесных), название или его часть, "
                "регистрационный номер. Для изображений — нужны специализированные services."
            ),
            min_length=2,
            max_length=300,
        ),
    ],
    classes_mktu: Annotated[
        list[int] | None,
        Field(
            description=(
                "Классы МКТУ (Ниццкая классификация) для filter — 1-45. "
                "Например [9, 42] для IT-категорий, [25] для одежды."
            ),
        ),
    ] = None,
    holder_inn: Annotated[
        str | None,
        Field(
            description="ИНН правообладателя (10 цифр для ЮЛ, 12 для ИП).",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    status: Annotated[
        str | None,
        Field(
            description="Статус ТЗ: 'active' / 'expired' / 'pending' / 'all' (default).",
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум результатов.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Поиск товарных знаков в реестре Роспатент.

    Use cases:
    - **Clearance** перед регистрацией — найти conflicting marks
    - **DD** — список ТЗ компании-target
    - **Infringement check** — verify mark наших конкурентов
    - **Portfolio audit** — все наши active ТЗ
    """
    logger.info("search_trademark query=%r classes=%s holder=%s limit=%d",
                query, classes_mktu, holder_inn, limit)

    params: dict[str, Any] = {
        "query": query,
        "limit": limit,
        "type": "trademark",
    }
    if classes_mktu:
        params["classes"] = ",".join(str(c) for c in classes_mktu)
    if holder_inn:
        params["holderInn"] = holder_inn
    if status:
        params["status"] = status

    data = await _api_request("GET", f"{SEARCH_API_BASE}/trademarks/search", params=params)

    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        logger.warning("Unexpected shape from /trademarks/search")
        return []

    return [_normalize_trademark(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_trademark(
    registration_number: Annotated[
        str,
        Field(
            description="Регистрационный номер ТЗ в Роспатент (6 цифр обычно).",
            pattern=r"^\d{4,8}$",
        ),
    ],
) -> dict[str, Any]:
    """Получает детальную карточку ТЗ — полные классы МКТУ, история, правообладатель.

    Returns:
        registration_number, mark_image_url, holder, address, classes_mktu (full),
        priority_date, registration_date, expiry_date, status, changes_history.
    """
    logger.info("get_trademark reg_num=%s", registration_number)
    data = await _api_request("GET", f"{SEARCH_API_BASE}/trademarks/{registration_number}")
    if not isinstance(data, dict):
        raise ToolError("Не удалось разобрать карточку ТЗ.")
    return _normalize_trademark_full(data)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_patent(
    query: Annotated[
        str | None,
        Field(
            description="Поисковая строка по названию / реферату / ключевым словам.",
            min_length=3,
            max_length=500,
        ),
    ] = None,
    patent_type: Annotated[
        str,
        Field(
            description=(
                "Тип патента: 'invention' (изобретение), 'utility_model' (полезная модель), "
                "'industrial_design' (промобразец)."
            ),
        ),
    ] = "invention",
    applicant_inn: Annotated[
        str | None,
        Field(
            description="ИНН патентообладателя.",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    inventor: Annotated[
        str | None,
        Field(
            description="ФИО автора / изобретателя.",
            max_length=200,
        ),
    ] = None,
    ipc_class: Annotated[
        str | None,
        Field(
            description=(
                "Класс МПК (Международная патентная классификация) — например 'G06F' "
                "(вычислительные системы), 'A61K' (фармацевтика)."
            ),
            max_length=20,
        ),
    ] = None,
    date_from: Annotated[
        str | None,
        Field(
            description="Дата приоритета не ранее (YYYY-MM-DD).",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум результатов.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Поиск патентов в реестре Роспатент.

    Use cases:
    - **FTO triage** — найти конкурирующие patents
    - **Patentability search** — prior art
    - **DD target** — patent portfolio assessment
    - **Tracking** конкурентов / inventors
    """
    if not any([query, applicant_inn, inventor, ipc_class]):
        raise ToolError("Нужен хотя бы один критерий: query / applicant_inn / inventor / ipc_class.")

    logger.info("search_patent type=%s query=%r applicant=%s limit=%d",
                patent_type, query, applicant_inn, limit)

    params: dict[str, Any] = {"type": patent_type, "limit": limit}
    if query:
        params["query"] = query
    if applicant_inn:
        params["applicantInn"] = applicant_inn
    if inventor:
        params["inventor"] = inventor
    if ipc_class:
        params["ipc"] = ipc_class
    if date_from:
        params["dateFrom"] = date_from

    data = await _api_request("GET", f"{SEARCH_API_BASE}/patents/search", params=params)
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []
    return [_normalize_patent(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_patent(
    patent_number: Annotated[
        str,
        Field(
            description="Номер патента (например '2700123' для изобретения).",
            pattern=r"^\d{4,8}$",
        ),
    ],
    patent_type: Annotated[
        str,
        Field(
            description="Тип: 'invention' / 'utility_model' / 'industrial_design'.",
        ),
    ] = "invention",
) -> dict[str, Any]:
    """Детальная карточка патента: формула, описание, чертежи (если есть).

    Returns claims (claims!), abstract, drawings_url, full_text_url, citations.
    """
    logger.info("get_patent number=%s type=%s", patent_number, patent_type)
    data = await _api_request(
        "GET",
        f"{SEARCH_API_BASE}/patents/{patent_type}/{patent_number}",
    )
    if not isinstance(data, dict):
        raise ToolError("Не удалось разобрать карточку патента.")
    return _normalize_patent_full(data)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_software(
    query: Annotated[
        str,
        Field(description="Название / часть названия ПО или БД.", min_length=3, max_length=300),
    ],
    sw_type: Annotated[
        str,
        Field(
            description="Тип: 'software' (программа для ЭВМ) / 'database' (БД) / 'all'.",
        ),
    ] = "all",
    holder_inn: Annotated[
        str | None,
        Field(
            description="ИНН правообладателя.",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум результатов.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Поиск зарегистрированных программ для ЭВМ / БД в Роспатент.

    Use case: проверка регистрации нашего ПО, IT-аккредитация check, DD ПО target.
    """
    logger.info("search_software query=%r type=%s limit=%d", query, sw_type, limit)
    params: dict[str, Any] = {"query": query, "limit": limit}
    if sw_type != "all":
        params["type"] = sw_type
    if holder_inn:
        params["holderInn"] = holder_inn

    data = await _api_request("GET", f"{SEARCH_API_BASE}/software/search", params=params)
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []
    return [_normalize_software(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def check_patent_attorney(
    full_name: Annotated[
        str | None,
        Field(description="ФИО патентного поверенного.", min_length=5, max_length=200),
    ] = None,
    registration_number: Annotated[
        str | None,
        Field(description="Регистрационный номер в реестре патентных поверенных.", max_length=10),
    ] = None,
) -> dict[str, Any]:
    """Verification статуса патентного поверенного в реестре Роспатент.

    Critical при engagement патентного поверенного для filing — verify лицензию + активность.
    Для иностранных заявителей (ст.1247 ГК) — патентный поверенный обязателен.
    """
    if not any([full_name, registration_number]):
        raise ToolError("Нужен ФИО или регистрационный номер.")

    params: dict[str, Any] = {}
    if registration_number:
        params["regNum"] = registration_number
    if full_name:
        params["fullName"] = full_name

    data = await _api_request(
        "GET",
        f"{SEARCH_API_BASE}/patentAttorneys/search",
        params=params,
    )

    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return {"status": "not_found", "query": full_name or registration_number}

    return _normalize_patent_attorney(items[0])


# ----------------------------------------------------------------------------
# Normalizers
# ----------------------------------------------------------------------------

def _normalize_trademark(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    reg_num = item.get("registrationNumber") or item.get("number")
    return {
        "registration_number": reg_num,
        "mark_text": item.get("markText") or item.get("text"),
        "mark_type": item.get("markType") or item.get("type"),
        "holder": _safe_dict_field(item.get("holder"), "name") or item.get("holderName"),
        "holder_inn": _safe_dict_field(item.get("holder"), "inn"),
        "classes_mktu": item.get("classesMktu") or item.get("classes"),
        "priority_date": item.get("priorityDate"),
        "registration_date": item.get("registrationDate"),
        "expiry_date": item.get("expiryDate"),
        "status": item.get("status"),
        "url": f"{FIPS_BASE}/registers-web/action?registerSelected=tm&number={reg_num}" if reg_num else None,
    }


def _normalize_trademark_full(item: dict[str, Any]) -> dict[str, Any]:
    base = _normalize_trademark(item)
    base.update(
        {
            "mark_image_url": item.get("imageUrl"),
            "address": _safe_dict_field(item.get("holder"), "address"),
            "representative": _safe_dict_field(item.get("representative"), "fullName"),
            "classes_mktu_detail": item.get("classesMktuDetail"),
            "changes_history": item.get("changesHistory"),
            "oppositions": item.get("oppositions"),
        }
    )
    return {k: v for k, v in base.items() if v is not None}


def _normalize_patent(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    patent_num = item.get("patentNumber") or item.get("number")
    patent_type = item.get("type")
    return {
        "patent_number": patent_num,
        "type": patent_type,
        "title": item.get("title") or item.get("name"),
        "applicant": _safe_dict_field(item.get("applicant"), "name") or item.get("applicantName"),
        "applicant_inn": _safe_dict_field(item.get("applicant"), "inn"),
        "inventors": item.get("inventors"),
        "ipc": item.get("ipc") or item.get("classification"),
        "application_number": item.get("applicationNumber"),
        "application_date": item.get("applicationDate"),
        "priority_date": item.get("priorityDate"),
        "publication_date": item.get("publicationDate"),
        "expiry_date": item.get("expiryDate"),
        "status": item.get("status"),
        "url": (
            f"{FIPS_BASE}/registers-web/action?registerSelected={patent_type or 'invent'}&number={patent_num}"
            if patent_num
            else None
        ),
    }


def _normalize_patent_full(item: dict[str, Any]) -> dict[str, Any]:
    base = _normalize_patent(item)
    base.update(
        {
            "abstract": item.get("abstract") or item.get("description"),
            "claims": item.get("claims") or item.get("formula"),
            "drawings_url": item.get("drawingsUrl"),
            "full_text_url": item.get("fullTextUrl"),
            "citations": item.get("citations"),
            "fees_paid": item.get("feesPaid"),  # для maintenance check
        }
    )
    return {k: v for k, v in base.items() if v is not None}


def _normalize_software(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    reg_num = item.get("registrationNumber") or item.get("number")
    return {
        "registration_number": reg_num,
        "name": item.get("name") or item.get("title"),
        "type": item.get("type"),  # software / database
        "holder": _safe_dict_field(item.get("holder"), "name") or item.get("holderName"),
        "holder_inn": _safe_dict_field(item.get("holder"), "inn"),
        "authors": item.get("authors"),
        "registration_date": item.get("registrationDate"),
        "url": f"{FIPS_BASE}/registers-web/action?registerSelected=evm&number={reg_num}" if reg_num else None,
    }


def _normalize_patent_attorney(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"status": "unknown"}
    return {
        "status": "active" if item.get("isActive", True) else "inactive",
        "registration_number": item.get("registrationNumber") or item.get("regNum"),
        "full_name": item.get("fullName"),
        "specialization": item.get("specialization"),
        "languages": item.get("languages"),
        "phone": item.get("phone"),
        "email": item.get("email"),
        "city": item.get("city"),
        "registration_date": item.get("registrationDate"),
    }


def _safe_dict_field(obj: Any, field: str) -> Any:
    return obj.get(field) if isinstance(obj, dict) else None


@mcp.resource("rospatent://mktu-cheatsheet")
def mktu_cheatsheet() -> str:
    """Справка по классам МКТУ (Ниццкая классификация) — часто используемые категории."""
    return (
        "# Классы МКТУ (Ниццкая классификация — 11-я редакция)\n\n"
        "## Товары (1-34)\n\n"
        "- **3** — косметика, парфюмерия, бытовая химия\n"
        "- **5** — фарм.препараты, медицинские товары\n"
        "- **9** — компьютеры, electronics, ПО (как товар), научные приборы\n"
        "- **10** — медицинская техника, диагностика\n"
        "- **14** — ювелирные изделия, часы\n"
        "- **18** — кожа, кошельки, чемоданы\n"
        "- **20** — мебель\n"
        "- **24** — текстиль, постельное\n"
        "- **25** — **одежда, обувь, головные уборы**\n"
        "- **28** — игры, спорттовары, ёлочные украшения\n"
        "- **29** — мясо, рыба, овощи (готовые)\n"
        "- **30** — кондитерские, кофе, чай, мука, выпечка\n"
        "- **32** — пиво, безалкогольные напитки\n"
        "- **33** — алкогольные напитки (кроме пива)\n\n"
        "## Услуги (35-45)\n\n"
        "- **35** — **реклама, business management, retail** (e-commerce!)\n"
        "- **36** — финансы, страхование, недвижимость\n"
        "- **37** — строительство, ремонт, монтаж\n"
        "- **38** — телекоммуникации, broadcasting\n"
        "- **39** — транспортировка, логистика, хранение\n"
        "- **41** — образование, развлечения, спорт-events\n"
        "- **42** — **научно-технические, design, ПО (как услуга — SaaS), R&D**\n"
        "- **43** — общепит, отели, гостиницы\n"
        "- **44** — медицинские, ветеринарные, beauty услуги\n"
        "- **45** — юридические, security услуги\n\n"
        "## Common combinations для tech business\n\n"
        "- IT product (SaaS): 9 + 35 + 42\n"
        "- Marketplace: 35 + 42\n"
        "- Fintech: 9 + 36 + 42\n"
        "- Edtech: 9 + 41 + 42\n"
        "- Healthtech: 9 + 10 + 44 + 42\n"
        "- E-commerce: 35 + (product class — 25, 28, 30, etc.)\n"
    )


def main() -> None:
    """Entry point для CLI (rospatent-mcp)."""
    logger.info("Starting rospatent-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
