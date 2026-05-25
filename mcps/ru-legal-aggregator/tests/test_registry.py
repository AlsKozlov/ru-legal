"""Tests для skill registry."""
from __future__ import annotations

from pathlib import Path

import pytest

from ru_legal_mcp.registry.skills import SkillRegistry


REPO_ROOT = Path(__file__).resolve().parents[3].parent
PACKS_ROOT = REPO_ROOT / "packs"


@pytest.fixture(scope="module")
def registry() -> SkillRegistry:
    r = SkillRegistry()
    r.load_from_packs(PACKS_ROOT)
    return r


def test_loads_all_skills(registry: SkillRegistry):
    """At least 100 skills должны быть загружены."""
    assert len(registry) >= 100, f"Expected ≥100 skills, got {len(registry)}"


def test_list_all_returns_metadata(registry: SkillRegistry):
    skills = registry.list_all()
    assert len(skills) > 0
    skill = skills[0]
    assert skill.skill_id
    assert "/" in skill.skill_id
    assert skill.description


def test_list_filter_by_pack(registry: SkillRegistry):
    labor_skills = registry.list_all(pack="labor-law")
    assert len(labor_skills) > 5
    for s in labor_skills:
        assert s.pack == "labor-law"


def test_get_known_skill(registry: SkillRegistry):
    skill = registry.get("labor-law/termination-review")
    assert skill is not None
    assert skill.body  # full content loaded
    assert len(skill.body) > 1000  # это killer skill, должен быть big


def test_get_unknown_returns_none(registry: SkillRegistry):
    assert registry.get("nonexistent/skill") is None


def test_keyword_search_termination(registry: SkillRegistry):
    """Search for 'увольнение сокращение' should find termination-review at top."""
    results = registry.keyword_search("увольнение сокращение")
    assert len(results) > 0
    top_skill, top_score = results[0]
    assert "termination" in top_skill.skill_id or "termination" in top_skill.name.lower()


def test_keyword_search_dd_контрагент(registry: SkillRegistry):
    results = registry.keyword_search("проверка контрагент")
    assert len(results) > 0
    # Какой-нибудь из diligence skills should top-rank
    top_ids = [s.skill_id for s, _ in results[:3]]
    assert any("diligence" in sid or "due-diligence" in sid for sid in top_ids)


def test_index_format(registry: SkillRegistry):
    index = registry.get_index_for_router()
    assert "Available skills" in index
    lines = index.split("\n")
    # 1 header + ≥100 skill lines
    assert len(lines) > 100
    # Each skill line должен иметь skill_id | description format
    skill_lines = [l for l in lines if " | " in l]
    assert len(skill_lines) > 50
