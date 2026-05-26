---
name: pep-screening
description: >
  PEP (Politically Exposed Persons) screening. РФ 115-ФЗ — иностранные публичные
  должностные лица (IPEP), должностные лица международных организаций (IOPEP),
  и российские публичные должностные лица (DPEP). Все требуют Enhanced Due
  Diligence (EDD).
argument-hint: "[name / position]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /pep-screening

## Назначение

Определить — является ли клиент / бенефициарный владелец / близкий родственник
publically exposed person (PEP). PEP status triggers EDD (Enhanced Due Diligence).

## Categories PEP (115-ФЗ)

### A. IPEP (Иностранные публичные должностные лица)

Иностранные лица, занимающие / занимавшие:
- Высшие государственные должности (президенты, премьеры, министры)
- Должности высших судебных, законодательных, военных чинов
- Руководящие посты центральных банков
- Послы и руководители консульств
- Топ-менеджмент гос.компаний (если "high importance")

Через **3 года** после прекращения полномочий — переоценка risk (но typically остаются PEP в общественном восприятии).

### B. IOPEP (Должностные лица международных организаций)

Высшее руководство:
- ООН и agencies
- World Bank / IMF
- EU institutions
- WTO, OECD
- Региональные международные (СНГ, ОДКБ, БРИКС institutions, и т.д.)

### C. DPEP (Российские публичные должностные лица)

С 2018 (Указом Президента) — включены в систему PEP:
- Президент РФ
- Председатель Правительства РФ + заместители
- Министры федеральные
- Депутаты Госдумы + Совет Федерации
- Высшие судьи (Конституционный Суд, Верховный Суд)
- Руководители ФОИВ (федеральных органов исполнительной власти)
- Главы субъектов РФ
- Послы РФ
- Топ-менеджмент гос.корпораций / гос.компаний (Газпром, Роснефть, Ростех, Сбербанк, ВТБ, и т.д.)
- Председатель ЦБ РФ + заместители

### D. Связанные лица (Related PEP)

- Супруг(а)
- Дети
- Родители (если применимо к политическому context)
- Иные близкие родственники

## Workflow

### Шаг 1. Verify identifying info

```markdown
## Subject

- **Имя:** [...]
- **Гражданство:** [...]
- **Должность:** [...]
- **Период работы:** [...]
- **Связь с client:** [self / спouse / child / parent / иное]
```

### Шаг 2. Search PEP databases

#### Sources

- **WorldCheck (Refinitiv)** — leading commercial
- **Dow Jones Risk & Compliance**
- **Accuity / Bankers Almanac**
- **РФ-specific:** СПАРК-Маркетинг, Контур.Фокус (для российских PEP)
- **Общие открытые источники:** Wikipedia, news media archives
- **Government websites:** rosznak.gov.ru (РФ должностные лица)
- **ФНС реестры:** для официальных позиций в гос.компаниях

#### Search strategy

- Exact name match
- Variations (transliteration, diminutives)
- Aliases / pseudonyms (если public figure)
- Spouse / family members search (для Related PEP)

### Шаг 3. Anaylze results

#### Case A: Active PEP

→ Apply EDD:
- Senior management approval onboarding
- Establishment of source of wealth + funds
- Enhanced monitoring транзакций
- Periodic review (annual minimum)
- Reasonable measures to determine if family members / close associates also need EDD

#### Case B: Former PEP (out of office > 3 года)

- Risk assessment per individual case
- Generally still EDD recommended если recent influence

#### Case C: Related PEP only

- EDD also applied
- Documentation того что PEP affiliation disclosed

#### Case D: Not PEP

- Standard CDD
- Document searches as "negative confirmation"

### Шаг 4. EDD measures для PEPs

#### Senior management approval

- Required for onboarding / continued relationship с PEP
- Documentation решения

#### Source of Wealth (SoW)

- Объяснение происхождения накопленного wealth (career, наследство, business, инвестиции)
- Documents support: tax declarations, business records, inheritance docs

#### Source of Funds (SoF)

- Для конкретных транзакций
- Documents: salary records, business income, sale of assets

#### Enhanced ongoing monitoring

- Более частое review транзакций
- Lower alert thresholds
- Regular CDD updates (annual)

### Шаг 5. РФ-specific considerations

#### Sanctions overlap

- Many РФ PEPs are on US OFAC / EU / UK sanctions lists post-2014/2022
- Cross-check sanctions screening (`/sanctions-screening`)
- If both PEP and sanctioned → automatic high concern + likely refuse / freeze

#### Anti-corruption (273-ФЗ)

- DPEP — раскрытие доходов в decларациях (ежегодно)
- Cross-check с публикуемой декларацией если accessible
- Для значительных incongruities — flag

#### Sanctions implications

- Public scrutiny — even legitimate transactions с PEPs могут привлечь внимание
- Reputation risk для финансового института

## Output

```markdown
# PEP Screening — [имя]

## Identification

- **Имя:** [...]
- **Position:** [...]
- **Country:** [...]
- **Category:** [IPEP / IOPEP / DPEP / Related PEP / Not PEP]
- **Active / Former:** [...]

## Sources checked

- [✓] WorldCheck
- [✓] Dow Jones
- [✓] СПАРК
- [✓] Open sources (Wikipedia, news)
- [✓] Government registries

## Cross-checks

- **Sanctions:** [cleared / hit found]
- **Adverse media:** [findings]
- **Anti-corruption (для DPEP):** [декларация о доходах подавалась? соответствие?]

## Decision

[Onboard with EDD / Onboard standard / Decline with rationale]

## EDD measures (если applies)

- [ ] Senior management approval — ФИО, дата
- [ ] SoW documented
- [ ] SoF documented per транзакции
- [ ] Enhanced monitoring enabled
- [ ] Periodic review scheduled — annual

## Documentation

- Saved in customer file: [path]
- Re-screen schedule: [annual / per-event]
```

## Что НЕ делает

- Не actually onboard с EDD — это compliance team
- Не делает publish PEP relationship — это confidential
- Не handles regulator inquiries — это outside-адв

**Правовая основа:**
- ФЗ-115 ст.7.3 (PEP determination + EDD)
- Положение ЦБ № 375-П
- ФАТФ Recommendations 12 (PEP-related)
- ФЗ-273 «О противодействии коррупции»

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
