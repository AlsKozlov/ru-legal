---
name: customize
description: >
  Guided customization compliance-aml profile.
argument-hint: "[название секции]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
---

# /customize (compliance-aml)

См. общий pattern в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md).

## Mapping

| Изменить | Секция |
|----------|--------|
| Тип организации (115-ФЗ scope) | `## Кто мы` |
| Sanctions exposure | `## Sanctions exposure` |
| KYC / screening инфраструктура | `## Compliance infrastructure` |
| Outside consultants | `## Outside consultants` |
| Risk posture | `## Risk posture` |

## Guardrails

- **Risk posture "агрессивный"** — strongly NOT recommended для AML
- **Compliance officer не назначен** — нарушение 115-ФЗ
- **ПВК не утверждены** — нарушение

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
