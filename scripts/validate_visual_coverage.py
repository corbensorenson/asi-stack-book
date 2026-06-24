#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(errors: list[str]) -> None:
    for error in errors:
        print(error)
    sys.exit(1)


def main() -> None:
    errors: list[str] = []

    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            path = ROOT / chapter["file"]
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "```{mermaid}" not in text:
                errors.append(f"Chapter lacks a Mermaid interface/lifecycle diagram: {chapter['file']}")

    index = (ROOT / "index.qmd").read_text(encoding="utf-8", errors="ignore")
    hero = ROOT / "assets" / "images" / "asi-stack-hero.png"
    if "assets/images/asi-stack-hero.png" not in index:
        errors.append("index.qmd does not reference the landing-page hero image.")
    if not hero.exists():
        errors.append("Landing-page hero image is missing: assets/images/asi-stack-hero.png")

    if errors:
        fail(errors)

    print("Visual coverage validation passed.")


if __name__ == "__main__":
    main()
