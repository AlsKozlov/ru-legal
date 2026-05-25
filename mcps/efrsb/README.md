# efrsb-mcp

MCP server для [bankrot.fedresurs.ru](https://bankrot.fedresurs.ru) — Единый
федеральный реестр сведений о банкротстве.

## Tools

| Tool | Purpose |
|------|---------|
| `check_company_bankruptcy` | Проверка ЮЛ / ИП на банкротство (ИНН / ОГРН / название) |
| `check_person_bankruptcy` | Проверка физ.лица (ФЗ-127 глава X — потребительское банкротство) |
| `get_bankruptcy_case_publications` | Список публикаций по делу (торги, отчёты, собрания) |
| `search_arbitration_manager` | Поиск арбитражного управляющего |

## Use cases в ru-legal packs

- **corporate-law/diligence-issue-extraction** — section D Bankruptcy DD
- **contract-law/vendor-agreement-review** — pre-deal vendor check
- **labor-law/termination-review** — verification работодатель не в банкротстве
- **tax-law/tax-audit-response** — assess контрагенты-"однодневки" в НДС цепочке
- **ip-law/infringement-triage** — assets recovery если infringer банкрот

## Installation

```bash
cd mcps/efrsb
pip install -e ".[dev]"
```

## Run

```bash
efrsb-mcp  # stdio MCP server
```

## Source

ЕФРСБ — official portal under ФЗ-127 ст.28 + Постановление Правительства РФ.
Этот MCP использует JSON endpoints `backend/companies`, `backend/persons`, и т.п.
Они публичны и стабильны (использованы front-end сайтом ЕФРСБ).

## License

Apache 2.0
