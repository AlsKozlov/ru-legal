# Contributing to ru-legal

Спасибо что хочешь contribute! Этот проект — community driven, и любая помощь ценна.

## Quick start

### 1. Самые ценные contributions сейчас

| Что | Сложность | Impact |
|-----|:---------:|--------|
| 🐛 **Feedback от практикующего юриста** на конкретный skill | ⭐ | 🔥🔥🔥 |
| 📝 **Новый skill** в существующий pack | ⭐⭐ | 🔥🔥 |
| 🔌 **Новый MCP** (ФАС / ФССП / РКН реестры) | ⭐⭐⭐ | 🔥🔥🔥 |
| 📦 **Новый pack** (банкротство / страхование / ВЭД) | ⭐⭐⭐⭐ | 🔥🔥🔥 |
| 📖 **README / docs** улучшения | ⭐ | 🔥 |
| 🔧 **Bug fixes** | ⭐⭐ | 🔥🔥 |
| 🌐 **Adapter** (LangChain / OpenAI / etc.) | ⭐⭐⭐ | 🔥 |

## Как сделать contribution

### Шаг 1. Discuss before code

Для всего что больше typo-fix — **открой issue или discussion** до начала работы. Можем сразу обсудить approach.

### Шаг 2. Fork + branch

```bash
git clone <repo-url>
cd ru-legal
git checkout -b feat/my-contribution
```

### Шаг 3. Зависимости

```bash
# Для skills работы — ничего не нужно, это просто Markdown
# Для MCP / harness работы:
pip install -e ".[dev]"
```

### Шаг 4. Test

```bash
# Если изменял Python код
ruff check .
pytest

# Если добавил новый skill
python scripts/validate_skills.py
```

### Шаг 5. PR

- Маленький focused PR > big monolith PR
- Описание в PR: что меняется + зачем + как тестировал
- Linked issue если есть

## Как добавить новый skill

### Структура pack

```
packs/<pack-name>/
├── pack.yaml           # манифест pack
├── PROFILE.md          # template профиля
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

### Template SKILL.md

```markdown
---
name: my-new-skill
description: >
  Одно предложение — что делает skill + для каких юристов.
argument-hint: "[путь к файлу или описание входа]"
user_invocable: true
ported_from: null  # ИЛИ commercial-legal/source-skill если порт
ported_at: 2026-MM-DD
adaptation_category: D  # A (light) / B (medium) / C (heavy) / D (RU-unique)
---

# /my-new-skill

## Назначение

[2-3 предложения — конкретно что делает, для кого, какое value]

## Pre-flight

- [Что должно быть готово до запуска]
- [Какие inputs ожидаются]

## Workflow

### Шаг 1. ...

[Конкретные actions]

### Шаг 2. ...

## Output

[Что возвращается — structure]

## Что НЕ делает

[Скоуп limitations — что НЕ замещает live юриста]

## Правовая основа

- ст. X.X ГК / ФЗ-XX / Постановление №NNN
- Постановление Пленума ВС РФ № X от DD.MM.YYYY
```

### Quality checklist для нового skill

- [ ] Cites конкретные нормы (статьи + номера ФЗ)
- [ ] Не дублирует existing skill в том же pack
- [ ] Имеет concrete output format
- [ ] Имеет "Что НЕ делает" секцию
- [ ] Если порт от Anthropic — указано `ported_from:` + Attribution секция
- [ ] **Disclaimer** автоматически добавится через `scripts/add_disclaimer.py`
- [ ] Зарегистрирован в `packs/<pack>/pack.yaml`

## Как добавить MCP

См. existing `mcps/pravo/` как reference structure:

```
mcps/<mcp-name>/
├── pyproject.toml
├── README.md
└── src/
    └── <mcp_name>_mcp/
        ├── __init__.py
        └── server.py     # main file
└── tests/
    └── test_server.py
```

Boilerplate:

```python
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

mcp = FastMCP(
    name="my-mcp",
    instructions="Когда и зачем использовать этот MCP",
)

@mcp.tool(annotations={"readOnlyHint": True})
async def search_something(query: str) -> list[dict]:
    """Подробное описание для LLM."""
    # ... твоя логика
    return results

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

### MCP quality checklist

- [ ] Все tools имеют `readOnlyHint` / `idempotentHint` annotations
- [ ] Все tools имеют typed Pydantic Field descriptions
- [ ] Errors через `ToolError` с human-readable message (не raw HTTP errors)
- [ ] Логи в stderr (НЕ stdout — stdout для MCP протокола)
- [ ] Cache + rate limiting
- [ ] Tests с respx (mock HTTP)
- [ ] README объясняет limitations + use cases
- [ ] Зарегистрирован в `packs/registry.json` → `mcps` array

## Code style

### Python

- Python 3.11+
- `ruff` formatting (см. existing pyproject.toml)
- Type annotations везде
- Docstrings для public functions / tools
- Без `# type: ignore` без объяснения

### Markdown (skills)

- Headers H2 (`##`) для основных секций
- Tables для structured data (не bullet lists)
- Code blocks с language hint (```python, ```markdown, ```bash)
- Цитаты норм в backticks: `ст.81 ТК`, `ст.452 ГК`
- Bilingual mix OK (русский + английские технические термины)

## Что **не нужно** делать

- ❌ Не открывай PR с 50+ файлами без discussion
- ❌ Не переписывай существующий skill полностью без согласования
- ❌ Не добавляй dependencies без обоснования
- ❌ Не делай breaking changes к public API без deprecation
- ❌ Не убирай attribution к Anthropic в ported skills

## Code of Conduct

См. [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). TL;DR — будь полезным, уважай других, фокус на улучшении проекта.

## Recognition

Все contributors указываются в [CONTRIBUTORS.md](CONTRIBUTORS.md). PRs с твоим именем + краткое описание contribution.

## Вопросы

Открой issue в репозитории. Контакты maintainer'ов будут добавлены позже.

Спасибо!
