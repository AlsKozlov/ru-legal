#!/usr/bin/env python3
"""Добавляет стандартный disclaimer ко всем SKILL.md файлам.

Идемпотентен: если disclaimer уже есть, файл не изменяется.
"""
from __future__ import annotations

from pathlib import Path

DISCLAIMER = """

---

## ⚠ Юридический disclaimer

Данный skill — **техническая платформа**, не оказывает юридических услуг по ст.2
ФЗ-63 «Об адвокатской деятельности». Outputs **не заменяют** консультацию
лицензированного юриста / адвоката ФПА.

AI может галлюцинировать, выдавать устаревшие нормы, неверно интерпретировать
факты. Material decisions (увольнение, M&A, налоговый спор, IP litigation) —
**обязательно** engage outside-адв ФПА с релевантной специализацией.

Проект `ru-legal` и его contributors не несут ответственности за решения,
принятые на основе outputs системы. Использование — на свой риск.
"""

DISCLAIMER_MARKER = "## ⚠ Юридический disclaimer"


def add_disclaimer(skill_path: Path) -> bool:
    """Returns True if file was modified."""
    content = skill_path.read_text(encoding="utf-8")
    if DISCLAIMER_MARKER in content:
        return False
    new_content = content.rstrip() + DISCLAIMER
    skill_path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skill_files = list(repo_root.glob("packs/*/skills/*/SKILL.md"))
    modified = 0
    for skill in skill_files:
        if add_disclaimer(skill):
            modified += 1
    print(f"Processed {len(skill_files)} SKILL.md files; modified {modified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
