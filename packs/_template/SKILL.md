---
name: skill-name-kebab-case          # snake-case-with-hyphens, must match directory name
description: |
  1-2 предложения. Что делает skill, кому полезен, когда применяется.
  Пример: "Анализ договора на риски. Юрист загружает текст договора + ИНН контрагента,
  получает structured отчёт со ссылками на актуальные нормы ГК + проверкой контрагента."

# === Tools (MCP integration) ===
required_tools:                       # без них skill не работает
  - pravo.search_npa
  - egrul.lookup_company
optional_tools:                       # graceful если недоступны
  - kad.search_cases
  - efrsb.check_bankruptcy

# === Версионирование ===
version: 1.0.0                        # semver: major.minor.patch
status: alpha                         # alpha | beta | stable

# === Maintenance metadata (ОБЯЗАТЕЛЬНО для всех skills) ===
last_legislative_update: "2026-05"    # YYYY-MM последней проверки актуальности НПА
domain_owner: "@github-username"      # GitHub handle ревьюера-эксперта (юрист-партнёр)
risk_level: medium                    # low | medium | high — насколько критична ошибка skill'а

# === Адаптация ===
ported_from: ""                       # путь в claude-for-legal если адаптировано (опц.)
adaptation_category: ""               # A (light) | B (moderate) | C (full rewrite) | "" если оригинал

# === НПА-ссылки (для refs-index) ===
references:
  - { code: "ГК РФ", article: "421", title: "Свобода договора" }
  - { code: "ФЗ", number: "152", year: "2006", title: "О персональных данных" }
  - { source: "ВС РФ", doc: "Постановление Пленума 49 от 25.12.2018" }
---

# {Заголовок skill'а на русском} — {1-line tagline}

## Назначение

Что именно делает этот skill. Когда юрист его использует. Что получает на выходе.

**Не для:** что НЕ должно делаться через этот skill (граница ответственности).

## Входные данные

Минимально необходимое от пользователя:
- **{Required input 1}** — описание формата
- **{Required input 2}** — ...

Опционально:
- **{Optional input}** — что улучшит точность

## Workflow

### Шаг 1 — {Что делаем}

Описание шага в **естественном языке**. Включая tool calls **в backticks**:

  Через `pravo.search_npa(query="ГК РФ ст.421", version="current")` получи
  актуальную редакцию статьи. Извлеки:
  - **Текущая редакция** (с датой последней правки)
  - **Номер закона который её изменил**

Если условие X — переходи к шагу 3.
Если условие Y — продолжай шаг 2.

### Шаг 2 — {Что делаем дальше}

  Параллельно вызови (можно одновременно):
  - `egrul.lookup_company(inn=user.inn)`
  - `efrsb.check_bankruptcy(inn=user.inn)`
  - `kad.search_cases(party_inn=user.inn, role="defendant")`

Из ответа извлеки {какие поля}.

### Шаг 3 — {Финал}

{Финальная процедура — что синтезируем, в каком формате выдаём}.

## Degraded mode

**ОБЯЗАТЕЛЬНАЯ СЕКЦИЯ.** Что делать когда MCPs недоступны.

**Если `pravo-mcp` недоступен:**
- Не используй цитаты НПА из своей training data (могут быть устаревшие)
- В output помеч: "⚠ Редакция статьи не сверена — рекомендуется проверка через pravo.gov.ru"

**Если `egrul-mcp` недоступен:**
- Продолжай анализ договора по тексту
- В output: "⚠ Контрагент по ЕГРЮЛ не проверен. Перепроверить вручную через nalog.gov.ru"

## Финальный отчёт

Структура output:

1. **Сводка** (3-5 строк) — главный вывод
2. **Анализ {что}** — детально
3. **Применимые НПА** — со ссылками на актуальную редакцию (что подтверждено через MCP)
4. **Найденные риски** — с уровнями: critical / major / minor
5. **Рекомендации** — конкретные next steps для юриста
6. **Проверенные источники** — кто/что верифицировано (✅) и не (⚠)

### Verified vs unverified маркеры

В тексте output используй:
- `[verified: pravo, 2026-05-15]` — после цитат НПА проверенных через MCP
- `[verified: egrul, 2026-05-26]` — после фактов о контрагенте
- `[⚠ unverified]` — если MCP был недоступен и используется guess

## Тестовые кейсы (Gold dataset)

Эталонные кейсы для regression testing → `tests/gold/{pack}/{skill}/`:
- `case-001-typical.yaml` — типовой кейс
- `case-002-edge.yaml` — edge case
- `case-003-broken-input.yaml` — невалидный input должен правильно отклоняться

## Известные ограничения

- **Не покрывает:** {что вне scope}
- **Спорные ситуации:** {где skill даёт mediocre результат}
- **Требует human review:** {когда обязательно перепроверять}

## Связанные skills

- См. также `{other-pack}/{other-skill}` — для {случай}
- Используется вместе с `{pack}/{skill}` — для {workflow}

## Версии (changelog)

- **1.0.0** (YYYY-MM-DD) — initial release
