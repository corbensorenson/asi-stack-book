#!/usr/bin/env python3
"""Validate reviewer-facing core-claim promotion paths in Appendix C."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
EVIDENCE_PLAN = ROOT / "docs" / "per_chapter_evidence_plan.md"
APPENDIX_C = ROOT / "appendices" / "C_claim_evidence_matrix.qmd"
ROW_RE = re.compile(r"^\|\s*([IVX]+)\s*\|\s*`([^`]+)`\s*\|")

REQUIRED_APPENDIX_STRINGS = [
    "What would promote this",
    "reviewer-facing promotion-path rows from `docs/per_chapter_evidence_plan.md`",
    "No chapter core claim is marked `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` yet.",
    "They do not promote any chapter core claim above `argument`.",
]

FORBIDDEN_STRINGS = [
    "automatically promotes",
    "promotion is guaranteed",
    "now source-derived",
    "now prototype-backed",
    "now synthetic-test-backed",
    "now empirical-test-backed",
    "now external-literature-backed",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def qmd_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def promotion_paths() -> dict[str, str]:
    paths: dict[str, str] = {}
    duplicates: set[str] = set()
    for line in EVIDENCE_PLAN.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = ROW_RE.match(line.strip())
        if not match:
            continue
        chapter_id = match.group(2)
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            continue
        acceptance_bar = cells[5]
        if chapter_id in paths:
            duplicates.add(chapter_id)
        paths[chapter_id] = acceptance_bar
    if duplicates:
        raise SystemExit(f"Duplicate promotion-path rows in docs/per_chapter_evidence_plan.md: {sorted(duplicates)}")
    return paths


def fail(errors: list[str]) -> None:
    print("Core claim promotion path validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def main() -> None:
    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    chapters = flatten_chapters(structure)
    chapter_ids = {str(chapter.get("id")) for chapter in chapters}
    paths = promotion_paths()
    appendix = APPENDIX_C.read_text(encoding="utf-8", errors="ignore")

    errors: list[str] = []
    if set(paths) != chapter_ids:
        missing = sorted(chapter_ids - set(paths))
        extra = sorted(set(paths) - chapter_ids)
        if missing:
            errors.append(f"Missing promotion-path rows for chapters: {missing}")
        if extra:
            errors.append(f"Promotion-path rows reference unknown chapters: {extra}")

    for needle in REQUIRED_APPENDIX_STRINGS:
        if needle not in appendix:
            errors.append(f"Appendix C missing required promotion-path text: {needle}")

    for chapter in chapters:
        chapter_id = str(chapter.get("id"))
        path = paths.get(chapter_id)
        if not path:
            continue
        expected_claim_id = f"`{chapter_id}.core`"
        if expected_claim_id not in appendix:
            errors.append(f"Appendix C missing claim row for {chapter_id}.")
        if qmd_escape(path) not in appendix:
            errors.append(f"Appendix C missing promotion path for {chapter_id}: {path}")
        if str(chapter.get("evidence_level")) != "argument":
            errors.append(f"{chapter_id}: promotion-path validator expects current support state argument.")

    lowered = appendix.lower()
    for forbidden in FORBIDDEN_STRINGS:
        if forbidden in lowered:
            errors.append(f"Appendix C contains forbidden promotion overclaim: {forbidden}")

    if errors:
        fail(errors)

    print(
        "Core claim promotion path validation passed: "
        f"{len(paths)} reviewer-facing promotion paths, "
        f"{len(chapters)} chapter core claims remain at argument."
    )


if __name__ == "__main__":
    main()
