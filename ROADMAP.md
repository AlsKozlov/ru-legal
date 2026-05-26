# ROADMAP

> Live-документ. Обновляется по факту прогресса + community feedback.
> Последнее обновление: 2026-05-26

## Vision

**ru-legal — open-source инфраструктура для работы юриста с AI в РФ.**

Цель: покрыть **85% популярных юр.вопросов** через комбинацию skills (методология) и MCP (доступ к госреестрам). Apache 2.0, self-hosted, works с любым MCP-клиентом.

**Что мы делаем хорошо** (отличие от закрытых решений):
- 🔓 Open-source — fork, modify, audit
- 🧩 MCP-стандарт — works с Claude Code / Cursor / Continue / LangGraph
- 🇷🇺 Multi-LLM — YandexGPT / GigaChat / Anthropic / OpenAI / DeepSeek / vLLM
- 🏛 Direct access к госреестрам (8 MCPs) — без посредников

---

## Текущее состояние (v0.1.0, май 2026)

✅ **145 skills** в 14 паках:
- contract-law (15), labor-law (14), corporate-law (12)
- tax-law (11), ip-law (10), real-estate (10)
- compliance-aml (9), data-protection (12), consumer-product (8)
- public-procurement (10), AI governance (10)
- regulatory-monitor (8), administrative-law (8), litigation (8)

✅ **8 MCP-серверов** к госреестрам:
- pravo-mcp, egrul-mcp, kad-mcp, efrsb-mcp
- rospatent-mcp, zakupki-mcp, rosreestr-mcp
- ru-legal-mcp (агрегатор)

✅ Совместимость: Claude Code, Cursor, Continue, LangGraph

**Что отсутствует** (явные дыры):
- Суды общей юрисдикции (СОЮ) — ~90% юр.практики (трудовые, семейные, наследственные споры)
- Семейное / наследственное / жилищное право
- Процессуальные документы (иски, отзывы, жалобы)
- Банкротство физлиц
- Compliance suite (санкции, лицензии, реестр МСП)

---

## Phase 1 — закрыть основные дыры (июнь-июль 2026)

**Цель:** покрытие популярных юр.вопросов 40% → 70%.

### MCPs (3 новых сервера)

#### 🔴 `gas-pravosudie-mcp` — суды общей юрисдикции
- `sudrf.ru` — federal портал СОЮ
- `vsrf.ru` — Верховный Суд РФ (определения, обзоры)
- `mos-gorsud.ru` — Мосгорсуд (отдельная картотека)

**Без этого MCP не покрываем больше половины юр.практики.** Top priority.

#### 🟡 `compliance-mcp` — объединённый сервер
- `check_sanctions_lists()` — Росфинмониторинг + ОФАК + ЕС
- `check_msp_status()` — Реестр МСП ФНС
- `check_blocked_accounts()` — счета юрлица в ФНС
- `check_disqualified_persons()` — реестр дисквалифицированных
- `check_license(ogrn)` — лицензии регулирующих органов

#### 🟢 `documents-mcp` — генератор шаблонов
- `draft_claim_template(case_type, jurisdiction)`
- `draft_appeal_template(case_type)`
- `format_motion(motion_type)`

### Skills (4 новых пака, ~40 skills)

#### `family-law` (10-12 skills)
- divorce-petition-prep, alimony-calculation, alimony-recovery
- property-division, child-custody, prenuptial-agreement-draft
- paternity-determination, adoption-petition
- parental-rights-deprivation, post-marital-disputes

#### `inheritance-law` (8-10 skills)
- estate-opening, acceptance-rejection
- mandatory-share-calc, will-validity-challenge
- heirs-dispute, estate-administrator-appointment
- intestate-succession, foreign-elements-inheritance

#### `process-documents` (12-15 skills) — cross-cutting
- claim-draft-civil, claim-draft-arbitration
- response-draft, appeal-draft, cassation-draft
- supervisory-complaint
- motion-judge-recusal, motion-evidence-collection, motion-expertise
- settlement-agreement, statement-of-claim-amendment
- procedural-deadlines-calc

#### `personal-bankruptcy` (8-10 skills)
- bankruptcy-filing-prep, creditor-protection
- extrajudicial-bankruptcy (через МФЦ)
- restructuring-plan, debt-discharge
- bankruptcy-eligibility, asset-protection

**Метрика Phase 1:** ~25 new MCP tools + 40 new skills.

---

## Phase 2 — Business & Financial domains (август-сентябрь 2026)

**Цель:** покрытие 70% → 85%.

### MCPs (3 новых сервера)

#### `banking-finance-mcp`
- ЦБ РФ API (справочник банков, отозванные лицензии)
- АСВ (страхование вкладов, банкротство банков)
- Реестр платежных систем ЦБ
- Реестр МФО

#### `real-estate-extended-mcp`
- Лесной реестр (земли лесфонда)
- Реестр объектов культурного наследия
- Публичная кадастровая карта
- Реестр СРО строителей/проектировщиков

#### `public-disclosure-mcp`
- `e-disclosure.ru` — раскрытие публичных АО
- Реестр аффилированных лиц ЦБ
- Раскрытие банков-эмитентов

### Skills (3 новых пака, ~30 skills)

#### `housing-law` (10 skills)
- communal-services-disputes, management-company-claims
- neighbor-disputes, redevelopment-permits
- equity-construction-protection, privatization-disputes
- eviction-defense, housing-conditions-claims

#### `financial-disputes` (8-10 skills)
- osago-insurance-disputes, kasco-disputes
- bank-account-blocking-appeal, microloan-disputes
- failed-bank-deposit-recovery
- credit-card-disputes, failed-payment-recovery

#### `social-benefits` (10 skills)
- pension-assignment, pension-recalculation
- maternity-capital-disputes, disability-status-appeal
- social-benefit-denial-appeal, benefit-priority-categories

---

## Phase 3 — Specialized + Community (октябрь-ноябрь 2026)

**Цель:** добить niche домены + переход на community-driven contributions.

### MCPs (2-3 niche)
- `sanctions-international-mcp` — OFAC + EU + UK lists
- `pravo-ru-news-mcp` — daily обзор изменений законодательства
- `b2b-center-mcp` — коммерческие тендеры

### Skills (2-3 новых пака, ~20 skills)
- `administrative-extended` (10) — ГИБДД, миграция, КоАП
- `medical-disputes` (5-7) — мед.споры, ОМС, пациентские права
- niche packs по запросам community

### Quality Infrastructure (критично!)

- **Legal Review Pipeline** — каждый skill review'ится практикующим юристом до merge
- **Gold Dataset** — 30-50 размеченных кейсов per pack, regression tests
- **Audit & Disclaimer** infrastructure — verified/unverified маркеры в каждом output

---

## Phase 4 — Sister project: ru-buh (декабрь 2026 - февраль 2027)

> Когда ru-legal достиг traction (500+ ⭐, активный community, 3-5 paid pilots) — стартуем отдельный проект для **бухгалтеров**.

**Логика:** аудитория бухгалтеров в РФ ~500k (vs 150k юристов). Workflow-heavy, MCP-friendly, нет open-source альтернатив.

**Архитектура:**
- Отдельный repo `ru-buh` (skills + MCPs для бухгалтерии)
- **Shared infrastructure** с ru-legal (тот же ru-legal-agent harness)
- Shared MCPs где есть overlap (ФНС, ЕГРЮЛ)
- Cross-promotion между проектами

См. [ru-buh repo](https://github.com/AlsKozlov/ru-buh) (создание в Phase 4).

---

## Долгосрочное (2027+)

### Возможные направления:
- **ru-legal-agent v1.0** — production-grade harness (LangGraph + checkpointing + HITL)
- **Telegram бот для SMB-юристов** — easy entry для тех кто не использует Claude Code
- **Web UI** — для юр.фирм с teams
- **Custom enterprise mirrors** — self-hosted database с госреестрами для compliance-heavy клиентов
- **Mobile companion** — quick checks от телефона
- **API for legaltech vendors** — embed ru-legal в их продукты

### Возможные новые домены:
- `ru-fintech` — банкинг, инвестиции, регулирование
- `ru-medical` — мед.право детально (помимо medical-disputes)
- `ru-customs` — таможенное право
- `ru-agro` — аграрное право

---

## Как контрибьютить

### Низкий порог входа

1. **Issue с предложением skill** — описываете workflow, мы обсуждаем
2. **PR с новым skill** — используйте `packs/_template/SKILL.md`
3. **PR с новым MCP** — используйте `mcps/_template/`
4. **Review существующих skills** (если вы юрист) — комментируйте в issues

### Recognition

- Имя в `CONTRIBUTORS.md`
- Mention в GitHub Releases
- (когда будет коммерческий tier) — first paid clients = опытные contributors

### Партнёры-юристы (мы ищем 3-5 человек)

Если вы практикующий юрист в области из roadmap (family, inheritance, housing, bankruptcy, financial disputes) — нужны:
- Review новых skills вашего домена (1-2 часа в неделю)
- Тестирование на реальных кейсах (анонимизированных)

В обмен:
- Recognition как domain owner в README
- Early access к ru-legal-agent (когда выйдет)
- Соавторство в публикациях / case studies
- (опционально) первые paid лицензии когда монетизируем

Связь: @alskozlov (Telegram) или Issues с тегом `domain-owner-application`.

---

## Метрики прогресса (будем обновлять)

| Метрика | Текущая (v0.1.0) | Phase 1 цель | Phase 2 цель | Phase 3 цель |
|---|---|---|---|---|
| Packs | 14 | 18 | 21 | 23 |
| Skills | 145 | 185 | 215 | 235 |
| MCPs | 8 | 11 | 14 | 16-17 |
| GitHub ⭐ | 0 | 200 | 500 | 1000 |
| Contributors | 1 | 5 | 15 | 30 |
| Domain owners (юристы-партнёры) | 0 | 3 | 5 | 8 |

---

## Подписка на updates

- [⭐ Star repo](https://github.com/AlsKozlov/ru-legal)
- [Watch releases](https://github.com/AlsKozlov/ru-legal/releases) — только когда новый release
- [Telegram канал](https://t.me/alskozlov) — статьи о развитии проекта
- [Discussions](https://github.com/AlsKozlov/ru-legal/discussions) — Q&A, feature requests

---

Roadmap корректируется на основе community feedback. Голосуйте через 👍 на issues с тегом `roadmap-vote`.
