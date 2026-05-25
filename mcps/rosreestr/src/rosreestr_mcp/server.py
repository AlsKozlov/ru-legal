"""MCP server для Росреестр / ЕГРН (Единый государственный реестр недвижимости).

Tools:
- search_object_by_cadastre — поиск по кадастровому номеру (наиболее точно)
- search_object_by_address — поиск по адресу
- get_object_details — карточка объекта (площадь, назначение, права, обременения)
- get_cadastre_value — кадастровая стоимость
- get_encumbrances — обременения объекта

Sources:
- pkk.rosreestr.ru (Публичная кадастровая карта) — публичный JSON API
- rosreestr.gov.ru — основной портал

**Important:** Полная выписка из ЕГРН (с правами + обременениями) — платная
услуга через Росреестр / Госуслуги (290-460 руб за выписку). Этот MCP provides
доступ к publicly available data (cadastre map + базовая инфо). Для полной
DD — заказать выписку через Росреестр.
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
logger = logging.getLogger("rosreestr-mcp")

PKK_BASE = "https://pkk.rosreestr.ru/api"
ROSREESTR_BASE = "https://rosreestr.gov.ru"

REQUEST_TIMEOUT_S = 30.0
MAX_CONCURRENT_REQUESTS = 3

mcp = FastMCP(
    name="rosreestr",
    instructions=(
        "Поиск и проверка объектов недвижимости через Публичную кадастровую карту "
        "(pkk.rosreestr.ru). Cadastre данные доступны бесплатно; полные ЕГРН "
        "выписки с правами + обременениями — заказывать через rosreestr.gov.ru или "
        "Госуслуги (платная услуга 290-460 руб). Используй для real estate DD."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None
_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_S = 3600.0  # cadastre data меняется медленно
_CACHE_MAX_ENTRIES = 500


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": "rosreestr-mcp/0.1.0",
                "Accept": "application/json",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Referer": "https://pkk.rosreestr.ru/",
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


async def _api_get(url: str, params: dict[str, Any] | None = None) -> Any:
    cache_key = f"GET {url} {json.dumps(params or {}, sort_keys=True, default=str)}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    client = _get_http_client()
    async with _get_semaphore():
        try:
            resp = await client.get(url, params=params)
        except httpx.TimeoutException as e:
            raise ToolError(f"Росреестр timed out за {REQUEST_TIMEOUT_S}s.") from e
        except httpx.RequestError as e:
            raise ToolError(f"Не удалось связаться с Росреестром: {e}") from e

    if resp.status_code == 404:
        raise ToolError("Объект не найден в ЕГРН.")
    if resp.status_code >= 500:
        raise ToolError(
            f"Росреестр вернул ошибку сервера (HTTP {resp.status_code}). "
            "pkk.rosreestr.ru periodically experiences outages."
        )
    if resp.status_code >= 400:
        logger.warning("HTTP %d from %s: %s", resp.status_code, url, resp.text[:500])
        raise ToolError(f"Ошибка запроса к Росреестру (HTTP {resp.status_code}).")

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError("Росреестр вернул не-JSON ответ. Источник may be degraded.") from e

    _cache_set(cache_key, data)
    return data


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_object_by_cadastre(
    cadastre_number: Annotated[
        str,
        Field(
            description=(
                "Кадастровый номер в формате 'XX:YY:ZZZZZZZ:NN' "
                "(район:квартал:объект:дополнительный). "
                "Например '77:01:0001017:1234' (Москва, ЦАО)."
            ),
            pattern=r"^\d{1,2}:\d{1,2}:\d{1,7}:\d{1,5}$",
            max_length=30,
        ),
    ],
) -> dict[str, Any]:
    """Поиск объекта по кадастровому номеру в Публичной кадастровой карте.

    Returns:
        cadastre_number, type (parcel / building / room / etc.), address,
        area, cadastre_value, purpose (назначение), encumbrances (basic),
        geographic coordinates.
    """
    logger.info("search_object_by_cadastre %s", cadastre_number)
    # PKK API uses query parameter format
    data = await _api_get(
        f"{PKK_BASE}/features/1",  # 1 = parcels; 5 = buildings; 6 = rooms
        params={"text": cadastre_number, "limit": 1, "tolerance": 1},
    )

    features = data.get("features") if isinstance(data, dict) else None
    if not features or not isinstance(features, list):
        # Try buildings (type 5)
        data = await _api_get(
            f"{PKK_BASE}/features/5",
            params={"text": cadastre_number, "limit": 1, "tolerance": 1},
        )
        features = data.get("features") if isinstance(data, dict) else None

    if not features or not isinstance(features, list):
        raise ToolError(f"Объект с кадастровым номером {cadastre_number} не найден.")

    return _normalize_object(features[0])


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_object_by_address(
    address: Annotated[
        str,
        Field(
            description=(
                "Адрес объекта в свободной форме. Lower precision чем cadastre number — "
                "может вернуть multiple matches или nothing. "
                "Лучше работает для крупных городов."
            ),
            min_length=5,
            max_length=300,
        ),
    ],
    limit: Annotated[
        int,
        Field(description="Максимум результатов.", ge=1, le=20),
    ] = 5,
) -> list[dict[str, Any]]:
    """Поиск объектов по адресу.

    **Note:** PKK address search — limited precision. Для точного DD получи
    кадастровый номер из выписки ЕГРН и потом используй search_object_by_cadastre.
    """
    logger.info("search_object_by_address %r", address)

    # PKK doesn't have direct address search; fallback к Google-style approach
    # In production — use Rosreestr search service / commercial geocoder
    data = await _api_get(
        f"{PKK_BASE}/features/1",
        params={"text": address, "limit": limit, "tolerance": 100},
    )

    features = data.get("features") if isinstance(data, dict) else None
    if not features or not isinstance(features, list):
        return []

    return [_normalize_object(f) for f in features[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_object_details(
    cadastre_number: Annotated[
        str,
        Field(
            description="Кадастровый номер объекта.",
            pattern=r"^\d{1,2}:\d{1,2}:\d{1,7}:\d{1,5}$",
            max_length=30,
        ),
    ],
) -> dict[str, Any]:
    """Детальная карточка объекта.

    Returns full details + reminder что для полной информации о правах + обременениях
    нужна выписка из ЕГРН (платная через rosreestr.gov.ru / Госуслуги).
    """
    result = await search_object_by_cadastre.fn(cadastre_number=cadastre_number)

    result["_note"] = (
        "Текущая информация — из Публичной кадастровой карты. "
        "Для полной DD — заказать выписку из ЕГРН через rosreestr.gov.ru "
        "или Госуслуги (290-460 руб; electronic — 5-7 раб.дней)."
    )
    result["egrn_request_url"] = (
        f"{ROSREESTR_BASE}/wps/portal/p/cc_present/EGRN_2"
    )
    return result


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_cadastre_value(
    cadastre_number: Annotated[
        str,
        Field(
            description="Кадастровый номер для получения cadastre стоимости.",
            pattern=r"^\d{1,2}:\d{1,2}:\d{1,7}:\d{1,5}$",
            max_length=30,
        ),
    ],
) -> dict[str, Any]:
    """Получает кадастровую стоимость объекта.

    Returns:
        cadastre_number, current_value, date_determined, can_be_challenged,
        challenge_url, tax_implications (рассчитанный налог на имущество для физ.лиц).

    Use cases:
    - Tax planning: налог на имущество = % от кадастровой стоимости (0.1-0.5% обычно)
    - Pre-purchase: kadastr value vs market value (для НДФЛ при продаже через 5 лет)
    - Challenge worthy?: если cadastre значительно > рыночной — оспаривание выгодно
    """
    object_data = await search_object_by_cadastre.fn(cadastre_number=cadastre_number)
    value = object_data.get("cadastre_value")
    if value is None:
        return {
            "cadastre_number": cadastre_number,
            "current_value": None,
            "_note": "Кадастровая стоимость не указана. Может быть в процессе определения.",
        }

    # Standard physical person property tax rates per НК
    type_obj = object_data.get("type", "").lower()
    if "квартир" in type_obj or "комнат" in type_obj or "жил" in type_obj:
        tax_rate = 0.001  # 0.1% жилые
    elif "торгов" in type_obj or "офис" in type_obj:
        tax_rate = 0.02  # 2% коммерческие
    else:
        tax_rate = 0.005  # default 0.5%

    return {
        "cadastre_number": cadastre_number,
        "current_value_rub": value,
        "date_determined": object_data.get("cadastre_value_date"),
        "can_be_challenged": True,
        "challenge_url": (
            "https://rosreestr.gov.ru/services/zaprosy/raspolozhenie-uchastka/"
            "rassmotrenie-sporov-o-rezultatah-opredeleniya-kadastrovoy-stoimosti/"
        ),
        "estimated_annual_property_tax_rub": int(value * tax_rate),
        "tax_rate_used": tax_rate,
        "_note": (
            "Налог рассчитан по типичной ставке для типа объекта. Конкретная ставка "
            "может варьироваться в зависимости от региона и стоимости. См. ст.406 НК."
        ),
    }


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_encumbrances(
    cadastre_number: Annotated[
        str,
        Field(
            description="Кадастровый номер для проверки обременений.",
            pattern=r"^\d{1,2}:\d{1,2}:\d{1,7}:\d{1,5}$",
            max_length=30,
        ),
    ],
) -> dict[str, Any]:
    """Проверка обременений объекта (ипотека, аренда зарегистрированная, арест, сервитут).

    **Important:** PKK API возвращает только базовые сведения. Для полной информации
    об обременениях — обязательно заказывать выписку из ЕГРН.

    Returns:
        - has_basic_encumbrances: Y/N — basic indicator
        - encumbrance_types: list of types найденных
        - egrn_extract_recommended: bool — recommendation
        - egrn_request_url
    """
    object_data = await search_object_by_cadastre.fn(cadastre_number=cadastre_number)

    encumbrances_basic = object_data.get("encumbrances_basic")

    return {
        "cadastre_number": cadastre_number,
        "has_basic_encumbrances": bool(encumbrances_basic),
        "encumbrance_types": encumbrances_basic or [],
        "egrn_extract_strongly_recommended": True,
        "egrn_request_url": f"{ROSREESTR_BASE}/wps/portal/p/cc_present/EGRN_2",
        "_note": (
            "Public кадастровая карта показывает limited info. Для material сделок "
            "ВСЕГДА запрашивай выписку из ЕГРН — это единственный authoritative source. "
            "Стандартная выписка — 290 руб electronic, до 460 руб с печатью."
        ),
    }


# ----------------------------------------------------------------------------
# Normalizers
# ----------------------------------------------------------------------------

# Map PKK type codes к human-readable.
_OBJECT_TYPES = {
    "1": "Земельный участок",
    "5": "Здание",
    "6": "Помещение (комната / квартира)",
    "7": "Сооружение",
    "8": "Объект незавершённого строительства",
    "9": "Машино-место",
}


def _normalize_object(feature: dict[str, Any]) -> dict[str, Any]:
    """Normalize PKK feature к стабильной форме."""
    if not isinstance(feature, dict):
        return {"raw": feature}

    attrs = feature.get("attrs") if isinstance(feature.get("attrs"), dict) else {}

    cn = attrs.get("cn") or feature.get("attrs", {}).get("cn")
    type_code = str(feature.get("type", ""))

    return {
        "cadastre_number": cn,
        "type": _OBJECT_TYPES.get(type_code, type_code or "unknown"),
        "type_code": type_code,
        "address": attrs.get("address") or attrs.get("adress"),
        "area_sq_m": _to_float(attrs.get("area_value")),
        "area_unit": attrs.get("area_unit", "м²"),
        "purpose": attrs.get("util_by_doc") or attrs.get("purpose"),
        "cadastre_value": _to_float(attrs.get("cad_cost")),
        "cadastre_value_date": attrs.get("date_cost"),
        "registration_date": attrs.get("date_create"),
        "status": attrs.get("statecd"),  # actuality of record
        "encumbrances_basic": attrs.get("encumbrances"),  # PKK may show flag only
        "owner_type": attrs.get("ownership_type"),
        "coordinates": _extract_center_coord(feature),
        "url_pkk": (
            f"https://pkk.rosreestr.ru/#/search?cadNumber={cn}" if cn else None
        ),
    }


def _extract_center_coord(feature: dict[str, Any]) -> dict[str, float] | None:
    center = feature.get("center")
    if isinstance(center, dict) and "x" in center and "y" in center:
        # PKK uses EPSG:3857 (Web Mercator); transform crude approximation
        return {"x": center["x"], "y": center["y"], "crs": "EPSG:3857"}
    extent = feature.get("extent")
    if isinstance(extent, dict):
        xmin = extent.get("xmin")
        ymin = extent.get("ymin")
        xmax = extent.get("xmax")
        ymax = extent.get("ymax")
        if all(v is not None for v in (xmin, ymin, xmax, ymax)):
            return {
                "x": (xmin + xmax) / 2,
                "y": (ymin + ymax) / 2,
                "crs": "EPSG:3857",
            }
    return None


def _to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@mcp.resource("rosreestr://egrn-cheatsheet")
def egrn_cheatsheet() -> str:
    return (
        "# ЕГРН + Кадастровая выписка — гайд\n\n"
        "## Что бесплатно (PKK / этот MCP)\n\n"
        "- Поиск объекта по кадастровому номеру\n"
        "- Базовая информация: тип, адрес, площадь\n"
        "- Кадастровая стоимость\n"
        "- Геокоординаты\n\n"
        "## Что нужно заказывать (выписка ЕГРН)\n\n"
        "- **Полные сведения о правах** (текущий собственник + history)\n"
        "- **Подробные обременения** (ипотека с реквизитами банка; аренда; арест)\n"
        "- **Переходы прав** (история сделок)\n"
        "- **Подтверждение для нотариальных сделок**\n\n"
        "## Типы выписок\n\n"
        "| Тип | Стоимость electronic | Назначение |\n"
        "|-----|----------------------|------------|\n"
        "| Об основных характеристиках + правах | 290 руб | Standard для DD сделок |\n"
        "| О переходе прав | 290 руб | History сделок |\n"
        "| О кадастровой стоимости | бесплатно через Госуслуги | Для оспаривания налога |\n"
        "| Об обременениях | 290 руб | Focus на encumbrances |\n"
        "| Расширенная (для нотариусов) | 460 руб | Полная инфо |\n\n"
        "## Где заказать\n\n"
        "- **rosreestr.gov.ru** — портал Росреестра\n"
        "- **Госуслуги** (gosuslugi.ru) — для физ.лиц проще\n"
        "- **МФЦ** — paper версия с печатью (если нужно)\n\n"
        "## Срок изготовления\n\n"
        "- Electronic — обычно **5-7 рабочих дней**\n"
        "- Paper в МФЦ — до 5 раб.дней\n"
        "- Срочная (3 раб.дня) — доступна для определённых типов с premium\n\n"
        "## DD recommendation\n\n"
        "Перед material real estate сделкой — **обязательно** заказать выписку ЕГРН **за <30 дней до сделки**. "
        "Старая выписка не показывает recent обременения / переходы.\n"
    )


def main() -> None:
    """Entry point для CLI (rosreestr-mcp)."""
    logger.info("Starting rosreestr-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
