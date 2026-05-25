"""Basic unit tests для efrsb-mcp."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from efrsb_mcp.server import (
    EFRSB_API_BASE,
    _normalize_company_bankruptcy,
    check_company_bankruptcy,
    check_person_bankruptcy,
)


@pytest.mark.asyncio
async def test_check_company_requires_criteria():
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError, match="хотя бы один"):
        await check_company_bankruptcy.fn()


@pytest.mark.asyncio
@respx.mock
async def test_check_company_not_found():
    respx.get(f"{EFRSB_API_BASE}/companies").mock(
        return_value=Response(200, json={"pageData": []})
    )
    result = await check_company_bankruptcy.fn(inn="7707000999")
    assert result["status"] == "not_found"


@pytest.mark.asyncio
@respx.mock
async def test_check_company_in_bankruptcy():
    fake_response = {
        "pageData": [
            {
                "id": "abc123",
                "name": "ООО Тест",
                "inn": "7707000001",
                "ogrn": "1027707000001",
                "bankruptCases": [
                    {
                        "id": "case-xyz",
                        "caseNumber": "A40-99999/2024",
                        "courtName": "АС города Москвы",
                        "statusName": "Конкурсное производство",
                        "startDate": "2024-03-15",
                        "arbitrManager": {
                            "fullName": "Иванов И.И.",
                            "inn": "770700000099",
                        },
                    }
                ],
            }
        ]
    }
    respx.get(f"{EFRSB_API_BASE}/companies").mock(return_value=Response(200, json=fake_response))

    result = await check_company_bankruptcy.fn(inn="7707000001")
    assert result["status"] == "in_bankruptcy"
    assert result["stage"] == "liquidation"
    assert result["stage_ru"] == "Конкурсное производство"
    assert result["case_number"] == "A40-99999/2024"
    assert result["arbitration_manager"] == "Иванов И.И."


@pytest.mark.asyncio
@respx.mock
async def test_check_company_no_bankruptcy():
    fake_response = {
        "pageData": [
            {
                "id": "ok-123",
                "name": "ООО Здоровый",
                "inn": "7707000050",
                "ogrn": "1027707000050",
                "bankruptCases": [],
            }
        ]
    }
    respx.get(f"{EFRSB_API_BASE}/companies").mock(return_value=Response(200, json=fake_response))

    result = await check_company_bankruptcy.fn(inn="7707000050")
    assert result["status"] == "no_bankruptcy"


def test_normalize_handles_invalid_shape():
    result = _normalize_company_bankruptcy("not a dict")  # type: ignore[arg-type]
    assert result["status"] == "unknown"


@pytest.mark.asyncio
async def test_check_person_requires_criteria():
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError):
        await check_person_bankruptcy.fn()
