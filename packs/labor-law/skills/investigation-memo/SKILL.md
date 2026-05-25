---
name: investigation-memo
description: >
  Draft legal memo по результатам внутреннего расследования. РФ specifics:
  privilege ТОЛЬКО через outside-адв ФПА; дисциплинарка по ст.193 ТК (объяснение,
  сроки); стандарт доказывания "balance of probabilities" для внутренних целей,
  но "обоснованность" для оспаривания в суде. Recommended action: какое
  взыскание / какой алгоритм для оформления.
argument-hint: "[matter-id]"
user_invocable: true
ported_from: employment-legal/investigation-memo
ported_at: 2026-05-18
adaptation_category: B
---

# /investigation-memo

## Назначение

Generate formal legal memo по результатам investigation. Final analytical document:
- Findings of fact
- Legal analysis (ТК + sectoral / contractual)
- Conclusions
- Recommended action
- Implementation steps

## Pre-flight критичные РФ checks

### A. Privilege

**Memo может быть НЕ privileged в РФ если drafted in-house.** Чтобы получить
адвокатскую тайну:
1. Memo должен быть запрошен адвокатом ФПА (с ордером)
2. Drafted адвокатом ФПА или под его руководством с привлечением как соавтора
3. Stored в адвокатском досье

**Without outside-адв involvement** — memo защищён только commercial-confidentiality
(98-ФЗ режим КТ) — that's NOT privilege в legal sense.

**Header strategy:**

| Privilege framing | Header |
|-------------------|--------|
| Privileged (outside-адв ФПА involved) | "ПРИВИЛЕГИРОВАННЫЙ ДОКУМЕНТ. Адвокатская тайна (ФЗ-63 ст.8). Запрос: адв. [ФИО], удост. №, ордер №" |
| Confidential business | "СЛУЖЕБНАЯ ТАЙНА. Режим коммерческой тайны (98-ФЗ). Не для распространения" |

**Никогда** не label memo "Privileged" если outside-адв ФПА не involved — это
misleading и не daст privilege в РФ суде.

### B. Дисциплинарка timing (ст.192-193 ТК)

Если recommended action — дисциплинарное взыскание:
- 1 месяц со дня обнаружения проступка (исключая болезнь / отпуск / время на учёт мнения профсоюза)
- 6 месяцев со дня совершения (2 года для финансовых нарушений)
- Объяснение работника **обязательно** запрошено в письменной форме
- 2 раб.дня на ответ; если не дал → составить акт об отказе
- Приказ с описанием проступка + ознакомление под подпись (3 раб.дня)

Memo должен **explicitly** address эти timing requirements.

### C. Категории взысканий (ст.192 ТК)

ТК предусматривает **только 3 вида** дисциплинарного взыскания:
1. **Замечание** (мягкое, без существенных последствий)
2. **Выговор** (средняя тяжесть)
3. **Увольнение** по ст.81 п.5 ТК (неоднократное) или п.6 (грубое нарушение)

**Не предусмотрены ТК (и поэтому незаконны как дисциплинарное):**
- Штраф / удержание из зарплаты (есть ст.137 ТК для материального ущерба — отдельно)
- "Строгий выговор" (есть только в специальных законах — военные, госслужащие)
- Перевод на нижеоплачиваемую должность (только по ст.72.1 с согласия)
- Лишение премии — **можно** если положением об оплате предусмотрена depremation

## Workflow

### Шаг 1. Read materials

- `intake.md`, `facts.md`, all `interviews/`, evidence index
- Existing `/investigation-query` outputs (если saved)

### Шаг 2. Structure memo

```markdown
# МЕМОРАНДУМ

**[ПРИВИЛЕГИРОВАННЫЙ ДОКУМЕНТ. Адвокатская тайна / СЛУЖЕБНАЯ ТАЙНА]**

**Дата:** [DD.MM.YYYY]
**От:** [ФИО, должность]
**Кому:** [ФИО, должность — обычно CEO / GC / HR Director]
**Тема:** Расследование [matter-id] — [короткое название]

---

## 1. Резюме

[3-5 предложений: что случилось, основной finding, recommended action]

## 2. Фактические обстоятельства

### 2.1. Background

[role subject, длительность работы, обязанности]

### 2.2. Триггер / обнаружение

- **Дата обнаружения проступка:** [DD.MM.YYYY] (ст.193 — 1-мес clock starts here)
- **Дата совершения:** [DD.MM.YYYY] (ст.193 — 6-мес clock starts here)
- **Источник:** [жалоба / докладная / audit alert]

### 2.3. Установленные факты

| # | Факт | Дата | Источник | Достоверность |
|---|------|------|----------|---------------|
| 1 | ... | ... | interview / документ / запись | high / medium / low |
| 2 | ... | ... | ... | ... |

### 2.4. Что НЕ удалось установить

[scope limitations — what evidence not available, what witnesses не доступны]

## 3. Правовой анализ

### 3.1. Применимые нормы

- **ТК:** [ст.X — основание / процедура]
- **ЛНПА компании:** [правила трудового распорядка п.X, должн.инструкция п.X]
- **Договор:** [п.X трудового / коллективного]

### 3.2. Квалификация поведения

**Является ли действие/бездействие нарушением?**

[Анализ — почему да / нет. Если да — какое именно нарушение (ТК / ЛНПА), какой
тяжести.]

### 3.3. Сроки (ст.193 ТК) — критично

- **1 мес со дня обнаружения:** истекает [DD.MM.YYYY] — осталось X дней
- **6 мес со дня совершения:** истекает [DD.MM.YYYY] — осталось X дней
- **Объяснение работника:** запрошено [DD.MM.YYYY] / получено [DD.MM.YYYY] /
  отказ — акт от [DD.MM.YYYY]
- **Учёт мнения профсоюза (если применимо):** запрошено / получено / срок истёк

**Вывод по срокам:** [процедура соблюдена / нарушена / под угрозой]

### 3.4. Аналогичные случаи / прецеденты

[Если в компании были аналогичные нарушения — как разрешались? Принцип равного
отношения важен для risk assessment.]

### 3.5. Risk assessment

| Сценарий | Probability | Impact | Mitigation |
|----------|-------------|--------|------------|
| Работник оспаривает в суд | [%] | восстановление + СЗП за вынужденный прогул | Соблюдение процедуры; готовность к compromise |
| Жалоба в ГИТ / прокуратуру | [%] | штрафы (КоАП ст.5.27), предписание | Документация полная |
| Профсоюз obstruction | [%] | Затягивание процедуры | Заранее запросить мнение |
| Negative PR / reputation | [%] | Talent retention | NDA conditions в releaseагрreement |

## 4. Выводы

1. [Finding 1 — на основании evidence X]
2. [Finding 2 — ...]
3. [Substantiated / unsubstantiated / inconclusive]

## 5. Рекомендации

### 5.1. Recommended action

**Вариант A (recommended):** [е.g. соглашение сторон ст.78 ТК с компенсацией X
окладов]

- Pros: [нет risk восстановления, controllable timing]
- Cons: [cost]

**Вариант B:** [е.g. выговор + последующее наблюдение]

- Pros: [низкая cost, рабочее место сохраняется]
- Cons: [возможны повторные эпизоды, escalation]

**Вариант C:** [е.g. увольнение по ст.81 п.5 / п.6]

- Pros: [removes risk]
- Cons: [высокий litigation risk если процедура не идеальна]

### 5.2. Implementation steps (для recommended action)

#### Если соглашение сторон (вариант A):

1. Draft соглашение с компенсацией [сумма] (см. attachment 1)
2. Negotiate с работником (один-на-один, в присутствии HR)
3. Подписать соглашение + приказ
4. Расчёт в день увольнения (ст.140 ТК)
5. Trudovaya books + НДФЛ отчётность

#### Если дисциплинарное взыскание:

1. До [DD.MM.YYYY] — запросить письменное объяснение (если не запрошено)
2. По истечении 2 раб.дней — составить акт об отказе (если без ответа)
3. Подготовить приказ с детальным описанием проступка + ТК ст.X
4. Учёт мнения профсоюза (если член, до 7 раб.дней — ст.373)
5. Ознакомить под подпись (3 раб.дня — ст.193)
6. Сохранить все docs в кадровое дело

## 6. Открытые вопросы

- [ ] [outstanding issue 1]
- [ ] [outstanding issue 2]

## Приложения

1. [Draft приказа / соглашения]
2. [Список evidence]
3. [Timeline]

---

[ФИО, должность]
[Подпись]
[Дата]
```

### Шаг 3. Review checklist перед finalize

- [ ] Privilege header корректный для context
- [ ] Все findings подтверждены ссылками на evidence
- [ ] Сроки ст.193 точно calculated
- [ ] Объяснение work обработано (получено / акт об отказе)
- [ ] Recommended action в рамках ст.192 ТК (3 вида взысканий)
- [ ] Risk assessment realistic (РФ суды pro-работника 65-80%)
- [ ] Implementation checklist конкретный и dated
- [ ] No conclusory legal opinions без analytical support

## Что НЕ делает

- Не оформляет приказ / соглашение (это HR / outside-адв drafts)
- Не replaces outside-адв advice для high-risk matters
- Не делает employment decision — это management

## Attribution

Adapted from [`employment-legal/investigation-memo`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/investigation-memo/SKILL.md)
by Anthropic (Apache 2.0).

**Категория B (medium adaptation):**
- Privilege analysis adapt — РФ in-house counsel НЕ privileged (US ACP отличается fundamental)
- Дисциплинарка procedural framework заменён US framework — ст.192-193 ТК
- 3 категории взысканий по ТК (vs US flexible discipline framework)
- Risk assessment пересчитан с realistic РФ статистикой (pro-работника суд)
- Аналогичные случаи — РФ "equal treatment" принцип критичен

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
