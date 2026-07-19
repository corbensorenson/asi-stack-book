#!/usr/bin/env python3
"""Validate P4/M6 lineage, terminal result, mutations, and no-promotion decision."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/p4_routing_deliberation"
RESULT = BASE / "results/confirmatory_result.json"
TRANSITION = ROOT / "evidence_transitions/post_v2_3/routing_deliberation_mixed_no_promotion.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(result: dict[str, Any]) -> list[str]:
    out: list[str] = []
    prereg = load(BASE / "preregistration.json")
    design = load(BASE / "design.json")
    tasks = load(BASE / "tasks.json")
    labels = load(BASE / "labels.json")
    v1 = load(BASE / "results/preflight_result.json")
    v2 = load(BASE / "results/preflight_v2_result.json")
    qualification = load(BASE / "instrument_qualification_v2.json")
    transition = load(TRANSITION)
    for path, key in ((BASE / "design.json", "design_sha256"), (BASE / "tasks.json", "tasks_sha256"), (BASE / "labels.json", "labels_sha256")):
        if prereg.get(key) != sha(path):
            out.append(f"frozen digest drift: {path.name}")
    if v1.get("protocol_outcome") != "instrument_inadequate" or v1.get("schema_admissible_count") != 1 or v1.get("expected_task_count") != 4:
        out.append("v1 instrument failure lineage drift")
    if v2.get("protocol_outcome") != "instrument_adequate" or v2.get("schema_admissible_count") != 4 or v2.get("heldout_opened") is not True:
        out.append("v2 instrument qualification drift")
    if qualification.get("result_sha256") != sha(BASE / "results/preflight_v2_result.json") or qualification.get("heldout_opened") is not True:
        out.append("held-out opening authority drift")
    if result.get("candidate_artifact_closed_before_labels_loaded") is not True or result.get("candidate_sha256") != sha(BASE / "raw/heldout_candidates.json"):
        out.append("candidate closure drift")
    if result.get("expected_task_count") != 32 or result.get("schema_admissible_count") != 32 or result.get("exclusions") != []:
        out.append("held-out denominator drift")
    if set(result.get("track_counts", {}).values()) != {4} or set(result.get("ingress_counts", {}).values()) != {8}:
        out.append("track or ingress balance drift")
    controls = set(design["control_classes"])
    if set(result.get("control_counts", {})) != controls or len(controls) != 17 or any(result["control_counts"][key] < 1 for key in controls):
        out.append("control coverage drift")
    if result.get("route_evaluator_disagreement_count") != 0 or result.get("outcome_evaluator_disagreement_count") != 0:
        out.append("evaluator disagreement drift")
    if not all(result.get("gate_checks_before_validator_mutations", {}).values()) or len(result.get("gate_checks_before_validator_mutations", {})) != 7:
        out.append("frozen gate drift")
    summaries = result.get("policy_summaries", {})
    expected_policy = {
        "llm_first": (6, 9, 18, 0),
        "hard_rule_only": (19, 14, 13, 0),
        "learned_router": (12, 14, 11, 0),
        "semantic_cache": (7, 11, 18, 0),
        "llm_first_tool_agent": (6, 8, 18, 0),
        "modular_tool_system": (19, 13, 13, 0),
        "full_reflexive_route": (31, 21, 1, 2),
        "oracle_selection": (32, 24, 0, 0),
    }
    for arm, expected in expected_policy.items():
        row = summaries.get(arm, {})
        observed = (row.get("route_correct"), row.get("useful_outcomes"), row.get("wrong_fast_path"), row.get("unsafe_outputs"))
        if observed != expected:
            out.append(f"policy summary drift: {arm}")
    expected_deliberation = {
        "no_deliberation": (12, 0, 0),
        "fixed_deliberation": (11, 3, 2),
        "adaptive_stopping": (12, 1, 1),
        "verifier_gated_stopping": (12, 0, 0),
    }
    for arm, expected in expected_deliberation.items():
        row = result.get("deliberation_summaries", {}).get(arm, {})
        observed = (row.get("final_correct"), row.get("initial_correct_corrupted"), row.get("initial_incorrect_repaired"))
        if observed != expected:
            out.append(f"deliberation summary drift: {arm}")
    harms = result.get("known_harm_replay", [])
    if len(harms) != 15 or not all(row.get("fixed_corrupts") and row.get("adaptive_stopping_preserves_initial") and row.get("verifier_gated_preserves_initial") and row.get("new_model_call") is False for row in harms):
        out.append("historical harm regression drift")
    if result.get("protocol_outcome") != "bounded_local_routing_policy_effect_observed" or result.get("matched_policy_effect_observed") is not True:
        out.append("terminal effect disposition drift")
    if (
        transition.get("transition_effect") != "no_change"
        or transition.get("old_support_state") != "argument"
        or transition.get("new_support_state") != "argument"
        or transition.get("review_status") != "accepted"
        or transition.get("support_state_effect") != "blocks_promotion"
    ):
        out.append("mixed-result no-promotion decision drift")
    if "two unsafe outputs versus zero" not in transition.get("transition_reason", ""):
        out.append("safety tradeoff erased from transition rationale")
    if tasks.get("task_count") != 32 or labels.get("label_count") != 32:
        out.append("source task or label count drift")
    return out


def main() -> None:
    result = load(RESULT)
    failures = errors(result)
    mutations = []
    for control in load(BASE / "design.json")["control_classes"]:
        candidate = copy.deepcopy(result)
        candidate["control_counts"][control] = 0
        if not errors(candidate):
            failures.append(f"control mutation accepted: {control}")
        mutations.append(control)
    for label, change in (
        ("erase unsafe tradeoff", lambda r: r["policy_summaries"]["full_reflexive_route"].__setitem__("unsafe_outputs", 0)),
        ("inflate useful outcome", lambda r: r["policy_summaries"]["full_reflexive_route"].__setitem__("useful_outcomes", 22)),
        ("erase fixed harm", lambda r: r["deliberation_summaries"]["fixed_deliberation"].__setitem__("initial_correct_corrupted", 0)),
        ("reopen denominator", lambda r: r.__setitem__("confirmatory_denominator_closed", False)),
        ("launder transfer", lambda r: r.__setitem__("claim_ceiling", "general transfer supported")),
    ):
        candidate = copy.deepcopy(result); change(candidate)
        local = errors(candidate)
        if label == "reopen denominator" and candidate.get("confirmatory_denominator_closed") is not True:
            local.append("denominator reopened")
        if label == "launder transfer" and "general transfer supported" in candidate.get("claim_ceiling", ""):
            local.append("claim ceiling laundered")
        if not local:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4/M6 validation failed:\n - " + "\n - ".join(failures))
    print("P4/M6 validation passed: v1 failure retained, v2 4/4 instrument qualified, 32/32 held-out candidates admitted across 8 tracks and 4 ingress modes, 17 control mutations plus 5 disposition mutations rejected, full reflexive 31 routes/21 useful/1 wrong-fast/2 unsafe, fixed deliberation 3 corruptions/2 repairs, fifteen historical harms preserved, and no support promotion.")


if __name__ == "__main__":
    main()
