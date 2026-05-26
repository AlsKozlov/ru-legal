---
name: matter-update
description: >
  Добавить событие к существующему matter — timestamped в history.md + refresh
  _log.yaml row. Используй когда пользователь говорит "обнови дело X", "записать
  событие в matter", "новое решение по матерy", или после: суд.заседания, получения
  документа от counterparty, изменения posture, settlement event, или critical
  deadline.
argument-hint: "[slug | название matter'а] [тип события]"
user_invocable: true
ported_from: litigation-legal/matter-update
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /matter-update

## Назначение

Update matter после событий — это event ledger дела. На основании событий
агрегируется portfolio status.

## Workflow

### Шаг 1. Identify matter

Если не указан slug — list active matters из `_log.yaml` и попроси выбрать.

### Шаг 2. Тип события

| Тип | Что вкладывается |
|-----|-------------------|
| `hearing` | Суд.заседание состоялось — outcome + next steps |
| `filing` | Поданы / получены документы |
| `discovery` | Этап обмена доказательствами (АПК ст.66) |
| `settlement-offer` | Settlement предложение получено/отправлено |
| `settlement-event` | Settlement подписан / отклонён |
| `decision` | Решение суда вынесено |
| `appeal` | Апелляция / кассация / надзор поданы или получены |
| `deadline-shift` | Изменился срок (например, продлили) |
| `posture-change` | Изменилась стратегия (settle / defend / withdraw) |
| `personnel-change` | Сменился lead attorney / outside counsel |
| `oc-communication` | Существенная переписка с outside counsel |
| `notice` | Получено уведомление от регулятора / суда |
| `escalation` | Эскалировано к GC / CEO / Board |
| `other` | Прочее |

### Шаг 3. Capture details

Для каждого события:
- **Date** (DD.MM.YYYY)
- **Author** (кто записывает)
- **Description** (что произошло, 1-3 предложения plain Russian)
- **Documents** (paths к relevant docs если есть)
- **Impact:** изменилось ли что-то в matter (risk, exposure, posture, key dates)?
- **Next action** (если есть — что делать дальше)
- **Owner** для next action

### Шаг 4. Settlement acceptance gate

Для типов `settlement-offer` / `settlement-event`:

**Если roль PROFILE.md `## Кто пользуется → Роль` = Non-lawyer:**

> "Подписание / acceptance settlement имеет legal consequences. Подтверждено ли с
> attorney + GC? Если нет — pause, прежде чем записать как accepted, и получи
> sign-off."

### Шаг 5. Write to history.md

Append к `~/.ru-legal/profiles/litigation/matters/[slug]/history.md`:

```markdown
## [DD.MM.YYYY] [тип события]
**Автор:** [имя]
**Описание:** [...]

**Документы:**
- [path1]
- [path2]

**Impact:** [что изменилось / не изменилось]
**Next action:** [действие]
**Owner:** [имя]
```

### Шаг 6. Refresh _log.yaml row

Update полей:
- `last_updated_at: YYYY-MM-DD`
- `next_deadline` (если изменился)
- `next_deadline_desc`
- `risk_rating` (если impact показывает escalation)
- `status` (если closed / settled / on_hold)

### Шаг 7. Trigger downstream

Если impact = "next deadline soon" — recommend `/litigation:matter-briefing` для
обновления статуса.

Если impact = "settlement accepted" — recommend `/litigation:matter-close` workflow.

---

## РФ-specific event types

- **`vnp-act-received`** — акт выездной налоговой проверки получен → срок 1 мес на
  возражения (НК ст.100 ч.6)
- **`koap-protocol-received`** — протокол КоАП → 15 дней на возражения
- **`pretensia-deadline-passed`** — 30-дневный срок ответа на досудебку истёк
  (АПК ст.4) → можно подавать иск
- **`isk-davnost-warning`** — приближается срок исковой давности (ст.196 ГК), 30
  дней до истечения

---

## Attribution

Adapted from [`litigation-legal/matter-update`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/matter-update/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:**
- Event types расширены для РФ (vnp-act, koap-protocol, pretensia-deadline,
  isk-davnost)
- Discovery → АПК ст.66 (истребование доказательств)
- Settlement gate под РФ legal advice context

**Path:** → `~/.ru-legal/profiles/litigation/matters/[slug]/`

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.
**Adapted by:** ru-legal contributors, 2026-05-18.

---

## Disclaimer

Update — utility. Не legal advice. Decisions (settlement, posture change) — за
lead attorney.

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
