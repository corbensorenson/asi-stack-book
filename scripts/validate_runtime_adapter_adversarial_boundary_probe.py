#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "runtime_adapter_adversarial_boundary" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "runtime_adapter_adversarial_boundary_probe.md"
CHAPTER = ROOT / "chapters" / "runtime-adapters-tool-permissions-and-human-approval.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "runtime-adapters-tool-permissions-and-human-approval.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "RuntimeAdapters.lean"

COMMAND = "python3 scripts/validate_runtime_adapter_adversarial_boundary_probe.py"
PROOF_TAG = "lean:runtime.adapters.adversarial_boundary_probe_bridge"
CODEX_TEST_NAME = "Runtime adapter adversarial boundary probe"
REQUIRED_THEOREMS = [
    "adapter_adversarial_confused_deputy_parent_mismatch_rejected",
    "adapter_adversarial_missing_permission_rejected",
    "adapter_adversarial_parent_authority_ceiling_rejected",
    "adapter_adversarial_lease_authority_ceiling_rejected",
    "adapter_adversarial_scoped_approval_mismatch_rejected",
    "adapter_adversarial_expired_approval_rejected",
    "adapter_adversarial_sandbox_escape_rejected",
    "adapter_adversarial_secret_materialization_rejected",
    "adapter_adversarial_missing_rollback_handle_rejected",
    "adapter_adversarial_missing_effect_receipt_rejected",
    "adapter_adversarial_missing_audit_refs_rejected",
    "adapter_adversarial_support_promotion_rejected",
    "adapter_adversarial_missing_non_claim_boundary_rejected",
    "adapter_adversarial_low_impact_dispatch_accepted",
    "adapter_adversarial_high_impact_dispatch_accepted",
    "runtime_adapter_adversarial_boundary_probe_bridge",
]
REQUIRED_NON_CLAIMS = [
    "does not execute a deployed adapter",
    "does not prove sandbox isolation",
    "does not prove approval-service behavior",
    "does not prove secret-handle safety",
    "does not prove policy-enforcement correctness",
    "does not prove rollback-service behavior",
    "does not create a support-state transition",
]


def base_review(**overrides: Any) -> dict[str, Any]:
    review: dict[str, Any] = {
        "parent_job_id": "job://adapter-boundary/base",
        "approval_parent_job_id": "job://adapter-boundary/base",
        "lease_parent_job_id": "job://adapter-boundary/base",
        "receipt_parent_job_id": "job://adapter-boundary/base",
        "adapter_id": "adapter://bounded-tool",
        "capability": "filesystem.write",
        "parent_permission_present": True,
        "high_impact": False,
        "approval_required": False,
        "approval_recorded": False,
        "approval_scope_matches": True,
        "approval_active": True,
        "lease_capability_matches": True,
        "lease_active": True,
        "lease_sandboxed": True,
        "sandbox_path_within_boundary": True,
        "requested_authority_rank": 1,
        "parent_authority_ceiling": 2,
        "lease_authority_ceiling": 2,
        "secret_materialized_to_model_context": False,
        "rollback_required": True,
        "rollback_handle_recorded": True,
        "effect_receipt_recorded": True,
        "audit_refs_recorded": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
        "external_effect_kind": "synthetic_record_gate_only",
        "expected_route": "dispatch",
    }
    review.update(overrides)
    return review


REVIEWS: list[dict[str, Any]] = [
    base_review(
        scenario_id="valid_scoped_low_impact_dispatch_review",
        expect_valid=True,
        parent_job_id="job://adapter-boundary/low-impact",
        approval_parent_job_id="job://adapter-boundary/low-impact",
        lease_parent_job_id="job://adapter-boundary/low-impact",
        receipt_parent_job_id="job://adapter-boundary/low-impact",
    ),
    base_review(
        scenario_id="valid_high_impact_scoped_approval_review",
        expect_valid=True,
        parent_job_id="job://adapter-boundary/high-impact",
        approval_parent_job_id="job://adapter-boundary/high-impact",
        lease_parent_job_id="job://adapter-boundary/high-impact",
        receipt_parent_job_id="job://adapter-boundary/high-impact",
        high_impact=True,
        approval_required=True,
        approval_recorded=True,
        approval_scope_matches=True,
        approval_active=True,
        requested_authority_rank=2,
        parent_authority_ceiling=2,
        lease_authority_ceiling=2,
    ),
    base_review(
        scenario_id="invalid_confused_deputy_parent_mismatch",
        expect_valid=False,
        approval_parent_job_id="job://adapter-boundary/different-caller",
        expected_route="deny_confused_deputy",
    ),
    base_review(
        scenario_id="invalid_parent_authority_ceiling_overrun",
        expect_valid=False,
        requested_authority_rank=3,
        parent_authority_ceiling=2,
        lease_authority_ceiling=3,
        expected_route="deny_authority_escalation",
    ),
    base_review(
        scenario_id="invalid_lease_authority_ceiling_overrun",
        expect_valid=False,
        requested_authority_rank=3,
        parent_authority_ceiling=3,
        lease_authority_ceiling=2,
        expected_route="deny_authority_escalation",
    ),
    base_review(
        scenario_id="invalid_approval_scope_mismatch",
        expect_valid=False,
        high_impact=True,
        approval_required=True,
        approval_recorded=True,
        approval_scope_matches=False,
        expected_route="request_scoped_approval",
    ),
    base_review(
        scenario_id="invalid_expired_approval",
        expect_valid=False,
        high_impact=True,
        approval_required=True,
        approval_recorded=True,
        approval_scope_matches=True,
        approval_active=False,
        expected_route="deny_expired_approval",
    ),
    base_review(
        scenario_id="invalid_sandbox_escape_path",
        expect_valid=False,
        sandbox_path_within_boundary=False,
        expected_route="deny_sandbox_escape",
    ),
    base_review(
        scenario_id="invalid_secret_materialized_to_model_context",
        expect_valid=False,
        secret_materialized_to_model_context=True,
        expected_route="deny_secret_exposure",
    ),
    base_review(
        scenario_id="invalid_missing_rollback_handle",
        expect_valid=False,
        high_impact=True,
        approval_required=True,
        approval_recorded=True,
        rollback_required=True,
        rollback_handle_recorded=False,
        expected_route="request_rollback_handle",
    ),
    base_review(
        scenario_id="invalid_missing_effect_receipt",
        expect_valid=False,
        effect_receipt_recorded=False,
        expected_route="request_effect_receipt",
    ),
    base_review(
        scenario_id="invalid_missing_audit_refs",
        expect_valid=False,
        audit_refs_recorded=False,
        expected_route="request_effect_receipt",
    ),
    base_review(
        scenario_id="invalid_support_state_promotion",
        expect_valid=False,
        support_state_effect="promote_chapter_core",
        expected_route="preserve_no_promotion_boundary",
    ),
    base_review(
        scenario_id="invalid_missing_non_claim_boundary",
        expect_valid=False,
        non_claims=[],
        expected_route="request_non_claim_boundary",
    ),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Runtime adapter adversarial boundary probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def route_for(review: dict[str, Any]) -> str:
    if (
        review["approval_parent_job_id"] != review["parent_job_id"]
        or review["lease_parent_job_id"] != review["parent_job_id"]
        or review["receipt_parent_job_id"] != review["parent_job_id"]
    ):
        return "deny_confused_deputy"
    if review["parent_permission_present"] is not True:
        return "deny_missing_permission"
    if (review["approval_required"] is True or review["high_impact"] is True) and (
        review["approval_recorded"] is not True or review["approval_scope_matches"] is not True
    ):
        return "request_scoped_approval"
    if review["approval_required"] is True and review["approval_active"] is not True:
        return "deny_expired_approval"
    if review["lease_capability_matches"] is not True:
        return "deny_mismatched_lease"
    if review["lease_active"] is not True:
        return "deny_expired_lease"
    if review["requested_authority_rank"] > review["parent_authority_ceiling"]:
        return "deny_authority_escalation"
    if review["requested_authority_rank"] > review["lease_authority_ceiling"]:
        return "deny_authority_escalation"
    if review["lease_sandboxed"] is not True or review["sandbox_path_within_boundary"] is not True:
        return "deny_sandbox_escape"
    if review["secret_materialized_to_model_context"] is True:
        return "deny_secret_exposure"
    if review["rollback_required"] is True and review["rollback_handle_recorded"] is not True:
        return "request_rollback_handle"
    if review["effect_receipt_recorded"] is not True or review["audit_refs_recorded"] is not True:
        return "request_effect_receipt"
    if review["support_state_effect"] != "none":
        return "preserve_no_promotion_boundary"
    if not review["non_claims"]:
        return "request_non_claim_boundary"
    return "dispatch"


def review_errors(review: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scenario_id = str(review.get("scenario_id", "<missing>"))
    for field, prefix in (
        ("parent_job_id", "job://"),
        ("approval_parent_job_id", "job://"),
        ("lease_parent_job_id", "job://"),
        ("receipt_parent_job_id", "job://"),
        ("adapter_id", "adapter://"),
    ):
        if not isinstance(review.get(field), str) or not review[field].startswith(prefix):
            errors.append(f"{scenario_id}: {field} must use {prefix}.")
    if not isinstance(review.get("capability"), str) or not review["capability"].strip():
        errors.append(f"{scenario_id}: capability must be non-empty.")
    for field in ("requested_authority_rank", "parent_authority_ceiling", "lease_authority_ceiling"):
        if not isinstance(review.get(field), int) or review[field] < 0:
            errors.append(f"{scenario_id}: {field} must be a non-negative integer.")

    actual_route = route_for(review)
    if actual_route != review.get("expected_route"):
        errors.append(f"{scenario_id}: expected_route {review.get('expected_route')!r} but route was {actual_route!r}.")
    if actual_route != "dispatch":
        errors.append(f"{scenario_id}: boundary review did not dispatch; route={actual_route}.")

    if review["approval_parent_job_id"] != review["parent_job_id"]:
        errors.append(f"{scenario_id}: approval parent does not match caller parent job.")
    if review["lease_parent_job_id"] != review["parent_job_id"]:
        errors.append(f"{scenario_id}: effect lease parent does not match caller parent job.")
    if review["receipt_parent_job_id"] != review["parent_job_id"]:
        errors.append(f"{scenario_id}: effect receipt parent does not match caller parent job.")
    if review["parent_permission_present"] is not True:
        errors.append(f"{scenario_id}: parent permission is missing.")
    if review["requested_authority_rank"] > review["parent_authority_ceiling"]:
        errors.append(f"{scenario_id}: requested authority exceeds parent ceiling.")
    if review["requested_authority_rank"] > review["lease_authority_ceiling"]:
        errors.append(f"{scenario_id}: requested authority exceeds lease ceiling.")
    if (review["approval_required"] is True or review["high_impact"] is True) and review["approval_recorded"] is not True:
        errors.append(f"{scenario_id}: high-impact or approval-required invocation lacks approval.")
    if (review["approval_required"] is True or review["high_impact"] is True) and review["approval_scope_matches"] is not True:
        errors.append(f"{scenario_id}: approval scope does not match the requested effect.")
    if review["approval_required"] is True and review["approval_active"] is not True:
        errors.append(f"{scenario_id}: approval is expired or inactive.")
    if review["lease_capability_matches"] is not True:
        errors.append(f"{scenario_id}: effect lease does not match requested capability.")
    if review["lease_active"] is not True:
        errors.append(f"{scenario_id}: effect lease is inactive.")
    if review["lease_sandboxed"] is not True or review["sandbox_path_within_boundary"] is not True:
        errors.append(f"{scenario_id}: sandbox boundary is not satisfied.")
    if review["secret_materialized_to_model_context"] is True:
        errors.append(f"{scenario_id}: secret handle was materialized into model-visible context.")
    if review["rollback_required"] is True and review["rollback_handle_recorded"] is not True:
        errors.append(f"{scenario_id}: rollback-required invocation lacks rollback handle.")
    if review["effect_receipt_recorded"] is not True:
        errors.append(f"{scenario_id}: effect receipt is missing.")
    if review["audit_refs_recorded"] is not True:
        errors.append(f"{scenario_id}: audit refs are missing.")
    if review["support_state_effect"] != "none":
        errors.append(f"{scenario_id}: support_state_effect must remain none.")

    non_claim_text = text_blob(review.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{scenario_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.runtime_adapter_adversarial_boundary_probe.v0",
        "result_id": "2026-07-02-runtime-adapter-adversarial-boundary-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_runtime_adapter_adversarial_boundary_probe",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(REVIEWS),
        "negative_controls": {
            "confused_deputy_parent_mismatch_rejected": True,
            "parent_authority_ceiling_overrun_rejected": True,
            "lease_authority_ceiling_overrun_rejected": True,
            "approval_scope_mismatch_rejected": True,
            "expired_approval_rejected": True,
            "sandbox_escape_path_rejected": True,
            "secret_materialization_rejected": True,
            "missing_rollback_handle_rejected": True,
            "missing_effect_receipt_rejected": True,
            "missing_audit_refs_rejected": True,
            "support_state_promotion_rejected": True,
            "missing_non_claim_boundary_rejected": True,
        },
        "boundary_coverage": {
            "low_impact_dispatch_admitted": True,
            "high_impact_scoped_approval_admitted": True,
            "caller_parentage_required": True,
            "parent_and_lease_authority_ceilings_checked": True,
            "approval_scope_and_expiry_checked": True,
            "sandbox_path_boundary_checked": True,
            "secret_handle_non_materialization_checked": True,
            "rollback_receipt_audit_records_required": True,
            "support_state_no_promotion_checked": True,
            "non_claim_boundary_checked": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.RuntimeAdapters",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "lowImpactDispatchAccepted": True,
                "highImpactDispatchAccepted": True,
                "negativeControlsRejected": True,
                "authorityAndApprovalBoundaries": True,
                "secretAndSandboxBoundaries": True,
                "supportStateEffectNone": True,
                "nonClaimBoundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic runtime-adapter adversarial boundary fixture only; no deployed adapter, production sandbox, approval service, secret broker, policy engine, rollback service, revocation service, or security audit was executed.",
            "The Runtime Adapters chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
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


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "runtime-adapters-tool-permissions-and-human-approval":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Runtime Adapters chapter.")
        return
    if CODEX_TEST_NAME.lower() not in text_blob(chapter.get("codex_tests", [])):
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "lowImpactDispatchAccepted",
        "highImpactDispatchAccepted",
        "negativeControlsRejected",
        "authorityAndApprovalBoundaries",
        "secretAndSandboxBoundaries",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Runtime Adapter Adversarial Boundary Probe",
            rel(RESULT),
            "two valid synthetic adapter boundary reviews",
            "twelve expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Runtime adapter adversarial boundary probe",
            rel(RESULT),
            "two valid synthetic adapter boundary reviews",
            "twelve expected-invalid controls",
        ],
        READER: [
            "Runtime adapter adversarial boundary probe",
            "two synthetic adapter boundary reviews",
            "not deployed adapter execution",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Runtime adapter adversarial boundary probe",
            "deterministic synthetic runtime-adapter adversarial boundary fixture",
            "no support-state promotion",
        ],
        CHANGELOG: ["Runtime adapter adversarial boundary probe", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_runtime_adapter_adversarial_boundary_probe.py",
            "docs/runtime_adapter_adversarial_boundary_probe.md",
            "experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json",
            'run_validator("validate_runtime_adapter_adversarial_boundary_probe.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required runtime-adapter adversarial surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for review in REVIEWS:
        expect_valid = bool(review.get("expect_valid"))
        current_errors = review_errors(review)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{review.get('scenario_id', '<missing>')}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic adapter boundary reviews.")
    if invalid_count != 12:
        errors.append("Expected exactly twelve expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Runtime adapter adversarial boundary probe validation passed.")


if __name__ == "__main__":
    main()
