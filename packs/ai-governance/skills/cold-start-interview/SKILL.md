---
name: cold-start-interview
description: >
  First-run для ai-governance pack. Заполняет PROFILE.md: AI maturity,
  использование LLM / ML / computer vision, regulatory context (152-ФЗ /
  115-ФЗ / sectoral), sanctions exposure (post-2022), internal AI policy.
argument-hint: "[optional: section]"
user_invocable: true
ported_from: ai-governance-legal/cold-start-interview
ported_at: 2026-05-19
adaptation_category: B
---

# /cold-start-interview (ai-governance)

## Workflow

### Шаг 1. Кто мы + AI maturity

- Тип организации
- AI maturity (exploring / piloting / production / scaled)
- Numerical estimates AI use cases

### Шаг 2. AI use focus

- Internal tools vs customer-facing vs core product
- Sectoral специфика (мед / фин / education / гос)

### Шаг 3. Текущие AI systems

- LLM services используемые (foreign vs Russian vs open-source)
- ML / classical / CV systems

### Шаг 4. Regulatory context

- 152-ФЗ ПДн applicability
- 115-ФЗ AML applicability
- Sectoral regulations (Банк России для финансовых; Минздрав для медицинских)
- Регуляторная sandbox (ФЗ-258)

### Шаг 5. Sanctions exposure (critical post-2022)

- Foreign AI services с restricted access
- Replacements (Russian alternatives)
- Risks operating через VPN / proxies

### Шаг 6. Internal AI policy state

- Policy утверждена?
- AI Officer / ethics board?
- Approval process для new use cases?

### Шаг 7. Sensitive data

- Training data sources
- ПДн в training
- Sensitive categories

### Шаг 8. Outside consultants + Risk posture + House style

### Шаг 9. Save + confirm

```
✓ PROFILE.md сохранён.

Загружены skills:
- /use-case-triage (PROCEED / IMPACT ASSESS / RESTRICT / PROHIBIT)
- /vendor-ai-review (AI vendor contracts review)
- /aia-generation (AI Impact Assessment — combines ОВПД 152-ФЗ + AI risks)
- /ai-inventory (всех AI systems в организации)
- /policy-starter (AI policy framework для РФ)
- /deployment-review (RU-unique — pre-production)
- /training-data-review (RU-unique — 152-ФЗ + авторские in training)
- /user-disclosure-check (RU-unique — мandatory disclosures users)
- /customize
```

## Attribution

Adapted from [`ai-governance-legal/cold-start-interview`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/cold-start-interview/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:** EU AI Act / US AI Bill of Rights / NIST framework → РФ landscape (152-ФЗ + 115-ФЗ + sectoral + национальная стратегия AI + ФЗ-258 sandboxes); post-2022 sanctions context.

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
