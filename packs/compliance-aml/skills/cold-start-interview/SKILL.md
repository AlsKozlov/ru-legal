---
name: cold-start-interview
description: >
  First-run для compliance-aml pack. Заполняет PROFILE.md: тип организации
  (определяет scope 115-ФЗ), регулятор (Банк России / Росфинмониторинг), KYC
  и sanctions screening инфраструктура, sanctions exposure.
argument-hint: "[optional: section]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview (compliance-aml)

## Workflow

### Шаг 1. Тип организации (определяет scope)

См. список в PROFILE.md template. Critical для:
- **Банки / кредитные**: full 115-ФЗ scope + ЦБ regulation
- **МФО / страховые / лизинговые**: significant scope
- **Юр.фирмы / нотариусы / риелторы**: limited scope (только определённые операции)
- **Иные**: частично

### Шаг 2. Регулятор

- **Банк России** для credit institutions
- **Росфинмониторинг** (СФМ) для остальных

### Шаг 3. Sectoral details

- ОКВЭДы
- Размер
- Клиентская база (резиденты / нерезиденты / дружественные / недружественные)

### Шаг 4. Sanctions exposure

- Cross-border сделки
- Иностранная валюта
- Корреспондентские отношения
- Sanctioned client (если есть — action plan)

### Шаг 5. Compliance infrastructure

- ПВК (внутренние правила) утверждены
- Compliance officer
- KYC система
- Sanctions screening
- Transaction monitoring
- Обучение

### Шаг 6. Open matters + outside consultants

### Шаг 7. Risk posture (recommend conservative / средний; aggressive NOT recommended для AML)

### Шаг 8. Save + confirm

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
