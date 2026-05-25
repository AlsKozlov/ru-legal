---
name: oc-status
description: >
  Weekly status emails к outside counsel — per-matter skeletons → markdown output
  + email drafts. Используй когда пользователь говорит "weekly OC update",
  "запросить статус у advocate", "что нового от внешних юристов".
argument-hint: "[--matter <slug> | --all-active] [--since <date>]"
user_invocable: true
ported_from: litigation-legal/oc-status
ported_at: 2026-05-18
adaptation_category: A
---

# /oc-status (status emails outside counsel)

## Назначение

In-house юристам нужно регулярно syncаться с outside counsel (внешние адвокаты).
Этот skill drafт'ит status request emails для всех active matter'ов с внешним
counsel.

## Workflow

### Шаг 1. Load matters

Read `_log.yaml` — filter:
- `status: active`
- `outside_counsel` не empty

Если `--matter` указан — только этот matter.

### Шаг 2. Для каждого matter

Read:
- `matter.md` (last status)
- `history.md` (last events)

Извлеки:
- Что мы знаем по последнему update'у
- Что нам нужно знать (next deadline approaching, open questions)

### Шаг 3. Draft email

```markdown
**To:** [outside counsel email]
**From:** [in-house attorney]
**Subject:** [Matter name] — статус на [DD.MM.YYYY]

Уважаемые коллеги,

Прошу обновить статус по делу [Matter name] / Slug [slug].

Конкретно интересует:

1. **Текущая фаза** — где мы сейчас (досудебка / иск подан / discovery / suд /
   appeal / settlement negotiation)?
2. **Last action** — что сделано с [date нашего last update']?
3. **Next deadline** — что и до какой даты?
4. **Open questions** для нас:
   [Если есть конкретные — list. Если нет — generic "что от нас требуется?"]
5. **Risk update** — изменился ли ваш view на исход / экспозицию?
6. **Recommended posture** — продолжаем текущий подход / стоит ли settle / другое?

**Когда удобно созвониться?** Доступны [варианты] — 30-минутный slot достаточно.

Спасибо,
[Имя]
[Должность]
[Контакт]
```

### Шаг 4. Custom additions по matter context

| Если matter тип | Добавь spec вопросы |
|-----------------|--------------------|
| Налоговый (НК) | Изменилась ли позиция ФНС? Есть новые письма Минфина / ФНС? |
| Антимонопольный (ФАС) | Public hearings назначены? Media presence? |
| Банкротство (127-ФЗ) | Включение в реестр требований — где этап? |
| Trade dispute через МКАС | Tribunal сформирован? Свидетели подтверждены? |
| Корпоративный | Внутренние корпоративные действия (собрания, решения) — требуется? |
| Уголовный экономический | Контакт с следователем — изменения? Меры пресечения? |

### Шаг 5. Output

Draft emails в:
- `matters/[slug]/oc-status-request-[DD.MM.YYYY].md` (markdown)
- Если Gmail / email MCP подключён — draft directly в outbox (без отправки)

### Шаг 6. Aggregate weekly report

После запросов — когда ответы приходят — agregate в weekly summary:

```markdown
# OC Status — Week of [DD.MM.YYYY]

| Matter | OC | Last contact | Status | Next deadline |
|--------|-----|--------------|--------|---------------|
| ... | ... | ... | ... | ... |

## Updates received this week

[Краткое summary по каждому matter где пришли updates]

## Pending responses

[OC ещё не ответили]

## Concerns

[Если по тону или content'у update'ов есть concerns]
```

---

## РФ-specific patterns

### Адвокатская тайна (ФЗ-63)

Communications между in-house и outside counsel (если outside — **адвокат с
удостоверением ФПА**) — защищаются адвокатской тайной. Это важно для:
- Email маркировки (можно add "Адвокатская тайна" header)
- Storage (не shared с другими отделами без необходимости)

In-house привилегии нет — но при работе с adv ФПА — есть.

### Биллинг attention

В РФ типично почасовые ставки 5,000-30,000 руб/час для quality OC. Periodic
status requests — это **billable time**. Не отправляй request чаще раз в 2 недели
без cause, иначе будет overhead.

---

## Attribution

Adapted from [`litigation-legal/oc-status`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/oc-status/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:**
- РФ-specific custom additions по типам дел (налоговые, антимонопольные, банкротство,
  МКАС)
- Адвокатская тайна context — when applicable
- Биллинг attention noted

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## Disclaimer

Drafts — utility. Не legal advice. Все emails review'ятся live attorney перед
отправкой.

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
