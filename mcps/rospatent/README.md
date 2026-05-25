# rospatent-mcp

MCP server для реестров [Роспатент / ФИПС](https://www1.fips.ru) — товарные
знаки, патенты, программы для ЭВМ / БД, патентные поверенные.

## Tools

| Tool | Purpose |
|------|---------|
| `search_trademark` | Поиск ТЗ (text, классы МКТУ, holder ИНН) |
| `get_trademark` | Полная карточка ТЗ |
| `search_patent` | Поиск изобретений / ПМ / промобразцов |
| `get_patent` | Карточка патента с claims |
| `search_software` | ПО / БД в реестре |
| `check_patent_attorney` | Verify статус патентного поверенного |

## Use cases в ru-legal packs

- **ip-law/clearance** — pre-filing collision check ТЗ
- **ip-law/fto-triage** — patent landscape для FTO
- **ip-law/infringement-triage** — verify our IP + check infringer
- **ip-law/portfolio** — наш IP inventory
- **ip-law/invention-intake** — prior art preliminary search
- **ip-law/rospatent-application** — verify патентного поверенного перед engagement
- **corporate-law/diligence-issue-extraction** — section G IP DD

## Installation

```bash
cd mcps/rospatent
pip install -e ".[dev]"
```

## Run

```bash
rospatent-mcp  # stdio MCP
```

## License

Apache 2.0
