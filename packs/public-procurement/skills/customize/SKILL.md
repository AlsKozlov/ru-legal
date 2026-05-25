---
name: customize
description: >
  Guided customization public-procurement profile — изменить ОКВЭДы, ЭТП
  аккредитации, МСП статус, outside consultants, risk posture.
argument-hint: "[название секции]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
---

# /customize (public-procurement)

См. общий pattern в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md).

## Mapping секций

| Хочет изменить | Секция в PROFILE.md |
|----------------|---------------------|
| Тип компании / МСП статус | `## Кто мы` |
| Виды закупок (44/223) | `## Виды закупок` |
| Сферы участия / ОКВЭДы | `## Сферы участия` |
| ЭТП аккредитации | `## Аккредитации` |
| Финансовые возможности | `## Финансовые возможности` |
| Risk posture | `## Risk posture` |

## РФ-specific guardrails

- **МСП статус** — verifiable через Реестр МСП ФНС; нельзя false-claim
- **РНП попадание** — automatic disqualification на 2 года; не игнорировать
- **Аккредитация на ЭТП** — automatic с 2018 для зарегистрированных в ЕИС

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
