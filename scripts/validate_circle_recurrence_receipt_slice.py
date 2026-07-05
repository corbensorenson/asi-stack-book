#!/usr/bin/env python3
"""Validate the public-safe Circle recurrence receipt slice.

This is a structural evidence-surface check. It keeps the Coil chapter concrete
about Circle recurrence-schedule receipt facts without allowing those facts to
turn into deployed recurrence, reasoning-quality, long-context, memory-quality,
or support-state claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_recurrence_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_recurrence_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_recurrence_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_recurrence_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

EXPECTED = {
    "result_id": "2026-07-05-local-circle-recurrence-receipt-slice",
    "slice_id": "circle_recurrence_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-RECURRENCE-001",
    "kind": "recurrence_schedule",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "571edd5dce4f7b64441806de323295218a3e2293b3b540dd4772ba34b9371515",
    "pytest_summary": "2 passed in 2.37s",
    "transition_id": "v1_x_measured.circle_recurrence_receipt.no_change",
    "claim_id": "circle-calculus.recurrence_schedule_receipt_slice",
}

THEOREMS = ("AIM-T0026", "AIM-T0130", "AIM-T0159")
RECOMMENDATIONS = (
    "RECURRENCE-USE-ACTIVE-TOKEN-WORK-SCHEDULE",
    "RECURRENCE-REUSE-WHOLE-PERIOD-SHIFT",
)
OUTPUT_HASHES = {
    "18dec9b030fdae61838ae778c9f22b39f318d7449611244f4e745e7e1d77d9ad": 38845,
    "2a4a40151f7c4ac900bcfcbb3a1f42fe68020c8eae269a523f971af5b794318d": 58239,
    "cbb84e6e0fcd374895ed998307380917849d30a1268c211dfa4e43bac1357689": 4060,
    "5b1d20752090cda0e4c2d0cf43b22c6832b46db6ae910f98fa3f18a4d47f32fa": 12285,
    "4ebae0342e485c764b9428f69b6f0535e7506cc353926f4c51e028fd1052d0d3": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove deployed recurrence behavior",
    "reasoning quality",
    "retrieval quality",
    "learned-memory behavior",
    "convergence",
    "model quality",
    "context length",
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
    "active_token_count_trace=[8, 6, 4, 2, 1]",
    "inactive_token_count_trace=[0, 2, 4, 6, 7]",
    "total_active_token_work=21",
    "total_inactive_token_work=19",
    "scheduled_work_saving=19",
    "post_period_multi_extension_scheduled_work_saving=43",
    "periodic_shift_required_steps_invariant=true",
    "periodic_shift_active_at_step_invariant=true",
    "theorem_count=64",
    EXPECTED["pytest_summary"],
    "circle_recurrence_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "recurrence receipt",
    "active token work",
    "scheduled work",
    "whole-period shift",
    EXPECTED["contract_id"],
    EXPECTED["contract_content_fingerprint"],
    EXPECTED["pytest_summary"],
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

    fixture = result.get("recurrence_fixture", {})
    expected_fixture = {
        "loop_period": 5,
        "sample_index": 8,
        "max_loops": 7,
        "required_steps": 4,
        "exit_step": 4,
        "overthinking_boundary": 5,
        "total_work_horizon_steps": 5,
        "active_token_count_trace": [8, 6, 4, 2, 1],
        "inactive_token_count_trace": [0, 2, 4, 6, 7],
        "active_token_count_trace_sum": 21,
        "inactive_token_count_trace_sum": 19,
        "active_token_count_trace_sum_matches_total": True,
        "inactive_token_count_trace_sum_matches_total": True,
        "first_inactive_steps_match_budget_successor": True,
        "total_active_token_work": 21,
        "total_inactive_token_work": 19,
        "full_loop_token_work": 40,
        "scheduled_work_saving": 19,
        "scheduled_work_saving_accounting": True,
        "active_inactive_work_accounting": True,
        "scheduled_work_saving_matches_inactive_work": True,
        "scheduled_work_saving_positive": True,
        "active_work_below_full_loop_work": True,
        "post_period_extension_horizon_steps": 6,
        "post_period_extension_total_active_token_work": 21,
        "post_period_extension_total_inactive_token_work": 27,
        "post_period_extension_full_loop_token_work": 48,
        "post_period_extension_scheduled_work_saving": 27,
        "post_period_extension_active_work_unchanged": True,
        "post_period_extension_saving_added_token_count": True,
        "post_period_extra_steps": 3,
        "post_period_multi_extension_horizon_steps": 8,
        "post_period_multi_extension_total_active_token_work": 21,
        "post_period_multi_extension_total_inactive_token_work": 43,
        "post_period_multi_extension_full_loop_token_work": 64,
        "post_period_multi_extension_scheduled_work_saving": 43,
        "post_period_multi_extension_active_work_unchanged": True,
        "post_period_multi_extension_saving_added_extra_token_count": True,
        "periodic_shift_base_token": 7,
        "periodic_shift_passes": 3,
        "periodic_shift_amount": 15,
        "periodic_shifted_token": 22,
        "periodic_shift_required_steps_invariant": True,
        "periodic_shift_recurrence_budget_invariant": True,
        "periodic_shift_training_free_budget_invariant": True,
        "periodic_shift_exit_step_invariant": True,
        "periodic_shift_overthinking_boundary_invariant": True,
        "periodic_shift_active_step": 2,
        "periodic_shift_active_at_step_invariant": True,
    }
    if fixture != expected_fixture:
        errors.append(f"{rel(RESULT)} recurrence_fixture drifted from the recorded Circle recurrence facts.")

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
    if receipt.get("theorem_count") != 64:
        errors.append(f"{rel(RESULT)} theorem_count must remain 64.")

    expected_fields = {
        "active_inactive_work_accounting": True,
        "periodic_shift_active_at_step_invariant": True,
        "periodic_shift_required_steps_invariant": True,
        "post_period_multi_extension_scheduled_work_saving": 43,
        "scheduled_work_saving": 19,
        "scheduled_work_saving_accounting": True,
        "scheduled_work_saving_positive": True,
        "total_active_token_work": 21,
    }
    if receipt.get("evidence_fields") != expected_fields:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded Circle recurrence receipt facts.")

    recommendations = receipt.get("planner_recommendations", [])
    if not isinstance(recommendations, list) or len(recommendations) != 2:
        errors.append(f"{rel(RESULT)} planner_recommendations must record exactly two recommendations.")
    else:
        ids = [rec.get("recommendation_id") for rec in recommendations if isinstance(rec, dict)]
        if tuple(ids) != RECOMMENDATIONS:
            errors.append(f"{rel(RESULT)} planner_recommendations must remain {RECOMMENDATIONS}.")
        require_fragments(rel(RESULT), text_blob(recommendations), ("not a runtime", "real looped transformer reasons better"), errors)

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
            "PYTHONPATH=. python3 scripts/recurrence_schedule_certify.py --loop-period 5",
            "ready=True fields=8 missing=0 theorems=64",
            "accepted true",
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
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            EXPECTED["contract_id"],
            EXPECTED["contract_content_fingerprint"],
            "does not create an upward support-state transition",
            "chapter core",
            "above argument",
            "deployed recurrence behavior",
            "reasoning quality",
            "long-context",
        ),
        errors,
    )


def validate_public_surfaces(errors: list[str]) -> None:
    for path in (README, SUMMARY, TRANSITION, LEDGER, STRUCTURE, OUTLINE, CHAPTER, READER, ROADMAP, APPENDIX_E):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        return

    for path in (SUMMARY, CHAPTER, OUTLINE, ROADMAP, APPENDIX_E, LEDGER):
        text = path.read_text(encoding="utf-8")
        require_fragments(rel(path), text, SURFACE_FRAGMENTS, errors)
    require_fragments(rel(READER), READER.read_text(encoding="utf-8"), READER_FRAGMENTS, errors)

    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
        return
    chapter = chapter_record(structure, "coil-attention-cyclic-memory-and-recurrence-contracts")
    if chapter.get("evidence_level") != "argument":
        errors.append("Coil chapter evidence_level must remain argument.")
    tests = text_blob(chapter.get("codex_tests", []))
    if "Circle recurrence receipt-slice validation" not in tests:
        errors.append("Coil chapter manifest is missing the Circle recurrence receipt-slice test row.")
    if "no deployed recurrence behavior, reasoning-quality, retrieval-quality, learned-memory behavior, convergence, long-context, model-quality, deployment, transfer, ASI, or support-state-transition claim" not in tests:
        errors.append("Coil chapter manifest test row must preserve recurrence non-claim boundary.")


def fail(errors: list[str]) -> None:
    print("Circle recurrence receipt-slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_transition(errors)
    validate_public_surfaces(errors)
    if errors:
        fail(errors)
    print("Circle recurrence receipt-slice validation passed.")


if __name__ == "__main__":
    main()
