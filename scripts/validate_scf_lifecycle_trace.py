#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "experiments" / "scf_lifecycle_trace" / "results" / "2026-07-02-local.json"

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
        for index, transition in enumerate(transitions):
            if not isinstance(transition, dict):
                errors.append(f"{trace_id}:transitions[{index}] must be an object.")
            else:
                errors.extend(transition_errors(trace_id, transition, index))

    non_claim_text = " ".join(str(item).lower() for item in trace.get("non_claims", []))
    for marker in REQUIRED_NONCLAIMS:
        if marker not in non_claim_text:
            errors.append(f"{trace_id}: non_claims must include {marker!r}.")

    return errors


def build_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    payload = json.dumps(TRACES, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "artifact": "scf_lifecycle_trace_probe",
        "date": "2026-07-02",
        "validator": "python3 scripts/validate_scf_lifecycle_trace.py",
        "fixture_fingerprint_sha256": hashlib.sha256(payload).hexdigest(),
        "valid_traces": valid_count,
        "expected_invalid_controls": invalid_count,
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

    if errors:
        print("SCF lifecycle trace probe failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    result = build_result(valid_count, invalid_count)
    if args.write_result:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "SCF lifecycle trace probe passed: "
        f"{valid_count} valid trace(s), {invalid_count} expected-invalid control(s)."
    )


if __name__ == "__main__":
    main()
