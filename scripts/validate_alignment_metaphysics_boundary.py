#!/usr/bin/env python3
"""Validate constitutional-alignment metaphysics and lineage boundaries.

This is a text/surface audit. It does not judge metaphysical truth, moral
correctness, alignment quality, deployed policy behavior, or chapter support.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "experiments"
    / "constitutional_alignment_metaphysics_boundary"
    / "results"
    / "2026-07-02-local.json"
)
DOC = ROOT / "docs" / "alignment_metaphysics_boundary_audit.md"
LIVE = ROOT / "chapters" / "constitutional-alignment-substrate.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "constitutional-alignment-substrate.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"

COMMAND = "python3 scripts/validate_alignment_metaphysics_boundary.py"
TEST_NAME = "Metaphysics lineage boundary audit"

SOURCE_NOTES = [
    ROOT / "sources" / "source_notes" / "alignment_field.md",
    ROOT / "sources" / "source_notes" / "field_of_god.md",
    ROOT / "sources" / "source_notes" / "eternal_code.md",
    ROOT / "sources" / "source_notes" / "coherence_exchange.md",
]

LIVE_REQUIRED = [
    "runtime constraint design surface, not moral proof, metaphysical proof, legal proof, or deployed safety",
    "Readers do not need to accept a worldview",
    "Some stay lineage or speculative context",
    "External positioning is comparator-only",
    "Metaphysical lineage only; not technical evidence for physics, consciousness, or safety.",
    "Speculative/computational metaphysics; not runtime evidence.",
    "support: argument",
]

READER_REQUIRED = [
    "not asking the reader to accept a complete moral theory",
    "including metaphysical and philosophical ones",
    "refusing to treat the lineage itself as empirical proof",
    "Metaphysical claims stay labeled as interpretation",
    "Speculative metaphysics cannot quietly become enforcement authority",
    "The support state should stay at",
]

SOURCE_NOTE_REQUIRED = {
    "alignment_field.md": [
        "translated into engineering constraints rather than treated as settled metaphysics",
        "not as empirical proof of consciousness",
        "speculative, metaphysical, or heuristic",
    ],
    "field_of_god.md": [
        "not as empirical evidence",
        "should not be cited as technical evidence",
        "Mark any consciousness or metaphysics-derived material as speculative",
    ],
    "eternal_code.md": [
        "speculative framing only",
        "not evidence for physics, consciousness, or AI governance outcomes",
        "Keep all metaphysical material clearly marked as speculative or design rationale",
    ],
    "coherence_exchange.md": [
        "speculative or metaphysical",
        "Blurring author-intent context with external evidence",
    ],
}

FORBIDDEN_UNSCOPED = [
    "metaphysics proves",
    "consciousness proves",
    "field of god proves",
    "eternal code proves",
    "metaphysical proof of alignment",
    "moral correctness is proven",
    "deployed constitutional alignment is proven",
    "proves deployed constitutional alignment",
    "runtime corrigibility is proven",
    "proves runtime corrigibility",
    "conscious-safe system",
]

SURFACE_REQUIREMENTS = {
    DOC: [
        "Alignment Metaphysics Boundary Audit",
        str(RESULT.relative_to(ROOT)),
        "no support-state transition",
    ],
    OUTLINE: [
        TEST_NAME,
        str(RESULT.relative_to(ROOT)),
        "no moral-correctness, consciousness, deployed-alignment, or support-state claim",
    ],
    ROADMAP: [
        TEST_NAME,
        "metaphysical and consciousness language",
        "no support-state promotion",
    ],
    CHANGELOG: [
        TEST_NAME,
        str(RESULT.relative_to(ROOT)),
    ],
    VALIDATE_BOOK: [
        "scripts/validate_alignment_metaphysics_boundary.py",
        "docs/alignment_metaphysics_boundary_audit.md",
        "experiments/constitutional_alignment_metaphysics_boundary/results/2026-07-02-local.json",
        'run_validator("validate_alignment_metaphysics_boundary.py")',
    ],
}

NON_CLAIMS = [
    "does not prove metaphysical claims",
    "does not prove consciousness claims",
    "does not prove moral correctness",
    "does not prove deployed constitutional alignment",
    "does not prove runtime corrigibility",
    "does not promote the chapter support state",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Alignment metaphysics boundary audit failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def has_phrase(text: str, phrase: str) -> bool:
    normalized_text = " ".join(text.lower().split())
    normalized_phrase = " ".join(phrase.lower().split())
    return normalized_phrase in normalized_text


def require_phrases(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing required file: {rel(path)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in phrases:
        if not has_phrase(text, phrase):
            errors.append(f"{rel(path)} missing required boundary phrase {phrase!r}.")


def validate_forbidden_claims(errors: list[str]) -> None:
    for path in [LIVE, READER, *SOURCE_NOTES]:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in FORBIDDEN_UNSCOPED:
            if phrase in text:
                errors.append(f"{rel(path)} contains forbidden unscoped phrase {phrase!r}.")


def validate_source_notes(errors: list[str]) -> None:
    for path in SOURCE_NOTES:
        required = SOURCE_NOTE_REQUIRED.get(path.name, [])
        require_phrases(path, required, errors)


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "constitutional-alignment-substrate":
                chapter = candidate
                break
    if not isinstance(chapter, dict):
        errors.append("book_structure.json missing constitutional-alignment-substrate chapter.")
        return
    tests = chapter.get("codex_tests", [])
    if not isinstance(tests, list):
        errors.append("book_structure.json constitutional codex_tests must be a list.")
        return
    blob = json.dumps(tests, sort_keys=True).lower()
    if TEST_NAME.lower() not in blob:
        errors.append(f"book_structure.json codex_tests missing {TEST_NAME!r}.")
    if "no moral-correctness, consciousness, deployed-alignment, or support-state claim" not in blob:
        errors.append("book_structure.json codex_tests missing metaphysics audit non-claim boundary.")


def expected_result() -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.alignment_metaphysics_boundary.v0",
        "result_id": "2026-07-02-alignment-metaphysics-boundary-audit",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "chapter_id": "constitutional-alignment-substrate",
        "surfaces_checked": [
            rel(LIVE),
            rel(READER),
            rel(OUTLINE),
            rel(ROADMAP),
            rel(DOC),
            rel(MANIFEST),
        ],
        "source_notes_checked": [rel(path) for path in SOURCE_NOTES],
        "boundary_checks": {
            "live_chapter_marks_metaphysics_as_lineage": True,
            "reader_chapter_marks_metaphysics_as_lineage": True,
            "source_notes_preserve_author_intent_vs_evidence": True,
            "external_comparators_remain_comparator_only": True,
            "chapter_core_support_effect": "none",
            "evidence_transition_created": False,
        },
        "verification_result": "pass",
        "support_state_effect": "none",
        "residuals": [
            "This is a text/surface audit only; it does not inspect deployed behavior, reviewer quality, moral correctness, source truth, or runtime policy enforcement.",
            "The chapter remains at argument support.",
        ],
        "non_claims": NON_CLAIMS,
    }


def validate_result(write_result: bool, errors: list[str]) -> None:
    expected = expected_result()
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    if value.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)} verification_result must be pass.")
    if value.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    if value.get("boundary_checks", {}).get("evidence_transition_created") is not False:
        errors.append(f"{rel(RESULT)} must not create an evidence transition.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    require_phrases(LIVE, LIVE_REQUIRED, errors)
    require_phrases(READER, READER_REQUIRED, errors)
    validate_source_notes(errors)
    validate_forbidden_claims(errors)
    validate_manifest(errors)
    for path, phrases in SURFACE_REQUIREMENTS.items():
        require_phrases(path, phrases, errors)
    validate_result(args.write_result, errors)

    if errors:
        fail(errors)
    print("Alignment metaphysics boundary audit passed.")


if __name__ == "__main__":
    main()
