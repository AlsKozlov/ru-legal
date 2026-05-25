---
name: tabular-review
description: >
  Multi-document review с tabular output — для DD scenarios. Принимает batch
  documents (договоры, корпоративные документы, тендерная документация и т.п.),
  extracts predefined fields, returns structured table. Differs от
  /diligence-issue-extraction — focused per-document field extraction, не
  cross-document analysis.
argument-hint: "[path к directory с documents] [template type]"
user_invocable: true
ported_from: corporate-legal/tabular-review
ported_at: 2026-05-19
adaptation_category: B
---

# /tabular-review

## Назначение

Batch review множества однотипных documents — extract structured fields в
таблицу. Common use cases:
- 50 contracts → review change-of-control + assignment clauses
- 30 ТД ключевых сотрудников → review key terms
- 20 договоров аренды → срок, индексация, расторжение
- 100 лицензионных договоров → срок, royalty, territory

Output — таблица для дальнейшего анализа.

## Pre-flight

- **Document type clear** — все документы одного типа (если mixed — split per type first)
- **Fields list** определён (см. templates ниже или custom)
- **Materiality filter** установлен — если > N документов, может applied (например, только > 5М руб)

## Workflow

### Шаг 1. Choose template

| Template | Use case | Fields |
|----------|----------|--------|
| `contracts-coc` | Review change-of-control / assignment | Стороны, сумма, срок, CoC clause, assignment, terminat. on CoC |
| `employment-key-terms` | DD по labor | ФИО, должность, дата приёма, оклад, срок, испытание, non-compete, severance |
| `leases` | Аренда недвижимости | Объект, арендодатель, площадь, ставка, индексация, срок, право продления, штрафы |
| `licenses` | IP/Tech licenses | Тип лицензии, scope, territory, term, royalty, exclusivity, terminat. rights |
| `loans` | Кредитные договоры | Кредитор, сумма, ставка, срок, обеспечение, ковенанты, default events |
| `litigation` | Открытые споры | Номер дела, суд, стороны, предмет, сумма, status, риск проигрыша |
| `custom` | Ad-hoc — user задаёт fields | — |

### Шаг 2. Apply field extraction per document

Для каждого документа:

1. **Identify** что это (если template fits — proceed; иначе flag)
2. **Extract** required fields из текста
3. **Compute derived fields** (если нужно — например, "% от annual revenue")
4. **Flag missing fields** (если в документе нет — flag "MISSING")
5. **Risk classification** (если template includes — определяет 🔴🟡🟢🔵)

### Шаг 3. Tabular output

```markdown
# Tabular Review — [template name]

**Documents reviewed:** [N]
**Date:** [DD.MM.YYYY]
**Reviewer:** [user]

## Table

| # | Документ | Поле 1 | Поле 2 | Поле 3 | ... | Risk |
|---|----------|--------|--------|--------|-----|------|
| 1 | [filename] | ... | ... | ... | ... | 🟢 |
| 2 | [filename] | ... | ... | ... | ... | 🔴 |
| ... | | | | | | |

## Aggregates

- **Total document count:** [N]
- **By risk:** 🔴 [n] / 🟡 [m] / 🟢 [k] / 🔵 [j]
- **By [key field if relevant]:** ...

## Flagged issues

[Documents где extraction failed / abnormalities found / risk 🔴]

1. [doc X] — issue
2. ...

## Next steps

- Drill-down to issued documents with `/diligence-issue-extraction` для detailed analysis
- Build summary for deal team with `/deal-team-summary`
```

## Templates (РФ-adapted)

### Template: contracts-coc

For DD по material contracts — change-of-control / assignment review.

| Поле | Что extract |
|------|-------------|
| Документ | filename |
| Контрагент | название + ИНН (если есть) |
| Тип договора | поставка / услуги / аренда / NDA / etc. |
| Дата | дата заключения |
| Срок | конкретная дата окончания / бессрочный |
| Сумма / value | annual / total |
| Change-of-control clause | Есть / нет; если есть — текст |
| Assignment restriction | Есть / нет; consent required? |
| Termination upon CoC | Right to terminate? Срок уведомления? |
| Risk | 🔴 если CoC = automatic terminat. с key vendor; 🟡 если consent required но likely OK; 🟢 если silent или standard |

### Template: employment-key-terms

For DD по labor portfolio.

| Поле | Что extract |
|------|-------------|
| Документ | filename |
| ФИО | работник |
| Должность | согласно ТД |
| Дата приёма | DD.MM.YYYY |
| Оклад | руб/мес |
| Премии | структура |
| Срок ТД | бессрочный / срочный (если срочный — основание ст.59) |
| Испытание | срок (max 3 мес обычно; 6 для топ-менеджеров) |
| Non-compete | есть? (в РФ unenforceable post-termination) |
| КТ обязательства | есть положение о КТ + договор? |
| IP assignment | ст.1295 ГК (служ.произведение) явно урегулирован? |
| Severance baseline | если есть |
| Risk | 🔴 если ст.59 violation (срочный без grounds) / non-compete enforceable claim / ст.57 missing terms |

### Template: leases

For DD по аренда портфелю.

| Поле | Что extract |
|------|-------------|
| Документ | filename |
| Объект | адрес + площадь |
| Арендодатель | название + ИНН |
| Кадастровый № | (если есть) |
| Срок | дата начала, дата окончания |
| Регистрация ЕГРН | если ≥ 1 года — должна быть зарегистрирована (ст.609 п.2 ГК) |
| Арендная плата | руб/мес |
| Индексация | формула / % per annum |
| Расторжение по инициативе арендодателя | условия |
| Расторжение по инициативе арендатора | условия |
| Преимущественное право продления | ст.621 ГК — по умолчанию есть |
| Штрафы / неустойки | формулы |
| Risk | 🔴 не зарегистрирован > 1 года; 🟡 close to expiration без renewal; 🟢 standard |

### Template: licenses (IP)

| Поле | Что extract |
|------|-------------|
| Документ | filename |
| Лицензиар | |
| Лицензиат | |
| Объект | (товарный знак / изобретение / ПО / БД / know-how) |
| № регистрации (если применимо — Роспатент) | |
| Тип | исключительная / неисключительная |
| Территория | |
| Срок | |
| Royalty | формула |
| Sublicensing | разрешено? |
| Termination | events |
| Регистрация в Роспатенте | обязательно для исключительных лицензий и для регистрируемых объектов (ст.1232 ГК + 1235) |
| Risk | 🔴 исключительная лицензия не зарегистрирована (cм.1232) → недействительна для третьих лиц |

### Template: loans

| Поле | Что extract |
|------|-------------|
| Документ | filename |
| Кредитор | |
| Сумма | |
| Валюта | RUB / USD / EUR / другая |
| Ставка | % per annum, fix / float |
| Срок | дата выдачи, дата возврата |
| Обеспечение | залог / поручительство / иное |
| Ковенанты — финансовые | формулы (debt/EBITDA, и т.п.) |
| Ковенанты — иные | (change-of-control restriction; new debt restriction; etc.) |
| Cross-default | trigger from other agreements |
| Прекращение по дефолту | events of default list |
| Currency risk (для FX loans) | hedged? |
| Risk | 🔴 cross-default tied to M&A; 🟡 covenants tight; 🟢 standard |

### Template: litigation

| Поле | Что extract |
|------|-------------|
| Документ | filename / case ref |
| № дела (kad.arbitr / суды ОЮ) | A40-XXX/YYYY |
| Суд | АС / СОЮ / СОЮ субъекта |
| Стороны | истец vs ответчик |
| Target роль | истец / ответчик |
| Предмет иска | |
| Сумма иска | руб |
| Дата подачи | |
| Текущая стадия | первая / апелляция / кассация / надзор |
| Дата ближайшего заседания | |
| Probability proigrysha (для target as ответчик) | high / med / low |
| Materiality | в % от деала value |
| Adequacy резерва (по бух.отчётности) | сформирован ли |
| Risk | 🔴 high probability + material; 🟡 med + material или high + immaterial; 🟢 low risk |

## Custom template

User задаёт fields:

```
> Какие fields extract?

> 1. Контрагент
> 2. Сумма
> 3. Срок
> 4. ст.452 досудебная претензия — какой срок указан?
> 5. Forum для споров (АС какой?)

> Хорошо. Process [N] documents в этой directory? [Y/N]
```

## Что НЕ делает

- Не делает cross-document analysis — это `/diligence-issue-extraction`
- Не делает legal opinion — это outside-адв
- Не negotiates contract terms

## Attribution

Adapted from [`corporate-legal/tabular-review`](https://github.com/anthropics/claude-for-legal/blob/main/corporate-legal/skills/tabular-review/SKILL.md)
by Anthropic (Apache 2.0).

**Категория B:**
- Templates пересмотрены под РФ contracts (ст.609 регистрация аренды > 1 года; ст.1232 регистрация исключительных лицензий; ст.59 срочный ТД grounds; ст.621 преимущ. право продления)
- Litigation template — kad.arbitr / суды ОЮ структура (vs US federal/state)
- Loans template — FX hedging post-2022 sanctions
- IP licenses — Роспатент регистрация specifics

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
