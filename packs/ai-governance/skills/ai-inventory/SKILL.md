---
name: ai-inventory
description: >
  Inventory всех AI systems в организации — где, какие, для чего, на каких
  данных, какой compliance status. Critical для regulatory compliance + risk
  management.
argument-hint: "[optional: pre-existing inventory file]"
user_invocable: true
ported_from: ai-governance-legal/ai-inventory
ported_at: 2026-05-19
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /ai-inventory

## Назначение

Comprehensive inventory всех AI systems используемых в организации. Goals:
- Visibility — что вообще AI used
- Compliance — каждое use case с appropriate review
- Risk management — identify high-risk использования
- Vendor management — leverage в negotiations + replacement planning

## Workflow

### Шаг 1. Discovery

Sources где может быть AI:

- **Productivity tools:** GitHub Copilot, ChatGPT business accounts, Notion AI, etc.
- **Communication:** AI translation tools, smart replies, etc.
- **Customer support:** chatbots, ticket classification, sentiment analysis
- **Marketing:** content generation, ad optimization, audience targeting
- **Sales:** lead scoring, CRM AI, sales call analysis
- **HR:** resume screening, employee analytics, performance prediction
- **Operations:** demand forecasting, route optimization, inventory
- **Finance:** fraud detection, credit scoring, transaction monitoring
- **Product:** recommendation engines, search, personalization
- **Engineering:** code review AI, anomaly detection, log analysis
- **Security:** threat detection, anomaly detection in network
- **Compliance:** AML transaction monitoring (115-ФЗ), DSAR routing

### Шаг 2. For each system, capture metadata

```markdown
## AI System: [name / ID]

### Identification

- **Internal name:** [...]
- **Vendor / source:** [vendor name OR "internal/self-hosted"]
- **Type:** [LLM / classical ML / CV / RL / other]
- **Underlying model:** [GPT-4 / Llama 3 / custom / proprietary / etc.]
- **Owner business unit:** [...]
- **Technical owner:** [team / person]
- **Date deployed:** [DD.MM.YYYY]
- **Status:** [pilot / production / sunsetting / decommissioned]

### Use case

- **Purpose:** [what it does]
- **Decision authority:** [AI alone / AI suggests + human / AI assists]
- **Users:** [internal / customer-facing / public-facing]
- **Estimated usage volume:** [requests / queries per period]

### Data

- **Inputs:** [data types — ПДн? Sensitive?]
- **Outputs:** [data types]
- **Training data sources:** [vendor data / our data / public / mixed]
- **Data sensitivity classification:** [public / internal / confidential / regulated]

### Compliance status

- **152-ФЗ applicability:** [Y/N + if Y — legal basis]
- **РКН уведомление:** [done / not applicable]
- **ОВПД (ст.18.1):** [done / not required]
- **AIA done:** [link]
- **Triage decision (см. `/use-case-triage`):** [PROCEED / IMPACT ASSESS / RESTRICT]
- **Sectoral compliance:** [Банк России / Минздрав / иное — status]

### Risk

- **Composite risk score (от AIA):** [N]
- **Material risk events recorded:** [count]
- **Last review:** [DD.MM.YYYY]
- **Next scheduled review:** [DD.MM.YYYY]

### Sanctions exposure

- **Vendor jurisdiction:** [country]
- **Sanctions-related access issues:** [Y/N]
- **Backup plan if cut off:** [...]

### Cost

- **Monthly / annual spend:** [сумма]
- **Pricing model:** [token / per-call / subscription / mixed]

### Notes

- [Any特ic considerations]
```

### Шаг 3. Tabular summary

```markdown
## AI Inventory Summary — [date]

### By type

| Type | Count | Production | Pilot |
|------|-------|------------|-------|
| LLM API | [N] | [N] | [N] |
| Classical ML | [N] | [N] | [N] |
| CV | [N] | [N] | [N] |
| Other | [N] | [N] | [N] |
| **Total** | [N] | [N] | [N] |

### By risk level

| Risk | Count | Action needed |
|------|-------|---------------|
| 🔴 High (composite > 60%) | [N] | Quarterly review + monitor |
| 🟡 Medium (40-60%) | [N] | Semi-annual review |
| 🟢 Low (< 40%) | [N] | Annual review |

### By compliance status

| Status | Count |
|--------|-------|
| Fully compliant + AIA approved | [N] |
| Pending AIA | [N] |
| Pending РКН уведомление | [N] |
| **Need attention** | [N] |

### By sanctions exposure

| Exposure | Count |
|----------|-------|
| Russian vendor | [N] |
| Open-source self-hosted | [N] |
| US/EU vendor (restricted access) | [N] |
| US/EU via proxy / VPN | [N] |
| **At risk** | [N] |
```

### Шаг 4. Action items

```markdown
## Action items

### Immediate (within 30 days)

- [ ] [Specific gap] — owner [...]
- [ ] [Specific gap]

### Short-term (30-90 days)

- [ ] [...]

### Long-term

- [ ] [...]
```

### Шаг 5. Periodic update process

```markdown
## Inventory maintenance

- **Update frequency:** quarterly (минимум)
- **Trigger-based updates:**
  - New AI system deployed
  - Vendor change
  - Material AI policy update
  - Material regulatory change
- **Review meeting:** monthly compliance / quarterly governance
- **Storage:** [shared system / wiki / specialized GRC tool]
- **Access:** [restricted к compliance / legal / executive]
```

## Шаг 6. Special considerations

### Shadow AI

**Pattern:** Employees use ChatGPT / Claude / etc. accounts personal для work tasks, bypassing organization controls.

**Risk:**
- Sensitive data sent в неauthorized vendor
- 152-ФЗ violation
- IP leakage

**Mitigation:**
- Education + policy clarity
- Provide org-approved AI tools (so employees don't need shadow)
- Monitor for shadow usage (limited but possible)
- Updated AUP (acceptable use policy)

### AI in third-party tools

Many vendors now have built-in AI (Notion AI, Slack AI, etc.). Inventory:
- Что AI vendor включает по умолчанию
- Что мы opted into
- Какие данные туда отправляются
- Opt-out где не нужен

### Embedded models in product

Models деpended on в product (recommendation engines, etc.) — must be в inventory.

## Что НЕ делает

- Не делает technical audit (это data science / engineering)
- Не handles vendor negotiations (это procurement + legal)
- Не replaces formal GRC system если в large organization

## Attribution

Adapted from [`ai-governance-legal/ai-inventory`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/ai-inventory/SKILL.md) by Anthropic (Apache 2.0).

**Категория A:**
- Inventory template universal
- Add РФ-specific compliance status fields (152-ФЗ / ОВПД / РКН / sectoral)
- Sanctions exposure category — РФ-specific risk dimension

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
