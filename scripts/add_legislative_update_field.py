#!/usr/bin/env python3
"""add_legislative_update_field.py — Bulk-добавление last_legislative_update.

144+ skills изначально написаны без `last_legislative_update` поля.
Этот script:
1. Сканирует все skills
2. Если поле отсутствует — добавляет с дефолтным значением
3. Если есть `ported_at` — использует его как initial date

Usage:
    python scripts/add_legislative_update_field.py --dry-run
    python scripts/add_legislative_update_field.py --apply
    python scripts/add_legislative_update_field.py --apply --default-date 2026-05
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.DOTALL)


def add_field_to_frontmatter(text: str, default_date: str) -> tuple[str, bool]:
    """Return (new_text, modified)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, False

    head, body, tail = m.group(1), m.group(2), m.group(3)

    # Already has the field?
    if re.search(r"^last_legislative_update\s*:", body, re.MULTILINE):
        return text, False

    # Try to extract initial date from ported_at if present
    initial_date = default_date
    ported_match = re.search(r"^ported_at\s*:\s*(\S+)", body, re.MULTILINE)
    if ported_match:
        raw_date = ported_match.group(1).strip().strip('"').strip("'")
        # YYYY-MM-DD → YYYY-MM
        if re.match(r"\d{4}-\d{2}-\d{2}", raw_date):
            initial_date = raw_date[:7]
        elif re.match(r"\d{4}-\d{2}", raw_date):
            initial_date = raw_date

    # Add field — try to put after `version` if present, else at end
    new_field_line = f'last_legislative_update: "{initial_date}"  # auto-added 2026-05-26'

    version_match = re.search(r"^(version\s*:\s*\S+\n)", body, re.MULTILINE)
    if version_match:
        # Insert after version line
        end_pos = version_match.end()
        new_body = body[:end_pos] + new_field_line + "\n" + body[end_pos:]
    else:
        # Append at end
        new_body = body.rstrip("\n") + "\n" + new_field_line

    return text.replace(m.group(0), head + new_body + tail, 1), True


def find_skills(packs_root: Path) -> list[Path]:
    skills = []
    for pack_dir in packs_root.iterdir():
        if not pack_dir.is_dir() or pack_dir.name.startswith("_"):
            continue
        skills_dir = pack_dir / "skills"
        if not skills_dir.exists():
            continue
        for skill_dir in skills_dir.iterdir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills.append(skill_file)
    return skills


def main():
    parser = argparse.ArgumentParser(description="Bulk-add last_legislative_update field")
    parser.add_argument("--packs-root", default="packs")
    parser.add_argument(
        "--default-date",
        default=datetime.utcnow().strftime("%Y-%m"),
        help="Default date if no ported_at found (YYYY-MM)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Specify --dry-run or --apply", file=sys.stderr)
        sys.exit(2)

    packs_root = Path(args.packs_root).resolve()
    skills = find_skills(packs_root)
    print(f"Found {len(skills)} skills")

    modified_count = 0
    already_count = 0

    for skill_path in skills:
        text = skill_path.read_text(encoding="utf-8")
        new_text, modified = add_field_to_frontmatter(text, args.default_date)
        rel = skill_path.relative_to(packs_root)

        if modified:
            modified_count += 1
            print(f"  ✏ {rel}")
            if args.apply:
                skill_path.write_text(new_text, encoding="utf-8")
        else:
            already_count += 1

    print(f"\nSummary:")
    print(f"  Modified: {modified_count}")
    print(f"  Already had field: {already_count}")
    print(f"  Mode: {'APPLIED' if args.apply else 'DRY-RUN (use --apply to write)'}")


if __name__ == "__main__":
    main()
