"""ru-legal-mcp — unified MCP server.

Exposes:
- *Skill management tools*:
  - list_skills(pack=None) → all available skills с метаданными
  - find_skill(query, top_k=3) → Strategy C router (LLM-based)
  - get_skill(skill_id) → full SKILL.md content

- *Skills as MCP prompts*:
  - Auto-register все 145 skills как prompts с argument-hint
  - Claude Code / Cursor will see them как slash commands

- *Все 33 tools из 7 sub-MCPs* (proxied / re-implemented):
  - Namespaced: pravo_search_npa, kad_search_cases, etc.
  - TODO: на текущем шаге добавляем только skill management; tool proxying в Phase 2

Run as: `ru-legal-mcp` (stdio MCP server)
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from ru_legal_mcp.registry.skills import SkillRegistry
from ru_legal_mcp.router.llm import RouterLLMClient
from ru_legal_mcp.router.router import SkillRouter

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ru-legal-mcp")


# ----------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------


def _find_packs_root() -> Path:
    """Locate packs/ directory — try env var, then package path, then walk up."""
    if env := os.getenv("RU_LEGAL_PACKS_ROOT"):
        path = Path(env).resolve()
        if path.exists():
            return path

    # Walk up from this file looking for packs/
    here = Path(__file__).resolve()
    for parent in here.parents[:8]:
        candidate = parent / "packs"
        if candidate.exists() and any(candidate.glob("*/skills/*/SKILL.md")):
            return candidate

    raise FileNotFoundError(
        "Cannot find packs/ directory. Set RU_LEGAL_PACKS_ROOT environment variable."
    )


_packs_root = _find_packs_root()
_registry = SkillRegistry()
_skills_loaded = _registry.load_from_packs(_packs_root)

_router_llm = RouterLLMClient()
_router = SkillRouter(_registry, llm=_router_llm if _router_llm.is_configured else None)


mcp = FastMCP(
    name="ru-legal",
    instructions=(
        f"ru-legal — open-source AI юрист для российского права. "
        f"{_skills_loaded} skills + интеграции с госреестрами РФ. "
        f"Используй find_skill для подбора нужного skill под query, "
        f"затем get_skill для загрузки полной инструкции. "
        f"Все skills доступны также как MCP prompts (slash-commands)."
    ),
)


# ----------------------------------------------------------------------------
# Skill management tools
# ----------------------------------------------------------------------------


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def list_skills(
    pack: Annotated[
        str | None,
        Field(
            description=(
                "Filter by pack ID (например 'labor-law' / 'tax-law'). "
                "None = все 14 packs."
            ),
            max_length=50,
        ),
    ] = None,
    only_user_invocable: Annotated[
        bool,
        Field(description="Skip sub-skills (default True)."),
    ] = True,
) -> list[dict[str, Any]]:
    """List available skills с метаданными.

    Returns: список skill metadata — skill_id, pack, name, description,
    argument_hint. Не возвращает body (для compactness).

    Используй чтобы LLM мог понять что доступно перед load конкретного skill.
    """
    logger.info("list_skills pack=%s", pack)
    skills = _registry.list_all(pack=pack, only_user_invocable=only_user_invocable)
    return [s.to_dict() for s in skills]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def find_skill(
    query: Annotated[
        str,
        Field(
            description=(
                "User query — что юрист хочет сделать. На русском, free-form. "
                "Например: 'сокращаю 5 разработчиков', 'нужна проверка контрагента "
                "перед сделкой 50М', 'review ДДУ перед подписанием'."
            ),
            min_length=3,
            max_length=2000,
        ),
    ],
    top_k: Annotated[
        int,
        Field(description="Сколько top candidates вернуть.", ge=1, le=10),
    ] = 3,
) -> list[dict[str, Any]]:
    """Найти подходящий skill для user query — Strategy C router.

    Two-tier подход:
    1. *Keyword shortlist* — filter to top-10 candidates без LLM (fast)
    2. *LLM picker* — choose best из shortlist (если LLM configured)

    Fallback: если LLM недоступен — keyword-only.

    Используй чтобы понять *какой* skill запускать перед `get_skill()`.

    Returns: top-K candidates с confidence + reasoning.
    """
    logger.info("find_skill query=%r top_k=%d", query[:100], top_k)
    candidates = await _router.find(query, top_k=top_k)
    return [c.to_dict() for c in candidates]


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_skill(
    skill_id: Annotated[
        str,
        Field(
            description=(
                "Skill ID в формате 'pack-name/skill-name'. "
                "Например 'labor-law/termination-review'. "
                "Получи доступные через list_skills() или find_skill()."
            ),
            pattern=r"^[a-z][a-z0-9-]*/[a-z][a-z0-9-]*$",
            max_length=80,
        ),
    ],
) -> dict[str, Any]:
    """Получить полное содержимое SKILL.md по ID.

    Returns: full skill — metadata + body (Markdown). Body содержит workflow,
    decision trees, цитаты норм, output format.

    Используй чтобы LLM получил полную инструкцию для исполнения. После
    этого LLM сможет вызывать нужные MCP tools согласно skill instructions.
    """
    logger.info("get_skill skill_id=%s", skill_id)
    skill = _registry.get(skill_id)
    if skill is None:
        raise ToolError(
            f"Skill {skill_id!r} не найден. "
            f"Используй list_skills() чтобы получить список доступных."
        )
    return skill.to_dict()


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def get_skill_index() -> str:
    """Получить compact index всех skills (для quick LLM scan).

    Returns: text format с одной строкой на skill:
        skill_id | description (first 150 chars)

    Use case: вместо list_skills() для browse сразу всего — ~30KB всё это.
    """
    return _registry.get_index_for_router()


# ----------------------------------------------------------------------------
# Skills as MCP prompts — auto-register all 145 skills
# ----------------------------------------------------------------------------


def _register_skills_as_prompts() -> int:
    """Auto-register все skills как MCP prompts.

    Это позволяет Claude Code / Cursor видеть skills как slash-commands
    (`/skill-name`).

    Returns: number of prompts registered.
    """
    count = 0
    for skill in _registry.list_all(only_user_invocable=True):
        # Decorator workaround — мы не можем @mcp.prompt() decorate dynamic functions
        # на module level, но FastMCP API поддерживает programmatic registration.
        try:
            _register_one_prompt(skill.skill_id, skill.name, skill.description, skill.argument_hint)
            count += 1
        except Exception as e:
            logger.warning("Failed to register skill %s as prompt: %s", skill.skill_id, e)
    return count


def _register_one_prompt(
    skill_id: str,
    name: str,
    description: str,
    argument_hint: str | None,
) -> None:
    """Register one skill как MCP prompt via fastmcp API.

    Note: fastmcp prompt API позволяет dynamic registration через `mcp.prompt()`
    decorator на closure. Имена prompts — kebab-case без pack prefix (typical
    Claude Code convention для slash-commands).
    """
    prompt_name = skill_id.replace("/", "_").replace("-", "_")

    @mcp.prompt(name=prompt_name, description=description.strip()[:500])
    async def _prompt_handler(input: str = "") -> str:
        """Dynamic prompt handler — returns full skill body."""
        skill = _registry.get(skill_id)
        if skill is None:
            return f"Skill {skill_id} not found"
        if input:
            return f"{skill.body}\n\n---\n\n## User input\n\n{input}"
        return skill.body


_prompts_registered = _register_skills_as_prompts()
logger.info("Registered %d skills as MCP prompts", _prompts_registered)


# ----------------------------------------------------------------------------
# Static resources
# ----------------------------------------------------------------------------


@mcp.resource("ru-legal://about")
def about_resource() -> str:
    """About ru-legal — что это, как использовать."""
    return f"""
# ru-legal MCP

Open-source AI юрист для российского права.

## Loaded

- {_skills_loaded} skills из 14 packs
- {_prompts_registered} зарегистрированы как MCP prompts
- Router LLM: {'configured (' + _router_llm.provider + ')' if _router_llm.is_configured else 'NOT configured (keyword-only routing)'}

## Tools

- `list_skills(pack=None)` — все skills с метаданными
- `find_skill(query, top_k=3)` — LLM router для подбора skill
- `get_skill(skill_id)` — full SKILL.md content
- `get_skill_index()` — compact text index всех skills

## Prompts

Все user-invocable skills доступны как MCP prompts. Имя prompt: pack_name_skill_name
(snake_case). Например: `labor_law_termination_review`.

## Configuration

- `RU_LEGAL_PACKS_ROOT` — путь к packs/ (auto-detected if не задан)
- `RU_LEGAL_ROUTER_LLM` — provider для router LLM (openai/yandexgpt/gigachat/...)
- `OPENAI_API_KEY` / `YC_IAM_TOKEN` / `GIGACHAT_API_KEY` — credentials

## Disclaimer

⚠ AI tool, не замена юриста. Material decisions — engage outside-адв ФПА.
"""


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------


def main() -> None:
    logger.info(
        "Starting ru-legal-mcp v0.1.0 — %d skills loaded, %d prompts registered, router=%s",
        _skills_loaded,
        _prompts_registered,
        _router_llm.provider or "keyword-only",
    )
    mcp.run()


if __name__ == "__main__":
    main()
