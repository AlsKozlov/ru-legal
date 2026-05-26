---
name: purchase-sale-review
description: >
  Review договора купли-продажи недвижимости перед подписанием. РФ specifics:
  ст.549-558 ГК (общие); обязательная регистрация в ЕГРН; нотариальная форма
  для определённых сделок (доли в общей собственности — ст.42 ФЗ-218);
  материнский капитал; ипотека; иностранцы — некоторые restrictions.
argument-hint: "[path к договору]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /purchase-sale-review

## Назначение

Pre-signing review договора купли-продажи недвижимости. Different from ДДУ
(`/ddu-review`) — это уже existing property.

## Pre-flight

- `/cadastre-check` done
- `/encumbrance-analysis` done — all encumbrances identified + resolution planned
- Side known (buyer / seller)

## Mandatory elements (ст.554-555 ГК + ФЗ-218)

Договор купли-продажи **должен** содержать:

1. **Определение конкретного объекта** (адрес, площадь, кадастровый номер)
2. **Цена** (ст.555 — обязательно для договоров куpli-продажи недвижимости)
3. **Регистрация в ЕГРН** — обязательна (ст.131 ГК + ФЗ-218)

Без этих — договор недействителен.

## Workflow

### Шаг 1. Verify mandatory elements

```markdown
- [ ] Объект описан конкретно (кадастровый номер, адрес, площадь)
- [ ] Цена указана конкретно
- [ ] Условия оплаты (когда + как)
- [ ] Условия о передаче объекта + акт приёма-передачи
- [ ] Регистрация в ЕГРН planned
```

### Шаг 2. Critical clauses

#### A. Цена + условия оплаты

```markdown
- **Цена:** [сумма]
- **Структура оплаты:**
  - Cash при подписании
  - Эскроу до регистрации (recommended for buyer)
  - Аккредитив банка
  - Безналичный — на recipient счёт
  - Часть — ипотека
  - Часть — материнский капитал
- **Дата оплаты:**
  - До подписания (нечасто)
  - При подписании
  - **Best for buyer:** после регистрации перехода в ЕГРН
  - **Best for seller:** при подписании или escrow до регистрации
- **Валюта:**
  - Только rubles для РФ residents (ст.317 ГК)
  - Иностранная валюта — limited cases

⚠ **Critical для buyer:** не платить **до** регистрации в ЕГРН без protections (эскроу).

⚠ **Critical для seller:** не передавать объект до получения оплаты.
```

#### B. Условие о передаче

```markdown
- **Дата передачи** объекта buyer (фактическая, не documentary)
- **Акт приёма-передачи** — обязательно (ст.556 ГК)
- **Состояние** объекта при передаче
- **Имущество включено** (если furnished)
- **Коммунальные** — задолженности кто несёт (до даты передачи — seller; после — buyer)
- **Ключи**

⚠ **Red flag** для buyer — нет четкой даты передачи; "передача в течение N дней с момента регистрации"
```

#### C. Налоги + расходы

```markdown
- **Госпошлина за регистрацию** — обычно buyer (~2000 для физ.лиц, ~22000 для ЮЛ)
- **Услуги риелтора** — кто платит (обычно seller для open market, иначе negotiation)
- **НДФЛ продавца:**
  - Физ.лицо: 13% / 15% (если cumulative > 5M годовых)
  - Льгота при владении > 5 лет (для большинства случаев — ст.217.1 НК)
  - Льгота при владении > 3 лет (специальные cases: наследство, приватизация, дарение от близкого родственника)
  - Налоговая база — фактическая цена, но если меньше cadastral × 0.7 — uses cadastral × 0.7 (НК ст.214.10)

⚠ **Red flag:** "цена в договоре" договорная low с цельью income tax dodging — иллегально + рискованно для buyer
```

#### D. Reps & warranties seller

```markdown
**Standard:**
- Seller — полноправный собственник
- Право не ограничено
- Нет обременений (кроме disclosed)
- Нет open lit / claims
- Все коммунальные оплачены (или disclosed)
- Нет прописанных третьих лиц без права прекращения (или disclosed)
- Нет общая собственность с супругом / другим без consent

**Sometimes added:**
- Соответствие cadastral data (площадь, этажность, и т.д.)
- Соответствие фактической планировки (нет несогласованных перепланировок)
- Нет задолженности по налогам / штрафам
```

#### E. Indemnification (ст.461 ГК)

```markdown
- Seller liable for изъятие объекта у buyer третьим лицом по основанию возникшему до сделки
- Indemnification — should be explicit для clarity
```

#### F. Расторжение

```markdown
- Грантуется по общим основаниям ГК
- Если ипотека buyer и она не оформилась — risk для seller
- Если payment не received после регистрации — risk для seller (отменить регистрацию tough)
- Recommendation: escrow для buyer protection до регистрации; payment confirmation requirement before объект передаётся для seller
```

### Шаг 3. Specific scenarios

#### Scenario A: Покупка квартиры с ипотекой

- Согласование банка с условиями сделки
- Дополнительный bank insurance
- Может требовать титульное страхование (3 года)
- Эскроу-счёт — часто
- Bank как со-сторона / observer

#### Scenario B: Маткапитал

- Дополнительные требования (Социальный фонд утверждение, доли детям)
- Pre-school кadastr verification specific
- Sometimes additional documentation

#### Scenario C: Доли в общей собственности

- **Нотариальное удостоверение обязательно** (ст.42 ФЗ-218)
- Преимущественное право других совладельцев (ст.250 ГК) — 30 дней
- Notary handles documents + Росреестр

#### Scenario D: Иностранец-покупатель

- Restrictions на земельные участки в погранрайонах (Указ Президента + ЗК)
- Указ 81/2022 — для покупки от резидентов РФ
- Дополнительные documentation требования

#### Scenario E: Несовершеннолетние сособственники

- Согласие органа опеки и попечительства required
- Substitute property для несовершеннолетнего

#### Scenario F: Покупка у ИП / ЮЛ-собственника

- НДС considerations (если ЮЛ на ОСНО — НДС применим к коммерческой недвижимости; не applicable к жилой)
- Корпоративные одобрения (если крупная сделка / с заинтересованностью — см. corporate-law/closing-checklist)

### Шаг 4. Output

```markdown
# Purchase-Sale Review — [объект]

## Side: [buyer / seller]

## Bottom line

[Sign / Don't sign / Sign with changes]

## Mandatory elements check

[Per Step 1]

## Critical clauses review

[Per Step 2]

## Specific scenario considerations

[If applicable]

## Negotiation points

1. [Most important]
2. ...

## Pre-closing actions

- [ ] [...]

## At closing actions

- [ ] [...]

## Post-closing

- [ ] Verify ЕГРН запись created (within 7-10 days)
- [ ] Final settlement
- [ ] Tax filings (если seller)
```

## Что НЕ делает

- Не handles ipoteku (это banking + отдельный workflow)
- Не handles нотариальное удостоверение (это нотариус)
- Не подаёт в Росреестр (это нотариус / стороны)

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
