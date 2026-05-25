---
name: renewal-tracker
description: >
  Показывает договоры с приближающимися deadline'ами расторжения и предупреждает
  до того как закроется окно уведомления, работая из maintained renewal register.
  Используй когда пользователь спрашивает "что скоро продлевается", "какие
  renewals подходят", "пропустили ли мы окно отказа", "добавь в renewal tracker",
  или по cron. Принимает handoffs от `saas-msa-review`.
argument-hint: "[--days N для изменения окна | --missed для пропущенных окон]"
user_invocable: true
ported_from: commercial-legal/renewal-tracker
ported_at: 2026-05-17
adaptation_category: A
---

# /renewal-tracker

Surface'ит что продлевается и до какой даты нужно уведомить об отказе.

## Назначение

Никто не читает договор дважды. Дата продления извлекается **один раз** — на этапе
review — и потом она живёт где-то. Идеально — там, где она **кричит** за 45 дней до
дедлайна уведомления, а не за 45 дней после.

Этот skill maintain'ит renewal register и surface'ит что подходит.

## Инструкции

1. **Прочитай register** `~/.ru-legal/profiles/contract-law/renewal-register.yaml`
   (живёт в config директории — survives plugin updates).

2. **Default mode (Mode 2):** что подходит в следующие 90 дней, grouped по urgency
   с half-open intervals чтобы каждый deadline попадал в ровно одну полосу:
   - 🔴 **0-13 дней** (critical — отправляй уведомление прямо сейчас)
   - 🟠 **14-44 дней** (high — запланируй на эту неделю)
   - 🟡 **45-89 дней** (medium — на радаре, но времени достаточно)

   Days 14, 45, и 90 — boundaries: каждая граница принадлежит ровно одной полосе.

3. **`--days N`:** change окно. Например `--days 180` — на 6 месяцев вперёд.

4. **`--missed`** (Mode 4): cancel-by deadlines, которые **прошли** без recorded
   cancellation. Это late warning, чтобы не давать auto-renew случиться silently.

5. **Если register пустой и [CLM coming soon] подключён:** offer Mode 3 — scan CLM
   для active agreements с renewal dates и bulk-load в register.

6. **Output включает recommended actions:** кому пинговать (business owner из каждой
   entry), какие имеют uncapped pricing (получи leverage до того как window закроется).

## Examples

```
/contract-law:renewal-tracker
```

```
/contract-law:renewal-tracker --days 180
```

```
/contract-law:renewal-tracker --missed
```

---

## Renewal register format

Лежит в `~/.ru-legal/profiles/contract-law/renewal-register.yaml`. Каждая entry:

```yaml
- counterparty: "ООО Яндекс.Облако"
  agreement: "Договор оказания услуг Yandex Cloud, № YC-12345"
  signed_date: 2025-06-15
  initial_term_end: 2026-06-15
  current_term_end: 2026-06-15          # катится вперёд после каждого auto-renew
  renewal_mechanism: "auto-renew annual"
  notice_period_days: 60                 # за сколько дней до окончания нужно уведомить
  notice_method: "email"                 # email / portal / courier / заказное письмо / per договор п.X
  transit_buffer_days: 0                 # 0 для электронной формы; 5 для заказного письма по РФ;
                                          # 10 для международной отправки
  cancel_by_calendar: 2026-04-16         # current_term_end минус notice_period_days
  cancel_by_effective: 2026-04-16        # roll'нуто к последнему рабочему дню если нужно
  send_by_effective: 2026-04-16          # cancel_by_effective минус transit_buffer_days
                                          # — дата к которой ДОЛЖНО быть ОТПРАВЛЕНО уведомление
  cancel_by_roll_note: ""                # например "roll'нуто с воскресенья 2026-11-01;
                                          # verify against договора definition рабочих дней"
  cancel_by_provenance: "[model calculation — verify против notice clause договора]"
  price_on_renewal: "then-current list (uncapped)"
  annual_value_rub: 1200000              # в рублях, для context
  currency: "RUB"                         # RUB / USD / EUR / другая — валютный контроль если не RUB
  vat_treatment: "с НДС 20%"             # как НДС отражён в цене
  business_owner: "ivanov@company.ru"
  responsible_legal: "petrova@company.ru"
  procurement_contact: "sidorov@company.ru"
  clm_id: ""                              # if connected
  edm_envelope: ""                        # if Контур.Сайн / СБИС / DiDoc
  status: "active"                        # active | cancelled | renewed | lapsed
  notes: "Cmid uncapped — revisit перед продлением. Альтернативы: VK Cloud, Selectel."
```

### Transit time — alert off `send_by_effective`, не `cancel_by_effective`

60-дневное окно с заказным письмом — это реально ~55 дней. Tracker, который alert'ит на
received-by date, — это tracker который **пропускает дедлайн**.

Compute `send_by_effective = cancel_by_effective - transit_buffer_days` и fire alerts
(🔴 / 🟠 / 🟡 urgency полосы в Mode 2) **на основе `send_by_effective`**. Mode 2 urgency
column показывает `send_by_effective`; detail column surface'ит `cancel_by_effective`,
`notice_method`, и `transit_buffer_days` чтобы reader видел delta и мог challenge buffer.

### Notice method и transit buffer для РФ

| Способ уведомления | Default `transit_buffer_days` | Notes |
|--------------------|------------------------------|-------|
| Email на authorized address | 0 | Default. Receipt через email read receipt или delivery notification |
| ЭДО (Контур.Сайн / СБИС / DiDoc) | 0 | Юр.значимо по ФЗ-63 (ЭП); timestamp сервиса = доказательство |
| Заказное письмо по РФ (Почта России) | 5 | Realistic; некоторые регионы — 7-10 |
| Заказное письмо с уведомлением о вручении | 7 | Гарантирует proof of delivery, но slower |
| Курьер по Москве/СПб | 1 | Same-day; буффер на сбои |
| Курьер по РФ | 3-5 | DHL/CDEK/etc. |
| Международная курьерская доставка | 7-14 | EMS, DHL international |
| Электронное уведомление через portal контрагента | 0-2 | Зависит от SLA портала |

**По умолчанию заводи минимальный буффер**, но **верифицируй против пункта договора о
порядке уведомлений.** Многие РФ договоры требуют "письменное уведомление" — это значит
заказное письмо, не email (если email не explicitly разрешён).

---

## Output formats

### Mode 2 — что подходит (default)

```markdown
# Renewal Tracker — состояние на 2026-05-17

## 🔴 СРОЧНО (0-13 дней до отправки уведомления)

| Контрагент | Договор | Send by | Cancel by | Сумма (год) | Бизнес-owner |
|------------|---------|---------|-----------|-------------|--------------|
| ООО Яндекс.Облако | YC-12345 | 2026-05-20 | 2026-05-25 | 1.2M ₽ | ivanov@ |

**Действия:**
- ivanov@: подтверди — продлеваем или отказываемся? Решение нужно до 2026-05-20.

## 🟠 Внимание (14-44 дней)

[table]

## 🟡 На радаре (45-89 дней)

[table]

---

## Pricing flag: uncapped увеличения цен на renewal

| Контрагент | Текущая цена | Условие | Recommended action |
|------------|--------------|---------|---------------------|
| ООО Яндекс.Облако | 1.2M ₽/год | "тогдашний прайс-лист" (uncapped) | Запроси цену продления СЕЙЧАС, до того как window закроется и leverage уменьшится |
```

### Mode 4 — `--missed`

```markdown
# Пропущенные окна уведомления

## ⚠️ Auto-renew сработал без отказа

| Контрагент | Договор | Должен был уведомить до | Auto-renew сработал | Стоимость года продления |
|------------|---------|--------------------------|---------------------|--------------------------|
| ООО Пример | EX-2345 | 2026-04-15 | 2026-06-15 | 2.5M ₽ |

**Recommended actions:**
- Эскалировать к юристу: возможны ли early termination опции?
- Проверить договор на наличие out-clause (расторжение по соглашению, по объективным причинам)
- Если no out-clause — план на cancel перед следующим renewal cycle (через год)
```

---

## Специфика для РФ контекста

### Особенности продления договоров в РФ

1. **Ст.610 ГК (аренда):** Если арендатор продолжает пользоваться имуществом после
   окончания срока — договор **считается возобновлённым на тот же срок** на тех же
   условиях. Это default правило для аренды.

2. **Ст.621 ГК (преимущественное право арендатора):** В большинстве случаев арендатор
   имеет преимущественное право на заключение нового договора. Это влияет на стратегию
   renewal'а.

3. **Договоры услуг (гл.39 ГК)** — нет default rule про auto-renewal. Условие должно
   быть **явно прописано** в договоре. Если не прописано — договор истекает.

4. **Договоры поставки (§3 гл.30):** аналогично — auto-renewal только если явно.

5. **Госконтракты по ФЗ-44:** **не имеют auto-renewal** в принципе. Каждый контракт —
   результат отдельной закупки. Tracker для них trivial: окончание срока = окончание.

6. **Форма уведомления:** ст.452 ГК — изменение/расторжение договора должно быть в той
   же форме что и договор. **Email достаточно** только если договор это явно разрешает.
   Иначе — письменное уведомление с подписью.

### Налоговые и валютные нюансы

- **Cross-border (валютный контроль 173-ФЗ):** если договор в иностранной валюте —
  cancel decision должно учитывать обязательства по валютному контролю (репатриация,
  decларации в банке). Add flag в register для FX deals.
- **Передача прав на ИС при cancel:** если в договоре переданы лицензии — что
  происходит после расторжения? ст.1235 ГК — лицензия прекращается с расторжением,
  если иное не предусмотрено.

### Контрагенты — особый case

- **Госкорпорации:** часто настаивают на standard formах с фиксированными условиями
  renewal. Negotiate cancellation conditions при initial signing — потом уже не
  изменить.
- **Иностранные контрагенты (особенно из недружественных стран):** проверь до cancel
  что нет sanctions implications. Прекращение договора может trigger contr-санкции
  по Указу №79.

---

## Что этот skill НЕ делает

- Не отправляет уведомления автоматически. Только flags и drafts.
- Не принимает решений "продлевать ли" — это бизнес-call. Skill surface'ит факт что
  нужно решать.
- Не редактирует сам договор (для этого `amendment-history` или `contract-review`).
- Не маневрирует через clauses о ранней расторгации — это требует юр.анализа conкретного
  кейса.

---

## Привязанные skills

- **`saas-msa-review`** → автоматически добавляет SaaS deals в register после review
- **`contract-review`** → при review договора с auto-renewal — offer добавить в tracker
- **`escalation-flagger`** → если cancel decision требует CEO/CFO одобрения

---

## Attribution

Adapted from [`commercial-legal/renewal-tracker`](https://github.com/anthropics/claude-for-legal/blob/main/commercial-legal/skills/renewal-tracker/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения от оригинала:**
- Register format расширен для РФ: `currency`, `vat_treatment`, `edm_envelope`
  (Контур.Сайн/СБИС/DiDoc), `responsible_legal`, `procurement_contact`
- Transit buffer таблица **полностью адаптирована** под РФ:
  - Заказное письмо по РФ — 5 дней (US: certified mail — другие сроки)
  - ЭДО (Контур.Сайн / СБИС / DiDoc) — 0 (юр.значимо по ФЗ-63)
  - International EMS / DHL — 7-14 дней
- Добавлена секция "Особенности продления в РФ":
  - Аренда (ст.610, 621 ГК) — auto-renew default rule
  - Услуги/поставка (гл.39 / §3 гл.30) — auto-renewal только if explicitly
  - Госконтракты ФЗ-44 — без renewal в принципе
  - Форма уведомления (ст.452 ГК)
- Добавлена секция про **налоговые и валютные нюансы** (173-ФЗ, ст.1235 ГК для IP)
- Контрагент-specific guidance: госкорпорации, иностранные с sanctions exposure
- Stакже все amounts в рублях, контрагенты — real РФ компании (Yandex Cloud, VK Cloud)
- Path: → `~/.ru-legal/profiles/contract-law/renewal-register.yaml`

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-17.

---

## Disclaimer

Этот skill производит tracking и preliminary action items. Не legal advice про
конкретное расторжение договора. Все cancel/renew decisions для high-value договоров
требуют верификации юристом, учитывая текущее состояние сделки и контрагента.

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
