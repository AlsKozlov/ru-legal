---
name: privilege-log-review
description: >
  Review privilege log при истребовании документов судом / органом. РФ адвокатская
  тайна (ФЗ-63 ст.8) — только для адвокатов ФПА. In-house counsel privilege в РФ
  НЕ имеет. Categorize документы: privileged / flagged / recommend disclose.
argument-hint: "[path to documents для review]"
user_invocable: true
ported_from: litigation-legal/privilege-log-review
ported_at: 2026-05-18
adaptation_category: C
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /privilege-log-review (review приvilege log)

## Назначение

При истребовании документов судом (АПК ст.66) или другими органами — необходимо
review каждый documеnt: подлежит ли disclosure или privileged?

В РФ **privilege landscape отличается от US fundamentally:**

| Привилегия | US | РФ |
|------------|----|----|
| Attorney-client (employee → in-house lawyer) | Yes — ACP applies | **НЕТ** — in-house без privilege |
| Attorney-client (employee → outside counsel) | Yes — ACP | **Yes** — адвокатская тайна (ФЗ-63 ст.8) — только если outside counsel = адвокат ФПА |
| Work product (mental impressions) | Yes — FRCP 26(b)(3) | **Limited** — нет аналога work-product doctrine в чистом виде |
| Banking secrecy | Limited | **Yes** — банковская тайна 395-1 ст.26 |
| Налоговая тайна | Not standalone | **Yes** — НК ст.102 |

## ⚠️ Pre-flight

**Critical для РФ:** **in-house counsel privilege НЕ имеет.** Communications между
employee и in-house lawyer — **не защищены** адвокатской тайной.

Это **fundamental** отличие от US/UK. Применяй этот фрейм consistently.

## Workflow

### Шаг 1. Identify scope

- Кто запрашивает (суд / РКН / ФНС / следователь)?
- На каком основании?
- Какие конкретно документы под scope?

### Шаг 2. Classify каждый документ

#### Категория 1: 🟢 Privileged (определённо не disclose)

- **Communications с outside counsel — адвокатом ФПА:**
  - Email / письма / меморандумы
  - Документы созданные адвокатом для нас в связи с юр.помощью
  - **Условие:** outside counsel — лицензированный адвокат ФПА (verify статус)

- **Сведения банковской тайны (395-1 ст.26):**
  - Banking операции наших клиентов
  - Disclosure только определённым органам по конкретным основаниям

- **Сведения налоговой тайны (НК ст.102):**
  - Сведения о налогах нас как налогоплательщика
  - Disclosure определённым лицам по основаниям

#### Категория 2: 🟡 Flagged (требует attorney review)

- **In-house counsel emails:**
  - В РФ — **не privileged**, но могут быть business sensitive
  - Recommend review для confidentiality concerns
  - Sometimes можно объявить commercial sensitivity (98-ФЗ) — но это не disclosure
    refusal, только request for confidential treatment

- **Документы с ПДн третьих лиц:**
  - Не основание refuse disclosure
  - Но требует sanitization / редактирования (см. `subpoena-triage`)

- **Документы коммерческой тайны (98-ФЗ):**
  - Не основание refuse disclosure государственному органу
  - Орган обязан соблюдать confidentiality полученных сведений
  - Request "режим коммерческой тайны" в proceeding

#### Категория 3: 🔴 Recommend disclose

- Документы без privilege grounds
- Прямо relevant к запросу
- Disclosure обязателен в указанный срок

#### Категория EU risk: in-house counsel privilege (Akzo Nobel)

**Akzo Nobel (CJEU 2010)** — EU recognizes in-house privilege limited. В РФ суды
**не** применяют этот pattern по умолчанию.

**Practical:** не полагайся на in-house privilege в РФ. Если документ создавался
in-house counsel — он не защищён.

### Шаг 3. Privilege log format

```markdown
# Privilege Log
**Запрос:** [источник + основание]
**Дата:** [DD.MM.YYYY]

| # | Документ | Дата | Авторы | Получатели | Категория | Основание | Status |
|---|----------|------|--------|------------|-----------|-----------|--------|
| 1 | "Меморандум по сделке X" | 15.03.2024 | Иванов И.И. (адвокат ФПА, ордер №...) | CEO + GC | 🟢 Privileged | Адвокатская тайна (ФЗ-63 ст.8) | NOT disclosed |
| 2 | "Email от in-house lawyer" | 20.03.2024 | Петров П.П. (in-house counsel) | CEO | 🔴 Disclose | In-house без privilege в РФ | Disclosed |
| 3 | "Bookkeeping за Q1" | 31.03.2024 | Accounting | внутренний | 🟡 Flagged | Содержит ПДн третьих лиц | Disclosed с sanitization |
| 4 | "Banking statement" | 15.04.2024 | Bank | компания | 🟢 Privileged | Банковская тайна (395-1 ст.26) | NOT disclosed без separate court order |
| ... | | | | | | | |
```

### Шаг 4. Submit к суду / органу

В большинстве случаев — privilege log subматывается **вместе с** disclosure'ом не
privileged documents.

```markdown
В соответствии с истребованием от [DD.MM.YYYY] № [N] предоставляем запрашиваемые
документы (приложение № 1).

Дополнительно сообщаем, что следующие документы не предоставляются на основании:

1. **Адвокатская тайна (ФЗ-63 ст.8):**
   - Документы № [N1], [N2] — указаны в privilege log (приложение № 2)
   - Основание: документы созданы или содержат сведения, полученные адвокатом
     ФПА [ФИО, удостоверение №] в связи с оказанием юр.помощи

2. **Банковская тайна (395-1 ст.26):**
   - Документы № [N3] — указаны в privilege log
   - Основание: содержат сведения о банковских операциях, disclosure которых
     ограничен указанной нормой

В случае несогласия со изъятием указанных документов просим суд принять
соответствующее решение по правилам АПК ст.66.

Приложения:
1. Перечень предоставленных документов
2. Privilege log
```

### Шаг 5. Track результаты

Some privileges могут быть overridden судом (особенно при уголовном производстве).
Track outcomes для будущих matters.

---

## Edge cases для РФ

### Outside counsel **не** адвокат ФПА

Если "outside counsel" — юридическая компания без адвокатов, или адвокат БЕЗ
действующего статуса (приостановлено / прекращено) — **privilege не работает.**

Verify status адвоката через реестр ФПА.

### Mixed documents

Документ содержит **и** privileged content, **и** non-privileged. Recommended:
- Provide redacted version
- Privilege log lists redacted portions с основаниями

### Уголовное производство

В рамках уголовного дела следователь может получить **санкцию суда** на изъятие
адвокатских документов (УПК ст.182). Тогда privilege может быть преодолён.

Even в этом случае — **адвокат должен present** при изъятии, может оспорить
санкцию.

### Документы клиентов (если мы — юр.фирма)

Если мы — адвокатское бюро / юр.фирма с адвокатами ФПА — документы наших клиентов
по матерam защищены адвокатской тайной от disclosure третьим лицам (включая суд
по делам других клиентов).

---

## Что НЕ делает

- Не делает final privilege decision — это manual review attorney
- Не валидирует статус адвоката в реестре ФПА — manual check
- Не genrates redacted versions documents — manual

---

## Attribution

Adapted from [`litigation-legal/privilege-log-review`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/privilege-log-review/SKILL.md)
by Anthropic (Apache 2.0).

**Категория C (substantial rewrite):**
- **Fundamental difference:** US ACP universal → РФ адвокатская тайна **только для
  адвокатов ФПА**, in-house без privilege
- Work product doctrine — нет прямого аналога в РФ
- Добавлено: банковская тайна (395-1), налоговая (НК ст.102), коммерческая (98-ФЗ
  — не grounds для refusal но grounds для confidentiality regime)
- Akzo Nobel (EU in-house privilege) — explicitly не применяется в РФ
- УПК ст.182 — privilege может быть overridden санкцией суда

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
