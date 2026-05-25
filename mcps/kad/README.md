# kad-mcp

MCP server для [kad.arbitr.ru](https://kad.arbitr.ru) — Картотека арбитражных
дел РФ.

## Tools

| Tool | Purpose |
|------|---------|
| `search_cases` | Поиск дел по номеру / истцу / ответчику / ИНН / суду / датам / суммам |
| `get_case_card` | Полная карточка дела с историей стадий + заседаний |
| `get_case_documents` | Список судебных актов по делу (с PDF ссылками) |
| `list_courts` | Справочник арбитражных судов РФ |

## Use cases в ru-legal packs

- **litigation/matter-intake** — verify номер дела + базовая инфо
- **litigation/portfolio-status** — tracking активных дел portfolio
- **litigation/oc-status** — outside counsel performance metrics
- **corporate-law/diligence-issue-extraction** — DD контрагента (открытые claims)
- **tax-law/arbitration-tax-disputes** — анализ practice по налоговым спорам
- **ip-law/infringement-triage** — поиск аналогичных IP cases в СИП
- **public-procurement/biased-tender-detection** — historical disputes по
  тендерам конкретного заказчика

## Installation

```bash
cd mcps/kad
pip install -e ".[dev]"
```

## Run

```bash
kad-mcp  # starts MCP server over stdio
```

## Limitations

**kad.arbitr.ru не имеет официального публичного API.** Этот MCP использует
JSON endpoints, доступные через анonymous browsing. У них есть:

- **Anti-bot защита** — частые requests блокируются (HTTP 403)
- **Rate limiting** — semaphore set to 3 concurrent connections
- **Cookie-based sessions** — иногда нужно session cookie management
- **Captchas** — при подозрительной активности

**Для production volumes рекомендуется:**

- **СПАРК-Маркетинг** (interfax.spark) — paid feed kad.arbitr + ЕГРЮЛ + другое
- **Контур.Фокус** — Контур.Бизнес ecosystem, paid
- **Casebook.ru** — специализированный legal-tech provider
- **Custom scraping infrastructure** — Playwright / Selenium + proxy rotation

В development / low-volume scenarios этот MCP работает.

## Configuration

В рамках ru-legal pack используется через `registry.json`:

```json
{
  "id": "kad",
  "path": "../mcps/kad",
  "command": ["python", "-m", "kad_mcp.server"],
  "requires_auth": false,
  "status": "mvp"
}
```

## License

Apache 2.0
