# ru-legal-mcp

> Unified MCP server для `ru-legal`. Подключи **один пакет** — получи 145 skills + 33 tools РФ legal AI.

[![PyPI](https://img.shields.io/pypi/v/ru-legal-mcp.svg)](https://pypi.org/project/ru-legal-mcp/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../../LICENSE)

## Quick start

### 1. Install

```bash
pip install ru-legal-mcp
# или
uvx ru-legal-mcp
```

### 2. Configure в Claude Code / Cursor / Cline / любом MCP-клиенте

```jsonc
// .mcp.json (или ~/.claude/mcp.json — depending на клиент)
{
  "mcpServers": {
    "ru-legal": {
      "command": "uvx",
      "args": ["ru-legal-mcp"]
    }
  }
}
```

### 3. Готово

Теперь твой LLM-клиент видит:

— **4 skill management tools** (`list_skills`, `find_skill`, `get_skill`, `get_skill_index`)
— **145 skills как MCP prompts** (slash-commands: `/labor_law_termination_review` и т.д.)
— *(coming in Phase 2)* **33 tool proxies** для гос.реестров РФ

## Что внутри

### Skill management tools

| Tool | Purpose |
|------|---------|
| `list_skills(pack=None)` | Все 145 skills с metadata (id, name, description, argument-hint) |
| `find_skill(query, top_k=3)` | **LLM router** — подбирает skill под user query на естественном языке |
| `get_skill(skill_id)` | Полный SKILL.md с workflow / decision tree / citations |
| `get_skill_index()` | Compact text index — quick scan всех skills |

### Skills as MCP prompts

Каждый user-invocable skill auto-зарегистрирован как MCP prompt. В Claude Code появляется как slash-command. Например:

```
/labor_law_termination_review
/corporate_law_diligence_issue_extraction
/tax_law_tax_audit_response
```

### Skill router (Strategy C)

Two-tier:

1. **Keyword shortlist** — keyword search по name + description → top-10 candidates (быстро, бесплатно)
2. **LLM picker** — small/cheap LLM (Haiku / GPT-4o-mini / Yandex Lite / DeepSeek) picks best 1-3 из shortlist

Fallback на keyword-only если LLM не configured.

### Configuration

```bash
# Path к packs/ — обычно auto-detected
export RU_LEGAL_PACKS_ROOT=/path/to/ru-legal/packs

# Provider для router LLM (auto-detected from env):
export OPENAI_API_KEY=sk-...           # → uses gpt-4o-mini
# OR
export YC_IAM_TOKEN=...
export YC_FOLDER_ID=...                 # → uses yandexgpt-lite
# OR
export GIGACHAT_API_KEY=...
# OR
export DEEPSEEK_API_KEY=...
# OR (override explicitly):
export RU_LEGAL_ROUTER_LLM=yandexgpt
```

Если ни одна credential не задана — router работает в keyword-only mode.

## Architecture

```
┌───────────────────────────────────────────┐
│  MCP client (Claude Code / Cursor / ...)  │
└────────────────┬──────────────────────────┘
                 │ MCP protocol (stdio)
                 ▼
┌───────────────────────────────────────────┐
│  ru-legal-mcp (this package)              │
│                                           │
│  ├── server.py — entrypoint               │
│  ├── registry/skills.py — load packs/     │
│  │      • 145 skills indexed at startup   │
│  └── router/                              │
│      ├── router.py — 2-tier router        │
│      └── llm.py — provider-agnostic LLM   │
└────────────────┬──────────────────────────┘
                 │ читает (read-only)
                 ▼
┌───────────────────────────────────────────┐
│  packs/                                   │
│  └── 14 packs × N skills × SKILL.md       │
└───────────────────────────────────────────┘
```

## Использование с LangGraph / LangChain

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

mcp_client = MultiServerMCPClient({
    "ru-legal": {
        "command": "uvx",
        "args": ["ru-legal-mcp"],
        "transport": "stdio",
    }
})

tools = await mcp_client.get_tools()
agent = create_react_agent(model="...", tools=tools)

result = await agent.ainvoke({"messages": [
    {"role": "user", "content": "проверь контрагента ИНН 7707000001"}
]})
```

## Roadmap

- [x] Phase 1: skill management + router + skills as prompts
- [ ] Phase 2: re-expose все 33 sub-MCP tools под одним сервером
- [ ] Phase 3: embedding-based router (top-K via vector search)
- [ ] Phase 4: subagent delegation (one skill calls another)

## Альтернатива — granular install

Если нужны только конкретные источники:

```bash
pip install pravo-mcp efrsb-mcp kad-mcp
# и т.д. — каждый как отдельный package
```

Тогда configure отдельные entries в `.mcp.json`. Подходит если ты хочешь только subset.

## License

Apache 2.0. См. [LICENSE](../../LICENSE).

## Disclaimer

⚠ AI tool, не замена юриста. Material decisions — engage outside-адв ФПА. См. [DISCLAIMER.md](../../DISCLAIMER.md).
