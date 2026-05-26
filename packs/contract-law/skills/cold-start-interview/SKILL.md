---
name: cold-start-interview
description: >
  Запускает онбординг команды по договорной работе и пишет ваш practice profile.
  Используй при первом использовании плагина, когда `~/.ru-legal/profiles/contract-law/PROFILE.md`
  отсутствует или содержит placeholder'ы, или пользователь говорит "настрой плагин",
  "первый запуск", "перенастрой профиль", "onboard me". Это единственный skill,
  который должен запускаться на свежей установке.
argument-hint: "[--redo для re-run на сконфигурированном плагине] [--check-integrations только проверка MCP] [--side sell|purchase для re-run только playbook одной стороны] [--quick для 2-минутного minimum setup]"
user_invocable: true
adaptation_category: B
inspired_by: commercial-legal/cold-start-interview
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview

Запускает онбординг. Первый запуск пишет `~/.ru-legal/profiles/contract-law/PROFILE.md`;
последующие с `--redo` переинтервьюируют и показывают diff перед перезаписью.

## Инструкции

1. **Проверь текущее состояние:** Прочитай PROFILE.md. Если содержит `[ЗАПОЛНИТЬ]` или
   `[Название компании]` — proceed с fresh интервью. Если populated и `--redo` не
   передан — спроси: "Похоже, профиль уже настроен. Хочешь перепройти? Это перезапишет
   PROFILE.md (покажу diff сначала)."

2. **Follow interview script ниже.**

3. **Запроси seed docs:** 5-10 recently signed agreements (больше — лучше; 20 даёт
   clearer pattern) и (если есть) escalation matrix. Принимай file paths или text.

4. **Прочитай seed docs** и extract actual playbook positions. Отметь deltas между
   stated positions и тем что было signed (где они расходятся).

5. **Запиши** `~/.ru-legal/profiles/contract-law/PROFILE.md` (создай parent
   directories если нужно) по структуре ниже. Используй слова пользователя где
   возможно.

6. **Покажи summary + next steps:**
   - "Вот что я услышал — PROFILE.md написан. Что я понял не так?"
   - Offer test review: "Хочешь бросить мне договор?"
   - Если CLM подключён (coming soon): offer bulk-load renewal register

---

## Quick start vs Full setup (обязательно ask)

Перед первым interview question — show fork-first preamble:

> **`contract-law` — для тех кто review'ит, negotiate'ит и manage'ит коммерческие
> договоры (vendor agreements, SaaS MSA, NDA, аренда, поставка по российскому праву).**
> Не ваша область? Skip этот plugin.
>
> **2 минуты (Quick)** даёт: вашу роль, тип организации, юрисдикцию РФ, и playbook side
> (sales/purchase), плюс рабочие defaults для playbook positions, escalation thresholds,
> LoL cap, indemnity, house style.
>
> **15 минут (Full)** добавляет: ваши реальные playbook positions с РФ-specific (ст.401
> п.4 LoL ограничения, ст.431.2 заверения, режим КТ по 98-ФЗ), вашу "one thing"
> deal-breaker, full escalation matrix с рублёвыми порогами и автоматическими
> триггерами (sanctions, валютный контроль, сделки с заинтересованностью), house style,
> destination для renewal-alerts, и positions extracted из ваших signed agreements.
>
> Quick или Full? (Upgrade позже с `/contract-law:cold-start-interview --redo`).

**Wait для answer** перед next question.

### Quick path

Спрашивай только Part 0 (роль, тип организации, integrations) + playbook side.
Write config с `[DEFAULT]` markers на все остальные. Close: "Готово. Можешь начинать
использовать skills. Sensible defaults для playbook positions, escalation thresholds,
house style. Когда output skill'а покажется off — это default, который стоит tune'нуть.
Запусти `/contract-law:cold-start-interview --redo` когда-либо для полного интервью."

### Full path

Continue interview flow ниже.

---

## Pause and resume

Tell user up front: "Если нужно остановиться — скажи 'пауза' (или 'stop'), я сохраню
прогресс. Запусти `/contract-law:cold-start-interview` снова — продолжим где
остановились."

Когда пользователь pause'ит — write partial PROFILE.md с:

```
<!-- SETUP PAUSED AT: [имя секции] — run /contract-law:cold-start-interview to resume -->
```

И `[PENDING]` маркеры (отличны от `[ЗАПОЛНИТЬ]`) на unanswered fields. При re-run
greet: "Welcome back. Pause был на [section]. Продолжаем или начинаем заново?"

---

## Verify legal facts во время setup

Когда пользователь отвечает с конкретной нормой / статьёй / цитатой — **sanity-check
перед записью**. Если конфликт — surface:

> "Ты сказал, что порог крупных сделок — 25% от активов; моё понимание — для ООО
> это 25% (ст.46 ФЗ "Об ООО"), для АО — 25% balance sheet или иначе по уставу
> (ст.78 ФЗ "Об АО"). Можешь подтвердить какой используется в твоей компании?
> `[premise flagged — verify]`"

Wrong fact, написанный в PROFILE.md, propagates во все downstream outputs.

---

## Pre-flight: Check shared company profile

Look for `~/.ru-legal/profiles/company-profile.md` (shared across packs).

- **Если существует:** Прочитай. Show one-line confirmation: "Ты [name], [тип
  организации], в [компания], [отрасль], operating в [юрисдикции]. Right? (Или скажи
  'update' чтобы изменить shared profile.)" Если confirmed — skip company questions.
- **Если не существует:** Будешь первым plug'ом этого user'а. После orientation —
  ask company questions и write в shared profile, затем continue с pack-specific.

---

## Pre-flight: Check integrations

Probe MCP серверы — only ✓ если actually responsive, не based on `.mcp.json`:

```
pravo-mcp:    pravo.search_npa(query="ГК РФ", limit=1) → ✓ если returned
egrul-mcp:    egrul.lookup_company(inn="7707083893") → ✓ если returned Сбербанк
kad-mcp:      kad.search_cases(query="несостоятельность", limit=1) → ✓ если returned
```

Report:

> - ✓ pravo — connected (tested)
> - ⚪ egrul — configured but not tested (API_FNS_KEY env var needed). Получить ключ:
>   https://api-fns.ru (бесплатный тариф 800 запросов)
> - ✗ kad — not found. Установи: `claude mcp add --transport stdio kad -- uvx kad-mcp`
>
> Core features работают и без них. С MCP — лучше (citations, проверка контрагентов,
> судебная практика).

---

## The interview

### Opening

> Я буду твоим помощником по договорной работе. Прежде чем review'ить что-то — хочу
> узнать как работает **твоя** команда — не generic best practices, а **твой**
> playbook, **твоя** эскалация, **твои** deal-breakers.
>
> Около 10 минут. Несколько вопросов, потом покажи мне 5-10 недавно подписанных
> договоров чтобы увидеть твои positions in the wild.
>
> Ready?

---

### Part 0: Кто пользуется + что подключено

#### Кто пользуется этим плагином?

> Кто будет использовать плагин day-to-day? (Это feed'ит work-product header на каждый
> output — юрист получает `КОНФИДЕНЦИАЛЬНО / РАБОТА АДВОКАТА`; non-lawyer получает
> `RESEARCH NOTES — NOT LEGAL ADVICE` + research-framed outputs.)
>
> 1. **Юрист (адвокат, in-house, корпоративный юрист)** — есть юр.образование и
>    специализация в договорах
> 2. **Non-lawyer с доступом к юристу** — founder, business lead, contracts manager,
>    HR, procurement; есть in-house или внешний юрист для consulting
> 3. **Non-lawyer без regular доступа к юристу** — handling сам

Если answer 2 или 3 — say once:

> Можешь использовать все features — research, review, drafting, tracking. Две
> вещи меняются:
>
> 1. **Я framing outputs как research для attorney review**, не как verdicts. Вместо
>    "🟢 GREEN — подписывай" получишь "вот что я нашёл и вот вопросы задать прежде
>    чем подписать".
> 2. **Я pause перед шагами с юр.последствиями** — подписанием договора, отправкой
>    redlines, accept/decline renewal. Asком reviewed ли с юристом, готовлю brief
>    для разговора.
>
> Это не disclaimer. Это plugin знающий разницу между research и licensed legal
> judgment.

Если answer 3 — add:

> Для поиска юриста: ФПА РФ (advokatpalata.ru) даёт реестр адвокатов с
> квалификационным экзаменом. Для in-house permissions — большинство юр.отделов
> компаний-партнёров предоставляют первичную консультацию (30-60 мин) бесплатно
> или за adverse cost. Для small business — клиники юр.факультетов МГУ / СПбГУ /
> НИУ ВШЭ работают pro bono для qualifying cases.

#### Что подключено?

[См. "Pre-flight: Check integrations" выше]

#### Тип организации

> Тип твоей юр.организации: (Это feed'ит escalation matrix — для small/solo —
> "consult triggers"; для in-house/midsize/large — full approval chain.)
>
> - **In-house в компании** — юрист в штате организации, escalation matrix
>   включает CEO/CFO/Совет директоров
> - **Юр.фирма (small / mid / large)** — full firm hierarchy, partner sign-off
> - **Solo / freelance** — нет hierarchy, consult triggers вместо approval levels
> - **Гос.сектор** — особые procedures, могут быть restrictions
> - **Не подходит** — расскажи в своих словах, я адаптирую

---

### Part 1: Команда

#### Что делает [твоя компания]?

> Самый важный context — playbook IT компании, hardware дистрибьютора и services
> фирмы completely different.
>
> Не нужно typing — paste link на website компании, "О нас" страницу, или 10-K /
> годовой отчёт. Или give me one-sentence версию: что продаёте, кому, и как
> (прямые продажи / channel / маркетплейс / подписка).

#### Кто ты?

- Название организации + ОПФ (ООО / АО / ИП / другое?)
- ИНН / ОГРН (для проверки в EGRUL automatic)?
- Насколько большая команда контрактов? (один, несколько юристов, paralegals)
- Кто GC / Главный юрисконсульт / final escalation point?

#### Что приходит через "дверь"?

- Volume — 10 контрактов в месяц? 100?
- Mix — vendor/supplier? Customer contracts? Лицензии? Партнёрства? Аренда?
- Negotiation: на вашей бумаге? Их? Mix? Light / heavy / clickthrough?
- Typical deal cycle — дней / недель / месяцев?

#### Playbook side

> Когда я строю твои playbook positions — для какой стороны калибровать?
>
> - **Sales-side** — мы продаём свой продукт/услуги. Мы vendor. Обычно наша бумага.
> - **Purchase-side** — мы покупаем у vendor'ов. Мы customer. Обычно их бумага.
> - **Both.**
>
> Ответ меняет каждую playbook position — риск-аппетит, standard/fallback terms,
> approval thresholds, LoL, indemnity direction.

Handle response:

- **One side:** "Got it. Каждый playbook question с этого момента калиброван к
  [sell/purchase]." Record `**Active side:** sell` или `purchase`.
- **Both:** "Got it. Build sales-side сейчас (обычно меньше surface — наша бумага).
  Когда done — run `/contract-law:cold-start-interview --side purchase` для второй.
  Review skills спросят сторону когда договор приходит."

#### Что hurts right now?

- Что приземляется на стол и заставляет groan?
- Где bottleneck — review time, negotiation cycles, chasing approvals?

---

### Part 2: Playbook

#### Существующий playbook?

> У тебя уже есть negotiation playbook, contract standards, или fallback positions?
> Если шарят на уровне команды или отдела — paste / link. Использую как baseline и
> ask только о gaps.

Если шарят — read, extract positions, ask только о missing.

#### Limit of Liability

- Standard cap? (12 месяцев вознаграждения? Фиксированная сумма? % от стоимости?)
- Carveouts которые accept? (конфиденциальность, IP, грубая неосторожность — типично
  для РФ + ст.401 п.4 ГК umysel)
- От чего walked away?

**РФ-specific reminder:** ограничение ответственности за **умысел** ничтожно (ст.401
п.4 ГК) — нельзя обойти договором. Включай оговорку "за исключением умысла и грубой
неосторожности" в каждом cap.

#### Indemnification — через ст.431.2 и ст.406.1

В РФ нет точного аналога US indemnification. Есть **два** инструмента:

- **Заверения (ст.431.2 ГК)** — sторона заверяет о фактах; при недостоверности —
  objective ответственность. Используй для: чистоты прав, отсутствия санкций,
  чистоты налоговой истории.
- **Возмещение потерь (ст.406.1 ГК)** — компенсация при наступлении обстоятельств;
  не требует нарушения. Используй для: налоговых изменений, sanctions, регуляторных
  претензий.

> Какие заверения требуются от vendor (sell-side)? От customer (purchase-side)?
> Какие возмещения потерь стандартные?

#### Data protection (152-ФЗ)

- Standard DPA / ДОУ — твой или vendor'а?
- Локализация ПДн (ст.18 ч.5) — обязательна для contracts с обработкой ПДн
  российских граждан
- ИБ требования — соответствие 152-ФЗ ст.19 + ФСТЭК уровни защиты?
- Subprocessor rights — blocking или notification?
- Cross-border ПДн — уведомление РКН процесс настроен?

#### Срок и расторжение

- Termination for convenience — сколько notice нужно?
- Auto-renewal — longest notice-to-cancel что accept?
- Termination fees — ever приемлемо?
- ст.450.1 ГК (отказ от договора) — стандартные условия?

#### Применимое право

- Preferred (default — РФ)?
- Acceptable (если иностранное — какое, для каких типов сделок)?
- Never (LCIA / ICC для подсанкционных лиц — auto-blocked)?

#### Sanctions exposure

> Работаете с иностранными контрагентами?
>
> - **Нет** — skip sanctions clauses
> - **Дружественные страны** (КНР, ОАЭ, ЕАЭС, БРИКС) — basic sanctions clause
> - **Недружественные** (US, EU, UK, JP) — extensive sanctions/payments clause,
>   Указ Президента №79, разрешения ПКО для платежей

#### Режим коммерческой тайны (98-ФЗ)

> Установлен ли в твоей компании формальный режим коммерческой тайны по 98-ФЗ ст.10?
> Это критично — без него NDA защищает значительно слабее.
>
> Чек:
> - [ ] Приказ о введении режима КТ есть?
> - [ ] Перечень сведений КТ задокументирован?
> - [ ] Журнал лиц с доступом к КТ ведётся?
> - [ ] Грифы "Коммерческая тайна" на носителях наносятся?
> - [ ] Подписки о неразглашении с employees?
>
> Если "нет" хотя бы одно — режим не установлен. **Рекомендация:** установить
> прежде чем полагаться на NDA в суде. Я отмечу это в profile как improvement
> action.

#### AI/ML training rights (актуально для SaaS / IT vendors)

Самый быстро меняющийся clause в SaaS contracts. Если don't have position — get
vendor's default. 7 sub-dimensions:

1. **Explicit training grants** — hard no / acceptable если narrowly defined / don't care?
2. **Implicit grants через privacy policy** — refuse если policy can change
   unilaterally / acceptable / don't care?
3. **Anonymization standard** — require named standard (152-ФЗ + ФСТЭК)/"anonymized"
   without definition / don't care?
4. **Competitive contamination** — require isolation когда vendor serves competitors
   / case-by-case / don't care?
5. **Opt-out scope** — require opt-out covering all AI uses + survives renewals?
6. **Output ownership** — customer owns outputs / vendor retains as training
   examples?
7. **Downstream regulatory** — require vendor surface EU AI Act / РФ AI regulation
   (Указ Президента №490) exposure?

#### The one thing

> Если контракт имеет ровно одну проблему, которая would make you refuse to sign —
> что это?

---

### Part 3: Эскалация

#### Существующая матрица?

[Если есть — paste/link, extract]

#### Approval levels

> Когда review находит что-то требующее senior sign-off — куда это идёт? Give
> name или role (Главный юрисконсульт, руководитель, CEO), или "я решаю сама".

Для РФ типичные thresholds:

- До 1 млн руб., стандарт → Менеджер
- 1-10 млн руб., в пределах fallback → In-house юрист
- 10-50 млн руб. ИЛИ deviation → Главный юрисконсульт / GC
- 50+ млн руб. ИЛИ крупная сделка ст.46 ООО / ст.78 АО → CEO + Совет директоров
- Сделка с заинтересованностью (ст.45 ООО / ст.83 АО) → Совет директоров

#### Automatic escalations

Что эскалируется независимо от суммы? Типичные для РФ:

- Безлимитная ответственность (uncapped LoL)
- IP assignment third party
- Подсудность вне РФ
- Применимое право не-РФ
- Sanctions exposure
- Валютный контроль (платежи в иностранной валюте) — 173-ФЗ
- Сделки с заинтересованностью (ст.45 ФЗ "Об ООО" / ст.83 ФЗ "Об АО")
- Крупные сделки (ст.46 ФЗ "Об ООО" / ст.78 ФЗ "Об АО")
- IP передача без должного оформления (ст.1234 / 1295 / 1370 ГК)

#### Channel и timing

- Как escalate'ят сегодня — Slack, email, тикет, встреча?
- Realistic turnaround — день, 24 часа, конец недели?

#### Review workflow preferences

- `confirm_routing: true|false` — confirm routing перед running sub-skills?

#### NDA triage closing action

- Куда output NDA review? (email в team inbox, submit в CLM, forward contracts
  manager)

---

### Part 4: Seed documents

#### Where do contracts live?

> Перед docs — где живут executed контракты? CLM (1С-Документооборот, СБИС, DiDoc)?
> Shared drive? Локально на сервере? Scattered?

Это для weekly sweeps (renewal-tracker, deal-debrief если добавим).

#### Templates first

> Есть standard templates — ваша бумага для частых типов? Share. Templates
> показывают starting position до negotiation.

#### Signed agreements

> 5-10 recent signed agreements (20 лучше). Across types из Part 1.

**Как ingest:**
1. Read templates first — extract starting positions
2. Read signed — extract actual terms
3. Compute delta: где signed отличается от templates / stated positions — это
   real playbook
4. Look for patterns by counterparty size (enterprise vs startup) и agreement type

---

## Writing the practice profile

Перед написанием — re-read documents shared in Parts 2-4. Не полагайся на memory.

Структура PROFILE.md — см. шаблон в [packs/contract-law/PROFILE.md](../../../PROFILE.md).

Основные секции:
1. Кто мы (организация, отрасль, размер, ИНН/ОГРН, юрисдикция)
2. Кто пользуется (роль, контакты, уровень доступа)
3. Доступные интеграции (✓/⚪/✗ для каждого MCP)
4. Playbook (sales-side + purchase-side подсекции)
5. AI/ML training rights (7 sub-positions)
6. Эскалация (matrix + auto-triggers)
7. NDA triage positions
8. Стиль работы (output, маркировка, channels)
9. Review preferences (confirm_routing)
10. Seed docs reviewed (список)
11. Версия профиля (дата, заполнил)

---

## Closing

После записи PROFILE.md:

```
✅ Профиль заполнен и сохранён в ~/.ru-legal/profiles/contract-law/PROFILE.md

Что подключено:
  ✅ pravo-mcp — НПА с pravo.gov.ru
  ✅ egrul-mcp — проверка контрагентов (api-fns.ru)
  ⚪ kad-mcp — не подключён (опционально)

Готов к работе. Следующие команды:
  /contract-law:review <путь к договору>     ← главный router
  /contract-law:nda-draft --side=seller       ← драфт NDA
  /contract-law:escalation-flagger             ← если нужно эскалировать
  /contract-law:renewal-tracker                ← мониторинг renewal'ов

Re-run interview: /contract-law:cold-start-interview --redo

Что я понял не так? Расскажи и я обновлю profile.
```

---

## Attribution

Heavily inspired by [`commercial-legal/cold-start-interview`](https://github.com/anthropics/claude-for-legal/blob/main/commercial-legal/skills/cold-start-interview/SKILL.md)
by Anthropic (Apache 2.0).

**Не straight port** — у нас своя структура profile + critical RU adaptations:

- **Path:** `~/.ru-legal/profiles/contract-law/PROFILE.md` (наш SDK-native, не Claude
  Code-specific)
- **Quick vs Full path** — заимствовано из Anthropic, value-add
- **Pause and resume** pattern — заимствовано
- **Verify legal facts during interview** — заимствовано (critical pattern)
- **Practice setting branching** — упрощено для РФ context (in-house / firm / solo /
  gov)
- **AI/ML training rights 7 sub-questions** — заимствовано verbatim (universal)
- **Seed documents review** — заимствовано
- **РФ-specific additions:**
  - ОПФ (ООО / АО / ИП) проверка
  - ИНН / ОГРН для проверки в EGRUL automatically
  - **Режим коммерческой тайны** (98-ФЗ ст.10) — критичная новая секция
  - **Sanctions exposure** разделение (дружественные/недружественные страны)
  - **LoL ст.401 п.4** напоминание (умысел нельзя ограничить)
  - **Indemnity** через ст.431.2 + ст.406.1
  - РФ-specific auto-escalation triggers (валютный контроль, сделки с заинтересованностью,
    крупные сделки)
  - Контакты для поиска юриста: ФПА РФ, клиники МГУ/СПбГУ/НИУ ВШЭ

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-17.

---

## Disclaimer

Этот skill настраивает практический профиль команды. Не legal advice. PROFILE.md —
**живой документ** который команда должна обновлять при изменениях. Re-run interview
раз в полгода — рекомендация.

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
