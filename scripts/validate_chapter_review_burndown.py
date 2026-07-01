#!/usr/bin/env python3
"""Validate the chapter-review burn-down in the v1.x roadmap.

The Claude chapter review is planning input, not evidence. This validator keeps
the roadmap action queue aligned with the current manifest so a future chapter
move, merge, or deletion cannot silently leave review weaknesses untracked.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
REVIEW = ROOT / "docs" / "CHAPTER_REVIEWS.md"

BURN_DOWN_HEADER = "### Milestone 2.5 - Chapter-by-Chapter Masterwork Burn-Down"
NEXT_HEADER_RE = re.compile(r"^###\s+", re.MULTILINE)
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")
PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|placeholder|fill this|later)\b", re.IGNORECASE)
ACTION_RE = re.compile(
    r"\b("
    r"add|added|archive|audit|backfill|build|cleanly|deepen|evaluate|finish|"
    r"ground|implement|import|keep|map|polish|pursue|reframe|refresh|replay|"
    r"rewrite|smooth|source-note|surface|tighten"
    r")\b",
    re.IGNORECASE,
)

REQUIRED_ROADMAP_FRAGMENTS = (
    "external-anchoring depth, not missing positioning",
    "narrow coverage, not weak proof",
    "qualitative signals until rechecked chapter by chapter",
    "This is not another scorecard.",
    "Do not mark a burn-down row complete in prose.",
    "Closure classes:",
    "proof-coverage",
    "test-or-evidence",
    "external-grounding",
    "reader-craft",
    "recorded-blocker",
)

REQUIRED_REVIEW_FRAGMENTS = (
    "Signal calibration (READ THIS",
    "engagement with the literature.",
    "Theorem count",
    "Test impl/planned cells are approximate.",
)


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure.get("parts", [])
        if isinstance(part, dict)
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def burn_down_section(roadmap_text: str) -> str:
    start = roadmap_text.find(BURN_DOWN_HEADER)
    if start == -1:
        raise ValueError(f"{ROADMAP.relative_to(ROOT)} is missing {BURN_DOWN_HEADER!r}.")
    match = NEXT_HEADER_RE.search(roadmap_text, start + len(BURN_DOWN_HEADER))
    return roadmap_text[start : match.start()] if match else roadmap_text[start:]


def table_rows(section: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    duplicates: list[str] = []
    for line in section.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        chapter_id, weakness, work = (part.strip() for part in match.groups())
        if chapter_id in rows:
            duplicates.append(chapter_id)
        rows[chapter_id] = (weakness, work)
    if duplicates:
        raise ValueError(f"Duplicate burn-down row(s): {', '.join(sorted(duplicates))}")
    return rows


def main() -> None:
    errors: list[str] = []

    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit(f"{STRUCTURE.relative_to(ROOT)} must contain an object.")
    chapters = flatten_chapters(structure)
    chapter_ids = [str(chapter.get("id", "")) for chapter in chapters]
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    review_text = REVIEW.read_text(encoding="utf-8")

    for fragment in REQUIRED_ROADMAP_FRAGMENTS:
        if fragment not in roadmap_text:
            errors.append(f"{ROADMAP.relative_to(ROOT)} missing roadmap calibration fragment: {fragment}")
    for fragment in REQUIRED_REVIEW_FRAGMENTS:
        if fragment not in review_text:
            errors.append(f"{REVIEW.relative_to(ROOT)} missing review calibration fragment: {fragment}")

    try:
        section = burn_down_section(roadmap_text)
        rows = table_rows(section)
    except ValueError as exc:
        errors.append(str(exc))
        rows = {}

    expected = set(chapter_ids)
    present = set(rows)
    for chapter_id in sorted(expected - present):
        errors.append(f"Missing burn-down row for manifest chapter `{chapter_id}`.")
    for chapter_id in sorted(present - expected):
        errors.append(f"Burn-down row references non-manifest chapter `{chapter_id}`.")

    for chapter_id in chapter_ids:
        if chapter_id not in rows:
            continue
        weakness, work = rows[chapter_id]
        if len(weakness) < 35:
            errors.append(f"`{chapter_id}` weakness cell is too vague: {weakness!r}")
        if len(work) < 55:
            errors.append(f"`{chapter_id}` roadmap-work cell is too vague: {work!r}")
        if PLACEHOLDER_RE.search(weakness) or PLACEHOLDER_RE.search(work):
            errors.append(f"`{chapter_id}` burn-down row contains placeholder language.")
        if not ACTION_RE.search(work):
            errors.append(f"`{chapter_id}` roadmap-work cell lacks an action verb.")

    circle_work = rows.get("circle-calculus-and-proof-carrying-ai-contracts", ("", ""))[1]
    if "source-verified" not in circle_work:
        errors.append("Circle burn-down row must require source-verified evidence before surfacing facts.")
    if "do not use trichotomy/undecided-interval language unless" not in circle_work:
        errors.append(
            "Circle burn-down row must guard trichotomy/undecided-interval language until source artifacts verify it."
        )

    structure_by_id = {str(chapter.get("id", "")): chapter for chapter in chapters}
    if structure_by_id.get("personal-compute-hives-and-federated-edge-intelligence", {}).get(
        "lean_module"
    ) != "AsiStackProofs.PersonalComputeHives":
        errors.append("Personal Compute Hives lean_module mapping is not wired.")
    if structure_by_id.get("artifact-steward-agents-and-living-project-governance", {}).get(
        "lean_module"
    ) != "AsiStackProofs.ArtifactStewardAgents":
        errors.append("Artifact Steward Agents lean_module mapping is not wired.")

    if errors:
        print("Chapter-review burn-down validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Chapter-review burn-down validation passed: "
        f"{len(rows)} roadmap rows cover {len(chapter_ids)} manifest chapters."
    )


if __name__ == "__main__":
    main()
