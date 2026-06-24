#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_WORDS = 18


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return "\n".join(lines[index + 1 :])
    return text


def paragraph_words(paragraph: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", paragraph)


def normalized_paragraphs(path: Path) -> list[str]:
    text = strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    paragraphs: list[str] = []
    in_code = False
    current: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            if current:
                paragraphs.append(" ".join(" ".join(current).split()))
                current = []
            continue
        current.append(stripped)

    if current:
        paragraphs.append(" ".join(" ".join(current).split()))

    filtered = []
    for paragraph in paragraphs:
        if paragraph.startswith("|"):
            continue
        if paragraph.startswith("#"):
            continue
        if len(paragraph_words(paragraph)) < MIN_WORDS:
            continue
        filtered.append(paragraph)
    return filtered


def main() -> None:
    locations: dict[str, list[str]] = defaultdict(list)
    for path in sorted((ROOT / "chapters").glob("*.qmd")):
        for paragraph in normalized_paragraphs(path):
            locations[paragraph].append(str(path.relative_to(ROOT)))

    repeats = {paragraph: paths for paragraph, paths in locations.items() if len(paths) > 1}
    if repeats:
        print(f"Repeated long prose paragraphs found: {len(repeats)}")
        for paragraph, paths in sorted(repeats.items(), key=lambda item: (-len(item[1]), item[0])):
            print(f" - {len(paths)}x {paths}: {paragraph[:220]}")
        sys.exit(1)

    print("Repeated prose validation passed.")


if __name__ == "__main__":
    main()
