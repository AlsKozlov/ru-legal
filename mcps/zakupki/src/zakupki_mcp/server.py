"""MCP server для zakupki.gov.ru — ЕИС (Единая информационная система в сфере закупок).

Tools:
- search_tenders — поиск закупок 44-ФЗ / 223-ФЗ
- get_tender — детальная карточка закупки
- check_rnp — проверка по Реестру недобросовестных поставщиков
- get_customer_history — история закупок конкретного заказчика
- get_supplier_contracts — контракты конкретного поставщика

Source: ЕИС закупки имеет public API (open data); endpoint stability varies.
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
logger = logging.getLogger("zakupki-mcp")

ZAKUPKI_BASE = "https://zakupki.gov.ru"
ZAKUPKI_API_BASE = f"{ZAKUPKI_BASE}/epz/api"
RNP_API_BASE = f"{ZAKUPKI_BASE}/epz/dishonestsupplier/api"

REQUEST_TIMEOUT_S = 30.0
MAX_CONCURRENT_REQUESTS = 5

mcp = FastMCP(
    name="zakupki",
    instructions=(
        "Поиск и анализ закупок в ЕИС zakupki.gov.ru — 44-ФЗ (государственные) и "
        "223-ФЗ (корпоративные с гос.участием). Также — проверка контрагентов через "
        "Реестр недобросовестных поставщиков (РНП). Use для tender review, bias "
        "detection (history конкретного заказчика), DD контрагентов."
    ),
)


_http_client: httpx.AsyncClient | None = None
_request_semaphore: asyncio.Semaphore | None = None
_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_S = 1800.0
_CACHE_MAX_ENTRIES = 500


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_S,
            headers={
                "User-Agent": "zakupki-mcp/0.1.0",
                "Accept": "application/json",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Referer": "https://zakupki.gov.ru/",
            },
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
            follow_redirects=True,
        )
    return _http_client


def _get_semaphore() -> asyncio.Semaphore:
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
        _cache.pop(next(iter(_cache)), None)
    _cache[key] = (time.monotonic(), value)


async def _api_get(url: str, params: dict[str, Any] | None = None) -> Any:
    cache_key = f"GET {url} {json.dumps(params or {}, sort_keys=True, default=str)}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    client = _get_http_client()
    async with _get_semaphore():
        try:
            resp = await client.get(url, params=params)
        except httpx.TimeoutException as e:
            raise ToolError(f"zakupki.gov.ru timed out за {REQUEST_TIMEOUT_S}s.") from e
        except httpx.RequestError as e:
            raise ToolError(f"Не удалось связаться с ЕИС: {e}") from e

    if resp.status_code == 404:
        raise ToolError("Закупка / запись не найдена в ЕИС.")
    if resp.status_code >= 500:
        raise ToolError(f"ЕИС вернул ошибку сервера (HTTP {resp.status_code}).")
    if resp.status_code >= 400:
        logger.warning("HTTP %d from %s: %s", resp.status_code, url, resp.text[:500])
        raise ToolError(f"Ошибка запроса к ЕИС (HTTP {resp.status_code}).")

    try:
        data = resp.json()
    except ValueError as e:
        raise ToolError("ЕИС вернул не-JSON ответ. Источник may be in degraded mode.") from e

    _cache_set(cache_key, data)
    return data


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_tenders(
    query: Annotated[
        str | None,
        Field(description="Поисковая строка по наименованию закупки.", max_length=300),
    ] = None,
    customer_inn: Annotated[
        str | None,
        Field(
            description="ИНН заказчика — для tracking конкретного гос.заказчика.",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    purchase_number: Annotated[
        str | None,
        Field(
            description="Номер извещения о закупке в ЕИС (19-21 цифра).",
            pattern=r"^\d{19,21}$",
        ),
    ] = None,
    law: Annotated[
        str,
        Field(
            description="Закон: '44-ФЗ' (гос.заказчики) / '223-ФЗ' (корпоративные с гос.участием) / 'all'.",
        ),
    ] = "all",
    price_min: Annotated[
        float | None,
        Field(description="НМЦК минимум (руб).", ge=0),
    ] = None,
    price_max: Annotated[
        float | None,
        Field(description="НМЦК максимум (руб).", ge=0),
    ] = None,
    status: Annotated[
        str | None,
        Field(
            description=(
                "Статус: 'active' (приём заявок) / 'completed' / 'cancelled' / 'all' (default)."
            ),
        ),
    ] = None,
    okpd_code: Annotated[
        str | None,
        Field(
            description="Код ОКПД2 (классификатор продукции по видам деятельности).",
            max_length=20,
        ),
    ] = None,
    region_code: Annotated[
        str | None,
        Field(
            description="Код региона РФ (2 цифры — например '77' для Москвы).",
            pattern=r"^\d{2}$",
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум результатов.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Поиск закупок в ЕИС.

    Use cases:
    - Tender opportunity scan (query / okpd / region)
    - History конкретного заказчика (customer_inn) — для biased-tender-detection
    - Tracking pipeline своих участий (по своему ИНН в search_supplier_contracts)
    """
    if not any([query, customer_inn, purchase_number, okpd_code]):
        raise ToolError(
            "Нужен хотя бы один из критериев: query / customer_inn / purchase_number / okpd_code."
        )

    logger.info("search_tenders query=%r customer=%s law=%s", query, customer_inn, law)

    params: dict[str, Any] = {"recordsPerPage": limit}
    if query:
        params["searchString"] = query
    if customer_inn:
        params["customerInn"] = customer_inn
    if purchase_number:
        params["purchaseNumber"] = purchase_number
    if law in ("44-ФЗ", "44", "223-ФЗ", "223"):
        params["fz"] = law.replace("-ФЗ", "")
    if price_min is not None:
        params["priceFrom"] = price_min
    if price_max is not None:
        params["priceTo"] = price_max
    if status:
        params["status"] = status
    if okpd_code:
        params["okpd"] = okpd_code
    if region_code:
        params["region"] = region_code

    data = await _api_get(f"{ZAKUPKI_API_BASE}/orders/search", params=params)
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []
    return [_normalize_tender(item) for item in items[:limit]]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_tender(
    purchase_number: Annotated[
        str,
        Field(
            description="Номер извещения о закупке в ЕИС (19-21 цифра).",
            pattern=r"^\d{19,21}$",
        ),
    ],
) -> dict[str, Any]:
    """Детальная карточка закупки.

    Returns: НМЦК + способ определения поставщика + сроки + документация ссылки +
    требования к участникам + результат если завершена.
    """
    logger.info("get_tender purchase_number=%s", purchase_number)
    data = await _api_get(f"{ZAKUPKI_API_BASE}/orders/{purchase_number}")
    if not isinstance(data, dict):
        raise ToolError("Не удалось разобрать карточку закупки.")
    return _normalize_tender_full(data)


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def check_rnp(
    inn: Annotated[
        str | None,
        Field(
            description="ИНН для проверки в РНП (Реестр недобросовестных поставщиков).",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ] = None,
    ogrn: Annotated[
        str | None,
        Field(
            description="ОГРН.",
            pattern=r"^\d{13}$|^\d{15}$",
        ),
    ] = None,
    name: Annotated[
        str | None,
        Field(description="Наименование для поиска.", max_length=300),
    ] = None,
    law: Annotated[
        str,
        Field(description="РНП: '44-ФЗ' / '223-ФЗ' / 'all'."),
    ] = "all",
) -> dict[str, Any]:
    """Проверка в РНП.

    Returns:
        - status: 'clean' / 'in_rnp' / 'historical' / 'not_found'
        - records (если найден): дата включения, основание, заказчик инициировавший,
          реквизиты решения ФАС, срок включения

    Critical: попадание в РНП = 2-летняя дисквалификация из гос.закупок.
    """
    if not any([inn, ogrn, name]):
        raise ToolError("Нужен хотя бы один: inn / ogrn / name.")

    logger.info("check_rnp inn=%s ogrn=%s name=%r law=%s", inn, ogrn, name, law)

    params: dict[str, Any] = {}
    if inn:
        params["inn"] = inn
    if ogrn:
        params["ogrn"] = ogrn
    if name:
        params["name"] = name
    if law in ("44-ФЗ", "44", "223-ФЗ", "223"):
        params["fz"] = law.replace("-ФЗ", "")

    data = await _api_get(f"{RNP_API_BASE}/search", params=params)
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        return {"status": "clean", "query_inn": inn, "query_name": name}

    # Determine status: any active records?
    active = [r for r in items if _is_rnp_record_active(r)]
    historical = [r for r in items if not _is_rnp_record_active(r)]

    return {
        "status": "in_rnp" if active else "historical",
        "active_records": [_normalize_rnp_record(r) for r in active],
        "historical_records": [_normalize_rnp_record(r) for r in historical],
        "query_inn": inn,
        "query_name": name,
    }


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_customer_history(
    customer_inn: Annotated[
        str,
        Field(
            description="ИНН заказчика для tracking historical pattern.",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ],
    date_from: Annotated[
        str | None,
        Field(
            description="С какой даты искать (YYYY-MM-DD).",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум закупок.", ge=1, le=200),
    ] = 50,
) -> dict[str, Any]:
    """История закупок конкретного заказчика — для bias detection.

    Returns:
        - tenders: list of tenders by this customer
        - top_winners: список наиболее частых победителей (potential favourites)
        - average_discount_from_nmck: средний % дисконта от НМЦК
        - patterns: identified patterns (если есть аномалии)
    """
    logger.info("get_customer_history customer_inn=%s", customer_inn)

    params: dict[str, Any] = {"customerInn": customer_inn, "recordsPerPage": limit}
    if date_from:
        params["dateFrom"] = date_from

    data = await _api_get(f"{ZAKUPKI_API_BASE}/orders/search", params=params)
    items = data.get("items") if isinstance(data, dict) else []
    if not isinstance(items, list):
        items = []

    tenders = [_normalize_tender(item) for item in items[:limit]]

    # Analyze patterns
    winners_count: dict[str, int] = {}
    discounts: list[float] = []
    for t in tenders:
        if winner := t.get("winner_name"):
            winners_count[winner] = winners_count.get(winner, 0) + 1
        if (nmck := t.get("nmck")) and (final := t.get("final_price")) and nmck > 0:
            discount = (1 - final / nmck) * 100
            discounts.append(discount)

    top_winners = sorted(winners_count.items(), key=lambda x: -x[1])[:5]

    return {
        "customer_inn": customer_inn,
        "total_tenders_analyzed": len(tenders),
        "tenders": tenders[:25],  # truncate для response size
        "top_winners": [{"name": n, "wins": c} for n, c in top_winners],
        "average_discount_from_nmck_pct": (
            round(sum(discounts) / len(discounts), 2) if discounts else None
        ),
        "_note": "Top winner со суммарной долей > 40% — flag для biased-tender-detection",
    }


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_supplier_contracts(
    supplier_inn: Annotated[
        str,
        Field(
            description="ИНН поставщика.",
            pattern=r"^\d{10}$|^\d{12}$",
        ),
    ],
    status: Annotated[
        str | None,
        Field(description="Статус контракта: 'active' / 'executed' / 'terminated' / 'all'."),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Максимум контрактов.", ge=1, le=100),
    ] = 25,
) -> list[dict[str, Any]]:
    """Контракты конкретного поставщика по 44-ФЗ.

    Use cases:
    - DD контрагента: история исполнения гос.контрактов
    - Self-assessment: our own track record
    - Competitive intelligence
    """
    logger.info("get_supplier_contracts supplier_inn=%s", supplier_inn)

    params: dict[str, Any] = {"supplierInn": supplier_inn, "recordsPerPage": limit}
    if status:
        params["status"] = status

    data = await _api_get(f"{ZAKUPKI_API_BASE}/contracts/search", params=params)
    items = data.get("items") if isinstance(data, dict) else []
    if not isinstance(items, list):
        return []
    return [_normalize_contract(item) for item in items[:limit]]


# ----------------------------------------------------------------------------
# Helpers + Normalizers
# ----------------------------------------------------------------------------


def _is_rnp_record_active(record: dict[str, Any]) -> bool:
    """Запись в РНП активна если:
    - end_date не указана, ИЛИ
    - end_date в будущем
    Период включения по 44-ФЗ — 2 года с даты включения."""
    if not isinstance(record, dict):
        return False
    end_date = record.get("endDate") or record.get("dateEnd")
    if not end_date:
        return True  # No end date = still active
    # Simplified — assume ISO format; production should parse properly
    today = time.strftime("%Y-%m-%d")
    return end_date >= today


def _normalize_tender(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    purchase_num = item.get("purchaseNumber") or item.get("number")
    return {
        "purchase_number": purchase_num,
        "name": item.get("name") or item.get("title"),
        "law": item.get("fz") or item.get("law"),
        "customer": _safe_dict_field(item.get("customer"), "name") or item.get("customerName"),
        "customer_inn": _safe_dict_field(item.get("customer"), "inn"),
        "nmck": item.get("price") or item.get("nmck"),
        "status": item.get("status"),
        "purchase_method": item.get("purchaseMethod") or item.get("method"),
        "publish_date": item.get("publishDate"),
        "submission_deadline": item.get("submissionDeadline") or item.get("dateEnd"),
        "result_date": item.get("resultDate"),
        "winner_name": _safe_dict_field(item.get("winner"), "name"),
        "winner_inn": _safe_dict_field(item.get("winner"), "inn"),
        "final_price": item.get("finalPrice"),
        "url": f"{ZAKUPKI_BASE}/epz/order/notice/ea44/view/common-info.html?regNumber={purchase_num}" if purchase_num else None,
    }


def _normalize_tender_full(item: dict[str, Any]) -> dict[str, Any]:
    base = _normalize_tender(item)
    base.update(
        {
            "okpd_codes": item.get("okpdCodes"),
            "requirements_supplier": item.get("supplierRequirements"),
            "security_deposit": item.get("securityDeposit"),
            "security_performance": item.get("securityPerformance"),
            "place_delivery": item.get("placeDelivery"),
            "performance_term": item.get("performanceTerm"),
            "etp_url": item.get("etpUrl"),  # электронная торговая площадка
            "documentation_urls": item.get("documentation"),
            "smp_required": item.get("smpRequired"),  # для МСП
        }
    )
    return {k: v for k, v in base.items() if v is not None}


def _normalize_contract(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    contract_num = item.get("contractNumber") or item.get("number")
    return {
        "contract_number": contract_num,
        "name": item.get("name") or item.get("subject"),
        "law": item.get("fz") or item.get("law"),
        "customer": _safe_dict_field(item.get("customer"), "name"),
        "customer_inn": _safe_dict_field(item.get("customer"), "inn"),
        "supplier": _safe_dict_field(item.get("supplier"), "name"),
        "supplier_inn": _safe_dict_field(item.get("supplier"), "inn"),
        "price": item.get("price"),
        "status": item.get("status"),
        "conclude_date": item.get("concludeDate"),
        "execution_date": item.get("executionDate"),
        "termination_date": item.get("terminationDate"),
        "url": (
            f"{ZAKUPKI_BASE}/epz/contract/contractCard/common-info.html?reestrNumber={contract_num}"
            if contract_num
            else None
        ),
    }


def _normalize_rnp_record(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"raw": item}
    return {
        "reg_number": item.get("regNumber") or item.get("id"),
        "supplier_name": item.get("supplierName") or _safe_dict_field(item.get("supplier"), "name"),
        "supplier_inn": item.get("supplierInn") or _safe_dict_field(item.get("supplier"), "inn"),
        "law": item.get("fz") or item.get("law"),
        "reason": item.get("reason"),
        "decision_authority": item.get("decisionAuthority"),
        "decision_date": item.get("decisionDate"),
        "decision_number": item.get("decisionNumber"),
        "include_date": item.get("includeDate") or item.get("dateStart"),
        "end_date": item.get("endDate") or item.get("dateEnd"),
        "customer_that_initiated": _safe_dict_field(item.get("customer"), "name"),
    }


def _safe_dict_field(obj: Any, field: str) -> Any:
    return obj.get(field) if isinstance(obj, dict) else None


@mcp.resource("zakupki://laws-cheatsheet")
def laws_cheatsheet() -> str:
    return (
        "# 44-ФЗ vs 223-ФЗ\n\n"
        "## 44-ФЗ «О контрактной системе»\n\n"
        "- Гос.заказчики: бюджетные учреждения, гос.органы, муниципалитеты\n"
        "- Строгая регуляция: способы определения поставщика, сроки, требования\n"
        "- Размещение в ЕИС обязательно\n"
        "- ФАС — основной organ надзора\n"
        "- Жалобы — через ЕИС в ФАС, бесплатно\n\n"
        "## 223-ФЗ «О закупках товаров, работ, услуг отдельными видами юр.лиц»\n\n"
        "- Корпоративные заказчики: гос.корпорации, гос.компании, естественные монополии,\n"
        "  субъекты с долей гос.участия > 50%\n"
        "- Более гибкие правила: каждый заказчик утверждает своё Положение о закупках\n"
        "- Меньше способов определения поставщика регулируется\n"
        "- Размещение в ЕИС обязательно, но процедуры варьируются\n\n"
        "## Common способы определения поставщика (44-ФЗ)\n\n"
        "- **Электронный аукцион** — наиболее распространён, low complexity товары\n"
        "- **Открытый конкурс** — для услуг с criteria (не только цена)\n"
        "- **Запрос котировок** — для small-value (< 3 млн руб)\n"
        "- **Запрос предложений** — для complex с переговорами\n"
        "- **Единственный поставщик** — узкие cases (ст.93 ФЗ-44)\n\n"
        "## Реестр недобросовестных поставщиков (РНП)\n\n"
        "- Срок включения: **2 года**\n"
        "- Основания: уклонение от заключения / существенные нарушения исполнения\n"
        "- Effect: 2-летняя дисквалификация из всех гос.закупок\n"
        "- Обжалование: в АС (3 мес с включения)\n"
    )


def main() -> None:
    """Entry point для CLI (zakupki-mcp)."""
    logger.info("Starting zakupki-mcp v0.1.0 over stdio transport")
    mcp.run()


if __name__ == "__main__":
    main()
