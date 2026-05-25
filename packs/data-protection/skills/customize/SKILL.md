---
name: customize
description: >
  Guided customization вашего privacy practice profile (PROFILE.md в data-protection)
  — изменить точечно без re-run полного cold-start. Adjust DSAR процесс, политику
  обработки ПДн commitments, эскалацию, integrations, регуляторный footprint.
  Используй когда говорите "измени мой DPO", "обнови privacy profile", "edit
  политику", "tune config".
argument-hint: "[название секции, или опиши что хочешь изменить]"
user_invocable: true
ported_from: privacy-legal/customize
ported_at: 2026-05-18
adaptation_category: A
---

# /customize (privacy profile)

См. полную методологию в [contract-law/customize](../../contract-law/skills/customize/SKILL.md) —
тот же pattern.

## Specifically для data-protection profile

Mapping секций PROFILE.md → что менять:

| Что хочет изменить | Секция в PROFILE.md |
|--------------------|---------------------|
| "DPO contact", "ответственный за ПДн" | `## Кто пользуется → Контакт DPO` |
| "Системы где обрабатывается ПДн" | `## Системы обработки ПДн` |
| "Локализация", "infrastructure" | `## Локализация ПДн` |
| "Cross-border" | `## Cross-border передача` |
| "DSAR процесс", "адрес для запросов" | `## DSAR процесс` |
| "Шаблоны ответов" | references/templates |
| "Политика обработки URL" | `## Политика обработки ПДн` |
| "Эскалация" | `## Эскалация` |
| "План реагирования на утечку" | `## Утечки / инциденты` |

## Что часто нужно изменять РФ DPO

1. **Контакт DPO** — смена ответственного, обновление email
2. **Системы где обрабатываются ПДн** — внедрение новой системы, отключение старой
3. **Локализация** — переезд в РФ ЦОД (часто после РКН проверок)
4. **Sub-processor'ы** — смена vendor (например, ушли с foreign SaaS на Yandex Cloud)
5. **План реагирования на утечку** — обновление по новым практикам РКН

## Attribution

Adapted from [`privacy-legal/customize`](https://github.com/anthropics/claude-for-legal/blob/main/privacy-legal/skills/customize/SKILL.md)
by Anthropic (Apache 2.0). РФ-adapted via mapping секций под data-protection
PROFILE.md.

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-18.

---

## Disclaimer

Customize — утилитный skill. Не legal advice. Изменения PROFILE.md влияют на все
downstream skills — review с DPO перед существенными changes.

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
