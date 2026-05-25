---
name: investigation-open
description: >
  Open new internal investigation matter — создаёт workspace для расследования
  (харассмент, дисциплинарка, утечка КТ, конфликт интересов и т.д.). РФ
  специфика: дисциплинарка по ст.192-193 ТК — 1 месяц со дня обнаружения, 6
  месяцев со дня совершения, обязательное objяснение от работника.
argument-hint: "[brief description of matter]"
user_invocable: true
ported_from: employment-legal/investigation-open
ported_at: 2026-05-18
adaptation_category: A
---

# /investigation-open

## Назначение

Открыть новое расследование. Создаёт workspace `~/.ru-legal/labor/investigations/[matter-id]/` со структурой:

```
[matter-id]/
  README.md           ← metadata + index
  intake.md           ← initial complaint / триггер
  facts.md            ← timeline (растёт через /investigation-add)
  evidence/           ← attached documents
  interviews/         ← interview notes (per witness)
  memo.md             ← legal analysis (создаётся /investigation-memo)
  summary.md          ← briefing summary (создаётся /investigation-summary)
  status.md           ← current status, next steps
```

См. полную методологию в [internal-investigation](../internal-investigation/SKILL.md) — backend framework.

## Workflow

### Шаг 1. Получи initial context

- **Тип:** харассмент / дискриминация / утечка КТ / конфликт интересов /
  дисциплинарка (прогул, неисполнение, хищение) / охрана труда (расследование
  НС) / финансовые нарушения / иное
- **Триггер:** жалоба / докладная / автоматический алерт / результат аудита
- **Дата триггера:** DD.MM.YYYY (critical для дисциплинарки — сроки ст.193 ТК)
- **Дата предполагаемого нарушения:** DD.MM.YYYY (critical — 6-мес limit ст.193)
- **Стороны:** заявитель / subject / свидетели
- **Severity initial assessment:** low / med / high / critical
- **Privilege framing:** in-house counsel (РФ — НЕ privileged) / outside adv (адв.тайна) / no counsel

### Шаг 2. Critical РФ pre-flight

#### A. Disciplinary deadlines (ст.193 ТК)

Если matter — потенциальная дисциплинарка (выговор / увольнение):

- **1 месяц** со дня обнаружения проступка (исключая болезнь, отпуск, время для учёта профсоюза)
- **6 месяцев** со дня совершения проступка (2 года для финансовых проверок)

**Flag immediately if:**
- > 6 мес со дня совершения → дисциплинарка невозможна, только civil claim / criminal
- > 3 недели с обнаружения → urgent, complete investigation в 1 нед

#### B. Объяснение работника (ст.193 ч.1 ТК)

**Обязательно** запросить письменное объяснение **до** применения дисциплинарного взыскания. **2 рабочих дня** на ответ. Без этого — взыскание незаконно.

#### C. Privilege framework

В РФ:
- **In-house lawyer involvement** — **НЕ** даёт адвокатскую тайну
- **Outside counsel — адвокат ФПА** → адвокатская тайна (ФЗ-63 ст.8)
- **Best practice:** при serious matters (потенциальный suit / criminal) — involve outside адвоката с начала

### Шаг 3. Generate matter ID

Format: `INV-[YYYY]-[NNN]` (например `INV-2026-014`)

### Шаг 4. Create workspace + README

```markdown
# Investigation [INV-2026-014]

## Metadata

- **Тип:** [type]
- **Open date:** [DD.MM.YYYY]
- **Триггер:** [trigger source + date]
- **Дата предполагаемого нарушения:** [DD.MM.YYYY]
- **Subject(s):** [pseudonyms или ФИО]
- **Заявитель:** [ФИО / anonymous]
- **Severity:** [low/med/high/critical]
- **Investigation lead:** [ФИО]
- **Counsel:** [in-house / outside ФИО / адвокат с ордером]
- **Privilege framework:** [in-house = НЕ privileged / outside-адв ФПА = privileged]

## ⚠ Дедлайны (если дисциплинарка)

- **Срок 1 мес с обнаружения (ст.193 ТК):** до [DD.MM.YYYY]
- **Срок 6 мес с совершения:** до [DD.MM.YYYY]
- **Объяснение запрошено:** [Y/N, дата] / срок ответа: 2 раб.дня
- **Дополнительно:** профсоюз / комиссия по трудовым спорам (если применимо)

## Status

[Open / In progress / Awaiting объяснение / Memo draft / Closed]

## Next steps

- [x] Запросить объяснение под подпись (срок 2 раб.дня)
- [ ] Собрать первичные документы
- [ ] Interview заявителя
- [ ] Interview subject (после получения объяснения)
- [ ] Interview свидетелей
- [ ] Legal memo
- [ ] Recommendation

## Index

- [intake.md](intake.md)
- [facts.md](facts.md)
- [evidence/](evidence/)
- [interviews/](interviews/)
```

### Шаг 5. Confirm + next action

```
✓ Investigation INV-2026-014 opened.
Workspace: ~/.ru-legal/labor/investigations/INV-2026-014/

⚠ Critical РФ deadlines:
- Объяснение по ст.193 ч.1 ТК — обязательно запросить ДО взыскания.
  Срок ответа 2 раб.дня. Текст обязательного запроса см. в memo
  template.
- 1 месяц с обнаружения — до DD.MM.YYYY.

Next: /investigation-add для записи фактов или
/investigation-add interview для интервью.
```

## Attribution

Adapted from [`employment-legal/investigation-open`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/investigation-open/SKILL.md)
by Anthropic (Apache 2.0).

**Категория A (light adaptation):** добавлены РФ-specific pre-flight checks (ст.193 ТК дедлайны, объяснение работника, privilege framework для РФ).

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
