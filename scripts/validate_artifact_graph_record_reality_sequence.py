#!/usr/bin/env python3
"""Validate a bounded Artifact Graph record-reality sequence fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (
    ROOT
    / "experiments"
    / "artifact_graph_record_reality_sequence"
    / "input"
    / "record_reality_sequence.json"
)
RESULT = (
    ROOT
    / "experiments"
    / "artifact_graph_record_reality_sequence"
    / "results"
    / "2026-07-04-local.json"
)

FRESH_REPLAY_GRADES = {"semantic", "byte_exact"}
VALID_TRANSACTION_STATES = {"replay_validated"}
VALID_INDEPENDENT_CHECKS = {"internal_independent", "external"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def non_claim_boundary(event: dict[str, Any]) -> bool:
    claims = event.get("non_claims")
    if not isinstance(claims, list) or not claims:
        return False
    text = " ".join(str(item).lower() for item in claims)
    return "does not" in text and "support" in text and "promot" in text


def event_is_fresh(event: dict[str, Any]) -> bool:
    return (
        event.get("replay_grade") in FRESH_REPLAY_GRADES
        and event.get("provenance_status") == "complete"
        and event.get("certificate_state") == "active"
        and event.get("transaction_validity_state") in VALID_TRANSACTION_STATES
        and event.get("artifact_digest_verified") is True
        and event.get("independent_check") in VALID_INDEPENDENT_CHECKS
        and event.get("support_state_effect") == "none"
        and non_claim_boundary(event)
    )


def route_event(event: dict[str, Any]) -> str:
    if event.get("support_state_effect") != "none":
        return "reject_support_state_effect"
    if not non_claim_boundary(event):
        return "require_non_claim_boundary"
    if event.get("certificate_state") != "active":
        return "block_stale_certificate"
    if event.get("replay_grade") not in FRESH_REPLAY_GRADES:
        return "block_incomplete_replay"
    if event.get("provenance_status") != "complete":
        return "block_incomplete_provenance"
    if event.get("transaction_validity_state") not in VALID_TRANSACTION_STATES:
        return "require_replay_validated_transaction"
    if event.get("artifact_digest_verified") is not True:
        return "require_digest_verification"
    if event.get("independent_check") not in VALID_INDEPENDENT_CHECKS:
        return "require_independent_check"
    return "eligible_for_bounded_review"


def validate_event_shape(event: Any, owner: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(event, dict):
        return [f"{owner}: event must be an object."]
    for field in (
        "event_id",
        "artifact_id",
        "replay_grade",
        "provenance_status",
        "certificate_state",
        "transaction_validity_state",
        "independent_check",
        "support_state_effect",
    ):
        if not isinstance(event.get(field), str) or not event.get(field, "").strip():
            errors.append(f"{owner}: {field} must be a non-empty string.")
    for field in ("artifact_digest_verified", "support_review_requested"):
        if not isinstance(event.get(field), bool):
            errors.append(f"{owner}: {field} must be a boolean.")
    if not isinstance(event.get("non_claims"), list):
        errors.append(f"{owner}: non_claims must be a list.")
    return errors


def evaluate_case(case: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    case_id = str(case.get("case_id", "unknown"))
    events = case.get("events")
    if not isinstance(events, list) or not events:
        return {"case_id": case_id, "routes": [], "final_eligible": False}, [f"{case_id}: events must be a non-empty list."]

    routes: list[str] = []
    eligible = False
    saw_block = False
    restored_after_block = False
    for index, event in enumerate(events):
        owner = f"{case_id}.events[{index}]"
        errors.extend(validate_event_shape(event, owner))
        if not isinstance(event, dict):
            continue
        route = route_event(event)
        routes.append(route)
        event_eligible = route == "eligible_for_bounded_review" and event_is_fresh(event)
        if event.get("support_review_requested") is True and not event_eligible:
            errors.append(f"{owner}: support review requested while record is not fresh enough.")
        if route != "eligible_for_bounded_review":
            saw_block = True
            eligible = False
        else:
            if saw_block:
                restored_after_block = True
            eligible = True

    expected_final = case.get("expected_final_eligible")
    if not isinstance(expected_final, bool):
        errors.append(f"{case_id}: expected_final_eligible must be a boolean.")
    elif expected_final != eligible:
        errors.append(f"{case_id}: expected final eligibility {expected_final} but computed {eligible}.")

    return (
        {
            "case_id": case_id,
            "routes": routes,
            "final_eligible": eligible,
            "saw_block": saw_block,
            "restored_after_block": restored_after_block,
            "event_count": len(events),
        },
        errors,
    )


def build_summary(fixture: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if fixture.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list.")
        cases = []

    accepted_cases: list[dict[str, Any]] = []
    expected_invalid_count = 0
    valid_count = 0
    invalid_controls_rejected = 0
    all_routes: set[str] = set()
    valid_event_count = 0
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"cases[{index}]: case must be an object.")
            continue
        expectation = case.get("expectation")
        if expectation not in {"valid", "invalid"}:
            errors.append(f"{case.get('case_id', index)}: expectation must be valid or invalid.")
            continue
        evaluated, case_errors = evaluate_case(case)
        all_routes.update(str(route) for route in evaluated["routes"])
        if expectation == "valid":
            valid_count += 1
            valid_event_count += int(evaluated["event_count"])
            errors.extend(case_errors)
            accepted_cases.append(evaluated)
        else:
            expected_invalid_count += 1
            if case_errors:
                invalid_controls_rejected += 1
            else:
                errors.append(f"{case.get('case_id', index)}: expected-invalid control passed.")

    valid_restored = any(case.get("restored_after_block") is True for case in accepted_cases)
    valid_final_eligible = all(case.get("final_eligible") is True for case in accepted_cases)
    summary = {
        "result_id": "artifact_graph_record_reality_sequence_2026_07_04_local",
        "fixture": rel(FIXTURE),
        "valid_case_count": valid_count,
        "expected_invalid_case_count": expected_invalid_count,
        "invalid_controls_rejected": invalid_controls_rejected,
        "valid_event_count": valid_event_count,
        "routes_observed": sorted(all_routes),
        "fresh_replay_restores_after_block": valid_restored,
        "valid_sequences_end_eligible": valid_final_eligible,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "non_claims": [
            "does not promote any chapter core support state",
            "does not prove deployed artifact graph behavior, real replay, verifier correctness, audit durability, or source interpretation",
        ],
    }
    if not valid_restored:
        errors.append("valid sequence must demonstrate fresh replay restoring bounded-review eligibility after a block.")
    if not valid_final_eligible:
        errors.append("all valid sequences must end eligible for bounded review.")
    if invalid_controls_rejected != expected_invalid_count:
        errors.append("not all expected-invalid controls were rejected.")
    return summary, errors


def validate_result(summary: dict[str, Any], errors: list[str]) -> None:
    if not RESULT.exists():
        errors.append(f"{rel(RESULT)} is missing; run this script with --write-result.")
        return
    result = load_json(RESULT)
    if result != summary:
        errors.append(f"{rel(RESULT)} is out of date; run this script with --write-result.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    fixture = load_json(FIXTURE)
    if not isinstance(fixture, dict):
        print(f"{rel(FIXTURE)} must contain a JSON object.")
        sys.exit(1)
    summary, errors = build_summary(fixture)
    if args.write_result:
        RESULT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    else:
        validate_result(summary, errors)
    if errors:
        print("Artifact graph record-reality sequence validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Artifact graph record-reality sequence validation passed: "
        f"{summary['valid_case_count']} valid sequence(s), "
        f"{summary['expected_invalid_case_count']} expected-invalid control(s), "
        f"{summary['invalid_controls_rejected']} rejected."
    )


if __name__ == "__main__":
    main()
