"""Юнит-тесты MCP server.

In-memory FastMCP Client + respx моки. Не делает реальных HTTP.
Каждый тест получает чистое состояние (без singleton'ов от предыдущих).
"""

from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp import Client

import egrul_mcp.server as srv
from egrul_mcp.server import (
    API_BASE,
    MIN_REQUEST_INTERVAL_S,
    _cache,
    mcp,
)

# Известные публичные идентификаторы Сбербанка — используем как валидные ИНН/ОГРН
SBERBANK_INN = "7707083893"
SBERBANK_OGRN = "1027700132195"
INVALID_INN = "1234567890"  # неправильная контрольная цифра


@pytest.fixture(autouse=True)
async def _isolate_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Кэш, singleton клиент, env var — всё свежее для каждого теста."""
    _cache.clear()
    if srv._http_client is not None:
        await srv._http_client.aclose()
        srv._http_client = None
    # Дефолтно ставим валидный ключ, чтобы тесты на бизнес-логику не падали на auth check.
    monkeypatch.setenv("API_FNS_KEY", "test_key_at_least_twenty_chars_long_xxx")
    # Disable rate-limit sleep в тестах — speed up
    srv._last_request_time = 0.0
    monkeypatch.setattr(srv, "MIN_REQUEST_INTERVAL_S", 0.0)
    yield
    _cache.clear()
    if srv._http_client is not None:
        await srv._http_client.aclose()
        srv._http_client = None


# ---------------------------------------------------------------------------
# validate_identifier — pure local, не должен делать HTTP
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_validate_identifier_recognizes_inn_ul() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("validate_identifier", {"value": SBERBANK_INN})
    assert not result.is_error
    assert result.data == {"valid": True, "kind": "inn-ul", "value": SBERBANK_INN}


@pytest.mark.asyncio
async def test_validate_identifier_recognizes_ogrn() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("validate_identifier", {"value": SBERBANK_OGRN})
    assert not result.is_error
    assert result.data["kind"] == "ogrn"


@pytest.mark.asyncio
async def test_validate_identifier_rejects_invalid() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("validate_identifier", {"value": INVALID_INN})
    assert not result.is_error
    assert result.data == {"valid": False, "kind": "invalid", "value": INVALID_INN}


# ---------------------------------------------------------------------------
# lookup_company
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_lookup_company_returns_flattened_legal_entity() -> None:
    fake = {
        "items": [
            {
                "ЮЛ": {
                    "ИНН": SBERBANK_INN,
                    "КПП": "773601001",
                    "ОГРН": SBERBANK_OGRN,
                    "НаимСокрЮЛ": "ПАО СБЕРБАНК",
                    "НаимПолнЮЛ": "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО",
                    "Статус": "Действующее",
                    "ДатаРег": "1991-06-20",
                    "Адрес": {"АдресПолн": "г. Москва, ул. Вавилова, 19"},
                    "ОснВидДеят": {"Код": "64.19", "Текст": "Денежное посредничество"},
                    "Руководитель": {
                        "ФИОПолн": "ГРЕФ ГЕРМАН ОСКАРОВИЧ",
                        "ИННФЛ": "770301760393",
                        "Должн": "ПРЕЗИДЕНТ",
                    },
                    "УставКап": {"СумКап": 67760844000},
                    "Учредители": [],
                }
            }
        ]
    }
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/egr").mock(return_value=httpx.Response(200, json=fake))

        async with Client(mcp) as client:
            result = await client.call_tool("lookup_company", {"identifier": SBERBANK_INN})

    assert not result.is_error
    data = result.data
    assert data["found"] is True
    assert data["type"] == "legal-entity"
    assert data["inn"] == SBERBANK_INN
    assert data["status"] == "Действующее"
    assert data["is_active"] is True
    assert data["director_name"] == "ГРЕФ ГЕРМАН ОСКАРОВИЧ"
    assert data["main_activity_code"] == "64.19"


@pytest.mark.asyncio
async def test_lookup_company_rejects_invalid_inn_locally() -> None:
    """Невалидный ИНН не должен уходить в HTTP — экономит квоту."""
    with respx.mock(assert_all_called=False) as mock:
        route = mock.get(f"{API_BASE}/egr").mock(return_value=httpx.Response(200, json={}))

        async with Client(mcp) as client:
            result = await client.call_tool(
                "lookup_company", {"identifier": INVALID_INN}, raise_on_error=False
            )

    assert result.is_error
    assert route.call_count == 0, "HTTP запрос не должен происходить для невалидного ИНН"


@pytest.mark.asyncio
async def test_lookup_company_not_found_returns_empty_marker() -> None:
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/egr").mock(
            return_value=httpx.Response(200, json={"items": []})
        )

        async with Client(mcp) as client:
            result = await client.call_tool("lookup_company", {"identifier": SBERBANK_INN})

    assert not result.is_error
    assert result.data == {"found": False, "identifier": SBERBANK_INN}


@pytest.mark.asyncio
async def test_lookup_company_handles_auth_error_string() -> None:
    """api-fns.ru возвращает auth-ошибку строкой, а не JSON-объектом."""
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/egr").mock(
            return_value=httpx.Response(200, text='"Неверный логин или пароль"')
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "lookup_company", {"identifier": SBERBANK_INN}, raise_on_error=False
            )

    assert result.is_error
    assert "ключ" in str(result.content[0].text).lower()


@pytest.mark.asyncio
async def test_lookup_company_handles_402_quota() -> None:
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/egr").mock(return_value=httpx.Response(402))

        async with Client(mcp) as client:
            result = await client.call_tool(
                "lookup_company", {"identifier": SBERBANK_INN}, raise_on_error=False
            )

    assert result.is_error
    error_text = str(result.content[0].text).lower()
    assert "402" in error_text or "квот" in error_text


# ---------------------------------------------------------------------------
# search_companies
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search_companies_returns_normalized_list() -> None:
    fake = {
        "items": [
            {
                "ЮЛ": {
                    "ИНН": SBERBANK_INN,
                    "НаимСокрЮЛ": "ПАО СБЕРБАНК",
                    "Статус": "Действующее",
                }
            },
            {
                "ЮЛ": {
                    "ИНН": "7706107510",
                    "НаимСокрЮЛ": "АО СБЕР ЛИЗИНГ",
                    "Статус": "Действующее",
                }
            },
        ]
    }
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/search").mock(return_value=httpx.Response(200, json=fake))

        async with Client(mcp) as client:
            result = await client.call_tool(
                "search_companies", {"query": "Сбер", "limit": 10}
            )

    assert not result.is_error
    items = result.data
    assert len(items) == 2
    assert items[0]["inn"] == SBERBANK_INN
    assert items[0]["name_short"] == "ПАО СБЕРБАНК"


# ---------------------------------------------------------------------------
# batch_check_problematic
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_batch_check_filters_invalid_locally() -> None:
    """Невалидные ИНН отсекаются локально, в HTTP идут только валидные."""
    captured: dict = {}

    def capture_request(request: httpx.Request) -> httpx.Response:
        captured["url"] = request.url
        return httpx.Response(200, json={"items": []})

    with respx.mock() as mock:
        mock.get(f"{API_BASE}/multcheck").mock(side_effect=capture_request)

        async with Client(mcp) as client:
            result = await client.call_tool(
                "batch_check_problematic",
                {"identifiers": [SBERBANK_INN, INVALID_INN, "abc"]},
            )

    assert not result.is_error
    data = result.data
    assert data["checked"] == 1
    assert data["invalid"] == [INVALID_INN, "abc"]
    # Только валидный ИНН должен попасть в URL
    req_param = captured["url"].params.get("req", "")
    assert SBERBANK_INN in req_param
    assert INVALID_INN not in req_param


@pytest.mark.asyncio
async def test_batch_check_all_invalid_skips_http() -> None:
    """Если все ИНН невалидны — HTTP не вызывается."""
    with respx.mock(assert_all_called=False) as mock:
        route = mock.get(f"{API_BASE}/multcheck").mock(
            return_value=httpx.Response(200, json={"items": []})
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "batch_check_problematic", {"identifiers": [INVALID_INN, "abc"]}
            )

    assert not result.is_error
    assert route.call_count == 0
    assert result.data["checked"] == 0
    assert result.data["invalid"] == [INVALID_INN, "abc"]


@pytest.mark.asyncio
async def test_batch_check_returns_problematic_entries() -> None:
    fake = {
        "items": [
            {
                "ЮЛ": {
                    "ИНН": SBERBANK_INN,
                    "НаимСокрЮЛ": "ТЕСТ",
                    "Статус": "Ликвидировано по 129-ФЗ",
                }
            }
        ]
    }
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/multcheck").mock(return_value=httpx.Response(200, json=fake))

        async with Client(mcp) as client:
            result = await client.call_tool(
                "batch_check_problematic", {"identifiers": [SBERBANK_INN]}
            )

    assert not result.is_error
    assert result.data["checked"] == 1
    assert len(result.data["problematic"]) == 1
    assert result.data["problematic"][0]["status"] == "Ликвидировано по 129-ФЗ"


# ---------------------------------------------------------------------------
# Auth: отсутствие ключа
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_missing_api_key_returns_friendly_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("API_FNS_KEY", raising=False)

    async with Client(mcp) as client:
        result = await client.call_tool(
            "lookup_company", {"identifier": SBERBANK_INN}, raise_on_error=False
        )

    assert result.is_error
    error_text = str(result.content[0].text).lower()
    assert "api_fns_key" in error_text


@pytest.mark.asyncio
async def test_short_api_key_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_FNS_KEY", "abc123")

    async with Client(mcp) as client:
        result = await client.call_tool(
            "lookup_company", {"identifier": SBERBANK_INN}, raise_on_error=False
        )

    assert result.is_error
    assert "коротк" in str(result.content[0].text).lower()


# ---------------------------------------------------------------------------
# Security: ключ не утекает в кэш-ключ и не попадает в логи
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_api_key_not_in_cache_key() -> None:
    """API ключ не должен попадать в cache key — иначе утечка через debug log."""
    fake = {"items": []}
    with respx.mock() as mock:
        mock.get(f"{API_BASE}/egr").mock(return_value=httpx.Response(200, json=fake))

        async with Client(mcp) as client:
            await client.call_tool("lookup_company", {"identifier": SBERBANK_INN})

    # Кэш должен содержать единственный ключ — проверяем, что ключа в нём нет.
    assert len(_cache) == 1
    cache_key = next(iter(_cache.keys()))
    assert "test_key_at_least_twenty_chars" not in cache_key
    assert "key" not in cache_key.lower() or "egr" in cache_key  # endpoint имя ок, но не key=


# ---------------------------------------------------------------------------
# Resource
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_resource_identifier_guide_loads() -> None:
    async with Client(mcp) as client:
        content = await client.read_resource("egrul://identifier-guide")
        text = str(content[0].text)
        assert "ИНН" in text
        assert "ОГРН" in text
        assert "Red flags" in text
