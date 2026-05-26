---
name: portfolio-status
description: >
  Rollup всего портфолио matter'ов: risk distribution, дедлайны в 14/30/60-day
  bands, материальность, distribution по типам дел, аномалии (stale, conflicts
  pending, etc.). Используй когда пользователь говорит "обзор портфолио",
  "что у нас по делам", "portfolio rollup", или для periodic review (weekly /
  monthly).
argument-hint: "[--window N (default 60 дней)]"
user_invocable: true
ported_from: litigation-legal/portfolio-status
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /portfolio-status

## Назначение

Bird's-eye view всего портфолио — что у нас, что критично, что требует attention.

## Workflow

### Шаг 1. Load all matters

Read `~/.ru-legal/profiles/litigation/matters/_log.yaml` — все active rows.

### Шаг 2. Aggregate

#### Risk distribution

| Rating | Count | Total exposure |
|--------|------:|---------------:|
| 🔴 Critical | [N] | [сумма руб] |
| 🟠 High | [N] | [...] |
| 🟡 Medium | [N] | [...] |
| 🟢 Low | [N] | [...] |

#### Deadline bands

| Окно | Count | Самый близкий |
|------|------:|---------------|
| 🔴 0-14 дней | [N] | [matter X — DD.MM.YYYY] |
| 🟠 15-30 дней | [N] | [...] |
| 🟡 31-60 дней | [N] | [...] |

#### Materiality

| Уровень | Count | Total exposure |
|---------|------:|---------------:|
| Сильно material (>Y руб) | [N] | [...] |
| Material (X-Y руб) | [N] | [...] |
| Не material (<X руб) | [N] | [...] |

#### По типам дел

| Тип | Count | Active / On hold | Average exposure |
|-----|------:|------------------|------------------|
| Договорные (ГК) | [N] | [N/N] | [...] |
| Налоговые (НК) | [N] | [N/N] | [...] |
| Корпоративные | [N] | [N/N] | [...] |
| Трудовые | [N] | [N/N] | [...] |
| Банкротство | [N] | [N/N] | [...] |
| Антимонопольные | [N] | [N/N] | [...] |
| ИС | [N] | [N/N] | [...] |
| Иные | [N] | [N/N] | [...] |

#### Stage breakdown

| Stage | Count |
|-------|------:|
| Pre-suit (досудебка) | [N] |
| Filed (поданы) | [N] |
| Discovery (АПК ст.66 этап) | [N] |
| Trial (рассмотрение) | [N] |
| Appeal (апелляция) | [N] |
| Settlement negotiation | [N] |

### Шаг 3. Anomalies

Flag matters which require attention:

#### 🚨 Conflicts pending

| Matter | Days since intake | Conflicts owner |
|--------|------------------|-----------------|
| [...] | [N] | [имя] |

#### ⚠️ Stale (no update >30 days)

| Matter | Last update | Days since |
|--------|-------------|------------|
| [...] | [DD.MM.YYYY] | [N] |

#### ⏰ Overdue deadlines

| Matter | Deadline | Days overdue | Action |
|--------|----------|--------------|--------|
| [...] | [...] | [N] | [...] |

#### 📊 Exposure concentration

Если concentration > 50% exposure в одном matter'е — flag:

> ⚠️ Matter "[X]" составляет [Y]% всего exposure — single point of failure.
> Recommend: backup attorney + frequent updates.

#### 💼 No outside counsel но severity high

Matters рейтинга high/critical без external attorney:

| Matter | Risk | Why no external? |
|--------|------|------------------|
| [...] | [...] | [reason или "needs review"] |

### Шаг 4. Trends (если есть history)

Если runs portfolio-status periodically — compare:

- Total exposure trend: [+/- N% vs last quarter]
- Active matters: [+/- N vs last quarter]
- Settlement rate: [% за последний период]
- Average matter duration: [N days]

### Шаг 5. Output

Combine secticons в single Markdown document.

В конце:

```markdown
## Recommended actions

1. [Critical action 1 — owner + deadline]
2. [Important action 2]
3. [...]
```

---

## РФ-specific aggregations

- **Налоговые споры:** доля выигрышных дел против ФНС за последний год (типично
  низкая для бизнеса — для context'а)
- **Антимонопольные:** active ФАС матеры — особый risk profile (часто публичный
  reputational)
- **Банкротство кредиторов:** включения в реестр требований кредиторов — стоит
  отдельный bucket (часто crowded forum)

---

## Attribution

Adapted from [`litigation-legal/portfolio-status`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/portfolio-status/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:** Russian terminology для типов дел, РФ-specific aggregations (налоговые,
банкротство), discovery → АПК ст.66.

**Path:** → `~/.ru-legal/profiles/litigation/matters/_log.yaml`

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## Disclaimer

Portfolio rollup — utility. Не legal advice. Strategic decisions за GC.

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
