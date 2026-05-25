---
name: matter-intake
description: >
  Intake нового судебного дела — uniform 10 шагов: идентификация, conflicts check,
  источник (как пришло), risk triage, материальность, outside counsel, ответственные,
  обеспечение доказательств, key dates, initial posture. Пишет matter.md, history.md
  и appendит structured row в _log.yaml. Используй когда пользователь говорит "новое
  дело", "intake этого matter'а", или хочет внести new matter в портфолио.
argument-hint: "[optional matter name]"
user_invocable: true
ported_from: litigation-legal/matter-intake
ported_at: 2026-05-18
adaptation_category: A
---

# /matter-intake (intake нового судебного дела)

## Назначение

Каждое новое дело проходит **uniform intake** чтобы портфель оставался comparable.
Uniform rows в `_log.yaml` позволяют status skill агрегировать. Narrative в matter.md
captures что row не может. History file — event record.

## Pre-flight

Прочитай:
- `~/.ru-legal/profiles/litigation/PROFILE.md` → risk calibration (триаж thresholds,
  материальность), landscape (stakeholders, outside counsel bench)
- `~/.ru-legal/profiles/litigation/matters/_log.yaml` — для confirm slug uniqueness

---

## Intake (10 шагов)

### 1. Идентификация

- **Matter name** (как commonly referenced, например "Acme v. Us 2026", "Налоговый
  спор по ВНП за 2024")
- **Counterparty** (контрагент по спору + ИНН/ОГРН если ЮЛ)
- **Matter type:**
  - `contract` — договорной (ГК ст.450-453)
  - `tax` — налоговый (НК)
  - `corporate` — корпоративный (ФЗ "Об ООО" / "Об АО")
  - `employment` — трудовой (ТК)
  - `bankruptcy` — банкротство (127-ФЗ)
  - `antimonopoly` — антимонопольный (ФАС, 135-ФЗ)
  - `ip` — ИС (ГК ч.4)
  - `administrative` — административный (КоАП)
  - `criminal-economic` — уголовный экономический (УК)
  - `other`

- **Наша роль:**
  - `истец / plaintiff` — мы инициируем
  - `ответчик / defendant` — нам предъявляют
  - `третье лицо` — заинтересованная сторона
  - `заявитель` — административный / банкротство
  - `обвиняемый` (для уголовных)

  Если PROFILE.md `## Side` указывает default (plaintiff/defense) — pre-fill из default'а
  и confirm. Если `varies by matter` — ask cold.

- **Юрисдикция / Forum:**
  - **Арбитражный суд** (для предпринимательских) — какой округ?
  - **Суд общей юрисдикции** (СОЮ) — для физлиц
  - **КАС РФ** — административные споры
  - **МКАС при ТПП РФ** — международный коммерческий арбитраж
  - **Третейский суд** — какой
  - **Регулятор** (ФАС / РКН / ЦБ) — досудебный этап

### 2. Conflicts check

**ГЕЙТ** — без этого шага intake не proceed'ит.

В РФ "конфликт интересов" не имеет такой же строгой нормативной базы как в US
(нет model rules of professional conduct в том же виде). Но для адвокатов
действует **ст.6 ФЗ-63** "Об адвокатской деятельности" — нельзя выступать против
интересов лица, которому ранее оказывал юр.помощь.

Для in-house — конфликты обычно corporate (мы уже представляем материнскую vs
дочернюю, etc.).

**Status:** `cleared | pending | not-run | waived`
**Method:** `outside-counsel | system-check | informal | corporate-legal`
**Cleared by:** name / team
**Cleared date:** YYYY-MM-DD
**Checked against:** контрагент, аффилированные ЛИЦА (через ЕГРЮЛ если есть ИНН),
opposing counsel (если известен), key witnesses
**Notes:** anything flagged but cleared

**Behavior:**
- `cleared` → proceed
- `pending` → proceed with флагом, surface на каждом /matter-update
- `not-run` → **STOP gate.** Три пути: run сейчас / mark pending с owner+due / bypass
  с rationale (documented в `conflicts.override`)
- `waived` → требуется waiver rationale

### 3. Источник

Как пришло?

- `complaint-served` → исковое заявление получено (если ответчики)
- `pretensia-received` → досудебная претензия получена (АПК ст.4 — обязательный
  претензионный порядок для большинства споров)
- `subpoena` → запрос суда / следствия / прокуратуры (АПК ст.66, ст.74, УПК)
- `regulator-inquiry` → запрос регулятора (РКН / ФАС / ЦБ / др.)
- `internal-report` → внутренний report (compliance, whistleblower)
- `pre-suit-threat` → угроза иска без официального requestа
- `tax-audit-act` → акт налоговой проверки (НК)
- `koap-protocol` → протокол КоАП

**Seed doc:** "Если есть initiating документ (иск / претензия / протокол / акт) —
прикрепи путь. Это sharpens intake."

### 4. Risk triage

По калибровке PROFILE.md:

- **Severity:** high / medium / low
- **Likelihood:** high / medium / low
- **Risk rating** (по матрице): critical / high / medium / low
- **Damages exposure** (приближённая оценка в рублях)
- **Non-monetary exposure:**
  - Реальное исполнение (ст.397 ГК — обязать сделать что-то)
  - Запрет (injunctive relief)
  - Прецедент (если решение может повлиять на другие сделки)
  - Реputational
  - Регуляторные последствия (отзыв лицензии, etc.)
  - Уголовный риск (если экономический спор может перейти в уголовное)

### 5. Материальность

Против house thresholds:

- **Не material:** ниже threshold X (default — 1 млн руб)
- **Material:** между X и Y (default — 10 млн руб)
- **Сильно material:** выше Y, требует sign-off Board

### 6. Outside counsel

- **Нужен внешний адвокат?** Да / Нет / Возможно
- **Если да:**
  - Конкретный кандидат (из PROFILE.md → outside counsel bench)
  - Биллинг (почасовой / fixed / contingency)
  - Engagement letter (есть / нужен)
- **Адвокатская тайна:** включается только если outside counsel — **адвокат с
  удостоверением ФПА** (ФЗ-63). In-house counsel privilege в РФ НЕ имеет.

### 7. Внутренние ответственные

- **Lead attorney:** [имя]
- **Backup attorney:** [имя]
- **Business owner:** [имя — кто внутри бизнеса owns this matter]
- **Paralegal / Support:** [...]

### 8. Обеспечение доказательств (РФ аналог legal hold)

**Не "legal hold"** как US ESI preservation, но похожая идея:

- **Необходимо ли preservation документов?** (для будущего иска / защиты)
  - АПК ст.72 — обеспечение доказательств арбитражным судом до подачи иска
    (нечасто, но возможно)
  - Внутренние preservation orders — компания просит сотрудников не удалять
    relevant docs
  - Email holds / file-share holds
- **Источник риска:** какие документы / системы / люди?
- **Ответственный:** IT + DPO (если ПДн затрагиваются)

### 9. Key dates

Critical для litigation:

| Тип даты | Норма | Срок |
|----------|-------|------|
| Срок ответа на досудебную претензию | АПК ст.4 ч.5 | 30 дней (если иное не установлено) |
| Срок исковой давности (общий) | ГК ст.196 | 3 года |
| Срок исковой давности (специальный) | ГК ст.197 / спец.нормы | разный |
| Срок подачи иска после досудебки | АПК ст.4 | по истечении срока ответа |
| Срок подачи в АС после получения копии решения нижестоящего | АПК ст.259 (апелляция) | 1 месяц |
| Срок кассации | АПК ст.276 | 2 месяца |
| Срок надзорной жалобы | АПК ст.291.1 | 3 месяца |

Заполни известные дедлайны.

### 10. Initial posture

Как мы планируем подходить?

- `defend-aggressively` — защищаем активно
- `defend-pragmatically` — защищаем но готовы settling
- `pursue-aggressively` — нападаем активно
- `pursue-pragmatically` — заявляем но готовы settle
- `settle-fast` — настроены на mediation / fast settle
- `wait-and-see` — мониторим, ждём действий counterparty

---

## Создать matter folder

После intake — generate slug (lowercase, hyphens, year — например "acme-vs-us-2026"
или "tax-vat-2024-q1").

Создать:

1. `~/.ru-legal/profiles/litigation/matters/[slug]/matter.md` — full narrative
   intake
2. `~/.ru-legal/profiles/litigation/matters/[slug]/history.md` — seeded с intake
   как первая запись
3. Append structured row в `~/.ru-legal/profiles/litigation/matters/_log.yaml`:

```yaml
- slug: acme-vs-us-2026
  name: "Acme v. Us 2026"
  type: contract
  role: defendant
  jurisdiction: "АС г. Москвы"
  counterparty: "ООО Акме"
  counterparty_inn: "7707083893"
  source: complaint-served
  conflicts:
    status: cleared
    method: corporate-legal
    cleared_by: "Петров П.П."
    cleared_date: 2026-05-18
  risk_rating: high
  severity: high
  likelihood: medium
  damages_exposure_rub: 25000000
  materiality: material
  outside_counsel: "Адвокатское бюро X"
  lead_attorney: "Иванов И.И."
  business_owner: "petrov@company.ru"
  preservation_order: yes
  key_dates:
    next_deadline: 2026-06-15
    next_deadline_desc: "Подача отзыва на иск"
    sol_expires: 2027-03-01  # срок исковой давности
  posture: defend-pragmatically
  status: active
  created_at: 2026-05-18
  last_updated_at: 2026-05-18
```

4. Confirm с user: "Вот row которую я запишу — есть правки?"

---

## Attribution

Adapted from [`litigation-legal/matter-intake`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/matter-intake/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения от оригинала:**
- **Matter types** расширены для РФ: tax (НК), corporate (ООО/АО), bankruptcy (127-ФЗ),
  antimonopoly (ФАС), tax-audit-act (акт ВНП), koap-protocol
- **Юрисдикция/Forum** под РФ — АС / СОЮ / КАС / МКАС / третейский / регулятор
- **Источник** дополнен РФ-specific: pretensia-received (АПК ст.4 досудебка),
  tax-audit-act, koap-protocol
- **Адвокатская тайна** explicit — только для адвокатов ФПА (ст.6 ФЗ-63), in-house без
- **Обеспечение доказательств** заменено на АПК ст.72 (не US ESI)
- **Key dates** — РФ сроки исковой давности (ст.196-197 ГК), apellation (АПК ст.259),
  досудебка (АПК ст.4)
- **Path:** → `~/.ru-legal/profiles/litigation/`

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.
**Adapted by:** ru-legal contributors, 2026-05-18.

---

## Disclaimer

Этот skill — intake utility для litigation team. Не legal advice. Final risk
assessment + strategy за lead attorney + GC.

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
