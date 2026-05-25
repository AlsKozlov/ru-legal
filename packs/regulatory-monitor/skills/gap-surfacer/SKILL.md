---
name: gap-surfacer
description: >
  Given regulatory change — identify какие наши ЛНПА / processes требуют update.
  Анализ через сравнение ЛНПА текста + сitations к измененной норме. Output:
  prioritized list ЛНПА для review + scope изменений в каждом.
argument-hint: "[NPA id измененной нормы]"
user_invocable: true
ported_from: regulatory-legal/gap-surfacer
ported_at: 2026-05-20
adaptation_category: B
---

# /gap-surfacer

## Назначение

Bridge от regulatory change → action items для compliance team. Без этого
skill — юрист должен manually пробегать все ЛНПА и понимать какие affected.

## Pre-flight

- `policy-diff` сделан — известно что changed
- ЛНПА repository доступен (из PROFILE.md)

## Workflow

### Шаг 1. Load наши ЛНПА

```markdown
- Положение о ПДн v3.2
- Антикоррупционная политика v2.1
- Правила внутреннего трудового распорядка v5.0
- ...
```

### Шаг 2. Scan каждый ЛНПА на ссылки к измененной норме

Для каждого ЛНПА — full-text search:
- Direct citation (`ст.5 152-ФЗ`)
- Indirect references (`персональные данные`, `обработка`)
- Concept matches (даже если не cited напрямую — semantic match)

### Шаг 3. Classify gap per ЛНПА

```markdown
| Gap type | Что | Priority |
|----------|-----|----------|
| **Direct citation broken** | ЛНПА cites старую ст.X которая теперь removed/renumbered | 🔴 immediate |
| **Required new section** | NPA добавил новое обязательство; наш ЛНПА не покрывает | 🔴 immediate |
| **Conflicting provision** | Наш ЛНПА противоречит новой норме | 🔴 immediate |
| **Outdated terminology** | NPA changed terminology; наш ЛНПА uses old | 🟡 medium |
| **No gap** | ЛНПА не affected | 🟢 none |
```

### Шаг 4. Generate gap report

```markdown
# Gap Analysis — [NPA name] изменения

## Date регуляторного change: [DD.MM.YYYY]
## Date наш review: [DD.MM.YYYY]
## Effective from: [DD.MM.YYYY]

## Affected ЛНПА

### 🔴 Critical updates (must do before effective date)

#### Положение о ПДн v3.2 → v3.3
- **Gap:** ст.5 152-ФЗ ч.2 расширила список special categories — добавлены биометрические vs было только при identification
- **Specific updates needed:**
  - Раздел 2.3 "Special categories" — добавить новые
  - Раздел 5 "Обработка биометрии" — refine consent requirements
- **Estimated effort:** 4-8 hours юриста
- **Action:** `/policy-redraft "Положение о ПДн"`

#### [next critical ЛНПА]

### 🟡 Medium updates

[...]

### 🟢 No update needed

- ЛНПА X — нет affected provisions

## Summary

- Total ЛНПА reviewed: [N]
- Critical updates: [N]
- Medium updates: [M]
- Estimated total effort: [hours]
- Deadline (NPA effective date): [DD.MM.YYYY]
```

### Шаг 5. Cross-references

- `/policy-redraft <ЛНПА>` — для каждого affected ЛНПА — auto-draft изменений
- HITL approval перед finalize
- Workflow integration с `corporate-law/policy-drafting` для new ЛНПА

## Attribution

Adapted from [`regulatory-legal/gap-surfacer`](https://github.com/anthropics/claude-for-legal/blob/main/regulatory-legal/skills/gap-surfacer/SKILL.md) by Anthropic (Apache 2.0).

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md).
