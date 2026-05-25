#!/usr/bin/env python3
"""Smoke-tests реальных endpoints у каждого MCP.

Не использует FastMCP framework — напрямую вызываем endpoints через httpx,
чтобы изолировать MCP server bugs от source-availability issues.

Usage:
    python3 scripts/smoke_test_mcps.py
"""
from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class SmokeResult:
    name: str
    endpoint: str
    status: str  # "ok" / "fail" / "blocked"
    detail: str
    latency_ms: int


TIMEOUT = httpx.Timeout(20.0)


async def check_pravo(client: httpx.AsyncClient) -> SmokeResult:
    """pravo.gov.ru — официальный JSON API, обычно стабильный."""
    url = "https://publication.pravo.gov.ru/api/Documents"
    params = {"name": "Гражданский кодекс", "pageSize": 1}
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.get(url, params=params, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            data = resp.json()
            items_count = len(data.get("items", []) if isinstance(data, dict) else [])
            return SmokeResult("pravo", url, "ok", f"returned {items_count} items", latency)
        return SmokeResult("pravo", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("pravo", url, "fail", str(e)[:120], 0)


async def check_egrul(client: httpx.AsyncClient) -> SmokeResult:
    """api-fns.ru — требует API key. Без ключа expect HTTP 401/403."""
    url = "https://api-fns.ru/api/check"
    params = {"req": "7707083893"}  # Сбербанк ИНН (public test)
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.get(url, params=params, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            return SmokeResult("egrul", url, "ok", "endpoint reachable + auth required", latency)
        if resp.status_code in (401, 403):
            return SmokeResult(
                "egrul", url, "blocked",
                "requires API_FNS_KEY (expected — paid service)", latency,
            )
        return SmokeResult("egrul", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("egrul", url, "fail", str(e)[:120], 0)


async def check_kad(client: httpx.AsyncClient) -> SmokeResult:
    """kad.arbitr.ru — known anti-bot защита, часто 403."""
    url = "https://kad.arbitr.ru/Kad/SearchInstances"
    payload = {"Page": 1, "Count": 1, "CaseNumbers": ["A40-1/2025"]}
    headers = {
        "Accept": "application/json",
        "Referer": "https://kad.arbitr.ru/",
        "X-Requested-With": "XMLHttpRequest",
    }
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            return SmokeResult("kad", url, "ok", "endpoint accessible", latency)
        if resp.status_code in (403, 429):
            return SmokeResult(
                "kad", url, "blocked",
                f"HTTP {resp.status_code} — anti-bot защита (known limitation)", latency,
            )
        return SmokeResult("kad", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("kad", url, "fail", str(e)[:120], 0)


async def check_efrsb(client: httpx.AsyncClient) -> SmokeResult:
    """bankrot.fedresurs.ru — publicly available."""
    url = "https://bankrot.fedresurs.ru/backend/companies"
    params = {"searchString": "7707083893", "limit": 1}
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.get(url, params=params, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            return SmokeResult("efrsb", url, "ok", "endpoint accessible", latency)
        if resp.status_code in (403, 429):
            return SmokeResult(
                "efrsb", url, "blocked",
                f"HTTP {resp.status_code} — likely rate-limited", latency,
            )
        return SmokeResult("efrsb", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("efrsb", url, "fail", str(e)[:120], 0)


async def check_rospatent(client: httpx.AsyncClient) -> SmokeResult:
    """www1.fips.ru — реестры Роспатент."""
    url = "https://www1.fips.ru/registers-web/api/trademarks/search"
    params = {"query": "test", "limit": 1, "type": "trademark"}
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.get(url, params=params, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            return SmokeResult("rospatent", url, "ok", "endpoint accessible", latency)
        if resp.status_code in (403, 429):
            return SmokeResult(
                "rospatent", url, "blocked",
                f"HTTP {resp.status_code}", latency,
            )
        if resp.status_code == 404:
            return SmokeResult(
                "rospatent", url, "fail",
                "404 — endpoint changed (ФИПС API нестабилен; update needed)", latency,
            )
        return SmokeResult("rospatent", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("rospatent", url, "fail", str(e)[:120], 0)


async def check_zakupki(client: httpx.AsyncClient) -> SmokeResult:
    """zakupki.gov.ru — ЕИС publicly available."""
    url = "https://zakupki.gov.ru/epz/api/orders/search"
    params = {"searchString": "поставка", "recordsPerPage": 1}
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.get(url, params=params, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            return SmokeResult("zakupki", url, "ok", "endpoint accessible", latency)
        if resp.status_code == 404:
            return SmokeResult(
                "zakupki", url, "fail",
                "404 — ЕИС endpoint changed (update needed)", latency,
            )
        if resp.status_code in (403, 429):
            return SmokeResult("zakupki", url, "blocked", f"HTTP {resp.status_code}", latency)
        return SmokeResult("zakupki", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("zakupki", url, "fail", str(e)[:120], 0)


async def check_rosreestr(client: httpx.AsyncClient) -> SmokeResult:
    """pkk.rosreestr.ru — Публичная кадастровая карта."""
    url = "https://pkk.rosreestr.ru/api/features/1"
    params = {"text": "77:01:0001017:1234", "limit": 1, "tolerance": 1}
    start = asyncio.get_event_loop().time()
    try:
        resp = await client.get(url, params=params, timeout=TIMEOUT)
        latency = int((asyncio.get_event_loop().time() - start) * 1000)
        if resp.status_code == 200:
            return SmokeResult("rosreestr", url, "ok", "endpoint accessible", latency)
        if resp.status_code in (403, 429):
            return SmokeResult(
                "rosreestr", url, "blocked", f"HTTP {resp.status_code}", latency,
            )
        return SmokeResult("rosreestr", url, "fail", f"HTTP {resp.status_code}", latency)
    except Exception as e:
        return SmokeResult("rosreestr", url, "fail", str(e)[:120], 0)


async def main() -> int:
    """Run all checks concurrently."""
    print("=" * 78)
    print("  ru-legal MCP smoke test")
    print("=" * 78)
    print(f"  Endpoints: {7}")
    print(f"  Timeout per request: {int(TIMEOUT.read)}s")
    print()

    async with httpx.AsyncClient(
        follow_redirects=True,
        headers={
            "User-Agent": "ru-legal-smoke-test/0.1",
            "Accept-Language": "ru-RU,ru;q=0.9",
        },
    ) as client:
        results = await asyncio.gather(
            check_pravo(client),
            check_egrul(client),
            check_kad(client),
            check_efrsb(client),
            check_rospatent(client),
            check_zakupki(client),
            check_rosreestr(client),
            return_exceptions=False,
        )

    print(f"{'MCP':<12} {'Status':<10} {'Latency':<10} {'Detail'}")
    print("-" * 78)
    ok_count = 0
    blocked_count = 0
    fail_count = 0
    for r in results:
        emoji = {"ok": "✅", "blocked": "⚠", "fail": "❌"}.get(r.status, "?")
        latency = f"{r.latency_ms}ms" if r.latency_ms else "-"
        print(f"{emoji} {r.name:<10} {r.status:<10} {latency:<10} {r.detail[:60]}")
        if r.status == "ok":
            ok_count += 1
        elif r.status == "blocked":
            blocked_count += 1
        else:
            fail_count += 1

    print("-" * 78)
    print(f"  Total: {len(results)}  |  OK: {ok_count}  |  Blocked: {blocked_count}  |  Failed: {fail_count}")
    print()
    if fail_count > 0:
        print("⚠  Some endpoints failed. Check stderr / network / source availability.")
        print("   `blocked` is expected for kad (anti-bot) and egrul (paid).")
    else:
        print("✅ All endpoints reachable (within expected behavior).")
    print()
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
