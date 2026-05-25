---
name: customize
description: >
  Guided customization ai-governance profile — изменить AI maturity, систему,
  regulatory context, sanctions exposure, AI policy state, risk posture.
argument-hint: "[название секции]"
user_invocable: true
ported_from: ai-governance-legal/customize
ported_at: 2026-05-19
adaptation_category: A
---

# /customize (ai-governance)

См. общий pattern в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md).

## Mapping

| Изменить | Секция |
|----------|--------|
| AI maturity | `## Кто мы` |
| AI use focus | `## AI use focus` |
| AI systems используемые | `## Текущие AI systems` |
| Regulatory context | `## Regulatory context` |
| Sanctions exposure | `## Sanctions exposure` |
| AI policy state | `## Internal AI policy` |
| Risk posture | `## Risk posture` |

## Guardrails

- **Risk posture "агрессивный" с медицинским / финансовым AI** — strongly NOT recommended (regulatory risk too high)
- **Production AI без AI policy** — flag для immediate attention
- **AI processing ПДн без 152-ФЗ compliance** — нарушение → штрафы РКН до 18M

## Attribution

Adapted from [`ai-governance-legal/customize`](https://github.com/anthropics/claude-for-legal/blob/main/ai-governance-legal/skills/customize/SKILL.md) by Anthropic (Apache 2.0).

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
