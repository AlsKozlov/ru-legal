---
name: material-contract-schedule
description: >
  Identify + tabulate material contracts target для DD / disclosure schedules /
  ongoing contract management. Categories: customer, supplier, distribution,
  financing, lease, IP licensing, employment (key persons), joint ventures.
  РФ specifics: ст.609 регистрация аренды > 1 года, ст.1232 регистрация
  IP лицензий, ст.46 ФЗ-14 / ст.78 ФЗ-208 крупные сделки.
argument-hint: "[path к contracts directory / dataroom]"
user_invocable: true
ported_from: corporate-legal/material-contract-schedule
ported_at: 2026-05-19
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /material-contract-schedule

## Назначение

Generate Material Contracts Schedule — tabular list существенных договоров с key
terms. Use cases:
- DD disclosure schedule
- Annual material contract review
- Pre-M&A inventory
- Audit support

## Materiality definition (configurable per PROFILE)

Default thresholds (РФ-typical для mid-cap):

| Category | Material if |
|----------|-------------|
| Customer / supplier | Annual revenue / cost > 5% от target's revenue / COGS |
| Lease (недвижимость) | Annual rent > 5М руб OR strategic location |
| Loan / credit facility | Principal > 50М руб OR cross-default tied к material activities |
| IP license | Strategic OR royalty > 1М руб annual |
| JV / partnership | Все |
| Employment (key persons) | Top management (CEO, CFO, key engineers) + severance / equity provisions |
| Insurance (D&O, BBB, etc.) | Все significant policies |
| Settlement / litigation | Все ongoing OR resolved within last 3 years > 10M |
| Tax (rulings, agreements) | Все |

## Workflow

### Шаг 1. Inventory contracts (sources)

- Data room
- Contract management system
- ERP / accounting (для определения top suppliers / customers by volume)
- Бух.отчётность (для loans, leases)
- HR system (employment)
- Реестры (Роспатент для IP)

### Шаг 2. Apply materiality filter

Для каждого контракта → material? Yes → include in schedule.

### Шаг 3. Extract key terms (categorized)

```markdown
# Material Contracts Schedule — [Target name]
**Дата:** [DD.MM.YYYY]
**Reviewer:** [user]

## Customer contracts

| # | Контрагент | ИНН | Дата | Срок | Annual revenue (RUB) | Change-of-control | Assignment | Termination rights | Risk |
|---|------------|-----|------|------|----------------------|-------------------|------------|---------------------|------|
| 1 | ООО "Альфа" | 7707... | 15.01.2024 | до 14.01.2027 | 250М | consent required | restricted | for cause + 90 дн notice | 🟡 CoC requires consent |
| 2 | ... | | | | | | | | |

## Supplier contracts

| # | Контрагент | ИНН | Дата | Срок | Annual cost | Change-of-control | Termination | Risk |
|---|------------|-----|------|------|-------------|-------------------|-------------|------|
| ... | | | | | | | | |

## Lease agreements (недвижимость)

| # | Объект | Арендодатель | Площадь | Annual rent | Срок | Регистрация ЕГРН | Индексация | Risk |
|---|--------|--------------|---------|-------------|------|-------------------|------------|------|
| 1 | Москва, ул. ..., 100 м² | ООО "Бета" | 100 м² | 6М | до 31.12.2027 | да (запись N) | CPI ± 5% | 🟢 |

## Loans & credit facilities

| # | Кредитор | Сумма | Валюта | Ставка | Срок | Обеспечение | Ковенанты | CoC | Risk |
|---|----------|-------|--------|--------|------|-------------|-----------|-----|------|
| 1 | Сбербанк | 500М | RUB | КС+3% | до 2028 | залог недвижимости | Debt/EBITDA < 3.5 | termination on CoC | 🔴 will be triggered by M&A |

## IP licenses (target as licensor)

| # | Объект IP | Лицензиат | Тип | Территория | Royalty | Срок | Регистрация Роспатент | Risk |
|---|-----------|-----------|-----|------------|---------|------|------------------------|------|
| 1 | ТЗ № 123456 | ООО "Гамма" | неисключительная | РФ | 5% net sales | 5 лет | да | 🟢 |

## IP licenses (target as licensee — incoming)

| # | Объект IP | Лицензиар | Тип | Territory | Royalty | Срок | CoC clause | Risk |
|---|-----------|-----------|-----|-----------|---------|------|------------|------|
| 1 | ПО "X" | Microsoft Ireland | enterprise | worldwide | $50k/year | до 31.12.2026 | termination on CoC | 🔴 |

## JV / partnership agreements

| # | Партнёр | Структура | Доля | Срок | Exit rights | Tag/drag | Risk |
|---|---------|-----------|------|------|-------------|----------|------|
| ... | | | | | | | |

## Employment — key persons

| # | ФИО | Должность | Annual comp | Срок | Severance | Non-compete | IP assignment | Risk |
|---|-----|-----------|-------------|------|-----------|-------------|---------------|------|
| 1 | Иванов И.И. | CEO | 12М (оклад + бонус) | бессрочный | 12 окладов по соглашению | n/a (РФ unenforceable) | ст.1295 покрыто | 🟢 |

## Insurance

| # | Тип | Страховщик | Лимит | Премия | Срок | Risk |
|---|-----|------------|-------|--------|------|------|
| 1 | D&O | ВСК | 100М | 500k | до 31.12.2026 | 🟢 |

## Settlement & litigation (active или recent)

| # | № дела | Стороны | Предмет | Сумма | Стадия | Risk для target |
|---|---------|---------|---------|-------|--------|------------------|
| 1 | A40-XXX/2024 | ФНС vs target | НДС доначисление | 50М | первая инстанция | 🔴 high probability проигрыша |

## Tax matters

| # | Тип | Период | Сумма | Status | Risk |
|---|-----|--------|-------|--------|------|
| 1 | ВНП решение 2022-2023 | 2022-2023 | 30М | оспаривается в АС | 🟡 в апелляции |

## Aggregates

- Total material contracts identified: [N]
- Estimated aggregate annual value: [сумма] млрд руб
- 🔴 critical: [N] / 🟡 medium: [M] / 🟢 minor: [K]
- **CoC-triggering contracts:** [N] — list separately
- **Contracts requiring third-party consent for M&A:** [N]
- **Termination-on-CoC contracts:** [N]

## Change-of-control summary

Для M&A — critical to identify:

| # | Контрагент | Контракт | CoC trigger | Required action |
|---|------------|----------|-------------|------------------|
| 1 | Сбербанк | Loan | automatic termination | Refinance OR get waiver |
| 2 | ООО "Альфа" (key customer) | Поставка | consent required | Engage early — risk loss |
| 3 | Microsoft | ПО license | termination | Renegotiate post-closing |
```

### Шаг 4. Cross-reference с другими skills

- → `/diligence-issue-extraction` — для deeper analysis flagged contracts
- → `/closing-checklist` — adding consent / waiver / renegotiation tasks
- → `/deal-team-summary` — distill для non-legal stakeholders

## РФ-specific things to watch

### 1. Регистрация в ЕГРН (для аренды > 1 года)

ст.609 п.2 ГК — договор аренды недвижимости на срок > 1 года **обязательно
регистрируется в ЕГРН** (с 2013). Без регистрации — не действителен для третьих
лиц.

→ Flag если в schedule есть unregistered long lease.

### 2. Регистрация в Роспатент (для исключительных IP licenses)

ст.1232 ГК + 1235 ГК — исключительные лицензии на регистрируемые объекты
(товарные знаки, изобретения, полезные модели, промобразцы) **обязательно
регистрируются**. Без регистрации — не действительны для третьих лиц.

→ Flag если в schedule есть unregistered exclusive licenses.

### 3. Крупные сделки (ст.46 ФЗ-14 / ст.78 ФЗ-208)

Если контракт = крупная сделка (> 25% активов) — **должен был быть одобрен** ОСУ
/ ОСА / СД (по уставу). Если не одобрен — оспорим.

→ Flag если в schedule есть material contracts без подтверждения одобрения.

### 4. Сделки с заинтересованностью

ст.45 ФЗ-14 / ст.81-84 ФЗ-208 — если в сделке участвует interested party
(директор, контролирующий участник, и т.п.), требуется одобрение.

→ Flag если в schedule contracts с потенциально заинтересованными лицами.

### 5. Договоры с резидентами недружественных стран (post-2022)

Указ Президента 81/2022 + Постановления Правительства — некоторые расчёты,
переводы средств с недружественными резидентами требуют разрешения Правкомиссии.

→ Flag international contracts.

## Что НЕ делает

- Не renegotiates contracts (это commercial team)
- Не получает consents / waivers — это outside-адв + corporate development
- Не делает legal opinion на enforceability — это outside-адв

## Attribution

Adapted from [`corporate-legal/material-contract-schedule`](https://github.com/anthropics/claude-for-legal/blob/main/corporate-legal/skills/material-contract-schedule/SKILL.md)
by Anthropic (Apache 2.0).

**Категория A:**
- Categories preserved (customer, supplier, lease, loans, IP, JV, employment, insurance, litigation, tax)
- Field schema preserved, добавлены РФ-specific fields (ИНН, регистрация ЕГРН / Роспатент)
- Materiality thresholds в RUB (vs USD/EUR в Anthropic original)
- ст.609, ст.1232, ст.46, ст.45 — РФ-specific compliance flags
- Указ 81/2022 — РФ-specific filter

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
