"""Basic unit tests для zakupki-mcp."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from zakupki_mcp.server import (
    RNP_API_BASE,
    ZAKUPKI_API_BASE,
    _normalize_tender,
    check_rnp,
    search_tenders,
)


@pytest.mark.asyncio
async def test_search_tenders_requires_criteria():
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError, match="хотя бы один"):
        await search_tenders.fn()


@pytest.mark.asyncio
@respx.mock
async def test_search_tenders_basic():
    fake = {
        "items": [
            {
                "purchaseNumber": "0173100007722000123",
                "name": "Поставка офисной мебели",
                "fz": "44",
                "customer": {"name": "ФГБУ Тест", "inn": "7707000050"},
                "price": 5000000,
                "status": "active",
                "purchaseMethod": "Электронный аукцион",
                "publishDate": "2025-01-15",
            }
        ]
    }
    respx.get(f"{ZAKUPKI_API_BASE}/orders/search").mock(return_value=Response(200, json=fake))

    result = await search_tenders.fn(query="мебель")
    assert len(result) == 1
    t = result[0]
    assert t["purchase_number"] == "0173100007722000123"
    assert t["nmck"] == 5000000
    assert t["law"] == "44"


@pytest.mark.asyncio
async def test_check_rnp_requires_input():
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError):
        await check_rnp.fn()


@pytest.mark.asyncio
@respx.mock
async def test_check_rnp_clean():
    respx.get(f"{RNP_API_BASE}/search").mock(return_value=Response(200, json={"items": []}))
    result = await check_rnp.fn(inn="7707000050")
    assert result["status"] == "clean"


@pytest.mark.asyncio
@respx.mock
async def test_check_rnp_active_record():
    fake = {
        "items": [
            {
                "regNumber": "RNP-2024-12345",
                "supplierName": "ООО Нарушитель",
                "supplierInn": "7707000100",
                "fz": "44",
                "reason": "Уклонение от заключения контракта",
                "decisionAuthority": "ФАС России",
                "decisionDate": "2024-06-15",
                "includeDate": "2024-06-20",
                "endDate": "2026-06-20",  # future = active
            }
        ]
    }
    respx.get(f"{RNP_API_BASE}/search").mock(return_value=Response(200, json=fake))

    result = await check_rnp.fn(inn="7707000100")
    assert result["status"] == "in_rnp"
    assert len(result["active_records"]) == 1
    assert result["active_records"][0]["reason"] == "Уклонение от заключения контракта"


def test_normalize_tender_handles_invalid():
    assert "raw" in _normalize_tender("not a dict")  # type: ignore[arg-type]
