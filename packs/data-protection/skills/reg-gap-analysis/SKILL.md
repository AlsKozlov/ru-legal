---
name: reg-gap-analysis
description: >
  Diff'ит новую или изменённую норму (152-ФЗ изменения, приказы РКН, ПП РФ, письма
  регулятора) против current политики и practice — outputs gap list и план
  remediation с owners и сроками. Используй когда вышел новый ФЗ-XXX, "влияет ли
  на нас [нормативный акт]", "gap analysis для [приказ РКН]", "compliance check
  против [регулирование]", или пользователь paste'ит regulatory text.
argument-hint: "[название регулирования, или paste regulatory text/summary]"
user_invocable: true
ported_from: privacy-legal/reg-gap-analysis
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /reg-gap-analysis (gap analysis для изменений 152-ФЗ)

## Назначение

152-ФЗ — **fast-moving regulatory area** в РФ:
- ФЗ-266 от 14.07.2022 — введение ОВПД
- ФЗ-420 от 30.11.2024 — увеличение штрафов
- С 01.03.2023 — двухэтапное уведомление РКН для cross-border
- С 30.05.2025 — штрафы до 18 млн (cross-border)
- С 01.07.2025 — ужесточение локализации
- Постановления Правительства РФ обновляются регулярно (например ПП №1119 — уровни защиты)
- Приказы РКН и Минцифры

Этот skill — **gap analysis** при появлении нового regulation: что нужно изменить
у нас?

---

## Workflow

### Шаг 1. Load PROFILE.md

Прочитай:
- `## Политика обработки ПДн` (commitments)
- `## Системы обработки ПДн` (где обрабатывается ПДн)
- `## Системы и инфраструктура`
- Existing compliance state

### Шаг 2. Получить regulation

- Пользователь paste'ил текст → use as is
- Указал название → fetch через `pravo-mcp` (если подключён)
- Если оба нет — спросить ссылку или text

### Шаг 3. Scope: applies ли к нам?

Определи:

**Юрисдикция:**
- Регулирование РФ? Применяется к operator'ам, обрабатывающим ПДн **российских
  граждан** (extraterritorial reach 152-ФЗ)
- Применяется к нашим operations?

**Sector:**
- Применяется к нашей отрасли? (некоторые приказы — только для банков, медицины, и т.д.)

**Thresholds:**
- Применяется при определённом размере (количество субъектов, оборот)?
- Применяется ли к нашим объёмам?

**Effective date:**
- Когда вступает в силу?
- Transition period есть?

Если **не applies** → output: "Это регулирование не применяется к [нашей
организации] по [конкретное основание]. No action needed." Stop.

### Шаг 4. Extract requirements

Из текста регулирования — extract **конкретные** требования:

```yaml
requirements:
  - id: req-1
    text: "Оператор обязан в течение 24 часов с момента обнаружения
           утечки ПДн уведомить Роскомнадзор."
    type: notification
    owner_role: DPO
    deadline_relative_to_event: 24h
    citation: "Приказ РКН №ХХХ ст.Y п.Z"

  - id: req-2
    text: "При обработке биометрических ПДн использовать сертифицированные
           средства защиты УЗ-2."
    type: technical_security
    owner_role: IT Security
    citation: "ПП РФ №1119"
```

### Шаг 5. Diff против current state

Для каждого requirement — check:

| Requirement | Current state | Gap | Priority |
|-------------|---------------|-----|----------|
| 24-hour инцидент notification | Сейчас 72 часа в incident-plan | **Yes** — обновить план | 🔴 Critical |
| Биометрия УЗ-2 средства | Сейчас УЗ-3 общие средства | **Yes** — закупить и сертифицировать | 🟡 High |
| Cross-border двухэтапное уведомление | Подаём один раз | **Yes** — добавить шаг 1 | 🔴 Critical |

### Шаг 6. Remediation plan

Для каждого gap'а:

```markdown
## Gap [N]: [Краткое описание]

**Requirement:** [цитата нормы]
**Citation:** [конкретная статья / пункт]
**Effective date:** [DD.MM.YYYY]

**Current state:** [что у нас сейчас]

**Action required:**
- [ ] [Конкретное действие 1]
- [ ] [Конкретное действие 2]

**Owner:** [DPO / Юрист / IT Security / др.]
**Deadline:** [DD.MM.YYYY — реалистичный с учётом effective date]
**Estimated effort:** [часов / дней / недель]
**Risk if not done:** [штраф / иск / репутационный]

**Dependencies:**
- [Если нужно coordinate с другими отделами]
```

### Шаг 7. Final output

```markdown
[МАРКИРОВКА]

# Reg Gap Analysis: [Название регулирования]

**Дата анализа:** [DD.MM.YYYY]
**Регулирование:** [Полное название + citation]
**Effective date:** [DD.MM.YYYY]

---

## Executive Summary

**Applies to us?** Да / Нет / Частично

[Если "Нет"]
[Объяснение почему — конкретные основания]

[Если "Да" или "Частично"]
**Gaps found:** [N]
- 🔴 Critical: [N]
- 🟡 High: [N]
- 🟢 Medium / Low: [N]

**Estimated total effort:** [hours / days / weeks]
**Deadline (earliest):** [DD.MM.YYYY]

---

## Scope check

[Какие части регулирования applies к нам, какие нет, с обоснованием]

---

## Gaps

### Critical

[List of critical gaps с remediation plans]

### High

[...]

### Medium / Low

[...]

---

## Remediation roadmap

| Sequence | Action | Owner | Deadline | Status |
|----------|--------|-------|----------|--------|
| 1 | [...] | DPO | [date] | ☐ |
| 2 | [...] | IT Security | [date] | ☐ |
| ... | | | | |

---

## Sign-off

После remediation — DPO + GC sign-off на закрытие gap'ов.
```

---

## Common РФ reg changes (примеры)

### ФЗ-266 от 14.07.2022

Введение обязательной ОВПД (ст.18.1). Все operator'ы должны проводить.

### ФЗ-420 от 30.11.2024

Существенное увеличение штрафов РКН:
- Утечка ПДн (>10 тыс субъектов): до 18 млн руб
- Утечка спец.категорий: до 25 млн руб
- Локализация (ст.18 ч.5): до 18 млн повторно
- Cross-border без уведомления: до 18 млн

### Постановление Правительства РФ от 04.07.2025 №1071 (примерное)

Новые требования к обезличиванию ПДн.

### Приказы РКН (несколько в год)

- Обновление перечня стран надлежащего уровня защиты для cross-border
- Методические рекомендации по проведению ОВПД
- Требования к содержанию политики обработки ПДн

---

## Что этот skill НЕ делает

- Не реализует remediation сам — только plan
- Не fetch'ит regulatory texts automatically (если pravo-mcp не подключён)
- Не делает legal opinion при сложной интерпретации — GC review
- Не следит за изменениями автоматически — это работа `regulatory-monitor` agent
  (Phase 2)

---

## Attribution

Adapted from [`privacy-legal/reg-gap-analysis`](https://github.com/anthropics/claude-for-legal/blob/main/privacy-legal/skills/reg-gap-analysis/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения от оригинала:**

- **Workflow universal** (категория A)
- **РФ regulatory landscape examples** — actual recent changes (ФЗ-266, ФЗ-420,
  ПП РФ 1119, приказы РКН)
- **Citations format** — РФ норма structure (статья, пункт, ПП РФ номер)
- **Path:** → `~/.ru-legal/profiles/data-protection/PROFILE.md`

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-18.

---

## Disclaimer

Этот skill производит gap analysis для DPO + GC. Не legal advice. Final
remediation plan утверждается + tracked DPO.

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
