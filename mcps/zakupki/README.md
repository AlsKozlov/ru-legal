# zakupki-mcp

MCP server для [zakupki.gov.ru](https://zakupki.gov.ru) — ЕИС закупки.

## Tools

| Tool | Purpose |
|------|---------|
| `search_tenders` | Поиск закупок (query / customer / ОКПД / регион / НМЦК / status) |
| `get_tender` | Карточка закупки (НМЦК + способ + сроки + требования + результат) |
| `check_rnp` | Проверка в РНП (Реестр недобросовестных поставщиков) |
| `get_customer_history` | История закупок заказчика — для bias detection |
| `get_supplier_contracts` | Контракты поставщика — DD / track record |

## Use cases в ru-legal packs

- **public-procurement/tender-documentation-review** — get_tender для full info
- **public-procurement/tender-eligibility-check** — verify eligibility / РНП
- **public-procurement/biased-tender-detection** — get_customer_history pattern analysis
- **public-procurement/rnp-check** — check_rnp прямой call
- **public-procurement/fas-complaint-draft** — supporting evidence по тендеру
- **corporate-law/diligence-issue-extraction** — DD контрагентов на гос.заказе

## License

Apache 2.0
