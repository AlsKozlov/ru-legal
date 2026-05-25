---
name: reg-feed-watcher
description: >
  Killer skill для regulatory-monitor. Daily / weekly scan новых НПА в нашей
  sphere of interest через pravo MCP. РФ specifics: source list — pravo.gov.ru
  (official), publication.pravo.gov.ru (новые акты), сайты ФНС / Банка России /
  РКН / ФАС для sectoral.
argument-hint: "[period: today/week/month] [areas: optional filter]"
user_invocable: true
ported_from: regulatory-legal/reg-feed-watcher
ported_at: 2026-05-20
adaptation_category: B
---

# /reg-feed-watcher

## Назначение

Регулярный scan новых нормативных актов РФ в наших sphere of interest. Output:
structured digest с classification (critical / material / informational).

## Pre-flight

- `cold-start-interview` пройден — areas of interest известны
- `pravo` MCP available

## Sources

| Источник | Что | Update freq |
|----------|-----|-------------|
| pravo.gov.ru (Documents API) | Все официально опубликованные НПА | Daily |
| Сайт Банка России — Положения / Указания | Банковское / страховое | Weekly |
| Сайт ФНС | Налоговые приказы / письма | Weekly |
| Сайт РКН | Положения о ПДн / реклама | Weekly |
| Сайт ФАС | Антимонопольные акты | Weekly |
| Минцифры — IT-сертификации / реестр ПО | IT-аккредитация | Monthly |
| Постановления Пленума ВС РФ | Судебная практика | Quarterly |

## Workflow

### Шаг 1. Determine period + scope

```markdown
- **Period:** [today / last 7 days / last 30 days]
- **Areas:** [список из PROFILE.md areas of interest]
- **Channels (NPA types):** [ФЗ, Указы, Постановления, Приказы]
```

### Шаг 2. Query pravo MCP per area

Для каждого area — search NPA published в period с relevant keywords:

```python
# Example psыeudocode
for area in profile.areas_of_interest:
    keywords = AREA_KEYWORDS[area]
    npa_list = pravo.search_npa(
        query=" OR ".join(keywords),
        date_from=period_start,
        date_to=today,
    )
    process(npa_list, area=area)
```

### Шаг 3. Classify каждый NPA

```markdown
| Tier | Что | Action |
|------|-----|--------|
| 🔴 **Critical** | Прямо меняет норму, на которой основаны наши ЛНПА | Immediate review + gap analysis |
| 🟡 **Material** | Меняет related нормы, может affect нас | Schedule review в течение недели |
| 🟢 **Informational** | Не влияет напрямую но в нашей area | Log в archive |
```

### Шаг 4. Generate digest

```markdown
# Regulatory Feed — [period]

## 🔴 Critical (требуют immediate action)

1. **[FZ-XX от DD.MM.YYYY]** — название акта
   - Что изменилось: [...]
   - Затронуто: [конкретные ЛНПА / processes]
   - Срок вступления в силу: [DD.MM.YYYY]
   - Recommended action: `/gap-surfacer NPA-id`

## 🟡 Material

[Same format]

## 🟢 Informational

[Same format]

## Summary

- Total NPA reviewed: [N]
- Critical: [N] / Material: [N] / Informational: [N]
- Next scheduled review: [DD.MM.YYYY]
```

### Шаг 5. Trigger downstream actions

Для каждого 🔴 NPA — recommend:
- `/policy-diff` — diff с previous version
- `/gap-surfacer` — какие наши ЛНПА need update
- `/policy-redraft` — auto-draft updated ЛНПА

## Output для TG bot

Compact format подходящий для daily TG notification:

```
📊 Regulatory digest за [DD.MM.YYYY]

🔴 1 critical: 152-ФЗ изменения — штрафы РКН до 18M
🟡 3 material: ст.5.27 КоАП обновлена; и др.
🟢 12 informational

Подробнее: /skill regulatory-monitor/reg-feed-watcher
```

## Что НЕ делает

- Не выполняет рассылку (это TG bot / email service)
- Не updates ЛНПА automatically (это `/policy-redraft` с HITL approval)
- Не replaces юр.эксперта для interpretation сложных изменений

## Attribution

Adapted from [`regulatory-legal/reg-feed-watcher`](https://github.com/anthropics/claude-for-legal/blob/main/regulatory-legal/skills/reg-feed-watcher/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:**
- US Federal Register / state feeds → РФ pravo.gov.ru + Банк России + ФНС + sectoral regulators
- Sectoral overlays РФ-specific

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md). Material regulatory changes — review outside-адв ФПА перед adapting наши compliance.
