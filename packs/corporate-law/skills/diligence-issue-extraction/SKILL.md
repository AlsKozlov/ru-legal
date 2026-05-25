---
name: diligence-issue-extraction
description: >
  Due Diligence findings extractor для РФ target. Категории: корпоративная
  структура (ЕГРЮЛ), налоговая (ФНС + камералки + ВНП), судебная (kad.arbitr +
  суды общей юрисдикции), банкротство (ЕФРСБ), недвижимость (Росреестр),
  лицензии / разрешения, IP (Роспатент), labor (ГИТ предписания), 152-ФЗ
  compliance, sanctions screening (US OFAC / EU / РФ контр-санкции).
argument-hint: "[path к DD documents / название target]"
user_invocable: true
ported_from: corporate-legal/diligence-issue-extraction
ported_at: 2026-05-19
adaptation_category: B
---

# /diligence-issue-extraction

## Назначение

Extract structured DD findings из multiple sources (documents, реестры, exhibits)
в tabular format с risk classification. Output — Issues List готовый к share с
deal team / acquirer / sellers.

## Pre-flight

- **Целевой target identified** (ОГРН / ИНН для запросов в реестры)
- **Scope DD** определён (full / focused; pre-LOI / post-LOI)
- **MCPs available:**
  - `egrul` — для ЕГРЮЛ / ЕГРИП (обязательно)
  - `kad` — для арбитражных судов (optional, but key для litigation findings)
  - `efrsb` — для банкротства (optional)
  - `pravo` — для НПА цитат
- **Materiality thresholds** загружены из PROFILE.md

## РФ DD категории — comprehensive checklist

### A. Корпоративная структура / ЕГРЮЛ

| Check | Source | Что искать |
|-------|--------|------------|
| Действующее юр.лицо? | ЕГРЮЛ | Не в стадии ликвидации, реорганизации |
| Уставный капитал оплачен | Устав + ЕГРЮЛ | Полная оплата подтверждена |
| Текущая редакция устава | Устав от DD.MM.YYYY | Совпадает с ЕГРЮЛ записью |
| Изменения в ЕГРЮЛ — последние 12 мес | ЕГРЮЛ выписка | Что меняли (директор, адрес, учредители, доли) |
| Бенефициарные владельцы (115-ФЗ) | Internal list + ФНС декларация | Заполнено корректно |
| Преобразование/реорганизация в истории | ЕГРЮЛ | Если было — все ли права/обязательства переданы |

### B. Налоговая

| Check | Source | Что искать |
|-------|--------|------------|
| Задолженность по налогам | Справка ФНС | Текущая на дату issuance |
| Открытые камеральные проверки | ФНС | Status, expected resolution |
| Открытые / завершённые ВНП | ФНС + outside-адв inquiry | Решения, оспаривания |
| Налоговые споры в суде (АС) | kad.arbitr | Список + claims |
| Реструктуризация налогового долга | ФНС | Графики платежей |
| Сложные операции с НДС (возмещение) | Audit + outside-адв | History blocks / questions |
| Transfer pricing документация (раздел V.1 НК) | Audit | Готовность documentation для controlled transactions |
| Налоговый мониторинг участник? | ФНС | Если да — лимитированы выездные |

### C. Судебная (арбитраж + ОЮ)

| Check | Source | Что искать |
|-------|--------|------------|
| Открытые иски target как ответчика | kad.arbitr | Суммы, вероятность proигрыша, materiality |
| Открытые иски target как истца | kad.arbitr | Возможные recoveries |
| Исполнительные производства (ФССП) | fssp.gov.ru | Долги к взысканию |
| Иски от работников (ГИТ + суды ОЮ) | Гид + outside-адв | Labor litigation |
| Корпоративные споры | kad.arbitr | Споры с участниками / другими акционерами |
| Уголовные дела (УК) против руководства | Public sources / outside-адв | Экон.УК (ст.159, 199, 201, 285-291) |

### D. Банкротство

| Check | Source | Что искать |
|-------|--------|------------|
| Target в реестре банкротов? | ЕФРСБ | Если да — STOP, escalate |
| Заявления о банкротстве в кат-арбитр | kad.arbitr | Pending applications |
| Знакомства с банкротными процедурами (даже как кредитор) | ЕФРСБ | Текущая involvement |
| Аффилированные лица в банкротстве | ЕФРСБ + аффилированность analysis | Risk of subsidiary liability |
| Subsidiary liability claims (КДЛ) | kad.arbitr | Личная ответственность руководства |

### E. Недвижимость

| Check | Source | Что искать |
|-------|--------|------------|
| Право собственности на ключевые объекты | Росреестр (ЕГРН) | Подтверждение |
| Обременения (ипотека, сервитуты, аренда) | ЕГРН | Не выявлены ли |
| Аренда — срок + условия | Договоры аренды | Renewal, termination clauses, indexation |
| Кадастровая стоимость vs балансовая | ЕГРН + бух.отчётность | Discrepancies |
| Споры по объектам недвижимости | kad.arbitr + суды ОЮ | Open litigation |

### F. Лицензии / разрешения

| Check | Source | Что искать |
|-------|--------|------------|
| Перечень лицензий и разрешений (ОКВЭД-driven) | Internal + регуляторы | Все ли действующие |
| Сроки действия | Лицензии | Истекают в ближайший год — flag |
| Условия передаваемости при смене учредителей | Лицензии + соответствующий регулятор | СРО членство, банковские, нефтегаз — все могут require notification |
| Нарушения лицензионных требований | Внутренние audit + регулятор | Предписания |
| Тех.условия (СОУТ, экология, etc.) | Внутренние audit | Действительны |

### G. IP (Роспатент / ФИПС)

| Check | Source | Что искать |
|-------|--------|------------|
| Товарные знаки — реестр | Роспатент | Действительные, в собственности target |
| Изобретения / полезные модели / промобразцы | Роспатент | То же |
| Лицензионные договоры (target как лицензиар) | Контракты + Роспатент | Зарегистрированы |
| Лицензионные / IP — target как лицензиат | Контракты | Termination on change-of-control? |
| ПО / БД — авторские права | Внутренний реестр | Servisno-trudovaya formula (ст.1295 ГК) |
| Открытые споры по IP | kad.arbitr + СИП | Cease & desist, infringement |

### H. Labor

| Check | Source | Что искать |
|-------|--------|------------|
| ТД ключевых сотрудников | HR | Подписаны, обязательные условия по ст.57 |
| Колдоговор, ЛНПА | HR | Действующие |
| Открытые трудовые споры | Суды ОЮ + ГИТ | Восстановления, СЗП за вынужденный прогул |
| ГИТ предписания | ГИТ + outside-адв | Исполнены / в обжаловании |
| Задолженность по зарплате | Бух + ФНС / СФР | Текущая |
| Использование самозанятых / ГПД | HR audit | Risk переквалификации (см. labor-law/worker-classification) |
| Иностранные работники | HR | Compliance ФЗ-115 |
| СОУТ актуальна (последние 5 лет) | HR + СОУТ карты | По всем рабочим местам |

### I. ПДн (152-ФЗ)

| Check | Source | Что искать |
|-------|--------|------------|
| Уведомление РКН подано | Реестр операторов на rkn.gov.ru | Есть запись |
| Политика обработки ПДн опубликована | Сайт компании | Доступна на сайте |
| ОВПД (оценки вреда) проведены | Internal | Для систем УЗ-1/2/3 |
| ПДн локализация (ст.18 ч.5 152-ФЗ) | IT audit | Базы данных РФ residents — в РФ |
| Cross-border передача — уведомление РКН | РКН реестр | Подано |
| Утечки за 12 мес | Internal incident log + РКН | Зарегистрированы |
| Штрафы РКН | Public records | За последние 3 года |

### J. Sanctions

| Check | Source | Что искать |
|-------|--------|------------|
| Target / бенефициары в US OFAC SDN list | OFAC | Sanctioned? |
| EU consolidated sanctions list | EU | Sanctioned? |
| UK sanctions | UK gov | Sanctioned? |
| Российский ответный санкционный список (Указы Президента) | Internal | Target / бенефициары в счёте |
| Counter-sanctions exposure (Указ Пр. РФ 81/2022, и т.д.) | Анализ структуры | Если иностранный акционер из недружественных |
| Доступ к платёжным системам, банкам | Operational checks | Не отрезали ли |

### K. Антимонопольное (ФАС)

| Check | Source | Что искать |
|-------|--------|------------|
| Доминирующее положение target в каком-либо рынке | ФАС реестр | Если да — limitations |
| Открытые ФАС дела | ФАС | По нарушениям закона о конкуренции |
| Согласование M&A required для текущей сделки? | Расчёт по ст.27-28 ФЗ-135 | Активы + выручка thresholds |
| Картельные соглашения / сговоры в истории | Audit + ФАС | Не было ли |

### L. Экология / охрана труда

| Check | Source | Что искать |
|-------|--------|------------|
| Природоохранные разрешения | Минприроды / Росприроднадзор | Действующие |
| Платежи за негативное воздействие | Бухгалтерия | Текущие |
| Аварии / инциденты экологические | Внутренний registry | За последние 3 года |
| Ответственность по ст.143 УК (охрана труда) | Public + GC | Уголовные дела руководства |

## Workflow

### Шаг 1. Scope confirmation

Из categories A-L — что в scope для данной DD? (Pre-LOI обычно focused —
B/C/D/J critical; full DD — все)

### Шаг 2. Document collection

- Из data room — все документы classified by category
- Из реестров (ЕГРЮЛ, kad.arbitr, ЕФРСБ, ЕГРН, Роспатент, РКН) — automated
  через MCP если available, manual otherwise

### Шаг 3. Issue extraction (per document)

Для каждого documenta:
- Category: A-L
- Issue identified: [конкретная findings]
- Risk severity: 🔴 critical / 🟡 medium / 🟢 minor / 🔵 informational
- Materiality: [сумма / impact в % от деала]
- Citation / source: [path + page]
- Recommended action: [pre-closing fix / representation & warranty / indemnity / price adjustment / walkaway]

### Шаг 4. Tabular output

```markdown
# DD Issues — [target name, ИНН XXX]
**Дата DD:** [DD.MM.YYYY]
**Scope:** [described]
**Reviewers:** [users]

## Critical issues (🔴)

| # | Category | Issue | Source | Materiality | Recommended action |
|---|----------|-------|--------|-------------|-------------------|
| 1 | B Tax | Открытая ВНП за 2023 г., ожидаемое доначисление ~50 млн руб (по протоколу осмотра) | Письмо ФНС от DD.MM, протокол осмотра №X | 50М руб (3% от deal value) | Pre-closing: получить решение ФНС; OR escrow 100% expected liability; OR specific indemnity uncapped |
| 2 | D Bankruptcy | Аффилированное лицо в банкротстве, подано заявление КДЛ против ГД target | ЕФРСБ + kad.arbitr A40-XXX/2024 | risk личной ответственности ~30M | Pre-closing: replace ГД; OR retain reps & warranties с indemnity |
| 3 | I ПДн | Утечка ПДн 200k records в 06.2025; штраф РКН 18 млн руб не уплачен | Внутр.incident log + предписание РКН | 18М штраф + 200M reputation impact | Spec.indemnity для штрафа + reps по 152-ФЗ status |

## Medium issues (🟡)

[Same table]

## Minor / informational (🟢 / 🔵)

[Same table]

## Summary

- **Total issues:** [N]
- **Critical:** [N] / **Medium:** [N] / **Minor:** [N]
- **Aggregate exposure (если quantifiable):** ~[сумма] млн руб
- **Deal-breakers:** [list if any]
- **Recommended path:**
  - [Proceed with current price / Reduce price by X / Restructure as asset deal /
     Walk away]
- **Required reps & warranties:** [topics]
- **Required indemnities:** [specific, uncapped if applicable]
- **Escrow recommendations:** [amount + release schedule]
```

### Шаг 5. Cross-skill integration

- `/material-contract-schedule` — для extract материальных договоров из DD
- `/closing-checklist` — для conditions precedent на основе DD findings
- `/integration-management` — для post-closing remediation плана
- `/deal-team-summary` — для distill DD к non-legal stakeholders

## РФ-specific красные флаги (always escalate)

- **Target в ЕФРСБ** (реестр банкротов) — STOP deal pending escalation
- **Уголовное дело УК ст.199 / ст.159 / ст.201 против бенефициара** — material exposure
- **Sanctioned бенефициар (US OFAC / EU / UK)** — sanctions exposure для acquirer
- **Иностранный недружественный акционер > 25%** — Указ Президента 81/2022, спецтребования к расчётам
- **Налоговый мониторинг exit / отзыв лицензии** — material consequence
- **Доминирующее положение target без ФАС согласования сделки** — required
- **Реестр участников ООО ведётся самой компанией (не через нотариусов в текущей редакции)** — нотариальное удостоверение долей с 2009 — все сделки с долями должны быть нотариальны

## Что НЕ делает

- Не делает final risk assessment — это outside-адв ФПА + deal team
- Не negotiates price adjustments — это деал team
- Не drafts reps & warranties — это transaction docs

## Attribution

Adapted from [`corporate-legal/diligence-issue-extraction`](https://github.com/anthropics/claude-for-legal/blob/main/corporate-legal/skills/diligence-issue-extraction/SKILL.md)
by Anthropic (Apache 2.0).

**Категория B:**
- Categories A-L полностью пересмотрены под РФ regulators (ФНС, kad.arbitr, ЕФРСБ, Росреестр, Роспатент, РКН, ФАС) — нет US equivalents
- Sanctions section добавлен — Counter-sanctions specific (РФ Указ 81/2022)
- 115-ФЗ бенефициары — нет US equivalent
- 152-ФЗ ПДн — нет US equivalent
- 422-ФЗ НПД переквалификация — РФ-specific risk
- Нотариус для долей ООО — РФ-specific требование (нет US LLC equivalent)

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
