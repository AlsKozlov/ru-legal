---
name: integration-management
description: >
  Post-M&A integration framework — что делать после closing. Tracks consents,
  notifications, legal entity housekeeping (rename, merger options),
  HR integration (ст.75 ТК — реорганизация vs. share deal differences),
  IT/системы, банк-счета, license transfers, IP инвентаризация.
argument-hint: "[deal name] [phase: 0-30 / 30-60 / 60-90 / 90-180]"
user_invocable: true
ported_from: corporate-legal/integration-management
ported_at: 2026-05-19
adaptation_category: B
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /integration-management

## Назначение

Post-closing integration framework. M&A — это not just signing. Integration —
это где 50%+ value delivery либо destruction.

Tracks tasks по фазам: T+0-30 (immediate), T+30-60 (early), T+60-90 (mid),
T+90-180 (mature).

## Pre-flight

- **Deal type:** share deal / asset deal / реорганизация
- **Integration model:** absorb / stand-alone / hybrid
- **Critical contracts identified** (из `/material-contract-schedule`)
- **DD findings** known (из `/diligence-issue-extraction`)
- **Day 1 communication plan** ready

## РФ-specific integration considerations

### При share deal (доли / акции)

- **Target preserves legal personality** — no automatic transfer of контракты, работников и т.п.
- **Change-of-control clauses** в контрактах — могут trigger termination / consent
- **Employees** — ТД сохраняются автоматически (ст.75 ч.5 ТК)
- **Лицензии** — могут require notification / re-issue для смены учредителей
- **Банковские счета** — нужна замена signatures (новые подписи; иногда новый KYC)

### При asset deal

- **Каждый контракт** transfers только если другая сторона consent (ст.382 ГК)
- **Employees** — особый режим (ст.75 ТК):
  - ст.75 ч.5: смена собственника имущества организации = ТД не прекращаются (но руководитель / заместители / главбух могут быть уволены за 3 мес)
  - При выделении / разделении части (как структурного подразделения) — ст.75 ч.2: ТД сохраняются если работник согласен; иначе ст.77 п.6 (отказ от работы у нового собственника)
- **Real estate** — отдельная regsration в ЕГРН
- **IP** — нужна перерегистрация в Роспатент

### При реорганизации (слияние / присоединение / разделение / выделение)

- **Universal succession** — все права и обязанности переходят правопреемнику автоматически (ст.58-59 ГК)
- **Employees** — ТД сохраняются (ст.75 ч.5)
- **Контракты** — переходят без consent (но change-of-control clauses всё ещё работают)
- **Период для кредиторских требований** — 2 мес с уведомления

## Workflow по фазам

### Phase T+0-30 (Immediate post-closing)

#### Корпоративные

- [ ] Подтверждение Day 1 — все share / долевой transfer закрыт + регистрация в ЕГРЮЛ / реестре
- [ ] Замена единоличного исп.органа (если планируется) — решение + регистрация Р13014 в 7 раб.дней
- [ ] Изменения в уставе если требуются — Р13014
- [ ] Smena корпоративного секретаря (для ПАО)
- [ ] Прекращение полномочий старых членов СД (если применимо)
- [ ] Назначение новых членов СД — внеочередное ОСУ/ОСА
- [ ] Обновление списка аффилированных лиц
- [ ] Решение об учёте mneniya аудитора (если меняется)

#### Финансовые

- [ ] Эскроу check — открыт / закрыт по графику
- [ ] Open accounts проверка — все ли согласованы
- [ ] Обновление подписей в банках (новый ГД)
- [ ] Аудиторский Q4 / Q1 close в течение периода
- [ ] Working capital adjustment начат (если механизм предусмотрен SPA)

#### Регуляторные

- [ ] ФНС — изменения в ЕГРЮЛ зарегистрированы
- [ ] СФР — изменения в registration
- [ ] РКН — если оператор data изменился — уведомление
- [ ] Банк России (для ПАО) — disclosure о deal в Сообщениях о существенных фактах
- [ ] ФАС — если согласование было — confirm closing completed
- [ ] Указ 81/2022 — если разрешение было получено — confirm conditions met

#### Контракты

- [ ] Notify контрагентов о смене учредителей / директора (для CoC clauses)
- [ ] Получить waivers / consents для CoC contracts identified в DD
- [ ] Refinance loans с automatic termination on CoC (если не достигнут waiver)
- [ ] Renegotiate IP licenses с termination-on-CoC
- [ ] Material customer contracts — early engagement для maintain retention

#### HR

- [ ] Communication работникам (Day 1)
- [ ] Retention bonuses для key persons — paid / accrued
- [ ] Severance для departing executives (соглашение сторон ст.78)
- [ ] Обновление кадрового учёта (новый собственник в personal cards)
- [ ] Review компенсация structures (для harmonization)

#### IT / системы

- [ ] Access management — старые admins removed, новые added
- [ ] Domain transfers
- [ ] Email / messaging integration plan started
- [ ] ERP / accounting систем consolidation roadmap
- [ ] Cyber security audit
- [ ] Data backup verification

### Phase T+30-60 (Early integration)

- [ ] R&W bring-down assessment — есть ли triggered breaches?
- [ ] Indemnity claims — если есть, оформить formal demand
- [ ] Tax filings consolidation — план для следующего periоd
- [ ] HR policies harmonization начата (ЛНПА — см. labor-law/handbook-updates)
- [ ] Vendors consolidation (один supplier per category, если предусмотрено)
- [ ] Office consolidation (если planned — leases)
- [ ] CSR / branding align (если applicable)
- [ ] Communications stakeholders (employees + customers + suppliers)

### Phase T+60-90 (Mid integration)

- [ ] First financial close consolidated (бух.отчётность combined)
- [ ] Cross-selling initiatives launched (если synergies planned)
- [ ] Severance / restructure decisions finalized
- [ ] License transfers completed (Роспатент, СРО, отраслевые регуляторы)
- [ ] Real estate consolidation moves (если planned)
- [ ] First operational synergies measured

### Phase T+90-180 (Mature integration)

- [ ] Indemnity period ongoing — track claims через `/material-contract-schedule` updates
- [ ] Synergies tracking — actual vs planned
- [ ] Integration declared complete либо ongoing items moved to BAU
- [ ] Decommission специальных PMO processes
- [ ] Lessons learned doc

## Integration scorecard

```markdown
# Integration Scorecard — [Deal name]
**Дата:** [DD.MM.YYYY] (T+[X days from closing])

## Корпоративные milestones

- [✓] Ownership transfer regis в ЕГРЮЛ — T+5
- [✓] New ГД appointed + Р13014 filed — T+10
- [✗] **OVERDUE:** Список аффилированных лиц updated — T+30
- ...

## Финансовые

- [✓] Banking signatures updated — T+15
- [✓] Working capital adjustment received — T+45
- [PENDING] Q1 close consolidated — T+60
- ...

## Контракты — CoC

| # | Контрагент | Контракт | Status | Action |
|---|------------|----------|--------|--------|
| 1 | Сбербанк | Loan 500M | refinanced T+45 | ✓ done |
| 2 | ООО Альфа (key client) | Поставка | consent received T+30 | ✓ done |
| 3 | Microsoft | ПО enterprise | termination notice received T+25, renegotiation pending | 🟡 in progress |
| 4 | ... | | | |

## HR

- Retention bonuses paid: 5/5 key persons
- Severance closed: 3 departing executives
- Policy harmonization: 50% complete (ПВТР done, Положение об оплате в работе)

## Synergies

| Synergy | Target | Actual @ T+90 | % of target |
|---------|--------|---------------|-------------|
| Cost (procurement) | 50M / year | 30M / year run-rate | 60% |
| Revenue (cross-sell) | 100M / year | 20M / year | 20% |
| Headcount reduction | 15 FTE | 12 FTE | 80% |

## R&W / indemnity

- Survival period: до DD.MM.YYYY
- Claims notified: [N] — total exposure [сумма]
- Escrow released: [сумма] / pending release [сумма]
- Open litigation post-closing: [N cases]

## Issues / blockers

[List]
```

## РФ-specific gotchas (always check)

### 1. ст.382 ГК — assignment контрактов при asset deal

При asset deal (не share / реорганизация) — каждый контракт **требует consent** другой стороны для уступки. Без — uplate price / penalty / нарушение.

### 2. ст.75 ТК — работники при разных типах сделок

| Тип сделки | Работники | Особенности |
|------------|-----------|--------------|
| Share deal (покупка долей / акций) | Сохраняются автоматически | Без consent |
| Реорганизация (слияние / присоединение / etc.) | Сохраняются автоматически (ст.75 ч.5) | Руководитель / заместители / главбух — могут быть уволены в 3 мес |
| Asset deal — целое предприятие | Переход с согласия работника (ст.75 ч.2) | Отказ → ст.77 п.6 |
| Asset deal — отдельные активы | ТД не переходят | Должны быть заключены новые ТД или уволены по сокращению ст.81 п.2 |

### 3. Налоги после closing

- НДС-режимы могут меняться при slияни / преобразовании
- Перенос убытков (НК ст.283) — реорганизация может limit
- Контролируемые сделки — новый affiliation triggers documentation требования
- Transfer pricing — для cross-border integration

### 4. Лицензии — re-issuance vs notification

| Тип | Action |
|-----|--------|
| Банковская лицензия | Notify Банк России; в ряде случаев — re-issue с smenой учредителей |
| Лицензия на нефтегаз | Notification Росприроднадзору |
| Лицензия фарм | Notification Минздрава |
| СРО членство | Notification СРО |
| ОСАГО / страхование | Banк России (с 2013 — все страх. под ЦБ) |

Без notifications — risk withdrawal license.

### 5. ПДн (152-ФЗ)

- Если operator данных меняется — нужно уведомить РКН
- Если cross-border передача меняется — отдельное уведомление

## Что НЕ делает

- Не управляет integration team (это PMO)
- Не negotiates consents — это commercial team + outside-адв
- Не подает в реестры — это секретарь / outside-адв

## Attribution

Adapted from [`corporate-legal/integration-management`](https://github.com/anthropics/claude-for-legal/blob/main/corporate-legal/skills/integration-management/SKILL.md)
by Anthropic (Apache 2.0).

**Категория B:**
- Phases preserved, items RU-adapted
- ст.75 ТК (работники при разных типах сделок) — нет US equivalent (US WARN Act другое)
- ст.382 ГК assignment of contracts — РФ-specific
- ФАС / ЦБ / РКН regulators — РФ-specific landscape
- Указ 81/2022 follow-up — post-2022 РФ-specific
- ст.58-59 ГК universal succession при реорганизации — РФ-specific

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

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
