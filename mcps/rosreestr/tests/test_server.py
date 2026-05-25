"""Basic unit tests для rosreestr-mcp."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from rosreestr_mcp.server import (
    PKK_BASE,
    _normalize_object,
    get_cadastre_value,
    search_object_by_cadastre,
)


@pytest.mark.asyncio
@respx.mock
async def test_search_object_by_cadastre():
    fake = {
        "features": [
            {
                "type": "1",
                "attrs": {
                    "cn": "77:01:0001017:1234",
                    "address": "Москва, ул. Тверская, д.1",
                    "area_value": 100.5,
                    "area_unit": "м²",
                    "util_by_doc": "Для жилищного строительства",
                    "cad_cost": 15000000,
                    "date_cost": "2024-01-15",
                    "statecd": "1",  # actuality
                },
                "center": {"x": 4188000, "y": 7507000},
            }
        ]
    }
    respx.get(f"{PKK_BASE}/features/1").mock(return_value=Response(200, json=fake))

    result = await search_object_by_cadastre.fn(cadastre_number="77:01:0001017:1234")
    assert result["cadastre_number"] == "77:01:0001017:1234"
    assert result["type"] == "Земельный участок"
    assert result["area_sq_m"] == 100.5
    assert result["cadastre_value"] == 15000000
    assert result["url_pkk"] is not None


@pytest.mark.asyncio
@respx.mock
async def test_search_object_not_found_raises():
    # Both type 1 (parcel) and type 5 (building) return empty
    respx.get(f"{PKK_BASE}/features/1").mock(return_value=Response(200, json={"features": []}))
    respx.get(f"{PKK_BASE}/features/5").mock(return_value=Response(200, json={"features": []}))

    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError, match="не найден"):
        await search_object_by_cadastre.fn(cadastre_number="99:99:9999999:9999")


@pytest.mark.asyncio
@respx.mock
async def test_get_cadastre_value_with_value():
    fake = {
        "features": [
            {
                "type": "6",  # помещение / квартира
                "attrs": {
                    "cn": "77:01:0001017:5678",
                    "address": "Москва, ул. Тестовая, д.5, кв.10",
                    "area_value": 65.0,
                    "util_by_doc": "Жилое помещение (квартира)",
                    "cad_cost": 20000000,
                    "date_cost": "2024-01-15",
                },
            }
        ]
    }
    respx.get(f"{PKK_BASE}/features/1").mock(return_value=Response(200, json=fake))

    result = await get_cadastre_value.fn(cadastre_number="77:01:0001017:5678")
    assert result["current_value_rub"] == 20000000
    # Жилое — должно применить 0.1% rate
    assert result["tax_rate_used"] == 0.001
    assert result["estimated_annual_property_tax_rub"] == 20000


def test_normalize_object_handles_invalid():
    assert "raw" in _normalize_object("not a dict")  # type: ignore[arg-type]


def test_normalize_object_with_extent_only():
    """Coordinates extraction works even если no center given."""
    feature = {
        "type": "5",
        "attrs": {"cn": "78:01:0001017:0001"},
        "extent": {"xmin": 100, "ymin": 200, "xmax": 200, "ymax": 300},
    }
    result = _normalize_object(feature)
    assert result["coordinates"] == {"x": 150, "y": 250, "crs": "EPSG:3857"}
