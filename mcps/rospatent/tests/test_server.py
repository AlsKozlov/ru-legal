"""Basic unit tests для rospatent-mcp."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from rospatent_mcp.server import (
    SEARCH_API_BASE,
    _normalize_patent,
    _normalize_trademark,
    check_patent_attorney,
    search_patent,
    search_trademark,
)


@pytest.mark.asyncio
@respx.mock
async def test_search_trademark_returns_normalized():
    fake = {
        "items": [
            {
                "registrationNumber": "555555",
                "markText": "АЛЬФА",
                "markType": "словесный",
                "holder": {"name": "ООО Альфа", "inn": "7707000001"},
                "classes": [35, 42],
                "priorityDate": "2020-01-15",
                "status": "active",
            }
        ]
    }
    respx.get(f"{SEARCH_API_BASE}/trademarks/search").mock(return_value=Response(200, json=fake))

    result = await search_trademark.fn(query="АЛЬФА")
    assert len(result) == 1
    tm = result[0]
    assert tm["registration_number"] == "555555"
    assert tm["mark_text"] == "АЛЬФА"
    assert tm["classes_mktu"] == [35, 42]
    assert tm["status"] == "active"


@pytest.mark.asyncio
async def test_search_patent_requires_criteria():
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError, match="хотя бы один критерий"):
        await search_patent.fn()


@pytest.mark.asyncio
@respx.mock
async def test_search_patent_basic():
    fake = {
        "items": [
            {
                "patentNumber": "2700123",
                "type": "invention",
                "title": "Способ обработки данных",
                "applicant": {"name": "ООО Технология", "inn": "7707000050"},
                "ipc": "G06F 17/00",
                "applicationDate": "2019-05-10",
                "priorityDate": "2019-05-10",
                "status": "active",
            }
        ]
    }
    respx.get(f"{SEARCH_API_BASE}/patents/search").mock(return_value=Response(200, json=fake))

    result = await search_patent.fn(query="обработка данных")
    assert len(result) == 1
    pat = result[0]
    assert pat["patent_number"] == "2700123"
    assert pat["title"] == "Способ обработки данных"
    assert pat["status"] == "active"


@pytest.mark.asyncio
async def test_check_patent_attorney_requires_input():
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError):
        await check_patent_attorney.fn()


@pytest.mark.asyncio
@respx.mock
async def test_check_patent_attorney_not_found():
    respx.get(f"{SEARCH_API_BASE}/patentAttorneys/search").mock(
        return_value=Response(200, json={"items": []})
    )
    result = await check_patent_attorney.fn(full_name="Не существующий")
    assert result["status"] == "not_found"


def test_normalize_invalid_shape():
    assert "raw" in _normalize_patent("not a dict")  # type: ignore[arg-type]
    assert "raw" in _normalize_trademark("not a dict")  # type: ignore[arg-type]
