#!/usr/bin/env python3
"""Validate concrete Circle receipt facts surfaced in the book.

The Circle external receipt slice is one of the project's few public-safe
prototype-backed evidence lanes. This check keeps the chapter prose concrete
without letting a structural receipt become model-quality, context-length,
runtime, transfer, deployment, or chapter-core evidence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "docs" / "circle_external_receipt_slice.md"
CONSUMER_GATE = ROOT / "docs" / "circle_public_replay_consumer_gate.md"
RESULT = ROOT / "experiments" / "circle_external_receipt_slice" / "results" / "2026-06-29-local.json"
CONSUMER_FIXTURE = (
    ROOT
    / "experiments"
    / "circle_public_replay"
    / "fixtures"
    / "valid"
    / "circle_rope_receipt.consumer.valid.json"
)
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CIRCLE_CHAPTER = ROOT / "chapters" / "circle-calculus-and-proof-carrying-ai-contracts.qmd"
COILRA_CHAPTER = ROOT / "chapters" / "coilra-multicoil-rope-and-cyclic-mixers.qmd"

THEOREM_IDS = (
    "AIRA-T0058",
    "AIRA-T0059",
    "AIRA-T0171",
    "AIRA-T0172",
    "AIRA-T0239",
    "AIRA-T0240",
    "AIRA-T0241",
)

CORE_FACTS = (
    "63b0f511",
    "CC-AI-CONTRACT-ROPE-001",
    "rope_position_distinguishability",
    "1/328459",
    "theorem_count 55",
    "fields=31 missing=0 theorems=75",
    "ROPE-USE-D19-MARGIN-FRONTIER",
    "91b72a6dcf821a9733f21800cd1093a3d0665588022031ba72c94893800330c3",
    "20e68c5f787e267c6611bc57b8d8e98e1cb0f5a74f272379716a5d83e761407d",
    "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468",
)

EXTERNAL_ONLY_FACTS = (
    "evidence.exact_discrete_pass=true",
    "evidence.total_bank_collision_pair_count=0",
    "145 passed in 718.24s (0:11:58)",
)

CONSUMER_FACTS = (
    "digest mismatch",
    "missing required theorem ID",
    "stale contract fingerprint status",
    "unsupported transfer-claim use",
)

NON_CLAIM_FRAGMENTS = (
    "does not promote any chapter core claim",
    "does not prove model quality",
    "context length",
    "speed",
    "memory",
    "deployment safety",
    "transfer",
    "ASI",
)

TARGET_CHAPTERS = {
    CIRCLE_CHAPTER: (
        "Concrete Circle Receipt Boundary",
        "theorem_count 55",
        "fields=31 missing=0 theorems=75",
        "seven theorem IDs",
        "does not promote the Circle core claim",
        "does not prove model quality",
    ),
    COILRA_CHAPTER: (
        "Recorded RoPE Receipt Boundary",
        "evidence.exact_discrete_pass=true",
        "evidence.total_bank_collision_pair_count=0",
        "diagnostic structural use",
        "does not prove longer usable context",
        "does not prove model quality",
    ),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    lower_text = text.lower()
    for fragment in fragments:
        lower_fragment = fragment.lower()
        if lower_fragment == "theorem_count 55":
            if "theorem_count" in lower_text and "55" in lower_text:
                continue
        if lower_fragment not in lower_text:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def main() -> None:
    errors: list[str] = []

    for path in (SUMMARY, CONSUMER_GATE, RESULT, CONSUMER_FIXTURE, STRUCTURE, OUTLINE, CIRCLE_CHAPTER, COILRA_CHAPTER):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    summary_text = SUMMARY.read_text(encoding="utf-8")
    consumer_text = CONSUMER_GATE.read_text(encoding="utf-8")
    result = load_json(RESULT)
    fixture = load_json(CONSUMER_FIXTURE)
    structure = load_json(STRUCTURE)
    outline_text = OUTLINE.read_text(encoding="utf-8")
    result_text = text_blob(result)
    fixture_text = text_blob(fixture)

    require_fragments(rel(SUMMARY), summary_text, CORE_FACTS + EXTERNAL_ONLY_FACTS + THEOREM_IDS + NON_CLAIM_FRAGMENTS, errors)
    require_fragments(rel(CONSUMER_GATE), consumer_text, CORE_FACTS[:3] + THEOREM_IDS + CONSUMER_FACTS + NON_CLAIM_FRAGMENTS, errors)
    require_fragments(rel(RESULT), result_text, CORE_FACTS[:8] + THEOREM_IDS + ("145 passed in 718.24s (0:11:58)",), errors)
    require_fragments(rel(CONSUMER_FIXTURE), fixture_text, CORE_FACTS[:3] + THEOREM_IDS + NON_CLAIM_FRAGMENTS, errors)

    if result.get("claim_id") != "circle-calculus.external_rope_receipt_replay":
        errors.append(f"{rel(RESULT)}: claim_id must remain the non-core Circle receipt claim.")
    if result.get("support_transition", {}).get("new_support_state") != "prototype-backed":
        errors.append(f"{rel(RESULT)}: support transition must remain prototype-backed for the narrow non-core claim.")

    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
    else:
        for chapter_id, expected_test in (
            (
                "circle-calculus-and-proof-carrying-ai-contracts",
                "Circle concrete receipt evidence-surface validation",
            ),
            (
                "coilra-multicoil-rope-and-cyclic-mixers",
                "Circle concrete RoPE boundary evidence-surface validation",
            ),
        ):
            record = chapter_record(structure, chapter_id)
            if record.get("evidence_level") != "argument":
                errors.append(f"{chapter_id}: evidence_level must remain argument.")
            tests = text_blob(record.get("codex_tests", []))
            if expected_test not in tests:
                errors.append(f"{chapter_id}: missing manifest test row {expected_test!r}.")

    for path, fragments in TARGET_CHAPTERS.items():
        text = path.read_text(encoding="utf-8")
        require_fragments(rel(path), text, CORE_FACTS[:7] + THEOREM_IDS + fragments + NON_CLAIM_FRAGMENTS, errors)
        if 'evidence_level: "argument"' not in text:
            errors.append(f"{rel(path)} must keep evidence_level argument.")
        if "support: argument" not in text:
            errors.append(f"{rel(path)} must keep core claim support at argument.")
        if "trichotomy" in text and "trichotomy" not in summary_text:
            errors.append(f"{rel(path)} mentions trichotomy without ASI receipt-summary verification.")
        if "undecided interval" in text and "undecided interval" not in summary_text:
            errors.append(f"{rel(path)} mentions undecided interval without ASI receipt-summary verification.")

    require_fragments(
        rel(OUTLINE),
        outline_text,
        (
            "Circle concrete receipt evidence-surface validation",
            "Circle concrete RoPE boundary evidence-surface validation",
            "theorem_count 55",
            "fields=31 missing=0 theorems=75",
            "evidence.total_bank_collision_pair_count=0",
            "does not promote chapter-core support",
        ),
        errors,
    )

    if errors:
        fail(errors)

    print("Circle concrete evidence-surface validation passed.")


def fail(errors: list[str]) -> None:
    print("Circle concrete evidence-surface validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
