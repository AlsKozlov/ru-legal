---
name: lease-residential
description: >
  Review договора найма / коммерческой аренды residential — apартмент / дом /
  доли. РФ specifics: ГК ст.671-688 (наём — civil); ЖК (для социального найма);
  обязательная регистрация для срока > 1 года; защита прав нанимателя (ст.687
  расторжение); налоговый агент по НДФЛ для landlord-физ.лица; самозанятый
  landlord (НПД 4%) opcion.
argument-hint: "[path к договору]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /lease-residential

## Назначение

Review residential lease для:
- Жильцы (tenants)
- Landlords
- Property management firms

## Two main types

### Тип 1: Договор найма жилого помещения (ст.671 ГК)

Most common для landlord-физ.лицо ↔ tenant-физ.лицо.

### Тип 2: Договор аренды (ст.606 ГК)

Если landlord или tenant — юр.лицо. Different framework (general lease law).

→ Always confirm правильный тип в начале.

## Workflow

### Шаг 1. Verify landlord rights

```markdown
- [ ] Выписка ЕГРН — кто собственник
- [ ] Если несколько собственников — согласие всех
- [ ] Если физ.лицо в браке — согласие супруга
- [ ] Если несовершеннолетние сособственники — согласие органа опеки
- [ ] Если ипотека — согласие банка-залогодержателя
```

### Шаг 2. Verify object

```markdown
- [ ] Адрес match
- [ ] Площадь match
- [ ] Состояние документировано (акт приёма с photo recommended)
- [ ] Имущество описано (мебель / техника)
- [ ] Доступ + ключи
```

### Шаг 3. Critical clauses

#### A. Срок

```markdown
- **Срок найма:** [...]
- **Default по ГК** — 5 лет максимум для найма (ст.683)
- **Краткосрочный наём** — до 1 года (different rules — ст.683 ч.2)
- **Регистрация в ЕГРН (ст.609):** обязательна для срока > 1 года

⚠ Common workaround — 11 мес с автоматическим продлением — НЕ trigger regulation
```

#### B. Плата

```markdown
- **Ежемесячная плата:** [сумма]
- **Когда платить:** до какого числа
- **Кому платить:** реквизиты / нал / mobile (платёжный сервис)
- **Индексация:** обычно нет в residential лучше fixed
- **Что включено:** только rent / + коммуналка / + интернет / etc.
- **Что не включено:** typically electricity meter
- **Late fee / penalty:** должно быть reasonable
```

#### C. Security deposit / залог

```markdown
- **Сумма** (typically 1 mes rent)
- **Возврат** при окончании если no damages
- **Хранение** — в чьих руках (landlord)
- **Может ли быть applied к последнему месяцу?** — yes if mutual agreement
```

#### D. Use + restrictions

```markdown
- [ ] Кто будет жить (только tenants заявленные? subletting allowed?)
- [ ] Регистрация по месту жительства (постоянная / временная)
- [ ] Pets allowed? Restrictions
- [ ] Smoking
- [ ] Hours / noise
- [ ] Гости — restrictions
- [ ] Alterations — изменения квартиры
```

#### E. Maintenance + repair

```markdown
ГК ст.681 default для найма:
- Текущий ремонт + текущая эксплуатация — tenant
- Капитальный ремонт — landlord

Договор может modify:
- [ ] Replacement техники — кто несёт
- [ ] Покраска / косметика
- [ ] Сантехника / электрика выход из строя
- [ ] Шумоизоляция improvements
```

#### F. Termination

```markdown
### Защита нанимателя (ст.687 ГК)

Наниматель имеет **сильную защиту**:

- **Право расторгнуть** наниматель в любое время с уведомлением **3 мес**
- **Landlord** — only через суд по limited grounds (например, неуплата > 6 мес для long-term)
- При расторжении судом — наниматель + сожители могут быть выселены **с отсрочкой до 1 года**

### Краткосрочный наём (< 1 года)

- Меньше защиты (ст.683 ч.2)
- Landlord может расторгнуть проще

[ ] Договор не пытается обойти ст.687 защиты
[ ] Notice periods adequately specified
```

#### G. Регистрация по месту жительства (прописка)

```markdown
- Tenant может потребовать **временную регистрацию** (постоянную — только если landlord согласен)
- Landlord должен уведомить МВД о проживании non-резидентов / иностранцев
- Без registration tenant имеет administrative проблемы (бесплатная медицина, школа детей и т.д.)

[ ] Условие о registration в договоре — Y/N
[ ] Если N — это significant disadvantage для tenant
```

### Шаг 4. Taxes для landlord-физ.лица

**3 основных option:**

| Option | Налог | Pros | Cons |
|--------|-------|------|------|
| **НДФЛ 13/15%** | На rent income | Default — without doing anything | Нужно подать декларацию + сам платить; высокая ставка |
| **НПД 4% / 6%** (самозанятый) | На rent income | Low rate; simplicity | Лимит 2.4M / год; не для apartments если business use |
| **ИП на УСН 6%** | На rent income | Деduct expenses; lower than НДФЛ | Бухгалтерия требует |

→ Recommend НПД для long-term residential rental — most efficient.

→ Cross-reference `tax-law/tax-system-choice` если landlord — наш client.

### Шаг 5. Disputes typical patterns

#### Pattern 1: Landlord удерживает security deposit без основания

- Tenant может pursue в суде
- Burden of proof на landlord для documenting damages

#### Pattern 2: Landlord prematurely terminates

- Если в нарушение ст.687 (long-term) — tenant может оспорить + получить compensation
- Защита очень сильная

#### Pattern 3: Quality issues

- Tenant имеет права по ст.681 + ЗЗПП (если landlord — ЮЛ или ИП)
- Возможны reduction арендной платы / compensation

#### Pattern 4: Unauthorized occupants

- Если subletting / гости постоянно проживают — landlord может potребовать прекращения
- Сложно proving + enforcing

### Шаг 6. Output

```markdown
# Residential Lease Review — [объект]

## Side: [tenant / landlord]

## Bottom line

[Sign / Sign with changes / Don't sign]

## Critical findings

[Per category выше]

## Term specifics

- Срок: [...]
- Plata: [...]
- Залог: [...]

## Negotiation points

1. [...]
2. ...

## Tax considerations (для landlord)

- Recommended режим: [НПД / ИП на УСН / НДФЛ]
- Estimated annual налог: [...]

## Risk summary

- [Risk 1]
- [Risk 2]
```

## Что НЕ делает

- Не handles регистрацию по месту жительства (МВД)
- Не делает property inspection (нужен в person с landlord / agent)
- Не replaces outside-адв ФПА для material матерей (rare для simple residential)

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
