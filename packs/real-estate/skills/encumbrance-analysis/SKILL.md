---
name: encumbrance-analysis
description: >
  Deep analysis обременений объекта недвижимости — ипотека, аренда,
  сервитут, арест, доверительное управление, договорные права третьих
  лиц, восстановительный охранный режим. Identification + impact +
  resolution path.
argument-hint: "[объект cadastre № или адрес]"
user_invocable: true
ported_at: 2026-05-19
adaptation_category: D
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /encumbrance-analysis

## Назначение

Detailed анализ encumbrances + risks they pose + resolution paths. Deeper чем
`/cadastre-check` overview.

## Pre-flight

- `/cadastre-check` done
- Выписка из ЕГРН recent (< 30 days)
- Sufficient time для resolution (часто weeks)

## Types обременений + analysis framework

### A. Ипотека (залог) — ст.334+ ГК / ФЗ-102

**Most common.**

```markdown
## Ипотека analysis

- **Залогодержатель:** [банк / иное]
- **Сумма обеспечения:** [...]
- **Дата регистрации:** [DD.MM.YYYY]
- **Срок ипотеки:** [...]
- **Связь с объектом:**
  - Кредит на покупку именно этого объекта?
  - Ипотека другого обязательства (например, business loan, оформленная под недвижимость)?

### Impact на нашу сделку (если планируем купить)

- **Без resolution:** не можем купить (ипотека переходит к нам с объектом)
- **Resolution paths:**
  - **A. Pre-closing repayment** — продавец погашает с продажи или предварительно. Bank снимает ипотеку (issue letter, 5-7 раб.дней).
  - **B. Subrogation** — мы погашаем продавец's кредит (часть купли цена), bank снимает
  - **C. Refinance к нашей ипотеке** — если планируем ипотеку. Согласие банка-залогодержателя на смену залогодателя или новый contract.

### Steps

- [ ] Получить актуальную справку из банка о остатке долга
- [ ] Negotiate с продавцом — кто платит / по какому графику
- [ ] Закрепить в договоре купли-продажи (escrow до снятия ипотеки)
- [ ] Verify снятие в ЕГРН перед closing
```

### B. Аренда (зарегистрированная) — ст.609 ГК

```markdown
## Lease encumbrance

- **Арендатор:** [...]
- **Срок аренды:** [...]
- **Размер платы:** [информация может не быть disclosed в ЕГРН]
- **Дата регистрации:** [...]

### Impact

- При покупке объекта — **аренда переходит с объектом** (ст.617 ГК — права арендатора preserved при смене собственника)
- Покупатель становится landlord для existing tenants
- **Преимущественное право продления** арендатора (ст.621 ГК)

### Resolution

#### Option A: Take с тенант

- Continue lease
- Treat аренду как income
- May renegotiate terms если break-events present

#### Option B: Terminate lease до closing

- Requires основания (ст.620 / 619 ГК — limited grounds)
- Negotiation с tenant
- Payment compensation if applicable

#### Option C: Buy-out lease

- Pay tenant за досрочное расторжение
- Get formal written termination
- Verify сnятие в ЕГРН

### Steps

- [ ] Связаться с tenant — understand intent
- [ ] Verify lease содержание (если copy не в ЕГРН — request от seller)
- [ ] Decide approach
- [ ] Document в SPA + closing conditions
```

### C. Сервитут — ст.274-277 ГК / ст.23 ЗК

```markdown
## Сервитут analysis

- **Тип:** [право прохода / проезда / прокладки коммуникаций / иное]
- **В пользу:** [конкретное лицо / неопределённый круг]
- **Период:** [бессрочный / на срок]
- **Условия:** [...]

### Impact

- **Permanent encumbrance** — обычно не resolvable
- Ограничивает use участка (для земли)
- Может reduce value
- Tenant / owner participates в сервитуте

### Resolution

#### A. Negotiate cancellation

- Если сервитут добровольный — может быть отменён по соглашению
- Compensation third party
- Document в нотариальной форме + регистрация

#### B. Accept и adjust pricing

- Если cannot remove — discount при покупке
- Document в SPA

### Steps

- [ ] Get full text сервитута
- [ ] Understand history (как / почему установлен)
- [ ] Engage outside-адв для assessment
```

### D. Арест / запрет регистрационных действий

```markdown
## Арест analysis (CRITICAL)

- **Наложен:** [ФССП — судебный пристав / суд / следователь УПК]
- **Основание:** [...]
- **Дата наложения:** [...]
- **Сумма claim:** [...]

### Impact

- **Сделка невозможна** до снятия
- ЕГРН откажет в регистрации перехода

### Resolution

- **A. Pay долг** (если арест по unpaid долгу) — продавец платит → ФССП снимает в 3-5 раб.дней
- **B. Замена ареста** — bond / иное обеспечение
- **C. Обжалование** ареста в суде — если незаконно

### Steps

- [ ] Get текст постановления о наложении ареста
- [ ] Understand creditor + сумма
- [ ] Negotiate с продавцом — кто платит
- [ ] Verify снятие через выписку ЕГРН — не purchase до этого
```

### E. Доверительное управление — ст.1012+ ГК

```markdown
## Доверительное управление

- **Управляющий:** [...]
- **Период:** [...]

### Impact

- Объект managed управляющим
- Собственник retains права на отчуждение, но с restrictions per договор
- May need consent управляющего

### Resolution

- Verify договор доверительного управления (содержание)
- Termination provisions
- Possibly negotiate buy-out
```

### F. Договорные права третьих лиц (могут быть не в ЕГРН)

```markdown
## Не-зарегистрированные права

Critical: **не все** rights находятся в ЕГРН. Verify дополнительно:

### Аренда менее 1 года

- Не подлежит регистрации
- Но imeет силу для сторон + успокаивающий покупатель
- Verify через document review + interviews

### Преимущественное право участников (для долей)

- Не в ЕГРН
- Существует by law для определённых situations

### Option agreements

- Buy-back rights, ROFO, ROFR — могут не быть в ЕГРН
- Verify через interviews / document review

### Tenants по неформальной договорённости

- Могут не fixed документально, но physically occupying
- High risk surprise после closing

### Steps

- [ ] Inspect объект physically — anyone living?
- [ ] Interview neighbors / management company
- [ ] Get written representation от seller о отсутствии других прав
```

### G. Restoration / охранные режимы

```markdown
## Охранные режимы

Применимо для:
- **Объекты культурного наследия** — restoration ограничения; ст.45-47 ФЗ-73
- **Природные охранные зоны** (запoведник, национальный парк)
- **Санитарно-защитные зоны** (вокруг production)
- **Лесные / водные охранные зоны**
- **Архитектурные ансамбли**

### Impact

- Ограничения на реконструкцию / снос
- Required разрешения для любых работ
- Documentation требования

### Resolution

- Часто permanent — cannot remove
- Lower the price
- Plan future works around restrictions

### Verification

- Map applicable охранные зоны (Росреестр + Минкультуры + Росприроднадзор)
```

## Workflow

### Шаг 1. Inventory обременений

```markdown
## Encumbrance inventory

[Из выписки ЕГРН + non-EГРН sources]

| # | Type | Дата | В пользу | Status | Resolution path |
|---|------|------|----------|--------|------------------|
| 1 | Ипотека | DD.MM.YYYY | Сбербанк | Active | Закрытие при продаже |
| 2 | Аренда | DD.MM.YYYY | ООО Альфа (commercial) | Active | Take или buy-out |
| 3 | (исторически) Арест | DD.MM.YYYY | ФССП | Снято DD.MM.YYYY | OK |
```

### Шаг 2. Risk + resolution analysis

Для каждого encumbrance — applicable section выше.

### Шаг 3. Resolution plan + costs

```markdown
## Resolution plan

| # | Encumbrance | Resolution | Cost | Timeline |
|---|--------------|------------|------|----------|
| 1 | Ипотека | Repay at closing | 5М (часть купли цены) | 5-7 раб.дней |
| 2 | Lease | Take + new agreement с tenant | 0 (negotiate) | 30 дней |
| ... | | | | |

## Total resolution time

[Realistic estimate]

## Total resolution cost (если applicable вне purchase price)

[Sum]
```

### Шаг 4. Documentation для SPA

```markdown
## SPA provisions для encumbrances

### Conditions precedent

- [ ] Снятие ипотеки до closing
- [ ] Резrescolution lease ситуации
- [ ] (Иные)

### Reps & warranties seller

- Seller представляет полный disclosure encumbrances
- Seller представляет что не существует других prior rights не disclosed
- Indemnity для material breaches

### Closing date

- Не fix до resolution всех critical encumbrances
- Buffer for unexpected
```

## Output

```markdown
# Encumbrance Analysis — [объект]

## Inventory

[Table из Step 1]

## Risk verdict per encumbrance

[Per Step 2]

## Resolution plan

[Per Step 3]

## SPA provisions recommended

[Per Step 4]

## Overall transaction verdict

[PROCEED / PROCEED WITH FIXES / DO NOT PROCEED]

## Engaged outside-адв ФПА?

[For material — yes]
```

## Что НЕ делает

- Не negotiates с counterparties (это деал team)
- Не handles снятие обременений (это banking / нотариус / Росреестр)
- Не делает physical inspection

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
