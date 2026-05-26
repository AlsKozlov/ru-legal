# MCP Status — Brutal Honesty Edition

> **Этот файл говорит правду о том, что работает, а что нет.** Обновляется еженедельно по результатам live endpoint tests.
> Последний audit: 2026-05-26
> Next audit: 2026-06-02

## Manifesto

В open-source legaltech полно проектов которые показывают impressive feature lists, а на запросах падают. Мы делаем иначе.

**Status legend:**
- 🟢 **GREEN** — endpoints протестированы на этой неделе, работают, output как описан
- 🟡 **YELLOW** — частично работает или работает с известными ограничениями
- 🔴 **RED** — не работает, ищем решение
- ⚫ **BLACK** — известно что не будет работать без paid feed / нового подхода

Каждый понедельник CI прогоняет smoke tests против реальных endpoints и обновляет этот файл.

---

## Сводная таблица

| MCP | Статус | Tools | Endpoint Health | Critical Issues |
|---|---|---|---|---|
| **`cbr`** ⭐ NEW | 🟢 **GREEN** | 5 | ✅ XML_daily + HTML key rate работают | None — first fully working MCP |
| `pravo` | 🟡 YELLOW | 5 | HTTP-only (TLS broken upstream с 2026-05-21) | Hardcoded Basic auth, нужен env-override |
| `egrul` | 🟡 YELLOW | 4 | ✅ работает с API ключом | Free tier 800 req total (не в день) |
| `kad` | 🟡 YELLOW ↑ | 4 | Browser UA добавлен 2026-05-26 — нужен ре-тест | Anti-bot может продолжать резать |
| `efrsb` | 🟡 YELLOW ↑ | 4 | Browser UA добавлен 2026-05-26 — нужен ре-тест | Anti-bot may still block |
| `rospatent` | ⚫ BLACK | 6 | ❌ HTTP 404 ВСЕ 4 endpoints | **Endpoints не существуют — спекулятивная реализация. Нужен полный rewrite на HTML scraping или paid API.** |
| `rosreestr` | 🟡 YELLOW | 5 | DDoS-Guard timeout | `get_encumbrances` misleading (всегда redirect на платную EGRN) |
| `zakupki` | 🟡 YELLOW | 5 | endpoint suspect (возможно не существует) | Нужна верификация `/epz/api/orders/search` |
| `ru-legal-aggregator` | 🟡 YELLOW | 4 + 145 skills | local FS only | `RU_LEGAL_PACKS_ROOT` env var required (НЕ документирован) |
| `sanctions` (planned) | ⚫ BLACKED | — | ❌ fedsfm/minjust не имеют публичных machine-readable endpoints | **JS-rendered tables, no XML/JSON dump. Нужен playwright или paid feed.** |

---

## Детально по каждому MCP

### pravo 🟡

**Что обещано:** Поиск НПА с актуальной редакцией.
**Что работает:** Базовый search/get НПА через HTTP (TLS на стороне pravo.gov.ru сломан с 2026-05-21, поэтому идём по `http://`).
**Что НЕ работает:**
- HTTPS upgrade fail (TLS broken upstream)
- Hardcoded Basic auth (`ips:newpassword2020`) может сломаться при ротации
- Все TLS-aware HTTP клиенты (например WebFetch) автоматически апгрейдят до HTTPS → timeout

**Test result (2026-05-26):**
```
GET http://publication.pravo.gov.ru/api/Documents?name=152-ФЗ → 200 OK (через httpx без HTTPS upgrade)
```

**Workaround:** в коде используется явный `http://`. Если меняете client — убедитесь что не делает auto-upgrade.

**Priority fix:** P2 — pinger чтобы мониторить когда TLS вернётся + env-override для Basic auth.

---

### egrul 🟡

**Что обещано:** Поиск ЕГРЮЛ по ИНН/ОГРН + проверка контрагентов.
**Что работает:** Полностью, если есть API ключ от api-fns.ru.
**Что НЕ работает:**
- Без API ключа → HTTP 403
- Free tier 800 запросов **суммарно за всё время** (не в день) — для прода непригоден

**Test result (2026-05-26):**
```
GET https://api-fns.ru/api/egr?req=7707083893 (с ключом) → 200 OK
```

**Workaround:** Получите бесплатный ключ на api-fns.ru, добавьте в `.env` как `API_FNS_KEY`. Для прода — рассмотрите dadata.ru.

**Priority fix:** P3 — добавить dadata.ru fallback adapter.

---

### kad 🔴

**Что обещано:** Поиск арбитражных дел по ИНН + получение карточки дела.
**Что работает:** Только code и схемы — endpoint kad.arbitr.ru блокирует bot UA.
**Что НЕ работает:**
- HTTP 451 для любого UA не похожего на браузер
- Cloudflare-like защита

**Test result (2026-05-26):**
```
POST https://kad.arbitr.ru/Kad/SearchInstances с UA=kad-mcp/0.1.0 → 451
```

**Workaround:**
- Установить браузерный UA + cookie-jar (planned для следующего sprint)
- Альтернатива: paid feed через casebook.ru или api-assist.com (~200 req/мес free, дальше платно)

**Priority fix:** P1 — это критичный gap для всей litigation практики.

---

### efrsb 🔴

**Что обещано:** Проверка банкротств юр/физлиц.
**Что работает:** Code корректный, schemas правильные.
**Что НЕ работает:**
- HTTP 403 для UA `efrsb-mcp/0.1.0`
- Нужен браузерный UA + Referer (Referer уже есть, UA — нет)

**Test result (2026-05-26):**
```
GET https://bankrot.fedresurs.ru/backend/companies?searchString=7707083893 → 403
```

**Workaround:** Подмените UA в `.env`:
```
EFRSB_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ..."
```

**Priority fix:** P1 — easy fix через UA подмену.

---

### rospatent ⚫ NEVER WORKED

**Это самый честный пункт во всём файле.**

**Что обещано:** Поиск патентов, ТЗ, ПО через ФИПС.
**Что работает:** Ничего. Endpoints в коде **не существуют у ФИПС.**

**Test result (2026-05-26):**
```
GET https://www1.fips.ru/registers-web/api/trademarks/search?query=Sber → 404
GET https://www1.fips.ru/registers-web/api/patents/search?query=quantum → 404
GET https://www1.fips.ru/registers-web/api/software/search?query=test → 404
GET https://www1.fips.ru/registers-web/api/patentAttorneys/search → 404
```

**Реальность:** У ФИПС нет публичного REST/JSON API. Только HTML-форма поиска (`new.fips.ru/registers-doc-view/fips_servlet`).

**Code в этом MCP — спекулятивная реализация по предполагаемой schema, никогда не валидированная.**

**Workaround:** Никакого. MCP **временно отключён из агрегатора** (см. registry).

**Priority fix:** P0 — три варианта:
1. **Удалить MCP полностью**, добавить notice
2. **Переписать на HTML scraping** `new.fips.ru` (1-2 недели работы)
3. **Платный API** `searchplatform.rospatent.gov.ru` (требует регистрации)

**Решение в работе.** До тех пор — **не используйте этот MCP.**

---

### rosreestr 🟡

**Что обещано:** Кадастр + права + обременения.
**Что работает:** Search by cadastre/address (когда DDoS-Guard пропускает).
**Что НЕ работает:**
- `get_encumbrances` — misleading: всегда возвращает `egrn_extract_strongly_recommended: True`. По факту это redirect на платную EGRN выписку.
- DDoS-Guard периодически блокирует
- Координаты возвращаются в EPSG:3857 (Mercator) без конверсии в WGS84 — для LLM consumer бесполезно

**Test result (2026-05-26):**
```
GET https://pkk.rosreestr.ru/api/features/1?text=77:01:0001017:1234 → timeout
```

**Workaround:** Retry с exponential backoff. Не обещайте обременения — только базовый кадастр.

**Priority fix:** P2 — переписать `get_encumbrances` как "stub-redirect" с явным описанием + EPSG conversion.

---

### zakupki 🟡

**Что обещано:** Поиск тендеров + проверка РНП + история закупок.
**Что работает:** Schemas корректные.
**Что НЕ работает (suspected):**
- Endpoint `https://zakupki.gov.ru/epz/api/orders/search` возможно **не существует**
- Реальный публичный API — только HTML поиск `/epz/order/extendedsearch/results.html` или official EIS Open Data SOAP (требует регистрации)

**Test result (2026-05-26):**
```
GET https://zakupki.gov.ru/epz/api/orders/search?searchString=test → timeout (не подтверждает что endpoint существует)
```

**Workaround:** Используйте только проверку РНП (более стабильный endpoint).

**Priority fix:** P1 — верифицировать endpoint, либо переход на HTML parsing.

---

### ru-legal-aggregator 🟡

**Что обещано:** Агрегатор всех 145 skills + 33 tools из 7 sub-MCPs.
**Что работает:** Skill management (list/find/get/index).
**Что НЕ работает:**
- **Tool proxying для 33 tools НЕ реализовано** (TODO в коде "Phase 2")
- `RU_LEGAL_PACKS_ROOT` env var **обязательный но НЕ документирован** в README
- Без packs/ — `FileNotFoundError`

**Test result (2026-05-26):** code review only.

**Workaround:**
```bash
export RU_LEGAL_PACKS_ROOT=/path/to/ru-legal/packs
uvx ru-legal-mcp
```

**Priority fix:** P2 — переименовать "aggregator" → "skills-router" пока tool-proxying не сделан. Документировать env var.

---

## Что мы делаем сейчас (Phase 0 fixes)

| # | Action | Owner | Target |
|---|---|---|---|
| 1 | Brutal honest update MCP-STATUS.md | @AlsKozlov | **DONE 2026-05-26** ✅ |
| 2 | Remove rospatent из агрегатора | @AlsKozlov | 2026-05-27 |
| 3 | Browser UA для kad/efrsb | @AlsKozlov | 2026-05-29 |
| 4 | Document RU_LEGAL_PACKS_ROOT в README | @AlsKozlov | 2026-05-27 |
| 5 | Shared library `ru_legal_mcp.common/` | @AlsKozlov | 2026-06-03 |
| 6 | New: cbr-mcp (SOAP, no auth) | @AlsKozlov | 2026-06-02 |
| 7 | New: sanctions-mcp (XML dumps) | @AlsKozlov | 2026-06-04 |

## Health check automation (planned)

```yaml
# .github/workflows/mcp-health.yml — daily
on:
  schedule:
    - cron: "0 6 * * *"

steps:
  - run: python scripts/mcp_health_check.py
    # Тестирует все endpoints, обновляет MCP-STATUS.md
    # Если статус изменился — создаёт PR с обновлением
```

## Подписаться на изменения

- Watch [github.com/AlsKozlov/ru-legal](https://github.com/AlsKozlov/ru-legal) → "Custom" → "Releases"
- RSS issues с лейблом `mcp-status-change`
- TG канал [@alskozlov](https://t.me/alskozlov)
