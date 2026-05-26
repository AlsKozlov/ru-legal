---
name: inspection-preparation
description: >
  Pre-inspection readiness — подготовка к плановой / внеплановой проверке любого
  регулятора по 248-ФЗ. Internal audit с typical findings, документация в
  порядок, сотрудники проинструктированы, outside-адв на готов.
argument-hint: "[regulator + дата проверки]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /inspection-preparation

## Назначение

Compliance readiness check + remediation plan перед проверкой регулятора.

## Pre-flight

- **Regulator** identified (ФНС / РКН / ФАС / Росздравнадзор / etc.)
- **Тип проверки:** плановая / внеплановая / документарная / выездная
- **Дата начала** известна (для плановой — в Плане проверок до 31 декабря)
- **Предмет проверки** definitively known (предмет → focus areas)

## Workflow

### Шаг 1. Identify scope of inspection

```markdown
## Inspection details

- **Регулятор:** [...]
- **Тип:** [плановая / внеплановая / документарная / выездная / профилактическая]
- **Решение о проверке № [N] от [DD.MM.YYYY]:** [reference]
- **Период проверки (что проверяется):** [from-to]
- **Предмет проверки:** [конкретно — например, 152-ФЗ compliance]
- **Срок проверки:** [N дней]
- **Состав проверяющих:** [list — verify через реестр регулятора]
- **Мораторий applicable?** (ПП РФ 336/2022 для МСП до 2026): [Y/N]
```

### Шаг 2. Identify likely focus areas

Каждый регулятор имеет typical checklist (publicly available в большинстве):

#### ФНС (если применимо — но обычно отдельный workflow tax-law/tax-audit-response)

- Налоговая отчётность compliance
- Контролируемые сделки
- Бенефициары

#### РКН

- Уведомление операторе ПДн актуально
- Политика обработки ПДн доступна на сайте
- ПВД (документы по обработке ПДн)
- ОВПД done для high-risk processing
- Локализация (152-ФЗ ст.18 ч.5)
- Cross-border transfer notification

#### ФАС

- Антимонопольные документы (если applicable)
- Сделки с признаками концентрации > порогов
- Реклама compliance (38-ФЗ)
- Гос.закупки (44/223) если participant

#### Росздравнадзор (мед/фарма)

- Лицензии актуальные
- Журналы учёта лекарственных средств
- Контроль качества

#### Роспотребнадзор

- СанПин compliance
- ПДн потребителей
- Documentation предприятия общепита / торговли

#### Ростехнадзор

- Лицензии на опасные производства
- Журналы ТБ
- Авариности
- Регистрация опасных производственных объектов

#### Росприроднадзор

- Экологические разрешения
- Платежи за негативное воздействие
- Учёт выбросов / отходов

#### МЧС (пожарная)

- Пожарная декларация / противопожарные мероприятия
- Журналы тренингов
- Сертификация оборудования

#### ГИТ (Роструд) — отдельно см. labor-law/trudovaya-inspeksiya-response

### Шаг 3. Internal audit (per scope)

```markdown
## Self-audit checklist

### Critical (если не в порядке → высокий risk нарушения)

- [ ] [Conkretно specific требование по типу регулятора]
- [ ] [Another требование]
- ...

### Important

- [ ] [...]

### Best practice

- [ ] [...]
```

### Шаг 4. Documentation review

```markdown
## Document readiness

### Internal documents

- [ ] ЛНПА регулирующие activity — актуальная редакция
- [ ] Журналы / акты внутреннего контроля — заполнены
- [ ] Сертификации / лицензии — действующие, копии готовы
- [ ] Reporting prior periodов — archived + accessible

### Communications

- [ ] Письма к / от регулятора — chronologically archived
- [ ] Запросы разъяснений + ответы регулятора
- [ ] Previous predписания (если были) — статус исполнения

### Internal training records

- [ ] Журналы обучения сотрудников
- [ ] Подписные листы ознакомления с ЛНПА
- [ ] Сертификаты профессионального обучения

### Statistical / operational

- [ ] Отчётность за период проверки
- [ ] Учётные регистры
- [ ] Договоры с контрагентами относящиеся к scope
```

### Шаг 5. Team briefing

```markdown
## Personnel preparation

### Key personnel ответственные за scope

- ФИО, должность — primary point of contact
- ФИО, должность — backup

### Briefing topics

- [ ] Объяснить scope проверки
- [ ] Подчеркнуть rights and obligations при проверке (см. `/inspection-defense`)
- [ ] Правила взаимодействия с проверяющими:
  - Не давать показаний без compliance officer / outside-адв
  - Не подписывать акты без review
  - Документировать все запросы
- [ ] Кому эскалировать questions
- [ ] Outside-адв ФПА contacts ready

### Mock interview / drilling (для high-stakes)

- Practice common questions
- Practice document delivery
- Practice "I'll get back to you" вместо ad-hoc answers
```

### Шаг 6. Outside-адв ФПА engagement

```markdown
## Outside counsel readiness

- **Engaged before проверка start?** [Y/N — recommended для material матерей]
- **Specific adv для этого типа проверки:** [name, contact]
- **Privilege framing:** documents prepared под адвокатской тайной (если applicable)
- **Communication channel:** routing through outside-адв for material communications
```

### Шаг 7. Remediation выявленных issues

Если self-audit выявил issues:

```markdown
## Pre-inspection remediation

### Critical issues (fix before inspection)

| Issue | Fix | Owner | Deadline | Status |
|-------|-----|-------|----------|--------|
| [...] | [...] | [...] | [DD.MM.YYYY] | [...] |

### Documentable issues (cannot fix entirely, but document)

[List + documentation strategy]

### Mitigation если cannot fully fix

- Voluntary disclosure (sometimes reduces fine)
- Ongoing remediation plan with evidence
- Engage outside-адв for advice о disclosure
```

### Шаг 8. Day-of-inspection preparation

```markdown
## Day-of-inspection

- [ ] Reception ready — verify identity проверяющих (удостоверения + решение)
- [ ] Conference room reserved для проверяющих
- [ ] Designated escort / liaison person ready
- [ ] Document delivery process clear
- [ ] Compliance officer + outside-адв on-call
- [ ] All employees briefed
- [ ] Acts / документы для possible signing — review process clear
```

## Output

```markdown
# Inspection Preparation — [regulator + дата]

## Self-audit findings

[Summary]

## Critical issues to fix pre-inspection

[List with deadlines]

## Documentation readiness

[Status]

## Personnel readiness

[Status]

## Outside-адв engagement

[Status]

## Day-of plan

[Status]

## Expected scope + likely findings

[Realistic assessment]

## Recommended actions next 7 days

[Concrete]
```

## Что НЕ делает

- Не handles непосредственно interaction с проверяющими (это `/inspection-defense`)
- Не fixes substantive compliance issues (это business units)
- Не replaces full outside-адв engagement для material матерей

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
