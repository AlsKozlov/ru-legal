---
name: portfolio
description: >
  Управление портфелем IP — tracking регистраций, сроков продления, пошлин,
  лицензионных договоров, споров. РФ specifics: ТЗ продление каждые 10 лет
  (ст.1491 ГК); патенты — ежегодные пошлины (с 3-го года); полезные модели —
  10 лет максимум; промобразцы — 5 + 4×5 продлений.
argument-hint: "[optional: section / type]"
user_invocable: true
ported_from: ip-legal/portfolio
ported_at: 2026-05-19
adaptation_category: A
---

# /portfolio

## Назначение

Tracking IP портфеля — что есть, когда что истекает / нужно платить / нужно
продлевать, кто infringes, кто лицензирует.

## Pre-flight

- PROFILE.md загружен — портфель registered IP
- Internal documentation IP available

## Workflow

### Шаг 1. Inventory current portfolio

```markdown
## Portfolio Snapshot — [DD.MM.YYYY]

### Товарные знаки

| # | № регистрации | Знак | Классы МКТУ | Дата подачи | Дата истечения | Status | Next action |
|---|---------------|------|-------------|-------------|----------------|--------|-------------|
| 1 | 555555 | "АЛЬФА" | 35, 42 | DD.MM.2015 | DD.MM.2025 → продлено до 2035 | Active | Following review 2034 |
| 2 | 666666 | "ALPHA" (latin) | 35 | DD.MM.2018 | DD.MM.2028 | Active | Maintenance |
| 3 | IR777777 | "Alpha" (Madrid) | 9, 42 | DD.MM.2019 | DD.MM.2029 | Active | (через WIPO) |

### Патенты (изобретения)

| # | № патента | Название | Дата приоритета | Срок действия | Пошлина | Status |
|---|-----------|----------|------------------|----------------|---------|--------|
| 1 | 9999999 | "Способ X" | DD.MM.2010 | до DD.MM.2030 | Уплачено за 2026 | Active |

### Полезные модели

| # | № | Название | Срок | Status |
|---|---|----------|------|--------|
| ... | | | | |

### Промышленные образцы

| # | № | Название | Срок | Status |
|---|---|----------|------|--------|
| ... | | | | |

### Авторские произведения / ПО / БД (если зарегистрированы)

| # | № свидетельства | Объект | Дата регистрации | Status |
|---|------------------|--------|-------------------|--------|
| 1 | RU... | ПО "X" | DD.MM.2020 | Active в реестре Минцифры |

### Ноу-хау (с режимом КТ)

| # | Обозначение | Содержание | Положение о КТ | Доступ |
|---|--------------|------------|------------------|--------|
| 1 | KH-001 | Производственная технология | Положение от DD.MM | список |
```

### Шаг 2. Maintenance schedule

#### ТЗ — продление каждые 10 лет (ст.1491)

- Срок действия — 10 лет с даты подачи заявки
- Продление — за **6 месяцев до окончания + 6 мес "lapsed" period с дополнительной пошлиной**
- Пошлина продления — fix amount
- Подача через патентного поверенного recommended

→ Calendar entry: за 12 мес до expiration — review + decision о продлении.

#### Патенты — ежегодные пошлины

- За **3-й год** и далее — ежегодная пошлина
- Растёт каждый год (на 2026 в районе 1700-30000 руб в зависимости от года жизни патента)
- Срок действия: **20 лет** для изобретения, **10 лет** для полезной модели, **5 + 5 + 5 + 5 + 5 = max 25 лет** для промобразца

→ Calendar entry для каждого патента: дата уплаты пошлины + 6 мес buffer.

#### Зарубежные filings

- PCT — национальные фазы (Дата приоритета + 30/31 мес)
- Мадридская система — продление through WIPO

### Шаг 3. Action items

```markdown
## Upcoming actions (next 12 months)

| Date | IP | Action | Owner | Status |
|------|-----|--------|-------|--------|
| [DD.MM.YYYY] | ТЗ № 555555 | Продление (10-year anniversary) | Outside patent attorney | Pending |
| [DD.MM.YYYY] | Патент 9999999 | Пошлина за 17-й год | Finance / patent attorney | Pending |
| [DD.MM.YYYY] | Заявка № 888888 | Ответ на запрос ФИПС | Patent attorney | In progress |
| [DD.MM.YYYY] | Лицензионный договор с X | Review + продление? | Legal team | Pending |
```

### Шаг 4. Licensing portfolio

```markdown
### Licensing in (где мы — лицензиат)

| # | Лицензиар | Object | Type | Срок | Royalty | CoC clause | Active disputes |
|---|-----------|--------|------|------|---------|-------------|-------------------|
| 1 | Microsoft | Win Server (enterprise) | Неискл | до 2026 | $50k/y | termination on CoC | None |

### Licensing out (где мы — лицензиар)

| # | Лицензиат | Object | Type | Срок | Royalty receivable | Quality control | Quality issues |
|---|-----------|--------|------|------|---------------------|------------------|------------------|
| 1 | ООО "Альфа" | ТЗ "АЛЬФА" в кл.35 | Неискл | до 2027 | 5% от revenue | Annually | None |
```

### Шаг 5. Active disputes / monitoring

```markdown
### Open IP matters

| # | Тип | Сторона | Объект | Status | Materiality | Next milestone |
|---|-----|---------|--------|--------|-------------|------------------|
| 1 | Infringement (we as plaintiff) | ООО "Подделка" | ТЗ 555555 | СИП первая инстанция | 2M компенсация | Заседание DD.MM.YYYY |
| 2 | Opposition (we as opposer) | Заявитель X | Заявка на сходный знак | Палата по патентным спорам | rejection sought | Заседание DD.MM.YYYY |
| 3 | Лицензионный спор | ООО "Лицензиат" | Royalty просрочка | Pre-litigation | 500k overdue | C&D sent |
```

### Шаг 6. Annual portfolio review

#### Activities

- [ ] Inventory complete (см. Step 1)
- [ ] All maintenance fees scheduled (Step 2)
- [ ] Lapsed registrations reviewed — restore worth it?
- [ ] Underutilized IP — divest / license to third parties?
- [ ] Strategic gaps — what new IP should we file?
- [ ] Competitive intelligence — what are competitors filing?

#### Strategic decisions

```markdown
## Strategic recommendations

### File new

- [ ] ТЗ in Class X (new product launch)
- [ ] Patent on innovation Y (filed Q4 by patent attorney)

### Drop / lapse

- [ ] ТЗ 333333 — no longer commercial relevance; let lapse 2027
- [ ] Patent 222222 — superseded by newer technology; not pay annual fee

### Defensive

- [ ] Опубликовать defensively → блокирует patents конкурентов but not ours

### License out

- [ ] ТЗ "АЛЬФА-PRO" — стороннее использование для дополнительной revenue stream
```

### Шаг 7. Output

```markdown
# IP Portfolio Status — [DD.MM.YYYY]

## Summary

- **Total registrations:** [N]
  - ТЗ: [N] active / [N] pending
  - Патенты: [N] active / [N] pending
  - ПО / БД: [N] registered
  - Ноу-хау: [N] documented under режим КТ
- **Active licenses (in):** [N]
- **Active licenses (out):** [N]
- **Open disputes:** [N]

## Upcoming actions (90 days)

[List]

## Strategic recommendations

[From Step 6]

## Budget forecast

- Maintenance fees: [сумма / year]
- Outside patent attorney costs: [сумма / year]
- New filings (planned): [сумма]
- Litigation reserves: [сумма]
```

## Что НЕ делает

- Не подаёт maintenance fees (это финансы)
- Не handles direct interactions с Роспатент (это патентный поверенный)
- Не negotiates licenses (это business + outside-адв)

## Attribution

Adapted from [`ip-legal/portfolio`](https://github.com/anthropics/claude-for-legal/blob/main/ip-legal/skills/portfolio/SKILL.md) by Anthropic (Apache 2.0).

**Категория A:**
- Portfolio template universal
- Maintenance schedule — РФ specifics (ТЗ 10-year, patents annual с 3-го года, промобразец 5+5+5+5+5)
- ПО в реестре Минцифры — РФ-specific
- ст.1491 ГК — РФ ТЗ продление

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
