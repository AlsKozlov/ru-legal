---
name: policy-diff
description: >
  Compare предыдущую и новую редакции НПА — что именно изменилось в тексте.
  Useful когда `reg-feed-watcher` flagged change — этим skill понимаем precisely
  what меняется. Output: structured diff с classification (added / removed /
  modified articles).
argument-hint: "[NPA id или название] [old version date] [new version date]"
user_invocable: true
ported_from: regulatory-legal/policy-diff
ported_at: 2026-05-20
adaptation_category: B
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /policy-diff

## Назначение

Article-by-article diff между двумя редакциями НПА.

## Pre-flight

- `pravo` MCP available
- Известны obe versions (через `get_npa_version_at_date`)

## Workflow

### Шаг 1. Fetch обе версии

```python
old = pravo.get_npa_version_at_date(hash, on_date=old_date)
new = pravo.get_npa_version_at_date(hash, on_date=new_date)
```

### Шаг 2. Identify changed articles

Для каждой статьи / части:
- **Added** — есть в new, нет в old
- **Removed** — есть в old, нет в new
- **Modified** — текст изменился

### Шаг 3. Classify materiality

```markdown
| Change | Materiality | Action |
|--------|-------------|--------|
| Editorial (опечатки, формат) | Minor | Log |
| Технические (definitions, references) | Medium | Review для cascade effects |
| Substantive (новые обязанности, штрафы, права) | Material | Trigger gap-surfacer |
| Структурные (новые главы, кодекс-level rewrites) | Critical | Immediate full review |
```

### Шаг 4. Output diff

```markdown
# Diff: [NPA name] — [old_date] → [new_date]

## Summary

- Added articles: [N]
- Removed articles: [M]
- Modified articles: [K]
- Materiality: [Critical / Material / Medium / Minor]

## Critical changes

### Added: ст.X (новая)

[Полный текст новой статьи]

**Materiality:** [...]
**Affects:** [какие наши ЛНПА / processes]
**Effective from:** [DD.MM.YYYY]

### Modified: ст.Y

**Old (до DD.MM.YYYY):**
> [Старый текст]

**New (с DD.MM.YYYY):**
> [Новый текст]

**Key difference:** [analysis]
**Affects:** [...]

### Removed: ст.Z

[Что было удалено]
**Replacement:** [если applicable, какая статья теперь применяется]

## Recommended actions

1. `/gap-surfacer NPA_id` — какие наши ЛНПА need update
2. `/policy-redraft <наш ЛНПА>` — auto-draft изменений
3. Engage outside-адв для interpretation если ambiguous
```

## Attribution

Adapted from [`regulatory-legal/policy-diff`](https://github.com/anthropics/claude-for-legal/blob/main/regulatory-legal/skills/policy-diff/SKILL.md) by Anthropic (Apache 2.0).

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md).
