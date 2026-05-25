---
name: pretensia-received
description: >
  Triage входящей претензии — extract поля, portfolio cross-check, merit
  assessment, 4 опции response (substantive / holding / settlement / ignore +
  preserve). Используй когда получили претензию от counterparty.
argument-hint: "[paste претензию или путь к docs]"
user_invocable: true
ported_from: litigation-legal/demand-received
ported_at: 2026-05-18
adaptation_category: B
---

# /pretensia-received (входящая претензия)

## Назначение

В РФ — получение претензии от counterparty запускает **30-дневный срок на ответ**
(АПК ст.4 ч.5). Если не отвечаем — counterparty может подать иск без preventiveными
ходатайствами.

## Workflow

### Шаг 1. Extract structured fields

Из претензии extract:

- **Sender:** ИНН, юр.лицо, контактное лицо
- **Date received:** DD.MM.YYYY (важно для 30-дневного срока!)
- **Method received:** заказное письмо / email / личное вручение (audit trail)
- **Basis:** какой договор / основание
- **Claims:**
  - Основной долг (если есть)
  - Проценты ст.395
  - Договорная неустойка
  - Убытки
  - Иные требования (расторжение, реальное исполнение, etc.)
- **Deadline для ответа:** [DD.MM.YYYY + 30 дней]

### Шаг 2. Portfolio cross-check

Read `_log.yaml` — есть ли:

- Existing matter с этим counterparty?
- Existing matter с этим договором?

Если **да** — link к existing matter (это update, не new intake).

Если **нет** — это **new matter**, recommend `/litigation:matter-intake`.

### Шаг 3. Merit assessment

Для каждого claim — evaluate:

| Параметр | Метод |
|----------|-------|
| **Юридически обоснован?** | Применимая статья ГК — действительно даёт право на это? |
| **Фактически достоверен?** | Соответствуют ли утверждения нашим documents? |
| **Расчёт correct?** | Math check |
| **Процедурные дефекты?** | Отправлена на правильный юр.адрес? Получена надлежащим лицом? |
| **Срок исковой давности (ст.196 ГК)?** | Не истёк ли 3-летний срок? |

Result:

- 🟢 **Strong claim** — нужно serious response
- 🟡 **Weak claim** — можно дискутировать
- 🔴 **Frivolous claim** — почти точно проигрышное для них

### Шаг 4. Strategic options

#### Option 1: Substantive response (договариваемся)

Если merit medium-strong и хотим settle:

- Acknowledge получение
- Принимаем некоторые требования / оспариваем другие
- Предлагаем compromise

**Когда применять:** ongoing relationship с counterparty, экономика подсказывает
settle.

#### Option 2: Holding response (выигрываем время)

Acknowledge получение, prosим дополнительные документы, дополнительное время на
review.

**Когда применять:** нужно больше времени для evaluation, но 30-дневный срок
истекает.

**Важно:** РФ суды не очень принимают "holding response" — counterparty может
сразу пойти в суд. Use carefully.

#### Option 3: Settlement offer

Если merit strong, predлагаем urgent settlement.

#### Option 4: Ignore + preservation

Если claim frivolous + relationship уже broken — игнорируем (counterparty всё равно
может подать иск, и мы готовы defending).

**Caveat:** ignore = окончательное закрытие door на settling. Часто плохая идея даже
для frivolous claims (показывает не reasonable side).

### Шаг 5. Draft response (если выбрали Option 1, 2, 3)

#### Acknowledge + request more info (Option 2 holding):

```markdown
[Адресат]

Уважаемые коллеги!

Подтверждаем получение Вашей досудебной претензии от [DD.MM.YYYY] № [N] (получена
нами [DD.MM.YYYY]).

В связи с необходимостью изучения изложенных в претензии обстоятельств и
расчётов, просим предоставить следующие документы / разъяснения:

1. [Что просим]
2. [Что просим]

После получения указанных документов нами будет дан substantive ответ в
разумный срок, но не позднее [date].

С уважением,
...
```

#### Substantive response (Option 1):

```markdown
[Адресат]

Уважаемые коллеги!

Рассмотрев Вашу досудебную претензию от [DD.MM.YYYY] № [N], направляем
содержательный ответ.

## Позиция по претензии

**По требованию 1 (основной долг X руб):**
[Признаём полностью / Признаём частично X из Y / Отклоняем]

Основания:
[Юр.аргументы со ссылками на ст. ГК + ваши documents]

**По требованию 2 (проценты по ст. 395):**
[...]

**По требованию 3 (неустойка):**
В случае удовлетворения требования о неустойке просим учесть несоразмерность
требуемой неустойки последствиям нарушения обязательства и снизить её на
основании ст. 333 ГК РФ.

## Предложение по урегулированию

[Compromise оффер — например "Готовы оплатить основной долг X руб + проценты по
ст.395 без договорной неустойки в течение 14 дней"]

С уважением,
...
```

### Шаг 6. Record + update

После отправки response:

- Save копию в `matters/[slug]/pretensia-response-[date].md`
- Update matter history (`/litigation:matter-update`)
- Set next deadline (отслеживать reaction counterparty)

### Шаг 7. If escalation

Если response = Option 4 (ignore) или counterparty responded негативно:

- Recommend `/litigation:matter-intake` для full intake если ещё не сделан
- Recommend `/litigation:legal-hold` для preservation документов
- Prep к иску — `/litigation:brief-section-drafter` для начала draft'а отзыва /
  встречного иска

---

## Critical РФ checks

### Юридический адрес и vrucenие

**Если претензия пришла не на наш юр.адрес из ЕГРЮЛ** — мы можем не обязаны
отвечать (counterparty не соблюл обязательный претензионный порядок). Verify через
`egrul-mcp`.

### 30-дневный срок

Срок начинается **с получения**, не с отправки. Documenting получение critical для
доказывания если counterparty подаст иск.

### Срок исковой давности

Ст.196 ГК — общий 3 года. Ст.197 — специальные сроки для определённых требований.

Если претензия по обязательству, по которому срок давности **уже истёк** — это
сильный аргумент для нас (можно not отвечать substantively, ссылаясь на пропуск
срока).

### Подписант с другой стороны

Verify что подписал претензию **уполномоченный** представитель counterparty:
- Руководитель организации (по ЕГРЮЛ)
- Представитель с действующей доверенностью
- Адвокат с ордером

Если претензия от неуполномоченного — ground для отклонения.

---

## Attribution

Adapted from [`litigation-legal/demand-received`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/demand-received/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:**
- "Demand received" → "досудебная претензия" (АПК ст.4)
- 4 опции response сохранены, content переписан под РФ
- РФ-specific checks: юр.адрес из ЕГРЮЛ, ст.196 исковой давности, ст.333 неустойка
- Подписант verification (ЕГРЮЛ / доверенность / адвокатский ордер)

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
