#!/usr/bin/env python3
"""Validate the public-safe Circle sparse-attention receipt slice.

This is a structural evidence-surface check. It keeps the Coil chapter concrete
about Circle sparse-attention gap and repair/fallback receipt facts without
allowing those facts to turn into coverage-success, deployed attention,
retrieval-quality, long-context, performance, or support-state claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_sparse_attention_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_sparse_attention_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_sparse_attention_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_sparse_attention_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

EXPECTED = {
    "result_id": "2026-07-05-local-circle-sparse-attention-receipt-slice",
    "slice_id": "circle_sparse_attention_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-SPARSE-001",
    "kind": "sparse_attention_coverage",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "c23809cef9b821b1e4f9cabf53fcac724a0757bf3f86594e1d12710fe0cd9ec1",
    "pytest_summary": "10 passed in 1.87s",
    "transition_id": "v1_x_measured.circle_sparse_attention_receipt.no_change",
    "claim_id": "circle-calculus.sparse_attention_receipt_slice",
}

THEOREMS = ("AIT-T0104", "AIT-T0172")
RECOMMENDATIONS = (
    "SPARSE-LOCAL-FIRST-INTERVAL-REPAIR",
    "SPARSE-DENSE-LOCAL-COMPLETE-FALLBACK",
)
OUTPUT_HASHES = {
    "3521b057c86435df7896d636c98d8981e8bd8550c3ec9ac39d782748c72bd4be": 11664,
    "8b3d6787cc13c84a9cdcd9d8312f185acdf126bb110f49ae9c1c194c025bd1e7": 35487,
    "3022d3631af609f518accbc8998e9f471f1c8b0929fbc754656215359682d210": 4664,
    "668b395f8850be6993a6be32ec7b83326e8056bbdb7d2d55599104a176e871a1": 11385,
    "bccd01af074f2766287e392495d35e1977aaa5cf050e80710d26a61ef606757f": 99,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove sparse-attention coverage success",
    "does not prove deployed sparse-attention behavior",
    "retrieval quality",
    "long-context",
    "model quality",
    "speed",
    "memory savings",
    "deployment safety",
    "transfer",
    "ASI",
)
SURFACE_FRAGMENTS = (
    EXPECTED["git_commit"],
    EXPECTED["contract_id"],
    EXPECTED["kind"],
    EXPECTED["contract_content_fingerprint"],
    "coverage_complete=false",
    "first_uncovered_lag=5",
    "uncovered_lag_count=109",
    "covered_lag_count=10",
    "complete_repair_window=119",
    "complete_repair_window_additional_local_slots=115",
    "complete_repair_window_minimal_for_declared_stride_family=true",
    "complete_repair_window_minimal_witness_lag=119",
    "interval_repair_plan_step_count=6",
    "lag_collision_pair_count=0",
    "query_collision_pair_count=0",
    "theorem_count=141",
    EXPECTED["pytest_summary"],
    "circle_sparse_attention_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "sparse-attention receipt",
    "coverage was incomplete",
    "first missed lag",
    "complete repair window",
    "dense-local fallback",
    "sparse-attention coverage contract",
    "two theorem IDs",
    "receipt fingerprint",
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
    for key in ("result_id", "slice_id"):
        if result.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} {key} must be {EXPECTED[key]!r}.")

    project = result.get("external_project", {})
    if not isinstance(project, dict) or project.get("git_commit") != EXPECTED["git_commit"]:
        errors.append(f"{rel(RESULT)} must record Circle commit {EXPECTED['git_commit']}.")
    if project.get("worktree_state") != "clean_before_commands":
        errors.append(f"{rel(RESULT)} must record the clean external worktree boundary.")

    fixture = result.get("sparse_fixture", {})
    expected_fixture = {
        "sequence_length": 120,
        "strides": [7, 13],
        "path_length": 3,
        "local_window": 4,
        "candidate_budget_per_query": 10,
        "full_attention_budget": 120,
        "coverage_complete": False,
        "coverage_ratio": 0.08403361344537816,
        "covered_lag_count": 10,
        "uncovered_lag_count": 109,
        "covered_lags": [1, 2, 3, 4, 7, 14, 21, 13, 26, 39],
        "uncovered_lag_intervals": [[5, 6], [8, 12], [15, 20], [22, 25], [27, 38], [40, 119]],
        "first_uncovered_lag": 5,
        "first_uncovered_interval_start": 5,
        "first_uncovered_interval_stop": 6,
        "first_uncovered_interval_length": 2,
        "first_uncovered_interval_additional_local_slots": 2,
        "first_uncovered_interval_repair_reaches_interval": True,
        "first_interval_repair_next_uncovered_lag": 8,
        "first_interval_repair_still_has_gap": True,
        "complete_repair_window": 119,
        "complete_repair_window_additional_local_slots": 115,
        "complete_repair_window_covers_context": True,
        "complete_repair_window_uses_dense_threshold": True,
        "complete_repair_window_minimal_for_declared_stride_family": True,
        "complete_repair_window_minimal_witness_lag": 119,
        "local_window_complete_threshold_is_exact_local_minimum": True,
        "interval_repair_plan": [[5, 6, 6, 2, 107], [8, 12, 12, 6, 102], [15, 20, 20, 8, 96], [22, 25, 25, 5, 92], [27, 38, 38, 13, 80], [40, 119, 119, 81, 0]],
        "interval_repair_plan_step_count": 6,
        "interval_repair_plan_final_window": 119,
        "interval_repair_plan_covers_context": True,
        "interval_repair_plan_strictly_progresses": True,
        "lag_collision_pair_count": 0,
        "query_collision_pair_count": 0,
        "lag_collision_pair_count_zero_iff_no_collision": True,
        "query_collision_pair_count_zero_iff_no_collision": True,
        "raw_budget_shortfall_certifies_incomplete": True,
        "contract_ready_theorem_count": 141,
        "circle_ai_receipt_theorem_count": 132,
    }
    if fixture != expected_fixture:
        errors.append(f"{rel(RESULT)} sparse_fixture drifted from the recorded Circle sparse-attention facts.")

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

    expected_fields = {
        "complete_repair_window": 119,
        "complete_repair_window_covers_context": True,
        "complete_repair_window_minimal_for_declared_stride_family": True,
        "complete_repair_window_minimal_witness_lag": 119,
        "first_uncovered_interval_start": 5,
        "first_uncovered_lag": 5,
    }
    if receipt.get("evidence_fields") != expected_fields:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded sparse receipt facts.")

    recommendations = receipt.get("planner_recommendations", [])
    if not isinstance(recommendations, list) or len(recommendations) != 2:
        errors.append(f"{rel(RESULT)} planner_recommendations must record exactly two selected recommendations.")
    else:
        ids = [rec.get("id") for rec in recommendations if isinstance(rec, dict)]
        if tuple(ids) != RECOMMENDATIONS:
            errors.append(f"{rel(RESULT)} planner_recommendations must remain {RECOMMENDATIONS}.")
        require_fragments(
            rel(RESULT),
            text_blob(recommendations),
            (
                "first reported gap interval only",
                "not a performance recommendation",
                "not a claim that dense local attention is efficient",
            ),
            errors,
        )

    boundary = result.get("circle_ai_certifier_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("request_passed") is not False:
        errors.append(f"{rel(RESULT)} must preserve request_passed=false for the sparse coverage boundary.")
    require_fragments(rel(RESULT), text_blob(boundary), ("does not cover all positive lags", "not a coverage-success claim"), errors)

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 5:
        errors.append(f"{rel(RESULT)} must record exactly five successful commands.")
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
            "PYTHONPATH=. python3 scripts/stride_family_certify.py --context 120 --strides 7,13 --path-length 3 --local-window 4 --format json",
            "ready=True fields=14 missing=0 theorems=141",
            "strict sparse-attention acceptance receipt accepted",
            EXPECTED["pytest_summary"],
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
    for path in (str(SUMMARY.relative_to(ROOT)), str(RESULT.relative_to(ROOT)), "scripts/validate_circle_sparse_attention_receipt_slice.py"):
        if path not in text_blob(transition):
            errors.append(f"{rel(TRANSITION)} missing artifact ref {path!r}.")
    require_fragments(rel(TRANSITION), text_blob(transition), NON_CLAIMS, errors)
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            "coverage_complete=false",
            "fresh public Circle replay",
            "ordinary full-attention and sparse-attention baselines",
            "does not create an upward support-state transition",
            "does not promote the Coil Attention chapter core claim",
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
    chapter = chapter_record(structure, "coil-attention-cyclic-memory-and-recurrence-contracts")
    if not chapter:
        errors.append(f"{rel(STRUCTURE)} missing Coil chapter record.")
        return
    tests = chapter.get("codex_tests", [])
    if not isinstance(tests, list) or not any(
        isinstance(test, dict) and test.get("name") == "Circle sparse-attention receipt-slice validation"
        for test in tests
    ):
        errors.append(f"{rel(STRUCTURE)} missing Circle sparse-attention receipt-slice Codex test.")
    open_gaps = text_blob(chapter.get("open_evidence_gaps", []))
    require_fragments(
        f"{rel(STRUCTURE)} open_evidence_gaps",
        open_gaps,
        (
            "coverage_complete=false",
            "no deployed sparse-attention behavior",
            "no retrieval quality",
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
        print("Circle sparse-attention receipt slice validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Circle sparse-attention receipt slice validation passed: "
        "CC-AI-CONTRACT-SPARSE-001 coverage_complete=false, first gap 5, "
        "complete repair window 119, no support-state promotion."
    )


if __name__ == "__main__":
    main()
