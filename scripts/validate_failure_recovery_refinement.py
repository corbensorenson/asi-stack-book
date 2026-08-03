#!/usr/bin/env python3
"""Independently validate the bounded failure-recovery Lean refinement."""

from __future__ import annotations

import copy
import itertools
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
    "rejected_observation_preserves_exact_state",
    "accepted_observation_starts_from_valid_operating_state",
    "admitted_observation_requires_record_evidence_independence_and_boundary",
    "accepted_observation_refines_recovery_detection",
    "accepted_observation_preserves_incident_identity",
    "accepted_observation_opens_residual_and_blocks_effects_and_promotion",
    "accepted_observation_cannot_assign_support_or_external_authority",
    "accepted_observation_records_exactly_one_incident_and_receipt",
    "missing_observation_receipt_requests_evidence",
    "unclassified_observation_preserves_unmapped_residual",
    "captured_detector_cannot_admit_recovery",
    "authority_over_ceiling_cannot_admit_recovery",
    "open_escape_without_quarantine_cannot_admit_recovery",
    "recurrence_marker_substitution_cannot_admit_recovery",
    "complete_recurrence_observation_admits_escalated_recovery",
    "complete_severe_irreversible_observation_admits_escalated_recovery",
    "complete_ordinary_observation_reaches_isolated_recovery",
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


OBSERVATION_ADMISSIONS = {
    "admitRecovery", "admitRecurrenceRecovery", "admitSevereRecovery",
}


def observation(event_digest: int = 1) -> dict[str, object]:
    return {
        "packet": packet(event_digest),
        "detectorObserverDigest": 501,
        "subjectDigest": 502,
        "incidentRecorded": True,
        "evidenceReceiptRecorded": True,
        "authorityRequested": 2,
        "authorityCeiling": 3,
        "escapePathOpen": False,
        "quarantineRecorded": True,
        "recurrenceObserved": False,
        "severityHigh": False,
        "reversible": True,
        "nonClaimBoundaryRecorded": True,
    }


def observation_admissible(current: dict[str, object], item: dict[str, object]) -> bool:
    event = item["packet"]
    assert isinstance(event, dict)
    return (
        control_state_valid(current)
        and current["stage"] == "operating"
        and all(current[name] == event[name] for name in IDENTITY)
        and event["eventDigest"] != current["lastEventDigest"]
        and bool(item["incidentRecorded"])
        and bool(item["evidenceReceiptRecorded"])
        and bool(event["failureObserved"])
        and bool(event["failureClassRecorded"])
        and bool(event["boundaryRecorded"])
        and bool(event["detectorIndependent"])
        and item["detectorObserverDigest"] != item["subjectDigest"]
        and int(item["authorityRequested"]) <= int(item["authorityCeiling"])
        and (not bool(item["escapePathOpen"]) or bool(item["quarantineRecorded"]))
        and bool(event["recurrenceOfPriorIncident"]) == bool(item["recurrenceObserved"])
        and bool(item["nonClaimBoundaryRecorded"])
        and not bool(event["supportAssignmentRequested"])
        and not bool(event["externalAuthorityRequested"])
    )


def observation_route(current: dict[str, object], item: dict[str, object]) -> str:
    event = item["packet"]
    assert isinstance(event, dict)
    if observation_admissible(current, item):
        if item["recurrenceObserved"]:
            return "admitRecurrenceRecovery"
        if item["severityHigh"] and not item["reversible"]:
            return "admitSevereRecovery"
        return "admitRecovery"
    if not control_state_valid(current):
        return "rejectInvalidControlState"
    if current["stage"] != "operating":
        return "rejectNonoperatingIngress"
    if any(current[name] != event[name] for name in IDENTITY):
        return "rejectIncidentSubstitution"
    if event["eventDigest"] == current["lastEventDigest"]:
        return "rejectObservationReplay"
    if not item["incidentRecorded"]:
        return "requestIncidentRecord"
    if not item["evidenceReceiptRecorded"]:
        return "requestEvidenceReceipt"
    if not event["failureObserved"] or not event["failureClassRecorded"] or not event["boundaryRecorded"]:
        return "preserveUnmappedResidual"
    if not event["detectorIndependent"] or item["detectorObserverDigest"] == item["subjectDigest"]:
        return "rejectCapturedDetector"
    if int(item["authorityCeiling"]) < int(item["authorityRequested"]):
        return "requestAuthorityReview"
    if item["escapePathOpen"] and not item["quarantineRecorded"]:
        return "requestQuarantine"
    if bool(event["recurrenceOfPriorIncident"]) != bool(item["recurrenceObserved"]):
        return "rejectRecurrenceSubstitution"
    if not item["nonClaimBoundaryRecorded"]:
        return "requestNonClaimBoundary"
    if event["supportAssignmentRequested"] or event["externalAuthorityRequested"]:
        return "rejectAuthorityLeak"
    return "requestNonClaimBoundary"


def ingest_observation(
    current: dict[str, object], item: dict[str, object]
) -> tuple[dict[str, object], str]:
    answer = observation_route(current, item)
    if not observation_admissible(current, item):
        return copy.deepcopy(current), answer
    event = item["packet"]
    assert isinstance(event, dict)
    updated, recovery_answer = apply(current, "detectAndIsolate", event)
    if recovery_answer != "acceptDetection":
        raise AssertionError(f"admitted observation failed recovery refinement: {recovery_answer}")
    return updated, answer


def main() -> None:
    failures: list[str] = []
    theorem_count = validate_formal_surface()

    boundary = json.loads(BOUNDARY_FIXTURE.read_text(encoding="utf-8"))
    detector = json.loads(DETECTOR_RESULT.read_text(encoding="utf-8"))
    if boundary.get("support_state_effect") != "record_shape_only":
        failures.append("failure boundary fixture support scope drifted")
    if detector.get("valid_incident_count") != 2 or detector.get("support_state_effect") != "none":
        failures.append("inherited detector result boundary drifted")

    observation_controls: list[tuple[str, dict[str, object], dict[str, object], str]] = []

    def add_observation_control(
        label: str,
        item: dict[str, object],
        expected_route: str,
        before: dict[str, object] | None = None,
    ) -> None:
        observation_controls.append((label, before or state(), item, expected_route))

    invalid_control = state()
    invalid_control["promotionEnabled"] = False
    add_observation_control(
        "invalid_control_state", observation(), "rejectInvalidControlState", invalid_control
    )
    add_observation_control(
        "nonoperating_ingress", observation(), "rejectNonoperatingIngress", state("detected")
    )
    for field in IDENTITY:
        changed = observation()
        changed_packet = changed["packet"]
        assert isinstance(changed_packet, dict)
        changed_packet[field] = int(changed_packet[field]) + 1000
        add_observation_control(f"observation_identity_{field}", changed, "rejectIncidentSubstitution")
    replay = observation(0)
    add_observation_control("observation_replay", replay, "rejectObservationReplay")
    missing_incident = observation()
    missing_incident["incidentRecorded"] = False
    add_observation_control("missing_incident_record", missing_incident, "requestIncidentRecord")
    missing_evidence = observation()
    missing_evidence["evidenceReceiptRecorded"] = False
    add_observation_control("missing_evidence_receipt", missing_evidence, "requestEvidenceReceipt")
    for field in ("failureObserved", "failureClassRecorded", "boundaryRecorded"):
        unmapped = observation()
        unmapped_packet = unmapped["packet"]
        assert isinstance(unmapped_packet, dict)
        unmapped_packet[field] = False
        add_observation_control(f"unmapped_{field}", unmapped, "preserveUnmappedResidual")
    captured_flag = observation()
    captured_packet = captured_flag["packet"]
    assert isinstance(captured_packet, dict)
    captured_packet["detectorIndependent"] = False
    add_observation_control("captured_detector_flag", captured_flag, "rejectCapturedDetector")
    captured_role = observation()
    captured_role["detectorObserverDigest"] = captured_role["subjectDigest"]
    add_observation_control("captured_detector_role", captured_role, "rejectCapturedDetector")
    excess_authority = observation()
    excess_authority["authorityRequested"] = 4
    add_observation_control("authority_over_ceiling", excess_authority, "requestAuthorityReview")
    open_escape = observation()
    open_escape["escapePathOpen"] = True
    open_escape["quarantineRecorded"] = False
    add_observation_control("open_escape_without_quarantine", open_escape, "requestQuarantine")
    recurrence_observation_only = observation()
    recurrence_observation_only["recurrenceObserved"] = True
    add_observation_control(
        "recurrence_observation_substitution",
        recurrence_observation_only,
        "rejectRecurrenceSubstitution",
    )
    recurrence_packet_only = observation()
    recurrence_packet = recurrence_packet_only["packet"]
    assert isinstance(recurrence_packet, dict)
    recurrence_packet["recurrenceOfPriorIncident"] = True
    add_observation_control(
        "recurrence_packet_substitution", recurrence_packet_only, "rejectRecurrenceSubstitution"
    )
    missing_nonclaim = observation()
    missing_nonclaim["nonClaimBoundaryRecorded"] = False
    add_observation_control("missing_nonclaim_boundary", missing_nonclaim, "requestNonClaimBoundary")
    for field in ("supportAssignmentRequested", "externalAuthorityRequested"):
        authority_leak = observation()
        authority_packet = authority_leak["packet"]
        assert isinstance(authority_packet, dict)
        authority_packet[field] = True
        add_observation_control(f"observation_{field}", authority_leak, "rejectAuthorityLeak")

    for label, before, item, expected_route in observation_controls:
        after, answer = ingest_observation(before, item)
        if answer != expected_route:
            failures.append(f"observation control {label} routed {answer}, expected {expected_route}")
        if answer in OBSERVATION_ADMISSIONS:
            failures.append(f"observation control admitted: {label}")
        if after != before:
            failures.append(f"rejected observation changed recovery state: {label}")

    accepted_observations: list[tuple[str, dict[str, object], str]] = []
    accepted_observations.append(("ordinary", observation(), "admitRecovery"))
    recurrence_item = observation()
    recurrence_item["recurrenceObserved"] = True
    recurrence_item_packet = recurrence_item["packet"]
    assert isinstance(recurrence_item_packet, dict)
    recurrence_item_packet["recurrenceOfPriorIncident"] = True
    accepted_observations.append(("recurrence", recurrence_item, "admitRecurrenceRecovery"))
    severe_item = observation()
    severe_item["severityHigh"] = True
    severe_item["reversible"] = False
    accepted_observations.append(("severe_irreversible", severe_item, "admitSevereRecovery"))

    for label, item, expected_route in accepted_observations:
        after, answer = ingest_observation(state(), item)
        if answer != expected_route:
            failures.append(f"accepted observation {label} routed {answer}, expected {expected_route}")
        for field, expected in {
            "stage": "detected",
            "openResidualCount": 1,
            "containmentActive": True,
            "externalEffectsEnabled": False,
            "promotionEnabled": False,
            "receiptCount": 1,
            "incidentCount": 1,
            "supportAssignmentCount": 0,
            "externalAuthorityCount": 0,
        }.items():
            if after[field] != expected:
                failures.append(f"accepted observation {label} {field} drifted")
        expected_recurrence = int(label == "recurrence")
        if after["recurrenceCount"] != expected_recurrence:
            failures.append(f"accepted observation {label} recurrence count drifted")

    exhaustive_observation_count = 0
    for values in itertools.product((False, True), repeat=8):
        item = observation()
        event = item["packet"]
        assert isinstance(event, dict)
        (
            item["incidentRecorded"], item["evidenceReceiptRecorded"],
            event["failureObserved"], event["failureClassRecorded"],
            event["boundaryRecorded"], event["detectorIndependent"],
            item["nonClaimBoundaryRecorded"], event["supportAssignmentRequested"],
        ) = values
        admissible = observation_admissible(state(), item)
        after, answer = ingest_observation(state(), item)
        if (answer in OBSERVATION_ADMISSIONS) != admissible:
            failures.append(f"exhaustive observation admission mismatch: {values}")
        if not admissible and after != state():
            failures.append(f"exhaustive rejected observation changed state: {values}")
        exhaustive_observation_count += 1

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
        "3 accepted observation-ingress classes, "
        f"{len(observation_controls)}/{len(observation_controls)} rejecting observation controls, "
        f"{exhaustive_observation_count} exhaustive observation combinations, "
        "5 reachable recovery stages, 5 accepted "
        f"transitions, {len(mutations)}/{len(mutations)} rejecting mutations, "
        f"{len(lifecycle) + 1} lifecycle splits, guarded readmission, "
        "recurrence re-isolation, support effect none."
    )


if __name__ == "__main__":
    main()
