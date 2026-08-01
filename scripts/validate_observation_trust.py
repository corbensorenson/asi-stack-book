#!/usr/bin/env python3
"""Validate correlated-evidence non-promotion and observation custody."""

from __future__ import annotations

import copy
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ObservationTrust.lean"
CHAPTER = ROOT / "chapters/perception-sensor-fusion-and-observation-trust.qmd"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/perception-sensor-fusion-and-observation-trust.md"

STAGES = [
    "captured", "identities_bound", "dependence_bound", "pair_reviewed",
    "use_bound", "handed_off", "invalidated",
]
EVENTS = [
    "bind_identities", "bind_dependence", "review_pair", "bind_use",
    "handoff_observation", "invalidate_for_change",
]
ACCEPTED = {
    "accept_identities", "accept_dependence", "accept_pair_review",
    "accept_use_binding", "accept_handoff", "accept_invalidation",
}
IDENTITY_FIELDS = [
    "observation_digest", "channel_set_digest", "calibration_digest",
    "clock_pose_digest", "dependence_digest", "hypothesis_digest",
    "consumer_digest", "residual_digest", "protocol_version",
    "pair_disposition", "computed_independent_count",
    "requested_independent_count",
]
THEOREMS = [
    "eligible_agreement_with_same_root_is_correlated",
    "declared_same_root_agreement_counts_one",
    "eligible_agreement_with_distinct_roots_is_independent",
    "eligible_disagreement_is_preserved",
    "correlated_pair_witness_counts_one_independent_item",
    "independent_pair_witness_counts_two_independent_items",
    "disagreement_witness_is_not_collapsed_into_agreement",
    "rejected_event_preserves_exact_state",
    "apply_event_preserves_observation_identity",
    "apply_event_cannot_assign_support_or_external_authority",
    "inflated_correlated_evidence_is_rejected",
    "correlated_pair_cannot_satisfy_two_item_use_request",
    "erased_disagreement_blocks_pair_review",
    "environmental_truth_overclaim_is_rejected",
    "stale_descendants_block_invalidation",
    "full_observation_lifecycle_reaches_invalidated_state",
]


def channel(root: int = 7, hypothesis: str = "obstacle") -> dict:
    return {
        "root": root,
        "hypothesis": hypothesis,
        "fresh": True,
        "calibrated": True,
        "lineage_present": True,
        "clock_pose_aligned": True,
    }


def usable(item: dict) -> bool:
    return all(item[field] for field in (
        "fresh", "calibrated", "lineage_present", "clock_pose_aligned"
    ))


def classify(left: dict, right: dict) -> str:
    if not usable(left) or not usable(right):
        return "inadmissible"
    if left["hypothesis"] != right["hypothesis"]:
        return "disagreement"
    if left["root"] == right["root"]:
        return "correlated_agreement"
    return "independent_agreement"


def evidence_count(disposition: str) -> int:
    return {
        "inadmissible": 0,
        "disagreement": 0,
        "correlated_agreement": 1,
        "independent_agreement": 2,
    }[disposition]


def canonical_packet(event_digest: int = 1) -> dict:
    packet = {
        "observation_digest": 801,
        "channel_set_digest": 802,
        "calibration_digest": 803,
        "clock_pose_digest": 804,
        "dependence_digest": 805,
        "hypothesis_digest": 806,
        "consumer_digest": 807,
        "residual_digest": 808,
        "protocol_version": 1,
        "event_digest": event_digest,
        "pair_disposition": "correlated_agreement",
        "computed_independent_count": 1,
        "requested_independent_count": 1,
        "sensor_identity_present": True,
        "calibration_present": True,
        "clock_pose_present": True,
        "lineage_present": True,
        "fresh": True,
        "dependence_roots_declared": True,
        "common_cause_reviewed": True,
        "pair_classification_present": True,
        "evidence_count_matches_classification": True,
        "disagreement_preserved": True,
        "authority_bounded": True,
        "expiry_present": True,
        "fallback_present": True,
        "residual_owner_present": True,
        "consumer_present": True,
        "maximum_inference_present": True,
        "independent_review": True,
        "material_change_recorded": True,
        "descendants_invalidated": True,
        "ordinary_route_blocked": True,
        "rereview_route_present": True,
        "environmental_truth_asserted": False,
        "independence_beyond_model_asserted": False,
        "support_assignment_requested": False,
        "external_authority_requested": False,
    }
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
    expected = EVENTS[STAGES.index(stage)] if stage != "invalidated" else EVENTS[-1]
    if event != expected:
        return "reject_wrong_stage"
    if any(packet[field] != state[field] for field in IDENTITY_FIELDS):
        return "reject_identity_substitution"
    if packet["event_digest"] == state["last_event_digest"]:
        return "reject_replay"
    if packet["support_assignment_requested"] or packet["external_authority_requested"]:
        return "reject_authority_leak"
    if packet["environmental_truth_asserted"] or packet["independence_beyond_model_asserted"]:
        return "reject_truth_overclaim"
    if stage == "captured":
        checks = [
            ("sensor_identity_present", "request_sensor_identity"),
            ("calibration_present", "request_calibration"),
            ("clock_pose_present", "request_clock_pose"),
            ("lineage_present", "request_lineage"),
            ("fresh", "request_freshness"),
        ]
    elif stage == "identities_bound":
        checks = [
            ("dependence_roots_declared", "request_dependence_roots"),
            ("common_cause_reviewed", "request_common_cause_review"),
        ]
    elif stage == "dependence_bound":
        if not packet["pair_classification_present"]:
            return "request_pair_classification"
        if not packet["evidence_count_matches_classification"]:
            return "request_evidence_count_match"
        if (packet["pair_disposition"] == "correlated_agreement"
                and packet["computed_independent_count"] > 1):
            return "reject_correlated_inflation"
        if (packet["pair_disposition"] == "disagreement"
                and not packet["disagreement_preserved"]):
            return "request_disagreement_preservation"
        return "accept_pair_review"
    elif stage == "pair_reviewed":
        if packet["requested_independent_count"] > packet["computed_independent_count"]:
            return "reject_correlated_inflation"
        checks = [
            ("authority_bounded", "request_bounded_authority"),
            ("expiry_present", "request_expiry"),
            ("fallback_present", "request_fallback"),
            ("residual_owner_present", "request_residual_owner"),
        ]
    elif stage == "use_bound":
        checks = [
            ("consumer_present", "request_consumer"),
            ("maximum_inference_present", "request_maximum_inference"),
            ("independent_review", "request_independent_review"),
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
        "captured": "accept_identities",
        "identities_bound": "accept_dependence",
        "pair_reviewed": "accept_use_binding",
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


def lifecycle_mutations() -> list[tuple[str, dict, str, dict, str]]:
    cases = []
    for index, stage in enumerate(STAGES[:-1]):
        wrong = EVENTS[(index + 1) % len(EVENTS)]
        cases.append((f"wrong_stage:{stage}", canonical_state(stage), wrong,
                      canonical_packet(index + 1), "reject_wrong_stage"))
    for field in IDENTITY_FIELDS:
        state = canonical_state("captured")
        packet = canonical_packet()
        if isinstance(packet[field], int):
            packet[field] += 1
        else:
            packet[field] = "independent_agreement"
        cases.append((f"identity:{field}", state, EVENTS[0], packet,
                      "reject_identity_substitution"))
    cases.append(("replay", canonical_state("captured"), EVENTS[0],
                  canonical_packet(0), "reject_replay"))
    for field, expected in [
        ("support_assignment_requested", "reject_authority_leak"),
        ("external_authority_requested", "reject_authority_leak"),
        ("environmental_truth_asserted", "reject_truth_overclaim"),
        ("independence_beyond_model_asserted", "reject_truth_overclaim"),
    ]:
        packet = canonical_packet(); packet[field] = True
        cases.append((field, canonical_state("captured"), EVENTS[0], packet, expected))
    stage_checks = {
        "captured": [
            ("sensor_identity_present", "request_sensor_identity"),
            ("calibration_present", "request_calibration"),
            ("clock_pose_present", "request_clock_pose"),
            ("lineage_present", "request_lineage"),
            ("fresh", "request_freshness"),
        ],
        "identities_bound": [
            ("dependence_roots_declared", "request_dependence_roots"),
            ("common_cause_reviewed", "request_common_cause_review"),
        ],
        "dependence_bound": [
            ("pair_classification_present", "request_pair_classification"),
            ("evidence_count_matches_classification", "request_evidence_count_match"),
        ],
        "pair_reviewed": [
            ("authority_bounded", "request_bounded_authority"),
            ("expiry_present", "request_expiry"),
            ("fallback_present", "request_fallback"),
            ("residual_owner_present", "request_residual_owner"),
        ],
        "use_bound": [
            ("consumer_present", "request_consumer"),
            ("maximum_inference_present", "request_maximum_inference"),
            ("independent_review", "request_independent_review"),
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
    state = canonical_state("dependence_bound"); state["computed_independent_count"] = 2
    packet = canonical_packet(); packet["computed_independent_count"] = 2
    cases.append(("correlated_count_inflation", state, EVENTS[2], packet,
                  "reject_correlated_inflation"))
    state = canonical_state("dependence_bound")
    state.update({"pair_disposition": "disagreement", "computed_independent_count": 0})
    packet = canonical_packet()
    packet.update({"pair_disposition": "disagreement", "computed_independent_count": 0,
                   "disagreement_preserved": False})
    cases.append(("erased_disagreement", state, EVENTS[2], packet,
                  "request_disagreement_preservation"))
    state = canonical_state("pair_reviewed"); state["requested_independent_count"] = 2
    packet = canonical_packet(); packet["requested_independent_count"] = 2
    cases.append(("two_item_request", state, EVENTS[3], packet,
                  "reject_correlated_inflation"))
    return cases


def main() -> None:
    failures = []
    declarations = re.findall(
        r"(?m)^theorem\s+([A-Za-z0-9_]+)", LEAN.read_text(encoding="utf-8")
    )
    if declarations != THEOREMS:
        failures.append(f"Lean theorem surface drifted: {declarations}")
    chapter = CHAPTER.read_text(encoding="utf-8")
    for phrase in (
        "support remains `argument`",
        "does not establish real sensor dependence",
        "does not prove environmental truth",
    ):
        if phrase not in chapter:
            failures.append(f"chapter boundary missing: {phrase}")
    if not DOSSIER.is_file():
        failures.append("proof-model dossier is missing")

    pair_cases = []
    correlated_left, correlated_right = channel(), channel()
    pair_cases.append(("correlated", correlated_left, correlated_right,
                       "correlated_agreement", 1))
    pair_cases.append(("independent", channel(), channel(root=9),
                       "independent_agreement", 2))
    pair_cases.append(("disagreement", channel(), channel(root=9, hypothesis="clear"),
                       "disagreement", 0))
    for field in ("fresh", "calibrated", "lineage_present", "clock_pose_aligned"):
        left = channel(); left[field] = False
        pair_cases.append((f"left_{field}", left, channel(), "inadmissible", 0))
        right = channel(); right[field] = False
        pair_cases.append((f"right_{field}", channel(), right, "inadmissible", 0))
    pair_cases.append(("root_mutation", channel(), channel(root=9),
                       "independent_agreement", 2))
    pair_cases.append(("hypothesis_mutation", channel(), channel(hypothesis="clear"),
                       "disagreement", 0))
    pair_failures = []
    for label, left, right, expected, expected_count in pair_cases:
        disposition = classify(left, right)
        if disposition != expected or evidence_count(disposition) != expected_count:
            pair_failures.append(label)
    if pair_failures:
        failures.append("pair-classification controls failed: " + ", ".join(pair_failures))

    state = canonical_state("captured")
    observed = []
    for index, event in enumerate(EVENTS, 1):
        state, route = apply_event(state, event, canonical_packet(index))
        observed.append(route)
    if observed != [
        "accept_identities", "accept_dependence", "accept_pair_review",
        "accept_use_binding", "accept_handoff", "accept_invalidation",
    ]:
        failures.append(f"accepted route sequence drifted: {observed}")
    if state["stage"] != "invalidated" or state["receipt_count"] != 6:
        failures.append("complete lifecycle did not reach invalidated with six receipts")
    if state["handoff_count"] != 1 or state["invalidation_count"] != 1:
        failures.append("handoff/invalidation accounting drifted")
    if state["support_assignment_count"] or state["external_authority_count"]:
        failures.append("accepted lifecycle minted support or external authority")

    mutations = lifecycle_mutations()
    escaped = []
    for label, before, event, packet, expected in mutations:
        after, route = apply_event(before, event, packet)
        if route != expected or after != before or route in ACCEPTED:
            escaped.append(f"{label}:{route}:{expected}")
    if escaped:
        failures.append("lifecycle mutations escaped: " + ", ".join(escaped))
    if len(mutations) != 46:
        failures.append(f"lifecycle mutation denominator drifted: {len(mutations)}")
    if len(pair_cases) != 13:
        failures.append(f"pair-control denominator drifted: {len(pair_cases)}")

    if failures:
        raise SystemExit("Observation-trust validation failed:\n - " + "\n - ".join(failures))
    print(
        "Observation trust passed: correlated agreement counts one independent item, "
        "independent agreement counts two, disagreement remains distinct, 7 stages, "
        "6 accepted transitions, 46/46 exact-state lifecycle mutations and 13/13 "
        "pair-classification controls, 16 Lean declarations, no support or external-authority effect."
    )


if __name__ == "__main__":
    main()
