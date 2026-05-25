---
name: use-case-triage
description: >
  Быстро определяет требует ли деятельность обработки ПДн оценку вреда (ОВПД по
  ст.18.1 152-ФЗ), уведомление РКН (трансграничная передача ст.12), или может
  proceeded без формальной оценки. Surface'ит конфликты с политикой обработки ПДн.
  Используй когда пользователь спрашивает "нужна ли ОВПД", "проверь эту фичу с
  точки зрения ПДн", "можно ли использовать X с точки зрения 152-ФЗ", или
  описывает новый processing activity / vendor relationship.
argument-hint: "[описание обработки ПДн или фичи]"
user_invocable: true
ported_from: privacy-legal/use-case-triage
ported_at: 2026-05-18
adaptation_category: B
---

# Privacy Use Case Triage (РФ adaptation)

## Назначение

Ответ на вопрос, который возникает **до** того как кто-то запускает ОВПД (оценку
вреда): "нужна ли она вообще?" И если да — какого типа, и что блокирует путь?

Privacy triage **быстрее** чем PIA generation, но **upstream** от неё. Не пишет
assessment — определяет нужна ли она и на каких условиях. `/data-protection:pia-generation`
делает deep work.

Output — одна из четырёх классификаций:

- 🟢 **PROCEED** — ОВПД не нужна. Standard safeguards применяются.
- 🟡 **OVPD REQUIRED** — нужна оценка вреда (ст.18.1) перед / параллельно deployment'у.
- 🟠 **OVPD + RKN NOTIFICATION** — обязательное уведомление РКН (cross-border, новый
  оператор, спец.категории). Привлечение DPO/GC.
- 🔴 **STOP** — Activity конфликтует с политикой обработки ПДн или не имеет правовых
  оснований по ст.6/9 152-ФЗ. Redesign before proceeding.

---

## Pre-flight: read config

Прочитай `~/.ru-legal/profiles/data-protection/PROFILE.md`. Триггер критерии,
регуляторный footprint, и политика обработки ПДн — authoritative.

Если файл отсутствует / содержит `[ЗАПОЛНИТЬ]`:

> "Profile ещё не настроен — без него я не могу tailor триаж под вашу practice.
>
> Два варианта:
> - Запусти `/data-protection:cold-start-interview` (2 минуты) → triage против YOUR practice
> - Скажи **'provisional'** → triage против generic defaults (средний риск, юрист,
>   нет playbook) с тегом `[PROVISIONAL]` для всех findings"

---

## Triage process

### Шаг 1. Понять activity

Если описание vague — спроси перед классификацией:

- **Какие ПДн** собираются / обрабатываются? Какие категории (ст.5 152-ФЗ — ФИО,
  паспорт, и т.д.; ст.10 — спец.категории; ст.11 — биометрия)?
- **Кто субъекты ПДн** — клиенты-физлица, сотрудники, кандидаты, третьи лица?
- **Цель обработки** (ст.5 ч.2 152-ФЗ требует конкретную, заранее определённую цель)?
- **Новая обработка** или re-purposing существующих ПДн?
- **Vendor / third party** вовлечён? Новый или existing?
- **Автоматизированное принятие решений** (ст.16) — влияет ли output на права субъекта?
- **Deployment context** — internal only, customer-facing, public?

"Новая фича" и "обработка данных" — **не достаточно** для accurate triage.

---

### Шаг 2. Check РФ overlays (отраслевые тайны)

**Перед тем как research 152-ФЗ-specific triggers — спроси про federal/sectoral overlays
для РФ.** Эти overlays часто supplybly controlling framework, не просто overlay.

> **Сектоrale overlays для РФ — спроси сразу:**
>
> Затрагивает ли эта обработка:
>
> - **Финансовые данные клиентов** (банковская тайна по ст.26 395-1 "О банках и
>   банковской деятельности")? Имеет substantive ограничения на disclosure,
>   отдельно от 152-ФЗ.
> - **Медицинские данные** (медицинская тайна по ст.13 323-ФЗ "Об основах охраны
>   здоровья")? Уведомление субъекта о disclosure обязательно; раскрытие — только
>   по конкретным основаниям закона.
> - **Данные о услугах связи** (тайна связи по ст.63 126-ФЗ "О связи")? Особые
>   правила для operator'ов связи.
> - **Налоговая информация** (налоговая тайна по ст.102 НК)? Substantive
>   ограничения от налоговой.
> - **Адвокатская тайна** (ФЗ-63 "Об адвокатской деятельности")? **Только для
>   адвокатов с удостоверением ФПА — не in-house counsel.**
> - **Биометрические ПДн** (ст.11 152-ФЗ + 572-ФЗ "О единой биометрической
>   системе")? Особый режим, согласие в письменной форме (ст.11 ч.1).
> - **Несовершеннолетние** (ст.9 ч.4 152-ФЗ — согласие родителя/опекуна для до 14)?
> - **ПДн госслужащих, кандидатов** (специальные нормы)?
>
> Если **да** на любой — sectoral norm supplies **controlling restriction**, не
> просто overlay. Research конкретную норму и **cite specific provision** перед
> continue.

**Critical:** активность "exempt" от стандартного 152-ФЗ режима через одну из
sectoral норм — **не automatically lawful**. Sectoral норма supplies свои ограничения.

---

### Шаг 3. Check house triggers

Прочитай PROFILE.md → `## ОВПД house style` → Триггер критерии.

Если house trigger met → как минимум **OVPD REQUIRED**.

Если house trigger **не** met — continue к Шагу 4 перед conclusion PROCEED. Некоторые
activities требуют ОВПД независимо от internal policy.

---

### Шаг 4. Mandatory ОВПД check (по 152-ФЗ)

#### 152-ФЗ обязательные triggers для ОВПД (ст.18.1)

С 01.09.2022 (ФЗ-266) оператор **обязан** проводить ОВПД при:

1. **Обработка спец.категорий ПДн** (ст.10): расовая принадлежность, политические
   взгляды, религиозные/философские убеждения, состояние здоровья, интимная жизнь,
   судимость, генетические данные → **OVPD REQUIRED**
2. **Биометрические ПДн** (ст.11) → **OVPD REQUIRED + согласие в письменной форме**
3. **ПДн несовершеннолетних** (ст.9 ч.4 — до 14 лет требует согласия родителя) →
   **OVPD REQUIRED**
4. **Автоматизированное принятие решений** (ст.16), создающее юридические
   последствия для субъекта или существенно затрагивающее права → **OVPD REQUIRED +
   право субъекта на возражение**
5. **Cross-border передача в третьи страны** (ст.12) → **OVPD + двухэтапное
   уведомление РКН** (с 01.03.2023):
   - Уведомление о намерении (до начала)
   - Уведомление о факте передачи
   - Штраф за неуведомление — до 18 млн руб.
6. **Поручение обработки ПДн третьему лицу** (ст.6 ч.3) — нужен ДОУ (договор об
   обработке) + проверка соответствия 152-ФЗ

#### Strong indicators (рекомендация — делать ОВПД)

- Новая технология или novel use существующей (AI / биометрия / новая аналитика)
- Дети и подростки
- Объединение datasets, которые не собирались вместе
- Обработка, которую субъекты не ожидают
- Targeted advertising по поведенческим данным
- Surveillance technologies (видеонаблюдение с face recognition)
- Cross-context behavioral advertising

Один или больше strong indicators **без** mandatory trigger → escalate to **OVPD
REQUIRED** (не OVPD + RKN notification, но флаг в output'е).

---

### Шаг 5. Privacy policy conflict check

Прочитай PROFILE.md → `## Политика обработки ПДн`. Check proposed activity против
**каждого** stated commitment.

#### Типичные конфликты для РФ

- Политика говорит "мы собираем X, Y, Z" — activity collects W → **обновление
  политики нужно** перед launch, или stop collecting W
- Политика "мы не передаём ПДн третьим лицам" — activity передаёт vendor'у → research
  попадает ли flow под "поручение обработки" (ст.6 ч.3 — нужен ДОУ) или **передачу**
  (нужно отдельное согласие субъекта)
- Политика specifies retention limits — activity retains data longer → **нарушение
  ст.5 ч.7** (хранение не дольше необходимости)
- Политика "используем только для [цель]" — activity uses for new purpose без свежего
  согласия → **нарушение ст.5 ч.2** (определённая цель)
- Политика specifies user rights — activity создаёт новую категорию ПДн, к которой
  rights процесс не построен → не нарушение, но **исправить процесс**

Если direct conflict → 🔴 **STOP**. Не "proceed с осторожностью" — policy conflict
must be resolved (update policy или redesign activity) перед continue.

---

### Шаг 6. Cross-border specifics

**Если activity включает cross-border передачу ПДн** — добавь специальные checks:

#### Куда передаётся?

- **Дружественные страны** (ЕАЭС, КНР, ОАЭ, БРИКС в основном): обычная процедура
  ст.12 152-ФЗ — двухэтапное уведомление РКН
- **Страны с надлежащим уровнем защиты** (перечень РКН) — упрощённая процедура
- **Недружественные страны** (US, EU, UK, JP): дополнительные restrictions, Указ
  Президента №79 — sanctions overlay

#### Локализация (ст.18 ч.5)

**Первичный сбор + хранение** ПДн российских граждан = **обязательно в РФ**.
Cross-border можно только **после** primary storage в РФ.

Если activity предполагает primary storage за рубежом → 🔴 **STOP** (нарушение
ст.18 ч.5; штраф с 30.05.2025 до 10 млн руб).

#### Уведомления РКН

С 01.03.2023 — двухэтапное:
1. О намерении (до начала передачи)
2. О факте передачи

Штраф за неуведомление — до 18 млн руб.

**Этим activity вашей компании выполняется?** Если нет — флагнуть в output'е как
**precondition** перед launch.

---

### Шаг 7. Output

```markdown
[МАРКИРОВКА из PROFILE.md]

## Privacy Use Case Triage: [Activity description]

**КЛАССИФИКАЦИЯ:** 🟢 PROCEED / 🟡 OVPD REQUIRED / 🟠 OVPD + RKN NOTIFICATION / 🔴 STOP

---

### Bottom line

[Одна строка — что это значит для launch]

---

**Activity:** [State the processing activity as understood]

**Subjects (категория ПДн субъектов):** [клиенты / сотрудники / кандидаты / др.]

**Categories of ПДн обрабатываемых:** [ФИО / адрес / email / биометрия / спец (ст.10) / др.]

**Sectoral overlay:** [None / банковская тайна / медицинская / тайна связи / др.]

**House trigger met:** [Yes / No / N/A]
**152-ФЗ mandatory trigger:** [Yes — [конкретный из ст.10/11/12/16/9/6 ч.3] / No]
**Privacy policy conflict:** [None / Yes — [specific conflict]]
**Cross-border:** [No / Yes — куда + статус уведомления РКН]

---

### Reasoning

[1-3 предложения. Для PROCEED — что makes safe. Для OVPD/STOP — что creates
obligation / conflict.]

---

[Если OVPD REQUIRED или OVPD + RKN NOTIFICATION — таблица conditions:]

| Requirement | Owner | Done? |
|-------------|-------|-------|
| Оценка вреда (ОВПД) по ст.18.1 152-ФЗ | DPO | ☐ |
| Уведомление РКН о намерении cross-border (ст.12 ч.5) | DPO + Юрист | ☐ |
| Согласие субъектов (если требуется ст.9) | DPO | ☐ |
| ДОУ с vendor (если поручение обработки ст.6 ч.3) | Юрист | ☐ |
| Обновление политики обработки ПДн | DPO | ☐ |
| Реализация прав субъектов (ст.14) для новой категории | Product + DPO | ☐ |
| ИБ требования (ст.19) — уровень защиты | ИБ | ☐ |

**Правовое основание** (ст.6 152-ФЗ): [Согласие ст.6 п.1.1 / Договор п.5 / Закон п.2
/ Жизненно важные интересы п.4 / Общественные интересы п.6 / Иное — точно указать]

**Next step — offer continue:**

> "Хочешь начать ОВПД сейчас? Запустим intake questions и produce assessment
> document без отдельной команды."

Если yes → load `pia-generation` skill.

---

[Если STOP:]

**Conflict:** [Конкретное обязательство политики / норма 152-ФЗ в конфликте]

**To proceed, one of these has to change:**

- **Option A — redesign activity** чтобы не создавать conflict
- **Option B — обновить политику обработки ПДн** (с notice субъектам если
  существенное изменение)
- **Option C — получить новое согласие** субъектов (если activity лишилось
  предыдущего основания)

Не предлагай path forward если его нет — если activity нельзя reconcile с lawful
basis, скажи это прямо.

---

### Шаг 8. Cross-plugin handoffs

**AI governance handoff:** если activity включает AI принимающий решения о
индивидах:

> "Activity включает AI decision-making. AI impact assessment likely required в
> дополнение к ОВПД. Используй `/ai-governance:aia-generation [activity]` для
> параллельного запуска — они не substitutes."

**Product handoff:** если new product launch:

> "Если это часть product launch, loop in product counsel.
> Используй `/consumer-product:launch-review` — он detect'ит privacy component и
> route'ит к этому plugin."

Флагни только relevant handoffs — не добавляй boilerplate'ом оба.

---

## Batch triage

Если пользователь презентует feature list, roadmap, или backlog — summary table
first, затем expand каждый non-PROCEED entry:

| # | Activity | Classification | Key condition / blocker |
|---|----------|:--------------:|--------------------------|
| 1 | [activity] | 🟢 Proceed | — |
| 2 | [activity] | 🟡 OVPD required | Lawful basis assessment needed; vendor ДОУ not in place |
| 3 | [activity] | 🟠 OVPD + RKN notification | Cross-border передача — уведомление РКН + переоформление согласий |
| 4 | [activity] | 🔴 STOP | Конфликт с политикой — purpose limitation, нет согласия на новую цель |

---

## Edge cases и failure modes

### "Это анонимизировано" не автоматически PROCEED

Спроси **как** anonymized и **realistic ли** re-identification given dataset. **В РФ
пseudonymized data всё ещё ПДн** (анонимизация требует уничтожения связи с субъектом
— ст.3 п.9 152-ФЗ "обезличивание").

### "Мы уже делаем что-то похожее" — не triage

Existing processing, которое никогда не assessed → не grandfather'ит new processing.
Если new activity materially different — triage заново.

### "Это просто пилот"

Pilot, который touches real user / employee ПДн → same triggers применяются. Apply
same classification.

### "Vendor handles all the privacy"

Vendor handles **infrastructure**. Вы всё ещё **оператор** определяющий цели. Если
ПДн flows к vendor → ДОУ обязателен (ст.6 ч.3) + triage applies к purpose.

### Inferred data и derived attributes count

Если activity генерирует inferred data (behavioral score, predicted preference) —
treat inferred attribute как ПДн. Не позволяй "мы просто вычисляем score" obscure
what the score represents.

### Биометрия для identification vs verification

Critical distinction:

- **Identification** (определить кто это среди N людей) — обычно нужно согласие в
  Единой биометрической системе (572-ФЗ)
- **Verification** (подтвердить что это тот же человек) — обычно проще, но всё ещё
  ст.11 152-ФЗ режим

### Cookies и аналитика

- **Strictly necessary** cookies — не требуют согласия (но рекомендуется в
  privacy notice)
- **Analytics / Marketing** cookies — требуют согласия по ст.9 + 152-ФЗ
- **Google Analytics** — auto-RED (квалифицирован РКН как нарушение локализации)
- РФ альтернативы: Яндекс.Метрика (РФ хостинг по дефолту), Mango Office, Roistat

### Targeted advertising

Поведенческая реклама на основе ПДн = обработка с целью продвижения товаров (ст.15
152-ФЗ — отдельные правила). **Согласие должно быть отдельным** от общего согласия
на обработку, **opt-in** по дефолту.

---

## Что этот skill НЕ делает

- Не пишет ОВПД — для этого `pia-generation`
- Не принимает risk decisions — flag'ает и classify'ет
- Не валидирует sanctions exposure (manual в Phase 1)
- Не делает legal opinion по конкретным фактам — это работа DPO/юриста

---

## Attribution

Adapted from [`privacy-legal/use-case-triage`](https://github.com/anthropics/claude-for-legal/blob/main/privacy-legal/skills/use-case-triage/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения от оригинала (substantial РФ adaptation):**

- **Classification scheme полностью переделан под 152-ФЗ:**
  - PIA / DPIA → **ОВПД** (оценка вреда по ст.18.1 152-ФЗ)
  - Добавлена 4-я категория: **OVPD + RKN NOTIFICATION** для cross-border / spec
- **Sectoral overlays полностью переписаны под РФ:**
  - GLBA → банковская тайна (395-1 ст.26)
  - HIPAA → медицинская тайна (323-ФЗ ст.13)
  - FERPA → нет прямого аналога (есть закон об образовании, отдельные нормы)
  - COPPA → ст.9 ч.4 152-ФЗ + ст.13 152-ФЗ (несовершеннолетние)
  - VPPA → нет аналога
  - TCPA → нет аналога
  - Добавлены: тайна связи (126-ФЗ), налоговая тайна (НК), адвокатская (ФЗ-63)
- **Mandatory triggers полностью переписаны под 152-ФЗ:**
  - ст.10 спец.категории
  - ст.11 биометрия
  - ст.9 ч.4 несовершеннолетние
  - ст.16 автоматизированное решение
  - ст.12 cross-border (двухэтапное уведомление РКН с 03.2023)
  - ст.6 ч.3 поручение обработки (ДОУ обязателен)
- **Cross-border specifics добавлены** — критично для РФ:
  - Локализация ст.18 ч.5 как gate
  - Дружественные / недружественные страны
  - Указ Президента №79 sanctions overlay
- **Edge cases переписаны под РФ практику:**
  - "Анонимизация" → "обезличивание" по ст.3 п.9
  - Cookies → Google Analytics auto-RED, РФ альтернативы (Яндекс.Метрика)
  - Targeted advertising → ст.15 152-ФЗ отдельные правила
  - Биометрия — distinction identification vs verification (572-ФЗ Единая
    биометрическая система)
- **Matter context секция убрана**
- **Path:** → `~/.ru-legal/profiles/data-protection/PROFILE.md`

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-18.

---

## Disclaimer

Этот skill производит preliminary triage для использования DPO / юристом /
руководителем product'а. Не legal advice.

**Особо важно для 152-ФЗ:**
- РКН практика быстро эволюционирует — verify актуальные positions через official
  channels (pd.rkn.gov.ru) для critical activities
- Sectoral overlays часто меняются — например, медицинская тайна имеет свою судебную
  практику отдельно от 152-ФЗ
- Для биометрии / спец.категорий — manual review DPO обязателен
- Cross-border ПДн — статус "недружественных" стран в любой момент может меняться

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
