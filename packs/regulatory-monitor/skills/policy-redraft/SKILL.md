---
name: policy-redraft
description: >
  Auto-draft изменений в нашем ЛНПА с учётом нового regulatory requirement.
  HITL approval перед finalize. Output: redline diff version + clean новая
  редакция. Cross-ref `corporate-law/policy-drafting` framework.
argument-hint: "[ЛНПА name] [trigger NPA / change description]"
user_invocable: true
ported_from: regulatory-legal/policy-redraft
ported_at: 2026-05-20
adaptation_category: B
---

# /policy-redraft

## Назначение

Generate draft updated version нашего ЛНПА в response на regulatory change.

## Pre-flight

- `gap-surfacer` flagged этот ЛНПА для update
- Current version ЛНПА available
- Trigger change (NPA) understood

## Workflow

### Шаг 1. Load current ЛНПА + trigger change

```markdown
- Current: [path/to/positsia-pdn-v3.2.docx]
- Trigger: Изменения 152-ФЗ — расширение special categories (с DD.MM.YYYY)
- Affected sections (from gap-surfacer): 2.3, 5
```

### Шаг 2. Draft изменений per section

Для каждой affected section:

```markdown
### Section 2.3 — Special categories ПДн

**Current text:**
> Special categories ПДн обрабатываются с письменного согласия (ст.10 152-ФЗ).
> Включают: расу, политические взгляды, религиозные убеждения, состояние
> здоровья, биометрию (для identification).

**Proposed text:**
> Special categories ПДн обрабатываются с письменного согласия (ст.10 152-ФЗ
> в редакции с DD.MM.YYYY). Включают: расу, политические взгляды, религиозные
> убеждения, состояние здоровья, биометрию (любое использование, не только для
> identification — изменение с DD.MM.YYYY), а также трудовую активность
> (новое требование).

**Reasoning:** ФЗ-XXX от DD.MM.YYYY расширил scope биометрии — теперь любая
обработка биометрии (не только для identification) treated как special category.
Plus добавлена категория "трудовая активность".

**Materiality:** 🔴 Material — без update наша compliance broken с DD.MM.YYYY.
```

### Шаг 3. Generate redline diff

```markdown
# REDLINE: Положение о ПДн v3.2 → v3.3

## Раздел 2.3 — Special categories ПДн

Special categories ПДн обрабатываются с письменного согласия (ст.10 152-ФЗ
~~в действующей редакции~~ **в редакции с DD.MM.YYYY**). Включают: расу,
политические взгляды, религиозные убеждения, состояние здоровья, биометрию
~~для identification~~ **(любое использование с DD.MM.YYYY)** **, а также
трудовую активность (новое)**.
```

### Шаг 4. Generate clean version

Clean version без markup — для финального текста после approval.

### Шаг 5. HITL approval

⚠ **Юрист должен review** redraft перед публикацией. Output skill — это draft,
не финальный документ.

Approval gates через harness/approval module:
1. Junior юрист review draft
2. Senior юрист / GC approve
3. Если профсоюз есть — учёт мнения по ст.372 (если applicable)
4. Officially утверждено приказом

### Шаг 6. Implementation actions

```markdown
## Post-approval actions

- [ ] Приказ об утверждении новой редакции
- [ ] (Если профсоюз) учёт мнения по ст.372 — выполнен
- [ ] (Если касается работников) лист ознакомления подготовлен
- [ ] Старая версия архивирована
- [ ] Внутренний portal updated
- [ ] Communications сотрудникам / клиентам если касается их
- [ ] (Опционально) внешнее раскрытие если ПДн / 152-ФЗ + изменение информирует субъектов
```

## РФ-specific considerations

### ст.74 ТК — изменение существенных условий

Если ЛНПА — это трудовое (правила, оплата, режим) и **меняет существенные
условия трудового договора** — нужна procedure ст.74 ТК:
- 2-мес уведомление работников
- Согласие или ст.77 п.7 увольнение

→ Этот skill flag's эту situation; **engaging labor-law/handbook-updates**.

### ст.372 ТК — учёт мнения профсоюза

Если профсоюз есть и ЛНПА в перечне learning mнения:
- Запрос мнения профсоюза перед утверждением
- 5 раб.дней на ответ
- Если negative — попытка договориться; иначе с протоколом разногласий

→ Cross-ref `labor-law/handbook-updates`.

## Attribution

Adapted from [`regulatory-legal/policy-redraft`](https://github.com/anthropics/claude-for-legal/blob/main/regulatory-legal/skills/policy-redraft/SKILL.md) by Anthropic (Apache 2.0).

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md). Material ЛНПА changes — engage outside-адв ФПА перед утверждением.
