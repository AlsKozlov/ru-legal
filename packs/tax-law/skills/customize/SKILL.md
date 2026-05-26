---
name: customize
description: >
  Guided customization tax profile — изменить систему налогообложения,
  открытые проверки / споры, outside-консультантов, risk posture.
argument-hint: "[название секции]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /customize (tax-law profile)

См. общий pattern в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md).

## Mapping секций

| Хочет изменить | Секция в PROFILE.md |
|----------------|---------------------|
| Налоговая система (переход ОСНО ↔ УСН) | `## Налоговая система` |
| Open налоговые проверки | `## Open налоговые вопросы` |
| Outside consultants | `## Outside consultants` |
| Risk posture | `## Risk posture` |
| Sector flags (IT, фарма, нефтегаз) | `## Кто мы` → Sector |

## РФ-specific guardrails

- **Переход с УСН на ОСНО mid-year** — обычно нельзя, переход с 1 января след.года
- **УСН с превышением лимита 251.4 млн (2026)** — automatic переход на ОСНО + retroactive recalc
- **Risk posture "агрессивный" для tax** — strongly NOT recommended; ВНП поднимет

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
