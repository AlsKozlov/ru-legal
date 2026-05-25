---
name: cold-start-interview
description: >
  First-run для regulatory-monitor pack. Заполняет PROFILE.md: areas of interest
  (152-ФЗ / 115-ФЗ / ТК / sectoral), subscription mode, ЛНПА repository.
argument-hint: "[optional: section]"
user_invocable: true
ported_from: regulatory-legal/cold-start-interview
ported_at: 2026-05-20
adaptation_category: B
---

# /cold-start-interview (regulatory-monitor)

## Workflow

### Шаг 1. Тип организации + ОКВЭДы

### Шаг 2. Areas of regulatory interest

Какие отрасли законодательства tracking? Выбери all applicable из list:
- ПДн (152-ФЗ + 215-ФЗ + sectoral)
- AML (115-ФЗ + Банк России acts)
- ТК + охрана труда
- НК + sectoral налоговые НПА
- IP (часть 4 ГК + Роспатент acts)
- Procurement (44/223 ФЗ + ПП РФ)
- Sanctions (Указы Президента post-2022)
- Sectoral (медицина / финансы / IT / иное)

### Шаг 3. Subscription mode

- Daily digest для critical (sanctions / banking)
- Weekly для most
- Event-driven для опциональных

### Шаг 4. ЛНПА repository inventory

List всех наших ЛНПА которые могут require updates при regulatory changes.

### Шаг 5. Notification channels

### Шаг 6. Save + confirm

## Attribution

Adapted from [`regulatory-legal/cold-start-interview`](https://github.com/anthropics/claude-for-legal/blob/main/regulatory-legal/skills/cold-start-interview/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:** sources заменены на РФ feeds (pravo.gov.ru, Банк России, ФНС, Минцифры, ФАС, и т.д.).

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## ⚠ Юридический disclaimer

Данный skill — **техническая платформа**, не оказывает юридических услуг по ст.2 ФЗ-63 «Об адвокатской деятельности». Outputs **не заменяют** консультацию лицензированного юриста / адвоката ФПА.

AI может галлюцинировать, выдавать устаревшие нормы, неверно интерпретировать факты. Material decisions — engage outside-адв ФПА с релевантной специализацией.
