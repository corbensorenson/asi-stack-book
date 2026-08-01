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
    "fail readiness and reach exact repair routes. Monotonicity laws preserve valid timing under "
    "reduced latency and preserve state or fallback rejection under worsened bounds. It establishes "
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
}


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
        "22 theorem declarations",
        "Thirteen independently checkable admission-axis mutations",
        "Chapter support remains `argument`",
        "Project Theseus closed-loop campaign",
    ):
        if fragment not in chapter_text:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in (
        "13 exact mutation routes",
        "three arithmetic monotonicity controls",
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
        "admission-axis mutations, 3 arithmetic monotonicity controls, and 22 exact Lean "
        "declarations; no plant-truth, physical/human-safety, deadline, safe-set, fallback-"
        "effectiveness, recovery, support, release, transfer, or external-effect claim."
    )


if __name__ == "__main__":
    main()
