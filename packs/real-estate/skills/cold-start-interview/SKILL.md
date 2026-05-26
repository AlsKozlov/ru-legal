---
name: cold-start-interview
description: >
  First-run для real-estate pack. Заполняет PROFILE.md: тип сделок, текущий
  портфель, outside-адв, material thresholds.
argument-hint: "[optional: section]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview (real-estate)

## Workflow

### Шаг 1. Тип сделок

- Жилая / commercial / земля / промышленная / ДДУ

### Шаг 2. Текущий портфель

- В собственности
- В аренде (мы арендатор)
- Сданы в аренду

### Шаг 3. Outside counsel

- Outside-адв ФПА
- Кадастровый инженер
- Нотариус
- Риелтор

### Шаг 4. Material thresholds + risk posture

### Шаг 5. Save + confirm

```
✓ PROFILE.md сохранён.

Загружены skills:
- /ddu-review (killer — 214-ФЗ)
- /lease-commercial
- /lease-residential
- /cadastre-check (Росреестр / ЕГРН)
- /encumbrance-analysis
- /purchase-sale-review
- /construction-contract-review
- /customize
```

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
