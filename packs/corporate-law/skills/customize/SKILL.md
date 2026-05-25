---
name: customize
description: >
  Guided customization corporate-law practice profile — точечно изменить
  тип компании, состав участников, material thresholds, outside counsel
  bench, нотариус (для ООО), risk posture.
argument-hint: "[название секции]"
user_invocable: true
ported_from: corporate-legal/customize
ported_at: 2026-05-19
adaptation_category: A
---

# /customize (corporate-law profile)

См. общий pattern в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md).

## Mapping секций

| Хочет изменить | Секция в PROFILE.md |
|----------------|---------------------|
| Тип компании (ООО / АО / ПАО / НКО) | `## Кто мы` |
| Уставный капитал (изменение) | `## Корпоративная структура` |
| Состав участников / акционеров | `## Стейкхолдеры` |
| Бенефициары (115-ФЗ) | Стейкхолдеры → бенефициары |
| Material thresholds для escalation | `## Material matter thresholds` |
| Outside counsel + **нотариус** (для ООО) | `## Outside counsel` |
| Risk posture | `## Risk posture` |
| Корпоративный календарь | `## ЕГРЮЛ / отчётность` |
| Учёт реестра (АО — у регистратора) | `## House style` |

## РФ-specific guardrails

- **Уставный капитал ниже 10,000 руб для ООО** — нельзя (ст.14 ФЗ-14)
- **Реестр акционеров АО не у регистратора** — нарушение с 2014 (ФЗ-39 ст.8 — только лицензированный регистратор)
- **Бенефициары не указаны** — нарушение 115-ФЗ; банки могут отказать в обслуживании
- **ПАО с risk posture "агрессивный"** — incompatible с Банка России регуляторными требованиями

## Attribution

Adapted from [`corporate-legal/customize`](https://github.com/anthropics/claude-for-legal/blob/main/corporate-legal/skills/customize/SKILL.md)
by Anthropic (Apache 2.0).

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
