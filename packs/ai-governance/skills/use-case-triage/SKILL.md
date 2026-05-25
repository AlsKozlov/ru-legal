---
name: use-case-triage
description: >
  Triage AI use case по уровню риска — PROCEED / IMPACT ASSESS / RESTRICT /
  PROHIBIT. РФ specifics: combination 152-ФЗ ПДн + sectoral overlay (Банк
  России для финансовых; Минздрав для мед; Минобрнауки для education; и т.д.)
  + национальная стратегия AI (Указ Президента 490/2019).
argument-hint: "[описание AI use case]"
user_invocable: true
ported_from: ai-governance-legal/use-case-triage
ported_at: 2026-05-19
adaptation_category: B
---

# /use-case-triage

## Назначение

Initial triage AI use case при request к compliance / legal team. Quick decision:
proceed normally / need formal AIA / restrict scope / prohibit.

## Pre-flight

- **Описание use case** конкретное (что делает, на каких данных, в какой контекст)
- **Stakeholders** (team requesting, end users affected)
- **Timeline desired** для deployment

## Triage levels

### Level 1: PROHIBIT

**Use case полностью запрещён.** Reason: severe legal / ethical risk.

Examples:
- Social scoring system по типу China
- Real-time biometric identification в public spaces без правовых оснований
- AI для manipulative practices targeting vulnerable groups
- AI ranking / decisions нарушающие конкретные правовые нормы:
  - Кредитный scoring without disclosure (ст.5 ФЗ-218)
  - Trial-like decisions в АС (нарушение принципа judicial independence)
  - Health diagnosis без medical license + врачебной верификации

### Level 2: RESTRICT / SIGNIFICANT MITIGATION

**Use case applicable только в restricted form** с substantial safeguards.

Examples:
- Hiring decisions с AI assistance (но не automated rejection)
- Medical advice (но не replacing врача)
- Credit scoring (только с disclosure + appeal rights)
- Educational assessment (с right human review)
- Predictive policing (extreme caution + judicial oversight)

### Level 3: IMPACT ASSESS

**Required formal AI Impact Assessment** before deployment.

Examples:
- New AI feature affecting > 1000 users
- AI processing ПДн special category (152-ФЗ ст.10)
- AI в gos.услугах / regulated activities
- AI с potential discrimination risk

→ Use `/aia-generation` для формальной AIA.

### Level 4: PROCEED

**Use case low risk + standard review.** Document decision но не need formal AIA.

Examples:
- Internal productivity tools (developer copilot, document drafts)
- Generic chatbots для FAQ
- Internal classification / search
- ML для optimization (не affecting outcomes для people)

## РФ-specific risk indicators

### A. 152-ФЗ ПДн applicability

| Pattern | Risk | Action |
|---------|------|--------|
| AI обрабатывает ПДн (имена, email, etc.) | Medium | Legal basis обоснование + transparency |
| AI обрабатывает Special category (ст.10) — health, политика, биометрия | High | Explicit consent + safeguards + AIA + 18.1 ОВПД |
| AI принимает automated decisions со significant effect (ст.16 152-ФЗ) | High | Right to human review + transparent logic |
| Cross-border ПДн transfers | High | 152-ФЗ ст.12 compliance + уведомление РКН |

### B. Sectoral overlays

#### Финансовые (Банк России)

- AI в кредитных решениях → ФЗ-353 «О потребительском кредите» + 218 «О кредитных историях» + Положения Банка России
- AML AI (115-ФЗ ст.6, ст.7) — AI assistance OK, automated decisions с caveat
- ИЛ-системы (искусственный интеллект для investments) — пилотный режим под Банком России

#### Медицинские

- AI как медицинское изделие → требует регистрации Росздравнадзора по ФЗ-323 + ПП 1416
- AI assistance к врачу OK; AI as primary doctor — НЕТ (no license)
- Telemedicine с AI — separate regulation (ст.36.2 ФЗ-323)

#### Образование

- AI в выставлении оценок — ограничения
- AI в приёме / отчислении — discrimination risk
- AI для адаптивного обучения OK

#### Гос.услуги

- AI для государственных решений → ПП 1503 / ФЗ-258 регуляторный sandbox
- Right to human review мandatory

#### Public-facing AI (chatbots)

- Disclosure обязателен (что это AI, не человек) — best practice
- Не misleading impersonation

### C. Sanctions / Foreign AI services

Post-2022 особые considerations:

- US AI services (OpenAI, Anthropic, Google) — restricted access — risk используем через VPN / proxies
- Sanctions enforcement по нашу сторону РФ — generally not actively pursued, но business risk
- Reputation / compliance risk для multinational presence

→ Recommend Russian alternatives или open-source self-hosted где possible.

### D. IP risks (training data)

- Training на скрапленных публичных данных без лицензии — потенциальный copyright risk
- Sources третьих сторон — licensing review
- Output similar к copyrighted works — risk

→ Cross-reference `ip-law/ip-clause-review` + `/training-data-review`.

## Workflow

### Шаг 1. Intake use case

```markdown
## Use case intake

- **Name:** [...]
- **Description:** [что делает AI]
- **Inputs:** [какие данные принимает]
- **Outputs:** [что produces]
- **Decision authority:** [AI решает / AI suggests + human approves / AI assists human]
- **Affected users:** [internal employees / customers / public / regulated subjects]
- **Estimated scale:** [N users, frequency]
- **Underlying technology:** [LLM / classical ML / CV / RL / generative / иное]
- **Vendor:** [foreign — какой / Russian / self-hosted / mixed]
- **Sensitive data involved:** [Y/N + categories]
- **Sectoral applicability:** [финансовое / мед / education / гос / иное]
- **Timeline desired:** [...]
```

### Шаг 2. Apply risk indicators

```markdown
## Risk assessment

| Risk dimension | Score | Reasoning |
|----------------|-------|-----------|
| Data sensitivity (152-ФЗ) | 1-5 | ... |
| Decision impact на person | 1-5 | ... |
| Vulnerable populations affected | 1-5 | ... |
| Discrimination risk | 1-5 | ... |
| Sectoral regulation applicable | 1-5 | ... |
| Transparency feasibility | 1-5 | ... |
| Human oversight feasibility | 1-5 | ... |
| Sanctions exposure | 1-5 | ... |
| IP risk (training data) | 1-5 | ... |

**Composite score:** [sum / max possible]
```

### Шаг 3. Decision

```markdown
## Triage decision

[PROCEED / IMPACT ASSESS / RESTRICT / PROHIBIT]

### Reasoning

[Why this level]

### If PROCEED

- Document decision
- Standard implementation
- Periodic review (annual)

### If IMPACT ASSESS

- Use `/aia-generation` для formal AIA
- Engage AI Officer / compliance officer
- Stakeholders consulted
- Final decision after AIA

### If RESTRICT

- Specific safeguards required:
  - [Human-in-the-loop для critical decisions]
  - [Transparency disclosure to affected users]
  - [Right to human review]
  - [Bias monitoring + correction]
  - [Audit logging]
- Limit scope (e.g., assistance not automation)
- Engage outside-адв ФПА для formal opinion если sectoral risk material

### If PROHIBIT

- Cannot proceed in current form
- Document specific reasons (legal / ethical)
- Suggest alternatives (e.g., manual process + AI assistance instead of full automation)
- Communicate to requesting team with constructive alternatives
```

### Шаг 4. Documentation + monitoring

```markdown
## Decision log

- **Date:** [DD.MM.YYYY]
- **Use case ID:** [...]
- **Triage level:** [...]
- **Reviewer:** [...]
- **AIA scheduled?** [Y/N — if yes — link к AIA report]
- **Implementation deadline:** [...]
- **Next review:** [DD.MM.YYYY]

## Future monitoring

- Performance metrics (accuracy, fairness, etc.)
- Incident reporting (если есть adverse outcomes)
- Drift monitoring (если applicable)
- Regulatory changes affecting this use case
```

## Что НЕ делает

- Не выполняет формальный AIA — это `/aia-generation`
- Не handles deployment — это `/deployment-review`
- Не replaces outside-адв legal opinion для material matters

## Attribution

Adapted from [`ai-governance-legal/use-case-triage`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/use-case-triage/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:**
- EU AI Act risk categorization → adapted к РФ regulatory mosaic (152-ФЗ + sectoral)
- Banking AI — Банк России framework вместо CFPB / EU MiCA
- Health AI — Росздравнадзор + ФЗ-323 вместо FDA / EU MDR
- Sanctions overlays — post-2022 РФ-specific
- Регуляторная sandbox — ФЗ-258 / ПП 1503

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
