---
name: legal-hold
description: >
  Обеспечение доказательств в РФ — issue / refresh / release / status. РФ-аналог
  US legal hold: обязательство сохранить documents для будущего иска или
  расследования. Применяется по АПК ст.72 (обеспечение доказательств арбитражным
  судом до подачи иска) или через внутренние preservation orders. Non-lawyer gate
  на issuance + release.
argument-hint: "<action: issue|refresh|release|status> [matter-slug]"
user_invocable: true
ported_from: litigation-legal/legal-hold
ported_at: 2026-05-18
adaptation_category: C
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /legal-hold (обеспечение доказательств)

## Назначение

В US — legal hold по FRCP 37(e) / ESI preservation. В РФ — **другая концепция**:

- **АПК ст.72** — обеспечение доказательств арбитражным судом до подачи иска (на
  basis заявления заинтересованного лица). Применяется когда есть угроза утраты
  доказательств.
- **Внутренние preservation orders** — приказы внутри компании о неудалении
  relevant документов. Договорная / административная мера, не процессуальная.
- **АПК ст.66 + ст.74** — истребование доказательств у других лиц (на этапе уже
  поданного иска).

Этот skill = **внутренний preservation order** для самой компании (не судебная
процедура).

## ⚠️ Non-lawyer gate

**Critical для РФ:** issuance / release legal hold — это **legal decision** с
последствиями.

Если PROFILE.md `## Кто пользуется → Роль` = Non-lawyer:

> "Issue / release preservation order требует подписи attorney (или DPO для ПДн
> данных). Подтверди:
> 1. Это decision согласован с GC / lead attorney?
> 2. Если release — есть assurance что matter resolved / lapsed?
>
> Если нет — pause и получи sign-off."

Не proceed без sign-off.

## Workflow

### Action: ISSUE

#### Шаг 1. Identify scope

- **Matter:** какой matter триггерит preservation?
- **Trigger event:**
  - Получена досудебная претензия
  - Подан иск против нас
  - Получен subpoena / запрос суда (АПК ст.66)
  - Запрос РКН / ФАС / ФНС / следователя
  - Reasonably anticipated litigation
- **Date of trigger:** [DD.MM.YYYY]

#### Шаг 2. Identify custodians

Кто из сотрудников и систем имеет relevant documents?

- Перечень сотрудников с access (имена + email + отделы)
- Перечень систем (email server, CRM, ERP, file-share, etc.)
- Внешние providers (cloud, archives, backups)

#### Шаг 3. Identify materials

Какие categories документов сохранять?

- Email переписка с counterparty и внутренняя
- Договоры, акты, накладные, счёт-фактуры
- Внутренние memos / решения
- Технические данные (logs, telemetry)
- ПДн обрабатываемые (применять с учётом 152-ФЗ — preservation не должно нарушать
  ст.21 на удаление)

#### Шаг 4. Date range

- **From:** [обычно — несколько лет до trigger event, e.g. срок исковой давности]
- **To:** indefinite (до release)

#### Шаг 5. Issue notice

```markdown
ПРИКАЗ № [N] от [DD.MM.YYYY]
"О сохранении документов в связи с матерой [matter name]"

В связи с [trigger event — например, получением досудебной претензии от ООО Acme
от 18.05.2026] и в целях сохранения доказательств для возможного судебного
разбирательства,

ПРИКАЗЫВАЮ:

1. Перечисленным ниже сотрудникам и подразделениям обеспечить сохранение всех
   документов, email-переписки, файлов и иных материалов, относящихся к
   следующему:

   [Перечень categories]

   За период с [DD.MM.YYYY] по момент отмены настоящего приказа.

2. Запрещается:
   - Уничтожение / удаление / изменение указанных документов и материалов
   - Удаление электронной переписки по delete-полиси (необходимо отключить
     auto-delete на email accounts: [список])
   - Очистка trash / архивов сотрудников по указанным категориям

3. Custodians (ответственные за сохранение):
   - [Имя 1] — отдел [...]
   - [Имя 2] — отдел [...]

4. Действие приказа продолжается до получения официального release ([release
   action] этого skill'а).

5. О любых вопросах и спорных ситуациях custodians обязаны незамедлительно
   уведомить [contact — GC / lead attorney].

Подписант: [имя GC / директора]
Дата: [DD.MM.YYYY]
МП
```

#### Шаг 6. Distribute notice

- Email custodians с return receipt confirmation
- IT enables holds на mail-boxes / file-shares
- Notice в matter folder

#### Шаг 7. Track в matter

Add в matter history:

```
[DD.MM.YYYY] LEGAL HOLD ISSUED
Trigger: получение претензии 18.05.2026
Custodians: [N человек]
Categories: [list]
```

---

### Action: REFRESH

**6-месячный default refresh.** Default refresh — каждые 6 месяцев notice
re-distributed (custodians могут забыть со временем).

Workflow:
- Identify все existing legal holds (out of `_log.yaml` or отдельный file)
- For each hold > 6 months old — distribute reminder notice
- Update last_refreshed_at

---

### Action: RELEASE

#### Шаг 1. Verify cause to release

Legal hold можно release когда:
- Matter resolved (settlement / judgment + appeals exhausted)
- Срок исковой давности истёк
- Counterparty явно отказался от claim
- Internal investigation closed

**Verify** с lead attorney перед release. **Premature release = риск spoliation
claim в будущем.**

#### Шаг 2. Issue release notice

```markdown
ПРИКАЗ № [N] от [DD.MM.YYYY]
"О снятии legal hold по матерy [matter name]"

В связи с [reason — например, заключением мирового соглашения и его исполнением]
настоящим уведомляю custodians о снятии legal hold, наложенного Приказом № [N]
от [DD.MM.YYYY].

С даты настоящего приказа документы и материалы, перечисленные в указанном
ранее приказе, могут обрабатываться в обычном порядке в соответствии с
retention policies компании и применимым законодательством (в том числе 152-ФЗ
для ПДн).

Подписант: [имя]
Дата: [DD.MM.YYYY]
МП
```

#### Шаг 3. Update в matter

```
[DD.MM.YYYY] LEGAL HOLD RELEASED
Reason: [...]
Released by: [имя]
```

---

### Action: STATUS

List active legal holds:

```markdown
| Matter | Issued | Custodians | Categories | Last refresh | Days active |
|--------|--------|------------|------------|--------------|-------------|
| ... | ... | N | ... | ... | N |
```

Flag if any hold > 6 months without refresh.

---

## РФ-specific

### АПК ст.72 — судебное обеспечение (не самосильное)

Если есть угроза утраты доказательств **у counterparty или у третьего лица** —
можно заявить в арбитражный суд ходатайство об обеспечении доказательств **до
подачи иска**. Суд может назначить:
- Судебная экспертиза
- Истребование документов
- Допрос свидетеля

Это **отдельная процедура** — не покрыто этим skill'ом (нужно отдельный draft
ходатайства).

### 152-ФЗ и preservation

При hold документов с ПДн:
- Преservation НЕ освобождает от обязанности удалить ПДн по запросу субъекта
  (ст.21)
- НО — если запрос субъекта получен после issuance hold — есть **legal basis
  обоснованного отказа** в удалении (data preservation для иска)
- DPO должен document этот case как exemption

### Запросы регуляторов

Если получили запрос РКН / ФАС / ФНС / следователя — отдельная процедура (см.
`/litigation:subpoena-triage`).

### Срок хранения после release

После release — общие retention rules:
- Бухгалтерия (402-ФЗ) — 5 лет
- Налоговые (НК ст.23) — 4 года после налогового периода
- HR (Росархив) — 75 лет для личных дел работников
- Прочие — по retention policy компании

**Important:** preservation order может extend срок выше нормального retention.
После release — back to normal retention.

---

## Attribution

Adapted from [`litigation-legal/legal-hold`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/legal-hold/SKILL.md)
by Anthropic (Apache 2.0).

**Категория C → B adaptation:**
- US FRCP 37(e) ESI preservation → РФ внутренний preservation order (договорный)
- АПК ст.72 (судебное обеспечение) — упомянуто как отдельная процедура (не
  скилл-сlope)
- 152-ФЗ overlay — preservation vs обязанность удалить ПДн
- Retention rules — по РФ нормам (402-ФЗ, НК, Росархив)
- "Spoliation" claims в РФ менее formalized чем US — но preservation все ещё good
  practice

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
