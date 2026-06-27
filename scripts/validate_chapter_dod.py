#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"

REQUIRED_SECTIONS = [
    "## Chapter status",
    "## Drafting guardrail",
    "## Problem",
    "## Why existing approaches are insufficient",
    "## Core Claim",
    "## Mechanism",
    "## Interfaces",
    "## Invariants",
    "## Failure modes",
    "## Minimum Viable Implementation",
    "## Beyond the State of the Art",
    "## Codex test plan",
    "## Source crosswalk",
    "## Summary",
]

ALLOWED_SUPPORT_STATES = {
    "unsupported",
    "argument",
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
    "deprecated",
    "refuted",
}

ALLOWED_CLAIM_LABELS = {
    "Demonstrated",
    "Measured",
    "Mechanized",
    "Hypothesized",
    "Design rationale",
    "Speculative",
}

BANNED_BEYOND_BOILERPLATE = [
    "is not the minimal artifact with more scale",
    "It is the chapter's idea turned into a product-grade",
    "For this chapter, beyond the state of the art means",
    "source mappings, schemas, Lean predicates, tests, benchmark records, runtime traces, review receipts, or governance artifacts",
    "This remains a target architecture. The support state should not rise until",
    "Its support state should not rise until the source mappings",
    "defines one boundary in the ASI Stack",
    "Its job is to make a capability more governable, not merely more impressive",
    "The reviewed sources justify",
    "The passage-reviewed sources justify",
    "The crosswalk identifies",
    "A mature implementation would make that contract visible through",
    "The smallest useful implementation is",
    "The practical standard is",
    "The next chapter",
    "the next chapter",
    "The current fixture",
    "The fixture should",
    "The schema validates",
    "Passing validation only",
    "That validation proves only",
    "This pass",
    "run in this pass",
    "mapped in this pass",
]

SUMMARY_BANNED_PATTERNS = [
    (
        "self-referential chapter phrase",
        re.compile(r"\b(?:this|the) chapter(?:'s)?\b", re.IGNORECASE),
    ),
    (
        "mechanical section handoff",
        re.compile(r"\bthe next section\b", re.IGNORECASE),
    ),
    (
        "live crosswalk reference",
        re.compile(r"\bcrosswalk\b", re.IGNORECASE),
    ),
]

PROBLEM_BANNED_PATTERNS = [
    (
        "self-referential chapter phrase",
        re.compile(r"\b(?:this|in this) chapter\b", re.IGNORECASE),
    ),
    (
        "mechanical backward handoff",
        re.compile(r"\bthe previous (?:chapter|layer)\b", re.IGNORECASE),
    ),
]

INSUFFICIENCY_BANNED_PATTERNS = [
    (
        "self-referential chapter phrase",
        re.compile(r"\b(?:this|the) chapter(?:'s)?\b", re.IGNORECASE),
    ),
    (
        "reader-direction meta phrase",
        re.compile(r"\bthe reader should treat this chapter\b", re.IGNORECASE),
    ),
]

SECTION_MIN_WORDS = {
    "## Problem": 130,
    "## Why existing approaches are insufficient": 130,
    "## Mechanism": 300,
    "## Interfaces": 130,
    "## Invariants": 110,
    "## Failure modes": 110,
    "## Minimum Viable Implementation": 125,
    "## Beyond the State of the Art": 200,
    "## Summary": 130,
}

SECTION_REQUIRED_PATTERNS = {
    "## Minimum Viable Implementation": [
        (
            "smallest honest start",
            re.compile(
                r"\b(minimum|minimal|first|smallest|viable|implementation|artifact|schema|fixture|validator|proof|test|trace|record|ledger|slice)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "non-promotion caveat",
            re.compile(
                r"\b(not|only|planned|remains|support|until|without|does not|should not|must not|unpromoted|argument)\b",
                re.IGNORECASE,
            ),
        ),
    ],
    "## Beyond the State of the Art": [
        (
            "mature target state",
            re.compile(
                r"\b(mature|logical end state|final product|end state|target architecture|product-level endpoint|beyond current practice)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "not current result",
            re.compile(
                r"\b(target architecture|not a current|remains a target|support should stay|support state|until|not a current-result claim)\b",
                re.IGNORECASE,
            ),
        ),
    ],
}

SECTION_PLACEHOLDERS = [
    "No manifest minimal implementation statement declared yet.",
    "No manifest beyond-state-of-the-art statement declared yet.",
]

MANIFEST_REQUIRED_TEXT_FIELDS = [
    "minimal_implementation",
    "beyond_state_of_art",
]


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            merged = dict(chapter)
            merged["_part_id"] = part["id"]
            merged["_part_title"] = part["title"]
            chapters.append(merged)
    return chapters


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf'^{re.escape(key)}:\s+"([^"]*)"', text, flags=re.MULTILINE)
    return match.group(1) if match else None


def section_body(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    next_heading = re.search(r"^##\s+", text[match.end() :], flags=re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end].strip()


def heading_positions(text: str, heading: str) -> list[int]:
    pattern = rf"^{re.escape(heading)}\s*$"
    return [match.start() for match in re.finditer(pattern, text, flags=re.MULTILINE)]


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def main() -> None:
    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")

    errors: list[str] = []
    for chapter in flatten_chapters(structure):
        for field in MANIFEST_REQUIRED_TEXT_FIELDS:
            value = chapter.get(field)
            if not isinstance(value, str) or not value.strip() or value.strip().startswith("No manifest "):
                errors.append(f"{chapter['file']}: manifest field {field!r} must be chapter-specific")

        path = ROOT / chapter["file"]
        if not path.exists():
            errors.append(f"{chapter['file']}: missing chapter file")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
        if missing_sections:
            errors.append(f"{chapter['file']}: missing DoD sections: {', '.join(missing_sections)}")

        section_positions: dict[str, list[int]] = {
            section: heading_positions(text, section) for section in REQUIRED_SECTIONS
        }
        duplicate_sections = [
            f"{section} ({len(positions)})"
            for section, positions in section_positions.items()
            if len(positions) > 1
        ]
        if duplicate_sections:
            errors.append(f"{chapter['file']}: duplicate DoD section headings: {', '.join(duplicate_sections)}")

        present_positions = [
            (section, positions[0]) for section, positions in section_positions.items() if positions
        ]
        if len(present_positions) == len(REQUIRED_SECTIONS):
            ordered_positions = [position for _, position in present_positions]
            if ordered_positions != sorted(ordered_positions):
                expected = " -> ".join(REQUIRED_SECTIONS)
                errors.append(f"{chapter['file']}: DoD sections must appear in order: {expected}")

        for section, min_words in SECTION_MIN_WORDS.items():
            body = section_body(text, section)
            if not body:
                continue
            words = word_count(body)
            if words < min_words:
                errors.append(
                    f"{chapter['file']}: {section} has {words} words; expected at least {min_words}"
                )
            for label, pattern in SECTION_REQUIRED_PATTERNS.get(section, []):
                if not pattern.search(body):
                    errors.append(f"{chapter['file']}: {section} must include a {label} signal")

        for placeholder in SECTION_PLACEHOLDERS:
            if placeholder in text:
                errors.append(f"{chapter['file']}: replace scaffold placeholder: {placeholder!r}")

        for phrase in BANNED_BEYOND_BOILERPLATE:
            if phrase in text:
                errors.append(f"{chapter['file']}: replace generic beyond-SOTA boilerplate phrase: {phrase!r}")

        summary = section_body(text, "## Summary")
        for label, pattern in SUMMARY_BANNED_PATTERNS:
            match = pattern.search(summary)
            if match:
                errors.append(
                    f"{chapter['file']}: ## Summary contains {label}: {match.group(0)!r}"
                )

        problem = section_body(text, "## Problem")
        for label, pattern in PROBLEM_BANNED_PATTERNS:
            match = pattern.search(problem)
            if match:
                errors.append(
                    f"{chapter['file']}: ## Problem contains {label}: {match.group(0)!r}"
                )

        insufficiency = section_body(text, "## Why existing approaches are insufficient")
        for label, pattern in INSUFFICIENCY_BANNED_PATTERNS:
            match = pattern.search(insufficiency)
            if match:
                errors.append(
                    f"{chapter['file']}: ## Why existing approaches are insufficient contains {label}: {match.group(0)!r}"
                )

        expected = {
            "chapter_id": chapter["id"],
            "part_id": chapter["_part_id"],
            "status": chapter.get("status", "conceptual"),
            "evidence_level": chapter.get("evidence_level", "argument"),
            "claim_label": chapter.get("claim_label", "Design rationale"),
        }
        for key, value in expected.items():
            actual = frontmatter_value(text, key)
            if actual != value:
                errors.append(f"{chapter['file']}: frontmatter {key!r} is {actual!r}, expected {value!r}")

        support = expected["evidence_level"]
        if support not in ALLOWED_SUPPORT_STATES:
            errors.append(f"{chapter['file']}: invalid evidence_level {support!r}")
        label = expected["claim_label"]
        if label not in ALLOWED_CLAIM_LABELS:
            errors.append(f"{chapter['file']}: invalid claim_label {label!r}")

        for source_id in chapter.get("source_ids", []):
            if f"`{source_id}`" not in text:
                errors.append(f"{chapter['file']}: source crosswalk does not mention `{source_id}`")

        if "| Test | Purpose | Status |" not in text:
            errors.append(f"{chapter['file']}: missing Codex test-plan table")

    if errors:
        print("Chapter Definition of Done validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Chapter DoD validation passed: {len(flatten_chapters(structure))} chapters.")


if __name__ == "__main__":
    main()
