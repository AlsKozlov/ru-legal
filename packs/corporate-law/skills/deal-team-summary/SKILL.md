---
name: deal-team-summary
description: >
  Audience-specific summary M&A или другой corporate matter для deal team
  members. Adjusts detail level + emphasis: CEO / CFO / Председатель СД /
  outside-адв ФПА / финансовый advisor / банк-кредитор / regulator
  (ФАС / ЦБ).
argument-hint: "[matter context] [audience]"
user_invocable: true
ported_from: corporate-legal/deal-team-summary
ported_at: 2026-05-19
adaptation_category: A
---

# /deal-team-summary

## Назначение

Audience-specific summary corporate matter (M&A, IPO, реорганизация, крупная
сделка). Differs from legal memo: focused на decision support stakeholders,
не на legal analysis (which goes к outside-адв ФПА).

## Audiences и адаптация

| Audience | Detail level | Privilege framing | Focus |
|----------|--------------|-------------------|-------|
| CEO | Strategic + risk | Privileged через outside-адв ФПА (если involve) | Decision-focused |
| CFO | Financial impact + risks | Same | Financial diligence + structuring |
| Председатель СД | Governance + asks | Same | Authorization required, formal record |
| Outside-адв ФПА | Full disclosure | Privileged communication | Legal-detailed |
| Финансовый advisor (banker) | Deal structure + timing | Confidential | Deal mechanics |
| Кредитор (банк) | Impact на covenants | Confidential | Credit considerations |
| ФАС | Только запрошенное | Public-facing | Compliance с filing requirements |
| ЦБ РФ (для ПАО) | Disclosure obligations | Public | Regulatory compliance |

## Pre-flight

- **Matter context** loaded (deal type, parties, value, current stage)
- **Audience** chosen
- **Privilege status** clear (outside-адв ФПА involved?)

## Workflow

### Шаг 1. Identify audience + main asks

Каждая audience имеет distinctive concerns:

#### CEO

- Strategic fit
- Material risks
- Decision required (proceed / pause / walk)
- Timeline impact

#### CFO

- Purchase price + structure
- Financing requirements
- Working capital adjustment
- Tax structuring
- Indemnification escrow

#### Председатель СД

- Authorizations required (one-shot or per-step)
- Independent directors involvement
- D&O insurance coverage
- Disclosure обязательства

#### Outside-адв ФПА

- DD findings — full
- R&W structure
- Indemnity caps + survival
- Conditions precedent
- Risks для litigation post-closing

#### Финансовый advisor

- Deal structure (share vs asset)
- Tax-optimized structure
- Earn-out / contingent consideration
- Closing mechanics
- Valuation considerations

#### Кредитор (банк)

- Covenant compliance assessment
- Change-of-control triggers
- Refinancing needs
- Subordination implications

#### ФАС

- Конкретные responses на запросы
- Notification + supporting материалы
- Activities target и acquirer

#### ЦБ РФ (для ПАО)

- Disclosure to be issued
- Timing relative к ФЗ-39 ст.30
- Sufficient material info

### Шаг 2. Generate summary per audience

#### Template: CEO briefing

```markdown
# CONFIDENTIAL — [Deal name] — CEO Briefing

**Дата:** [DD.MM.YYYY]
**Стадия:** [LOI / DD / signing / closing / integration]
**Целевая дата signing:** [DD.MM.YYYY]
**Целевая дата closing:** [DD.MM.YYYY]

## Bottom line (одно предложение)

[Recommendation: PROCEED at [price], PAUSE pending [issue], or WALK from deal because [reason]]

## Strategic rationale (3 bullets)

- [Why this deal still makes sense]
- ...

## Material risks (top 3)

1. **[Risk]** — [conclusion]: [recommendation]
2. ...

## Asks

- [ ] Approval to [действие]
- [ ] Budget [сумма] для outside-адв ФПА
- [ ] Decisions on R&W escrow target (recommend [X% от deal value])

## Timeline критичные milestones

- ФАС filing (если applicable): [DD.MM.YYYY], approval expected [DD.MM.YYYY]
- Signing target: [DD.MM.YYYY]
- Closing target: [DD.MM.YYYY]
- First DD-findings deadline: [DD.MM.YYYY]

## Что не рассмотрено

[Scope limitations]
```

#### Template: CFO briefing

```markdown
# CONFIDENTIAL — [Deal name] — CFO Briefing

## Financial structure

- **Purchase price:** [сумма] руб
- **Структура:** [cash / equity / cash + earn-out / cash + escrow / etc.]
- **Налоговая структура:** [share deal (no НДС) / asset deal (НДС применим)]
- **Working capital adjustment:** [yes/no — механизм]
- **Earn-out:** [terms]
- **Escrow:** [сумма + срок release]

## Financing

- Source of funds: [own cash / banking facility / bridge / iz]
- New facility required: Y/N, сумма [...]
- Existing covenants impact: [нет / triggered, мер: ...]

## Tax structuring

- НДФЛ / налог на прибыль для seller: [...]
- Buyer — НДС: [применим / неприменим]
- Stamp duty / госпошлины: [...]
- Налоговые льготы (5-летнее владение для физ.лиц-продавцов): [...]
- Cross-border considerations: [...]

## Synergies / accretion

- Cost synergies: [сумма / срок]
- Revenue synergies: [сумма / срок]
- EPS impact: [...]
- Integration costs: [...]

## Key DD findings (financial)

- Quality of earnings: [findings]
- Working capital: [findings]
- Inventory / receivables: [findings]
- Tax exposures (open ВНП, споры): [список + сумма]

## Indemnity / escrow recommendation

- Cap: [% from deal value]
- Survival: [12 / 18 / 24 months]
- Specific indemnities (uncapped): [list — tax, ПДн, sanctions]
- Escrow: [сумма] held [X months]
```

#### Template: Председатель СД — для одобрения СД

```markdown
# Brief для Совета директоров — [Deal name]

## Резюме

[1-2 предложения]

## Запрос к Совету директоров

Просим СД принять решение о:

1. Одобрении сделки [SPA] с [Seller] на сумму [...]
2. Уполномочии [Genеральный директор / иное лицо] на подписание deal-documents
3. Одобрении сделки как "крупной" / "с заинтересованностью" (если applicable) в соответствии со [ст.46 ФЗ-14 / ст.78 ФЗ-208 / ст.45 ФЗ-14]
4. [Иные одобрения, если применимо]

## Сведения для решения

- Стороны сделки: [seller, buyer, target]
- Стоимость сделки: [сумма] руб
- Балансовая стоимость отчуждаемых активов / приобретаемых: [сумма]
- % от балансовой стоимости активов общества: [%]
- Заинтересованные лица (если ст.45): [перечень]
- DD findings основные: [высокоуровнево]
- Структура финансирования: [...]
- R&W + indemnity arrangements: [...]

## Independent directors involvement

[Если есть — рекомендация со стороны independent directors]

## D&O coverage

- Текущая policy покрывает данную сделку: Y/N
- Требуется ли отдельное покрытие: Y/N

## Прилагаемые материалы

1. Draft SPA + schedules
2. DD findings summary
3. Решения предыдущих органов (если каскад)
4. Financial advisor opinion (если есть)
5. Outside-адв legal opinion / memorandum

## Дата заседания СД для одобрения

[DD.MM.YYYY]

## Дата signing после одобрения

[DD.MM.YYYY]
```

#### Template: ФАС-уведомление о сделке

```markdown
# Ходатайство о согласовании сделки экономической концентрации

**В:** Федеральную антимонопольную службу (или территориальное управление)
**От:** [Buyer / Acquirer]
**Дата:** [DD.MM.YYYY]

В соответствии со ст.27-28 ФЗ-135 «О защите конкуренции» обращаемся с
ходатайством о согласовании сделки.

## Сведения о сделке

- **Тип:** [share deal / asset deal / реорганизация]
- **Стороны:** [seller, buyer, target — с ИНН]
- **Объект сделки:** [доли / акции / активы]
- **Стоимость:** [сумма] руб
- **Дата планируемого совершения:** [DD.MM.YYYY]

## Сведения о target

- ОКВЭД основной + дополнительные
- География деятельности
- Финансовые показатели: выручка + активы за последний год
- Доля на рынке (per OECД-classification рынки) — если есть данные

## Сведения о buyer (group)

- Same as выше

## Pre-merger concentration analysis

- Релевантные рынки: [определение]
- Совокупная доля после сделки: [% / диапазон]
- Не приводит ли к ограничению конкуренции: [analysis]

## Подтверждающие документы

1. Учредительные документы обеих сторон
2. Финансовая отчётность за 3 года
3. Бизнес-план / стратегия
4. Сведения о affiliated лицах
5. Иные

[Подпись + дата]
```

### Шаг 3. Review checklist before sending

- [ ] Audience-appropriate (по detail, language, focus)
- [ ] Confidentiality / privilege framing correct
- [ ] ПДн / commercially sensitive — minimum disclosed
- [ ] No legal conclusions если audience non-legal
- [ ] Timing критичные milestones included

## Что НЕ делает

- Не заменяет outside-адв legal opinion для material decisions
- Не подает в регуляторы — это outside-адв
- Не negotiates terms

## Attribution

Adapted from [`corporate-legal/deal-team-summary`](https://github.com/anthropics/claude-for-legal/blob/main/corporate-legal/skills/deal-team-summary/SKILL.md)
by Anthropic (Apache 2.0).

**Категория A:**
- Audience list adapted to РФ realities (ФАС / ЦБ specific templates)
- Корпоративные одобрения (ст.46/78, ст.45) — РФ-specific decision framework для СД
- ФАС ходатайство template — РФ-specific format
- Indemnification structure с ссылками на ст.431.2 / 406.1 ГК

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
