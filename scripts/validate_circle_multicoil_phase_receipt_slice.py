#!/usr/bin/env python3
"""Validate the public-safe Circle MultiCoil phase receipt slice.

This is a structural evidence-surface check. It keeps the CoilRA chapter
concrete about Circle MultiCoil phase-feature and relative-phase fixture facts
without allowing those facts to turn into model-quality, attention-quality,
retrieval, context-length, deployment, or support-state claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_multicoil_phase_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_multicoil_phase_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_multicoil_phase_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_multicoil_phase_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coilra-multicoil-rope-and-cyclic-mixers.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coilra-multicoil-rope-and-cyclic-mixers.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

EXPECTED = {
    "result_id": "2026-07-05-local-circle-multicoil-phase-receipt-slice",
    "slice_id": "circle_multicoil_phase_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-PHASE-FEATURE-001",
    "kind": "multicoil_phase_feature",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "4b562beab64ec863903e4267f50c90049f0d3fa612f6c1bb2f06ad07e821ffd7",
    "receipt_content_fingerprint": "f801f27b4d9218c4132648f9dd9439ac9a0c459fb82c972eab1f6af874696a16",
    "pytest_summary": "3 passed in 2.99s",
    "contract_ready_pytest_summary": "1 passed in 1.76s",
    "transition_id": "v1_x_measured.circle_multicoil_phase_receipt.no_change",
    "claim_id": "circle-calculus.multicoil_phase_receipt_slice",
}

THEOREMS = ("AIA-T0001", "AIA-T0002", "AIA-T0004", "AIT-T0004", "AIT-T0005")
RECOMMENDATIONS = (
    "PHASE-USE-JOINT-REPEAT-HORIZON",
    "PHASE-AUDIT-RELATIVE-SHIFT-INVARIANT",
)
OUTPUT_HASHES = {
    "c09ee4c02492c6909dd0512a75016023ee4ff4aeb7151d61ab5d86f6ca1f60b9": 6055,
    "72e5d297069f63596aab41ded949aa85b8321f6e49a0903595449dc4a344e1d8": 14026,
    "e4e80f9c65bd8b38820b71c5765164794b24551b05e7be9fe093ece632ba1fb9": 1562,
    "e6a4eb2722b409830ad45a30848b88d1af534fbaa6ac328495316ba47a94ab4d": 1378,
    "74fd32ab05d781b43e82019531ebaeb3be97b7097d9592ad5920069166b639b8": 98,
    "6262a8e2e6f2ad2d2de112173e9d549955762f82a7ab80d9fb2f247e0426b472": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove MultiCoil, RoPE, attention, retrieval, or model quality",
    "context length",
    "runtime speed",
    "memory scaling",
    "hardware efficiency",
    "training stability",
    "deployment readiness",
    "transfer",
    "benchmark performance",
    "ASI",
)
SURFACE_FRAGMENTS = (
    EXPECTED["git_commit"],
    EXPECTED["contract_id"],
    EXPECTED["kind"],
    EXPECTED["contract_content_fingerprint"],
    "periods=[5, 7]",
    "phase_tuple=[2, 2]",
    "shifted_phase_tuple=[2, 2]",
    "joint_repeat_horizon=35",
    "relative_phase=3",
    "shifted_relative_phase=3",
    "relative_phase_invariant=true",
    "theorem_count=5",
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
    "circle_multicoil_phase_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "MultiCoil phase receipt",
    "joint repeat horizon",
    "relative phase",
    "shifted_relative_phase=3",
    EXPECTED["contract_id"],
    EXPECTED["contract_content_fingerprint"],
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS


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
    for key in ("result_id", "slice_id"):
        if result.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} {key} must be {EXPECTED[key]!r}.")

    project = result.get("external_project", {})
    if not isinstance(project, dict) or project.get("git_commit") != EXPECTED["git_commit"]:
        errors.append(f"{rel(RESULT)} must record Circle commit {EXPECTED['git_commit']}.")
    if project.get("worktree_state") != "clean_before_commands":
        errors.append(f"{rel(RESULT)} must record the clean external worktree boundary.")

    fixture = result.get("phase_fixture", {})
    expected_fixture = {
        "periods": [5, 7],
        "position": 37,
        "phase_tuple": [2, 2],
        "shifted_position": 72,
        "shifted_phase_tuple": [2, 2],
        "joint_repeat_horizon": 35,
        "query_position": 41,
        "key_position": 18,
        "relative_period": 5,
        "relative_phase": 3,
        "shifted_relative_phase": 3,
        "relative_phase_invariant": True,
        "ordinary_baselines": ["existing_position_bucket", "learned_position", "wrong_period", "no_phase_feature"],
        "contract_ready_theorem_count": 5,
        "circle_ai_receipt_theorem_count": 5,
    }
    if fixture != expected_fixture:
        errors.append(f"{rel(RESULT)} phase_fixture drifted from the recorded Circle MultiCoil phase facts.")

    receipt = result.get("accepted_receipt", {})
    if not isinstance(receipt, dict):
        errors.append(f"{rel(RESULT)} accepted_receipt must be an object.")
        return result
    for key in ("contract_id", "kind", "receipt_schema", "schema_id", "pack_content_fingerprint", "contract_content_fingerprint", "receipt_content_fingerprint"):
        if receipt.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} accepted_receipt.{key} must be {EXPECTED[key]!r}.")
    if receipt.get("accepted") is not True:
        errors.append(f"{rel(RESULT)} accepted_receipt.accepted must be true.")
    if tuple(receipt.get("required_theorem_ids", [])) != THEOREMS:
        errors.append(f"{rel(RESULT)} theorem IDs must remain {THEOREMS}.")
    if tuple(receipt.get("required_recommendation_ids", [])) != RECOMMENDATIONS:
        errors.append(f"{rel(RESULT)} recommendation IDs must remain {RECOMMENDATIONS}.")
    if receipt.get("theorem_count") != 5:
        errors.append(f"{rel(RESULT)} theorem_count must remain 5.")
    if receipt.get("evidence_fields") != {"joint_repeat_horizon": 35, "relative_phase": 3}:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded MultiCoil receipt facts.")

    recommendations = receipt.get("planner_recommendations", [])
    if not isinstance(recommendations, list) or len(recommendations) != 2:
        errors.append(f"{rel(RESULT)} planner_recommendations must record exactly two recommendations.")
    else:
        ids = [rec.get("id") for rec in recommendations if isinstance(rec, dict)]
        if tuple(ids) != RECOMMENDATIONS:
            errors.append(f"{rel(RESULT)} planner_recommendations must remain {RECOMMENDATIONS}.")
        require_fragments(
            rel(RESULT),
            text_blob(recommendations),
            (
                "not a learned-embedding, extrapolation, training-stability, context-length, or model-quality proof",
                "not an attention quality, retrieval, equivariant-model, or model-quality theorem",
            ),
            errors,
        )

    boundary = result.get("circle_ai_certifier_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("request_passed") is not True:
        errors.append(f"{rel(RESULT)} must preserve request_passed=true for the phase-feature boundary.")
    require_fragments(
        rel(RESULT),
        text_blob(boundary),
        ("unsupported_fields", "feature usefulness in a trained model", "all-real-phase RoPE separation", "not MultiCoil"),
        errors,
    )

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 6:
        errors.append(f"{rel(RESULT)} must record exactly six successful commands.")
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
            "PYTHONPATH=. python3 scripts/multicoil_phase_feature_certify.py --format json",
            "ready=True fields=7 missing=0 theorems=5",
            "strict MultiCoil phase acceptance receipt accepted",
            EXPECTED["pytest_summary"],
            EXPECTED["contract_ready_pytest_summary"],
        ):
            if fragment not in command_text:
                errors.append(f"{rel(RESULT)} command summaries missing {fragment!r}.")

    if result.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIMS, errors)
    return result


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    transition = load_json(TRANSITION)
    if not isinstance(transition, dict):
        errors.append(f"{rel(TRANSITION)} must contain a JSON object.")
        return
    expected_pairs = {
        "transition_id": EXPECTED["transition_id"],
        "claim_id": EXPECTED["claim_id"],
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "verification_result": "pass",
        "support_state_effect": "blocks_promotion",
    }
    for key, expected in expected_pairs.items():
        if transition.get(key) != expected:
            errors.append(f"{rel(TRANSITION)} {key} must be {expected!r}.")
    for path in (str(SUMMARY.relative_to(ROOT)), str(RESULT.relative_to(ROOT)), "scripts/validate_circle_multicoil_phase_receipt_slice.py"):
        if path not in text_blob(transition):
            errors.append(f"{rel(TRANSITION)} missing artifact ref {path!r}.")
    require_fragments(rel(TRANSITION), text_blob(transition), NON_CLAIMS, errors)
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            "joint_repeat_horizon=35",
            "relative_phase=3",
            "shifted_relative_phase=3",
            "ordinary position-bucket, learned-position, RoPE, dense-attention, recurrent, or state-space baselines",
            "does not create an upward support-state transition",
            "does not promote the CoilRA chapter core claim",
        ),
        errors,
    )


def validate_surfaces(errors: list[str]) -> None:
    for path in (README, SUMMARY, LEDGER, STRUCTURE, OUTLINE, CHAPTER, READER, ROADMAP, APPENDIX_E):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        fragments = READER_FRAGMENTS if path == READER else SURFACE_FRAGMENTS
        require_fragments(rel(path), text, fragments, errors)

    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
        return
    chapter = chapter_record(structure, "coilra-multicoil-rope-and-cyclic-mixers")
    if not chapter:
        errors.append(f"{rel(STRUCTURE)} missing CoilRA chapter record.")
        return
    if chapter.get("evidence_level") != "argument":
        errors.append("CoilRA chapter evidence_level must remain argument.")
    tests = chapter.get("codex_tests", [])
    if not isinstance(tests, list) or not any(
        isinstance(test, dict) and test.get("name") == "Circle MultiCoil phase receipt-slice validation"
        for test in tests
    ):
        errors.append(f"{rel(STRUCTURE)} missing Circle MultiCoil phase receipt-slice Codex test.")
    open_gaps = text_blob(chapter.get("open_evidence_gaps", []))
    require_fragments(
        f"{rel(STRUCTURE)} open_evidence_gaps",
        open_gaps,
        (
            "joint_repeat_horizon=35",
            "relative_phase=3",
            "no MultiCoil phase benchmark",
            "no model-quality",
            "no support-state transition",
        ),
        errors,
    )


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_transition(errors)
    validate_surfaces(errors)

    if errors:
        print("Circle MultiCoil phase receipt slice validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Circle MultiCoil phase receipt slice validation passed: "
        "CC-AI-CONTRACT-PHASE-FEATURE-001 joint_repeat_horizon=35, "
        "relative_phase=3, no support-state promotion."
    )


if __name__ == "__main__":
    main()
