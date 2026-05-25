"""Basic unit tests для kad-mcp server."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from kad_mcp.server import (
    KAD_API_BASE,
    _normalize_case_card,
    _normalize_case_item,
    get_case_card,
    list_courts,
    search_cases,
)


@pytest.mark.asyncio
async def test_list_courts_returns_static_reference():
    """list_courts возвращает зашитый справочник без external call."""
    result = await list_courts.fn()
    assert isinstance(result, list)
    assert len(result) > 20
    # СИП обязательно в списке (для IP-споров)
    assert any(c["id"] == "СИП" for c in result)
    # АС Москвы — самый используемый
    assert any(c["id"] == "А40" for c in result)


@pytest.mark.asyncio
async def test_search_cases_requires_criteria():
    """search_cases без критериев — должен raise ToolError."""
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError, match="хотя бы один из критериев"):
        await search_cases.fn()


@pytest.mark.asyncio
@respx.mock
async def test_search_cases_by_case_number():
    """Search по номеру дела возвращает normalized list."""
    fake_response = {
        "Result": {
            "Items": [
                {
                    "CaseNumber": "A40-12345/2025",
                    "Court": {"Name": "АС города Москвы"},
                    "Plaintiffs": [{"Name": "ООО Истец", "Inn": "7707000001"}],
                    "Respondents": [{"Name": "ООО Ответчик", "Inn": "7707000002"}],
                    "FiledDate": "2025-01-15",
                    "StageName": "Принят к производству",
                    "ClaimSum": 1500000,
                }
            ]
        }
    }
    respx.post(f"{KAD_API_BASE}/SearchInstances").mock(return_value=Response(200, json=fake_response))

    result = await search_cases.fn(case_number="A40-12345/2025")

    assert len(result) == 1
    case = result[0]
    assert case["case_number"] == "A40-12345/2025"
    assert case["court"] == "АС города Москвы"
    assert case["plaintiffs"][0]["name"] == "ООО Истец"
    assert case["sum_claim"] == 1500000
    assert "kad.arbitr.ru" in case["url"]


@pytest.mark.asyncio
@respx.mock
async def test_get_case_card_returns_full_card():
    """get_case_card возвращает полную карточку с hearings."""
    fake_response = {
        "Result": {
            "CaseNumber": "A40-12345/2025",
            "Court": {"Name": "АС города Москвы"},
            "Category": "О взыскании задолженности",
            "Plaintiffs": [{"Name": "ООО Истец", "Inn": "7707000001"}],
            "Respondents": [{"Name": "ООО Ответчик", "Inn": "7707000002"}],
            "ThirdParties": [],
            "StageName": "Назначено к рассмотрению",
            "FiledDate": "2025-01-15",
            "ClaimSum": 1500000,
            "Hearings": [
                {"Date": "2025-03-10", "Time": "10:30", "Type": "Предварительное"}
            ],
        }
    }
    respx.post(f"{KAD_API_BASE}/Card").mock(return_value=Response(200, json=fake_response))

    result = await get_case_card.fn(case_number="A40-12345/2025")

    assert result["case_number"] == "A40-12345/2025"
    assert result["category"] == "О взыскании задолженности"
    assert len(result["plaintiffs"]) == 1
    assert result["hearings"][0]["date"] == "2025-03-10"


def test_normalize_case_item_handles_missing_fields():
    """Normalizer не должен падать при partial data."""
    item = {"CaseNumber": "A40-1/2025"}
    result = _normalize_case_item(item)
    assert result["case_number"] == "A40-1/2025"
    # Missing fields should be None or absent
    assert result.get("court") is None


def test_normalize_case_card_handles_invalid_shape():
    """Normalizer для нелогичного response не падает."""
    result = _normalize_case_card({"unexpected": "shape"})
    assert "_warning" in result or "case_number" in result
