---
name: matter-close
description: >
  Закрытие matter'а — capture outcome, update _log.yaml status:closed, append
  closing block в history.md и matter.md. Используй когда matter завершён:
  settlement подписан, решение вступило в силу, withdrawal, dismissal, или
  пользователь говорит "закрой matter X".
argument-hint: "<slug>"
user_invocable: true
ported_from: litigation-legal/matter-close
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /matter-close

## Назначение

После окончания дела — formal closing записывает outcome и lessons learned, для
будущего reference.

## Workflow

### Шаг 1. Confirm matter ready для close

Не закрывать если:
- Settlement подписан, но средства не выплачены
- Решение вступило в силу но appeal еще возможен (срок не истёк)
- В active discovery / pleading stage

Если есть doubt — спроси: "Готов закрыть, или подождать [X]?"

### Шаг 2. Capture outcome

| Outcome | Что зафиксировать |
|---------|-------------------|
| `won-judgment` | Решение в нашу пользу — сумма взыскания, исполнительный лист получен? |
| `lost-judgment` | Решение против нас — сумма, обжалуем? |
| `settled-paid` | Settlement подписан + выплачено — условия, сумма |
| `settled-unpaid` | Settlement подписан но не выплачено — risk note |
| `withdrawn` | Иск отозван — кем (нами / истцом), причина |
| `dismissed` | Прекращено судом — основание |
| `transferred` | Передано другому суду — куда, почему |
| `escalated-criminal` | Перешло в уголовное — handoff |
| `lapsed` | Срок исковой давности истёк |
| `voluntary-resolved` | Resolved до иска (settlement до подачи) |
| `other` | Прочее |

### Шаг 3. Financial summary

- **Total exposure realized:** [сумма реально взысканная / уплаченная]
- **Outside counsel fees:** [сумма / hours]
- **Internal time invested:** [приближённо часов]
- **Settlement / judgment amount:** [сумма]
- **Net economic outcome:** [для нас плюс / минус Y руб]

### Шаг 4. Lessons learned

Краткие notes для портфельной памяти:

- **Что сработало:** [strategy / argument / evidence что зашло]
- **Что не сработало:** [что не зашло / mistake]
- **Counterparty pattern:** [про их poведение / negotiation style]
- **Outside counsel performance:** [если был — recommend / not recommend для
  будущих похожих кейсов]
- **Process improvements:** [что бы сделали иначе]

### Шаг 5. Update files

**matter.md** — append closing section:

```markdown
---

## Closing — [DD.MM.YYYY]

**Outcome:** [outcome type + details]
**Final financial:** [см. Шаг 3]
**Lessons learned:** [см. Шаг 4]
**Closing approved by:** [имя — обычно lead attorney + GC]
```

**history.md** — последняя запись:

```markdown
## [DD.MM.YYYY] CLOSE
**Автор:** [имя]
**Outcome:** [type]
**Описание:** [одно-два предложения]
```

**_log.yaml** — обновить row:

```yaml
status: closed
closed_at: YYYY-MM-DD
outcome: <тип outcome>
financial_outcome: <сумма для нас в руб>
closing_approved_by: <имя>
```

### Шаг 6. Archive / preservation

После close:
- **Matter folder перемещается в** `~/.ru-legal/profiles/litigation/matters/_archived/<slug>/`
- **Документы preserved** — НЕ удаляем сразу (возможны related matters, regulatory
  inquiries, тax audit вопросы)
- **Retention rule:** держать **минимум 5 лет** после close (общая практика
  бухгалтерских / договорных archives — 402-ФЗ)
- Для **налоговых споров** — 4 года (НК ст.23) после закрытия налогового периода
- Для **трудовых споров** — 75 лет (личные дела работников по приказу Росархива)

### Шаг 7. Trigger handoffs

- Если outcome = `settled-unpaid` или `won-judgment` без получения → handoff к
  collections / исполнительное производство (ФЗ-229)
- Если outcome = `escalated-criminal` → handoff к external criminal counsel
- Если outcome = `regulatory-impact` → handoff к compliance team

---

## РФ-specific outcomes

| Тип | Особенность |
|-----|-------------|
| `won-judgment` + **исполнительное производство** | Подача исп.листа в ФССП — отдельный этап |
| Trade dispute settled через **МКАС** | Признание решения МКАС в РФ — отдельная процедура |
| **Налоговый спор** won | Возврат переплаты — через ФНС, отдельный процесс |
| Settlement через **mediator** | Медиативное соглашение по 193-ФЗ |
| **Банкротство** counterparty | Включение в реестр требований кредиторов — отдельный workflow |

---

## Attribution

Adapted from [`litigation-legal/matter-close`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/matter-close/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:**
- Outcome types дополнены РФ-specific (lapsed, voluntary-resolved, escalated-criminal)
- Retention rules — по РФ нормам (402-ФЗ, НК, Росархив)
- Handoffs к ФССП, МКАС, реестр кредиторов 127-ФЗ

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## Disclaimer

Closing — utility. Не legal advice. Final approval за lead attorney + GC.

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
