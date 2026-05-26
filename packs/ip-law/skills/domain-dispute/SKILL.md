---
name: domain-dispute
description: >
  RU-unique. Споры по доменным именам в зонах .RU / .РФ / .SU. Через Координационный
  центр доменов (КЦ) — мирное урегулирование; АДРД (Альтернативное разрешение
  доменных споров) — арбитраж по правилам КЦ; СИП — судебный путь. Critical
  для cybersquatting + typosquatting + brand protection.
argument-hint: "[доменное имя + наш ТЗ]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /domain-dispute

## Назначение

Resolve спор по доменному имени, нарушающему наши IP rights (типично ТЗ). Pathways:
- Direct contact с registrant + cease & desist
- Через регистратора домена (формальная процедура — для очевидных нарушений)
- АДРД (Альтернативное разрешение доменных споров) через КЦ
- Судебный путь в СИП

## Pre-flight

- **Наш IP:** ТЗ зарегистрирован? Дата приоритета? Классы МКТУ?
- **Spornoye доменное имя:** [domain.ru / .рф / .su]
- **Кто registrant:** [физ.лицо / ЮЛ — данные через WHOIS]
- **Содержание сайта:** [активно работает? пустой? редирект на конкурента?]
- **Materiality:** [конкретный business loss? reputational?]

## Available paths

### A. Direct outreach + C&D

- Email / phone к registrant
- Формальная претензия (см. `/cease-desist`)
- Cheapest path
- Limited если registrant ignores / unknown

### B. Через регистратора (formal procedure)

Каждый registrar (REG.RU, NIC.RU, etc.) имеет formal anti-cybersquatting procedure:
- Submit claim с доказательствами IP rights
- Registrar requests response от registrant
- Если no response / не убедителен — registrar может suspend / transfer domain
- Но реgistrar usually не "judges" disputes полностью — only clearcut cases

### C. АДРД (Альтернативное разрешение доменных споров)

**Создано КЦ доменов в 2014** по образцу WIPO UDRP.

**Применяется:** для зон **.RU / .РФ**.

**Process:**
1. Подача жалобы в Координационный центр (cctld.ru)
2. КЦ передаёт в коммиссию арбитров
3. Арбитры рассматривают (3 эксперта обычно)
4. Решение в 60 дней
5. Если в нашу пользу — domain transfered к нам (или cancelled)

**Cost:** ~50-100k руб + опционально outside-консультант

**Стандарт доказывания (по правилам АДРД, similar к UDRP):**

Claimant должен доказать **all three:**
1. **Сходство до степени смешения** между domain и нашим ТЗ (или фирменным наименованием)
2. **Отсутствие у registrant прав / законных интересов** на это domain
3. **Регистрация и использование в bad faith** (e.g., для cybersquatting / typosquatting / unfair competition / disruption of competitor)

### D. Судебный путь — СИП

**Применяется:** Сложные случаи (когда АДРД cannot decide, или иные основания
помимо чистого IP — например, "защита деловой репутации").

**Process:**
- Иск в СИП (или АС субъекта в зависимости от характера)
- Требования: пресечение использования + аннулирование регистрации domain + компенсация
- Срок 3-9 мес

**Cross-reference:** `litigation/matter-intake` + `/infringement-triage`.

## Workflow

### Шаг 1. Identify domain + facts

```markdown
## Domain dispute analysis

### Spornoye domain

- **Domain name:** [domain.ru / .рф]
- **Дата регистрации:** [DD.MM.YYYY] (важно сравнить с датой приоритета нашего ТЗ)
- **Registrant** (по WHOIS):
  - Имя / название: [...]
  - Контакты: [...]
  - Страна: [...]
- **Реgistrar (where registered):** [REG.RU / NIC.RU / иной]
- **Сайт:** [active / inactive / redirect to competitor / placeholder]
- **Содержание (если active):** [...]

### Наш ТЗ / brand

- **ТЗ:** № регистрации, дата приоритета
- **Классы МКТУ:** [...]
- **Domain:** какой degree сходства с ТЗ
- **Длительность использования brand:** [...]

### Bad faith indicators

- [ ] Domain registered after our ТЗ priority date
- [ ] Registrant имеет no legitimate connection к этому слову
- [ ] Domain redirects на конкурента
- [ ] Domain offered нам for purchase by registrant
- [ ] Registrant has portfolio similar domains (typosquatting pattern)
- [ ] Прямая отсылка / mention нашего brand на сайте
- [ ] Misleading content suggesting affiliation с нами
```

### Шаг 2. Path selection

```markdown
## Path matrix

| Path | Probability success | Time | Cost | Когда применять |
|------|---------------------|------|------|-----------------|
| A. Direct C&D | Med | 1-2 мес | ~10k | First step — always try |
| B. Через регистратора | Low-Med | 2-4 мес | minimal | Если C&D ignored |
| C. АДРД | High (если 3 elements met) | 2-3 мес | 50-100k | Most cybersquatting cases |
| D. СИП | High (если ТЗ strong) | 6-12 мес | 200k+ | Complex cases or АДРД failed |

## Recommendation

[Path + reason]

## Parallel paths

Часто рекомендую — A first, потом если no success — C (АДРД) is best balance time/cost.
```

### Шаг 3. АДРД жалоба draft (если этот путь)

```markdown
# В Координационный центр доменов .RU/.РФ
# Арбитражная коллегия по доменным спорам

# ЖАЛОБА
# по доменному спору
# domain.ru vs нашего ТЗ N

## Стороны

- **Истец (Claimant):** [Полное наименование правообладателя]
- **Ответчик (Respondent):** [Имя registrant per WHOIS]

## Spornoye doman

[domain.ru] — registered [DD.MM.YYYY]

## Наш ТЗ / brand

- ТЗ № [NNNNNN], зарегистрирован [DD.MM.YYYY]
- Дата приоритета: [DD.MM.YYYY]
- Знак: [текст / image]
- Классы МКТУ: [...]
- Использование с [DD.MM.YYYY] в business activities компании

## По существу — 3 elements

### Element 1: Сходство до степени смешения

Spornoye domain [domain.ru] **сходно до степени смешения** с нашим ТЗ:

- **Visual similarity:** [analysis — comparing letters / графика]
- **Phonetic similarity:** [...]
- **Semantic similarity:** [...]

Аналогичные cases в practice АДРД / СИП:
- [пример 1]

### Element 2: Отсутствие у Respondent прав / законных интересов

Респондент **не имеет legitimate interests** в данном domain по следующим причинам:

1. Respondent **не имеет** регистрации ТЗ / фирменного наименования / коммерческого обозначения с этим словом
2. Respondent **не известен** под этим именем в business
3. Сайт на domain **не используется** в bona fide business
4. Иные обстоятельства

### Element 3: Регистрация и использование в bad faith

Респондент **зарегистрировал и использует** domain в bad faith:

- **Дата регистрации domain:** [DD.MM.YYYY] — **после** даты приоритета нашего ТЗ
- **Использование:**
  - Redirect на сайт конкурента, ИЛИ
  - Размещение misleading content suggesting affiliation с нами, ИЛИ
  - Offered нам for purchase, ИЛИ
  - Иные bad faith elements

- **Pattern активности:** Respondent имеет portfolio similar domains [list if applicable]

- **Прямая отсылка к нашему brand:** [evidence]

## Просим

Принять решение о:

1. **Передаче доменного имени [domain.ru] от Respondent к Claimant**

ИЛИ (alternative):

2. **Аннулировании регистрации** доменного имени [domain.ru]

## Приложения

1. Свидетельство Роспатент на ТЗ № N — [N] листов
2. Скриншоты сайта по [domain.ru] от [DD.MM.YYYY] — [N] листов
3. Документы о деловой репутации / использовании ТЗ — [N] листов
4. Корреспонденция между сторонами (попытки досудебного урегулирования) — [N] листов
5. WHOIS data на [domain.ru] — [N] листов
6. Иные доказательства bad faith — [N] листов

[Подпись]
[Дата]
```

### Шаг 4. Tracking + outcome

```markdown
## Tracking

### АДРД timeline

- Жалоба подана: [DD.MM.YYYY]
- Уведомление Respondent: [DD.MM.YYYY]
- Ответ Respondent: [DD.MM.YYYY] (10 days typically)
- Решение арбитров: [DD.MM.YYYY] (60 days deadline)
- Implementation if win: 10 days for transfer

### If win

- Domain transferred к нам — proceed to use
- Document outcome

### If lose

- Decision binding под АДРД, но не excludes судебный путь
- СИП может consider de novo
- Engage outside-адв для appeal / suit
```

## Common pitfalls

### 🔴 Critical

- **Слабый ТЗ** (descriptive / weak distinctive character) — может lose первый element
- **Domain зарегистрирован до нашего ТЗ** — strong defense для Respondent
- **Legitimate use** Respondent (например, его имя / фирма содержит слово) — не bad faith
- **Не собранные доказательства** — АДРД strict on evidence

### 🟡 Medium

- High legal cost для marginal cases
- АДРД vs суд — каждый имеет lacking — суд может give больше remedies но longer
- Cross-border respondents — limited enforceability

## Что НЕ делает

- Не подаёт через АДРД automatically (нужны actions + ответы на questions)
- Не handles registrar abuse reports (delegate)
- Не handles trademark watch (separate service)

**Правовая основа:**
- Правила регистрации доменных имён в .RU / .РФ (КЦ)
- Правила АДРД (КЦ доменов, 2014 + регулярные обновления)
- ГК часть 4 (ТЗ ст.1477+, фирменное наименование ст.1473+, коммерческое обозначение ст.1538+)
- ст.1252 ГК — пресечение нарушения для domain case
- АПК / ГПК — для судебного пути

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
