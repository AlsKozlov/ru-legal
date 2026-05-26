---
name: reg-feed-watcher
description: |
  Killer skill для regulatory-monitor. Daily/weekly scan новых НПА в sphere of
  interest клиента. Source — pravo.gov.ru (official) + sectoral regulators
  (ЦБ, ФНС, РКН, ФАС, Минцифры). Output: structured digest с classification
  (critical / material / informational).
required_tools:
  - pravo.search_npa
optional_tools:
  - cbr.lookup_bank_by_bic
  - egrul.lookup_company
version: 2.0.0
status: alpha
last_legislative_update: "2026-05"
domain_owner: TBD
risk_level: medium
references:
  - { code: "ФЗ-149", title: "Об информации, информационных технологиях и о защите информации" }
  - { code: "Указ Президента", number: "763", year: "1996", title: "О порядке опубликования НПА" }
---

# /reg-feed-watcher — Сканер регуляторных изменений

## Назначение

Регулярный (daily/weekly) scan новых нормативных актов РФ в **sphere of
interest** конкретного клиента. Возвращает structured digest с
classification по уровню важности для бизнеса клиента.

**Применяется в:**
- In-house юр.отдел — мониторинг изменений регулирования
- Compliance team — отслеживание новых требований
- Юр.фирмы — ежемесячные client alerts

**Не для:**
- Real-time alerts (это работа отдельной cron job через [ru-legal-agent harness](../../../README.md))
- Полного юридического анализа изменения (это `/gap-surfacer` + `/policy-redraft`)

## Pre-flight

1. **cold-start-interview пройден** — `client_profile.areas_of_interest` известны
2. **pravo MCP доступен** — без него skill не работает
3. **last_scan_date известен** — period scan-а определяется относительно него

## Источники данных

| Источник | Что покрывает | Update freq | Доступ |
|---|---|---|---|
| `pravo.gov.ru` | Все официально опубликованные НПА РФ | Daily | через `pravo-mcp` |
| Сайт Банка России | Положения / Указания (банковское/страховое) | Weekly | через `cbr-mcp` (когда будет API) |
| Сайт ФНС | Налоговые приказы / письма | Weekly | через `fns-extended-mcp` (planned) |
| Сайт РКН | 152-ФЗ / реклама / блокировки | Weekly | scraping (planned) |
| Сайт ФАС | Антимонопольные акты | Weekly | scraping (planned) |
| Минцифры | IT-аккредитация / реестр ПО | Monthly | через open data API |
| Постановления Пленума ВС РФ | Прецедентная практика | Quarterly | через `gas-pravosudie-mcp` (planned) |

**Текущий статус:** `pravo-mcp` работает, остальные — в roadmap. Skill работает
с `pravo-mcp` базово, остальные источники подключаются по мере готовности.

## Workflow

### Шаг 1 — Определение периода и охвата

На основе input от пользователя ИЛИ дефолтных настроек client_profile:

- **Period** — `today` / `last_7_days` / `last_30_days` / `since={last_scan}`
- **Areas of interest** — берём из `client_profile.areas` (трудовое, налоговое,
  152-ФЗ, IT-регулирование, и т.д.)
- **NPA types** — обычно: ФЗ, Указы Президента, Постановления Правительства,
  Приказы министерств. Можно фильтровать по client_profile.

Если client_profile отсутствует — попроси пользователя указать areas of interest
перед продолжением.

### Шаг 2 — Запрос pravo MCP для каждой area

Для каждой `area` из areas_of_interest вызови:

  Через `pravo.search_npa(query=area_keywords, date_from=period_start, date_to=today)`
  получи список НПА опубликованных за период.

Где `area_keywords` это поисковые термины для области. Примеры:

- **Трудовое:** `["трудовой кодекс", "оплата труда", "увольнение", "охрана труда"]`
- **152-ФЗ / ПДн:** `["персональные данные", "Роскомнадзор", "ПДн", "152-ФЗ"]`
- **Налоговое:** `["налоговый кодекс", "НДС", "налог на прибыль", "ФНС приказ"]`
- **IT-регулирование:** `["информационные технологии", "программное обеспечение",
  "реестр ПО", "Минцифры"]`
- **Корпоративное:** `["акционерное общество", "ООО", "ЦБ", "корпоративное"]`

Аккумулируй результаты в плоский список НПА для дальнейшей классификации.

### Шаг 3 — Классификация каждого НПА

Для каждого НПА определи **tier важности** на основе:

1. **Совпадение с client.protected_npa_list** — какие НПА затрагивают конкретные
   нормы на которых основаны ЛНПА клиента (внутренние политики, договоры,
   процессы)?
2. **Тип акта** — ФЗ > Указ > Постановление Правительства > Приказ министерства
   > Письмо/Разъяснение (informational only)
3. **Дата вступления в силу** — если < 30 дней до вступления → tier выше
4. **Сфера применения** — отраслевые или общеприменимые

Применяй классификацию:

| Tier | Критерий | Action |
|---|---|---|
| 🔴 **Critical** | Прямо меняет норму, на которой основаны клиентские ЛНПА; критичный отраслевой акт | Immediate review (24-48 часов) + gap analysis |
| 🟡 **Material** | Меняет связанные нормы; может affect процессы клиента | Review в течение недели |
| 🟢 **Informational** | В области интереса, но не влияет напрямую | Log в archive, ежемесячный sweep |

### Шаг 4 — Генерация digest

Структурируй output:

```
# Regulatory Feed — за период {period}

## 🔴 Critical (требуют immediate action)

1. **{Название акта}** (ФЗ-XX от DD.MM.YYYY)
   - **Что изменилось:** {краткое описание}
   - **Затронуто:** {конкретные ЛНПА клиента / процессы}
   - **Срок вступления в силу:** DD.MM.YYYY (через {N} дней)
   - **Recommended action:** Запустить `/gap-surfacer` для затронутых ЛНПА
   - **Source:** {URL pravo.gov.ru} [verified: pravo, {date}]

## 🟡 Material

[Same format]

## 🟢 Informational

[Same format — короче]

## Summary

- Total NPA reviewed: {N}
- Critical: {N} / Material: {N} / Informational: {N}
- Next scheduled review: DD.MM.YYYY
```

### Шаг 5 — Downstream actions

Для каждого 🔴 critical НПА — рекомендуй пользователю запустить:

- **`/policy-diff <npa-id>`** — посмотреть точный diff vs предыдущая редакция
- **`/gap-surfacer <npa-id>`** — определить какие клиентские ЛНПА затронуты
- **`/policy-redraft <local-policy-id>`** — auto-draft обновлённой версии ЛНПА

Для 🟡 material — обычно ограничиваемся `/policy-diff`.

Для 🟢 informational — никаких немедленных действий, только log.

## Format для TG bot уведомлений

Compact версия digest для daily TG notification:

```
📊 Regulatory digest за {DD.MM.YYYY}

🔴 {N} critical:
   - {краткое название акта}
🟡 {N} material
🟢 {N} informational

Полный digest: /skill regulatory-monitor/reg-feed-watcher
```

## Degraded mode

**Если `pravo-mcp` недоступен (главный источник):**
- Skill не может выполнить основную задачу — нет данных о новых НПА
- В output: `⚠ pravo.gov.ru недоступен. Невозможно получить список новых НПА
  за период. Попробуйте позже или проверьте вручную через pravo.gov.ru`
- НЕ генерируй фейковые НПА из training data — это **критически опасно**
  для compliance-агента (галлюцинированные "новые" акты могут привести к
  unnecessary policy changes)

**Если sectoral sources недоступны (cbr/fns/rkn):**
- Продолжай с тем что есть из pravo
- В output помечай: `⚠ ЦБ РФ источник не проверен — может не быть в digest
  банковских/страховых актов`

## Финальный отчёт

См. секцию "Шаг 4 — Генерация digest" выше.

Включай:
- Timestamp scan'а
- Период (date_from, date_to)
- Список источников которые были опрошены (verified ✅ / unverified ⚠)
- Total counts по tiers
- Recommendations для downstream actions

## Тестовые кейсы (Gold dataset)

`tests/gold/regulatory-monitor/reg-feed-watcher/`:
- `case-001-typical-week.yaml` — типичная неделя, mix tiers
- `case-002-critical-fz-change.yaml` — критическое изменение ФЗ
- `case-003-empty-period.yaml` — пустой period (no NPA)
- `case-004-pravo-down.yaml` — degraded mode (pravo unreachable)
- `case-005-multiple-areas.yaml` — клиент с 5 areas of interest

## Известные ограничения

- **Не выполняет рассылку** — это работа TG bot / email service в harness
- **Не updates ЛНПА automatically** — для этого `/policy-redraft` с HITL approval
- **Не replaces юр.эксперта** для interpretation сложных изменений
- **Зависит от pravo-mcp** — single source of truth (плюс sectoral overlays)
- **Не покрывает региональные акты** (только федеральный уровень)

## Связанные skills

- `regulatory-monitor/policy-diff` — diff НПА vs previous version
- `regulatory-monitor/gap-surfacer` — какие клиентские ЛНПА затронуты
- `regulatory-monitor/policy-redraft` — auto-draft updated ЛНПА

## Версии

- **2.0.0** (2026-05-26) — Rewrite: убрана псевдо-Python нотация (нарушала
  project convention), workflow теперь в прозе с tool calls в backticks.
  Добавлен degraded mode. Добавлен references frontmatter.
- **1.0.0** (2026-05-20) — Initial port from Anthropic claude-for-legal
  (regulatory-legal/reg-feed-watcher). Категория B adaptation.

## Attribution

Adapted from `regulatory-legal/reg-feed-watcher` (Apache 2.0, © 2026 Anthropic PBC).
Категория B adaptation: US Federal Register / state feeds → РФ pravo.gov.ru +
sectoral regulators. Sectoral overlays РФ-specific.
