---
name: deployment-review
description: >
  RU-unique. Pre-deployment review AI system перед production. Final gates:
  AIA approved, technical safeguards implemented, monitoring set up, incident
  response ready, training данных compliant, vendor contracts signed.
  Differs от AIA — это checklist на действительной готовности.
argument-hint: "[AI system ID или name]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /deployment-review

## Назначение

Pre-production go/no-go review для AI system. Final checkpoint перед deployment.

## Pre-flight

- AI system development complete
- `/aia-generation` completed (если IMPACT ASSESS level)
- Technical testing done
- Stakeholders готовы для deployment

## Workflow

### Шаг 1. Verify AIA + approvals

```markdown
## AIA + approvals verification

- [ ] `/use-case-triage` completed: [PROCEED / IMPACT ASSESS / RESTRICT]
- [ ] AIA document exists + signed: [link, date]
- [ ] AI Officer approval: [signed]
- [ ] Compliance Officer approval (для ПДн / 115-ФЗ): [signed]
- [ ] CISO approval (для security): [signed]
- [ ] (Material) Outside-адв ФПА review: [signed]
- [ ] (Material) Board approval: [signed if required]

[Stop if any gap]
```

### Шаг 2. Verify technical safeguards

```markdown
## Technical safeguards

### Pre-deployment

- [ ] Input validation implemented
- [ ] Output filtering / content moderation set up
- [ ] Rate limiting configured
- [ ] Authentication / authorization verified
- [ ] Logging implemented (without ПДн leakage)
- [ ] Encryption at rest + in transit verified
- [ ] Access controls reviewed
- [ ] Backup / disaster recovery plan
- [ ] (For LLM) Confidence scoring + thresholds
- [ ] (For LLM) Fallback к human для low-confidence

### Bias / fairness (если applicable)

- [ ] Bias testing done на representative datasets
- [ ] Fairness metrics meet thresholds
- [ ] Subgroup performance acceptable
- [ ] Adversarial testing done (если applicable)

### Adversarial robustness (если applicable)

- [ ] Prompt injection testing (для LLM)
- [ ] Model evasion testing (для security AI)
- [ ] Data poisoning safeguards
```

### Шаг 3. Verify data compliance

```markdown
## Data compliance

### 152-ФЗ (если processing ПДн)

- [ ] Legal basis documented в РКН уведомлении
- [ ] Specific consents collected где требуется
- [ ] Локализация confirmed (storage в РФ)
- [ ] Cross-border transfers — уведомления поданы
- [ ] Data retention period defined
- [ ] ПДн deletion mechanism implemented
- [ ] User rights (доступ, удаление) implemented
- [ ] ОВПД (ст.18.1) на disk
- [ ] DPO consulted

### Training data

- [ ] Sources licensed properly (см. `/training-data-review`)
- [ ] No copyright violations
- [ ] No ПДн leakage в training data (без legal basis)
- [ ] Sensitive content filtered

### Production data

- [ ] Data sources documented
- [ ] Data quality verified
- [ ] Anomaly detection set up
```

### Шаг 4. Verify monitoring

```markdown
## Monitoring

### Performance

- [ ] Accuracy / quality metrics dashboard
- [ ] Latency / throughput metrics
- [ ] Error rate monitoring
- [ ] Alerting thresholds set

### Bias / fairness ongoing

- [ ] Subgroup performance tracked
- [ ] Drift detection (для accuracy)
- [ ] Drift detection (для fairness)
- [ ] Periodic re-audit scheduled

### Security

- [ ] Anomalous query patterns detected
- [ ] Failed auth attempts monitored
- [ ] Adversarial input detection

### Logs

- [ ] Audit logs implemented
- [ ] User actions tracked (для appeal / dispute)
- [ ] Logs immutable / tamper-evident
- [ ] Logs retention policy meets compliance
```

### Шаг 5. Verify incident response

```markdown
## Incident response

- [ ] Incident response plan documented
- [ ] On-call rotation established
- [ ] Escalation chain clear (technical → AI Officer → executives)
- [ ] User-facing incident communication procedure
- [ ] Regulator notification procedure (если applicable)
- [ ] Post-incident review process
- [ ] Severity classification (P0 / P1 / P2 / P3)
- [ ] Common incidents practiced (table-top exercise recommended)
```

### Шаг 6. Verify user disclosures

См. `/user-disclosure-check` для full framework.

```markdown
## User disclosures

- [ ] AI usage disclosed to users где applicable
- [ ] Right to human review explained (для automated decisions)
- [ ] Privacy policy updated к include AI processing
- [ ] Terms of service updated
- [ ] FAQs / help docs prepared
- [ ] Customer support trained на handling AI-related queries
```

### Шаг 7. Verify vendor relationships (если vendor-based)

```markdown
## Vendor relationships

- [ ] Contract signed (см. `/vendor-ai-review`)
- [ ] DPA в place (если ПДн processing)
- [ ] No training on our data confirmed
- [ ] Data location confirmed
- [ ] SLA defined
- [ ] Exit / portability plan
- [ ] Backup vendor identified (для sanctions / continuity risk)
```

### Шаг 8. Verify training / awareness

```markdown
## Training

### Internal users (employees using AI tool)

- [ ] Initial training conducted
- [ ] Acceptable use policy acknowledged
- [ ] Reporting issues understood

### Operators (team running AI system)

- [ ] Technical training on operating model
- [ ] Incident response training
- [ ] Bias monitoring training

### Customer-facing teams

- [ ] How to explain AI usage to customers
- [ ] Appeal / dispute process training
- [ ] Escalation procedures
```

### Шаг 9. Verify rollout plan

```markdown
## Rollout plan

### Approach

- [ ] Gradual / pilot / full rollout? [...]
- [ ] Specific phases planned
- [ ] Rollback procedure defined
- [ ] Success criteria per phase

### Initial monitoring

- [ ] Enhanced monitoring для первых 30 days
- [ ] Daily / weekly review meetings scheduled
- [ ] Threshold для pausing rollout если issues

### Communication

- [ ] Stakeholders informed
- [ ] Users (если customer-facing) — communication plan
- [ ] Internal teams ready
```

### Шаг 10. Final go/no-go

```markdown
## Decision

[GO / NO-GO / CONDITIONAL GO]

### If CONDITIONAL GO

Specific conditions to meet before final go:

- [ ] [condition 1]
- [ ] [condition 2]

Re-review scheduled: [DD.MM.YYYY]

### If NO-GO

Reasons:
- [...]

Remediation plan:
- [...]

Re-review: [DD.MM.YYYY]
```

## Post-deployment immediate actions

```markdown
## T+0 to T+30

### Daily

- [ ] Monitoring dashboard reviewed
- [ ] Incident log reviewed
- [ ] User feedback channels checked

### Weekly

- [ ] Team review meeting (technical + business + compliance)
- [ ] Performance trends analyzed
- [ ] Any incidents discussed + RCA

### After 30 days

- [ ] Post-deployment AIA review (does AIA still accurate?)
- [ ] Performance vs predicted
- [ ] User satisfaction (если customer-facing)
- [ ] Updated risk assessment
```

## Что НЕ делает

- Не replaces formal AIA — это `/aia-generation`
- Не handles technical testing — это QA / data science teams
- Не replaces outside-адв legal opinion для material matters

## Why RU-unique

US/EU AI deployment frameworks (NIST AI RMF / EU AI Act conformity assessment) — different
checkpoints + actors. РФ — combination 152-ФЗ + sectoral + АI Officer + DPO в local
context.

**Правовая основа:**
- 152-ФЗ + ОВПД ст.18.1
- 115-ФЗ если AI в AML
- Sectoral regulations
- Указ 490/2019 — национальная стратегия AI
- Внутренняя AI policy организации (см. `/policy-starter`)

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
