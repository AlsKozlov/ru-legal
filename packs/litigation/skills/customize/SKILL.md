---
name: customize
description: >
  Guided customization litigation practice profile — изменить точечно risk
  calibration, materiality thresholds, OC bench, escalation, etc., без re-run
  полного cold-start.
argument-hint: "[название секции]"
user_invocable: true
ported_from: litigation-legal/customize
ported_at: 2026-05-18
adaptation_category: A
---

# /customize (litigation profile)

См. полную методологию в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md) —
тот же pattern.

## Mapping секций для litigation profile

| Хочет изменить | Секция в PROFILE.md |
|----------------|---------------------|
| Risk calibration / materiality thresholds | `## Calibration рисков` |
| Outside counsel bench | `## Outside counsel` |
| Эскалация | `## Эскалация` |
| Юрисдикции | `## Юрисдикция и forums` |
| Тип практики (in-house / firm / адвокат) | `## Кто мы` |
| House style / маркировка | `## House style` |

## Attribution

Adapted from [`litigation-legal/customize`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/customize/SKILL.md)
by Anthropic (Apache 2.0). РФ-adapted mapping секций.

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
