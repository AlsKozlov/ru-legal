"""Unit-тесты pravo-mcp server.

Используем in-memory FastMCP Client — без subprocess и без сетевых запросов.
HTTP запросы мокаются через respx.
"""

from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp import Client

import pravo_mcp.server as srv
from pravo_mcp.server import (
    IPS_API_BASE,
    PUBLICATION_API_BASE,
    _cache,
    mcp,
)


@pytest.fixture(autouse=True)
async def _isolate_state() -> None:
    """Каждый тест начинает с чистого кэша и свежего httpx-клиента.

    Singleton _http_client может пропустить respx-мок, если был создан в предыдущем тесте.
    """
    _cache.clear()
    if srv._http_client is not None:
        await srv._http_client.aclose()
        srv._http_client = None
    yield
    _cache.clear()
    if srv._http_client is not None:
        await srv._http_client.aclose()
        srv._http_client = None


@pytest.mark.asyncio
async def test_search_npa_returns_normalized_items() -> None:
    fake_response = {
        "items": [
            {
                "eid": "0001202401010001",
                "name": "О защите персональных данных",
                "documentType": "federal_law",
                "documentDate": "2006-07-27",
                "number": "152-ФЗ",
            }
        ]
    }
    with respx.mock(assert_all_called=True) as mock:
        mock.get(f"{PUBLICATION_API_BASE}/Documents").mock(
            return_value=httpx.Response(200, json=fake_response)
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "search_npa", {"query": "персональных данных", "limit": 5}
            )

    assert not result.is_error
    items = result.data
    assert len(items) == 1
    assert items[0]["eid"] == "0001202401010001"
    assert items[0]["number"] == "152-ФЗ"
    assert items[0]["publicationUrl"].startswith("https://publication.pravo.gov.ru/")


@pytest.mark.asyncio
async def test_search_npa_handles_empty_list() -> None:
    with respx.mock() as mock:
        mock.get(f"{PUBLICATION_API_BASE}/Documents").mock(
            return_value=httpx.Response(200, json={"items": []})
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "search_npa", {"query": "несуществующий закон", "limit": 10}
            )

    assert not result.is_error
    assert result.data == []


@pytest.mark.asyncio
async def test_search_npa_handles_502_gracefully() -> None:
    with respx.mock() as mock:
        mock.get(f"{PUBLICATION_API_BASE}/Documents").mock(
            return_value=httpx.Response(502, text="Bad Gateway")
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "search_npa", {"query": "ГК РФ"}, raise_on_error=False
            )

    assert result.is_error
    assert "сервера" in str(result.content[0].text).lower()


@pytest.mark.asyncio
async def test_get_npa_returns_full_document() -> None:
    fake_doc = {
        "eid": "0001202401010001",
        "name": "О защите персональных данных",
        "documentType": "federal_law",
        "pdfUrl": "https://publication.pravo.gov.ru/file/...pdf",
        "htmlContent": "<html>...</html>",
    }
    with respx.mock() as mock:
        mock.get(f"{PUBLICATION_API_BASE}/Document/0001202401010001").mock(
            return_value=httpx.Response(200, json=fake_doc)
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_npa", {"eid": "0001202401010001"}
            )

    assert not result.is_error
    doc = result.data
    assert doc["eid"] == "0001202401010001"
    assert doc["pdfUrl"].endswith(".pdf")
    assert "htmlContent" in doc


@pytest.mark.asyncio
async def test_get_npa_rejects_path_traversal() -> None:
    """eid с '/' или '..' должен отсечься на валидации Pydantic, не уйти в URL."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_npa", {"eid": "../../etc/passwd"}, raise_on_error=False
        )
    assert result.is_error

    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_npa", {"eid": "foo/bar"}, raise_on_error=False
        )
    assert result.is_error


@pytest.mark.asyncio
async def test_get_npa_handles_404() -> None:
    with respx.mock() as mock:
        mock.get(f"{PUBLICATION_API_BASE}/Document/missing").mock(
            return_value=httpx.Response(404)
        )

        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_npa", {"eid": "missing"}, raise_on_error=False
            )

    assert result.is_error
    assert "не найден" in str(result.content[0].text).lower()


@pytest.mark.asyncio
async def test_get_npa_version_at_date_passes_date_param() -> None:
    fake_doc = {"eid": "abc", "name": "ГК РФ часть первая", "documentDate": "1994-11-30"}
    with respx.mock() as mock:
        route = mock.get(f"{IPS_API_BASE}/legislation/document").mock(
            return_value=httpx.Response(200, json=fake_doc)
        )

        async with Client(mcp) as client:
            await client.call_tool(
                "get_npa_version_at_date",
                {"document_hash": "abc123", "on_date": "2024-01-01"},
            )

    assert route.called
    call = route.calls[0]
    assert call.request.url.params["hash"] == "abc123"
    assert call.request.url.params["onDate"] == "2024-01-01"


@pytest.mark.asyncio
async def test_list_document_types_normalizes_response() -> None:
    fake = [
        {"code": "FZ", "name": "Федеральный закон"},
        {"code": "PR_PRES", "name": "Указ Президента РФ"},
    ]
    with respx.mock() as mock:
        mock.get(f"{PUBLICATION_API_BASE}/DocumentTypes").mock(
            return_value=httpx.Response(200, json=fake)
        )

        async with Client(mcp) as client:
            result = await client.call_tool("list_document_types", {})

    assert not result.is_error
    types = result.data
    assert {"code": "FZ", "name": "Федеральный закон"} in types


@pytest.mark.asyncio
async def test_cache_avoids_duplicate_requests() -> None:
    fake_response = {"items": [{"eid": "x", "name": "test"}]}
    with respx.mock() as mock:
        route = mock.get(f"{PUBLICATION_API_BASE}/Documents").mock(
            return_value=httpx.Response(200, json=fake_response)
        )

        async with Client(mcp) as client:
            await client.call_tool("search_npa", {"query": "test", "limit": 5})
            await client.call_tool("search_npa", {"query": "test", "limit": 5})

    assert route.call_count == 1, "Second call must hit cache"


@pytest.mark.asyncio
async def test_resource_cheatsheet_loads() -> None:
    async with Client(mcp) as client:
        content = await client.read_resource("pravo://doc-types-cheatsheet")
        text = str(content[0].text)
        assert "Конституция РФ" in text
        assert "152-ФЗ" in text
