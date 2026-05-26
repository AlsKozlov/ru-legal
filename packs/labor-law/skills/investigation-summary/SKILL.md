---
name: investigation-summary
description: >
  Audience-specific summary of investigation для stakeholder briefing —
  CEO / HR director / профсоюз / external counsel / regulator. Adjusts
  detail level, privilege framing, и legal context per audience.
argument-hint: "[matter-id] [audience]"
user_invocable: true
ported_from: employment-legal/investigation-summary
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /investigation-summary

## Назначение

Generate audience-specific briefing summary из investigation materials. **Не** drafts
legal memo — это `/investigation-memo`. Summary — для stakeholder consumption.

## Audiences и адаптация

| Audience | Detail | Privilege framing | Tone |
|----------|--------|-------------------|------|
| CEO / topmgmt | High-level findings + business impact + ask | Privileged через outside-адв ФПА (если возможно) | Decision-focused |
| HR Director | Process compliance, дисциплинарка status, next steps | Internal — no outside privilege | Operational |
| Профсоюз | Только relevant к коллективному договору / правам работника | Public-facing | Formal, neutral |
| Outside-адв ФПА | Full disclosure, all evidence indexed | Privileged communication | Legal-detailed |
| Regulator (ГИТ / прокуратура) | Only what's обязательно disclose | Mind disclosure obligations | Formal, factual |
| Board / акционеры | Strategic risk + financial exposure | Через GC / outside-адв | Risk-framed |

## Workflow

### Шаг 1. Identify matter + audience

Audience выбор обязательный — определяет ВСЁ ниже.

### Шаг 2. Pre-flight РФ-checks

#### A. Privilege framing для РФ

Если audience requires privilege — **проверь:**
- Outside-адв ФПА involved с самого начала?
- Memo / выводы создавались адвокатом ФПА?
- Если **нет** outside-адв involvement — **НЕТ** privilege в РФ для in-house communications
- В summary — не делай assumption о privilege; явно укажи статус

#### B. ПДн в summary

Если subject / свидетели — поименно (ФИО, должность):
- Internal audiences — OK
- External (regulator / publication / cross-jurisdiction) — review ст.6 ч.1 152-ФЗ:
  есть ли законное основание для disclosure?
- Best practice: pseudonyms (Сотрудник A, Сотрудник B) если можно

#### C. Дисциплинарка timing

Если matter — потенциальная дисциплинарка:
- Always include current срок до истечения 1-мес / 6-мес periods (ст.193 ТК)
- Always flag whether объяснение работника запрошено

### Шаг 3. Generate summary per audience

#### Template A: CEO / topmgmt

```markdown
# Briefing: [matter description]

**Confidentiality:** [privileged через outside-адв / business-confidential / public]

## Bottom line (1 sentence)

[E.g. "Workplace harassment жалоба на регионального директора — substantiated
по 2 эпизодам, рекомендуем дисциплинарное взыскание + внутренний training."]

## Что произошло (3-5 bullets)

- [factual finding 1]
- [factual finding 2]
- ...

## Юридический / business risk

- **Если ничего не делать:** [exposure]
- **Если применить рекомендованное:** [residual risk]
- **Дедлайны:** [е.g. до DD.MM.YYYY по ст.193 ТК]

## Asks

- [ ] Approval of recommended action
- [ ] Budget for external advisor (если требуется)
- [ ] Communication plan stakeholders

## Что я НЕ исследовал

[scope limitations]
```

#### Template B: HR Director

```markdown
# Investigation [INV-XXX] — Operational summary

## Status

[Open / pending объяснение / memo draft / closed]

## Workflow checklist (ст.193 ТК если применимо)

- [x] Объяснение запрошено под подпись (DD.MM.YYYY)
- [x] 2 раб.дня прошли (DD.MM.YYYY) — объяснение получено / акт об отказе составлен
- [x] Доказательства собраны
- [ ] Приказ о взыскании в подготовке
- [ ] Срок ознакомления (3 раб.дня)

## Findings (operational)

[что произошло, без legal conclusion]

## Recommended HR actions

- [действие 1 — owner, timeline]
- ...

## Documentation status

- All interviews logged: Y/N
- Evidence chain of custody: complete / pending
- Privilege markings on docs: applied / pending
```

#### Template C: Профсоюз (если применимо)

```markdown
# Извещение профсоюзу — [matter description]

Уважаемые коллеги,

В соответствии с [ст.82 ТК — если сокращение / ст.374 если член профсоюза /
коллективный договор п.X] уведомляем о следующем:

## Существо обращения

[brief, neutral statement of facts]

## Принимаемые меры

[planned actions с указанием правовых оснований]

## Запрос мнения профсоюза (если требуется)

- В соответствии с [норма] просим предоставить мотивированное мнение в течение
  [срок — 7 раб.дней по ст.373 ТК]

С уважением,
[ФИО, должность]
```

#### Template D: Outside-адв ФПА

```markdown
# Privileged & Confidential

# Briefing — [matter description]

**Prepared for:** [ФИО адвоката, удостоверение N, ордер N]
**Privilege basis:** Адвокатская тайна (ФЗ-63 ст.8)
**Author:** [In-house / corporate counsel]

## Full materials index

- [intake.md](intake.md)
- [facts.md](facts.md)
- [interviews/...](interviews/)
- [evidence/...](evidence/)
- [memo.md](memo.md)

## Specific asks

- [ ] Recommendation on potential litigation exposure
- [ ] Review draft приказа о взыскании
- [ ] Privilege review всех materials
- [ ] Strategy: if subject sues — restoration risk?

## Materiality / urgency

[дедлайны, sums at stake, public exposure risk]
```

#### Template E: Regulator (ГИТ / прокуратура)

```markdown
# Ответ на запрос [ГИТ / прокуратуры] № [N] от [DD.MM.YYYY]

В ответ на ваш запрос сообщаем следующее.

## По существу

[ТОЛЬКО запрошенные факты — не volunteering additional info]

## Прилагаемые документы

1. [doc 1 — относится к запросу пункт N]
2. ...

## Сведения, не подлежащие предоставлению

[Если что-то — банковская/налоговая/коммерческая тайна — отдельным письмом,
с правовым основанием отказа]

Подпись, дата.
```

### Шаг 4. Review checklist перед отправкой

- [ ] Audience-appropriate detail level
- [ ] Privilege framing correct для РФ context
- [ ] ПДн handling compliant (152-ФЗ ст.6)
- [ ] Дисциплинарка timing flagged (если применимо)
- [ ] No legal conclusions если audience не legal-trained
- [ ] Footer с timestamp, author, version

## Attribution

Adapted from [`employment-legal/investigation-summary`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/investigation-summary/SKILL.md)
by Anthropic (Apache 2.0).

**Категория A:** audience list заменён РФ-realities (профсоюз, ГИТ, outside-адв ФПА вместо US generic "outside counsel"), privilege framing strictly по РФ (in-house = НЕ privileged), templates для каждой audience.

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
