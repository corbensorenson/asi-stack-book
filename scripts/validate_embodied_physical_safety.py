#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "EmbodiedPhysicalSafety.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
CHAPTER = ROOT / "chapters" / "embodied-agency-real-time-control-and-physical-safety.qmd"
DOSSIER = ROOT / "evidence_quality" / "proof_model_dossiers" / "embodied-agency-real-time-control-and-physical-safety.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
FIXTURE = ROOT / "tests" / "fixtures" / "proof_models" / "embodied_control_lease.json"

TAG = "lean:embodiment.missing_safety_state_blocks_control"
MODULE = "AsiStackProofs.EmbodiedPhysicalSafety"
FORMAL_TARGET = (
    "A finite control-lease model derives freshness, timing, state-envelope, actuator, "
    "fallback-distance, stop, effect, custody, and boundary conditions from authored fields; "
    "one complete lease reaches only a Project Theseus closed-loop trial, while 13 axis mutations "
    "fail readiness and reach exact repair routes. A separate eight-stage simulation-trial review "
    "lifecycle proves arbitrary-run nine-field identity custody, support/effect non-authority, exact "
    "receipts, stop-count monotonicity, accepted traces, batch composition, absorbing closure, and "
    "safety-axis start blocking; an independent consumer rejects 105/105 mutations. It establishes "
    "no plant truth, physical or human safety, deadline satisfaction, safe-set validity, fallback "
    "effectiveness, recovery, support, release, transfer, or external effect."
)


def complete_lease() -> dict[str, Any]:
    return {
        "commandRequested": True,
        "plantIdentityBound": True,
        "leaseVersionCurrent": True,
        "currentTick": 5,
        "leaseExpiresAt": 8,
        "stateObservedAt": 4,
        "maximumObservationAge": 2,
        "worstCaseLatency": 2,
        "controlPeriod": 3,
        "deadlineSlack": 3,
        "safeLower": 2,
        "safeUpper": 10,
        "estimateLower": 4,
        "estimateUpper": 7,
        "requestedMagnitude": 4,
        "actuatorLimit": 6,
        "stopDistanceUpperBound": 3,
        "remainingDistanceMargin": 5,
        "fallbackControllerReady": True,
        "independentStopArmed": True,
        "effectObservationReady": True,
        "residualCustodyPresent": True,
        "nonClaimBoundaryPresent": True,
    }


def checks(lease: dict[str, Any]) -> list[tuple[str, bool, str]]:
    lease_current = lease["currentTick"] <= lease["leaseExpiresAt"]
    observation_fresh = (
        lease["stateObservedAt"] <= lease["currentTick"]
        and lease["currentTick"]
        <= lease["stateObservedAt"] + lease["maximumObservationAge"]
    )
    state_within_envelope = (
        lease["safeLower"] <= lease["estimateLower"]
        <= lease["estimateUpper"] <= lease["safeUpper"]
    )
    timing_within_budget = (
        lease["worstCaseLatency"] <= lease["controlPeriod"]
        and lease["worstCaseLatency"] <= lease["deadlineSlack"]
    )
    command_within_envelope = lease["requestedMagnitude"] <= lease["actuatorLimit"]
    fallback_reachable = (
        lease["fallbackControllerReady"]
        and lease["stopDistanceUpperBound"] <= lease["remainingDistanceMargin"]
    )
    return [
        ("commandRequest", lease["commandRequested"], "noCommandRequested"),
        ("plantIdentity", lease["plantIdentityBound"], "repairPlantIdentity"),
        ("leaseVersion", lease["leaseVersionCurrent"], "renewLeaseVersion"),
        ("leaseCurrent", lease_current, "renewExpiredLease"),
        ("observationFreshness", observation_fresh, "refreshStateEstimate"),
        ("stateEnvelope", state_within_envelope, "restoreStateEnvelope"),
        ("timingBudget", timing_within_budget, "restoreTimingBudget"),
        ("actuatorEnvelope", command_within_envelope, "reduceCommandMagnitude"),
        ("fallbackReachability", fallback_reachable, "restoreFallbackReachability"),
        ("independentStop", lease["independentStopArmed"], "armIndependentStop"),
        ("effectObservation", lease["effectObservationReady"], "restoreEffectObservation"),
        ("residualCustody", lease["residualCustodyPresent"], "assignResidualCustody"),
        ("nonClaimBoundary", lease["nonClaimBoundaryPresent"], "recordNonClaimBoundary"),
    ]


def ready(lease: dict[str, Any]) -> bool:
    return all(value for _, value, _ in checks(lease))


def route(lease: dict[str, Any]) -> str:
    for _, value, repair in checks(lease):
        if not value:
            return repair
    return "eligibleForTheseusClosedLoopTrial"


Mutation = Callable[[dict[str, Any]], None]
MUTATIONS: dict[str, Mutation] = {
    "commandRequest": lambda lease: lease.update(commandRequested=False),
    "plantIdentity": lambda lease: lease.update(plantIdentityBound=False),
    "leaseVersion": lambda lease: lease.update(leaseVersionCurrent=False),
    "leaseCurrent": lambda lease: lease.update(leaseExpiresAt=4),
    "observationFreshness": lambda lease: lease.update(stateObservedAt=1, maximumObservationAge=2),
    "stateEnvelope": lambda lease: lease.update(estimateUpper=11),
    "timingBudget": lambda lease: lease.update(worstCaseLatency=4),
    "actuatorEnvelope": lambda lease: lease.update(requestedMagnitude=7),
    "fallbackReachability": lambda lease: lease.update(stopDistanceUpperBound=6),
    "independentStop": lambda lease: lease.update(independentStopArmed=False),
    "effectObservation": lambda lease: lease.update(effectObservationReady=False),
    "residualCustody": lambda lease: lease.update(residualCustodyPresent=False),
    "nonClaimBoundary": lambda lease: lease.update(nonClaimBoundaryPresent=False),
}

REQUIRED_THEOREMS = {
    "complete_control_lease_is_ready",
    "complete_control_lease_routes_only_to_theseus_trial",
    "admissible_control_lease_is_ready",
    "every_control_axis_omission_blocks_readiness",
    "every_control_axis_omission_reaches_exact_repair_route",
    "every_control_axis_omission_blocks_trial_eligibility",
    "reduced_latency_preserves_timing_validity",
    "lower_state_violation_persists_under_downward_widening",
    "fallback_distance_violation_persists_when_bound_grows",
    "readiness_requires_command_request",
    "readiness_requires_plant_identity",
    "readiness_requires_current_lease_version",
    "readiness_requires_unexpired_lease",
    "readiness_requires_fresh_observation",
    "readiness_requires_state_envelope",
    "readiness_requires_timing_budget",
    "readiness_requires_actuator_envelope",
    "readiness_requires_reachable_fallback",
    "readiness_requires_independent_stop",
    "readiness_requires_effect_observation",
    "readiness_requires_residual_custody",
    "readiness_requires_non_claim_boundary",
    "accepted_trial_step_is_accepted",
    "accepted_trial_step_applies_event",
    "apply_trial_event_preserves_identity",
    "accepted_trial_step_preserves_identity",
    "accepted_trial_step_preserves_non_authority",
    "accepted_trial_step_adds_exactly_one_receipt",
    "accepted_trial_step_advances_stage",
    "apply_trial_event_stop_count_monotone",
    "accepted_trial_step_stop_count_monotone",
    "accepted_trial_run_preserves_identity",
    "accepted_trial_run_preserves_support",
    "accepted_trial_run_preserves_external_effect",
    "accepted_trial_run_accounts_exact_receipts",
    "accepted_trial_run_stop_count_monotone",
    "accepted_trial_run_has_accepted_trace",
    "trial_run_append",
    "closed_trial_state_accepts_no_event",
    "complete_trial_reaches_closed_with_receipts_and_stop",
    "missing_safety_axis_cannot_start_trial",
}

TRIAL_STAGES = [
    "proposed", "leaseBound", "independentlyReviewed", "commandStaged",
    "observationRecorded", "stopRecorded", "reconciled", "closed",
]
TRIAL_EVENTS = [
    "bindLease", "reviewLease", "stageCommand", "recordObservation",
    "recordStop", "reconcile", "close",
]
IDENTITY_KEYS = [
    "plantDigest", "leaseDigest", "controllerDigest", "estimatorDigest",
    "policyDigest", "safetyEnvelopeDigest", "actuatorDigest", "observerDigest",
    "resultDigest",
]


def trial_state(stage: str = "proposed") -> dict[str, Any]:
    state = {key: 7001 + index for index, key in enumerate(IDENTITY_KEYS)}
    state.update(stage=stage, lastEventDigest=0, receiptCount=0, stopReceiptCount=0,
                 supportAssigned=False, externalEffectCommitted=False)
    return state


def trial_packet(kind_index: int, lease: dict[str, Any] | None = None) -> dict[str, Any]:
    packet = {key: 7001 + index for index, key in enumerate(IDENTITY_KEYS)}
    packet.update(
        eventDigest=kind_index + 1,
        lease=deepcopy(lease if lease is not None else complete_lease()),
        independentReview=True,
        boundedCommand=True,
        observationReceipt=True,
        stopReceipt=True,
        residualClosure=True,
        nonClaims=True,
        supportRequested=False,
        externalEffectRequested=False,
    )
    return packet


def trial_route(state: dict[str, Any], kind: str, packet: dict[str, Any]) -> str:
    stage_index = TRIAL_STAGES.index(state["stage"])
    if state["stage"] == "closed" or kind != TRIAL_EVENTS[stage_index]:
        return "rejectWrongStage"
    if any(packet[key] != state[key] for key in IDENTITY_KEYS):
        return "rejectIdentitySubstitution"
    if packet["eventDigest"] == state["lastEventDigest"]:
        return "rejectEventReplay"
    if packet["supportRequested"] or packet["externalEffectRequested"]:
        return "rejectAuthorityLeak"
    requirements = [
        (ready(packet["lease"]), "requestLeaseRepair", "acceptLease"),
        (packet["independentReview"], "requestIndependentReview", "acceptReview"),
        (packet["boundedCommand"], "requestBoundedCommand", "acceptCommandStage"),
        (packet["observationReceipt"], "requestObservationReceipt", "acceptObservation"),
        (packet["stopReceipt"], "requestStopReceipt", "acceptStop"),
        (packet["residualClosure"], "requestResidualClosure", "acceptReconciliation"),
        (packet["nonClaims"], "requestNonClaims", "acceptClosure"),
    ]
    passed, rejected, accepted = requirements[stage_index]
    return accepted if passed else rejected


def trial_step(state: dict[str, Any], kind: str, packet: dict[str, Any]) -> dict[str, Any] | None:
    selected = trial_route(state, kind, packet)
    if not selected.startswith("accept"):
        return None
    next_state = deepcopy(state)
    next_state["stage"] = TRIAL_STAGES[TRIAL_STAGES.index(state["stage"]) + 1]
    next_state["lastEventDigest"] = packet["eventDigest"]
    next_state["receiptCount"] += 1
    if selected == "acceptStop":
        next_state["stopReceiptCount"] += 1
    return next_state


def trial_run(events: list[tuple[str, dict[str, Any]]],
              initial: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    states = [deepcopy(initial) if initial is not None else trial_state()]
    for kind, packet in events:
        next_state = trial_step(states[-1], kind, packet)
        if next_state is None:
            raise ValueError(f"trial rejected at {states[-1]['stage']}: {kind}")
        states.append(next_state)
    return states


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit(
            "Embodied physical-safety validation failed:\n"
            + "\n".join(f" - {error}" for error in errors)
        )


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE, FIXTURE):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    fail(errors)

    complete = load(FIXTURE)
    if complete != complete_lease():
        errors.append("public control-lease fixture drifted from the closed Lean witness")
    expected_routes = {axis: repair for axis, _, repair in checks(complete)}
    if not ready(complete) or route(complete) != "eligibleForTheseusClosedLoopTrial":
        errors.append("complete lease must reach only the Project Theseus closed-loop trial")
    if set(MUTATIONS) != set(expected_routes) or len(MUTATIONS) != 13:
        errors.append("mutation denominator must cover exactly 13 admission axes")
    for axis, mutate in MUTATIONS.items():
        lease = deepcopy(complete)
        mutate(lease)
        if ready(lease):
            errors.append(f"{axis} mutation remained ready")
        if route(lease) != expected_routes[axis]:
            errors.append(f"{axis} mutation reached {route(lease)}, expected {expected_routes[axis]}")

    for reduced_latency in range(complete["worstCaseLatency"] + 1):
        reduced = deepcopy(complete)
        reduced["worstCaseLatency"] = reduced_latency
        if not next(value for axis, value, _ in checks(reduced) if axis == "timingBudget"):
            errors.append(f"reduced latency {reduced_latency} invalidated a valid timing budget")
    lower_violation = deepcopy(complete)
    lower_violation["estimateLower"] = 1
    for wider_lower in range(lower_violation["estimateLower"] + 1):
        widened = deepcopy(lower_violation)
        widened["estimateLower"] = wider_lower
        if next(value for axis, value, _ in checks(widened) if axis == "stateEnvelope"):
            errors.append(f"downward-widened lower bound {wider_lower} laundered a state violation")
    fallback_violation = deepcopy(complete)
    fallback_violation["stopDistanceUpperBound"] = 6
    for larger_stop_distance in range(6, 10):
        worsened = deepcopy(fallback_violation)
        worsened["stopDistanceUpperBound"] = larger_stop_distance
        if next(value for axis, value, _ in checks(worsened) if axis == "fallbackReachability"):
            errors.append(f"larger stop-distance bound {larger_stop_distance} laundered fallback rejection")

    events = [(kind, trial_packet(index)) for index, kind in enumerate(TRIAL_EVENTS)]
    states = trial_run(events)
    final = states[-1]
    if (final["stage"], final["receiptCount"], final["stopReceiptCount"]) != ("closed", 7, 1):
        errors.append("complete simulation-trial review did not close with seven receipts and one stop")
    for state in states:
        if any(state[key] != states[0][key] for key in IDENTITY_KEYS):
            errors.append(f"identity custody failed at {state['stage']}")
        if state["supportAssigned"] or state["externalEffectCommitted"]:
            errors.append(f"non-authority failed at {state['stage']}")
    if any(states[index]["stopReceiptCount"] > states[index + 1]["stopReceiptCount"] for index in range(7)):
        errors.append("stop-receipt count decreased across an accepted transition")
    for split in range(8):
        prefix_final = trial_run(events[:split])[-1]
        composed_final = trial_run(events[split:], prefix_final)[-1]
        if composed_final != final:
            errors.append(f"trace composition failed at split {split}")

    rejected_mutations = 0
    for stage_index, state in enumerate(states[:-1]):
        kind, baseline_packet = events[stage_index]
        for key in IDENTITY_KEYS:
            packet = deepcopy(baseline_packet)
            packet[key] += 1
            rejected_mutations += trial_step(state, kind, packet) is None
        packet = deepcopy(baseline_packet)
        if stage_index == 0:
            packet["lease"] = deepcopy(complete)
            MUTATIONS["stateEnvelope"](packet["lease"])
        else:
            requirement_keys = [None, "independentReview", "boundedCommand", "observationReceipt",
                                "stopReceipt", "residualClosure", "nonClaims"]
            packet[requirement_keys[stage_index]] = False
        rejected_mutations += trial_step(state, kind, packet) is None
        wrong_kind = TRIAL_EVENTS[(stage_index + 1) % len(TRIAL_EVENTS)]
        rejected_mutations += trial_step(state, wrong_kind, deepcopy(baseline_packet)) is None
        packet = deepcopy(baseline_packet)
        packet["eventDigest"] = state["lastEventDigest"]
        rejected_mutations += trial_step(state, kind, packet) is None
        packet = deepcopy(baseline_packet)
        packet["supportRequested"] = True
        rejected_mutations += trial_step(state, kind, packet) is None
        packet = deepcopy(baseline_packet)
        packet["externalEffectRequested"] = True
        rejected_mutations += trial_step(state, kind, packet) is None
    for index, kind in enumerate(TRIAL_EVENTS):
        rejected_mutations += trial_step(final, kind, trial_packet(index)) is None
    if rejected_mutations != 105:
        errors.append(f"simulation-trial mutation rejection drifted: {rejected_mutations}/105")

    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if theorem_names != REQUIRED_THEOREMS:
        errors.append(
            f"Lean theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    if "import AsiStackProofs.EmbodiedPhysicalSafety" not in LEAN_ROOT.read_text(encoding="utf-8"):
        errors.append("root Lean module does not import EmbodiedPhysicalSafety")
    for forbidden in (
        "plantTruthEstablished",
        "physicalSafetyEstablished",
        "humanSafetyEstablished",
        "deadlineSatisfactionEstablished",
        "safeSetValidityEstablished",
        "fallbackEffectivenessEstablished",
        "supportStatePromoted",
        "externalEffectAllowed",
    ):
        if forbidden in lean_text:
            errors.append(f"forbidden overclaim surface present: {forbidden}")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or len(triage_rows) != 1:
        errors.append("proof manifest and triage must each contain exactly one target row")
    else:
        if (
            manifest_rows[0].get("module"),
            manifest_rows[0].get("formal_target"),
            manifest_rows[0].get("status"),
        ) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof manifest target binding drifted")
        if (
            triage_rows[0].get("module"),
            triage_rows[0].get("formal_target"),
            triage_rows[0].get("target_status"),
        ) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof triage target binding drifted")

    chapters = [chapter for part in load(STRUCTURE)["parts"] for chapter in part.get("chapters", [])]
    owners = [row for row in chapters if row.get("id") == "embodied-agency-real-time-control-and-physical-safety"]
    if len(owners) != 1:
        errors.append("book structure must contain exactly one owner chapter")
    elif not any(
        row.get("tag") == TAG and row.get("status") == "implemented"
        for row in owners[0].get("proof_targets", [])
    ):
        errors.append("book structure target is not implemented")

    chapter_text = CHAPTER.read_text(encoding="utf-8")
    dossier_flat = re.sub(r"\s+", " ", DOSSIER.read_text(encoding="utf-8"))
    for fragment in (
        TAG,
        "41 theorem declarations",
        "Thirteen independently checkable admission-axis mutations",
        "105/105 lifecycle mutations",
        "Chapter support remains `argument`",
        "Project Theseus closed-loop campaign",
    ):
        if fragment not in chapter_text:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in (
        "13 exact mutation routes",
        "three arithmetic monotonicity controls",
        "105 lifecycle mutations",
        "support_state_effect` remains `none",
    ):
        if fragment not in dossier_flat:
            errors.append(f"proof-model dossier missing fragment: {fragment}")
    outline_text = OUTLINE.read_text(encoding="utf-8")
    if f"| `{TAG}` | `{MODULE}` | {FORMAL_TARGET} | implemented |" not in outline_text:
        errors.append("outline target row drifted")

    fail(errors)
    print(
        "Embodied physical-safety validation passed: complete finite lease, 13/13 exact "
        "admission-axis mutations, 3 arithmetic monotonicity controls, an eight-stage "
        "simulation-trial lifecycle with 105/105 rejected mutations, and 41 exact Lean "
        "declarations; no plant-truth, physical/human-safety, deadline, safe-set, fallback-"
        "effectiveness, recovery, support, release, transfer, or external-effect claim."
    )


if __name__ == "__main__":
    main()
