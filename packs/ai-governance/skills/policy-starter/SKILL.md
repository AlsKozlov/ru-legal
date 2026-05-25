---
name: policy-starter
description: >
  Draft AI Policy для организации. РФ specifics: integrate с 152-ФЗ положение
  о ПДн; sectoral overlays; пилотные regulatory sandboxes (ФЗ-258); national
  AI strategy (Указ 490/2019) принципы; sanctions context. Template для
  Acceptable Use + Risk Management + Governance bodies.
argument-hint: "[draft new / review existing]"
user_invocable: true
ported_from: ai-governance-legal/policy-starter
ported_at: 2026-05-19
adaptation_category: B
---

# /policy-starter

## Назначение

Draft formal AI policy для организации. Это foundational document defining
governance, allowed/prohibited uses, processes для approvals.

## Pre-flight

- `/cold-start-interview` пройден
- `/ai-inventory` initial done (для realism)
- Stakeholders identified (legal, compliance, IT, business)
- Готовы spend time на iterative drafting

## AI Policy structure

```markdown
# AI Policy
# [Полное наименование организации]

**Версия:** 1.0
**Дата утверждения:** [DD.MM.YYYY]
**Утверждено:** [руководитель / Совет директоров — depending на materiality]
**Следующий review:** [DD.MM.YYYY] (рекомендуется annual)
**Применимость:** Все сотрудники, подрядчики, представители

## 1. Общие положения

### 1.1. Цели

[Полное наименование] (далее — Организация) внедряет искусственный интеллект (AI)
для повышения эффективности своей деятельности при обеспечении прав сотрудников,
клиентов и третьих лиц.

Настоящая политика определяет:

- Принципы, на которых Организация использует AI
- Разрешённые и запрещённые use cases
- Процесс одобрения новых AI use cases
- Роли и ответственность
- Compliance с применимым законодательством РФ

### 1.2. Правовая основа

- Конституция РФ
- Гражданский кодекс РФ (особ. часть 4 — IP aspects)
- ФЗ-152 «О персональных данных»
- ФЗ-115 «О противодействии легализации» (для финансовых applications AI)
- ФЗ-258 «Об экспериментальных правовых режимах в сфере цифровых инноваций» (sandbox)
- ФЗ-149 «Об информации» (включая обязательства information intermediaries)
- Указ Президента РФ 490/2019 «О национальной стратегии развития ИИ»
- Sectoral regulations (для регулируемых сфер)
- Внутренние ЛНПА Организации

### 1.3. Применимость

Распространяется на:
- Все AI systems используемые Организацией
- Все сотрудники, занятые в design / deployment / operation AI
- Все клиенты / пользователи affected AI решениями
- Подрядчиков, имеющих доступ к AI системам Организации
- Vendor relationships с AI providers

### 1.4. Определения

- **AI (искусственный интеллект)** — система, способная automatically generate outputs (прогнозы, классификации, рекомендации, контент, решения) на основе training data + algorithms

- **AI system** — software / hardware solution implementing AI

- **AI vendor** — third-party providing AI service / API / library

- **AI Officer** — должностное лицо, ответственное за AI governance в Организации
```

### Section 2: Principles

```markdown
## 2. Принципы

Использование AI в Организации opирается на следующие принципы (соответствуют
ст.2 Указа 490/2019):

### 2.1. Защита прав и свобод человека

AI не используется способом, нарушающим основные права (Конституция РФ + Хартия
прав человека). В particular:
- Право на ПДн (152-ФЗ)
- Право не подвергаться automated decisions со significant effect без human review
- Право на information о применении AI

### 2.2. Безопасность

AI systems обеспечивают безопасность данных, операций, инфраструктуры. Включает:
- Кибербезопасность
- Защита от adversarial attacks
- Continuity of operations

### 2.3. Прозрачность

Организация:
- Documents AI usage (см. `/ai-inventory`)
- Discloses AI usage к users (см. требования к disclosure ниже)
- Provides reasonable explanations decisions affecting users
- Maintains audit trails

### 2.4. Технологический суверенитет

Приоритет на:
- Российские AI решения, где applicable
- Open-source self-hosted решения (для control)
- Reducing зависимости от foreign vendors с potential sanctions exposure

### 2.5. Ответственность

- AI не replaces human responsibility для material decisions
- Clear accountability — кто отвечает за каждое AI use case
- Documentation решений для возможности audit и appeal

### 2.6. Защита уязвимых групп

Особое внимание защите:
- Несовершеннолетние
- Инвалиды (соблюдение ФЗ-181)
- Защищённые ст.3 ТК категории в employment AI
```

### Section 3: Allowed / Prohibited uses

```markdown
## 3. Разрешённые и запрещённые use cases

### 3.1. Разрешённые без специального approval (PROCEED level)

- Productivity tools (developer assistance, document drafts) с appropriate guardrails
- Internal classification / search
- Generic chatbots для FAQ
- Анализ без personal или sensitive data
- (Other low-risk use cases)

### 3.2. Требуют IMPACT ASSESS (formal AIA через `/aia-generation`)

- AI обрабатывающий ПДн special category (152-ФЗ ст.10)
- Customer-facing AI affecting > 1000 users
- AI в гос.услугах / regulated activities
- AI с potential discrimination risk
- (См. `/use-case-triage` для full list)

### 3.3. Restricted (с specific safeguards)

- Hiring AI — assistance only, not automated rejection
- Medical AI assistance — врач retains decision authority
- Credit scoring — с disclosure + appeal rights
- (С specific mitigation requirements)

### 3.4. Prohibited

- Social scoring systems
- Surveillance без legal basis
- Manipulative practices targeting vulnerable groups
- Automated decisions в criminal law context
- AI выдающее себя за human без disclosure (kennen impersonation)
- (Other prohibited use cases)
```

### Section 4: Governance

```markdown
## 4. Governance

### 4.1. Роли

#### AI Officer

- Назначение: [ФИО]
- Подотчётность: непосредственно руководителю
- Ответственность:
  - Maintenance AI policy
  - Approval IMPACT ASSESS / RESTRICTED use cases
  - Liaison с регуляторами по AI matters
  - AI incident reporting
  - Training сотрудников

#### Compliance Officer

- Liaison для 152-ФЗ / 115-ФЗ / sectoral compliance integration

#### CISO (Chief Information Security Officer)

- Cybersecurity aspects AI systems

#### Data Protection Officer (DPO)

- 152-ФЗ aspects AI processing ПДн

#### AI Ethics Committee (optional но recommended для крупных орг)

- Composition: AI Officer + Compliance + Legal + Business representatives + (опционально) external ethics advisor
- Frequency: monthly / quarterly
- Reviews high-risk use cases, sets policy direction

### 4.2. Процесс одобрения

См. `/use-case-triage` workflow:

1. Use case proposed
2. `/use-case-triage` classification
3. Если PROCEED → standard implementation
4. Если IMPACT ASSESS → `/aia-generation` + AI Officer approval
5. Если RESTRICT → enhanced safeguards + AI Officer + outside-адв
6. Если PROHIBIT → cannot proceed

### 4.3. Reporting

- AI incidents reported через [channel]
- Quarterly AI portfolio review meeting
- Annual AI policy review
```

### Section 5: Compliance с конкретными нормами

```markdown
## 5. Compliance

### 5.1. 152-ФЗ (для AI с ПДн)

- Legal basis установлен для каждого use case
- Уведомление РКН подано если применимо
- ОВПД (ст.18.1) для high-risk processing
- Локализация (ст.18 ч.5) обеспечена
- Right to information + human review (ст.16) implemented

### 5.2. ИС / IP

- Training data: licensed properly (см. `/training-data-review`)
- Outputs: ownership determined per vendor contract
- Avoidance of infringement в outputs

### 5.3. Sectoral

- Финансовые AI — Банк России регуляторика
- Медицинские — Росздравнадзор регистрация (для AI as medical device)
- Образовательные — Минобрнауки требования
- (Other sectoral)

### 5.4. Anti-discrimination

- Защищённые категории по ст.3 ТК / Конституции РФ / ФЗ-181
- Bias testing pre-deployment
- Ongoing monitoring для drift

### 5.5. Vendor management

- Все AI vendor contracts reviewed (см. `/vendor-ai-review`)
- Sanctions exposure managed
- Backup vendors / fallback documented
```

### Section 6: AI usage guidelines (Acceptable Use Policy)

```markdown
## 6. Guidelines для сотрудников

### 6.1. Use approved AI tools

- ChatGPT / Claude / иной personal accounts НЕ используются для work data
- Используйте только AI tools, approved AI Officer

### 6.2. Confidentiality

- НЕ feed Confidential / Sensitive / ПДн в external AI tools
- Approved tools могут have specific data handling guarantees — check policy per tool

### 6.3. Verification

- AI outputs могут быть incorrect / hallucinated
- Verify factual outputs before relying на них
- Особо critical для legal / financial / medical content

### 6.4. Disclosure

- При использовании AI в work products affecting third parties — disclose в applicable contexts
- НЕ presenting AI outputs as human work без appropriate attribution

### 6.5. Reporting issues

- AI incidents (errors с impact, bias detected, security concerns) — report к AI Officer immediately
```

### Section 7: Update + review

```markdown
## 7. Update + review

- Annual policy review (с участием всех stakeholder groups)
- Trigger-based updates:
  - New применимое законодательство
  - Material AI incident
  - New significant use case
  - Vendor changes

- Communication of updates к employees
- Re-training when material changes
```

### Section 8: Enforcement + violations

```markdown
## 8. Enforcement + violations

Нарушения настоящей политики могут влечь:

- Дисциплинарные взыскания (по ТК — см. labor-law/termination-review для framework)
- Reporting к регуляторам если нарушение closer к legal violation
- Уголовная ответственность для extreme cases

Подпись с ознакомлением — required from all employees.
```

## Workflow

### Шаг 1. Determine scope + maturity level

- Small organization — concise policy (5-10 pages)
- Medium — comprehensive (20-30 pages)
- Large enterprise — multi-layered (policy + standards + procedures)

### Шаг 2. Draft sections

Use template above as basis. Modify per organization's:
- Sectoral specifics
- AI maturity
- Size
- Risk tolerance

### Шаг 3. Stakeholder review

- Legal review
- Compliance review
- IT / security review
- Business unit feedback
- (Material) Outside-адв ФПА review
- Board / executive review

### Шаг 4. Утверждение + распространение

- Formal approval per organization's governance
- Communication к employees
- Training сотрудников (recommended)
- Acknowledgment под подпись

### Шаг 5. Operationalization

- Set up procesы:
  - `/use-case-triage` workflow operational
  - AIA template + approval flow
  - AI inventory maintenance
  - Vendor review process
  - Incident reporting channel
- Set up tools:
  - GRC system или shared registry
  - Communication channels

## Что НЕ делает

- Не replaces full legal review для material organizations
- Не handles operationalization (HR / IT / Compliance teams)
- Не tracks specific AI implementations (это `/ai-inventory`)

## Attribution

Adapted from [`ai-governance-legal/policy-starter`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/policy-starter/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:**
- Universal AI policy structure preserved
- Принципы — Указ 490/2019 национальная стратегия AI integrated
- 152-ФЗ + sectoral overlays РФ vs US/EU references
- ФЗ-258 sandbox mentioned
- Sanctions / sovereignty principles — РФ-specific
- ПП РФ 1186 (Strategy development AI) included as basis

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
