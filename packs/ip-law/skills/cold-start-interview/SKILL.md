---
name: cold-start-interview
description: >
  First-run setup для ip-law pack. Заполняет PROFILE.md: тип бизнеса, портфель
  IP (ТЗ / патенты / ПО / БД), география защиты, outside counsel (включая
  патентного поверенного — обязательного для подачи заявок).
argument-hint: "[optional: section]"
user_invocable: true
ported_from: ip-legal/cold-start-interview
ported_at: 2026-05-19
adaptation_category: B
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview (ip-law)

## Workflow

### Шаг 1. Тип бизнеса + IP focus

- Сектор (tech / fashion / FMCG / media / pharma / иное)
- Какие виды IP критичны (ТЗ / патенты / авторские / ноу-хау / ПО)

### Шаг 2. Текущий портфель

- ТЗ — список + классы МКТУ + регионы регистрации
- Патенты — изобретения / полезные модели / промобразцы
- ПО / БД — зарегистрированы в Роспатент? IT-аккредитация в Минцифры?
- Ноу-хау — установлен ли режим КТ по 98-ФЗ?

### Шаг 3. География защиты

- РФ — basis
- EAEU единый ТЗ (с 2021) — Армения / Беларусь / Казахстан / Киргизия / РФ
- Мадридская система — список стран
- PCT — национальные фазы

### Шаг 4. Outside counsel

**Critical:** для подачи заявок в Роспатент **рекомендован** патентный поверенный
(обязателен только для иностранных заявителей — ст.1247 ГК). Регистрационный
номер в реестре патентных поверенных Роспатент.

### Шаг 5. Open matters + material thresholds

### Шаг 6. Risk posture

### Шаг 7. Save + confirm

```
✓ PROFILE.md сохранён.

Загружены skills:
- /clearance (ТЗ + патенты pre-launch search)
- /fto-triage (Freedom to Operate)
- /infringement-triage (analysis нарушения)
- /cease-desist (досудебная претензия по IP)
- /ip-clause-review (review IP clauses в договорах)
- /invention-intake (intake изобретений + ст.1295 служ.произведение)
- /oss-review (OSS license compliance)
- /portfolio (управление портфелем)
- /takedown (ФЗ-149 ст.15.7 + антипиратский)
- /rospatent-application (RU-unique — заявка в Роспатент / ФИПС)
- /domain-dispute (RU-unique — споры по доменам)
- /customize
```

## Attribution

Adapted from [`ip-legal/cold-start-interview`](https://github.com/anthropics/claude-for-legal/blob/main/ip-legal/skills/cold-start-interview/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:** US USPTO / USPATENT framework → РФ Роспатент / ФИПС; включён EAEU TM; патентный поверенный (РФ-specific institution); ст.1247 ГК.

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
