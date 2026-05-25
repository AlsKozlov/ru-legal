# rosreestr-mcp

MCP server для Росреестр / ЕГРН (через Публичную кадастровую карту
[pkk.rosreestr.ru](https://pkk.rosreestr.ru)).

## Tools

| Tool | Purpose |
|------|---------|
| `search_object_by_cadastre` | Поиск по кадастровому номеру (точно) |
| `search_object_by_address` | Поиск по адресу (less reliable) |
| `get_object_details` | Карточка объекта |
| `get_cadastre_value` | Кадастровая стоимость + tax estimation |
| `get_encumbrances` | Базовые обременения (для full — заказать ЕГРН выписку) |

## Use cases в ru-legal packs

- **real-estate/cadastre-check** — main user
- **real-estate/encumbrance-analysis** — initial scan
- **real-estate/ddu-review** — verify застройщик объект существует
- **real-estate/purchase-sale-review** — verify object identity
- **corporate-law/diligence-issue-extraction** — section E Real estate DD

## Important: PKK vs ЕГРН выписка

**Этот MCP — это Публичная Кадастровая Карта** (free, public). Для **полных
ЕГРН данных** (текущий собственник, full обременения, history) — нужно заказать
**выписку из ЕГРН** через [rosreestr.gov.ru](https://rosreestr.gov.ru) или
[Госуслуги](https://gosuslugi.ru):

- Electronic — 290 руб
- С печатью / расширенная — до 460 руб
- Срок: 5-7 рабочих дней

Этот MCP **не** заказывает выписки — это manual / paid procedure через portal.
Но дает все publicly available data + рекомендует когда нужна выписка.

## License

Apache 2.0
