# cbr-mcp

> MCP server для ЦБ РФ — банковский справочник, курсы валют, ключевая ставка, расчёт пеней.

**Status:** 🟢 GREEN — endpoints протестированы, работают без auth.

## Что внутри

5 tools:

| Tool | Описание |
|---|---|
| `get_exchange_rates(date_iso=None)` | Все курсы валют на дату (USD/EUR/CNY/...) |
| `get_exchange_rate(currency, date_iso=None)` | Курс одной валюты |
| `get_key_rate()` | Текущая ключевая ставка ЦБ РФ |
| `lookup_bank_by_bic(bic)` | Справочник БИК (название банка + корр.счёт + адрес) |
| `calculate_penalty(amount, days, basis)` | Расчёт пеней по НК ст.75 или ГК ст.395 |

## Источники данных

- `https://www.cbr.ru/scripts/XML_daily.asp` — курсы валют (XML)
- `https://www.cbr.ru/scripts/XML_keyrate.asp` — ключевая ставка
- `https://www.cbr.ru/scripts/xml_bic.asp` — справочник БИК

Все endpoints **публичные, без auth, без rate limits** (рекомендуется не более 5 req/s).

## Установка

```bash
cd mcps/cbr
uv venv && source .venv/bin/activate
uv pip install -e .
```

## Подключение к Claude Code / Cursor

`.mcp.json`:
```json
{
  "mcpServers": {
    "cbr": {
      "command": "uvx",
      "args": ["cbr-mcp"]
    }
  }
}
```

## Пример использования

В skill можно вызывать так:

```markdown
### Шаг: Расчёт пеней по налоговой задолженности

Через `cbr.calculate_penalty(principal_amount=user.debt, days_overdue=user.days, rate_basis="key_rate")`
получи расчёт пеней по ст.75 НК РФ.
```

LLM получит:
```json
{
  "penalty": 1234.56,
  "principal_amount": 100000,
  "days_overdue": 30,
  "key_rate_percent": 16.0,
  "legal_basis": "НК РФ ст.75",
  "formula": "100000 × (16.0% / 300) × 30",
  "verified": "cbr-mcp:get_key_rate"
}
```

## Тестирование

```bash
pytest tests/
```

Smoke test:
```bash
python -c "
import asyncio
from cbr_mcp.server import get_key_rate
print(asyncio.run(get_key_rate.fn()))
"
# → KeyRateRecord(rate=16.0, effective_date='2025-12-15')
```

## Ограничения

- Cache 1 час — для быстрых пересчётов
- При недоступности cbr.ru → возвращает кешированное значение (если есть), иначе error

## Лицензия

Apache 2.0 (общая лицензия ru-legal).
