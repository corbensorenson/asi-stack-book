#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "tests/fixtures/protocol_records/white_box_evidence_packet.valid.json"
PROTOCOL = ROOT / "experiments/white_box_argument_exit/preregistration.json"
LEAN = ROOT / "lean/AsiStackProofs/WhiteBoxEvidence.lean"
CHAPTER = ROOT / "chapters/white-box-evidence-interpretability-and-activation-governance.qmd"
EXPECTED_LEAN_THEOREM_COUNT = 36
EXPECTED_LIFECYCLE_EVENT_COUNT = 6
EXPECTED_LIFECYCLE_MUTATION_COUNT = 51


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def lifecycle_packet() -> dict[str, Any]:
    return {
        "exact_identity": True,
        "lineage_fresh": True,
        "method_assumptions_present": True,
        "negative_controls_passed": True,
        "behavioral_cross_check": True,
        "causal_intervention_passed": True,
        "separate_evaluator": True,
        "stability_recorded": True,
        "coverage_residual_recorded": True,
        "side_effects_resolved": True,
        "material_change_observed": False,
        "release_requested": False,
        "evidence_state": "causal_bounded",
        "requested_authority": "preserve",
    }


IDENTITY_FIELDS = (
    "packet_id", "model_id", "checkpoint_digest", "method_digest",
    "population_id", "packet_version", "packet",
)


def scientifically_admissible(packet: dict[str, Any]) -> bool:
    common = all(packet[key] for key in (
        "exact_identity", "lineage_fresh", "method_assumptions_present",
        "negative_controls_passed", "stability_recorded",
        "coverage_residual_recorded",
    ))
    if not common:
        return False
    state = packet["evidence_state"]
    if state == "observational":
        return True
    if state == "predictive":
        return packet["behavioral_cross_check"] is True
    if state == "causal_bounded":
        return all(packet[key] is True for key in (
            "behavioral_cross_check", "causal_intervention_passed",
            "separate_evaluator",
        ))
    return False


def route_for(packet: dict[str, Any]) -> str:
    if not scientifically_admissible(packet):
        return "reject"
    if packet["material_change_observed"]:
        return "expire"
    if packet["requested_authority"] == "widen" or packet["release_requested"]:
        return "escalate"
    if not packet["side_effects_resolved"]:
        return "restrict"
    return "restrict" if packet["requested_authority"] == "restrict" else "preserve"


def lifecycle_initial_state() -> dict[str, Any]:
    return {
        "packet_id": 11,
        "model_id": 22,
        "checkpoint_digest": 33,
        "method_digest": 44,
        "population_id": 55,
        "packet_version": 1,
        "packet": lifecycle_packet(),
        "authority_ceiling": 5,
        "active_authority": 3,
        "route": "reject",
        "identity_receipt": False,
        "method_receipt": False,
        "intervention_receipt": False,
        "review_receipt": False,
        "policy_receipt": False,
        "rejection_receipt": False,
        "residual_count": 0,
        "support_authority": False,
        "external_effect_authority": False,
        "stage": "raw",
        "logical_time": 0,
    }


def lifecycle_event(
    kind: str, from_stage: str, to_stage: str, logical_time: int,
    receipt: str | None = None,
) -> dict[str, Any]:
    state = lifecycle_initial_state()
    event = {
        key: copy.deepcopy(state[key]) for key in IDENTITY_FIELDS
    }
    event.update({
        "kind": kind,
        "from_stage": from_stage,
        "to_stage": to_stage,
        "requested_authority": 3,
        "route": "preserve",
        "identity_receipt": False,
        "method_receipt": False,
        "intervention_receipt": False,
        "review_receipt": False,
        "policy_receipt": False,
        "rejection_receipt": False,
        "residual_count": 0,
        "support_promotion_requested": False,
        "external_effect_requested": False,
        "logical_time": logical_time,
    })
    if receipt:
        event[receipt] = True
    return event


def lifecycle_reference_events() -> list[dict[str, Any]]:
    return [
        lifecycle_event("bind_identity", "raw", "identity_bound", 1, "identity_receipt"),
        lifecycle_event("check_method", "identity_bound", "method_checked", 2, "method_receipt"),
        lifecycle_event("check_intervention", "method_checked", "intervention_checked", 3, "intervention_receipt"),
        lifecycle_event("review_independently", "intervention_checked", "independently_reviewed", 4, "review_receipt"),
        lifecycle_event("route_policy", "independently_reviewed", "policy_routed", 5, "policy_receipt"),
        lifecycle_event("consume", "policy_routed", "consumed", 6),
    ]


def lifecycle_event_errors(state: dict[str, Any], event: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if state["stage"] != event["from_stage"]:
        out.append("stage custody failed")
    for key in IDENTITY_FIELDS:
        if state[key] != event[key]:
            out.append(f"identity custody failed: {key}")
    if state["logical_time"] >= event["logical_time"]:
        out.append("logical time did not advance")
    if event["support_promotion_requested"]:
        out.append("event requests support promotion")
    if event["external_effect_requested"]:
        out.append("event requests external effect")
    kind = event["kind"]
    if kind == "bind_identity":
        if (event["from_stage"], event["to_stage"]) != ("raw", "identity_bound"):
            out.append("identity binding stage failed")
        if not all(event[key] > 0 for key in IDENTITY_FIELDS[:-1]):
            out.append("identity binding contains zero identity")
        if not event["packet"]["exact_identity"] or not event["identity_receipt"]:
            out.append("identity binding lacks exact identity or receipt")
        if event["requested_authority"] > state["active_authority"]:
            out.append("identity binding widens authority")
    elif kind == "check_method":
        if (event["from_stage"], event["to_stage"]) != ("identity_bound", "method_checked"):
            out.append("method stage failed")
        if not all(event["packet"][key] for key in (
            "lineage_fresh", "method_assumptions_present", "negative_controls_passed",
        )) or not event["method_receipt"]:
            out.append("method boundary failed")
        if event["requested_authority"] != state["active_authority"]:
            out.append("method check changes authority")
    elif kind == "check_intervention":
        if (event["from_stage"], event["to_stage"]) != ("method_checked", "intervention_checked"):
            out.append("intervention stage failed")
        if event["packet"]["evidence_state"] != "causal_bounded" or not all(
            event["packet"][key] for key in (
                "behavioral_cross_check", "causal_intervention_passed",
            )
        ) or not event["intervention_receipt"]:
            out.append("intervention boundary failed")
        if event["requested_authority"] != state["active_authority"]:
            out.append("intervention check changes authority")
    elif kind == "review_independently":
        if (event["from_stage"], event["to_stage"]) != ("intervention_checked", "independently_reviewed"):
            out.append("review stage failed")
        if not event["packet"]["separate_evaluator"] or not event["review_receipt"]:
            out.append("independent review boundary failed")
        if event["requested_authority"] != state["active_authority"]:
            out.append("review changes authority")
    elif kind == "route_policy":
        if (event["from_stage"], event["to_stage"]) != ("independently_reviewed", "policy_routed"):
            out.append("policy route stage failed")
        if not scientifically_admissible(event["packet"]):
            out.append("inadmissible packet reached policy route")
        if event["route"] != route_for(event["packet"]) or event["route"] == "grant_widening":
            out.append("policy route launders disposition")
        if not event["policy_receipt"]:
            out.append("policy receipt missing")
        if event["requested_authority"] > state["active_authority"]:
            out.append("policy route widens authority")
    elif kind == "consume":
        if (event["from_stage"], event["to_stage"]) != ("policy_routed", "consumed"):
            out.append("consumption stage failed")
        if state["route"] not in {"preserve", "restrict"}:
            out.append("non-consumable route consumed")
        if not all(state[key] for key in (
            "identity_receipt", "method_receipt", "intervention_receipt",
            "review_receipt", "policy_receipt",
        )):
            out.append("consumption lacks complete receipts")
        if event["requested_authority"] != state["active_authority"]:
            out.append("consumption changes authority")
        if event["residual_count"] != 0:
            out.append("residual-bearing packet consumed")
    else:
        out.append("unknown lifecycle event")
    if event["residual_count"] != state["residual_count"] and kind != "consume":
        out.append("residual custody failed")
    return out


def apply_lifecycle_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    if event["kind"] == "route_policy":
        next_state["active_authority"] = min(
            state["active_authority"], event["requested_authority"]
        )
        next_state["route"] = event["route"]
    for key in (
        "identity_receipt", "method_receipt", "intervention_receipt",
        "review_receipt", "policy_receipt", "rejection_receipt",
    ):
        next_state[key] = state[key] or event[key]
    next_state["residual_count"] = event["residual_count"]
    next_state["stage"] = event["to_stage"]
    next_state["logical_time"] = event["logical_time"]
    return next_state


def run_lifecycle(
    initial: dict[str, Any], events: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    state = copy.deepcopy(initial)
    for index, event in enumerate(events):
        event_failures = lifecycle_event_errors(state, event)
        if event_failures:
            return None, [f"event {index}: {item}" for item in event_failures]
        state = apply_lifecycle_event(state, event)
    return state, []


def lifecycle_errors(container: dict[str, Any]) -> list[str]:
    initial = container["state"]
    events = container["events"]
    out: list[str] = []
    if len(events) != EXPECTED_LIFECYCLE_EVENT_COUNT:
        out.append("lifecycle event denominator drifted")
    final, run_failures = run_lifecycle(initial, events)
    out.extend(run_failures)
    if final is None:
        return out
    if final["stage"] != "consumed":
        out.append("reference lifecycle did not reach consumption")
    if final["active_authority"] > initial["active_authority"]:
        out.append("reference lifecycle widened authority")
    if final["support_authority"] or final["external_effect_authority"]:
        out.append("reference lifecycle gained support or effect authority")
    for key in IDENTITY_FIELDS:
        if final[key] != initial[key]:
            out.append(f"reference lifecycle changed identity: {key}")
    return out


def lifecycle_mutations() -> list[tuple[str, Any]]:
    mutations: list[tuple[str, Any]] = []
    for field in IDENTITY_FIELDS:
        def mutate_identity(value: dict[str, Any], key: str = field) -> None:
            value["events"][4][key] = (
                {**value["events"][4][key], "lineage_fresh": False}
                if key == "packet" else value["events"][4][key] + 1000
            )
        mutations.append((f"substitute {field}", mutate_identity))
    receipt_slots = (
        (0, "identity_receipt"), (1, "method_receipt"),
        (2, "intervention_receipt"), (3, "review_receipt"),
        (4, "policy_receipt"),
    )
    for index, field in receipt_slots:
        mutations.append((
            f"remove {field}",
            lambda value, i=index, key=field: value["events"][i].__setitem__(key, False),
        ))
    for index in range(EXPECTED_LIFECYCLE_EVENT_COUNT):
        mutations.append((
            f"wrong from-stage {index}",
            lambda value, i=index: value["events"][i].__setitem__("from_stage", "raw" if i else "consumed"),
        ))
        mutations.append((
            f"nonmonotonic time {index}",
            lambda value, i=index: value["events"][i].__setitem__("logical_time", i),
        ))
        mutations.append((
            f"support request {index}",
            lambda value, i=index: value["events"][i].__setitem__("support_promotion_requested", True),
        ))
        mutations.append((
            f"external effect request {index}",
            lambda value, i=index: value["events"][i].__setitem__("external_effect_requested", True),
        ))
    for field in (
        "exact_identity", "lineage_fresh", "method_assumptions_present",
        "negative_controls_passed", "stability_recorded",
        "coverage_residual_recorded", "behavioral_cross_check",
        "causal_intervention_passed", "separate_evaluator",
    ):
        def mutate_packet(value: dict[str, Any], key: str = field) -> None:
            value["state"]["packet"][key] = False
            for event in value["events"]:
                event["packet"][key] = False
        mutations.append((f"packet {field} false", mutate_packet))
    mutations.extend([
        ("route grant widening", lambda value: value["events"][4].__setitem__("route", "grant_widening")),
        ("route authority widening", lambda value: value["events"][4].__setitem__("requested_authority", 4)),
        ("consume with residual", lambda value: value["events"][5].__setitem__("residual_count", 1)),
        ("material change laundering", lambda value: [
            event["packet"].__setitem__("material_change_observed", True)
            for event in value["events"]
        ]),
        ("release request laundering", lambda value: [
            event["packet"].__setitem__("release_requested", True)
            for event in value["events"]
        ]),
        ("unresolved side effects laundering", lambda value: [
            event["packet"].__setitem__("side_effects_resolved", False)
            for event in value["events"]
        ]),
    ])
    return mutations


def packet_errors(packet: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if packet.get("schema_version") != "asi_stack.white_box_evidence_packet.v1":
        out.append("packet schema identity drifted")
    identity = packet.get("identity", {})
    for field in (
        "model_id", "checkpoint_digest", "tokenizer_digest", "substrate",
        "runtime_digest", "capture_site", "population_id", "captured_at",
    ):
        if not identity.get(field):
            out.append(f"packet identity missing {field}")
    method = packet.get("method", {})
    if not method.get("assumptions") or not method.get("implementation_digest") or not method.get("configuration_digest"):
        out.append("method assumptions or identity missing")
    interpretation = packet.get("interpretation", {})
    if not interpretation.get("hard_counterexamples") or not interpretation.get("alternative_hypotheses"):
        out.append("interpretation alternatives or counterexamples missing")
    causal = packet.get("causal_evidence", {})
    if not causal.get("negative_controls") or not causal.get("positive_controls"):
        out.append("positive or negative control denominator missing")
    if packet.get("disposition") == "causal_bounded":
        if causal.get("status") not in {"necessity_bounded", "sufficiency_bounded", "mediation_bounded"}:
            out.append("bounded-causal disposition launders a noncausal state")
        if not causal.get("behavioral_cross_check") or not causal.get("interventions"):
            out.append("bounded-causal disposition lacks cross-check or intervention")
        stability = packet.get("stability", {})
        if not all(stability.get(key) for key in ("held_out_prompts", "seed_variation", "transformation_tests", "checkpoint_tests")):
            out.append("bounded-causal disposition lacks stability coverage")
        if not packet.get("independence", {}).get("separate_implementation"):
            out.append("bounded-causal disposition lacks separate evaluator implementation")
    coverage = packet.get("coverage_and_residual", {})
    for field in (
        "reconstruction_ref", "dead_or_missing_objects_ref", "split_merge_ref",
        "unexplained_residual_ref", "method_disagreement_ref",
    ):
        if not coverage.get(field):
            out.append(f"coverage/residual record missing {field}")
    if coverage.get("complete_mechanism_claimed") is not False:
        out.append("packet claims a complete mechanism")
    governance = packet.get("governance", {})
    if governance.get("policy_effect") not in {"preserve", "restrict", "escalate", "reject"}:
        out.append("packet requests an unauthorized governance effect")
    if governance.get("authority_delta") not in {"none", "reduced"}:
        out.append("packet widens authority")
    if governance.get("release_authority") is not False:
        out.append("packet claims release authority")
    expiry = packet.get("expiry", {})
    if expiry.get("material_change_observed") is True:
        if packet.get("disposition") != "expired" or governance.get("policy_effect") != "reject":
            out.append("materially changed packet remains consumable")
    if packet.get("support_state_effect") != "none":
        out.append("packet claims support movement")
    non_claims = " ".join(packet.get("non_claims", [])).lower()
    for phrase in ("no model", "no feature", "support", "agi", "asi"):
        if phrase not in non_claims:
            out.append(f"packet non-claim boundary missing {phrase}")
    return out


def protocol_errors(protocol: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if protocol.get("campaign_id") != "WHITE-BOX-ARGUMENT-EXIT-01":
        out.append("campaign identity drifted")
    if protocol.get("state") != "protocol_ready_resource_isolated_not_executed":
        out.append("protocol execution state drifted")
    if protocol.get("protected_outcomes_opened") is not False:
        out.append("protected white-box outcomes were opened")
    if protocol.get("support_state_effect") != "none" or protocol.get("current_support_state") != "argument":
        out.append("protocol launders support")
    selection = protocol.get("selection_before_outcomes", {})
    if len(selection.get("behavior_candidates", [])) != 3 or len(selection.get("forbidden_selection_inputs", [])) != 5:
        out.append("prospective behavior selection or forbidden-input denominator drifted")
    methods = protocol.get("method_families", [])
    if len(methods) != 2 or len({row.get("implementation_owner") for row in methods}) != 2:
        out.append("two independently owned method families are not frozen")
    if len(protocol.get("comparators", [])) < 6:
        out.append("comparator set is incomplete")
    custody = protocol.get("data_custody", {})
    if not all(custody.get(key) for key in ("development_split", "qualification_split", "held_out_split", "transfer_split", "denominator_separation")):
        out.append("split custody is incomplete")
    if len(protocol.get("competence_gates", [])) != 7:
        out.append("seven-gate competence denominator drifted")
    if len(protocol.get("rescue_ladder", [])) != 6:
        out.append("bounded rescue ladder drifted")
    if len(protocol.get("outcomes", [])) != 9:
        out.append("joint outcome denominator drifted")
    decision = protocol.get("decision_rule", {})
    if not all(decision.get(key) for key in ("positive", "negative_exact", "inconclusive")):
        out.append("positive, exact-negative, or inconclusive rule missing")
    if not str(decision.get("maximum_negative_level", "")).startswith("N3 for the exact frozen"):
        out.append("negative inference ceiling exceeds N3 exact scope")
    resource = protocol.get("resource_and_isolation_gate", {})
    if resource.get("minimum_free_space_before_materialization_gib") != 62:
        out.append("resource isolation floor drifted")
    if resource.get("p2_reserved_storage_may_be_reclaimed") is not False or resource.get("p2_images_or_denominators_may_be_changed") is not False:
        out.append("white-box lane may displace protected P2 work")
    if len(protocol.get("artifact_contract", [])) != 9:
        out.append("claim-bearing artifact contract drifted")
    non_claims = " ".join(protocol.get("non_claims", [])).lower()
    for phrase in ("not an interpretability experiment", "no support", "agi", "asi"):
        if phrase not in non_claims:
            out.append(f"protocol non-claim boundary missing {phrase}")
    return out


def source_errors(source: str, chapter: str) -> list[str]:
    out: list[str] = []
    normalized_chapter = re.sub(r"\s+", " ", chapter)
    required_lean = (
        "def ScientificallyAdmissible",
        "def WhiteBoxRouteFor",
        "theorem evidence_never_grants_authority",
        "theorem invalid_packet_rejected",
        "theorem admitted_causal_packet_records_crosscheck_intervention_and_evaluator",
        "theorem material_change_expires_admissible_packet",
        "theorem successful_governance_run_preserves_identity",
        "theorem successful_governance_run_authority_nonincreasing",
        "theorem successful_governance_run_preserves_support_authority",
        "theorem successful_governance_run_preserves_external_effect_authority",
        "theorem successful_governance_run_has_valid_trace",
        "theorem governance_run_append",
        "theorem accepted_policy_route_requires_admissible_packet",
        "theorem accepted_policy_route_never_grants_widening",
        "theorem accepted_consumption_requires_complete_receipts",
        "theorem accepted_consumption_requires_zero_residual",
        "theorem governance_reference_trace_reaches_consumed",
        "GovernanceRoute.grantWidening",
    )
    for token in required_lean:
        if token not in source:
            out.append(f"Lean semantic surface missing {token}")
    if len(re.findall(r"(?m)^theorem ", source)) != EXPECTED_LEAN_THEOREM_COUNT:
        out.append("WhiteBoxEvidence theorem denominator drifted")
    for phrase in (
        "protocol-ready and resource-isolated, not executed",
        "record and workflow properties",
        "cannot grant execution or release authority",
        "No model-internal outcome was opened",
    ):
        if phrase not in normalized_chapter:
            out.append(f"chapter terminal boundary missing: {phrase}")
    return out


def errors(data: dict[str, Any]) -> list[str]:
    return packet_errors(data["packet"]) + protocol_errors(data["protocol"]) + source_errors(data["lean"], data["chapter"])


def main() -> None:
    data = {
        "packet": load(PACKET),
        "protocol": load(PROTOCOL),
        "lean": LEAN.read_text(encoding="utf-8"),
        "chapter": CHAPTER.read_text(encoding="utf-8"),
    }
    failures = errors(data)
    lifecycle = {
        "state": lifecycle_initial_state(),
        "events": lifecycle_reference_events(),
    }
    failures.extend(lifecycle_errors(lifecycle))
    mutations = [
        ("grant release", lambda value: value["packet"]["governance"].__setitem__("release_authority", True)),
        ("widen authority", lambda value: value["packet"]["governance"].__setitem__("authority_delta", "widened")),
        ("claim completeness", lambda value: value["packet"]["coverage_and_residual"].__setitem__("complete_mechanism_claimed", True)),
        ("erase negative controls", lambda value: value["packet"]["causal_evidence"].__setitem__("negative_controls", [])),
        ("erase alternatives", lambda value: value["packet"]["interpretation"].__setitem__("alternative_hypotheses", [])),
        ("consume stale packet", lambda value: value["packet"].__setitem__("disposition", "observed")),
        ("open protected outcomes", lambda value: value["protocol"].__setitem__("protected_outcomes_opened", True)),
        ("claim execution", lambda value: value["protocol"].__setitem__("state", "completed_positive")),
        ("delete competence gate", lambda value: value["protocol"]["competence_gates"].pop()),
        ("raise negative scope", lambda value: value["protocol"]["decision_rule"].__setitem__("maximum_negative_level", "N5 field-wide")),
        ("take P2 storage", lambda value: value["protocol"]["resource_and_isolation_gate"].__setitem__("p2_reserved_storage_may_be_reclaimed", True)),
        ("invent support", lambda value: value["protocol"].__setitem__("support_state_effect", "empirical-test-backed")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    lifecycle_mutation_set = lifecycle_mutations()
    if len(lifecycle_mutation_set) != EXPECTED_LIFECYCLE_MUTATION_COUNT:
        failures.append("lifecycle mutation denominator drifted")
    for label, mutation in lifecycle_mutation_set:
        candidate = copy.deepcopy(lifecycle)
        mutation(candidate)
        final, _ = run_lifecycle(candidate["state"], candidate["events"])
        if final is not None:
            failures.append(f"lifecycle mutation accepted: {label}")
    lean_result = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/WhiteBoxEvidence.lean"],
        cwd=ROOT / "lean", text=True, capture_output=True,
    )
    if lean_result.returncode:
        failures.append("WhiteBoxEvidence Lean check failed: " + (lean_result.stdout + lean_result.stderr).strip())
    if failures:
        raise SystemExit("White-box evidence contract failed:\n - " + "\n - ".join(failures))
    print(
        "White-box evidence contract passed: one schema fixture, two formal targets "
        f"implemented through {EXPECTED_LEAN_THEOREM_COUNT} theorem declarations, "
        f"one {EXPECTED_LIFECYCLE_EVENT_COUNT}-event independent lifecycle with "
        f"{EXPECTED_LIFECYCLE_MUTATION_COUNT}/{EXPECTED_LIFECYCLE_MUTATION_COUNT} "
        "rejected mutations, 2 independently owned method families, 7 competence "
        "gates, 6 rescue steps, 9 joint outcomes, 12 packet/protocol mutations "
        "rejected; empirical and support effects none."
    )


if __name__ == "__main__":
    main()
