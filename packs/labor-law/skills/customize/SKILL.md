---
name: customize
description: >
  Guided customization labor-law practice profile — точечно изменить
  jurisdictional footprint (если филиалы в нескольких регионах), risk
  posture, severance baseline, escalation contacts, без re-run полного
  cold-start interview.
argument-hint: "[название секции]"
user_invocable: true
ported_from: employment-legal/customize
ported_at: 2026-05-18
adaptation_category: A
---

# /customize (labor-law profile)

См. общий pattern в [contract-law/customize](../../../contract-law/skills/customize/SKILL.md) — методология идентичная.

## Mapping секций для labor-law profile

| Хочет изменить | Секция в PROFILE.md |
|----------------|---------------------|
| Тип работодателя (микро / малое / среднее / крупное) | `## Кто мы` |
| Регионы присутствия (районные коэффициенты, северные надбавки) | `## Юрисдикции` |
| Категории работников (защищённые, иностранцы, удалёнка) | `## Состав персонала` |
| Risk posture (консервативный / средний / агрессивный) | `## Risk posture` |
| Severance baseline (соглашение сторон — какая компенсация по умолчанию) | `## Termination practice` |
| Эскалация (HR директор / внешний адвокат) | `## Эскалация` |
| Outside counsel bench (юристы по трудовым спорам) | `## Outside counsel` |
| ЛНПА репозиторий (путь к правилам, положениям) | `## ЛНПА repository` |

## РФ-specific guardrails

- **Беременные и работники с детьми до 3 лет** — нельзя disable защиту в profile.
  Это императивная норма (ст.261 ТК).
- **Сокращение штата** — нельзя выставить риск aggressive ниже определённого
  уровня. Procedural defects → восстановление + средний заработок за вынужденный
  прогул. Это load-bearing constraint.
- **Профсоюз** — если есть, обязательная секция в profile. Невозможно "skip".

## Attribution

Adapted from [`employment-legal/customize`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/customize/SKILL.md)
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
