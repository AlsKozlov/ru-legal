---
name: internal-investigation
description: >
  Backend framework для investigation suite — defines workspace structure,
  privilege protocols (РФ-specific!), interview templates, evidence chain of
  custody, дисциплинарные timing rules (ст.192-193 ТК). Sub-skill: вызывается
  из /investigation-open, -add, -query, -memo, -summary. Не user-invocable.
user_invocable: false
ported_from: employment-legal/internal-investigation
ported_at: 2026-05-18
adaptation_category: B
---

# internal-investigation (framework)

## Назначение

**Sub-skill / framework.** Не вызывается напрямую пользователем. Используется как
shared knowledge базой для investigation suite:

- `/investigation-open`
- `/investigation-add`
- `/investigation-query`
- `/investigation-memo`
- `/investigation-summary`

Этот файл определяет **общие** РФ-specific protocols, чтобы каждый из выше
skills consistently их применял.

## 1. Workspace structure

Каждое расследование — отдельная папка:

```
~/.ru-legal/labor/investigations/[matter-id]/
  README.md           ← metadata, status, index, deadlines
  intake.md           ← initial complaint / триггер
  facts.md            ← timeline (append-only)
  evidence/           ← attached documents + sha256 log
  interviews/         ← per-witness notes
  memo.md             ← legal analysis (optional, выпускается /investigation-memo)
  summary.md          ← audience-specific briefings
  status.md           ← status updates
```

### Matter ID format

`INV-[YYYY]-[NNN]` (например `INV-2026-014`)

## 2. Privilege protocols для РФ

### Принципиальное отличие от US/UK

**В РФ:**
- **In-house counsel privilege НЕТ.** Communications между сотрудниками и
  in-house lawyer — **не защищены** адвокатской тайной.
- **Адвокатская тайна (ФЗ-63 ст.8)** — только для **outside-адв ФПА** (с
  удостоверением + ордером).
- **Work-product doctrine** — нет аналога. Mental impressions in-house counsel
  не защищены автоматически.
- **Коммерческая тайна (98-ФЗ)** — это business secrecy, **не** privilege от
  суда. Государственный орган может изъять documents под режимом КТ.

### Practical implications

| Scenario | Защита |
|----------|--------|
| Investigation by in-house team только | НЕТ privilege; защита через 98-ФЗ КТ — недостаточно от суда |
| Investigation under direction outside-адв ФПА с ордером | Адвокатская тайна — full |
| Memo drafted by in-house, reviewed by outside-адв | Mixed — privilege может быть, но courts могут pierce |
| Interview notes от HR | НЕ privileged даже если labeled "Privileged" |

### Best practice

**Для serious matters** (увольнение high-level, sexual harassment с PR exposure,
финансовые нарушения с фrak suit risk, criminal nexus):
1. **Engage outside-адв ФПА с самого начала** — с ордером.
2. Все communications routed через адвоката (CC или письмо на адв.).
3. Memo drafted адвокатом или под его руководством.
4. Documents stored в адвокатском досье.
5. Header на documents: "Адвокатская тайна (ФЗ-63 ст.8). Адв. [ФИО], удост. №, ордер №"

**Для routine matters** (мелкая дисциплинарка, conflict resolution):
- Privilege не нужен, работайте под "СЛУЖЕБНАЯ ТАЙНА. 98-ФЗ режим КТ"
- Don't mislabel "Privileged" — это даёт false confidence

## 3. Дисциплинарные сроки (ст.192-193 ТК)

### Clock 1: "Со дня обнаружения"

- 1 месяц со дня, когда работодатель **узнал** о проступке
- Исключаются периоды:
  - Болезнь работника
  - Отпуск работника
  - Время для учёта мнения профсоюза (ст.373)

### Clock 2: "Со дня совершения"

- 6 месяцев со дня самого проступка (hard cap)
- 2 года для нарушений, выявленных в результате аудита / inventarisации /
  financial check

### Объяснение работника (ст.193 ч.1)

- **Запрашивается до взыскания** письменно
- 2 рабочих дня на ответ
- Если не дал — составляется акт об отказе
- **БЕЗ запроса объяснения** взыскание автоматически незаконно

### Учёт мнения профсоюза (ст.373)

Если работник — член профсоюза, и matter — увольнение по инициативе работодателя
(ст.81), кроме исключений:
- Запрос мотивированного мнения профсоюза письменно
- 7 рабочих дней на ответ
- Если мнение отрицательное — дополнительные консультации в течение 3 раб.дней,
  затем работодатель может принять решение
- При увольнении — оформить в течение **месяца** со дня получения мотивированного
  мнения

### Срок ознакомления с приказом

- 3 раб.дня со дня издания приказа
- Если работник отказывается — акт об отказе

## 4. Виды дисциплинарных взысканий (ст.192 ТК — exhaustive list)

ТК предусматривает **только 3 вида:**
1. **Замечание**
2. **Выговор**
3. **Увольнение** по основаниям ст.81 (соответствующие ground'ы — п.5, п.6, п.7-10)

**За одно нарушение — только одно взыскание** (ст.193 ч.5).

### Что НЕ является дисциплинарным взысканием (но иногда применяется отдельно)

- **Лишение премии** — если положением об оплате предусмотрена depremation за
  нарушения. Не взыскание, но связано.
- **Удержание из зарплаты** — только для материального ущерба по ст.137 ТК
  (не "штраф" за поведение).
- **Перевод на нижеоплачиваемую** — только по ст.72.1 с согласия работника.

### Что **незаконно** делать

- Штрафы за опоздание ("$50 за каждое")
- "Строгий выговор" (нет в ТК)
- Объявления в чате с переходом на личность
- Депремирование "за всё" без формального положения об оплате
- Парные взыскания за одно нарушение (например, замечание + лишение премии за
  тот же случай — могут оспорить)

## 5. Interview protocols

### Витнесы / subject в РФ

- **Рабочее время** — interview в рабочее время по умолчанию; иначе требует
  consent / overtime pay
- **Право на представителя** — работник может прийти с представителем профсоюза
  / адвокатом / coworker (соглашение по practice)
- **Перевод** — если работник плохо говорит русский, ensure перевод
- **Recording** — только с consent (УК ст.137 — приватность). Best practice:
  notes only, не record audio без consent.

### Subject (потенциальный subject дисциплинарки)

- Inform что cooperation воluntary (но отказ может быть основанием для самостоятельного
  взыскания если есть должн.инструкция)
- **Объяснение по ст.193 ч.1** — отдельный formal step, не заменяется interview
  notes. Подписывается work-ом.
- Право молчать имеется (Конст.ст.51 — не свидетельствовать против себя)

### Confidentiality

- Сообщить — "to extent possible" — не promise total secrecy если matter может
  привести к суду / ГИТ
- Объяснить privilege framework честно (in-house = ограниченная защита в РФ)

## 6. Evidence handling

### Chain of custody

Для каждого attached evidence:
1. Source identified (who, when produced)
2. SHA256 hash calculated на момент receipt
3. Storage location logged
4. Access log maintained
5. Если digital — copy preserved в original form, working copy separately

### ПДн в evidence

Documents часто содержат ПДн третьих лиц. Для investigation:
- Cross-reference legal basis processing (ст.6 152-ФЗ) — обычно "законные
  интересы" (ст.6 ч.1 п.7)
- Disclosure только authorized investigators
- Retention — purpose-limited (после закрытия matter — review for deletion)

### Государственная тайна / банковская / врачебная

Если в materials есть такие сведения:
- Дополнительные ограничения disclosure
- Не сообщать outside-адв без separate clearance (для гостайны)
- Med info — только с consent или по запросу полномочного органа

## 7. Эскалация thresholds

| Triggering condition | Action |
|----------------------|--------|
| Subject — топ-менеджер / член совета директоров | Notify Board chair / акционеры |
| Estimated litigation exposure > 5 млн руб | Engage outside-адв ФПА |
| Criminal nexus (хищение, мошенничество, коммерческий подкуп УК ст.204) | Lawyers + decision about reporting to правоохрана |
| PR / media exposure risk | Coordinate с PR + outside-адв |
| Sanctions touch (US/EU PEPs) | Compliance отдельно (если есть pack) |
| Sexual harassment с physical contact | Criminal nexus check (УК ст.131-135) + outside-адв |
| Discrimination claim под защищ.категорию (ст.3 ТК) | Outside-адв + ГИТ exposure analysis |

## Attribution

Adapted from [`employment-legal/internal-investigation`](https://github.com/anthropics/claude-for-legal/blob/main/employment-legal/skills/internal-investigation/SKILL.md)
by Anthropic (Apache 2.0).

**Категория B (medium adaptation):**
- Privilege protocols **fundamentally** разные от US ACP — РФ требует outside-адв ФПА
- Disciplinary timeline framework пересмотрен с ТК ст.192-193 (1 мес / 6 мес / 2 года)
- Виды взысканий — 3-tier exhaustive list по ст.192 (не open-ended как US progressive discipline)
- Объяснение работника по ст.193 ч.1 — нет US equivalent
- Профсоюзный учёт мнения (ст.373) — нет US equivalent
- Interview protocols — РФ ПДн + представитель + recording consent
- Эскалация thresholds — РФ sums, РФ criminal codes (УК ст.131-135, ст.204), РФ ГИТ exposure

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
