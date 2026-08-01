#!/usr/bin/env python3
"""Validate the learned-objective non-identification and integrity lifecycle contract."""

from __future__ import annotations

import copy
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/LearnedObjectiveIntegrity.lean"
CHAPTER = ROOT / "chapters/inner-alignment-mesa-optimization-and-learned-objective-integrity.qmd"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/inner-alignment-mesa-optimization-and-learned-objective-integrity.md"

STAGES = [
    "scoped", "hypotheses_bound", "evidence_bound", "intervention_reviewed",
    "mitigation_reviewed", "use_bound", "handed_off", "invalidated",
]
EVENTS = [
    "register_hypotheses", "bind_evidence", "review_interventions",
    "review_mitigation", "bind_use", "handoff_for_readiness",
    "invalidate_for_change",
]
ACCEPTED = {
    "accept_hypotheses", "accept_evidence", "accept_intervention_review",
    "accept_mitigation_review", "accept_use_binding", "accept_handoff",
    "accept_invalidation",
}
IDENTITY_FIELDS = [
    "record_digest", "model_digest", "checkpoint_digest", "outer_target_digest",
    "signal_lineage_digest", "hypothesis_set_digest", "evidence_plan_digest",
    "use_envelope_digest", "reviewer_digest", "consumer_digest",
    "residual_digest", "protocol_version", "hypothesis_count",
    "unresolved_hypothesis_count",
]
THEOREMS = [
    "equal_trace_distinct_objectives_not_both_identified",
    "compliant_trace_has_distinct_objective_witness",
    "compliant_behavior_alone_cannot_identify_both_worlds",
    "separating_opportunity_distinguishes_the_witness",
    "rejected_event_preserves_exact_state",
    "apply_event_preserves_identity",
    "apply_event_cannot_assign_support_or_external_authority",
    "accepted_event_adds_one_receipt",
    "behavior_only_evidence_does_not_bind_integrity",
    "objective_identity_overclaim_is_rejected",
    "absence_of_deception_overclaim_is_rejected",
    "unresolved_hypothesis_is_required_for_bounded_use",
    "stale_descendants_block_invalidation",
    "full_integrity_lifecycle_reaches_invalidated_state",
]


def canonical_packet(event_digest: int = 1) -> dict:
    packet = {field: 700 + index for index, field in enumerate(IDENTITY_FIELDS, 1)}
    packet.update({
        "protocol_version": 1,
        "hypothesis_count": 2,
        "unresolved_hypothesis_count": 1,
        "event_digest": event_digest,
        "outer_target_present": True,
        "signal_lineage_present": True,
        "distinct_hypotheses_recorded": True,
        "competence_control_passed": True,
        "behavioral_evidence_present": True,
        "training_process_evidence_present": True,
        "causal_evidence_present": True,
        "white_box_evidence_present": True,
        "independent_evaluator": True,
        "intervention_sealed": True,
        "distribution_shift_tested": True,
        "opportunity_relevant": True,
        "conditional_positive_control_passed": True,
        "monitor_independent": True,
        "monitor_disagreement_recorded": True,
        "separation_outcome_recorded": True,
        "mitigation_outcome_recorded": True,
        "concealment_tested": True,
        "capability_damage_tested": True,
        "mitigation_residual_recorded": True,
        "authority_bounded": True,
        "expiry_present": True,
        "rollback_present": True,
        "descendant_custody_present": True,
        "residual_owner_present": True,
        "independent_review": True,
        "maximum_inference_present": True,
        "material_change_recorded": True,
        "descendants_invalidated": True,
        "ordinary_route_blocked": True,
        "rereview_route_present": True,
        "objective_identity_asserted": False,
        "absence_of_deception_asserted": False,
        "support_assignment_requested": False,
        "external_authority_requested": False,
    })
    return packet


def canonical_state(stage: str) -> dict:
    packet = canonical_packet()
    state = {field: packet[field] for field in IDENTITY_FIELDS}
    state.update({
        "stage": stage,
        "last_event_digest": 0,
        "receipt_count": 0,
        "handoff_count": 0,
        "invalidation_count": 0,
        "support_assignment_count": 0,
        "external_authority_count": 0,
    })
    return state


def route_for(state: dict, event: str, packet: dict) -> str:
    stage = state["stage"]
    expected = EVENTS[STAGES.index(stage)] if stage != "invalidated" else "invalidate_for_change"
    if event != expected:
        return "reject_wrong_stage"
    if any(packet[field] != state[field] for field in IDENTITY_FIELDS):
        return "reject_identity_substitution"
    if packet["event_digest"] == state["last_event_digest"]:
        return "reject_replay"
    if packet["support_assignment_requested"] or packet["external_authority_requested"]:
        return "reject_authority_leak"
    if packet["objective_identity_asserted"] or packet["absence_of_deception_asserted"]:
        return "reject_objective_certainty"
    if stage == "scoped":
        if not packet["outer_target_present"]: return "request_outer_target"
        if not packet["signal_lineage_present"]: return "request_signal_lineage"
        if packet["hypothesis_count"] < 2: return "request_plural_hypotheses"
        if not packet["distinct_hypotheses_recorded"]: return "request_distinct_hypotheses"
        return "accept_hypotheses"
    if stage == "hypotheses_bound":
        checks = [
            ("competence_control_passed", "request_competence_control"),
            ("behavioral_evidence_present", "request_behavioral_evidence"),
            ("training_process_evidence_present", "request_training_process_evidence"),
            ("causal_evidence_present", "request_causal_evidence"),
            ("white_box_evidence_present", "request_white_box_evidence"),
            ("independent_evaluator", "request_independent_evaluator"),
        ]
    elif stage == "evidence_bound":
        checks = [
            ("intervention_sealed", "request_sealed_intervention"),
            ("distribution_shift_tested", "request_distribution_shift"),
            ("opportunity_relevant", "request_relevant_opportunity"),
            ("conditional_positive_control_passed", "request_conditional_positive_control"),
            ("monitor_independent", "request_independent_monitor"),
            ("monitor_disagreement_recorded", "request_monitor_disagreement"),
            ("separation_outcome_recorded", "request_separation_outcome"),
        ]
    elif stage == "intervention_reviewed":
        checks = [
            ("mitigation_outcome_recorded", "request_mitigation_outcome"),
            ("concealment_tested", "request_concealment_test"),
            ("capability_damage_tested", "request_capability_damage_test"),
            ("mitigation_residual_recorded", "request_mitigation_residual"),
        ]
    elif stage == "mitigation_reviewed":
        if packet["unresolved_hypothesis_count"] == 0:
            return "request_residual_hypothesis"
        checks = [
            ("authority_bounded", "request_bounded_authority"),
            ("expiry_present", "request_expiry"),
            ("rollback_present", "request_rollback"),
            ("descendant_custody_present", "request_descendant_custody"),
            ("residual_owner_present", "request_residual_owner"),
        ]
    elif stage == "use_bound":
        checks = [
            ("independent_review", "request_independent_review"),
            ("maximum_inference_present", "request_maximum_inference"),
        ]
    elif stage == "handed_off":
        checks = [
            ("material_change_recorded", "request_material_change"),
            ("descendants_invalidated", "request_descendant_invalidation"),
            ("ordinary_route_blocked", "request_ordinary_route_block"),
            ("rereview_route_present", "request_rereview_route"),
        ]
    else:
        return "reject_wrong_stage"
    for field, rejection in checks:
        if not packet[field]:
            return rejection
    return {
        "hypotheses_bound": "accept_evidence",
        "evidence_bound": "accept_intervention_review",
        "intervention_reviewed": "accept_mitigation_review",
        "mitigation_reviewed": "accept_use_binding",
        "use_bound": "accept_handoff",
        "handed_off": "accept_invalidation",
    }[stage]


def apply_event(state: dict, event: str, packet: dict) -> tuple[dict, str]:
    route = route_for(state, event, packet)
    if route not in ACCEPTED:
        return copy.deepcopy(state), route
    result = copy.deepcopy(state)
    result["stage"] = STAGES[STAGES.index(state["stage"]) + 1]
    result["last_event_digest"] = packet["event_digest"]
    result["receipt_count"] += 1
    result["handoff_count"] += route == "accept_handoff"
    result["invalidation_count"] += route == "accept_invalidation"
    return result, route


def mutation_cases() -> list[tuple[str, dict, str, dict, str]]:
    cases = []
    accepted_stages = STAGES[:-1]
    for index, stage in enumerate(accepted_stages):
        wrong_event = EVENTS[(index + 1) % len(EVENTS)]
        cases.append((f"wrong_stage:{stage}", canonical_state(stage), wrong_event,
                      canonical_packet(index + 1), "reject_wrong_stage"))
    for field in IDENTITY_FIELDS:
        packet = canonical_packet()
        packet[field] += 1
        cases.append((f"identity:{field}", canonical_state("scoped"), EVENTS[0], packet,
                      "reject_identity_substitution"))
    replay = canonical_packet(0)
    cases.append(("replay", canonical_state("scoped"), EVENTS[0], replay, "reject_replay"))
    for field, expected in [
        ("support_assignment_requested", "reject_authority_leak"),
        ("external_authority_requested", "reject_authority_leak"),
        ("objective_identity_asserted", "reject_objective_certainty"),
        ("absence_of_deception_asserted", "reject_objective_certainty"),
    ]:
        packet = canonical_packet(); packet[field] = True
        cases.append((field, canonical_state("scoped"), EVENTS[0], packet, expected))
    stage_checks = {
        "scoped": [
            ("outer_target_present", "request_outer_target"),
            ("signal_lineage_present", "request_signal_lineage"),
            ("distinct_hypotheses_recorded", "request_distinct_hypotheses"),
        ],
        "hypotheses_bound": [
            ("competence_control_passed", "request_competence_control"),
            ("behavioral_evidence_present", "request_behavioral_evidence"),
            ("training_process_evidence_present", "request_training_process_evidence"),
            ("causal_evidence_present", "request_causal_evidence"),
            ("white_box_evidence_present", "request_white_box_evidence"),
            ("independent_evaluator", "request_independent_evaluator"),
        ],
        "evidence_bound": [
            ("intervention_sealed", "request_sealed_intervention"),
            ("distribution_shift_tested", "request_distribution_shift"),
            ("opportunity_relevant", "request_relevant_opportunity"),
            ("conditional_positive_control_passed", "request_conditional_positive_control"),
            ("monitor_independent", "request_independent_monitor"),
            ("monitor_disagreement_recorded", "request_monitor_disagreement"),
            ("separation_outcome_recorded", "request_separation_outcome"),
        ],
        "intervention_reviewed": [
            ("mitigation_outcome_recorded", "request_mitigation_outcome"),
            ("concealment_tested", "request_concealment_test"),
            ("capability_damage_tested", "request_capability_damage_test"),
            ("mitigation_residual_recorded", "request_mitigation_residual"),
        ],
        "mitigation_reviewed": [
            ("authority_bounded", "request_bounded_authority"),
            ("expiry_present", "request_expiry"),
            ("rollback_present", "request_rollback"),
            ("descendant_custody_present", "request_descendant_custody"),
            ("residual_owner_present", "request_residual_owner"),
        ],
        "use_bound": [
            ("independent_review", "request_independent_review"),
            ("maximum_inference_present", "request_maximum_inference"),
        ],
        "handed_off": [
            ("material_change_recorded", "request_material_change"),
            ("descendants_invalidated", "request_descendant_invalidation"),
            ("ordinary_route_blocked", "request_ordinary_route_block"),
            ("rereview_route_present", "request_rereview_route"),
        ],
    }
    for stage, checks in stage_checks.items():
        event = EVENTS[STAGES.index(stage)]
        for field, expected in checks:
            packet = canonical_packet(); packet[field] = False
            cases.append((f"{stage}:{field}", canonical_state(stage), event, packet, expected))
    state = canonical_state("scoped"); state["hypothesis_count"] = 1
    packet = canonical_packet(); packet["hypothesis_count"] = 1
    cases.append(("plural_hypotheses", state, EVENTS[0], packet, "request_plural_hypotheses"))
    state = canonical_state("mitigation_reviewed"); state["unresolved_hypothesis_count"] = 0
    packet = canonical_packet(); packet["unresolved_hypothesis_count"] = 0
    cases.append(("residual_hypothesis", state, EVENTS[4], packet, "request_residual_hypothesis"))
    return cases


def main() -> None:
    failures = []
    lean_text = LEAN.read_text(encoding="utf-8")
    declarations = re.findall(r"(?m)^theorem\s+([A-Za-z0-9_]+)", lean_text)
    if declarations != THEOREMS:
        failures.append(f"Lean theorem surface drifted: {declarations}")
    if "support remains `argument`" not in CHAPTER.read_text(encoding="utf-8"):
        failures.append("chapter no-support boundary is missing")
    if not DOSSIER.is_file():
        failures.append("proof-model dossier is missing")

    trace = ("comply", "comply", "comply")
    worlds = [("intended", trace, "comply"), ("shortcut", trace, "exploit")]
    if worlds[0][1] != worlds[1][1] or worlds[0][0] == worlds[1][0]:
        failures.append("non-identification witness is malformed")
    for inferred in ("intended", "shortcut", "conditional"):
        if inferred == worlds[0][0] and inferred == worlds[1][0]:
            failures.append("one trace inference identified both distinct objectives")
    if worlds[0][2] == worlds[1][2]:
        failures.append("separating opportunity does not distinguish witness worlds")

    state = canonical_state("scoped")
    observed_routes = []
    for index, event in enumerate(EVENTS, 1):
        state, route = apply_event(state, event, canonical_packet(index))
        observed_routes.append(route)
    if state["stage"] != "invalidated" or state["receipt_count"] != 7:
        failures.append("complete lifecycle did not reach invalidated with seven receipts")
    if state["handoff_count"] != 1 or state["invalidation_count"] != 1:
        failures.append("handoff/invalidation accounting drifted")
    if state["support_assignment_count"] != 0 or state["external_authority_count"] != 0:
        failures.append("accepted lifecycle minted support or external authority")
    if observed_routes != [
        "accept_hypotheses", "accept_evidence", "accept_intervention_review",
        "accept_mitigation_review", "accept_use_binding", "accept_handoff",
        "accept_invalidation",
    ]:
        failures.append(f"accepted route sequence drifted: {observed_routes}")

    cases = mutation_cases()
    escaped = []
    for label, before, event, packet, expected in cases:
        after, route = apply_event(before, event, packet)
        if route != expected or after != before or route in ACCEPTED:
            escaped.append(f"{label}:{route}:{expected}")
    if escaped:
        failures.append("mutations escaped exact rejection: " + ", ".join(escaped))
    if len(cases) != 59:
        failures.append(f"mutation denominator drifted: {len(cases)}")

    if failures:
        raise SystemExit("Learned-objective integrity validation failed:\n - " + "\n - ".join(failures))
    print(
        "Learned-objective integrity passed: two equal compliant traces with distinct "
        "objective hypotheses and separating opportunity, 8 stages, 7 accepted transitions, "
        f"{len(cases)}/{len(cases)} exact-state rejecting mutations, 14 Lean declarations, "
        "no support or external-authority effect."
    )


if __name__ == "__main__":
    main()
