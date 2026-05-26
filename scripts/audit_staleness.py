#!/usr/bin/env python3
"""audit_staleness.py — Аудит skills на staleness.

Сканирует все skills в packs/*/skills/*/SKILL.md и проверяет:
1. Имеют ли поле `last_legislative_update` в frontmatter
2. Если имеют — давно ли обновлялись (>6 месяцев = stale)
3. Имеют ли обязательные поля: name, description, required_tools, version

Output:
- Console report (color-coded)
- JSON file для CI integration
- Exit code != 0 если есть stale/missing → блокирует merge

Usage:
    python scripts/audit_staleness.py
    python scripts/audit_staleness.py --json output.json
    python scripts/audit_staleness.py --max-age-months 12
    python scripts/audit_staleness.py --strict   # exit 1 если есть warnings
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================================
# Frontmatter parser (без зависимостей — простой regex)
# ============================================================================

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Простой YAML-frontmatter parser. Поддерживает key: value и key: |\\n ... block."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    result: dict[str, Any] = {}
    current_key = None
    current_block: list[str] = []
    in_block = False

    for line in raw.split("\n"):
        if in_block:
            if line.startswith("  ") or line.startswith("\t") or not line.strip():
                current_block.append(line.lstrip())
                continue
            else:
                # Block ended
                result[current_key] = "\n".join(current_block).strip()
                in_block = False
                current_key = None
                current_block = []
                # Fall through to parse current line

        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "|" or val == ">":
                in_block = True
                current_key = key
                current_block = []
            elif val.startswith("[") or val.startswith("{"):
                # Try simple JSON-like
                try:
                    result[key] = json.loads(val.replace("'", '"'))
                except Exception:
                    result[key] = val
            elif val.startswith('"') and val.endswith('"'):
                result[key] = val[1:-1]
            elif val.lower() in ("true", "false"):
                result[key] = val.lower() == "true"
            else:
                result[key] = val
        elif line.startswith("  - ") and current_key:
            # List item
            existing = result.get(current_key)
            if not isinstance(existing, list):
                result[current_key] = []
            result[current_key].append(line[4:].strip())

    if in_block and current_key:
        result[current_key] = "\n".join(current_block).strip()

    return result


# ============================================================================
# Audit logic
# ============================================================================

REQUIRED_FIELDS = ["name", "description"]  # absolute minimum
RECOMMENDED_FIELDS = ["version", "last_legislative_update", "required_tools", "domain_owner", "risk_level"]


def parse_legislative_date(value: str) -> datetime | None:
    """Парсит дату из last_legislative_update. Принимает YYYY-MM или YYYY-MM-DD."""
    if not value or not isinstance(value, str):
        return None
    v = value.strip().strip('"').strip("'")
    # Strip inline comment if present
    if "#" in v:
        v = v.split("#", 1)[0].strip().strip('"').strip("'")
    formats = ["%Y-%m-%d", "%Y-%m", "%Y/%m/%d", "%Y/%m"]
    for fmt in formats:
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    return None


def months_since(date: datetime) -> int:
    """Сколько целых месяцев прошло от date до сегодня."""
    today = datetime.utcnow()
    return (today.year - date.year) * 12 + (today.month - date.month)


def audit_skill(skill_path: Path, max_age_months: int) -> dict[str, Any]:
    """Аудит одного skill файла. Возвращает dict с issues."""
    text = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    result = {
        "path": str(skill_path.relative_to(skill_path.parents[3])),
        "name": fm.get("name", "<missing>"),
        "version": fm.get("version", "<missing>"),
        "issues": [],
        "warnings": [],
        "info": [],
    }

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in fm or not fm[field]:
            result["issues"].append(f"missing required field: {field}")

    # Recommended fields
    for field in RECOMMENDED_FIELDS:
        if field not in fm or not fm[field]:
            result["warnings"].append(f"missing recommended field: {field}")

    # Last legislative update check
    last_update = fm.get("last_legislative_update")
    if last_update:
        parsed = parse_legislative_date(str(last_update))
        if parsed is None:
            result["issues"].append(f"invalid last_legislative_update format: {last_update!r}")
        else:
            age = months_since(parsed)
            result["info"].append(f"last_legislative_update: {last_update} ({age} months ago)")
            if age > max_age_months:
                result["warnings"].append(
                    f"STALE: last_legislative_update {age} months ago (max {max_age_months})"
                )

    # Quality checks
    if "## Workflow" not in text:
        result["warnings"].append("missing '## Workflow' section")
    if "## Degraded mode" not in text and "## degraded mode" not in text.lower():
        result["warnings"].append("missing '## Degraded mode' section")
    if "required_tools" in fm and "`" not in text:
        result["warnings"].append("required_tools declared but no tool calls (backticks) in workflow")

    return result


def find_skills(packs_root: Path) -> list[Path]:
    """Найди все SKILL.md в packs/*/skills/*/."""
    skills = []
    for pack_dir in packs_root.iterdir():
        if not pack_dir.is_dir():
            continue
        if pack_dir.name.startswith("_"):
            continue
        skills_dir = pack_dir / "skills"
        if not skills_dir.exists():
            continue
        for skill_dir in skills_dir.iterdir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills.append(skill_file)
    return skills


# ============================================================================
# Reporting
# ============================================================================

def format_console(results: list[dict[str, Any]], max_age_months: int) -> str:
    """Human-readable color report."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    total = len(results)
    has_issues = [r for r in results if r["issues"]]
    has_warnings = [r for r in results if r["warnings"] and not r["issues"]]
    clean = [r for r in results if not r["issues"] and not r["warnings"]]
    stale = [
        r for r in results
        if any("STALE" in w for w in r["warnings"])
    ]
    missing_legislative = [
        r for r in results
        if any("missing recommended field: last_legislative_update" in w for w in r["warnings"])
    ]

    lines = [
        f"{BOLD}=== ru-legal skill staleness audit ==={RESET}",
        f"Date: {datetime.utcnow().isoformat()}",
        f"Max age: {max_age_months} months",
        f"",
        f"Total skills: {total}",
        f"  {GREEN}✅ Clean: {len(clean)}{RESET}",
        f"  {YELLOW}⚠ Warnings: {len(has_warnings)}{RESET}",
        f"  {RED}❌ Issues: {len(has_issues)}{RESET}",
        f"",
        f"By category:",
        f"  {RED}STALE (>{max_age_months}mo): {len(stale)}{RESET}",
        f"  {YELLOW}Missing last_legislative_update: {len(missing_legislative)}{RESET}",
        f"",
    ]

    if has_issues:
        lines.append(f"{RED}{BOLD}=== Critical Issues ==={RESET}")
        for r in has_issues:
            lines.append(f"{RED}❌ {r['path']}{RESET}")
            for issue in r["issues"]:
                lines.append(f"     - {issue}")
        lines.append("")

    if stale:
        lines.append(f"{RED}{BOLD}=== STALE skills (>{max_age_months} months) ==={RESET}")
        for r in stale:
            lines.append(f"{RED}🕰 {r['path']}{RESET}")
            for warning in r["warnings"]:
                if "STALE" in warning:
                    lines.append(f"     {warning}")
        lines.append("")

    if missing_legislative:
        lines.append(f"{YELLOW}{BOLD}=== Skills без last_legislative_update ==={RESET}")
        lines.append(f"(Это {len(missing_legislative)} из {total} skills — нужно добавить поле)")
        for r in missing_legislative[:20]:  # top-20 to avoid spam
            lines.append(f"  {YELLOW}⚠ {r['path']}{RESET}")
        if len(missing_legislative) > 20:
            lines.append(f"  ... ещё {len(missing_legislative) - 20}")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Audit skills staleness")
    parser.add_argument("--packs-root", default="packs", help="Path to packs/ directory")
    parser.add_argument("--max-age-months", type=int, default=6, help="Max age before STALE warning")
    parser.add_argument("--json", help="Output path for JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any warnings")
    args = parser.parse_args()

    packs_root = Path(args.packs_root).resolve()
    if not packs_root.exists():
        print(f"Error: packs root not found: {packs_root}", file=sys.stderr)
        sys.exit(2)

    skills = find_skills(packs_root)
    if not skills:
        print(f"Warning: no skills found in {packs_root}", file=sys.stderr)
        sys.exit(2)

    results = [audit_skill(s, args.max_age_months) for s in skills]
    results.sort(key=lambda r: r["path"])

    # Console report
    print(format_console(results, args.max_age_months))

    # JSON report
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({
                "audit_date": datetime.utcnow().isoformat(),
                "max_age_months": args.max_age_months,
                "total_skills": len(results),
                "results": results,
            }, f, ensure_ascii=False, indent=2)
        print(f"\nJSON report: {args.json}")

    # Exit code
    has_issues = any(r["issues"] for r in results)
    has_warnings = any(r["warnings"] for r in results)
    if has_issues:
        sys.exit(1)
    if args.strict and has_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
