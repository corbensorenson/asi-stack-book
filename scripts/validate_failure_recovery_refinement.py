#!/usr/bin/env python3
"""Independently validate the bounded failure-recovery Lean refinement."""

from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/FailureRecoveryRefinement.lean"
BOUNDARY_FIXTURE = ROOT / "tests/fixtures/protocol_records/failure_boundary_map.valid.json"
DETECTOR_RESULT = ROOT / "experiments/failure_taxonomy_detector/results/2026-07-02-local.json"

STAGES = ["operating", "detected", "contained", "remediated", "reviewed"]
EXPECTED = {
    "operating": "detectAndIsolate",
    "detected": "confirmContainment",
    "contained": "recordRemediation",
    "remediated": "recordReview",
    "reviewed": "requestReadmission",
}
NEXT = {
    "operating": "detected",
    "detected": "contained",
    "contained": "remediated",
    "remediated": "reviewed",
    "reviewed": "operating",
}
IDENTITY = (
    "incidentId", "boundaryVersion", "architectureDigest", "policyDigest",
    "detectorDigest", "containmentDigest", "remediationDigest",
    "reviewerDigest", "assuranceDigest",
)
ACCEPTED = {
    "acceptDetection", "acceptContainment", "acceptRemediation",
    "acceptReview", "acceptReadmission",
}
GATES = {
    "operating": (
        ("failureObserved", False, "requestObservation"),
        ("failureClassRecorded", False, "requestFailureClass"),
        ("boundaryRecorded", False, "requestBoundary"),
        ("detectorIndependent", False, "rejectSelfJudgment"),
    ),
    "detected": (
        ("containmentApplied", False, "requestContainment"),
        ("escapePathClosed", False, "requestEscapeClosure"),
        ("containmentOwnerAccepted", False, "requestContainmentOwner"),
    ),
    "contained": (
        ("causeRecorded", False, "requestCause"),
        ("remediationApplied", False, "requestRemediation"),
        ("regressionEvidencePassed", False, "requestRegressionEvidence"),
    ),
    "remediated": (
        ("independentReviewRecorded", False, "requestIndependentReview"),
        ("reviewerIndependent", False, "rejectReviewerCapture"),
        ("residualRecorded", False, "requestResidual"),
    ),
    "reviewed": (
        ("assuranceCurrent", False, "requestCurrentAssurance"),
        ("taxonomyCurrent", False, "requestCurrentTaxonomy"),
        ("residualDischarged", False, "requestResidualDischarge"),
        ("readmissionAuthorityPresent", False, "requestReadmissionAuthority"),
    ),
}
EXPECTED_THEOREMS = {
    "apply_event_preserves_incident_identity",
    "accepted_step_is_accepted",
    "accepted_step_applies_event",
    "accepted_step_adds_exactly_one_receipt",
    "accepted_step_starts_from_valid_control_state",
    "accepted_step_updates_incident_count_exactly",
    "accepted_step_updates_recovery_count_exactly",
    "accepted_step_updates_recurrence_count_exactly",
    "accepted_step_incident_recovery_and_recurrence_monotone",
    "successful_run_preserves_incident_identity",
    "successful_run_cannot_assign_support_or_external_authority",
    "successful_run_adds_exactly_one_receipt_per_event",
    "successful_run_incident_recovery_and_recurrence_monotone",
    "successful_run_has_valid_trace",
    "recovery_run_composes_across_event_batches",
    "rejected_event_preserves_exact_state",
    "transition_cannot_assign_support_or_external_authority",
    "nonoperating_valid_state_blocks_effects_and_promotion",
    "accepted_detection_opens_residual_and_blocks_effects_and_promotion",
    "accepted_readmission_closes_residual_and_restores_bounded_operation",
    "accepted_readmission_requires_complete_review",
    "missing_escape_closure_blocks_containment",
    "captured_reviewer_blocks_review",
    "stale_assurance_blocks_readmission",
    "authority_leak_blocks_every_stage",
    "bounded_failure_recovery_reaches_guarded_readmission",
    "bounded_recurrence_reisolates_after_recovery",
}


def validate_formal_surface() -> int:
    source = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z][A-Za-z0-9_]*)", source))
    if names != EXPECTED_THEOREMS:
        raise AssertionError(
            "Lean theorem surface drifted; "
            f"missing={sorted(EXPECTED_THEOREMS - names)}, "
            f"extra={sorted(names - EXPECTED_THEOREMS)}"
        )
    command = ["lake", "env", "lean", "AsiStackProofs/FailureRecoveryRefinement.lean"]
    completed = subprocess.run(command, cwd=ROOT / "lean", capture_output=True, text=True)
    if completed.returncode:
        raise AssertionError(completed.stdout + completed.stderr)
    return len(names)


def state(stage: str = "operating") -> dict[str, object]:
    open_incident = stage != "operating"
    return {
        "stage": stage, "incidentId": 41, "boundaryVersion": 3,
        "architectureDigest": 101, "policyDigest": 102, "detectorDigest": 103,
        "containmentDigest": 104, "remediationDigest": 105,
        "reviewerDigest": 106, "assuranceDigest": 107, "lastEventDigest": 0,
        "receiptCount": 0, "incidentCount": int(open_incident),
        "recoveryCount": 0, "recurrenceCount": 0,
        "openResidualCount": int(open_incident),
        "containmentActive": open_incident,
        "externalEffectsEnabled": stage == "operating",
        "promotionEnabled": stage == "operating",
        "supportAssignmentCount": 0, "externalAuthorityCount": 0,
    }


def packet(event_digest: int) -> dict[str, object]:
    return {
        "incidentId": 41, "boundaryVersion": 3, "architectureDigest": 101,
        "policyDigest": 102, "detectorDigest": 103, "containmentDigest": 104,
        "remediationDigest": 105, "reviewerDigest": 106,
        "assuranceDigest": 107, "eventDigest": event_digest,
        "failureObserved": True, "failureClassRecorded": True,
        "boundaryRecorded": True, "detectorIndependent": True,
        "containmentApplied": True, "escapePathClosed": True,
        "containmentOwnerAccepted": True, "causeRecorded": True,
        "remediationApplied": True, "regressionEvidencePassed": True,
        "independentReviewRecorded": True, "reviewerIndependent": True,
        "residualRecorded": True, "assuranceCurrent": True,
        "taxonomyCurrent": True, "residualDischarged": True,
        "readmissionAuthorityPresent": True,
        "recurrenceOfPriorIncident": False,
        "supportAssignmentRequested": False, "externalAuthorityRequested": False,
    }


def route(current: dict[str, object], kind: str, event: dict[str, object]) -> str:
    stage = str(current["stage"])
    if not control_state_valid(current):
        return "rejectInvalidControlState"
    if kind != EXPECTED[stage]:
        return "rejectWrongStage"
    if any(current[name] != event[name] for name in IDENTITY):
        return "rejectIncidentSubstitution"
    if event["eventDigest"] == current["lastEventDigest"]:
        return "rejectEventReplay"
    if event["supportAssignmentRequested"] or event["externalAuthorityRequested"]:
        return "rejectAuthorityLeak"
    for field, bad, answer in GATES[stage]:
        if event[field] is bad:
            return answer
    return {
        "operating": "acceptDetection", "detected": "acceptContainment",
        "contained": "acceptRemediation", "remediated": "acceptReview",
        "reviewed": "acceptReadmission",
    }[stage]


def control_state_valid(current: dict[str, object]) -> bool:
    operating = current["stage"] == "operating"
    return (
        current["containmentActive"] is (not operating)
        and current["externalEffectsEnabled"] is operating
        and current["promotionEnabled"] is operating
        and current["openResidualCount"] == int(not operating)
    )


def apply(current: dict[str, object], kind: str, event: dict[str, object]) -> tuple[dict[str, object], str]:
    answer = route(current, kind, event)
    if answer not in ACCEPTED:
        return copy.deepcopy(current), answer
    updated = copy.deepcopy(current)
    updated["stage"] = NEXT[str(current["stage"])]
    updated["lastEventDigest"] = event["eventDigest"]
    updated["receiptCount"] = int(current["receiptCount"]) + 1
    updated["incidentCount"] = int(current["incidentCount"]) + (answer == "acceptDetection")
    updated["recoveryCount"] = int(current["recoveryCount"]) + (answer == "acceptReadmission")
    updated["recurrenceCount"] = int(current["recurrenceCount"]) + (
        answer == "acceptDetection" and bool(event["recurrenceOfPriorIncident"])
    )
    if answer == "acceptDetection":
        updated["openResidualCount"] = int(current["openResidualCount"]) + 1
    elif answer == "acceptReadmission":
        updated["openResidualCount"] = int(current["openResidualCount"]) - 1
    updated["containmentActive"] = answer != "acceptReadmission"
    updated["externalEffectsEnabled"] = answer == "acceptReadmission"
    updated["promotionEnabled"] = answer == "acceptReadmission"
    return updated, answer


def run(current: dict[str, object], events: list[tuple[str, dict[str, object]]]) -> dict[str, object] | None:
    result = copy.deepcopy(current)
    for kind, event in events:
        result, answer = apply(result, kind, event)
        if answer not in ACCEPTED:
            return None
    return result


def main() -> None:
    failures: list[str] = []
    theorem_count = validate_formal_surface()

    boundary = json.loads(BOUNDARY_FIXTURE.read_text(encoding="utf-8"))
    detector = json.loads(DETECTOR_RESULT.read_text(encoding="utf-8"))
    if boundary.get("support_state_effect") != "record_shape_only":
        failures.append("failure boundary fixture support scope drifted")
    if detector.get("valid_incident_count") != 2 or detector.get("support_state_effect") != "none":
        failures.append("inherited detector result boundary drifted")

    mutations: list[tuple[str, dict[str, object], str, dict[str, object]]] = []
    for index, stage_name in enumerate(STAGES, 1):
        before = state(stage_name)
        for wrong_kind in EXPECTED.values():
            if wrong_kind != EXPECTED[stage_name]:
                mutations.append((
                    f"wrong_stage_{stage_name}_{wrong_kind}", before,
                    wrong_kind, packet(index),
                ))
        for field in IDENTITY:
            changed = packet(20 + index)
            changed[field] = int(changed[field]) + 1000
            mutations.append((
                f"identity_{stage_name}_{field}", before,
                EXPECTED[stage_name], changed,
            ))
        replay = packet(0)
        mutations.append((
            f"event_replay_{stage_name}", before, EXPECTED[stage_name], replay,
        ))
        for field in ("supportAssignmentRequested", "externalAuthorityRequested"):
            leaked = packet(30 + index)
            leaked[field] = True
            mutations.append((
                f"authority_{stage_name}_{field}", before,
                EXPECTED[stage_name], leaked,
            ))
        for field in (
            "containmentActive", "externalEffectsEnabled", "promotionEnabled",
        ):
            invalid = copy.deepcopy(before)
            invalid[field] = not bool(invalid[field])
            mutations.append((
                f"control_{stage_name}_{field}", invalid,
                EXPECTED[stage_name], packet(40 + index),
            ))
        invalid_residual = copy.deepcopy(before)
        invalid_residual["openResidualCount"] = 2
        mutations.append((
            f"control_{stage_name}_openResidualCount", invalid_residual,
            EXPECTED[stage_name], packet(50 + index),
        ))
    for stage_name, gates in GATES.items():
        for field, bad, _ in gates:
            rejected = packet(60 + len(mutations))
            rejected[field] = bad
            mutations.append((f"gate_{stage_name}_{field}", state(stage_name), EXPECTED[stage_name], rejected))

    for label, before, kind, event in mutations:
        after, answer = apply(before, kind, event)
        if answer in ACCEPTED:
            failures.append(f"mutation accepted: {label}")
        if after != before:
            failures.append(f"rejected mutation changed state: {label}")

    lifecycle = [(EXPECTED[stage_name], packet(digest))
                 for digest, stage_name in enumerate(STAGES, 1)]
    current = state()
    reachable = [copy.deepcopy(current)]
    for kind, event in lifecycle:
        current, answer = apply(current, kind, event)
        if answer not in ACCEPTED:
            failures.append(f"canonical lifecycle blocked at {kind}: {answer}")
        if not control_state_valid(current):
            failures.append(f"canonical lifecycle produced invalid control state at {kind}")
        reachable.append(copy.deepcopy(current))
    for split in range(len(lifecycle) + 1):
        prefix = run(state(), lifecycle[:split])
        if prefix != reachable[split]:
            failures.append(f"prefix replay drifted at split {split}")
            continue
        suffix = run(prefix, lifecycle[split:])
        if suffix != current:
            failures.append(f"composition replay drifted at split {split}")
    expected_recovery = {
        "stage": "operating", "receiptCount": 5, "incidentCount": 1,
        "recoveryCount": 1, "openResidualCount": 0,
        "recurrenceCount": 0, "containmentActive": False,
        "externalEffectsEnabled": True, "promotionEnabled": True,
        "supportAssignmentCount": 0,
        "externalAuthorityCount": 0,
    }
    for field, expected in expected_recovery.items():
        if current[field] != expected:
            failures.append(f"recovery witness {field} drifted")

    recurrence = packet(6)
    recurrence["recurrenceOfPriorIncident"] = True
    current, answer = apply(current, "detectAndIsolate", recurrence)
    expected_recurrence = {
        "stage": "detected", "receiptCount": 6, "incidentCount": 2,
        "recoveryCount": 1, "recurrenceCount": 1, "openResidualCount": 1,
        "containmentActive": True, "externalEffectsEnabled": False,
        "promotionEnabled": False, "supportAssignmentCount": 0,
        "externalAuthorityCount": 0,
    }
    if answer != "acceptDetection":
        failures.append(f"recurrence witness blocked: {answer}")
    for field, expected in expected_recurrence.items():
        if current[field] != expected:
            failures.append(f"recurrence witness {field} drifted")

    if failures:
        raise SystemExit("Failure-recovery refinement failed:\n - " + "\n - ".join(failures))
    print(
        f"Failure-recovery refinement passed: {theorem_count} Lean theorems, "
        "5 reachable stages, 5 accepted "
        f"transitions, {len(mutations)}/{len(mutations)} rejecting mutations, "
        f"{len(lifecycle) + 1} lifecycle splits, guarded readmission, "
        "recurrence re-isolation, support effect none."
    )


if __name__ == "__main__":
    main()
