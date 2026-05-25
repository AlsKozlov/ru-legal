"""MCP server для pravo.gov.ru — нормативные правовые акты РФ.

Использует публичный JSON API портала официального опубликования
(publication.pravo.gov.ru), который не требует регистрации или API-ключа.

Логирование строго в stderr — stdout зарезервирован под MCP протокол.
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
logger = logging.getLogger("pravo-mcp")

# TLS на publication.pravo.gov.ru / ips.pravo.gov.ru сломан с 2026-05-21:
# handshake висит на обоих IP (95.173.157.131, 95.173.147.131). HTTP отвечает
# нормально за <200ms. Данные публичные — переключение на HTTP допустимо.
# Когда портал починит TLS — вернуть https://.
PUBLICATION_API_BASE = "http://publication.pravo.gov.ru/api"
IPS_API_BASE = "http://ips.pravo.gov.ru/api/ips"

REQUEST_TIMEOUT_S = 60.0
MAX_CONCURRENT_REQUESTS = 5

# API /Documents принимает pageSize только из дискретного enum.
# Подтверждено перебором 2026-05-21 — остальные значения дают HTTP 400.
_VALID_PAGE_SIZES: tuple[int, ...] = (10, 30, 100, 200)

# ips.pravo.gov.ru требует Basic auth, hard-coded в их SPA-фронте (main.js, 2026-05).
# Без неё nginx молча таймаутит запросы. Креды публичные (зашиты в JS, который
# отдаётся всем), но имеют шанс ротации — тогда обновить из /preload/config.json.
IPS_BASIC_AUTH = ("ips", "newpassword2020")

mcp = FastMCP(
    name="pravo",
    instructions=(
        "Поиск и получение текстов нормативных правовых актов РФ с официального "
        "портала pravo.gov.ru. Используй когда нужны действующие редакции законов, "
        "указов Президента, постановлений Правительства, приказов министерств."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None

_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_S = 600.0
_CACHE_MAX_ENTRIES = 500


def _get_http_client() -> httpx.AsyncClient:
    """Singleton httpx client with connection pooling."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": "pravo-mcp/0.1.0",
                "Accept": "application/json",
            },
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
            follow_redirects=True,
        )
    return _http_client


def _get_semaphore() -> asyncio.Semaphore:
    # Lazy-init to bind to the event loop FastMCP actually runs on (Python 3.10+).
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
        # FIFO eviction — Python dict preserves insertion order since 3.7.
        oldest_key = next(iter(_cache))
        _cache.pop(oldest_key, None)
    _cache[key] = (time.monotonic(), value)


def _build_cache_key(url: str, params: dict[str, Any] | None) -> str:
    # json.dumps tolerates mixed types in params; plain sorted() would TypeError.
    serialized = json.dumps(
        sorted((params or {}).items()),
        ensure_ascii=False,
        default=str,
    )
    return f"GET {url} {serialized}"


async def _api_get(url: str, params: dict[str, Any] | None = None) -> Any:
    """Шлёт GET к pravo.gov.ru API. Обрабатывает таймауты и HTTP ошибки человекочитаемо."""
    cache_key = _build_cache_key(url, params)
    cached = _cache_get(cache_key)
    if cached is not None:
        logger.debug("cache hit: %s", cache_key)
        return cached

    # IPS-домен требует Basic auth; publication-домен — нет (его передача не вредит,
    # но не нужна). Раздаём auth только для ips.pravo.gov.ru.
    auth = IPS_BASIC_AUTH if "ips.pravo.gov.ru" in url else None

    client = _get_http_client()
    async with _get_semaphore():
        try:
            resp = await client.get(url, params=params, auth=auth)
        except httpx.TimeoutException as e:
            logger.warning("Timeout: %s", url)
            raise ToolError(
                f"pravo.gov.ru не ответил за {REQUEST_TIMEOUT_S} сек. Попробуй позже."
            ) from e
        except httpx.RequestError as e:
            logger.warning("Network error: %s: %s", url, e)
            raise ToolError(f"Не удалось связаться с pravo.gov.ru: {e}") from e

    if resp.status_code == 404:
        raise ToolError("Документ не найден на pravo.gov.ru.")
    if resp.status_code >= 500:
        raise ToolError(
            f"pravo.gov.ru вернул ошибку сервера (HTTP {resp.status_code}). "
            "Источник иногда нестабилен — попробуй позже."
        )
    if resp.status_code >= 400:
        # Не пробрасываем тело upstream-ответа в LLM-контекст — оно может содержать
        # внутренние сообщения / трассы pravo.gov.ru. В stderr для оператора пишем полностью.
        logger.warning("HTTP %d from %s: %s", resp.status_code, url, resp.text[:500])
        raise ToolError(
            f"Ошибка запроса к pravo.gov.ru (HTTP {resp.status_code}). "
            "Проверь параметры: тип документа, формат даты (YYYY-MM-DD), корректность eid."
        )

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError(
            "pravo.gov.ru вернул не-JSON ответ. Источник может быть в degraded mode."
        ) from e

    _cache_set(cache_key, data)
    return data


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_npa(
    query: Annotated[
        str,
        Field(
            description=(
                "Поисковая строка — название или фрагмент названия НПА. "
                "Примеры: 'Гражданский кодекс', 'О защите персональных данных', '152-ФЗ'."
            ),
            min_length=2,
            max_length=500,
        ),
    ],
    doc_type: Annotated[
        str | None,
        Field(
            description=(
                "Тип документа (опционально). Допустимые значения: "
                "'federal_law', 'presidential_decree', 'government_resolution', "
                "'code', 'order'. None = искать по всем типам."
            ),
        ),
    ] = None,
    date_from: Annotated[
        str | None,
        Field(
            description="Дата принятия не ранее (YYYY-MM-DD).",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    date_to: Annotated[
        str | None,
        Field(
            description="Дата принятия не позднее (YYYY-MM-DD).",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум документов в ответе.", ge=1, le=100),
    ] = 10,
) -> list[dict[str, Any]]:
    """Поиск нормативных правовых актов на portal pravo.gov.ru.

    Источник — реестр **официальных публикаций** (publication.pravo.gov.ru) с
    ~2011 года. Поэтому:
    - Хорошо: находит ФЗ по номеру ('51-ФЗ'), недавние указы Президента,
      постановления Правительства, региональные акты после 2011.
    - Плохо: НЕ содержит консолидированные действующие тексты базовых кодексов
      (ГК ч.1/1994, УК/1996, ТК/2001 и т.п.) — найдутся лишь законы,
      *вносящие изменения* в эти кодексы.
    - Для текущего текста кодекса/статьи на дату используй
      get_npa_version_at_date с хешем из ips.pravo.gov.ru, либо обратись к
      загруженным skills/packs ru-legal — они уже содержат тексты кодексов.

    Поиск подстрочный по полю name — выдача шумная (региональные постановления
    про ФЗ всплывают первыми). Чтобы отфильтровать: задавай doc_type, либо ищи
    по точному номеру акта (например '152-ФЗ').

    Возвращает список документов с метаданными. Для получения полного текста
    используй get_npa(eid) на eid каждого документа.
    """
    logger.info("search_npa query=%r type=%s limit=%d", query, doc_type, limit)

    api_page_size = next((s for s in _VALID_PAGE_SIZES if s >= limit), _VALID_PAGE_SIZES[-1])
    params: dict[str, Any] = {"name": query, "pageSize": api_page_size}
    if doc_type:
        params["documentTypes"] = doc_type
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to

    data = await _api_get(f"{PUBLICATION_API_BASE}/Documents", params=params)

    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        logger.warning("Unexpected response shape from /Documents: %s", type(data).__name__)
        return []

    return [_normalize_npa_item(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_npa(
    eid: Annotated[
        str,
        Field(
            description=(
                "Уникальный идентификатор документа на portal pravo.gov.ru "
                "(поле 'eid' из ответа search_npa)."
            ),
            min_length=1,
            max_length=200,
            # pravo.gov.ru eids — alphanumeric плюс - и _. Pattern не пускает '/' и '..',
            # предотвращая URL path traversal к произвольным endpoints.
            pattern=r"^[A-Za-z0-9_\-]+$",
        ),
    ],
) -> dict[str, Any]:
    """Получает полные метаданные и текст НПА по его eid с pravo.gov.ru.

    Используй после search_npa чтобы получить текст найденного документа.
    """
    logger.info("get_npa eid=%s", eid)
    data = await _api_get(f"{PUBLICATION_API_BASE}/Document/{eid}")
    return _normalize_npa_item(data, include_text=True)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_npa_version_at_date(
    document_hash: Annotated[
        str,
        Field(
            description=(
                "Хеш-идентификатор документа в ИПС (информационно-правовой системе) "
                "pravo.gov.ru. Получается из ips.pravo.gov.ru."
            ),
            min_length=1,
            max_length=256,
            pattern=r"^[A-Za-z0-9_\-]+$",
        ),
    ],
    on_date: Annotated[
        str | None,
        Field(
            description=(
                "Дата, на которую нужна редакция (YYYY-MM-DD). "
                "None = последняя действующая редакция."
            ),
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
) -> dict[str, Any]:
    """Получает редакцию НПА на конкретную дату через ИПС pravo.gov.ru.

    Используй когда нужно процитировать редакцию закона, действовавшую на момент
    заключения договора / возникновения спора / совершения деяния.
    """
    logger.info("get_npa_version_at_date hash=%s date=%s", document_hash, on_date)
    params: dict[str, Any] = {"hash": document_hash}
    if on_date:
        params["onDate"] = on_date
    data = await _api_get(f"{IPS_API_BASE}/legislation/document", params=params)
    return _normalize_npa_item(data, include_text=True)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def list_document_types() -> list[dict[str, str]]:
    """Возвращает справочник типов документов, доступных на pravo.gov.ru.

    Полезно для уточнения параметра doc_type в search_npa.
    """
    logger.info("list_document_types")
    data = await _api_get(f"{PUBLICATION_API_BASE}/DocumentTypes")
    items = data if isinstance(data, list) else data.get("items", [])
    return [
        {"code": str(it.get("code", "")), "name": str(it.get("name", ""))}
        for it in items
        if isinstance(it, dict)
    ]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def list_signatory_authorities(
    block: Annotated[
        str,
        Field(
            description=(
                "Категория органов: 'president' (Президент), 'government' (Правительство), "
                "'parliament' (ФС), 'ministries' (министерства), 'agencies' (агентства)."
            ),
        ),
    ],
) -> list[dict[str, str]]:
    """Справочник органов, издающих НПА.

    Полезно когда нужно найти все акты конкретного министерства / службы.
    """
    logger.info("list_signatory_authorities block=%s", block)
    data = await _api_get(
        f"{PUBLICATION_API_BASE}/SignatoryAuthorities",
        params={"block": block},
    )
    items = data if isinstance(data, list) else data.get("items", [])
    return [
        {
            "id": str(it.get("id", "")),
            "name": str(it.get("name", "")),
            "shortName": str(it.get("shortName", "")),
        }
        for it in items
        if isinstance(it, dict)
    ]


def _normalize_npa_item(item: dict[str, Any], include_text: bool = False) -> dict[str, Any]:
    """Приводит ответ pravo.gov.ru к стабильной форме для LLM."""
    if not isinstance(item, dict):
        return {"raw": item, "_warning": "unexpected response shape"}

    normalized = {
        "eid": item.get("eid") or item.get("id"),
        "name": item.get("name") or item.get("title"),
        "complexName": item.get("complexName"),
        "documentType": item.get("documentType") or item.get("type"),
        "signatoryAuthority": item.get("signatoryAuthority") or item.get("authority"),
        "documentDate": item.get("documentDate") or item.get("date"),
        "number": item.get("number"),
        "publicationUrl": _build_publication_url(item.get("eid") or item.get("id")),
    }

    if include_text:
        normalized["pdfUrl"] = item.get("pdfUrl")
        normalized["xmlUrl"] = item.get("xmlUrl")
        normalized["htmlContent"] = item.get("htmlContent") or item.get("content")

    return {k: v for k, v in normalized.items() if v is not None}


def _build_publication_url(eid: str | None) -> str | None:
    if not eid:
        return None
    return f"https://publication.pravo.gov.ru/Document/View/{eid}"


@mcp.resource("pravo://doc-types-cheatsheet")
def doc_types_cheatsheet() -> str:
    """Справка по основным типам НПА РФ — полезно для понимания иерархии."""
    return (
        "# Иерархия НПА РФ\n\n"
        "1. **Конституция РФ** (1993) — высший уровень.\n"
        "2. **Федеральные конституционные законы** (ФКЗ) — например, о Правительстве.\n"
        "3. **Кодексы** — ГК, НК, ТК, УК, ЖК и др. Имеют приоритет над обычными ФЗ в своей сфере.\n"
        "4. **Федеральные законы** (ФЗ) — например, 152-ФЗ \"О ПДн\", 44-ФЗ \"О закупках\".\n"
        "5. **Указы Президента РФ** — могут регулировать вопросы, не относящиеся к ФЗ.\n"
        "6. **Постановления Правительства РФ** — реализация ФЗ.\n"
        "7. **Приказы министерств и ведомств** — детализация постановлений.\n"
        "8. **Региональные законы** — для субъектов РФ (вне API portal pravo.gov.ru).\n"
        "9. **Муниципальные акты** — ниже всех.\n\n"
        "**Особый статус:**\n"
        "- **Постановления Пленумов ВС РФ** — обязательны для всех судов.\n"
        "- **Решения Конституционного Суда РФ** — связаны с проверкой конституционности норм.\n"
        "- **Письма Минфина / ФНС** — не НПА, но имеют разъяснительный характер.\n"
    )


def main() -> None:
    """Entry point для запуска MCP сервера через CLI (uvx pravo-mcp).

    Closing httpx client at shutdown is best-effort. FastMCP owns the event loop —
    after mcp.run() returns, the loop is closed and we cannot await aclose().
    Process exit will drop sockets cleanly enough for stdio MCP.
    """
    logger.info("Starting pravo-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
