---
name: investigation-query
description: >
  Query existing investigation — найти факты / документы / интервью по теме,
  свидетелю, дате, тегу. Read-only: не пишет, не суммирует. Quick lookup
  во время drafting memo или briefing.
argument-hint: "[matter-id] [query string]"
user_invocable: true
ported_from: employment-legal/investigation-query
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /investigation-query

## Назначение

Быстрый поиск по materials расследования. Read-only — не drafts, не concludes,
не updates статус. Просто returns relevant excerpts.

Используется во время:
- Drafting `/investigation-memo`
- Подготовки `/investigation-summary` для stakeholders
- Reviewing perspective subject перед interview
- Tracking commitments / next-steps

## Workflow

### Шаг 1. Identify matter + query

Если matter-id не указан → ask который из активных.

Query types:
- **Текст:** "что Иванов говорил про bonus?"
- **По свидетелю:** "all interviews с Петрова"
- **По дате:** "что произошло между 10.03 и 20.03?"
- **По теме / tag:** "все упоминания финансовых нарушений"
- **По документу:** "ссылки на договор № 45"
- **Status check:** "что ещё нужно сделать?"

### Шаг 2. Search across matter files

Files в matter folder:
- `intake.md`
- `facts.md`
- `interviews/*.md`
- `evidence/` (только filenames + descriptions из README — не reads attached docs)
- `status.md`
- `memo.md` / `summary.md` (если уже drafted)

### Шаг 3. Return results

#### Format: relevant excerpts с context

```markdown
## Query: "что Иванов говорил про bonus?"

### From interviews/ivanov.md (15.03.2026):

> Q: Кто принимал решение по bonus pool на Q4?
> A: Это всегда CFO утверждает, но в этом квартале CEO напрямую сказал
>    "перераспределить" в пользу sales. Я не знаю причину.

> Q: Вы видели emails об этом?
> A: Да, был email от 22.02.2026 — но я не помню точно содержание.

### From facts.md (timeline):

- 22.02.2026 — email CEO → CFO, тема "bonus reallocation Q4" (см. evidence/email-2026-02-22.eml)
- 25.02.2026 — bonus distribution выпущена с новыми пропорциями

### From evidence:

- `email-2026-02-22.eml` — email цепочка, addresses bonus reallocation
- `bonus-distribution-q4.xlsx` — финальный список

### Related followups:

- [open] interview CFO про rationale (status.md)
```

### Шаг 4. Suggest next actions (если очевидно)

```markdown
## Suggested follow-ups

- Иванов упоминает email от 22.02 — мы его уже в evidence/ ✓
- Не interviewed CFO ещё — это relevant для понимания decision flow
```

## РФ-specific query patterns

### Дисциплинарка clock query

> "Сколько времени осталось по ст.193?"

→ Returns:
- Дата обнаружения: DD.MM.YYYY
- Дата совершения: DD.MM.YYYY
- 1-мес срок истекает: DD.MM.YYYY (осталось X дней)
- 6-мес срок истекает: DD.MM.YYYY (осталось X дней)
- Объяснение запрошено: Y/N
- Если N — обязательно до взыскания

### Privilege check query

> "Какие документы под privilege?"

→ Returns documents created by / containing communications с outside-адв ФПА. Flag in-house lawyer involvement (НЕ privileged в РФ).

### Свидетели / профсоюз check

> "Кто из работников может быть профсоюзным представителем?"

→ List witnesses + ИО членов профсоюза (если info в profile).

## Что НЕ делает

- Не drafts memo (это `/investigation-memo`)
- Не creates summary (это `/investigation-summary`)
- Не updates статус (это `/investigation-add`)
- Не reads attached binary docs (PDF, DOCX) — только filenames + descriptions

## Attribution

Adapted from [`employment-legal/investigation-query`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/investigation-query/SKILL.md)
by Anthropic (Apache 2.0).

**Категория A:** добавлены РФ-specific query patterns (дисциплинарка clock, privilege check для РФ, профсоюз).

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## ⚠ Юридический disclaimer

Данный skill — **техническая платформа**, не оказывает юридических услуг по ст.2
ФЗ-63 «Об адвокатской деятельности». Outputs **не заменяют** консультацию
лицензированного юриста / адвоката ФПА.

AI может галлюцинировать, выдавать устаревшие нормы, неверно интерпретировать
факты. Material decisions (увольнение, M&A, налоговый спор, IP litigation) —
**обязательно** engage outside-адв ФПА с релевантной специализацией.

Проект `ru-legal` и его contributors не несут ответственности за решения,
принятые на основе outputs системы. Использование — на свой риск.
