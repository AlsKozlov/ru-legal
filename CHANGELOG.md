# Changelog

Все значимые изменения в `ru-legal` документируются здесь.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
проект следует [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- `packs/registry.json` — single source of truth для всех packs и MCP
- `packs/*/pack.yaml` — portable runtime-agnostic manifests для каждого pack

---

## [0.1.0] - planned (first public release)

Первый публичный релиз. Repository содержит две части: skills (Markdown content) и MCP servers (Python packages).

### Skills (`packs/`) — 145 skills в 14 packs

- **contract-law** (12 skills) — NDA / vendor agreement / SaaS MSA review, договоры услуг / поставки / аренды
- **data-protection** (8) — DSAR response, 152-ФЗ compliance
- **litigation** (17) — matter intake, brief drafting
- **labor-law** (17) — termination review, ЛНПА drafting
- **corporate-law** (13) — share-deal review, DD
- **tax-law** (9) — tax-audit response (ВНП)
- **public-procurement** (9) — tender documentation review (44-ФЗ / 223-ФЗ)
- **compliance-aml** (9) — sanctions screening, 115-ФЗ
- **ip-law** (13) — clearance, infringement triage, takedown (ФЗ-149)
- **ai-governance** (10) — use-case triage, vendor AI review
- **administrative-law** (8) — КоАП violation response
- **real-estate** (9) — ДДУ review (214-ФЗ), cadastre check
- **regulatory-monitor** (6) — reg-feed watcher
- **consumer-product** (5) — launch review (ЗЗПП + 152-ФЗ + 38-ФЗ)

### MCP servers (`mcps/`) — 8 пакетов

| MCP | Источник | Что даёт |
|-----|----------|----------|
| `pravo-mcp` | pravo.gov.ru | Тексты ФЗ / Указов / Постановлений |
| `egrul-mcp` | api-fns.ru | ЕГРЮЛ (требует API key) |
| `kad-mcp` | kad.arbitr.ru | Арбитражные дела |
| `efrsb-mcp` | bankrot.fedresurs.ru | Реестр банкротств |
| `rospatent-mcp` | fips.ru | ТЗ / патенты / ПО |
| `zakupki-mcp` | zakupki.gov.ru | Гос.закупки + РНП |
| `rosreestr-mcp` | pkk.rosreestr.ru | Кадастр недвижимости |
| `ru-legal-mcp` (aggregator) | — | Unified entry-point: skills как MCP prompts + Strategy C router |

### Aggregator features
- 145 skills auto-зарегистрированы как MCP prompts (slash-commands)
- Tools: `list_skills`, `find_skill`, `get_skill`, `get_skill_index`
- Strategy C router — keyword shortlist + optional LLM picker (OpenAI / YandexGPT / GigaChat / DeepSeek auto-detected из env)

### Vendored content
- `vendor/claude-for-legal/` — git submodule с upstream Anthropic claude-for-legal (Apache 2.0). Используется как reference для adapted ports — см. attribution в frontmatter каждого ported skill.
