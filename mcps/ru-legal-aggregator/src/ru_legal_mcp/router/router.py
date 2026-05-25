"""Skill router — Strategy C (LLM-based skill selection by descriptions).

Анalogously to Anthropic claude-for-legal pattern: when user query comes,
LLM looks at compact index всех skill descriptions and picks top-K candidates.

Two-tier подход:
1. Keyword shortlist — filter to ~10 candidates без LLM (fast, ~ms)
2. LLM picker — choose best 1-3 из shortlist (slower, ~1s)

Fallback: если LLM недоступен или confidence low — возвращает top-K из keyword search.

Cost: ~$0.001-0.005 per routing call (using cheap LLM like Haiku/Llama-8B/Yandex-Lite).
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Protocol, runtime_checkable

from ru_legal_mcp.registry.skills import SkillMetadata, SkillRegistry

logger = logging.getLogger(__name__)


@dataclass
class RouterCandidate:
    """One skill candidate from router."""

    skill_id: str
    description: str
    confidence: float  # 0.0 - 1.0
    reasoning: str | None = None
    source: str = "router"  # "keyword" / "llm" / "fallback"

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "description": self.description,
            "confidence": round(self.confidence, 3),
            "reasoning": self.reasoning,
            "source": self.source,
        }


@runtime_checkable
class RouterLLM(Protocol):
    """Minimal LLM interface для router.

    Не зависим от full ru_legal SDK провайдеров — router может работать с любым
    LLM который умеет выдавать structured output (JSON).
    """

    async def complete(self, system: str, user: str) -> str: ...


class SkillRouter:
    """Two-tier skill router.

    Usage:
        router = SkillRouter(registry, llm=my_llm)
        candidates = await router.find("сокращаю 5 разработчиков", top_k=3)
        # → [{skill_id: "labor-law/termination-review", confidence: 0.95, ...}]
    """

    def __init__(
        self,
        registry: SkillRegistry,
        llm: RouterLLM | None = None,
        shortlist_size: int = 10,
    ):
        """
        Args:
            registry: loaded SkillRegistry.
            llm: optional RouterLLM for tier-2 picking. Если None — только
                keyword tier.
            shortlist_size: how many candidates из keyword tier для LLM picker.
        """
        self.registry = registry
        self.llm = llm
        self.shortlist_size = shortlist_size

    async def find(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RouterCandidate]:
        """Find top-K skill candidates for user query.

        Returns: sorted list by confidence descending.
        """
        # Tier 1: keyword shortlist (always — cheap)
        shortlist = self._keyword_shortlist(query, limit=self.shortlist_size)
        if not shortlist:
            return [self._fallback_candidate()]

        # Tier 2: LLM picker (если available)
        if self.llm is not None and len(shortlist) > 1:
            try:
                llm_picks = await self._llm_pick(query, shortlist, top_k=top_k)
                if llm_picks:
                    return llm_picks
            except Exception as e:
                logger.warning("LLM router failed, falling back to keyword: %s", e)

        # Fallback: top-K из keyword search
        return [
            RouterCandidate(
                skill_id=skill.skill_id,
                description=skill.description.strip()[:200],
                confidence=min(score / 10.0, 1.0),
                source="keyword",
            )
            for skill, score in shortlist[:top_k]
        ]

    def _keyword_shortlist(
        self,
        query: str,
        limit: int = 10,
    ) -> list[tuple[SkillMetadata, float]]:
        return self.registry.keyword_search(query, limit=limit)

    async def _llm_pick(
        self,
        query: str,
        shortlist: list[tuple[SkillMetadata, float]],
        top_k: int = 3,
    ) -> list[RouterCandidate]:
        """Tier 2: LLM picks best из shortlist."""
        if not self.llm:
            raise ValueError("LLM not configured")

        skills_block = "\n".join(
            f"{i+1}. {skill.skill_id}\n   {skill.description.strip()[:200]}"
            for i, (skill, _) in enumerate(shortlist)
        )

        system = (
            "You are a skill router for a Russian legal AI system. "
            "Given a user query, pick the most relevant skill(s) from the list. "
            "Output strict JSON, nothing else."
        )

        user = (
            f"User query (Russian): {query}\n\n"
            f"Candidate skills:\n{skills_block}\n\n"
            f"Pick top-{top_k} most relevant skills. Return strict JSON in this format:\n"
            f'[{{"skill_id": "...", "confidence": 0.0-1.0, "reasoning": "..."}}, ...]\n'
            f"Order by confidence descending. Use confidence < 0.5 if uncertain. "
            f"If no skill matches well, return empty array []."
        )

        response = await self.llm.complete(system=system, user=user)
        return self._parse_llm_response(response, shortlist)

    def _parse_llm_response(
        self,
        response: str,
        shortlist: list[tuple[SkillMetadata, float]],
    ) -> list[RouterCandidate]:
        """Parse LLM JSON response into candidates."""
        # Strip markdown fences if present
        text = response.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning("Router LLM returned non-JSON: %s", e)
            return []

        if not isinstance(data, list):
            return []

        shortlist_index = {skill.skill_id: skill for skill, _ in shortlist}
        candidates: list[RouterCandidate] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            skill_id = item.get("skill_id")
            if not skill_id or skill_id not in shortlist_index:
                continue
            skill = shortlist_index[skill_id]
            try:
                confidence = float(item.get("confidence", 0.5))
            except (TypeError, ValueError):
                confidence = 0.5
            candidates.append(
                RouterCandidate(
                    skill_id=skill_id,
                    description=skill.description.strip()[:200],
                    confidence=min(max(confidence, 0.0), 1.0),
                    reasoning=item.get("reasoning"),
                    source="llm",
                )
            )

        candidates.sort(key=lambda c: -c.confidence)
        return candidates

    def _fallback_candidate(self) -> RouterCandidate:
        """Возвращается когда ничего не нашли."""
        return RouterCandidate(
            skill_id="contract-law/contract-review",
            description="Default fallback — generic contract review skill",
            confidence=0.1,
            reasoning="No specific match found; falling back to generic review skill",
            source="fallback",
        )
