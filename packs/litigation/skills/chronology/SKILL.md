---
name: chronology
description: >
  Извлечь события из документов matter'а → de-dupe → significance tag (🔴/🟡/⚪) →
  output в working / SOF (statement of facts) / witness-specific форматах. Используй
  когда пользователь говорит "построй хронологию по [matter]", "что произошло в
  деле X с T1 по T2", "chronology для witness Y", или готовишься к hearing /
  brief'у.
argument-hint: "<slug> [--format working|sof|witness] [--witness <name>]"
user_invocable: true
ported_from: litigation-legal/chronology
ported_at: 2026-05-18
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /chronology (хронология событий)

## Назначение

Litigation требует accurate chronology — какое событие когда, в каком порядке,
кто был свидетелем. Этот skill извлекает события из docs и строит chronology в
нужном формате.

## Workflow

### Шаг 1. Load matter

Прочитай:
- `matter.md`, `history.md` (если есть)
- Перечисленные attached docs

Если documents не указаны — спроси: "Откуда извлекать события? Дай paths к
documents или ссылку на matter folder."

### Шаг 2. Extract events

Из каждого document извлеки события:

```yaml
events:
  - date: 2024-03-15
    description: "Подписан Договор поставки № 42 между сторонами"
    source: "contract-42.pdf, стр. 1"
    actors: ["ООО Истец", "ООО Ответчик"]
    type: contract-signed
  - date: 2024-06-01
    description: "Поставлена партия товара по накладной № 100"
    source: "shipping-100.pdf"
    actors: ["ООО Истец"]
    witnesses: ["Иванов И.И. — менеджер логистики"]
    type: performance
  - date: 2024-07-15
    description: "Отправлена досудебная претензия"
    source: "pretensia-2024-07-15.docx"
    type: pretensia-sent
```

Категории event types:
- `contract-signed`, `amendment-signed`
- `performance`, `non-performance`
- `payment-made`, `payment-overdue`
- `notice-sent`, `notice-received`
- `pretensia-sent`, `pretensia-received`, `pretensia-response`
- `claim-filed`, `hearing-held`
- `decision-issued`, `appeal-filed`
- `settlement-offer`, `settlement-signed`
- `regulatory-event` (РКН проверка, акт ВНП, КоАП protocol)

### Шаг 3. De-duplicate

Если одно событие в нескольких документах — merge с consolidated source.

### Шаг 4. Significance tagging

| Tag | Когда |
|-----|-------|
| 🔴 Critical | Material для исхода — formation, breach, mitigation, damages calculations |
| 🟡 Important | Context для critical events |
| ⚪ Background | Useful background, low impact |

### Шаг 5. Format output

#### Working format (для внутренней работы)

```markdown
# Chronology — [Matter name] (working)

| Дата | Sig | Событие | Источник | Свидетели |
|------|:---:|---------|----------|-----------|
| 15.03.2024 | 🔴 | Подписан Договор № 42 | contract-42.pdf | Иванов |
| 01.06.2024 | 🔴 | Поставка по накладной № 100 | shipping-100.pdf | Петров, Сидоров |
| 10.07.2024 | 🟡 | Уведомление о просрочке оплаты | email-2024-07-10.pdf | Иванов |
| 15.07.2024 | 🔴 | Отправлена досудебная претензия | pretensia.docx | — |
| ... | | | | |
```

#### SOF format (Statement of Facts для иска / отзыва)

Plain narrative, без таблицы:

```markdown
# Statement of Facts — [Matter name]

15 марта 2024 года между ООО Истец и ООО Ответчик был заключён договор поставки №
42, в соответствии с которым Истец принял на себя обязательство поставлять
товар, а Ответчик — принимать и оплачивать поставленный товар (Договор № 42, стр.
1).

1 июня 2024 года Истец осуществил поставку партии товара на основании накладной №
100 (накладная № 100, акт приёма-передачи от 01.06.2024).

После 30 дней с момента поставки оплата не поступила. 10 июля 2024 года Истец
направил Ответчику уведомление о просрочке оплаты (email от 10.07.2024).

15 июля 2024 года Истец направил досудебную претензию в соответствии с АПК РФ
ст.4 (досудебная претензия от 15.07.2024, копия с отметкой получения).

[... продолжение ...]
```

#### Witness-specific format

Фильтр событий по witness:

```markdown
# Chronology — [Witness name] для [Matter name]

События, в которых [Witness] участвовал или о которых он/она имеет первичную
информацию:

| Дата | Событие | Знание witness'а |
|------|---------|------------------|
| 01.06.2024 | Поставка по накладной № 100 | Менеджер логистики, организовал отгрузку |
| ... | | |
```

### Шаг 6. Output to file

Сохрани:
- `matters/[slug]/chronology-working-[YYYY-MM-DD].md`
- `matters/[slug]/chronology-sof-[YYYY-MM-DD].md` (если SOF)
- `matters/[slug]/chronology-witness-[name].md` (если witness)

---

## Quality checks

Перед output'ом:

- [ ] Все даты в одном формате (DD.MM.YYYY)
- [ ] Все источники — конкретные docs (не "memory"), с page references если возможно
- [ ] Witnesses identified правильно
- [ ] Critical events помечены 🔴
- [ ] Cross-reference: каждый event имеет source — никаких "по словам attorney"
      без supporting doc

---

## Что НЕ делает

- Не оценивает legal significance событий (только factual)
- Не fабрикует события (если нет в docs — не добавляет)
- Не интерпретирует ambiguous документы — флагнёт [неясно — verify]

---

## Attribution

Adapted from [`litigation-legal/chronology`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/chronology/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:**
- Event types расширены для РФ (досудебка ст.452, регуляторные события РКН/ФАС/НК)
- SOF format следует структуре РФ исков (даты + ссылки на ст. НПА если применимо)
- АПК ст.4 досудебка явно упомянута

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## Disclaimer

Chronology — factual extraction. Не legal advice о significance событий. Significance
tags — preliminary, verifier — lead attorney.

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
