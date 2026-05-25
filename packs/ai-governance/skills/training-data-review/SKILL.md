---
name: training-data-review
description: >
  RU-unique. Review training data на compliance — 152-ФЗ ПДн в training data,
  авторские права (для generative AI — критично!), public datasets licensing,
  sensitive content filtering, sanctions-related sources (post-2022).
argument-hint: "[training data source / описание]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
---

# /training-data-review

## Назначение

Pre-training review data sources для compliance + risk avoidance. Critical для:
- Fine-tuning LLM на specific data
- Training classical ML на customer data
- Computer vision training на images
- Building NL processing dataset

## Categories training data sources

### A. Internal data (наша)

- Customer interactions (chat logs, support tickets, calls)
- Internal documents
- Employee data
- Business transactions

### B. Public data (open source)

- Common Crawl
- Wikipedia
- Public papers / books in public domain
- Open datasets (HuggingFace, Kaggle, etc.)

### C. Purchased / Licensed data

- Commercial datasets от vendors
- News archives под licenses
- Industry-specific data

### D. User-generated content (UGC)

- Social media posts / comments (если у нас platform)
- Forum posts
- Reviews

### E. Synthetic / generated data

- Augmented from real data
- Fully synthetic generation
- LLM-generated training data

## Review framework

### A. ПДн compliance (152-ФЗ)

#### Identify ПДн в training data

```markdown
## ПДн assessment

- [ ] Имена / контакты
- [ ] Адреса
- [ ] Идентификаторы (ИНН, СНИЛС, паспорт)
- [ ] Биометрия
- [ ] Health data (special category — ст.10)
- [ ] Political / religious / sexual orientation (special category)
- [ ] Photos / voice — могут identifying
- [ ] Quasi-identifiers (комбинации dating, location, demographic — могут identify)

If any → 152-ФЗ applies.
```

#### Legal basis assessment

```markdown
## Legal basis для использования ПДн в training

| Basis | Когда applicable | Documentation needed |
|-------|------------------|-----------------------|
| Согласие субъекта (ст.6 ч.1 п.1) | Если consent explicitly включает training AI | Запись согласия + scope |
| Договор (ст.6 ч.1 п.5) | Если training необходимо для оказания услуг по договору | Договор + анализ необходимости |
| Законные интересы (ст.6 ч.1 п.7) | Если интерес weighs over interest субъекта | Документация баланса interests + assessment |
| Public availability (ст.6 ч.1 п.10) | Если data publicly available **и** разглашена самим субъектом | Документация source — public |

⚠ **Если нет legal basis** → нельзя использовать ПДн.
```

#### Anonymization / De-identification

```markdown
## Если anonymization possible

- **Direct identifiers removal** (имена, ID, контакты) — minimum
- **Quasi-identifiers** (combinations) — requires careful handling
- **k-anonymity / differential privacy** — для material exposure
- **After anonymization** — если truly anonymized, no longer ПДн (ст.3 152-ФЗ)
- **Risk re-identification** — high if data rich

→ Recommend anonymization где applicable; verify сложность re-identification.
```

#### Special category ПДн

```markdown
## Special category check (ст.10 152-ФЗ)

If training data contains:
- Раса / этническое происхождение
- Политические взгляды
- Религиозные / философские убеждения
- Сведения о здоровье
- Биометрия (для identification)
- Sex life / sexual orientation
- Criminal records
- (новые с 2024: трудовая активность, имущественное положение, и др.)

→ Use требует **отдельное явное согласие** OR одно из ограниченных оснований
ст.10. **Higher scrutiny**.
```

### B. Copyright + IP compliance

#### Copyright в training data

```markdown
## Copyright assessment

### Licensed for training?

- [ ] Source имеет explicit "OK for AI training" — best
- [ ] Source имеет broad license covering ML use — good
- [ ] Source — public domain — OK
- [ ] Source — CC license — check specific (some restrict commercial use)
- [ ] Source — fair use claimed (с argument) — risky в РФ (нет US fair use doctrine)
- [ ] Source — unlicensed scraped — high risk

### РФ-specific copyright considerations

- РФ не имеет US fair use doctrine — strict licensing required
- **Ст.1274 ГК** — citation / scientific use allowed limited (не commercial training)
- **Произведения public domain** — после 70 лет с смерти автора (ст.1281 ГК)
- **Произведения с CC-BY** — атрибуция required
- **Произведения с CC-NC** — нельзя commercial use (в т.ч. training)

### Specific risk areas

| Source type | Risk | Mitigation |
|-------------|------|------------|
| News articles | High | Licensed datasets only |
| Books | High | Public domain only or licensed |
| Code (GitHub) | Medium | Check repository licenses; OSS licenses preserved |
| Images | High | Stock photo licensing или CC-BY/CC0 only |
| Music / audio | High | Licensed only |
| Movies / video | High | Licensed only |
| Wikipedia text | Low | CC-BY-SA — share-alike but attribution required |
| Scientific papers | Med | Open access (CC) OK; subscription — careful |
```

### C. Sensitive content filtering

```markdown
## Sensitive content в training data

- [ ] Hate speech / extremism (запрещён ст.6 ФЗ-114 для distribution)
- [ ] Criminal content
- [ ] Sexually explicit material
- [ ] Content involving minors
- [ ] Self-harm / suicide content
- [ ] Misinformation / disinformation
- [ ] State secrets

→ Filter / remove before training. Otherwise:
- Model может generate such content
- Liability для harmful outputs
- Compliance violations
```

### D. РФ-specific concerns post-2022

```markdown
## Sanctions / source country issues

### Sources from недружественных stran

- US-origin datasets — потенциальная access ограничена (HuggingFace might restrict)
- Some datasets могут содержать content "discrediting" РФ (ст.20.3.3 КоАП) — flag

### Russian government data

- Открытые государственные dataset (https://data.gov.ru) — OK
- Restricted source data — separate clearance

### Foreign vendors

- US OFAC may restrict providing data services к РФ entities
- Practical workarounds (proxy / VPN access) — business risk
```

### E. Quality + bias

```markdown
## Quality + bias

- [ ] Data representative of population AI будет serve?
- [ ] Subgroup coverage adequate?
- [ ] Labels / annotations quality verified?
- [ ] Data freshness / staleness OK?
- [ ] Outliers / noise managed
- [ ] Class imbalance addressed
```

## Workflow

### Шаг 1. Inventory training data sources

```markdown
## Training data inventory

| # | Source | Type | Volume | License | ПДн? | Risk |
|---|--------|------|--------|---------|------|------|
| 1 | Internal chat logs 2023-2025 | Internal | 1M conversations | Internal use | Yes (имена, content) | 🟡 |
| 2 | Wikipedia RU | Public | 5GB | CC-BY-SA | No | 🟢 |
| 3 | Customer support tickets | Internal | 500k | Internal use | Yes | 🟡 |
| 4 | Industry papers (purchased) | Licensed | 100GB | Vendor license | Maybe (authors) | 🟢 |
| 5 | Web scrape news 2024 | Scraped public | 50GB | None | Yes (subjects in news) | 🔴 |
```

### Шаг 2. Per-source compliance check

Apply checklists A-E above to each source.

### Шаг 3. Risk findings + mitigation

```markdown
## Findings

### 🔴 Critical

1. **Web scrape news (source 5)** — copyright violation risk + ПДн без legal basis
   - Mitigation: drop этот источник, ИЛИ licensed alternative

### 🟡 Medium

1. **Internal chat logs (source 1)** — ПДн в training requires legal basis
   - Mitigation: anonymize before training, ИЛИ documented legitimate interests

### 🟢 OK

1. Wikipedia, licensed papers
```

### Шаг 4. Remediation plan

```markdown
## Action items

- [ ] Drop / replace problematic sources
- [ ] Anonymization pipeline implemented
- [ ] Legal basis documented для каждого ПДн source
- [ ] Licensed alternatives explored для replacement
- [ ] Filtering pipeline для sensitive content
- [ ] Documentation of training data lineage (для audit)
```

### Шаг 5. Documentation

Создать **Datasheet** для training data (industry best practice):
- Sources
- Legal basis per source
- Volumes
- Date range
- Known issues
- Mitigations applied

## Output

```markdown
# Training Data Review — [model / use case]

## Bottom line

[Proceed with training / Modify and re-review / Cannot proceed without fundamental changes]

## Sources analyzed

[Table from Step 1]

## Critical issues

[From Step 3 🔴]

## Mitigations applied

[From Step 4]

## Datasheet attachment

[Link to formal datasheet]

## Sign-off needed

- [ ] DPO (для 152-ФЗ aspects)
- [ ] IP counsel (для copyright)
- [ ] AI Officer
```

## Что НЕ делает

- Не performs actual anonymization (это data engineering)
- Не licensed datasets (это procurement + legal)
- Не handles legal review для material commercial models — engage outside-адв ФПА

## Why RU-unique

US fair use doctrine — allows certain unlicensed training (с растущим legal challenge). РФ — no fair use; strict licensing required. Plus 152-ФЗ + sanctions overlays.

**Правовая основа:**
- 152-ФЗ (особ. ст.6, ст.10, ст.18.1)
- Часть 4 ГК РФ (особ. ст.1270, 1274, 1281)
- ФЗ-114 «О противодействии экстремизму»
- ФЗ-149 «Об информации»
- ст.20.3.3 КоАП («discrediting» РФ ВС — для filtering)

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
