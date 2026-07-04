#!/usr/bin/env python3
"""Validate the public-safe Circle cyclic-memory receipt slice.

This is a structural evidence-surface check. It keeps the Coil chapter concrete
about Circle receipt facts without allowing residue/winding bookkeeping to turn
into a learned-memory, long-context, or support-state claim.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_cyclic_memory_receipt_slice" / "results" / "2026-07-02-local.json"
README = ROOT / "experiments" / "circle_cyclic_memory_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_cyclic_memory_receipt_slice.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"

EXPECTED = {
    "result_id": "2026-07-02-local-circle-cyclic-memory-receipt-slice",
    "slice_id": "circle_cyclic_memory_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-MEMORY-001",
    "kind": "cyclic_memory_residue_winding",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a",
    "pytest_summary": "3 passed in 2.51s",
}

THEOREMS = ("AIM-T0001", "AIM-T0002", "AIM-T0004", "AIM-T0005")
RECOMMENDATIONS = (
    "MEMORY-ATTACH-WINDING-ALIAS-PROVENANCE",
    "MEMORY-AUDIT-FINITE-ALIAS-LOAD",
)
OUTPUT_HASHES = {
    "67d4a8f79a3e12e673e35f979360d168a62522e99e1b76c190d0ecd3020d1bf9": 5630,
    "e87f0835f24fca86c62b028582e40ed2792be9581da0f8fe3d972168d9e0fafc": 895,
    "4efa49e37b258c58a67fd6915ff26772bd53cff4937329f9382c98530c39426e": 3924,
    "657b1e3ad1e0cd9c3ab032ed29b580e716a78fc082f3d3517dffc07f7ce070a6": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove retrieval quality",
    "model quality",
    "context length",
    "memory scaling",
    "deployment safety",
    "transfer",
    "ASI",
)
READER_SURFACE_FRAGMENTS = (
    "concrete Circle receipt",
    "finite residue/winding fixture",
    "one residue slot",
    "one winding index",
    "four same-residue events",
    "four same-residue windings",
    "bounded alias load",
    "expected theorem IDs",
    "alias-provenance",
    "finite-load audit",
    "recorded a fingerprint",
    EXPECTED["pytest_summary"],
) + NON_CLAIMS


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    lower = " ".join(text.lower().split())
    for fragment in fragments:
        normalized = " ".join(fragment.lower().split())
        if normalized not in lower:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def validate_result(errors: list[str]) -> dict[str, Any]:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}.")
        return {}
    result = load_json(RESULT)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain a JSON object.")
        return {}

    if "/Users/" in text_blob(result):
        errors.append(f"{rel(RESULT)} must not contain absolute local user paths.")

    project = result.get("external_project", {})
    if not isinstance(project, dict) or project.get("git_commit") != EXPECTED["git_commit"]:
        errors.append(f"{rel(RESULT)} must record Circle commit {EXPECTED['git_commit']}.")
    if project.get("worktree_state") != "clean_before_commands":
        errors.append(f"{rel(RESULT)} must record the clean external worktree boundary.")

    receipt = result.get("accepted_receipt", {})
    if not isinstance(receipt, dict):
        errors.append(f"{rel(RESULT)} accepted_receipt must be an object.")
        return result
    for key in ("contract_id", "kind", "receipt_schema", "schema_id", "pack_content_fingerprint", "contract_content_fingerprint"):
        if receipt.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} accepted_receipt.{key} must be {EXPECTED[key]!r}.")
    if receipt.get("accepted") is not True:
        errors.append(f"{rel(RESULT)} accepted_receipt.accepted must be true.")
    if tuple(receipt.get("required_theorem_ids", [])) != THEOREMS:
        errors.append(f"{rel(RESULT)} theorem IDs must remain {THEOREMS}.")
    if tuple(receipt.get("required_recommendation_ids", [])) != RECOMMENDATIONS:
        errors.append(f"{rel(RESULT)} recommendation IDs must remain {RECOMMENDATIONS}.")

    fields = receipt.get("evidence_fields", {})
    expected_fields = {
        "bank_size": 8,
        "event_index": 23,
        "event_count": 32,
        "residue_slot": 7,
        "winding": 2,
        "same_residue_events": [7, 15, 23, 31],
        "same_residue_windings": [0, 1, 2, 3],
        "max_alias_load": 4,
        "slot_loads": [4, 4, 4, 4, 4, 4, 4, 4],
    }
    if fields != expected_fields:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded Circle fixture facts.")

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 4:
        errors.append(f"{rel(RESULT)} must record exactly four successful commands.")
    else:
        seen_hashes: dict[str, int] = {}
        command_text = text_blob(commands)
        for command in commands:
            if not isinstance(command, dict):
                errors.append(f"{rel(RESULT)} commands must be objects.")
                continue
            if command.get("verification_result") != "pass":
                errors.append(f"{rel(RESULT)} command {command.get('command')} did not record pass.")
            sha = command.get("output_sha256")
            size = command.get("output_bytes")
            if isinstance(sha, str) and isinstance(size, int):
                seen_hashes[sha] = size
        for sha, size in OUTPUT_HASHES.items():
            if seen_hashes.get(sha) != size:
                errors.append(f"{rel(RESULT)} missing output hash {sha} with byte size {size}.")
        for fragment in (
            "PYTHONPATH=. python3 scripts/cyclic_memory_certify.py --format json",
            EXPECTED["pytest_summary"],
            "ready=True fields=3 missing=0 theorems=4",
            "accepted true",
        ):
            if fragment not in command_text:
                errors.append(f"{rel(RESULT)} command summaries missing {fragment!r}.")

    if result.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIMS, errors)
    for fragment in ("ModuleNotFoundError", "C.UTF-8"):
        if fragment not in text_blob(result.get("discarded_attempts", [])):
            errors.append(f"{rel(RESULT)} discarded_attempts missing {fragment!r}.")
    return result


def validate_public_surfaces(errors: list[str]) -> None:
    for path in (README, SUMMARY, STRUCTURE, OUTLINE, CHAPTER, READER, ROADMAP):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        return

    result_fragments = (
        EXPECTED["git_commit"],
        EXPECTED["contract_id"],
        EXPECTED["kind"],
        EXPECTED["contract_content_fingerprint"],
        "same_residue_events",
        "[7, 15, 23, 31]",
        "same_residue_windings",
        "[0, 1, 2, 3]",
        "max_alias_load=4",
        EXPECTED["pytest_summary"],
    ) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS

    for path in (SUMMARY, CHAPTER, OUTLINE, ROADMAP):
        text = path.read_text(encoding="utf-8")
        require_fragments(rel(path), text, result_fragments, errors)
    require_fragments(
        rel(READER),
        READER.read_text(encoding="utf-8"),
        READER_SURFACE_FRAGMENTS,
        errors,
    )

    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
        return
    chapter = chapter_record(structure, "coil-attention-cyclic-memory-and-recurrence-contracts")
    if chapter.get("evidence_level") != "argument":
        errors.append("Coil chapter evidence_level must remain argument.")
    tests = text_blob(chapter.get("codex_tests", []))
    if "Circle cyclic memory receipt-slice validation" not in tests:
        errors.append("Coil chapter manifest is missing the Circle cyclic memory receipt-slice test row.")
    if "no retrieval-quality, long-context, model-quality, speed, memory-scaling, deployment, transfer, ASI, or support-state-transition claim" not in tests:
        errors.append("Coil chapter manifest test row must preserve non-claim boundary.")


def fail(errors: list[str]) -> None:
    print("Circle cyclic-memory receipt-slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_public_surfaces(errors)
    if errors:
        fail(errors)
    print("Circle cyclic-memory receipt-slice validation passed.")


if __name__ == "__main__":
    main()
