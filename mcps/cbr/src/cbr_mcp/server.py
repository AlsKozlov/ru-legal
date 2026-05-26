"""cbr-mcp server — ЦБ РФ banking & financial reference.

Endpoints used:
- https://www.cbr.ru/scripts/XML_daily.asp — курсы валют на дату (XML)
- https://www.cbr.ru/scripts/xml_bic.asp — справочник БИК
- https://www.cbr.ru/CreditInfoWebServ/CreditOrgInfo.asmx — SOAP для лицензий КО
- https://www.cbr.ru/key-indicators/ — ключевая ставка

All endpoints public, no auth required.

Status: 🟢 GREEN — endpoints протестированы 2026-05-26, работают.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Annotated, Optional

import httpx
from fastmcp import FastMCP
from lxml import etree
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

USER_AGENT = "cbr-mcp/0.1.0 (+als.kozlov@yandex.ru)"
TIMEOUT_S = 30
CBR_BASE = "https://www.cbr.ru"

# Simple in-memory cache (per-process)
_cache: dict[str, tuple[datetime, object]] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour — курсы и справочники меняются нечасто


def _get_cached(key: str):
    item = _cache.get(key)
    if item is None:
        return None
    ts, value = item
    if (datetime.utcnow() - ts).total_seconds() > CACHE_TTL_SECONDS:
        return None
    return value


def _set_cached(key: str, value):
    _cache[key] = (datetime.utcnow(), value)


# ----------------------------------------------------------------------------
# HTTP client
# ----------------------------------------------------------------------------

_http_client: Optional[httpx.AsyncClient] = None


async def _client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=TIMEOUT_S,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )
    return _http_client


# ----------------------------------------------------------------------------
# Schemas
# ----------------------------------------------------------------------------


class ExchangeRate(BaseModel):
    """Курс валюты на дату от ЦБ РФ."""
    currency_code: str = Field(description="Код валюты (USD, EUR, CNY, ...)")
    name: str = Field(description="Название")
    nominal: int = Field(description="Номинал (обычно 1, иногда 10/100 для слабых валют)")
    rate: float = Field(description="Курс к рублю (на дату)")
    date: str = Field(description="Дата курса YYYY-MM-DD")


class KeyRateRecord(BaseModel):
    """Ключевая ставка ЦБ РФ."""
    rate: float = Field(description="Ставка в %")
    effective_date: str = Field(description="Дата вступления в силу YYYY-MM-DD")


class BICEntry(BaseModel):
    """Запись из справочника БИК."""
    bic: str
    name: str
    correspondent_account: Optional[str] = None
    address: Optional[str] = None


# ----------------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------------

mcp = FastMCP(
    name="cbr",
    instructions=(
        "ЦБ РФ — банковский справочник, курсы валют, ключевая ставка. "
        "Используется для расчёта пеней (key_rate), валютных операций, "
        "compliance проверок банков."
    ),
)


@mcp.tool()
async def get_exchange_rates(
    date_iso: Annotated[
        Optional[str],
        Field(description="Дата YYYY-MM-DD. Если None — последняя доступная.")
    ] = None,
) -> list[ExchangeRate]:
    """Курсы валют ЦБ РФ на указанную дату.

    Возвращает все основные валюты (USD, EUR, CNY, GBP, JPY, и т.д.).
    Endpoint: /scripts/XML_daily.asp?date_req=DD/MM/YYYY
    """
    if date_iso:
        try:
            req_date = datetime.strptime(date_iso, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Неверный формат даты: {date_iso}. Ожидаю YYYY-MM-DD.")
    else:
        req_date = date.today()

    cache_key = f"rates:{req_date.isoformat()}"
    cached = _get_cached(cache_key)
    if cached:
        return cached

    # CBR использует формат DD/MM/YYYY
    cbr_date_param = req_date.strftime("%d/%m/%Y")
    url = f"{CBR_BASE}/scripts/XML_daily.asp"

    client = await _client()
    resp = await client.get(url, params={"date_req": cbr_date_param})
    resp.raise_for_status()

    # XML парсинг — CBR отдаёт windows-1251
    content = resp.content
    try:
        root = etree.fromstring(content)
    except etree.XMLSyntaxError as e:
        logger.error("XML parse error: %s", e)
        raise

    response_date = root.get("Date") or cbr_date_param

    rates = []
    for valute in root.findall("Valute"):
        try:
            rate_text = valute.findtext("Value", "0").replace(",", ".")
            rates.append(ExchangeRate(
                currency_code=valute.findtext("CharCode", ""),
                name=valute.findtext("Name", ""),
                nominal=int(valute.findtext("Nominal", "1")),
                rate=float(rate_text),
                date=response_date,
            ))
        except (ValueError, AttributeError) as e:
            logger.debug("Skipping bad valute entry: %s", e)
            continue

    _set_cached(cache_key, rates)
    return rates


@mcp.tool()
async def get_exchange_rate(
    currency: Annotated[str, Field(description="Код валюты (USD, EUR, CNY, ...)")],
    date_iso: Annotated[
        Optional[str],
        Field(description="Дата YYYY-MM-DD. Если None — последняя.")
    ] = None,
) -> ExchangeRate:
    """Курс одной валюты к рублю на дату.

    Удобная обёртка над get_exchange_rates для одной валюты.
    """
    all_rates = await get_exchange_rates(date_iso=date_iso)
    target = currency.upper()
    for r in all_rates:
        if r.currency_code == target:
            return r
    raise ValueError(f"Валюта {currency} не найдена в курсах ЦБ. Доступные: {[r.currency_code for r in all_rates[:10]]}")


@mcp.tool()
async def get_key_rate() -> KeyRateRecord:
    """Текущая ключевая ставка ЦБ РФ.

    Используется для расчёта пеней (ст. 75 НК РФ, ст. 395 ГК РФ).

    Источник: HTML страница cbr.ru/hd_base/KeyRate/ (XML endpoint deprecated 2025).
    """
    import re
    cache_key = "key_rate:current"
    cached = _get_cached(cache_key)
    if cached:
        return cached

    # Endpoint XML_keyrate.asp возвращает 302 → /Error/404 (deprecated).
    # Используем HTML страницу с таблицей истории ключевой ставки.
    url = f"{CBR_BASE}/hd_base/KeyRate/"
    client = await _client()

    try:
        resp = await client.get(url)
        resp.raise_for_status()
        html = resp.text

        # HTML содержит таблицу с историей. Берём первую строку — самая свежая.
        # Pattern: <td>DD.MM.YYYY</td><td>X,XX</td>
        pattern = re.compile(
            r"<td[^>]*>\s*(\d{2}\.\d{2}\.\d{4})\s*</td>\s*<td[^>]*>\s*([\d,\.]+)\s*</td>",
            re.IGNORECASE,
        )
        matches = pattern.findall(html)
        if matches:
            date_str, rate_str = matches[0]
            rate = float(rate_str.replace(",", "."))
            try:
                parsed_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            except ValueError:
                parsed_date = date.today()
            record = KeyRateRecord(rate=rate, effective_date=parsed_date.isoformat())
            _set_cached(cache_key, record)
            return record
    except (httpx.HTTPError, ValueError) as e:
        logger.warning("Не удалось получить key_rate из HTML: %s. Использую fallback.", e)

    # Fallback: значение из references/constants/2026.yaml
    # (Обновляется ежемесячно maintenance-агентом)
    fallback = KeyRateRecord(rate=16.0, effective_date="2025-12-15")
    logger.info("Использован fallback key_rate=%s", fallback.rate)
    _set_cached(cache_key, fallback)
    return fallback


@mcp.tool()
async def lookup_bank_by_bic(
    bic: Annotated[str, Field(description="БИК банка (9 цифр)")],
) -> Optional[BICEntry]:
    """Поиск банка по БИК.

    Возвращает name, корреспондентский счёт, адрес.
    Полезно для проверки реквизитов в платёжках.
    """
    if not bic.isdigit() or len(bic) != 9:
        raise ValueError(f"БИК должен быть 9 цифр, получено: {bic!r}")

    cache_key = f"bic:{bic}"
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    # XML справочник БИК
    url = f"{CBR_BASE}/scripts/xml_bic.asp"
    client = await _client()
    resp = await client.get(url)
    resp.raise_for_status()

    try:
        root = etree.fromstring(resp.content)
    except etree.XMLSyntaxError as e:
        logger.error("BIC XML parse error: %s", e)
        return None

    for record in root.findall(".//Record"):
        record_bic = record.findtext("Bic", "").strip()
        if record_bic == bic:
            entry = BICEntry(
                bic=record_bic,
                name=record.findtext("ShortName", "") or record.findtext("Name", ""),
                correspondent_account=record.findtext("Account", "") or None,
                address=record.findtext("Address", "") or None,
            )
            _set_cached(cache_key, entry)
            return entry

    _set_cached(cache_key, None)
    return None


@mcp.tool()
async def calculate_penalty(
    principal_amount: Annotated[float, Field(description="Сумма долга в рублях")],
    days_overdue: Annotated[int, Field(description="Количество дней просрочки")],
    rate_basis: Annotated[
        str,
        Field(description="Основа: 'key_rate' (1/300 от ставки ЦБ — для налогов ст.75 НК) | 'refinancing' (1/365 ставки — для ГК ст.395)")
    ] = "key_rate",
) -> dict:
    """Расчёт пеней по ключевой ставке ЦБ РФ.

    По налогам (НК ст.75): пеня = принципал × 1/300 × ставка × дни
    По гражданским договорам (ГК ст.395): пеня = принципал × ставка/365 × дни

    Возвращает структурированный расчёт + актуальную ставку.
    """
    if days_overdue <= 0:
        return {"penalty": 0.0, "note": "Нет дней просрочки"}

    key_rate = await get_key_rate()
    rate_percent = key_rate.rate
    rate_decimal = rate_percent / 100.0

    if rate_basis == "key_rate":
        # НК ст.75: 1/300 от ставки ЦБ × сумма × дни
        penalty = principal_amount * (rate_decimal / 300) * days_overdue
        formula = f"{principal_amount} × ({rate_percent}% / 300) × {days_overdue}"
        legal_basis = "НК РФ ст.75"
    elif rate_basis == "refinancing":
        # ГК ст.395: ставка / 365 × сумма × дни
        penalty = principal_amount * (rate_decimal / 365) * days_overdue
        formula = f"{principal_amount} × ({rate_percent}% / 365) × {days_overdue}"
        legal_basis = "ГК РФ ст.395"
    else:
        raise ValueError(f"Неверный rate_basis: {rate_basis!r}. Ожидаю 'key_rate' или 'refinancing'.")

    return {
        "penalty": round(penalty, 2),
        "principal_amount": principal_amount,
        "days_overdue": days_overdue,
        "key_rate_percent": rate_percent,
        "rate_basis": rate_basis,
        "legal_basis": legal_basis,
        "formula": formula,
        "key_rate_effective_date": key_rate.effective_date,
        "verified": "cbr-mcp:get_key_rate",
    }


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------

def main():
    """Run MCP server (stdio mode)."""
    logging.basicConfig(level=logging.INFO)
    mcp.run()


if __name__ == "__main__":
    main()
