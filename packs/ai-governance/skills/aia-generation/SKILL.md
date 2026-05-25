---
name: aia-generation
description: >
  AI Impact Assessment (AIA) — formal documentation для AI use case рассматриваемого
  как medium/high risk. РФ specifics: AIA combines AI-specific risks с ОВПД framework
  (152-ФЗ ст.18.1) если processing ПДн. Структура: scope + risks + mitigation +
  approval. Subject to compliance officer / AI Officer / outside-адв ФПА review.
argument-hint: "[use case ID или description]"
user_invocable: true
ported_from: ai-governance-legal/aia-generation
ported_at: 2026-05-19
adaptation_category: B
---

# /aia-generation

## Назначение

Generate formal AI Impact Assessment document. Required after `/use-case-triage`
classified use case как IMPACT ASSESS level.

## Pre-flight

- `/use-case-triage` completed — IMPACT ASSESS classified
- Stakeholders identified (technical, business, legal, security, ethics)
- Готовы spend several days на полную AIA

## AIA structure

```markdown
# AI Impact Assessment
# Use case: [name]

**Version:** 1.0
**Date:** [DD.MM.YYYY]
**Authors:** [names + roles]
**Status:** [Draft / Under Review / Approved]
**Privilege framing:** [Privileged через outside-адв ФПА / Business-confidential]
```

### Section 1: Use case description

```markdown
## 1. Use case description

### 1.1. Purpose

[What this AI system is supposed to do, who benefits, what value]

### 1.2. Scope

[Specific functions, boundaries, what it doesn't do]

### 1.3. Stakeholders

| Role | Specific persons | Interest in this AI |
|------|------------------|---------------------|
| Customer | [...] | [...] |
| End user | [...] | [...] |
| Internal team | [...] | [...] |
| Regulator | [Минцифры / ЦБ / ФАС / etc.] | [oversight] |

### 1.4. Stages of usage

- Training / fine-tuning
- Deployment
- Production usage
- Periodic retraining / updates
- Decommissioning
```

### Section 2: Technical details

```markdown
## 2. Technical details

### 2.1. Underlying technology

- **Type:** [LLM / classical ML / CV / иное]
- **Vendor or self-hosted:** [...]
- **Model architecture:** [transformer / RNN / classical / иное]
- **Training data:** [source — internal / public / purchased / mixed]
- **Fine-tuning?** [Y/N + on what data]

### 2.2. Input / Output

- **Inputs accepted:** [data types, examples]
- **Outputs produced:** [data types, examples]
- **Decision authority:** [AI alone / AI + human / AI assists]

### 2.3. Performance characteristics

- **Expected accuracy:** [%]
- **Throughput:** [N requests / second]
- **Latency:** [seconds]
- **Failure modes:** [known limitations]

### 2.4. Update / maintenance

- Retraining frequency
- Monitoring metrics
- Performance degradation triggers
```

### Section 3: Legal compliance analysis

```markdown
## 3. Legal compliance

### 3.1. 152-ФЗ (если ПДн обрабатываются)

- **Processing roles:** [we as operator / vendor as processor]
- **Categories ПДн:** [...]
- **Legal basis:** [contract / consent / законные интересы / иное]
- **Special category** (ст.10) — health, биометрия, политика и пр.: [Y/N + safeguards]
- **Локализация (ст.18 ч.5):** processing в РФ confirmed
- **Cross-border transfer:** [Y/N + основание]
- **Уведомление РКН подано:** [Y/N + when]
- **ОВПД (ст.18.1) — оценка вреда:** done или not required?

### 3.2. Sectoral compliance

[Если применимо]

- **Финансовое (Банк России):** ФЗ-353 / 218 / 115 — compliance
- **Медицинское (Минздрав):** ФЗ-323 / лицензирование / Росздравнадзор регистрация AI as medical device
- **Образовательное (Минобрнауки):** ФЗ-273
- **Гос.услуги:** ПП 1503 / ФЗ-258 sandbox

### 3.3. Anti-discrimination

- **Risk:** AI может дискриминировать по защищённым категориям (раса, пол, возраст, инвалидность, и пр.)?
- **Mitigation:** [bias testing, fairness metrics, audit logs]
- **Legal basis для defense:** [ст.3 ТК если employment-related; ФЗ-181 если касается инвалидов]

### 3.4. Transparency requirements

- **Disclosure к user:** [что это AI, не человек] — see `/user-disclosure-check`
- **Explanation:** [right to explanation of automated decision — ст.16 152-ФЗ]
- **Documentation publicly available:** [policy / FAQ]

### 3.5. Intellectual property

- **Training data IP:** licensed properly? (см. `/training-data-review`)
- **Output IP:** ownership clear?
- **Copyright risks:** outputs similar к existing works?
```

### Section 4: Risk assessment

```markdown
## 4. Risk assessment

### 4.1. Identified risks

| # | Risk | Likelihood (1-5) | Impact (1-5) | Composite | Mitigation |
|---|------|-------------------|----------------|-----------|------------|
| 1 | Hallucination в production user-facing answer | 4 | 3 | 12 | Confidence scoring + disclaimers + human review для high-stakes |
| 2 | ПДн leakage в logs | 2 | 5 | 10 | Encryption + access controls + log redaction |
| 3 | Discrimination в outputs | 3 | 4 | 12 | Bias testing pre-deployment + ongoing monitoring + appeal process |
| 4 | Sanctions-related vendor unavailability | 3 | 4 | 12 | Backup Russian alternative + open-source fallback |
| 5 | Regulatory change requires rework | 3 | 3 | 9 | Periodic regulatory monitoring (см. `data-protection/reg-gap-analysis`) |
| 6 | ... | | | | |

### 4.2. Acceptable residual risk

[After mitigation — is the remaining risk acceptable?]

[Y/N + reasoning]
```

### Section 5: Mitigations + controls

```markdown
## 5. Mitigations + controls

### 5.1. Technical mitigations

- [ ] Input validation / sanitization
- [ ] Output filtering / content moderation
- [ ] Rate limiting per user
- [ ] Anomaly detection
- [ ] A/B testing pre-rollout
- [ ] Confidence scoring with thresholds
- [ ] Fallback to human для low-confidence cases

### 5.2. Procedural mitigations

- [ ] Human-in-the-loop для significant decisions
- [ ] Right to human review (ст.16 152-ФЗ если applicable)
- [ ] Appeal / dispute mechanism
- [ ] Periodic accuracy / fairness audits
- [ ] Incident reporting process
- [ ] User feedback channels

### 5.3. Documentation

- [ ] Internal documentation полная
- [ ] User-facing explanations
- [ ] Model cards (industry best practice)
- [ ] Datasheet for training data

### 5.4. Monitoring + alerts

- Performance metrics tracked
- Drift detection
- Adverse outcome notifications
- Quarterly review meetings
```

### Section 6: Stakeholder consultation

```markdown
## 6. Stakeholder consultation

| Stakeholder | Date consulted | Concerns raised | Resolution |
|-------------|----------------|-------------------|-------------|
| Legal | DD.MM.YYYY | ... | ... |
| Compliance | DD.MM.YYYY | ... | ... |
| InfoSec | DD.MM.YYYY | ... | ... |
| Affected business unit | DD.MM.YYYY | ... | ... |
| (External) outside-адв ФПА | DD.MM.YYYY | ... | ... |
| (External) AI ethics board | DD.MM.YYYY | ... | ... |
```

### Section 7: Recommendation

```markdown
## 7. Recommendation

[APPROVE FOR DEPLOYMENT / APPROVE WITH CONDITIONS / NEEDS REWORK / DO NOT APPROVE]

### Conditions (если applicable)

1. [Concrete condition]
2. ...

### Approvers required

- [ ] AI Officer
- [ ] Compliance Officer
- [ ] CISO (для security implications)
- [ ] Legal (in-house GC)
- [ ] (Material) Outside-адв ФПА review
- [ ] (Material) Board / Executive committee
```

### Section 8: Implementation plan

```markdown
## 8. Implementation plan

### Pre-deployment

| Action | Owner | Deadline |
|--------|-------|----------|
| [...] | [...] | [...] |

### Deployment

[Rollout plan — gradual / pilot / full]

### Post-deployment monitoring

[Schedule + metrics + escalation triggers]
```

### Section 9: Review schedule

```markdown
## 9. Review schedule

- **Initial review post-deployment:** [DD.MM.YYYY] (1-3 months)
- **Annual review:** [DD.MM.YYYY]
- **Trigger-based review:** [conditions — adverse outcome, regulatory change, material model update]
```

## Workflow

### Шаг 1. Set up document

Create AIA document for the specific use case. Pull data from PROFILE.md и `/use-case-triage` outputs.

### Шаг 2. Fill in sections

Sections 1-2 — technical input from product team / data scientists.

Sections 3-5 — legal / compliance analysis. Это major value-add от skill.

Section 6 — track consultations.

Sections 7-9 — recommendations + plan.

### Шаг 3. Review + iteration

- Internal review (legal + compliance)
- Stakeholder feedback
- (Material) outside-адв ФПА review
- Updates based on feedback

### Шаг 4. Approval

- Sign-off от required approvers
- Document approval chain
- Store в AIA registry

### Шаг 5. Post-AIA monitoring

- Track that mitigations actually implemented
- Periodic re-AIA при material changes
- Incident tracking + reporting

## Что НЕ делает

- Не делает technical AI testing (это data science / ML engineers)
- Не replaces outside-адв legal opinion для material matters
- Не выполняет actual implementation — это product / engineering

## Attribution

Adapted from [`ai-governance-legal/aia-generation`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/aia-generation/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:**
- EU AI Act FRAIA / NIST AI RMF template → adapted к РФ context
- 152-ФЗ ст.18.1 ОВПД integration — РФ-specific
- ст.16 152-ФЗ право на review automated decisions — РФ-specific
- Sectoral overlays РФ (Банк России / Минздрав / Росздравнадзор) вместо US/EU
- Sanctions risk dimension — РФ-specific
- Outside-адв ФПА involvement для privilege — РФ-specific

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
