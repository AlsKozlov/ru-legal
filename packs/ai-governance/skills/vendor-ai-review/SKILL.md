---
name: vendor-ai-review
description: >
  Review AI vendor contracts (LLM API providers, ML libraries, AI services).
  Включает SaaS-MSA общие issues (см. contract-law/saas-msa-review) + AI-specific:
  training data rights, output ownership, model warranty, hallucination liability,
  rate limits, API stability, безопасность (запрет training на our data),
  exit strategy + portability. Post-2022 sanctions specifics.
argument-hint: "[path к AI vendor contract]"
user_invocable: true
ported_from: ai-governance-legal/vendor-ai-review
ported_at: 2026-05-19
adaptation_category: B
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /vendor-ai-review

## Назначение

Review AI vendor / API / library contracts. Differs from generic SaaS-MSA review
(см. `contract-law/saas-msa-review`) — focus на AI-specific clauses.

## Pre-flight

- **Vendor identified:** [имя + type: hyperscaler LLM API / Russian LLM / open-source / SDK / library]
- **Sanctions exposure check:** US/EU vendor with restricted РФ access? (post-2022)
- **Use case clear:** [для каких задач будем использовать AI]
- **Data sensitivity:** [какие данные будем sending к vendor]

## AI-specific contract review points

### A. Data rights — наши данные у vendor

#### Training on our data

**Critical:** Vendor может использовать наш input / output для training future models?

- **Best:** "Vendor shall not use Customer Data for training models" — explicit
- **OK:** Opt-out available + opt-out exercised
- **Problematic:** Default training on customer data with no opt-out
- **Bad:** Training explicit + irrevocable license к vendor

**Examples in industry:**
- **OpenAI Enterprise:** Не trains on data (default for enterprise)
- **OpenAI consumer ChatGPT:** Trains by default (opt-out exists)
- **Anthropic Claude (API):** Не trains by default
- **Google Bard / Gemini Enterprise:** Не trains by default
- **YandexGPT API:** Check current terms (varies)
- **GigaChat:** Check current terms

→ Push for explicit "no training" в SaaS-MSA.

#### Data retention

- Как долго vendor stores наши queries / responses?
- Recommended: short retention (30 days max)
- Logs минимум для дoзinformation troubleshooting

#### Data location

- Где stored (geographic)?
- 152-ФЗ ст.18 ч.5 (локализация — для ПДн РФ residents) — нужно processing в РФ
- Cross-border — уведомление РКН

### B. Output rights — кому принадлежит result

#### Generated content ownership

**Best:** "Customer owns all rights в outputs" — explicit assignment

**Common ambiguity:** Outputs могут быть subject к terms ограничивающим use, even if "owned".

#### Restrictions на output use

- Можно ли использовать commercially?
- Можно ли redistribute?
- Можно ли train other models на outputs?
- Attribution required?

### C. Model warranty (или disclaimer)

#### Что vendor warrants?

**Common reality (almost все):**
- AS-IS basis
- No warranty of accuracy / completeness
- No warranty of fitness for particular purpose
- Disclaimer hallucinations / errors

**Что мы хотим:**
- Reasonable level of accuracy для intended use
- Notification если material model changes
- Removal of harmful outputs (если known)

→ Negotiate carve-outs из broad disclaimers для material reliance scenarios.

### D. Hallucination / error liability

**Default:** Vendor имеет broad disclaimer + cap on damages.

**Risk shift:**
- Customer absorbs full liability для use cases dependent on AI accuracy
- Customer must verify outputs before reliance
- High-stakes decisions (medical, legal, financial) — extra caution

### E. Rate limits + API stability

- **Rate limits:** Что happens если exceeded? Soft cap / hard cap?
- **API stability:** Versioning policy — backwards compatible breaking changes?
- **Deprecation notice:** Sufficient lead time для migration?
- **Uptime SLA:** Realistic + remedies для downtime?

### F. Pricing model

- **Token-based** (typical for LLM):
  - Input tokens / output tokens — separate rates
  - Predictability — high usage может escalate quickly
- **Per-API-call:** more predictable
- **Subscription:** flat fee — but cap usage
- **Mixed:** combo

→ Negotiate cap на monthly costs / requests.

### G. Security + confidentiality

- **Запрет on training:** see (A) above
- **Доступ vendor staff** к customer data — restricted?
- **Encryption:** transit + at-rest
- **Audit rights:** can we audit security practices?
- **Breach notification:** how fast?

### H. Compliance с 152-ФЗ (для ПДн)

Если будем sending ПДн в vendor:
- Vendor — accepts role как processor (DPA от data-protection pack)
- Локализация — vendor processes в РФ или есть legal basis для cross-border
- Уведомление РКН подано?
- Vendor agrees к РКН аудиту?

### I. Exit / portability

- **Termination rights:** какие events trigger? Срок уведомления?
- **Data export:** при выходе можем export все наши data?
- **Format:** machine-readable?
- **Fine-tuned models:** ownership / portability?
- **Transition support:** vendor cooperates в migration?

### J. Post-2022 sanctions specifics

#### Если vendor — US/EU

- **Access restrictions** — мы можем technically not access (geofencing)
- **Payment restrictions** — банк может block transactions
- **Sanction-driven termination** — vendor may unilaterally terminate
- **No guarantee** of continued availability

→ For material reliance — risky. Either backup vendor (Russian) или self-hosted (open-source).

#### Если vendor — Russian

- Generally OK от sanctions perspective
- Quality / capability — variable (YandexGPT / GigaChat reasonable for Russian content; might fall behind US frontier models for specialized tasks)
- Vendor lock-in risk reduced

#### Self-hosted open-source

- Llama / Mistral / Yi / Qwen — generally accessible
- Operational cost higher
- Quality control полностью our (good and bad)

### K. AI-specific compliance representations

**Vendor представляет:**
- Compliance с applicable laws (152-ФЗ если processing ПДн)
- Training data licensed properly (для generative AI — copyright concerns)
- Не trained on illegal / sensitive data в нарушение
- No backdoors / surveillance built-in (для post-2022 РФ vendors — particularly relevant)

## Workflow

### Шаг 1. Identify vendor + scope

```markdown
## Vendor

- **Name:** [...]
- **Type:** [LLM API / ML SaaS / library SDK / иное]
- **Country:** [...]
- **Sanctions exposure:** [Y/N]
- **Use case:** [для чего будем использовать]
- **Volume estimated:** [requests / data]
- **Data sensitivity:** [ПДн / sensitive / public]
```

### Шаг 2. Apply checklist (A-K above)

Для каждого section — review contract language + flag risks.

### Шаг 3. Risk summary

```markdown
## Risk findings

### 🔴 Critical

1. [Vendor trains on customer data by default — must change to opt-out]
2. [Sanctions exposure без backup — material risk]
3. ...

### 🟡 Medium

1. [Rate limits not transparent]
2. [Indemnity caps too low]

### 🟢 OK

[List]
```

### Шаг 4. Recommended changes

```markdown
## Recommended contract changes

### Required (won't sign without)

- [ ] "Vendor shall not use Customer Data for training" — added
- [ ] Customer owns all rights в outputs — added
- [ ] Backup arrangement или termination right if material API change

### Strongly desired

- [ ] Reduce data retention к 30 days
- [ ] Increase indemnity cap к [X]
- [ ] Audit rights expanded

### Nice to have

- [ ] Negotiate volume discount
- [ ] Add SLA для new model versions
```

### Шаг 5. Output

```markdown
# AI Vendor Review — [vendor + product]

## Bottom line

- **Sign / Don't sign / Sign with changes:** [...]
- **Critical issues:** [count]

## Issues detail

[From Step 3]

## Required changes

[From Step 4]

## Alternative vendors considered

- [Russian alternative 1]: pros / cons
- [Open-source alternative]: pros / cons

## Strategic recommendation

[Use this vendor / Use alternative / Hybrid (this for X, alternative for Y)]
```

## Что НЕ делает

- Не negotiates contract (это business + outside-адв)
- Не делает security audit vendor (это infosec team)
- Не replaces outside-адв legal opinion для high-stakes deals

## Attribution

Adapted from [`ai-governance-legal/vendor-ai-review`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/vendor-ai-review/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:**
- Universal AI vendor concerns preserved
- 152-ФЗ ПДн processor obligations — РФ-specific
- Post-2022 sanctions overlay — РФ-specific risk
- Russian vendor alternatives (YandexGPT / GigaChat) — РФ-specific

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
