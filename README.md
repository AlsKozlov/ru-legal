# ru-legal

> **Open-source legal knowledge + data layer для российского права.** 145 skills + 7 MCP-интеграций с госреестрами (+ aggregator MCP). Apache 2.0. Подключи через MCP к любому AI-клиенту: Claude Code / Cursor / Continue / LangGraph / собственный harness.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Skills](https://img.shields.io/badge/skills-145-success.svg)](packs/)
[![MCPs](https://img.shields.io/badge/MCPs-8-success.svg)](mcps/)

> ⚠ AI-инструмент, **не замена юриста**. См. [DISCLAIMER.md](DISCLAIMER.md).

---

## Что это

`ru-legal` — **infrastructure layer**, не приложение. Две вещи:

1. **145 skills** в 14 packs — кодифицированные workflow по российскому праву (Markdown с YAML frontmatter — формат от Anthropic)
2. **7 data-MCP серверов** — интеграции с госреестрами (pravo.gov.ru, ЕГРЮЛ, kad.arbitr, ЕФРСБ, Роспатент, ЕИС закупки, Росреестр) + **1 aggregator MCP** (`ru-legal-mcp`) — unified entry-point на всё. Итого **8 MCP** в репозитории.

## Архитектура — два слоя

```
┌─────────────────────────────────────────────────────────┐
│  ru-legal (этот repo)                                    │
│  Open-source legal knowledge + data layer                │
│                                                          │
│  ├── packs/         — 145 skills (Markdown)              │
│  ├── mcps/          — 7 специализированных MCP           │
│  └── mcps/ru-legal-aggregator/                           │
│       └── ru-legal-mcp — unified entry-point             │
└─────────────────────┬───────────────────────────────────┘
                      │ MCP protocol
                      ▼
              ANY MCP-compatible client:
   ┌──────────┬────────────┬──────────┬─────────────┐
   ▼          ▼            ▼          ▼             ▼
Claude Code Cursor    Continue   LangGraph   ru-legal-agent
 (plugin)  (.mcp.json) (.json)   (langchain   (отдельный
                                  MCP adapter) project)
```

## Quick start — 3 пути

### Путь 1: ru-legal-mcp в Claude Code / Cursor / Cline

```bash
pip install ru-legal-mcp
```

```jsonc
// .mcp.json (или .claude/mcp.json — depends on client)
{
  "mcpServers": {
    "ru-legal": {
      "command": "uvx",
      "args": ["ru-legal-mcp"]
    }
  }
}
```

Теперь LLM-клиент видит:
- **145 skills** как MCP prompts (slash-commands)
- **Skill management tools** (`find_skill`, `get_skill`, `list_skills`)
- **(Phase 2)** 33 tools из 7 sub-MCPs

### Путь 2: Granular install — отдельные MCP

```bash
pip install pravo-mcp efrsb-mcp kad-mcp rospatent-mcp
```

Подключи отдельные entries в `.mcp.json`. Подходит если нужен subset.

### Путь 3: Build your own harness — embed via LangGraph

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient({
    "ru-legal": {
        "command": "uvx",
        "args": ["ru-legal-mcp"],
        "transport": "stdio",
    }
})
tools = await client.get_tools()
agent = create_react_agent(model="yandex-gpt", tools=tools)
result = await agent.ainvoke({"messages": [
    {"role": "user", "content": "проверь контрагента ИНН 7707000001"}
]})
```

## Что внутри

### 14 packs / 145 skills

| Pack | Skills | Killer skill |
|------|-------:|--------------|
| [contract-law](packs/contract-law/) | 12 | nda-review, vendor-agreement-review, saas-msa-review |
| [data-protection](packs/data-protection/) | 8 | **dsar-response** (РКН штрафы до 18M ₽) |
| [litigation](packs/litigation/) | 17 | matter-intake, brief-section-drafter |
| [labor-law](packs/labor-law/) | 17 | **termination-review** (13 grounds + защ. категории) |
| [corporate-law](packs/corporate-law/) | 13 | share-deal-review (нотариус ст.21 ФЗ-14), DD |
| [tax-law](packs/tax-law/) | 9 | **tax-audit-response** (ВНП доначисления) |
| [public-procurement](packs/public-procurement/) | 9 | tender-documentation-review, biased-tender-detection |
| [compliance-aml](packs/compliance-aml/) | 9 | sanctions-screening (multi-jurisdiction) |
| [ip-law](packs/ip-law/) | 13 | clearance, infringement-triage, takedown ФЗ-149 |
| [ai-governance](packs/ai-governance/) | 10 | use-case-triage, vendor-ai-review, AIA |
| [administrative-law](packs/administrative-law/) | 8 | koap-violation-response, 10-day appeal |
| [real-estate](packs/real-estate/) | 9 | **ddu-review** 214-ФЗ, cadastre-check |
| [regulatory-monitor](packs/regulatory-monitor/) | 6 | reg-feed-watcher, gap-surfacer |
| [consumer-product](packs/consumer-product/) | 5 | launch-review (ЗЗПП + 152-ФЗ + 38-ФЗ) |

### 7 MCP integrations (госреестры)

| MCP | Источник | Что даёт |
|-----|----------|----------|
| [pravo](mcps/pravo/) | pravo.gov.ru | Тексты ФЗ / Указов / Постановлений |
| [egrul](mcps/egrul/) | api-fns.ru | Проверка контрагентов в ЕГРЮЛ (требует API ключ) |
| [kad](mcps/kad/) | kad.arbitr.ru | Арбитражные дела |
| [efrsb](mcps/efrsb/) | bankrot.fedresurs.ru | Реестр банкротств |
| [rospatent](mcps/rospatent/) | fips.ru | ТЗ / патенты / ПО |
| [zakupki](mcps/zakupki/) | zakupki.gov.ru | Гос.закупки + РНП |
| [rosreestr](mcps/rosreestr/) | pkk.rosreestr.ru | Кадастр недвижимости |

**6 из 7 работают полностью бесплатно**, без API-ключей.

### Aggregator MCP (`ru-legal-mcp`)

Один пакет, объединяющий всё:

- Все 145 skills доступны через `list_skills` / `find_skill` / `get_skill`
- **Strategy C router** — LLM-based подбор skill под user query (если configured), keyword fallback
- Skills auto-зарегистрированы как MCP prompts (slash-commands)
- *(Phase 2)*: re-export всех 33 tools из 7 sub-MCPs

См. [`mcps/ru-legal-aggregator/README.md`](mcps/ru-legal-aggregator/README.md).

## Не входит в этот repo

- ❌ Harness / agent loop / tool-call orchestration → отдельный repo (planned: `ru-legal-agent`, LangGraph-based)
- ❌ Telegram bot → туда же
- ❌ Web UI / REST API → туда же
- ❌ Memory / audit / approval / citation verification modules → туда же
- ❌ CLI app → туда же

Этот repo — pure **content + data**. Никаких opinions про harness.

## LLM-агностично

Сам по себе `ru-legal-mcp` — pure data + skills. Какую LLM использовать — выбирает harness:

- **Claude** — если есть доступ
- **OpenAI GPT-4** — то же
- **YandexGPT** — доступен в РФ без VPN ✅
- **GigaChat** — доступен в РФ без VPN ✅
- **DeepSeek** — доступен ✅
- **Self-hosted** (Llama / Qwen / Mistral через vLLM / Ollama)

Router LLM (для Strategy C skill selection) auto-detects из env vars (`OPENAI_API_KEY` / `YC_IAM_TOKEN` / `GIGACHAT_API_KEY` / `DEEPSEEK_API_KEY`).

## Вдохновлено Anthropic claude-for-legal

`ru-legal` — это **локализованный adaptation** [`claude-for-legal`](https://github.com/anthropics/claude-for-legal) (Apache 2.0, Anthropic):

- *Структура skill (Markdown + YAML frontmatter)* — их формат
- *Концепция packs* — их идея
- *Pattern «skill prescribes tool calls»* — их подход

Что мы добавили:
- 14 packs vs 12 — RU-unique (tax-law, public-procurement, compliance-aml, administrative-law, real-estate)
- 145 skills vs 110 — РФ-уникальные процедуры
- Deep content adaptation под РФ (ст. ГК / ТК / НК / ФЗ + российская практика)
- 7 MCP интеграций с РФ госреестрами (Anthropic ничего такого не делал)
- LLM-агностичность (Anthropic — Claude-only)

Attribution-метаданные содержатся в YAML frontmatter каждого портированного skill (`ported_from`, `ported_at`). Полный текст лицензии Anthropic — [`vendor/claude-for-legal/LICENSE`](vendor/claude-for-legal/LICENSE).

## Contributing

См. [CONTRIBUTING.md](CONTRIBUTING.md).

Самые полезные contributions:

- 🐛 **Feedback от практикующего юриста** на конкретный skill
- 📝 **Новый skill** в существующий pack (пример: `packs/*/skills/*/SKILL.md`)
- 🔌 **Новый MCP** (ФАС / ФССП / РКН реестры в roadmap)
- 📦 **Новый pack** (банкротство / страхование / ВЭД)
- 📖 **Документация**

## Roadmap

- ✅ Phase 1: 14 packs / 145 skills / 7 MCPs / aggregator MCP
- 🚧 Phase 2: split + `ru-legal-agent` separate repo + tool proxying в aggregator
- ⏳ Phase 3: embedding-based router, более sophisticated memory integration
- ⏳ Phase 4: community-contributed packs (banking law / customs / fintech)

## License

Apache 2.0. См. [LICENSE](LICENSE).

## Disclaimer

⚠ **Это AI-tool, не замена юриста.** AI галлюцинирует, нормы устаревают, контекст важен. Material decisions — engage outside-адв ФПА. Полный disclaimer: [DISCLAIMER.md](DISCLAIMER.md).
