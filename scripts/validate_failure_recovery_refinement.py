#!/usr/bin/env python3
"""Independently validate the bounded failure-recovery Lean refinement."""

from __future__ import annotations

import copy
import json
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
        ("readmissionAuthorityPresent", False, "requestReadmissionAuthority"),
    ),
}


def state(stage: str = "operating") -> dict[str, object]:
    return {
        "stage": stage, "incidentId": 41, "boundaryVersion": 3,
        "architectureDigest": 101, "policyDigest": 102, "detectorDigest": 103,
        "containmentDigest": 104, "remediationDigest": 105,
        "reviewerDigest": 106, "assuranceDigest": 107, "lastEventDigest": 0,
        "receiptCount": 0, "recoveryCount": 0, "recurrenceCount": 0,
        "containmentActive": stage != "operating",
        "externalEffectsEnabled": stage == "operating",
        "supportAssignmentCount": 0, "externalAuthorityCount": 0,
    }


def packet(event_digest: int) -> dict[str, object]:
    return {
        "incidentId": 41, "boundaryVersion": 3, "architectureDigest": 101,
        "policyDigest": 102, "detectorDigest": 103, "containmentDigest": 104,
        "remediationDigest": 105, "reviewerDigest": 106,
        "assuranceDigest": 107, "eventDigest": event_digest,
        "failureObserved": True, "detectorIndependent": True,
        "containmentApplied": True, "escapePathClosed": True,
        "containmentOwnerAccepted": True, "causeRecorded": True,
        "remediationApplied": True, "regressionEvidencePassed": True,
        "independentReviewRecorded": True, "reviewerIndependent": True,
        "residualRecorded": True, "assuranceCurrent": True,
        "taxonomyCurrent": True, "readmissionAuthorityPresent": True,
        "recurrenceOfPriorIncident": False,
        "supportAssignmentRequested": False, "externalAuthorityRequested": False,
    }


def route(current: dict[str, object], kind: str, event: dict[str, object]) -> str:
    stage = str(current["stage"])
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


def apply(current: dict[str, object], kind: str, event: dict[str, object]) -> tuple[dict[str, object], str]:
    answer = route(current, kind, event)
    if answer not in ACCEPTED:
        return copy.deepcopy(current), answer
    updated = copy.deepcopy(current)
    updated["stage"] = NEXT[str(current["stage"])]
    updated["lastEventDigest"] = event["eventDigest"]
    updated["receiptCount"] = int(current["receiptCount"]) + 1
    updated["recoveryCount"] = int(current["recoveryCount"]) + (answer == "acceptReadmission")
    updated["recurrenceCount"] = int(current["recurrenceCount"]) + (
        answer == "acceptDetection" and bool(event["recurrenceOfPriorIncident"])
    )
    updated["containmentActive"] = answer != "acceptReadmission"
    updated["externalEffectsEnabled"] = answer == "acceptReadmission"
    return updated, answer


def main() -> None:
    failures: list[str] = []
    source = LEAN.read_text(encoding="utf-8")
    for needle in (
        "rejected_event_preserves_exact_state",
        "accepted_readmission_requires_complete_review",
        "bounded_failure_recovery_reaches_guarded_readmission",
        "bounded_recurrence_reisolates_after_recovery",
    ):
        if needle not in source:
            failures.append(f"Lean source missing {needle}")

    boundary = json.loads(BOUNDARY_FIXTURE.read_text(encoding="utf-8"))
    detector = json.loads(DETECTOR_RESULT.read_text(encoding="utf-8"))
    if boundary.get("support_state_effect") != "record_shape_only":
        failures.append("failure boundary fixture support scope drifted")
    if detector.get("valid_incident_count") != 2 or detector.get("support_state_effect") != "none":
        failures.append("inherited detector result boundary drifted")

    mutations: list[tuple[str, dict[str, object], str, dict[str, object]]] = []
    for index, stage_name in enumerate(STAGES, 1):
        wrong_kind = "detectAndIsolate" if stage_name == "reviewed" else "requestReadmission"
        mutations.append((f"wrong_stage_{stage_name}", state(stage_name), wrong_kind, packet(index)))
    for field in IDENTITY:
        changed = packet(20)
        changed[field] = int(changed[field]) + 1000
        mutations.append((f"identity_{field}", state(), EXPECTED["operating"], changed))
    replay = packet(0)
    mutations.append(("event_replay", state(), EXPECTED["operating"], replay))
    for field in ("supportAssignmentRequested", "externalAuthorityRequested"):
        leaked = packet(21)
        leaked[field] = True
        mutations.append((f"authority_{field}", state(), EXPECTED["operating"], leaked))
    for stage_name, gates in GATES.items():
        for field, bad, _ in gates:
            rejected = packet(22)
            rejected[field] = bad
            mutations.append((f"gate_{stage_name}_{field}", state(stage_name), EXPECTED[stage_name], rejected))

    for label, before, kind, event in mutations:
        after, answer = apply(before, kind, event)
        if answer in ACCEPTED:
            failures.append(f"mutation accepted: {label}")
        if after != before:
            failures.append(f"rejected mutation changed state: {label}")

    current = state()
    for digest, stage_name in enumerate(STAGES, 1):
        current, answer = apply(current, EXPECTED[stage_name], packet(digest))
        if answer not in ACCEPTED:
            failures.append(f"canonical lifecycle blocked at {stage_name}: {answer}")
    expected_recovery = {
        "stage": "operating", "receiptCount": 5, "recoveryCount": 1,
        "recurrenceCount": 0, "containmentActive": False,
        "externalEffectsEnabled": True, "supportAssignmentCount": 0,
        "externalAuthorityCount": 0,
    }
    for field, expected in expected_recovery.items():
        if current[field] != expected:
            failures.append(f"recovery witness {field} drifted")

    recurrence = packet(6)
    recurrence["recurrenceOfPriorIncident"] = True
    current, answer = apply(current, "detectAndIsolate", recurrence)
    expected_recurrence = {
        "stage": "detected", "receiptCount": 6, "recoveryCount": 1,
        "recurrenceCount": 1, "containmentActive": True,
        "externalEffectsEnabled": False, "supportAssignmentCount": 0,
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
        "Failure-recovery refinement passed: 5 reachable stages, 5 accepted "
        f"transitions, {len(mutations)}/{len(mutations)} rejecting mutations, "
        "guarded readmission, recurrence re-isolation, support effect none."
    )


if __name__ == "__main__":
    main()
