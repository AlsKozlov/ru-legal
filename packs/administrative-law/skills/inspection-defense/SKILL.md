---
name: inspection-defense
description: >
  Защита компании при проведении проверки регулятором. Права + обязанности
  стороны проверяемой (248-ФЗ ст.36-37). Tactical handling: проверка идентичности
  проверяющих, требование подтверждения оснований, document delivery, fixation
  proverочных actions, отказ от давления / неправомерных запросов.
argument-hint: "[regulator + текущий statусs]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /inspection-defense

## Назначение

Real-time guidance во время проверки. Не replaces `/inspection-preparation`
(которое до) — это во время.

## Pre-flight

- `/inspection-preparation` done
- Outside-адв ФПА engaged / on-call
- Designated liaison ready
- Team briefed

## Rights проверяемого (248-ФЗ + sectoral)

### Право 1: Verify проверяющих

- Удостоверения проверяющих
- Решение о проведении проверки (с реквизитами)
- Соответствие списка проверяющих в решении и pry проверке
- Соответствие предмета проверки с решением
- Срок проверки — не превышен?

**Если что-то не сходится** → fix письменно + at the very basic — `/inspection-defense` requires:
- Refuse доступ к объекту (если cannot verify legitimacy) — но с care чтобы не быть obstructive
- Contact outside-адв + supervising orgان immediately
- Видео / аудио fixation of проверочных actions (с согласия — but if illegitimate, нужно document)

### Право 2: Присутствие представителя

- Право иметь at minimum один представитель компании присутствующим при всех проверочных actions
- Право иметь outside-адв ФПА

### Право 3: Ознакомление с материалами

- Право ознакомиться с актами / документами составляемыми в ходе проверки
- Право получить copies всего проверочного производства

### Право 4: Возражения

- Право заявлять возражения в любой момент (за protocol)
- Право подавать ходатайства о дополнительных проверочных actions
- Право заявлять отводы проверяющим

### Право 5: Конфиденциальность

- Право требовать confidentиальности коммерческой тайны (98-ФЗ режим КТ)
- Право не разглашать ПДн третьих лиц без legal basis
- Banking тайна (395-1 ст.26), врачебная тайна, etc. — preserved

### Право 6: Не свидетельствовать против себя

- Конституционное право (ст.51) — нет obligation давать показания свидетельствующие против себя / близких
- Hide вокруг proper questioning techniques

## Workflow

### Шаг 1. Initial encounter

```markdown
## Прибытие проверяющих

### Verification steps

- [ ] Удостоверения предъявлены
- [ ] Решение о проверке № [N] от [DD.MM.YYYY] — копия получена
- [ ] Состав соответствует решению
- [ ] Предмет соответствует решению
- [ ] Срок проверки в пределах решения
- [ ] (Если мораторий applicable для МСП) — проверка legitimate под мораторий?

### Recording

- [ ] Журнал проверок Открыт (ведём свой)
- [ ] Запись начата (с согласия / документально)
- [ ] Свидетели наши присутствуют
```

### Шаг 2. Document delivery management

**Critical:** не давать больше чем запрошено.

```markdown
## Document delivery protocol

### Сначала request specifically what they want

- "Какие конкретно documents?"
- "За какой период?"
- "В каком форме?"

### Готовить documents copies

- Originals — show + return (не передавать без необходимости)
- Copies — provided
- Inventory list with пере numбер listы / pages

### Confidentiality flags

Для каждого документа containing:
- Коммерческая тайна (КТ под 98-ФЗ) — explicit label
- ПДн третьих лиц — minimize / redact
- Адвокатская тайна (ФЗ-63 — если outside-адв involved) — PRIVILEGED не disclose

### Out-of-scope requests

Если просят что-то outside заявленного предмета проверки:
- Politely decline
- Письменно зафиксировать "Запрос выходит за рамки предмета проверки от [DD]"
- Не provide
- Note для возражений по акту
```

### Шаг 3. Interview / opros management

**Critical:** не давать показания без compliance officer / outside-адв.

```markdown
## Interview protocols

### Перед началом

- [ ] Identify proverявший (ФИО + должность)
- [ ] Identify subject — кому будут задавать
- [ ] Confirm присутствие compliance officer / outside-адв
- [ ] Confirm subject understands his rights

### Во время

- Subject имеет право:
  - Молчать (ст.51 Конституции)
  - Отвечать только в письменной форме
  - Получить copy показаний
  - Внести замечания в протокол

- Subject **должен avoiд**:
  - Speculation
  - Admissions без подумать
  - Volunteer additional information

- Recommended approach:
  - "Я подумаю и предоставлю ответ в письменной форме"
  - Document everything что say

### Если давление / угрозы

- Stop interview
- Document conditions
- Engage outside-адв немедленно
- File complaint к supervising органу + прокуратуре
```

### Шаг 4. Daily fixation

```markdown
## Daily inspection log

- **Date:** [DD.MM.YYYY]
- **Actions taken by проверяющими:**
  - [...]
  - [...]
- **Documents delivered:**
  - [...]
- **Interviews conducted:**
  - [subject, time, topics]
- **Issues / concerns:**
  - [...]
- **Photos / records taken by проверяющими:**
  - [list]
```

### Шаг 5. Specific situations

#### Изъятие документов / выемка

- Допустимо только при особых procedures (УПК если уголовное; КоАП с judicial санкцией для определённых cases)
- Без proper санкции — illegal
- Document всё (видео если возможно)
- Engage outside-адв immediately
- Inventory of изъятого — sign only after careful review

#### Осмотр помещений

- Должен быть в присутствии представителя
- Только в рамках scope проверки
- Photo / measurements — document parallel со своей стороны

#### Контрольная закупка / эксперимент

- Проверяющие могут проводить контрольную закупку (in some categories)
- Должна быть documented

### Шаг 6. Завершение проверки — акт

```markdown
## Акт проверки

### Critical — review before signing

- [ ] Read entire акт
- [ ] Check соответствие с фактическими обстоятельствами
- [ ] Identify нарушения отмеченные — agree / disagree
- [ ] Identify конкретные нормы упомянутые

### Signing options

#### Option A: Подписать без возражений

- Принимаем все findings
- Risk: closed acceptance — limits ability to obжаловать later

#### Option B: Подписать с возражениями

- Сделать отметку "С актом ознакомлен. Возражения будут представлены в установленный срок (15 раб.дней по 248-ФЗ ст.39)"
- Standard approach — preserves rights

#### Option C: Отказ от подписания

- Составляется акт об отказе
- Не лишает права обжалования
- Лучше Option B обычно

### After signing

- Get copy акта
- Inventory of all attached documents
- Schedule prep возражений
```

### Шаг 7. Post-inspection actions

```markdown
## Post-inspection workflow

### Within 7 days

- [ ] Internal debrief — what went well / poorly
- [ ] Document acts / документы collected
- [ ] Initial assessment likely findings

### Within 15 days

- [ ] Возражения на акт submitted (см. также `/koap-violation-response`)
- [ ] Outside-адв ФПА engaged

### Within 30 days

- [ ] Track выдача предписания (если будут)
- [ ] Track решение о возбуждении дела об адм.правонарушении

### Если выдано предписание

- Срок исполнения соблюдать (если согласны)
- ИЛИ обжаловать (см. `/administrative-appeal`)

### Если возбуждено дело об админ.правонарушении

- → `/koap-violation-response`
```

## Common pitfalls

### 🔴 Critical

- **Signing акт без review** → closed acceptance + limits для обжалования
- **Volunteering информации** outside scope → expands scope проверки
- **Confessional statements** under pressure → admissible evidence
- **No document trail** — невозможно argue later что нарушений не было
- **Не engaging outside-адв** для material матерей

### 🟡 Medium

- Failing to fix процессуальные нарушения (запись, dates, etc.)
- Disorganized document delivery — выглядим как hiding
- Inconsistent answers between team members

### 🟢 Best practices

- Calm, professional демeanor
- Document everything
- "I'll get back to you" preferred над speculation
- Outside-адв on-call

## Что НЕ делает

- Не handles substantive compliance fixes
- Не negotiates с проверяющими (это outside-адв в material cases)
- Не replaces formal legal advice для high-stakes situations

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
