---
name: sanctions-screening
description: >
  Multi-jurisdictional sanctions screening — US OFAC, EU, UK, UN, РФ контр-санкции.
  РФ post-2022 — особо критичная area: Указы Президента 79, 81, 95, 252, 281, 322,
  430, 618, 950 и др. + соответствующие постановления Правительства. Sanctioned
  parties в client base = automatic freeze + report.
argument-hint: "[name / ИНН / address для screening]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /sanctions-screening

## Назначение

Screen клиента / контрагента / транзакции против sanctions lists multi-jurisdictional.

## Lists для screening

### A. РФ списки (обязательные)

| Список | Источник | Что |
|--------|----------|-----|
| **Перечень террористов и экстремистов** | Росфинмониторинг (fedsfm.ru) | ФИО + ID террористов / экстремистов |
| **Перечень организаций, причастных к терроризму** | Росфинмониторинг | Юр.лица |
| **Перечень для применения мер по замораживанию (ОМП)** | Росфинмониторинг | Организации финансирующие ОМП |

### B. Российские контр-санкции (post-2022)

| Указ | Что |
|------|-----|
| **Указ № 79 (28.02.2022)** | Ограничения по операциям с резидентами недружественных стран |
| **Указ № 81 (01.03.2022)** | Ограничения на сделки иностранцев с резидентами РФ |
| **Указ № 95 (05.03.2022)** | Временный порядок исполнения обязательств перед иностранными кредиторами |
| **Указ № 252 (03.05.2022)** | Меры по защите от недружественных действий |
| **Указ № 322 (01.06.2022)** | Временные правила выплаты долгов |
| **ПП РФ № 430 (08.05.2022)** | Перечень недружественных стран |
| **Указ № 618 (08.09.2022)** | Доп.требования к сделкам с участием недружественных |
| **Указ № 950 (15.10.2022)** | Особенности перевода долгов |
| Иные акты — обновляются regularly | Check current state |

**Перечень недружественных стран (ПП 430 + дополнения):**
- США
- Все страны ЕС (Австрия, Бельгия, Болгария, ..., все 27)
- Канада, Великобритания, Австралия, Япония, Новая Зеландия
- Швейцария, Норвегия, Исландия, Лихтенштейн, Монако
- Тайвань (китайский)
- Сан-Марино, Микронезия
- Албания, Северная Македония, Черногория
- Украина (с 2022)
- (Plus периодические дополнения)

### C. US OFAC

- **SDN List** (Specially Designated Nationals)
- **Sectoral Sanctions Identifications (SSI)** — restricted dealings
- **Non-SDN Communist Chinese Military Companies**
- **Иные**

### D. EU sanctions

- **Consolidated List** (financial restrictions, asset freezing)
- **Restrictive measures** по странам/regimes
- Russia-related sanctions (extensive)

### E. UK sanctions

- **OFSI Consolidated List**
- Russia-related restrictions

### F. UN sanctions

- **UN Consolidated List** (Al-Qaida, Taliban, и другие resolutions)
- Country-based (Iran, North Korea, и др.)

## Workflow

### Шаг 1. Identify данные для screening

```markdown
## Subject

- **Полное имя / наименование:** [exactly как в documents]
- **Variations имени:** [transliteration в кириллице + латинице; псевдонимы]
- **Дата рождения** (для физ.лица): [DD.MM.YYYY]
- **Гражданство:** [список если несколько]
- **Адрес:** [регистрации + фактический]
- **Документы удостоверяющие личность:** [номера]
- **Для ЮЛ:** ИНН + ОГРН + страна регистрации
- **Аффилированные лица** (для деep screening): [...]
- **Бенефициары** (для юр.лица): [физ.лица]
```

### Шаг 2. Run screening (multi-list)

#### Manual screening sources

- **Росфинмониторинг:** http://www.fedsfm.ru
- **OFAC:** https://sanctionssearch.ofac.treas.gov/
- **EU:** https://webgate.ec.europa.eu/europeaid/online-services/index.cfm?do=publi.welcome&nbPubliList=15&orderby=upd&orderbyad=Desc&searchtype=QS&aofr=125660
- **UK:** https://sanctionssearchapp.ofsi.hmtreasury.gov.uk/

#### Automated systems

- WorldCheck (Refinitiv)
- Dow Jones Risk & Compliance
- Accuity / Bankers Almanac
- Compliance-only services (e.g. Sanctions.io)
- For РФ-specific — СПАРК-Маркетинг, Контур.Фокус

### Шаг 3. Analyze hits

#### A. True positive (точное совпадение)

→ **STOP. Freeze. Report.**
- Block transaction / refuse onboarding
- Уведомить Росфинмониторинг в течение 1 раб.дня (для замораживания)
- Document полностью

#### B. Potential match (similar name / partial match)

→ Investigate:
- Additional identifiers (DOB, address, ИНН)
- Cross-check с другими sources
- Consult outside-адв ФПА если significant doubt

#### C. False positive (similar name только)

→ Document почему false positive:
- Different DOB / address / гражданство / контекст
- "Cleared" с обоснованием

### Шаг 4. Document результат

```markdown
# Sanctions Screening Report

**Subject:** [...]
**Date screened:** [DD.MM.YYYY HH:MM]
**Screener:** [user]

## Lists screened

- [✓] Росфинмониторинг (террористы)
- [✓] Росфинмониторинг (ОМП)
- [✓] РФ контр-санкции (недружественные страны)
- [✓] US OFAC SDN
- [✓] EU consolidated
- [✓] UK OFSI
- [✓] UN consolidated

## Result

[Cleared / Match found / Potential match — investigating]

## If match found

- **List(s):** [...]
- **Match strength:** exact / partial
- **Identifiers matching:** [name, DOB, address, etc.]
- **Action taken:** [freeze + report / declined onboarding / escalated to compliance officer]
- **Documentation:** [screenshot, doc references]

## If потенциально false positive

- **Reason for clearance:** [...]
- **Documentation:**

## Periodic re-screening

- **Next scheduled:** [DD.MM.YYYY] (regular interval per ПВК — typical 6-12 мес)
- **Triggers для ad-hoc re-screening:** изменение activity, новые beneficial owners, и т.п.
```

### Шаг 5. Action при confirmed match

#### A. Применение мер по замораживанию

- **Немедленно** заморозить операции subject
- Уведомить Росфинмониторинг в 1 раб.день через formal SAR
- Документировать действия
- Continuing monitoring (не "разморозить" без основания)

#### B. Если subject уже в client base

- Apply freeze к существующим операциям
- Reverse невыполненные транзакции если applicable
- Cross-reference со всеми аккаунтами subject

#### C. Уведомление subject

- Generally **не** уведомляем subject о причине отказа / замораживания
- 115-ФЗ запрещает "tipping off" — informing subject о SAR / freeze

#### D. Engagement outside-адв ФПА

- For complex cases — privileged advice
- Particularly important для cross-border situations (US OFAC violations have extraterritorial reach)

## Specific scenarios

### Scenario 1: Российская компания с иностранным владельцем (из недружественной страны)

Post-2022:
- Проверка через Указы 79, 81, 95
- May require разрешение Правкомиссии для определённых операций
- Limitations на расчёты, переводы
- Engage outside-адв для structuring

### Scenario 2: Корреспондент-банк в США / EU отказывает в платеже

- Часто из-за их собственного OFAC compliance
- Не РФ regulatory issue, но business consequence
- Alternative: использовать banks с continuing access (Asian, etc.)

### Scenario 3: Sanctioned client пытается провести транзакцию

- Block
- Report Росфинмониторингу
- Document полностью
- Internal procedure if appeal received

### Scenario 4: Beneficial owner в OFAC SDN

- Юр.лицо может быть "blocked person" если > 50% owned by SDN (50% rule)
- Apply blocking
- Considerar restructuring если business critical

## Что НЕ делает

- Не handles US OFAC voluntary disclosure (это outside-адв с US-bar credentials)
- Не replaces compliance team — это вспомогательный tool
- Не unblocks/declassifies (это формальная procedure через Росфинмониторинг)

## Why critical для РФ post-2022

Sanctions landscape для РФ businesses dramatically изменён с 2022:
- US/EU/UK ужесточили санкции — РФ counterparties под scrutiny
- РФ introduced контр-санкции — иностранцы под scrutiny
- Compliance — bidirectional + multi-layer
- Banks могут freeze accounts если sanctions concerns

**Правовая основа:**
- ФЗ-115 (ПОД-ФТ)
- Указы Президента РФ (Sanctions-related, 2014-2025+)
- Постановления Правительства РФ
- ОФАК, EU, UK regulations (extraterritorial reach)
- ФАТФ Recommendations

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
