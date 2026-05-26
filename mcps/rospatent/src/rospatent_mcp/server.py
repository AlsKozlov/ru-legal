"""MCP server для Роспатент/ФИПС — URL-builder mode (v0.2.0).

⚠ ВАЖНО — изменение архитектуры в v0.2.0:

Предыдущая версия (0.1.0) использовала endpoints www1.fips.ru/registers-web/api/...
которые НЕ СУЩЕСТВУЮТ (HTTP 404 на всех 4 endpoint'ах). Это была спекулятивная
реализация по предполагаемой schema, никогда не валидированная.

ФИПС реальность (audit 2026-05-26):
- new.fips.ru/iiss/db.xhtml — JSF портал (jsessionid + ViewState — сложно скрейпить)
- new.fips.ru/registers-doc-view/fips_servlet — старый servlet (24-byte ответ)
- searchplatform.rospatent.gov.ru/api/* — JSON API, **требует регистрации/API ключа**

Этот rewrite (0.2.0) — HONEST URL-BUILDER MODE:
- НЕ делает реальные API вызовы (нет работающего public endpoint)
- Возвращает ПРЯМЫЕ ССЫЛКИ на поиск/карточки в ФИПС/Роспатент
- LLM-агент даёт юристу ссылки, он сам открывает в браузере
- Когда найдётся работающий API (paid registration на searchplatform или
  собственная HTML scraping infrastructure) — переключим на real calls

Status: 🟡 YELLOW — честный stub, не врёт что работает.

Tools:
- build_trademark_search_url — ссылка на поиск ТЗ в ФИПС
- build_patent_search_url — ссылка на поиск патентов
- build_software_search_url — ссылка на поиск ПО
- get_trademark_card_url — карточка ТЗ по номеру регистрации
- get_patent_card_url — карточка патента по номеру
- check_attorney_register_url — реестр патентных поверенных
"""

from __future__ import annotations

import logging
import sys
from typing import Annotated, Optional
from urllib.parse import quote_plus

from fastmcp import FastMCP
from pydantic import BaseModel, Field

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("rospatent-mcp")

# ============================================================================
# Конфигурация
# ============================================================================

# Реальные work URLs для ручного открытия в браузере
FIPS_PORTAL = "https://new.fips.ru"
FIPS_TRADEMARK_SEARCH = "https://new.fips.ru/registers-doc-view/fips_servlet?DB=RUTM&rn={number}"
FIPS_PATENT_SEARCH = "https://new.fips.ru/registers-doc-view/fips_servlet?DB=RUPAT&rn={number}"
FIPS_SOFTWARE_SEARCH = "https://new.fips.ru/registers-doc-view/fips_servlet?DB=EVM&rn={number}"
ROSPATENT_OPEN_PORTAL = "https://rospatent.gov.ru"

# Search portal pages (для query-based поиска)
FIPS_TRADEMARK_PORTAL = "https://new.fips.ru/iiss/db.xhtml?type=TRADEMARK&query={query}"
FIPS_PATENT_PORTAL = "https://new.fips.ru/iiss/db.xhtml?type=PATENT&query={query}"

# ============================================================================
# Schemas
# ============================================================================


class SearchURL(BaseModel):
    """URL для открытия в браузере для ручного поиска."""

    url: str = Field(description="Прямая ссылка для открытия в браузере")
    description: str = Field(description="Что юрист увидит на этой странице")
    note: str = Field(description="Ограничения / комментарий")


class RegisterCardURL(BaseModel):
    """URL карточки в реестре по номеру."""

    url: str = Field(description="Прямая ссылка на карточку")
    register_type: str = Field(description="Тип реестра (RUTM/RUPAT/EVM)")
    registration_number: str = Field(description="Номер регистрации")
    description: str = Field(description="Что юрист увидит")


# ============================================================================
# MCP server
# ============================================================================

mcp = FastMCP(
    name="rospatent",
    instructions=(
        "ВАЖНО: этот MCP в URL-BUILDER MODE (v0.2.0). У ФИПС нет публичного REST API. "
        "Tools возвращают прямые ссылки для ручного открытия в браузере. "
        "Когда LLM использует эти tools — выдаёт юристу URL, юрист сам проверяет на сайте. "
        "Это честный stub до момента подключения paid API (searchplatform.rospatent.gov.ru)."
    ),
)


# ============================================================================
# Tools
# ============================================================================


@mcp.tool()
def build_trademark_search_url(
    query: Annotated[str, Field(description="Поисковый запрос (название бренда, описание)")],
    nice_class: Annotated[
        Optional[int],
        Field(description="Класс МКТУ (1-45). Если None — поиск по всем классам.")
    ] = None,
) -> SearchURL:
    """Построить URL для поиска товарных знаков в ФИПС.

    ⚠ Этот tool НЕ выполняет реальный поиск (у ФИПС нет публичного API).
    Возвращает прямую ссылку — юрист открывает её в браузере.

    Полезно для:
    - Pre-clearance check перед регистрацией нового ТЗ
    - Проверка существующих ТЗ конкурентов
    - Поиск возможных столкновений по классу МКТУ
    """
    encoded = quote_plus(query)
    url = FIPS_TRADEMARK_PORTAL.format(query=encoded)
    if nice_class:
        url += f"&niceClass={nice_class}"

    return SearchURL(
        url=url,
        description=(
            f"Поиск ТЗ по запросу '{query}'"
            + (f" в классе МКТУ {nice_class}" if nice_class else " по всем классам")
            + " на портале new.fips.ru"
        ),
        note=(
            "У ФИПС нет публичного API — открой ссылку в браузере, выполни поиск. "
            "Время поиска ~5-15 сек, результаты с детальными карточками."
        ),
    )


@mcp.tool()
def build_patent_search_url(
    query: Annotated[str, Field(description="Поисковый запрос (тема, ключевые слова)")],
    patent_type: Annotated[
        str,
        Field(description="Тип: 'invention' (изобретение) | 'utility' (полезная модель) | 'design' (промобразец)")
    ] = "invention",
) -> SearchURL:
    """Построить URL для поиска патентов в ФИПС.

    ⚠ URL-only mode — реальный поиск выполняется юристом в браузере.
    """
    encoded = quote_plus(query)
    url = FIPS_PATENT_PORTAL.format(query=encoded)
    type_param_map = {
        "invention": "INVENTION",
        "utility": "UTILITY_MODEL",
        "design": "INDUSTRIAL_DESIGN",
    }
    if patent_type in type_param_map:
        url += f"&patentType={type_param_map[patent_type]}"

    return SearchURL(
        url=url,
        description=f"Поиск патентов ({patent_type}) по запросу '{query}' на new.fips.ru",
        note=(
            "URL-only mode. Юрист открывает ссылку, выполняет поиск в портале ФИПС. "
            "Для programmatic access потребуется регистрация на "
            "searchplatform.rospatent.gov.ru (paid API)."
        ),
    )


@mcp.tool()
def get_trademark_card_url(
    registration_number: Annotated[
        str,
        Field(description="Номер регистрации ТЗ (5-7 цифр)")
    ],
) -> RegisterCardURL:
    """Построить URL карточки товарного знака по номеру регистрации.

    Карточка содержит: владельца, дату регистрации, классы МКТУ, изображение знака.

    Пример номера: 762341
    """
    rn = registration_number.strip().lstrip("№").strip()
    if not rn.isdigit():
        raise ValueError(f"Номер регистрации должен быть числом: {registration_number!r}")

    url = FIPS_TRADEMARK_SEARCH.format(number=rn)
    return RegisterCardURL(
        url=url,
        register_type="RUTM",
        registration_number=rn,
        description=(
            f"Карточка ТЗ № {rn} в реестре RUTM (Российские товарные знаки). "
            "Содержит: правообладатель, дата приоритета, классы МКТУ, изображение."
        ),
    )


@mcp.tool()
def get_patent_card_url(
    registration_number: Annotated[
        str,
        Field(description="Номер патента (6-7 цифр, для изобретений RU2)")
    ],
) -> RegisterCardURL:
    """Построить URL карточки патента по номеру.

    Содержит: формулу изобретения, описание, патентообладатель, статус.

    Пример номера: 2742123
    """
    rn = registration_number.strip().lstrip("RU").lstrip("№").strip()
    if not rn.isdigit():
        raise ValueError(f"Номер патента должен быть числом: {registration_number!r}")

    url = FIPS_PATENT_SEARCH.format(number=rn)
    return RegisterCardURL(
        url=url,
        register_type="RUPAT",
        registration_number=rn,
        description=(
            f"Карточка патента № {rn} в реестре RUPAT. "
            "Содержит: формула, описание, патентообладатель, статус, дата подачи."
        ),
    )


@mcp.tool()
def build_software_search_url(
    query: Annotated[str, Field(description="Название ПО или описание")],
) -> SearchURL:
    """Построить URL для поиска зарегистрированных программ для ЭВМ.

    Реестр ЕВМ (программ для ЭВМ и баз данных) — отдельная регистрация в ФИПС.
    """
    encoded = quote_plus(query)
    url = f"https://new.fips.ru/iiss/db.xhtml?type=EVM&query={encoded}"
    return SearchURL(
        url=url,
        description=f"Поиск программ для ЭВМ и БД по запросу '{query}'",
        note="Реестр EVM. URL-only mode — поиск в браузере.",
    )


@mcp.tool()
def check_attorney_register_url(
    attorney_name: Annotated[
        Optional[str],
        Field(description="ФИО патентного поверенного (опц.)")
    ] = None,
) -> SearchURL:
    """URL реестра патентных поверенных РФ.

    Полезно для:
    - Проверка является ли лицо действующим патентным поверенным
    - Поиск поверенного для регистрации ТЗ/патента
    """
    url = "https://rospatent.gov.ru/ru/sites/default/files/docs/registry/patent-attorneys.html"
    note_text = (
        "Реестр патентных поверенных Роспатента. "
        "Поиск по фамилии через Ctrl+F в браузере."
    )
    if attorney_name:
        encoded = quote_plus(attorney_name)
        url += f"?search={encoded}"
        note_text = (
            f"Реестр патентных поверенных. Ищите {attorney_name} через поиск страницы."
        )

    return SearchURL(
        url=url,
        description="Реестр патентных поверенных Роспатента",
        note=note_text,
    )


# ============================================================================
# Entry point
# ============================================================================


def main():
    """Run MCP server (stdio mode)."""
    mcp.run()


if __name__ == "__main__":
    main()
