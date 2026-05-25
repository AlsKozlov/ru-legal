---
name: transaction-monitoring
description: >
  Мониторинг операций клиентов на признаки подозрительности. РФ: обязательный
  контроль ≥ 1М (ст.6 115-ФЗ), подозрительные операции (Постановления Правительства
  + Положения ЦБ + Информсообщения Росфинмониторинга). Output: flag / clear /
  SAR draft.
argument-hint: "[customer + transaction details]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
---

# /transaction-monitoring

## Назначение

Анализ конкретной транзакции на признаки подозрительности или обязательного
контроля.

## Два типа triggers

### A. Обязательный контроль (ст.6 115-ФЗ)

Операции **≥ 1 млн руб** (с 2022; до 2022 был 600k):

- Снятие со счёта / зачисление наличных
- Покупка / продажа иностранной валюты в наличной форме
- Приобретение / погашение ценных бумаг за наличные
- Обмен банкнот разных номиналов
- Получение от иностранного юр.лица
- Внесение в УК наличными
- Иные — closed list в ст.6

Операции **≥ 5 млн руб** по сделкам с недвижимостью.

Операции с **лицами из списков терроризма** — независимо от суммы.

→ **All обязательные операции должны быть reported** в Росфинмониторинг в течение 3 рабочих дней (СПО — сообщение).

### B. Подозрительные операции (ст.7 115-ФЗ)

Subjective + objective criteria. Источники:
- Постановление Правительства РФ № 35 (общие критерии)
- Положение ЦБ № 375-П (для кредитных)
- Информсообщения Росфинмониторинга (regularly updated)

Common red flags:

#### Activity inconsistent с client profile

- Резкое увеличение объёмов
- Новые типы операций для клиента
- Несоответствие декларированной activity и реальной

#### Структурирование (smurfing)

- Множественные операции под порогом обязательного контроля (например, 6 операций по 900k каждая)
- Распределение крупного перевода между несколькими счетами
- Использование подставных лиц

#### Сложные нелогичные расчёты

- Цепочки между связанными лицами без экономического смысла
- Транзитные операции (получил → сразу transfer дальше)
- Round trip transactions

#### Cash-heavy operations

- Регулярные крупные cash deposits / withdrawals
- Особенно если business profile не requires cash

#### Geographical red flags

- Операции с offshore jurisdictions
- High-risk countries (по ФАТФ списку)
- Sanctioned jurisdictions

#### Structuring around sanctions

- Использование сложных схем для bypassing санкций
- Transactions через third-party countries
- Smurfing через множественные счета

#### Iдентификационные red flags

- Refusal to provide documents
- Inconsistent / changing information
- Mass-registered company (массовая регистрация по адресу / директором)
- Newly formed company с large transactions

## Workflow

### Шаг 1. Extract transaction details

```markdown
## Transaction analysis

- **Date:** [DD.MM.YYYY HH:MM]
- **Type:** [перевод / снятие / зачисление / иное]
- **Amount + currency:** [сумма + руб / USD / EUR / иное]
- **Sender:** [имя + ИНН + account]
- **Recipient:** [имя + ИНН + account]
- **Purpose:** [как указано в платёжке]
- **Sender country:** [...]
- **Recipient country:** [...]
- **Operation type per классификатор:** [ОКВ]
```

### Шаг 2. Apply ст.6 check (обязательный контроль)

```markdown
## ст.6 mandatory control check

- [ ] Amount ≥ 1 млн руб (cash, FX наличные, ценные бумаги, и т.д.)
- [ ] Real estate ≥ 5 млн руб
- [ ] Party from sanctions list

If YES to any → mandatory reporting к Росфинмониторингу в 3 раб.дня (СПО)
```

### Шаг 3. Red flags analysis

```markdown
## Suspicion indicators

| Indicator | Triggered? | Details |
|-----------|-----------|---------|
| Activity inconsistent с profile | [Y/N] | [описание] |
| Структурирование | [Y/N] | [история операций клиента last 30 дней] |
| Нелогичные расчёты | [Y/N] | [...] |
| Cash-heavy | [Y/N] | [...] |
| Geographical red flags | [Y/N] | [...] |
| Sanctions structuring | [Y/N] | [...] |
| ID red flags | [Y/N] | [...] |

**Score:** [N triggered]

**Suspicion level:** Low / Med / High
```

### Шаг 4. Decision

#### Если только обязательный контроль (без подозрительности)

→ Process transaction.
→ Report в СПО Росфинмониторингу в 3 раб.дня (standard category — ст.6).

#### Если подозрительный

→ STOP transaction если возможно (для banks — can block before completion).
→ Generate SAR (`/sar-submission`).
→ Report в Росфинмониторинг **в 1 рабочий день**.
→ Document decision rationale.
→ Continue monitoring клиента.
→ Consider client de-risking (terminate relationship).

#### Если ambiguous (low/med suspicion)

→ Enhanced monitoring:
- Дополнительные документы от клиента (KYC update, SoF)
- More frequent transaction review
- Escalation в compliance officer

#### Если clear

→ Document analysis (audit trail).
→ Process transaction.

### Шаг 5. Documentation

```markdown
## Transaction Monitoring Decision

- **Transaction ID:** [...]
- **Decision:** [Process normally / Process с reporting / Stop and SAR / Stop and de-risk]
- **Rationale:** [...]
- **SAR submitted:** [Y/N, дата]
- **Internal escalation:** [compliance officer / руководитель]
- **Documentation saved in:** [system / file]
- **Reviewer:** [user] @ [timestamp]
```

## Patterns specific для РФ post-2022

### Pattern 1: Sanctions evasion через third country

- Платежи через банк в Армении / Турции / Узбекистане для recipient в US/EU
- Documents indicate "trade" но без physical movement of goods
- → High suspicion + SAR

### Pattern 2: Cryptocurrency cash-out

- Переводы в обмен на cash от unknown ботом
- → High suspicion (особенно если client не declared crypto activity)

### Pattern 3: Структурирование платежей в недружественные страны

- Множественные платежи < $5,000 каждый = bypassing limit на personal transfers
- → Suspicious

### Pattern 4: "Параллельный" импорт без proper documentation

- Резкий рост платежей по "marketing services" к иностранным компаниям
- Реально — закрытые goods через third parties
- → Need additional documents; possibly suspicious

## Что НЕ делает

- Не blocks transactions автоматически — это banking system
- Не handles client de-risking communication — это relationship manager / compliance
- Не reports — это `/sar-submission`

**Правовая основа:**
- ФЗ-115 ст.6 (обязательный контроль)
- ФЗ-115 ст.7 (подозрительные операции)
- Постановление Правительства № 35 (критерии)
- Положение ЦБ № 375-П (для банков)
- Информсообщения Росфинмониторинга

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
