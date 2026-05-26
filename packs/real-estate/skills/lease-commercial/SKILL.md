---
name: lease-commercial
description: >
  Review договора commercial аренды (офис / склад / торговое помещение). РФ
  specifics: ст.609 ГК — обязательная регистрация в ЕГРН для срока > 1 года;
  ст.621 преимущественное право продления; ст.622 возврат; индексация по
  formula или CPI; security deposit (без формального института — workaround
  через предварительную оплату).
argument-hint: "[path к договору]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /lease-commercial

## Назначение

Review commercial lease перед подписанием с любой стороны (арендатор / арендодатель).

## Pre-flight

- **Side:** мы tenant or landlord?
- **Object:** офис / склад / торговое / mixed
- **Срок планируемый:** [...]
- **Цена ставки:** [руб/м²/мес]

## Workflow

### Шаг 1. Verify object + landlord rights

```markdown
## Объект verification

- [ ] Cadastre check (см. `/cadastre-check`)
- [ ] Адрес + площадь точно identified
- [ ] Назначение помещения соответствует нашему planned use
- [ ] Encumbrance check (см. `/encumbrance-analysis`)

## Landlord rights

- [ ] Право собственности (если арендодатель = собственник) — выписка ЕГРН
- [ ] ИЛИ право distribute (если арендодатель — sub-landlord) — выписка ЕГРН + договор основной аренды + согласие собственника на сдачу в субаренду
- [ ] Если ЮЛ — устав / полномочия подписанта
- [ ] Если физ.лицо в браке — согласие супруга (нотариально) для long-term lease > 1 года
```

### Шаг 2. Critical clauses

#### A. Срок

```markdown
- **Срок аренды:** [...]
- **Регистрация в ЕГРН (ст.609 ГК):** обязательна для срока > 1 года
  - Госпошлина: ~22,000 для ЮЛ
  - Не зарегистрирован → договор недействителен для третьих лиц
  - Common workaround — аренда на 11 мес с автоматическим продлением (loophole)

- [ ] Срок > 1 года? → план registration
- [ ] Срок < 1 года? → не требует регистрации
- [ ] Условия о продлении (преимущественное право — ст.621 ГК)
```

#### B. Арендная плата

```markdown
- **Ставка:** [руб/м²/мес]
- **Структура:**
  - Базовая ставка
  - НДС (если арендодатель плательщик НДС — обычно ЮЛ на ОСНО)
  - Коммунальные расходы — включены / отдельно
  - Эксплуатационные расходы — common area maintenance
  - Капитальный ремонт — кто несёт (typically landlord — ст.616 ГК)

- **Indexation:**
  - Annual % indexation, ИЛИ
  - CPI-based, ИЛИ
  - Fixed schedule повышения
  - Cap на indexation
  - First indexation date

⚠ **Watch:** ставка только в USD/EUR — для РФ residents должна быть в рублях (по ст.317 ГК — обязательство в иностранной валюте недопустимо для договоров на территории РФ кроме определённых случаев)
```

#### C. Security deposit

```markdown
**В РФ нет formального института security deposit** для аренды. Workarounds:

- **"Обеспечительный платёж"** — предусмотрен ст.381.1 ГК
  - Удерживается landlord
  - Возвращается при окончании если no breach
  - Может быть applied к last month rent
- **"Задаток"** — другой механизм (более restrictive)
- **"Предварительная оплата"** — простая форма

[ ] Структура secure deposit clear
[ ] Условия возврата
[ ] Right to withhold (для compensation damages)
```

#### D. Use restrictions

```markdown
- [ ] Назначение объекта — соответствует нашему use
- [ ] Subleasing — разрешено? (default по ГК — с согласия landlord)
- [ ] Sharing с affiliated — ОК или нет
- [ ] Изменения помещения (alterations) — какие нужны согласия
- [ ] Vывески / реклама — limit
- [ ] Hours of operation (для торгового / общепита)
```

#### E. Maintenance + repair

```markdown
ГК ст.616 default:
- Капитальный ремонт — за счёт landlord
- Текущий ремонт + содержание — за счёт tenant

Договор может modify:
- [ ] Какие types repair кто несёт
- [ ] Replacement инженерных систем (отопление, кондиционирование)
- [ ] Common areas в commercial centre
- [ ] Эксплуатационные расходы (CAM)
- [ ] Security
- [ ] Парковка
```

#### F. Termination

```markdown
### Right of tenant terminate

ГК ст.620 — only через суд за определённые основания (default).
**В договоре** часто predusmotrены additional grounds + право unилatorial:

- [ ] С уведомлением (typical 3-6 мес)
- [ ] Без причины (break fee)
- [ ] С причинами (без break fee — capital change, sale of object, и т.д.)

### Right of landlord terminate

ГК ст.619 — only через суд для определённых.
В договоре:

- [ ] При неуплате аренды > N мес
- [ ] При нарушении назначения
- [ ] При нарушении субаренды restrictions
- [ ] Иные основания

### Notice periods

[Critical — too short / too long?]

### Consequences termination

- Return объекта в указанном состоянии
- Final settlement
- Recovery security deposit
```

#### G. Insurance + liability

```markdown
- [ ] Insurance объекта — landlord?
- [ ] Insurance contents tenant — tenant
- [ ] Liability insurance tenant — landlord может require
- [ ] Mutual indemnification (interest events vs negligence)
```

#### H. Force majeure

```markdown
- [ ] Common force majeure clause (war, natural disasters, government acts)
- [ ] Post-2022 — sanctions force majeure (vary by language — explicit better)
- [ ] Pandemic provisions (после COVID experience)
- [ ] Notification requirements
```

### Шаг 3. РФ-specific traps

#### Trap 1: Lease на физ.лицо vs ЮЛ landlord

- Физ.лицо landlord — должен платить НДФЛ 13% (или 15%) с rent income
- Часто landlord wants tenant withhold and remit — может быть в договоре
- Tenant юр.лицо как налоговый агент по соглашению — but verifications

#### Trap 2: Sub-tenant chains

- Длинные chains аренды → multiplied risk при failure прямого landlord
- Verify entire chain rights

#### Trap 3: Государственное / муниципальное имущество

- Особенности (ФЗ-135 ст.17, торги, ограничения)
- Часто только через ст.17.1 ФЗ-135 — torgах

#### Trap 4: Land lease for built object

- Building на земле + лeасе только land — separate scheme
- При продаже постройки — что с землёй?
- ст.272 ГК + ст.39.20 ЗК

#### Trap 5: Изменение целевого назначения

- Если использовать not as documented — risk requirements re-certification + затраты

### Шаг 4. Output

```markdown
# Commercial Lease Review — [объект]

## Bottom line

[Sign / Sign with changes / Don't sign]

## Critical issues

[Per category выше]

## Negotiation points

1. [Most important]
2. ...

## Cost / risk summary

- Annual rent + escalation projection
- Termination costs (break fee если applicable)
- Hidden costs (capital improvements expected, taxes если на нас)
- Risk concentration (long-term commit?)

## Outside-адв engagement

[Yes для material commercial deals]
```

## Что НЕ делает

- Не negotiates (это business + outside-адв)
- Не handles регистрацию в ЕГРН (это нотариус / Росреестр)
- Не делает full DD объекта (это `/cadastre-check` + `/encumbrance-analysis`)

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
