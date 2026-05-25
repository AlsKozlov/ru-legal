# Examples

Три realistic end-to-end сценария использования `ru-legal`.

| # | Сценарий | Skills | MCPs | Кто использует |
|---|----------|--------|------|----------------|
| [1](01-vendor-dd.md) | DD контрагента перед сделкой | `corporate-law/diligence-issue-extraction` | egrul, kad, efrsb, rospatent | In-house GC, юрист сделок |
| [2](02-termination-review.md) | Анализ увольнения по сокращению | `labor-law/termination-review` | pravo | HR-юрист, in-house |
| [3](03-ddu-review.md) | Review договора долевого участия | `real-estate/ddu-review` | pravo, efrsb | Юрист по недвижимости, физ.лицо-покупатель |

## Как читать examples

Каждый файл содержит:
1. **Контекст** — кто, зачем, что нужно
2. **User prompt** — как юрист обращается к Claude / GigaChat
3. **Tool calls** — какие MCPs LLM зовёт под капотом
4. **Output** — пример reasonable response

Это **не реальные кейсы** (данные fictional), но показывают типичный flow.

## Запуск

### В Claude Code (зарегистрирован plugin)

Просто введи slash-команду из примера:

```
/diligence-issue-extraction 7707000001
```

### Через Telegram-бот (apps/telegram_bot)

```
/dd 7707000001
```

### Через прямой MCP call (Cursor / Continue)

В Cursor открой чат, упомяни нужный MCP tool:

```
@mcp:efrsb проверь ИНН 7707000001 на банкротство
```
