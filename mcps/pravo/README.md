# pravo-mcp

MCP server для официального портала правовой информации РФ — [pravo.gov.ru](https://pravo.gov.ru).

Поиск НПА, получение текстов законов, версии на конкретную дату. **Без регистрации и API ключа** — использует публичный JSON API портала.

---

## Установка

```bash
# Запустить разово через uvx (рекомендуется)
uvx pravo-mcp

# Или установить и запускать вручную
pip install pravo-mcp
pravo-mcp
```

---

## Подключение к Claude Code

```bash
claude mcp add --transport stdio pravo -- uvx pravo-mcp
```

Или через `.mcp.json` в проекте:

```json
{
  "mcpServers": {
    "pravo": {
      "type": "stdio",
      "command": "uvx",
      "args": ["pravo-mcp"]
    }
  }
}
```

---

## Что умеет

| Tool | Назначение |
|------|-----------|
| `search_npa(query, doc_type?, date_from?, date_to?, limit?)` | Поиск НПА по названию / типу / дате |
| `get_npa(eid)` | Полный текст и метаданные документа по идентификатору |
| `get_npa_version_at_date(document_hash, on_date?)` | Редакция НПА на конкретную дату через ИПС |
| `list_document_types()` | Справочник типов документов |
| `list_signatory_authorities(block)` | Справочник органов-издателей |

Resources:
- `pravo://doc-types-cheatsheet` — справка по иерархии НПА РФ

---

## Примеры использования через Claude

```
>>> Найди закон о персональных данных
[вызывает search_npa(query="О персональных данных", doc_type="federal_law", limit=5)]

>>> Дай полный текст 152-ФЗ
[вызывает get_npa(eid=<eid из предыдущего поиска>)]

>>> Какая была редакция ст. 421 ГК РФ на 1 января 2024?
[вызывает get_npa_version_at_date(document_hash=<hash ГК>, on_date="2024-01-01")]
```

---

## Технические детали

- **Источник:** `publication.pravo.gov.ru/api/` (поиск, тексты) + `ips.pravo.gov.ru/api/ips/` (версионирование)
- **Транспорт:** stdio (для Claude Code, Claude Desktop, Cursor)
- **Кэширование:** 10 минут TTL в памяти процесса
- **Rate limit:** 5 одновременных запросов (защита от перегрузки источника)
- **Timeout:** 30 секунд per запрос

---

## Ограничения

- API портала **не имеет официальной документации** — структура ответов реверс-инжинирилась сообществом. При изменениях API возможны temporary failures.
- Тексты больших кодексов (ГК, НК) могут возвращаться в виде ссылки на PDF/XML, а не inline HTML — для таких случаев используй `pdfUrl` / `xmlUrl` поля из ответа.
- Региональные НПА не покрываются — только федеральные.

---

## Разработка

```bash
git clone <repo-url>
cd ru-legal/mcps/pravo
pip install -e ".[dev]"
pytest
```

Локально для Claude Code:

```bash
claude mcp add --transport stdio pravo-local -- python -m pravo_mcp.server
```

---

## License

Apache 2.0.
