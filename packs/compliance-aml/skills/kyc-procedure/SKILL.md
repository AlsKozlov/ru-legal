---
name: kyc-procedure
description: >
  KYC (Know Your Customer) procedure по 115-ФЗ. Identification клиента +
  CDD (customer due diligence) + EDD для high-risk + ongoing monitoring.
argument-hint: "[customer onboarding context]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
---

# /kyc-procedure

## Назначение

End-to-end KYC procedure от onboarding до ongoing monitoring клиента.

## KYC stages

### Stage 1: Pre-onboarding screening

- Identity verification
- Sanctions screening (`/sanctions-screening`)
- PEP screening (`/pep-screening`)
- РНП check (если applicable — `public-procurement/rnp-check`)
- Adverse media search
- DNB / commercial DD (если ЮЛ)

### Stage 2: Identification

#### Для физ.лиц

Required (115-ФЗ ст.7):
- ФИО + дата рождения
- Гражданство
- Реквизиты документа удостоверяющего личность
- Адрес регистрации (фактического проживания)
- ИНН (если есть)
- СНИЛС
- Контактная информация

Documents:
- Паспорт (РФ или иностранный + миграционная карта / РВП / ВНЖ)
- ИНН свидетельство
- Иные

#### Для юр.лиц

Required:
- Наименование + ИНН + ОГРН
- Адрес
- Учредительные документы
- Сведения о руководителе
- Бенефициарные владельцы (`/beneficial-owner-check`)
- Структура collective management (если applicable)
- Цели деятельности

Documents:
- Устав
- ЕГРЮЛ выписка (актуальная)
- Свидетельство о госрегистрации
- Решение о назначении руководителя
- Лицензии (если деятельность лицензируется)
- Финансовая отчётность (для CDD)

### Stage 3: Customer Due Diligence (CDD)

#### Risk categorization

| Категория | Indicators | CDD scope |
|-----------|-----------|-----------|
| **Низкий** | Резидент РФ, прозрачный business, малые суммы, retail | Simplified CDD |
| **Средний** | Default | Standard CDD |
| **Повышенный** | См. high-risk indicators ниже | Enhanced DD (EDD) |

#### High-risk indicators

- PEP клиент (Foreign / Domestic / International organization)
- Юр.лицо из недружественной страны (post-2022)
- Сложная корпоративная структура (cascading > 3 уровней)
- High net worth individual (HNWI)
- Cash-intensive business
- Cross-border activity dominant
- Высокая текучесть beneficial owners
- Adverse media
- Predecessor / similar company в РНП / реестрах нарушителей
- Регулярные крупные транзакции с offshore центрами
- Структура с trust / nominees / номинальными директорами

### Stage 4: Enhanced Due Diligence (EDD)

Для high-risk клиентов:

- Additional documentation:
  - Источник благосостояния (Source of Wealth — SoW)
  - Источник средств для конкретных транзакций (Source of Funds — SoF)
  - Tax compliance proof (для cross-border)
- Visits / face-to-face meetings (для HNWI)
- Senior management approval onboarding
- Enhanced monitoring (более частые reviews)
- Reporting к compliance officer + руководству

### Stage 5: Ongoing monitoring

- Transaction monitoring (`/transaction-monitoring`)
- Periodic review (annually for high-risk; biannually for medium; per-event for low)
- Triggers re-assessment:
  - Изменение activity pattern (necesarными типичные)
  - Новые beneficial owners
  - Жалобы / inquiries регулятора
  - Adverse media
  - Sanctions list updates
  - Изменение risk category клиента

## Workflow

### Шаг 1. Onboarding kickoff

```markdown
## Customer onboarding: [имя]

- **Date:** [DD.MM.YYYY]
- **Onboarding officer:** [user]
- **Risk category preliminary:** [Low / Med / High]
- **Documents requested:**
  - [list]
```

### Шаг 2. Document review

Each document:
- **Validity:** срок действия, подлинность
- **Consistency:** инфо matches across docs
- **Completeness:** все required fields filled
- **Compliance with regulator format:** наш regulator (ЦБ / Росфинмониторинг)

### Шаг 3. Verification + searches

- Sanctions screening done
- PEP screening done
- РНП checked (если applicable)
- Beneficial owners identified (для ЮЛ)
- Adverse media searched

### Шаг 4. Risk scoring

```markdown
## Risk score

| Factor | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Customer type (физ/юр + статус) | 0.20 | [0-100] | ... |
| Country / geography | 0.20 | ... | ... |
| Business activity | 0.15 | ... | ... |
| Transaction patterns expected | 0.15 | ... | ... |
| Beneficial owners (для ЮЛ) | 0.15 | ... | ... |
| Adverse media | 0.10 | ... | ... |
| Source of wealth / funds clarity | 0.05 | ... | ... |
| Total | | | [weighted average] |

**Risk category:** Low (< 30) / Med (30-70) / High (> 70)
```

### Шаг 5. Decision

#### Approve

- Onboard standard channel
- Apply ongoing monitoring per risk category
- Schedule periodic review

#### Approve with conditions

- EDD required first
- Senior approval before active business

#### Decline

- Document основание (115-ФЗ ст.7 ч.5.2 — обязательный отказ при невозможности идентификации / подозрении в легализации)
- Уведомление Росфинмониторинга (для повторных отказов в течение года)
- Не "tipping off" клиента (без подробностей причин)

### Шаг 6. Documentation

#### Customer file requirements

- All documents collected (originals или certified copies)
- KYC questionnaire (signed)
- Risk assessment
- Sanctions / PEP / РНП screening results
- BO analysis (для ЮЛ)
- Source of wealth / source of funds (для high-risk)
- Senior management approval (для high-risk)
- Onboarding decision rationale
- Retention period: **5 лет с момента прекращения отношений** (115-ФЗ ст.7 ч.4)

## Common pitfalls

### 🔴 Critical

- **Onboard без полной идентификации** — нарушение 115-ФЗ → штрафы + risk кaddrov ЦБ / Росфинмониторинга
- **Не identified beneficial owners** для ЮЛ — нарушение
- **Не проведена sanctions screening** — material AML failure
- **Документация incomplete** — at audit time issues

### 🟡 Medium

- Periodic review skipped или late
- Risk category incorrectly assigned (typically too low)
- EDD не triggered when should
- SoW / SoF inadequately documented

### 🟢 OK

- Standard onboarding с full documentation
- All searches done
- Risk-based approach applied

## Что НЕ делает

- Не actually onboard клиента (это banking system)
- Не handles compliance system integration (это IT + compliance team)
- Не handles disputes / complaints — это customer service / compliance

**Правовая основа:**
- ФЗ-115 ст.7 (KYC обязанности)
- ФЗ-115 ст.3 (определение бенефициарного владельца)
- Положение ЦБ № 499-П (для кредитных)
- Постановление Правительства № 667 (для прочих)
- ФАТФ Recommendations 10, 11, 12 (CDD framework)

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
