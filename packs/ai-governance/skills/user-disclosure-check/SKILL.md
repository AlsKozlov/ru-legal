---
name: user-disclosure-check
description: >
  RU-unique. Verify обязательные disclosure к users об AI usage. РФ specifics:
  ст.16 152-ФЗ — право знать про automated decisions; ст.10 ФЗ-149 — обязанности
  information services; ФЗ-2300-1 «О защите прав потребителей» для consumer
  context; sectoral disclosures (банковский / медицинский / education).
argument-hint: "[AI feature + user context]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /user-disclosure-check

## Назначение

Verify что users получают required disclosure об AI usage. Различные contexts
require разные disclosures.

## Disclosure requirements

### A. General principles (ст.16 152-ФЗ)

Если AI принимает automated decisions со значимыми последствиями для субъекта
ПДн:

- **Информирование** субъекта о принятии решения автоматически
- **Объяснение** логики решения (на упрощённом языке)
- **Право возразить** против automated decision-only processing
- **Право на review** человеком

→ Required в applicable contexts. Disclosure в момент interaction.

### B. Information intermediaries (ФЗ-149 ст.10)

Если organization — information intermediary (платформа / social media / messenger):

- Обязанности по identifying user content vs system-generated content
- (Recent regulations — для специфических types AI-generated content) labeling
- Для recommender systems — transparency о принципах работы

### C. Consumer protection (ФЗ-2300-1)

Если AI used в consumer context (B2C):

- Information о товаре / услуге должна быть **truthful + complete**
- AI-generated content presented как такое (если applicable)
- Recommendations + ranking — algorithm logic disclosure (best practice)

### D. Banking AI (ЦБ РФ regulations)

Если AI в credit / lending решениях:

- Credit decision — disclosure (ФЗ-218 ст.5)
- Reason for denial — provided
- Right to appeal к bank's complaints procedure
- (Для significant individuals — ЦБ РФ может require additional)

### E. Medical AI (Минздрав)

Если AI в medical context:

- Disclosure что AI used в diagnosis / treatment
- Final decision — human врач
- Patient consent для AI-assisted care

### F. Educational AI

Если AI в admissions / grading / testing:

- Disclosure for students / parents
- Right to traditional evaluation alternative
- Appeals process

### G. Employment AI

Если AI в hiring / promotion / monitoring:

- Disclosure to candidates / employees
- ТК соответствующие consent / notification requirements
- Anti-discrimination considerations (ст.3 ТК)

## Disclosure formats

### Privacy policy

Section dedicated к AI use:

```markdown
## Использование искусственного интеллекта (AI)

Мы используем технологии искусственного интеллекта для следующих целей:

- [Конкретные цели: e.g. персонализированные рекомендации; chat support]

### Какие данные обрабатываются с помощью AI

[...]

### Принимаются ли автоматические решения

[Y/N + если Y — what about, какие consequences]

### Ваши права в связи с AI

- Знать когда используется AI в обработке ваших данных
- Получить explanation логики автоматического решения
- Возразить против decisions, принимаемых только AI
- Запросить human review

Чтобы воспользоваться правами, обратитесь: [contact]
```

### In-product disclosure

```markdown
### Examples disclosure formats

#### Chatbot opening

"Здравствуйте! Я AI-ассистент [имя]. Если нужна помощь человека, скажите 'оператор'."

#### Recommendation system

"Эти товары подобраны для вас алгоритмом на основе вашей истории покупок."

#### Automated decision (e.g., loan rejection)

"К сожалению, мы не можем одобрить ваш запрос. Это автоматическое решение, основанное на следующих факторах: [list]. Вы вправе запросить пересмотр решения сотрудником банка по адресу: [contact]."

#### AI-generated content

"Этот текст / изображение было создано с помощью AI."
```

### Settings / preferences

For high-impact AI, provide user controls:

- Toggle для personalization / AI recommendations
- Opt-out (если business model allows)
- Data retention preferences

## Workflow

### Шаг 1. Identify disclosure contexts

```markdown
## Disclosure context matrix

| AI feature | User-facing? | ПДн used? | Automated decision? | Sectoral overlay | Required disclosures |
|------------|---------------|------------|---------------------|--------------------|----------------------|
| Internal dev copilot | No (only employees) | Internal data | No | None | Internal AUP only |
| Customer chatbot | Yes | Yes (имя + content) | Sometimes (escalation routing) | Consumer protection | Bot identification + escalation option |
| Product recommendations | Yes | Yes (history) | Yes (which products shown) | Consumer protection | Algorithm disclosure |
| Credit scoring AI | Yes | Yes (financial) | Yes (loan decision) | Banking (ФЗ-218) + ст.16 152-ФЗ | Decision disclosure + appeal rights |
| Resume screening AI | Yes (candidates) | Yes (CV) | Yes (initial filter) | Employment (ТК ст.3 anti-discrimination) | Candidate notification + human review |
```

### Шаг 2. For each context — verify disclosures

```markdown
## Per-context disclosure check

### Context: Customer chatbot

- [ ] Bot identification — within first 2 messages
- [ ] How to reach human operator — clear instruction
- [ ] Data handling notice — link to privacy policy
- [ ] In privacy policy — section about chatbot AI

### Context: Credit scoring

- [ ] Decision notification (approval / denial)
- [ ] Reason for denial (если denied)
- [ ] Appeal process — formal procedure
- [ ] Privacy policy update
- [ ] Human review available

### Context: Resume screening

- [ ] Job posting mentions AI screening
- [ ] Candidate notified about AI usage
- [ ] Human review for shortlisted
- [ ] Opt-out (где applicable)
- [ ] Anti-discrimination assurances
```

### Шаг 3. Gaps + remediation

```markdown
## Gaps identified

| Context | Gap | Severity | Remediation |
|---------|------|----------|-------------|
| Chatbot | Bot identification only in 5th message | 🟡 | Move к первого message |
| Credit scoring | No formal appeals process | 🔴 | Implement + document |
| Resume screening | Not mentioned in job posting | 🟡 | Update job posting template |
```

### Шаг 4. Implementation

```markdown
## Implementation plan

### Privacy policy updates

- [ ] Add AI section к privacy policy
- [ ] Specific subsections per use case
- [ ] Publish updated policy
- [ ] User notification of policy change

### In-product changes

- [ ] Add bot identification к chatbot
- [ ] Add recommendation algorithm disclosure
- [ ] Add decision notification mechanism для credit AI
- [ ] Update resume screening disclosure

### Operational changes

- [ ] Appeals process documentation
- [ ] Customer support training на handling AI questions
- [ ] Complaints procedure updated
```

### Шаг 5. Periodic audits

```markdown
## Disclosure audit

- Quarterly review (или после material AI changes)
- Sample check that disclosures appearing actually
- User feedback (complaints about lack of transparency = red flag)
- Update on regulatory changes
```

## Common pitfalls

### 🔴 Critical

- **Automated decisions без disclosure** — нарушение ст.16 152-ФЗ; complaints к РКН; potential суд
- **AI assistance не disclosed** в high-stakes contexts (medical, financial) — regulatory risk
- **Misleading impersonation** AI as human — consumer protection violation

### 🟡 Medium

- Disclosure exists но spread (нужно "click here" → 3 clicks deep)
- Generic privacy policy без AI-specific section
- Inconsistent disclosures across products / channels

### 🟢 Acceptable

- Clear, prominent, accessible disclosures
- Specific languages для specific contexts
- User-friendly controls

## Что НЕ делает

- Не drafts полную privacy policy (это `data-protection/policy-monitor` + lawyer)
- Не handles complaints (это customer support + compliance)
- Не updates product UI (это product team)

## Why RU-unique

EU GDPR has aналогичные disclosure requirements (Art. 22 для automated decisions), но РФ имеет:
- 152-ФЗ ст.16 — отдельная норма про automated decisions
- ФЗ-149 — для information intermediaries
- ФЗ-2300-1 — consumer protection specifics
- Sectoral (Банк России / Минздрав / ТК / Минобрнауки) requirements

**Правовая основа:**
- 152-ФЗ ст.14, ст.16, ст.18.1
- ФЗ-149 ст.10, ст.10.1, ст.10.7 (для рекомендательных systems)
- ФЗ-2300-1 «О защите прав потребителей»
- ФЗ-218 ст.5 (банковский context)
- ФЗ-323 ст.36.2 (телемедицина)
- ТК ст.3, ст.86 (employment context)

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
