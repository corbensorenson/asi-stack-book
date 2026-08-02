#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/governed_world_model_packet.schema.json"
FIXTURE = ROOT / "tests/fixtures/protocol_records/governed_world_model_packet.valid.json"
PROTOCOL = ROOT / "experiments/governed_world_model_argument_exit/preregistration.json"
LEAN = ROOT / "lean/AsiStackProofs/GovernedWorldModels.lean"
CHAPTER = ROOT / "chapters/governed-world-models-and-reality-grounding.qmd"

LIFECYCLE_NEXT = {
    "awaitingObservation": ("bindObservation", "observationBound", "acceptObservation"),
    "observationBound": ("bindModel", "modelBound", "acceptModel"),
    "modelBound": ("qualifyBranch", "branchQualified", "acceptBranch"),
    "branchQualified": ("handoffForPlanning", "planningHandoff", "acceptPlanningHandoff"),
    "planningHandoff": ("recordObservedEffect", "effectObserved", "acceptEffectObservation"),
    "effectObserved": ("reconcileResidual", "reconciled", "acceptReconciliation"),
}


def lifecycle_route(state: dict[str, Any], kind: str, packet: dict[str, Any]) -> str:
    expected = LIFECYCLE_NEXT.get(state["stage"], ("bindObservation", "observationBound", "acceptObservation"))[0]
    if kind != expected:
        return "rejectWrongStage"
    for field in (
        "modelIdentity", "modelVersion", "observationDigest", "branchDigest",
        "actionDigest", "effectDigest", "authorityCeiling",
    ):
        if state[field] != packet[field]:
            return "rejectIdentitySubstitution"
    if packet["eventDigest"] == state["lastEventDigest"]:
        return "rejectEventReplay"
    if packet["supportAssignmentRequested"] or packet["executionAuthorityRequested"]:
        return "rejectAuthorityLaundering"
    stage = state["stage"]
    if stage in {"awaitingObservation", "reconciled"}:
        if not packet["observationAdmitted"]:
            return "requestAdmittedObservation"
        if not packet["observationFresh"]:
            return "requestFreshObservation"
        if not packet["observationMarkedActual"]:
            return "rejectImaginationAsObservation"
        return "acceptObservation"
    if stage == "observationBound":
        if not packet["modelCheckpointBound"]:
            return "requestBoundModel"
        if not packet["modelCurrent"]:
            return "requestCurrentModel"
        return "acceptModel"
    if stage == "modelBound":
        if not packet["interventionSemanticsBound"]:
            return "requestInterventionSemantics"
        if not packet["horizonBound"]:
            return "requestBoundHorizon"
        if not packet["calibrationCurrent"]:
            return "requestCalibration"
        if not packet["supportQualified"]:
            return "requestQualifiedSupport"
        if packet["materialDisagreement"] and not packet["disagreementDispositionPresent"]:
            return "requestDisagreementDisposition"
        if not packet["branchDerivedFromObservation"]:
            return "requestObservationLineage"
        if not packet["branchMarkedImagined"]:
            return "requestImaginedLabel"
        return "acceptBranch"
    if stage == "branchQualified":
        return "acceptPlanningHandoff" if packet["plannerUseBounded"] else "requestBoundedPlannerUse"
    if stage == "planningHandoff":
        if not packet["actionReceiptPresent"]:
            return "requestActionReceipt"
        if not packet["effectIndependentlyObserved"]:
            return "requestIndependentEffectObservation"
        if not packet["effectMarkedActual"]:
            return "requestActualityLabel"
        return "acceptEffectObservation"
    if not packet["residualComputed"]:
        return "requestResidual"
    if packet["materialResidual"] and not packet["residualResponseSelected"]:
        return "requestResidualResponse"
    if not packet["residualOwnerPresent"]:
        return "requestResidualOwner"
    return "acceptReconciliation"


def canonical_lifecycle_packet(event_digest: int) -> dict[str, Any]:
    return {
        "modelIdentity": 401, "modelVersion": 7, "observationDigest": 402,
        "branchDigest": 403, "actionDigest": 404, "effectDigest": 405,
        "authorityCeiling": 2, "eventDigest": event_digest,
        "observationAdmitted": True, "observationFresh": True,
        "observationMarkedActual": True, "modelCheckpointBound": True,
        "modelCurrent": True, "interventionSemanticsBound": True,
        "horizonBound": True, "calibrationCurrent": True, "supportQualified": True,
        "materialDisagreement": False, "disagreementDispositionPresent": True,
        "branchDerivedFromObservation": True, "branchMarkedImagined": True,
        "plannerUseBounded": True, "actionReceiptPresent": True,
        "effectIndependentlyObserved": True, "effectMarkedActual": True,
        "residualComputed": True, "materialResidual": True,
        "residualResponseSelected": True, "residualOwnerPresent": True,
        "supportAssignmentRequested": False, "executionAuthorityRequested": False,
    }


def lifecycle_checks() -> list[str]:
    failures: list[str] = []
    state = {
        "stage": "awaitingObservation", "modelIdentity": 401, "modelVersion": 7,
        "observationDigest": 402, "branchDigest": 403, "actionDigest": 404,
        "effectDigest": 405, "authorityCeiling": 2, "lastEventDigest": 0,
        "receiptCount": 0, "planningHandoffCount": 0, "observedEffectCount": 0,
        "reconciliationCount": 0, "supportAssignmentCount": 0, "effectAuthorityCount": 0,
    }
    stages: list[dict[str, Any]] = [copy.deepcopy(state)]
    events = [
        "bindObservation", "bindModel", "qualifyBranch", "handoffForPlanning",
        "recordObservedEffect", "reconcileResidual",
    ]
    for digest, kind in enumerate(events, start=1):
        packet = canonical_lifecycle_packet(digest)
        route = lifecycle_route(state, kind, packet)
        expected_kind, next_stage, expected_route = LIFECYCLE_NEXT[state["stage"]]
        if kind != expected_kind or route != expected_route:
            failures.append(f"lifecycle event {kind} routed {route}, expected {expected_route}")
            break
        state = copy.deepcopy(state)
        state["stage"] = next_stage
        state["lastEventDigest"] = digest
        state["receiptCount"] += 1
        state["planningHandoffCount"] += kind == "handoffForPlanning"
        state["observedEffectCount"] += kind == "recordObservedEffect"
        state["reconciliationCount"] += kind == "reconcileResidual"
        stages.append(copy.deepcopy(state))
    expected_final = {
        "stage": "reconciled", "receiptCount": 6, "planningHandoffCount": 1,
        "observedEffectCount": 1, "reconciliationCount": 1,
        "supportAssignmentCount": 0, "effectAuthorityCount": 0, "authorityCeiling": 2,
    }
    for field, expected in expected_final.items():
        if state.get(field) != expected:
            failures.append(f"lifecycle final {field} was {state.get(field)!r}, expected {expected!r}")

    mutations = [
        (0, "bindObservation", "observationFresh", False, "requestFreshObservation"),
        (0, "bindObservation", "observationMarkedActual", False, "rejectImaginationAsObservation"),
        (1, "bindModel", "modelCurrent", False, "requestCurrentModel"),
        (2, "qualifyBranch", "supportQualified", False, "requestQualifiedSupport"),
        (2, "qualifyBranch", "branchMarkedImagined", False, "requestImaginedLabel"),
        (3, "handoffForPlanning", "plannerUseBounded", False, "requestBoundedPlannerUse"),
        (3, "handoffForPlanning", "executionAuthorityRequested", True, "rejectAuthorityLaundering"),
        (4, "recordObservedEffect", "actionReceiptPresent", False, "requestActionReceipt"),
        (4, "recordObservedEffect", "effectIndependentlyObserved", False, "requestIndependentEffectObservation"),
        (5, "reconcileResidual", "residualComputed", False, "requestResidual"),
        (5, "reconcileResidual", "residualOwnerPresent", False, "requestResidualOwner"),
    ]
    for stage_index, kind, field, value, expected in mutations:
        packet = canonical_lifecycle_packet(stage_index + 1)
        packet[field] = value
        route = lifecycle_route(stages[stage_index], kind, packet)
        if route != expected:
            failures.append(f"lifecycle mutation {field} routed {route}, expected {expected}")
    return failures


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    schema = data["schema"]
    fixture = data["fixture"]
    protocol = data["protocol"]
    lean_text = data["lean_text"]
    chapter = data["chapter"]
    schema_errors = sorted(Draft202012Validator(schema).iter_errors(fixture), key=lambda error: list(error.path))
    out.extend(f"fixture schema: {'.'.join(map(str, error.path))}: {error.message}" for error in schema_errors)
    if fixture.get("origin_class") != "repository_fixture" or fixture.get("disposition") != "safe_hold":
        out.append("fixture must remain a safe-hold record-shape fixture")
    model = fixture.get("model_identity", {})
    observation = fixture.get("observation_basis", {})
    prediction = fixture.get("prediction", {})
    disagreement = fixture.get("calibration_and_disagreement", {})
    admission = fixture.get("planner_admission", {})
    authority = fixture.get("authority_boundary", {})
    residual = fixture.get("residual_and_lifecycle", {})
    if model.get("current_version") is not False or observation.get("fresh") is not False:
        out.append("fixture must retain stale model and observation predicates")
    if prediction.get("support_ceiling") != "unsupported" or disagreement.get("material_disagreement") is not True:
        out.append("fixture must remain unsupported with material disagreement")
    if admission.get("decision") != "safe_hold" or admission.get("accepted_uses") != []:
        out.append("fixture planner disposition must remain no-use safe hold")
    if authority != {
        "authority_ceiling_ref": "fixture://no-effect-authority",
        "authority_delta": "none",
        "effect_authorized": False,
        "release_authority": False,
        "reversibility_ref": "fixture://no-effect-to-reverse",
    }:
        out.append("fixture authority boundary drifted")
    if residual.get("material_residual") is not True or residual.get("required_route") != "safe_hold":
        out.append("material fixture residual must route to safe hold")
    if fixture.get("support_state_effect") != "none" or len(fixture.get("non_claims", [])) < 2:
        out.append("fixture support or non-claim boundary drifted")

    if protocol.get("state") != "protocol_ready_resource_isolated_not_executed":
        out.append("claim-bearing protocol state drifted")
    if protocol.get("protected_outcomes_opened") is not False or protocol.get("support_state_effect") != "none":
        out.append("protocol opened outcomes or invented support")
    if len(protocol.get("arms", [])) != 6:
        out.append("protocol must retain six prospectively matched arms")
    if len(protocol.get("competence_gates", [])) != 8 or len(protocol.get("rescue_ladder", [])) != 7:
        out.append("protocol competence or rescue denominator drifted")
    if len(protocol.get("outcomes", [])) != 10 or len(protocol.get("causal_ablations", [])) != 6:
        out.append("protocol outcome or ablation denominator drifted")
    decision = protocol.get("decision_rule", {})
    if not str(decision.get("maximum_negative_level", "")).startswith("N3"):
        out.append("protocol exact negative ceiling drifted")
    isolation = protocol.get("resource_and_isolation_gate", {})
    if isolation.get("p2_reserved_storage_may_be_reclaimed") is not False or isolation.get("p2_images_or_denominators_may_be_changed") is not False:
        out.append("protocol violates P2 resource or denominator isolation")
    predecessor = protocol.get("predecessor_evidence_boundary", {})
    if predecessor.get("disposition") != "adjacent_bounded_synthetic_evidence_only" or "does not establish this chapter core" not in predecessor.get("prohibited_transfer", ""):
        out.append("P4/M8 predecessor support boundary drifted")

    if len(re.findall(r"(?m)^theorem ", lean_text)) != 32:
        out.append("GovernedWorldModels theorem denominator drifted")
    for theorem in (
        "unsupported_rollout_no_authority",
        "reality_residual_forces_route",
        "rollout_never_authorizes_effect",
        "material_residual_selects_bounded_response",
        "complete_world_model_lifecycle_reconciles_without_authority",
        "successful_lifecycle_run_preserves_identity",
        "successful_lifecycle_run_preserves_non_authority",
        "successful_lifecycle_run_preserves_authority_ceiling",
        "accepted_effect_record_requires_independent_actuality",
    ):
        if f"theorem {theorem}" not in lean_text:
            out.append(f"Lean theorem missing: {theorem}")
    for phrase in (
        "Why this boundary earns a chapter",
        "integrate at argument support",
        "protocol-ready and resource-isolated, not executed",
        "governed_world_model_packet.schema.json",
        "AsiStackProofs.GovernedWorldModels",
        "does not establish the chapter core",
    ):
        if phrase not in chapter:
            out.append(f"chapter contract phrase missing: {phrase}")
    return out


def main() -> None:
    data = {
        "schema": load(SCHEMA),
        "fixture": load(FIXTURE),
        "protocol": load(PROTOCOL),
        "lean_text": LEAN.read_text(encoding="utf-8"),
        "chapter": CHAPTER.read_text(encoding="utf-8"),
    }
    failures = errors(data) + lifecycle_checks()
    mutations = [
        ("authorize effect", lambda d: d["fixture"]["authority_boundary"].__setitem__("effect_authorized", True)),
        ("grant release", lambda d: d["fixture"]["authority_boundary"].__setitem__("release_authority", True)),
        ("freshness laundering", lambda d: d["fixture"]["observation_basis"].__setitem__("fresh", True)),
        ("support laundering", lambda d: d["fixture"].__setitem__("support_state_effect", "synthetic-test-backed")),
        ("admit unsupported fixture", lambda d: d["fixture"]["planner_admission"].__setitem__("decision", "admit")),
        ("erase residual", lambda d: d["fixture"]["residual_and_lifecycle"].__setitem__("material_residual", False)),
        ("open outcomes", lambda d: d["protocol"].__setitem__("protected_outcomes_opened", True)),
        ("drop competence gate", lambda d: d["protocol"]["competence_gates"].pop()),
        ("drop baseline", lambda d: d["protocol"]["arms"].pop(0)),
        ("inflate negative", lambda d: d["protocol"]["decision_rule"].__setitem__("maximum_negative_level", "N5 architecture-general")),
        ("borrow predecessor", lambda d: d["protocol"]["predecessor_evidence_boundary"].__setitem__("disposition", "chapter_core_evidence")),
        ("allow P2 displacement", lambda d: d["protocol"]["resource_and_isolation_gate"].__setitem__("p2_reserved_storage_may_be_reclaimed", True)),
        ("erase formal ceiling", lambda d: d.__setitem__("chapter", d["chapter"].replace("does not establish the chapter core", "proves the chapter core"))),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    lean = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/GovernedWorldModels.lean"],
        cwd=ROOT / "lean", text=True, capture_output=True,
    )
    if lean.returncode:
        failures.append("GovernedWorldModels Lean compile failed: " + (lean.stdout + lean.stderr).strip())
    if failures:
        raise SystemExit("Governed world-model contract failed:\n - " + "\n - ".join(failures))
    print(
        "Governed world-model contract passed: one safe-hold record fixture, two public "
        "targets through 32 theorem declarations, one six-event transaction lifecycle, "
        "11 lifecycle rejections, 6 matched arms, 8 competence gates, 7 rescue steps, "
        "10 outcomes, 6 causal ablations, 13 fixture/protocol mutations rejected; "
        "protected outcomes closed and support/effect authority none."
    )


if __name__ == "__main__":
    main()
