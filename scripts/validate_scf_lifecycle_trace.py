#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "experiments" / "scf_lifecycle_trace" / "results" / "2026-07-02-local.json"
LEAN_PATH = ROOT / "lean" / "AsiStackProofs" / "StableCapabilityFields.lean"

STATES = {"shadow", "canary", "qualified", "default", "deprecated", "retired", "quarantined"}
FORWARD_STEPS = {
    ("shadow", "canary"),
    ("canary", "qualified"),
    ("qualified", "default"),
    ("default", "deprecated"),
    ("deprecated", "retired"),
}
REQUIRED_NONCLAIMS = [
    "does not execute deployed route validation",
    "does not prove evaluator-integrity measurement",
    "does not execute rollback",
    "does not promote the chapter support state",
]
EXPECTED_THEOREMS = {
    "authority_expanding_replacement_without_grant_rejected",
    "field_identity_mismatch_rejects_replacement",
    "stale_qualification_lease_requires_requalification",
    "missing_evidence_requires_requalification",
    "captured_evaluator_routes_to_governance_review",
    "authority_expansion_without_grant_routes_to_governance_review",
    "open_incident_requires_rollback",
    "complete_default_review_routes_to_default",
    "retired_state_cannot_transition",
    "default_transition_requires_full_readiness",
    "default_without_qualification_evidence_rejected",
    "default_without_regression_floor_rejected",
    "default_authority_expansion_rejected",
    "default_without_rollback_rejected",
    "default_with_open_incident_rejected",
    "apply_lifecycle_event_preserves_exact_identity",
    "apply_lifecycle_event_cannot_assign_support_or_external_effect",
    "accepted_lifecycle_event_advances_and_records_receipt",
    "rejected_lifecycle_event_preserves_exact_state",
    "run_lifecycle_events_preserve_exact_identity",
    "run_lifecycle_events_cannot_assign_support_or_external_effect",
    "run_lifecycle_events_compose",
    "terminal_lifecycle_event_is_rejected",
    "terminal_lifecycle_state_is_absorbing",
    "complete_scf_lifecycle_trace_reaches_exact_retired_state",
    "incident_trace_reaches_exact_absorbing_quarantine_state",
}

TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_scf_forward_lifecycle",
        "expect_valid": True,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "shadow",
                "to": "canary",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": False,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-forward-shadow-canary",
            },
            {
                "from": "canary",
                "to": "qualified",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-forward-canary-qualified",
            },
            {
                "from": "qualified",
                "to": "default",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-forward-qualified-default",
            },
            {
                "from": "default",
                "to": "deprecated",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": True,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-forward-default-deprecated",
            },
            {
                "from": "deprecated",
                "to": "retired",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": True,
                "retirement_receipt_present": True,
                "receipt": "receipt://scf-forward-deprecated-retired",
            },
        ],
        "non_claims": REQUIRED_NONCLAIMS + [
            "does not prove real regression preservation",
        ],
    },
    {
        "trace_id": "valid_scf_incident_quarantine",
        "expect_valid": True,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "canary",
                "to": "quarantined",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": False,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": True,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-incident-canary-quarantine",
                "residual_owner": "owner://scf-review-board",
            },
        ],
        "non_claims": REQUIRED_NONCLAIMS + [
            "does not prove monitor quality",
        ],
    },
    {
        "trace_id": "invalid_identity_drift",
        "expect_valid": False,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "shadow",
                "to": "canary",
                "field_identity_preserved": False,
                "qualification_evidence_present": True,
                "regression_floor_preserved": False,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-invalid-identity-drift",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_default_without_regression_floor",
        "expect_valid": False,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "qualified",
                "to": "default",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": False,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-invalid-default-regression",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_default_authority_expansion",
        "expect_valid": False,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "qualified",
                "to": "default",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": False,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-invalid-default-authority",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_retired_restart",
        "expect_valid": False,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "retired",
                "to": "canary",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": True,
                "retirement_receipt_present": True,
                "receipt": "receipt://scf-invalid-retired-restart",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_deprecation_without_notice",
        "expect_valid": False,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "default",
                "to": "deprecated",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": False,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-invalid-deprecation-notice",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_retirement_without_receipt",
        "expect_valid": False,
        "field_id": "field://public-book-route-selector",
        "support_state_effect": "none",
        "transitions": [
            {
                "from": "deprecated",
                "to": "retired",
                "field_identity_preserved": True,
                "qualification_evidence_present": True,
                "regression_floor_preserved": True,
                "authority_within_ceiling": True,
                "rollback_ready": True,
                "incident_open": False,
                "deprecation_notice_present": True,
                "retirement_receipt_present": False,
                "receipt": "receipt://scf-invalid-retirement-receipt",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
]


def transition_errors(trace_id: str, transition: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    prefix = f"{trace_id}:transitions[{index}]"
    from_state = transition.get("from")
    to_state = transition.get("to")

    if from_state not in STATES:
        errors.append(f"{prefix}: from must be one of {sorted(STATES)}.")
    if to_state not in STATES:
        errors.append(f"{prefix}: to must be one of {sorted(STATES)}.")
    if from_state not in STATES or to_state not in STATES:
        return errors

    if transition.get("field_identity_preserved") is not True:
        errors.append(f"{prefix}: field identity must be preserved.")
    if from_state == "retired":
        errors.append(f"{prefix}: retired state cannot transition.")

    forward = (from_state, to_state) in FORWARD_STEPS
    quarantine = transition.get("incident_open") is True and to_state == "quarantined"
    if not forward and not quarantine:
        errors.append(f"{prefix}: transition must be a forward lifecycle step or incident quarantine.")

    if to_state == "canary":
        if transition.get("qualification_evidence_present") is not True:
            errors.append(f"{prefix}: canary transition requires qualification evidence.")
        if transition.get("rollback_ready") is not True:
            errors.append(f"{prefix}: canary transition requires rollback readiness.")
    if to_state == "qualified":
        if transition.get("qualification_evidence_present") is not True:
            errors.append(f"{prefix}: qualified transition requires qualification evidence.")
        if transition.get("regression_floor_preserved") is not True:
            errors.append(f"{prefix}: qualified transition requires regression-floor preservation.")
    if to_state == "default":
        for field in (
            "qualification_evidence_present",
            "regression_floor_preserved",
            "authority_within_ceiling",
            "rollback_ready",
        ):
            if transition.get(field) is not True:
                errors.append(f"{prefix}: default transition requires {field}.")
        if transition.get("incident_open") is True:
            errors.append(f"{prefix}: default transition requires closed incidents.")
    if to_state == "deprecated" and transition.get("deprecation_notice_present") is not True:
        errors.append(f"{prefix}: deprecated transition requires deprecation notice.")
    if to_state == "retired" and transition.get("retirement_receipt_present") is not True:
        errors.append(f"{prefix}: retired transition requires retirement receipt.")
    if to_state == "quarantined" and not transition.get("residual_owner"):
        errors.append(f"{prefix}: quarantine transition requires residual owner.")

    receipt = transition.get("receipt")
    if not isinstance(receipt, str) or not receipt.startswith("receipt://"):
        errors.append(f"{prefix}: transition receipt must use receipt://.")

    return errors


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    if not str(trace.get("field_id", "")).startswith("field://"):
        errors.append(f"{trace_id}: field_id must use field://.")
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must be none.")

    transitions = trace.get("transitions")
    if not isinstance(transitions, list) or not transitions:
        errors.append(f"{trace_id}: transitions must be a non-empty list.")
    else:
        previous_to: str | None = None
        for index, transition in enumerate(transitions):
            if not isinstance(transition, dict):
                errors.append(f"{trace_id}:transitions[{index}] must be an object.")
            else:
                if previous_to is not None and transition.get("from") != previous_to:
                    errors.append(
                        f"{trace_id}:transitions[{index}] must begin at prior state {previous_to}."
                    )
                errors.extend(transition_errors(trace_id, transition, index))
                previous_to = transition.get("to")

    non_claim_text = " ".join(str(item).lower() for item in trace.get("non_claims", []))
    for marker in REQUIRED_NONCLAIMS:
        if marker not in non_claim_text:
            errors.append(f"{trace_id}: non_claims must include {marker!r}.")

    return errors


def validate_formal_surface(errors: list[str]) -> dict[str, Any]:
    lean_text = LEAN_PATH.read_text(encoding="utf-8")
    theorem_names = set(
        re.findall(r"(?m)^theorem\s+([A-Za-z][A-Za-z0-9_]*)", lean_text)
    )
    if theorem_names != EXPECTED_THEOREMS:
        missing = sorted(EXPECTED_THEOREMS - theorem_names)
        extra = sorted(theorem_names - EXPECTED_THEOREMS)
        errors.append(f"Lean theorem surface drifted; missing={missing}, extra={extra}.")

    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/StableCapabilityFields.lean"],
        cwd=ROOT / "lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        errors.append(f"Lean module failed to compile:\n{completed.stdout}")
    return {
        "theorem_count": len(theorem_names),
        "lean_module": str(LEAN_PATH.relative_to(ROOT)),
        "lean_compile_exit_code": completed.returncode,
        "arbitrary_run_identity_custody": True,
        "arbitrary_run_no_support_or_external_effect": True,
        "exact_run_composition": True,
        "terminal_states_absorbing": True,
    }


def build_result(
    valid_count: int, invalid_count: int, formal_surface: dict[str, Any]
) -> dict[str, Any]:
    payload = json.dumps(TRACES, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "artifact": "scf_lifecycle_trace_probe",
        "date": "2026-07-02",
        "validator": "python3 scripts/validate_scf_lifecycle_trace.py",
        "fixture_fingerprint_sha256": hashlib.sha256(payload).hexdigest(),
        "valid_traces": valid_count,
        "expected_invalid_controls": invalid_count,
        "formal_surface": formal_surface,
        "transition_coverage": {
            "shadow_to_canary": True,
            "canary_to_qualified": True,
            "qualified_to_default": True,
            "default_to_deprecated": True,
            "deprecated_to_retired": True,
            "incident_to_quarantine": True,
        },
        "negative_control_coverage": {
            "identity_drift": True,
            "default_without_regression_floor": True,
            "default_authority_expansion": True,
            "retired_restart": True,
            "deprecation_without_notice": True,
            "retirement_without_receipt": True,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "non_claims": [
            "does not execute deployed route validation",
            "does not prove evaluator-integrity measurement",
            "does not execute rollback",
            "does not prove real regression preservation",
            "does not enforce lifecycle transitions in production",
            "does not promote the chapter support state",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Write the deterministic local result JSON.")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for trace in TRACES:
        expect_valid = bool(trace.get("expect_valid"))
        trace_id = str(trace.get("trace_id", "<missing>"))
        current_errors = trace_errors(trace)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{trace_id}: expected-invalid control unexpectedly passed.")

    valid_traces = [trace for trace in TRACES if trace.get("expect_valid") is True]
    if valid_traces[0]["transitions"][-1].get("to") != "retired":
        errors.append("Forward lifecycle trace must terminate at retired.")
    if valid_traces[1]["transitions"][-1].get("to") != "quarantined":
        errors.append("Incident lifecycle trace must terminate at quarantined.")

    formal_surface = validate_formal_surface(errors)

    if errors:
        print("SCF lifecycle trace probe failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    result = build_result(valid_count, invalid_count, formal_surface)
    if args.write_result:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "SCF lifecycle trace probe passed: "
        f"{valid_count} valid trace(s), {invalid_count} expected-invalid control(s), "
        f"{formal_surface['theorem_count']} Lean theorem(s), exact terminal-state checks."
    )


if __name__ == "__main__":
    main()
