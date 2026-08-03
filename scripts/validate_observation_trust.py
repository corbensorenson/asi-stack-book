#!/usr/bin/env python3
"""Validate correlated-evidence non-promotion and observation custody."""

from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ObservationTrust.lean"
CHAPTER = ROOT / "chapters/perception-sensor-fusion-and-observation-trust.qmd"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/perception-sensor-fusion-and-observation-trust.md"
FIXTURE = ROOT / "tests/fixtures/proof_models/observation_trust.json"

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
    "apply_event_preserves_exact_observation_identity",
    "accepted_observation_step_is_accepted",
    "accepted_observation_step_applies_event",
    "accepted_observation_step_preserves_exact_identity",
    "accepted_observation_step_adds_one_receipt",
    "rejected_observation_step_preserves_exact_state",
    "successful_observation_run_preserves_exact_identity",
    "successful_observation_run_preserves_non_authority",
    "successful_observation_run_accounts_receipts",
    "successful_observation_run_has_valid_trace",
    "observation_runs_compose",
    "invalidated_observation_state_rejects_every_event",
    "invalidated_observation_state_has_no_nonempty_run",
    "pairwise_root_summary_collides_across_global_common_cause",
    "exact_common_cause_state_separates_pairwise_root_collision",
    "no_exact_global_independence_classifier_from_pairwise_roots_only",
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
    if stage == "invalidated":
        return "reject_wrong_stage"
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


def run_events(state: dict, events: list[str], start_digest: int = 1) -> dict | None:
    current = copy.deepcopy(state)
    for offset, event in enumerate(events):
        current, route = apply_event(
            current, event, canonical_packet(start_digest + offset)
        )
        if route not in ACCEPTED:
            return None
    return current


def global_independence_admitted(case: dict) -> bool:
    return case["left_root"] != case["right_root"] and not case["common_cause_present"]


def validate_lean_surface() -> None:
    declarations = re.findall(
        r"(?m)^theorem\s+([A-Za-z0-9_]+)", LEAN.read_text(encoding="utf-8")
    )
    if declarations != THEOREMS:
        raise SystemExit(f"Observation-trust Lean theorem surface drifted: {declarations}")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/ObservationTrust.lean"],
        cwd=ROOT / "lean",
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise SystemExit(
            "Observation-trust Lean recompilation failed:\n"
            + completed.stdout
            + completed.stderr
        )


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
    validate_lean_surface()
    failures = []
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if fixture.get("schema_version") != "1.0.0" or fixture.get("support_state_effect") != "none":
        failures.append("observation-trust fixture metadata drifted")
    chapter = CHAPTER.read_text(encoding="utf-8")
    for phrase in (
        "support remains `argument`",
        "does not establish real sensor dependence",
        "does not prove environmental truth",
        "pairwise roots do not establish global independence",
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

    initial = canonical_state(fixture["initial_stage"])
    state = copy.deepcopy(initial)
    observed = []
    fixture_events = fixture["event_sequence"]
    for index, event in enumerate(fixture_events, 1):
        state, route = apply_event(state, event, canonical_packet(index))
        observed.append(route)
    if fixture_events != EVENTS or observed != fixture["expected_routes"]:
        failures.append(f"accepted route sequence drifted: {observed}")
    expected_final = fixture["expected_final"]
    if any(state.get(field) != value for field, value in expected_final.items()):
        failures.append("complete lifecycle drifted from the fixture's exact final projection")

    composition_failures = []
    for split in range(len(EVENTS) + 1):
        middle = run_events(initial, EVENTS[:split])
        if middle is None:
            composition_failures.append(f"front:{split}")
            continue
        composed = run_events(middle, EVENTS[split:], split + 1)
        if composed != state:
            composition_failures.append(f"back:{split}")
    if composition_failures:
        failures.append("lifecycle composition failed: " + ", ".join(composition_failures))

    terminal_failures = []
    for index, event in enumerate(EVENTS, 1):
        after, route = apply_event(state, event, canonical_packet(index + 20))
        if route in ACCEPTED or after != state:
            terminal_failures.append(f"{event}:{route}")
    if terminal_failures:
        failures.append("invalidated terminal controls failed: " + ", ".join(terminal_failures))

    common_cause_collisions = []
    roots = [7, 9, 11, 13]
    for left_root in roots:
        for right_root in roots:
            if left_root == right_root:
                continue
            clear = {
                "left_root": left_root,
                "right_root": right_root,
                "common_cause_present": False,
            }
            shared = {**clear, "common_cause_present": True}
            clear_summary = (clear["left_root"], clear["right_root"])
            shared_summary = (shared["left_root"], shared["right_root"])
            if (
                clear_summary != shared_summary
                or not global_independence_admitted(clear)
                or global_independence_admitted(shared)
            ):
                common_cause_collisions.append(f"{left_root}:{right_root}")
    if common_cause_collisions:
        failures.append(
            "common-cause summary collisions failed: "
            + ", ".join(common_cause_collisions)
        )
    collision = fixture["common_cause_collision"]
    clear_fixture = {
        "left_root": collision["left_root"],
        "right_root": collision["right_root"],
        "common_cause_present": collision["clear_common_cause_present"],
    }
    shared_fixture = {
        **clear_fixture,
        "common_cause_present": collision["shared_common_cause_present"],
    }
    if (
        global_independence_admitted(clear_fixture) != collision["clear_admitted"]
        or global_independence_admitted(shared_fixture) != collision["shared_admitted"]
    ):
        failures.append("fixture common-cause collision drifted")

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
        "Observation trust passed: exact 32-theorem Lean surface recompiled; correlated "
        "agreement counts one independent item, distinct declared roots count two only "
        "inside the pair model, disagreement remains distinct, 7 stages, 6 accepted "
        "transitions, 7 composition splits, 46/46 exact-state lifecycle mutations, "
        "13/13 pair-classification controls, 6 invalidated-state event kinds, and 12 "
        "same-root-summary/opposite-common-cause controls; no sensor truth, global "
        "independence, support, safety, or external-authority effect."
    )


if __name__ == "__main__":
    main()
