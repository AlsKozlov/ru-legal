---
name: cold-start-interview
description: >
  First-run для administrative-law pack. Заполняет PROFILE.md: тип организации,
  ОКВЭДы (определяют regulators), open проверки / предписания / штрафы,
  outside-адв.
argument-hint: "[optional: section]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview (administrative-law)

## Workflow

### Шаг 1. Тип организации + ОКВЭДы

### Шаг 2. Regulator landscape (зависит от ОКВЭД)

См. PROFILE.md template — list common regulators в РФ.

### Шаг 3. Open admin matters

### Шаг 4. Outside counsel + risk posture

### Шаг 5. Save + confirm

```
✓ PROFILE.md сохранён.

Загружены skills:
- /koap-violation-response (killer skill — ответ на протокол)
- /inspection-preparation (готовность к проверке)
- /inspection-defense (защита при проверке)
- /administrative-appeal (обжалование 10 дней)
- /statute-of-limitations-check (ст.4.5 КоАП — может отменить)
- /fines-calculator
- /customize
```

## Why RU-unique

Anthropic не имеет административно-правового pack-а. US административное право — federal agencies + state agencies + APA — different structure. РФ — единый КоАП + 248-ФЗ + sectoral regulators.

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
