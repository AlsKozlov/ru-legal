---
name: investigation-add
description: >
  Add fact / interview / document / decision к existing investigation. Routes
  по типу: fact → facts.md timeline, interview → interviews/[name].md,
  evidence → evidence/ + log, decision → status.md.
argument-hint: "[matter-id] [type: fact|interview|evidence|decision]"
user_invocable: true
ported_from: employment-legal/investigation-add
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /investigation-add

## Назначение

Append к расследованию: новый факт в timeline, interview notes, attached evidence,
status update. Каждый тип сохраняется в свой sub-file.

## Workflow

### Шаг 1. Identify matter

Если matter-id не указан — ask:
> Какое расследование? Доступные: [list из ~/.ru-legal/labor/investigations/]

### Шаг 2. Identify type

| Type | Куда писать | Format |
|------|-------------|--------|
| `fact` | `facts.md` (append timeline entry) | дата + факт + источник |
| `interview` | `interviews/[witness].md` | timestamp, ФИО, role, Q&A |
| `evidence` | `evidence/[filename]` + log в README index | копия документа + описание |
| `decision` | `status.md` + appendto README "Next steps" | дата + decision + rationale |
| `objяснение` | `evidence/explanation-[YYYY-MM-DD].md` | дословный текст объяснения работника |

### Шаг 3a. Fact entry

```markdown
## [DD.MM.YYYY HH:MM] — [short description]

**Источник:** [docнт / interview / system log]

**Содержание:**
[detailed fact, по возможности дословно]

**Подтверждается:**
- Документ: evidence/[file]
- Свидетель: [имя]
- Другое:

**Tags:** [#harassment #financial #safety etc.]

**Logged by:** [user] @ [timestamp]
```

### Шаг 3b. Interview entry

```markdown
# Interview — [ФИО] ([role: complainant / subject / witness])

- **Дата:** [DD.MM.YYYY]
- **Время:** [HH:MM — HH:MM]
- **Место:** [office / video / phone]
- **Присутствовали:** [investigator, представитель работника (право по ст.193 если дисциплинарка)]
- **Privilege framing:** [если outside-адв ФПА — privileged communication]

## ⚠ РФ caveat

- Working hours — interview в рабочее время, иначе требует согласия / оплаты сверхурочных
- Работник имеет право на представителя (профсоюз / адвокат)
- При дисциплинарке — formal запрос объяснения отдельно (ст.193 ч.1 ТК), не заменяется interview

## Notes

### Background

[role, tenure, reporting line]

### Q&A

**Q:** ...
**A:** ...

**Q:** ...
**A:** ...

### Demeanor / observations

[only факты, no conclusions yet — это в memo]

### Documents referenced

- [doc 1]
- [doc 2]

### Follow-ups needed

- [ ] ...
```

### Шаг 3c. Evidence

1. Copy file → `evidence/[descriptive-name].[ext]`
2. Calculate SHA256 hash → log (для chain of custody)
3. Add к README index с описанием

```markdown
- `[file]` — [описание], SHA256: [hash], добавлено [DD.MM.YYYY HH:MM] by [user]
```

### Шаг 3d. Decision / status update

```markdown
## [DD.MM.YYYY] — [decision short title]

**Decision:** [что решено]

**Rationale:** [почему]

**Supporting evidence:**
- [link]

**Next actions:**
- [ ] [action 1, owner, deadline]

**Decided by:** [ФИО, role]
```

### Шаг 4. Update timeline

После любого add — update README.md `Last updated:` field + status.md.

## РФ-specific reminders

### Дисциплинарка clock check

При каждом add — если это дисциплинарный matter:
- Если приближаемся к 1-мес сроку с обнаружения (ст.193) → flag urgent
- Если приближаемся к 6-мес сроку с совершения → flag critical

### Объяснение запрошено?

Если subject ещё не дал объяснение и matter — потенциальная дисциплинарка:
- Reminder: запросить объяснение под подпись (срок 2 раб.дня)
- Без этого — взыскание оспоримо

## Attribution

Adapted from [`employment-legal/investigation-add`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/investigation-add/SKILL.md)
by Anthropic (Apache 2.0).

**Категория A:** добавлен `объяснение` как отдельный type (РФ-specific — ст.193 ТК), РФ caveat по interview practice (профсоюз / адвокат, рабочее время).

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
