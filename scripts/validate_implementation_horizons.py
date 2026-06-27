#!/usr/bin/env python3
"""Validate manifest implementation horizons and generated Appendix K.

`book_structure.json` is the source of truth for each chapter's first-build
slice and mature endpoint. Appendix K is generated from those fields. This
check keeps the build-horizon map exact, ordered, and public-safe without
claiming that any implementation, proof, benchmark, or release artifact exists.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
APPENDIX = ROOT / "appendices" / "K_implementation_horizons.qmd"

MINIMUM_FIELD = "minimal_implementation"
BEYOND_FIELD = "beyond_state_of_art"
MINIMUM_WORD_FLOOR = 7
BEYOND_WORD_FLOOR = 55

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
ROW_RE = re.compile(r"^\| `([^`]+)` \| (.*?) \| (.*?) \| (.*?) \| `([^`]+)` \|$")
ARTIFACT_SIGNAL_RE = re.compile(
    r"\b("
    r"artifact|appendix|bot|checklist|constitution|contract|controller|crosswalk|"
    r"dashboard|derivation|diagram|example|field|file|fixture|format|ledger|"
    r"lifecycle|matrix|model|plan|predicate|protocol|record|registry|repo|"
    r"report|rubric|schema|state machine|table|template|trace|validator|"
    r"workflow|workspace|taxonomy"
    r")s?\b",
    re.IGNORECASE,
)
MATURE_SIGNAL_RE = re.compile(
    r"\b(mature version|logical end state|mature boundary|product-level endpoint|"
    r"product surface|end state|operational contract|target architecture)\b",
    re.IGNORECASE,
)
PLACEHOLDER_RE = re.compile(
    r"\b(No manifest|declared yet|TBD|TODO|placeholder|to be written)\b",
    re.IGNORECASE,
)
CURRENT_RESULT_RE = re.compile(
    r"\b(implemented and validated|validated locally|benchmark result|proof result|"
    r"has been reproduced|is proven|is deployed)\b",
    re.IGNORECASE,
)


def fail(errors: list[str]) -> None:
    print("Implementation horizon validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_structure() -> dict:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_parts(structure: dict) -> list[dict]:
    return [part for part in structure.get("parts", []) if isinstance(part, dict)]


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part_index, part in enumerate(flatten_parts(structure), start=1):
        for chapter_index, chapter in enumerate(part.get("chapters", []), start=1):
            if not isinstance(chapter, dict):
                continue
            merged = dict(chapter)
            merged["_part_index"] = part_index
            merged["_part_title"] = str(part.get("title", ""))
            merged["_chapter_index"] = chapter_index
            chapters.append(merged)
    return chapters


def qmd_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def validate_manifest_fields(chapters: list[dict]) -> list[str]:
    errors: list[str] = []
    for chapter in chapters:
        chapter_id = str(chapter.get("id", ""))
        minimum = str(chapter.get(MINIMUM_FIELD, "")).strip()
        beyond = str(chapter.get(BEYOND_FIELD, "")).strip()
        support = str(chapter.get("evidence_level", "")).strip()

        if not minimum:
            errors.append(f"{chapter_id}: missing {MINIMUM_FIELD}.")
        if not beyond:
            errors.append(f"{chapter_id}: missing {BEYOND_FIELD}.")
        if PLACEHOLDER_RE.search(minimum):
            errors.append(f"{chapter_id}: {MINIMUM_FIELD} still contains placeholder language.")
        if PLACEHOLDER_RE.search(beyond):
            errors.append(f"{chapter_id}: {BEYOND_FIELD} still contains placeholder language.")
        if word_count(minimum) < MINIMUM_WORD_FLOOR:
            errors.append(
                f"{chapter_id}: {MINIMUM_FIELD} has {word_count(minimum)} words; "
                f"minimum is {MINIMUM_WORD_FLOOR}."
            )
        if word_count(beyond) < BEYOND_WORD_FLOOR:
            errors.append(
                f"{chapter_id}: {BEYOND_FIELD} has {word_count(beyond)} words; "
                f"minimum is {BEYOND_WORD_FLOOR}."
            )
        if minimum and not ARTIFACT_SIGNAL_RE.search(minimum):
            errors.append(
                f"{chapter_id}: {MINIMUM_FIELD} should name a concrete artifact, "
                "record, schema, table, plan, validator, fixture, trace, or workflow."
            )
        if beyond and not MATURE_SIGNAL_RE.search(beyond):
            errors.append(
                f"{chapter_id}: {BEYOND_FIELD} should explicitly frame a mature "
                "target state or operational contract."
            )
        if CURRENT_RESULT_RE.search(minimum) or CURRENT_RESULT_RE.search(beyond):
            errors.append(
                f"{chapter_id}: implementation horizon text appears to claim a current "
                "result; horizons must remain target/build-planning text."
            )
        if not support:
            errors.append(f"{chapter_id}: evidence_level is missing.")

    return errors


def appendix_rows(text: str) -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    for line in text.splitlines():
        match = ROW_RE.match(line)
        if match:
            rows.append(match.groups())
    return rows


def validate_appendix(structure: dict, chapters: list[dict]) -> list[str]:
    errors: list[str] = []
    if not APPENDIX.exists():
        return [f"Missing generated appendix: {APPENDIX.relative_to(ROOT)}"]

    text = APPENDIX.read_text(encoding="utf-8", errors="ignore")
    parts = flatten_parts(structure)
    rows = appendix_rows(text)

    required_strings = [
        "# Implementation Horizons",
        "This appendix is generated from `book_structure.json`.",
        "The minimum viable implementation column is not a claim that the implementation already exists.",
        "The beyond-state-of-the-art column is a target architecture, not a current-result claim.",
        f"Current generated coverage: {len(chapters)} chapter implementation horizons.",
    ]
    for needle in required_strings:
        if needle not in text:
            errors.append(f"appendices/K_implementation_horizons.qmd is missing required text: {needle!r}")

    for part in parts:
        title = str(part.get("title", ""))
        if f"## {qmd_escape(title)}" not in text:
            errors.append(f"appendices/K_implementation_horizons.qmd is missing part section: {title!r}")

    if len(rows) != len(chapters):
        errors.append(
            f"appendices/K_implementation_horizons.qmd has {len(rows)} chapter rows; "
            f"manifest has {len(chapters)} chapters."
        )

    for index, chapter in enumerate(chapters):
        if index >= len(rows):
            break
        row_id, row_title, row_minimum, row_beyond, row_support = rows[index]
        expected = (
            qmd_escape(chapter.get("id", "")),
            qmd_escape(chapter.get("title", "")),
            qmd_escape(chapter.get(MINIMUM_FIELD, "")),
            qmd_escape(chapter.get(BEYOND_FIELD, "")),
            qmd_escape(chapter.get("evidence_level", "")),
        )
        actual = (row_id, row_title, row_minimum, row_beyond, row_support)
        if actual != expected:
            errors.append(
                "appendices/K_implementation_horizons.qmd row "
                f"{index + 1} does not match manifest chapter "
                f"{chapter.get('id', '')!r}."
            )

    return errors


def main() -> None:
    structure = load_structure()
    chapters = flatten_chapters(structure)
    errors = validate_manifest_fields(chapters)
    errors.extend(validate_appendix(structure, chapters))

    if errors:
        fail(errors)

    print(
        "Implementation horizon validation passed: "
        f"{len(chapters)} chapters across {len(flatten_parts(structure))} parts."
    )


if __name__ == "__main__":
    main()
