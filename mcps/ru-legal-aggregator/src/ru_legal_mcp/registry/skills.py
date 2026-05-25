"""Skill registry — loads + indexes all 145 skills from packs/.

Provides:
- list_skills() — все skills с метаданными
- get_skill(skill_id) — full SKILL.md
- search_skills(query) — keyword search по name/description
- get_skill_index() — компактный index (для LLM router)

Loaded once at startup, cached in memory.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass
class SkillMetadata:
    """Compact metadata из skill frontmatter."""

    skill_id: str  # "pack-name/skill-name"
    pack: str
    name: str
    description: str
    argument_hint: str | None = None
    user_invocable: bool = True
    ported_from: str | None = None
    adaptation_category: str | None = None
    path: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "pack": self.pack,
            "name": self.name,
            "description": self.description.strip(),
            "argument_hint": self.argument_hint,
            "user_invocable": self.user_invocable,
        }


@dataclass
class Skill(SkillMetadata):
    """Full skill — metadata + body."""

    body: str = ""

    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base["body"] = self.body
        return base


class SkillRegistry:
    """In-memory registry всех skills.

    Loaded once at startup via load_from_packs(). Thread-safe для read.
    """

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def __len__(self) -> int:
        return len(self._skills)

    def load_from_packs(self, packs_root: Path | str) -> int:
        """Load all SKILL.md files under packs_root.

        Returns:
            Number of skills loaded.
        """
        packs_path = Path(packs_root).resolve()
        if not packs_path.exists():
            raise FileNotFoundError(f"Packs directory not found: {packs_path}")

        count = 0
        for skill_md in packs_path.glob("*/skills/*/SKILL.md"):
            try:
                skill = self._parse_skill_file(skill_md, packs_path)
                if skill is not None:
                    self._skills[skill.skill_id] = skill
                    count += 1
            except Exception as e:
                logger.warning("Failed to load %s: %s", skill_md, e)

        self._loaded = True
        logger.info("Loaded %d skills from %s", count, packs_path)
        return count

    def _parse_skill_file(self, path: Path, packs_root: Path) -> Skill | None:
        """Parse SKILL.md — extract frontmatter + body."""
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            logger.warning("No frontmatter in %s, skipping", path)
            return None

        # Split frontmatter / body
        m = re.match(r"^---\s*\n(.+?)\n---\s*\n(.*)$", content, re.DOTALL)
        if not m:
            logger.warning("Invalid frontmatter in %s", path)
            return None

        try:
            fm = yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            logger.warning("YAML parse error in %s: %s", path, e)
            return None

        if not isinstance(fm, dict):
            return None

        body = m.group(2).strip()

        # Derive skill_id from path: packs/<pack>/skills/<skill_name>/SKILL.md
        rel = path.relative_to(packs_root)
        parts = rel.parts
        if len(parts) < 4 or parts[1] != "skills":
            return None
        pack_name = parts[0]
        skill_name = parts[2]
        skill_id = f"{pack_name}/{skill_name}"

        return Skill(
            skill_id=skill_id,
            pack=pack_name,
            name=fm.get("name", skill_name),
            description=str(fm.get("description", "")),
            argument_hint=fm.get("argument-hint") or fm.get("argument_hint"),
            user_invocable=bool(fm.get("user_invocable", True)),
            ported_from=fm.get("ported_from"),
            adaptation_category=fm.get("adaptation_category"),
            path=path,
            body=body,
        )

    def list_all(
        self,
        pack: str | None = None,
        only_user_invocable: bool = True,
    ) -> list[SkillMetadata]:
        """Return all skills (optionally filtered)."""
        result = []
        for skill in self._skills.values():
            if only_user_invocable and not skill.user_invocable:
                continue
            if pack is not None and skill.pack != pack:
                continue
            result.append(skill)
        return sorted(result, key=lambda s: s.skill_id)

    def get(self, skill_id: str) -> Skill | None:
        """Get full skill by ID."""
        return self._skills.get(skill_id)

    def keyword_search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[tuple[SkillMetadata, float]]:
        """Simple keyword search — scores skills by query term frequency.

        Returns:
            List of (skill, score) sorted by score descending.
        """
        terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
        if not terms:
            return []

        scored: list[tuple[SkillMetadata, float]] = []
        for skill in self._skills.values():
            if not skill.user_invocable:
                continue
            haystack = f"{skill.skill_id} {skill.name} {skill.description}".lower()
            score = 0.0
            for term in terms:
                # Count occurrences with quadratic boost для multi-match
                occurrences = haystack.count(term)
                if occurrences:
                    score += occurrences * 1.0 + (occurrences ** 0.5)
            if score > 0:
                scored.append((skill, score))

        scored.sort(key=lambda x: -x[1])
        return scored[:limit]

    def get_index_for_router(self) -> str:
        """Compact index of all skills для LLM router.

        Format:
            <skill_id> | <description (first 120 chars)>

        ~145 skills × ~150 chars = ~22KB — fits comfortably в context.
        """
        lines = ["Available skills (skill_id | description):"]
        for skill in sorted(self._skills.values(), key=lambda s: s.skill_id):
            if not skill.user_invocable:
                continue
            desc = re.sub(r"\s+", " ", skill.description).strip()
            if len(desc) > 150:
                desc = desc[:147] + "..."
            lines.append(f"  {skill.skill_id} | {desc}")
        return "\n".join(lines)
