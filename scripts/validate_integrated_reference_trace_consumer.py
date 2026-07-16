#!/usr/bin/env python3
"""Independently execute the bounded cross-layer trace join model."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments/integrated_reference_trace/corpus/2026-07-15.json"
RESULT = ROOT / "experiments/integrated_reference_trace/results/2026-07-15-local.json"
LEAN = ROOT / "lean/AsiStackProofs/IntegratedReferenceTrace.lean"
SCHEMA = ROOT / "schemas/integrated_reference_trace_consumer.schema.json"

LAYERS = {
    "request", "intent", "context", "plan", "route", "authorize", "job",
    "adapter", "effect", "observe", "evaluate", "evidence", "terminal", "quarantine",
}
KINDS = {"advance", "commit_effect", "acknowledge", "evaluate", "evidence", "rollback", "terminal", "quarantine"}
ADVANCE_PAIRS = {
    ("request", "intent"), ("intent", "context"), ("context", "plan"),
    ("plan", "route"), ("route", "authorize"), ("authorize", "job"),
    ("job", "adapter"),
}
MUTATIONS = (
    (0, "parent_artifact", 999),
    (0, "state_before", 9999),
    (0, "requested_authority", 4),
    (0, "residual_owner_present", False),
    (0, "non_claim_present", False),
    (0, "produced_artifact", 0),
    (4, "gate_present", False),
    (7, "effect_delta", 0),
    (7, "rollback_ready", False),
    (8, "acknowledgement_delta", 2),
    (8, "independent_observation", False),
    (9, "independent_evaluator", False),
    (10, "residual_discharged", 2),
    (11, "receipt_present", False),
    (11, "support_after", 2),
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expand(base: dict[str, Any], patches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for patch in patches:
        event = copy.deepcopy(base)
        event.update(patch)
        events.append(event)
    return events


def reasons(state: dict[str, Any], event: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    kind = event.get("kind")
    if kind not in KINDS:
        return ["unknown_event_kind"]
    if event.get("from_layer") not in LAYERS or event.get("to_layer") not in LAYERS:
        failures.append("unknown_layer")
    if event.get("requested_authority", -1) > state.get("active_authority", -1):
        failures.append("authority_widening")
    if state.get("active_authority", -1) > state.get("authority_ceiling", -1):
        failures.append("state_authority_above_ceiling")
    if event.get("from_layer") != state.get("current_layer"):
        failures.append("layer_join_mismatch")
    if event.get("parent_artifact") != state.get("last_artifact"):
        failures.append("parent_artifact_mismatch")
    if event.get("state_before") != state.get("canonical_state"):
        failures.append("canonical_state_mismatch")
    if event.get("produced_artifact") == 0:
        failures.append("missing_produced_artifact")
    if event.get("logical_time", -1) < state.get("logical_time", -1):
        failures.append("logical_time_regression")
    if event.get("residual_discharged", -1) > state.get("open_residuals", 0) + event.get("residual_created", 0):
        failures.append("residual_erasure")
    if event.get("support_before") != state.get("support_level"):
        failures.append("support_lineage_mismatch")
    if event.get("residual_owner_present") is not True:
        failures.append("missing_residual_owner")
    if event.get("non_claim_present") is not True:
        failures.append("missing_non_claim_boundary")
    if event.get("gate_required") is True and event.get("gate_present") is not True:
        failures.append("missing_governance_gate")

    no_effect = event.get("effect_delta") == 0 and event.get("acknowledgement_delta") == 0 and event.get("rollback_delta") == 0
    if kind == "advance":
        if (event.get("from_layer"), event.get("to_layer")) not in ADVANCE_PAIRS:
            failures.append("invalid_layer_advance")
        if not no_effect:
            failures.append("advance_has_effect")
        if event.get("support_after") != event.get("support_before"):
            failures.append("advance_changes_support")
    elif kind == "commit_effect":
        if (event.get("from_layer"), event.get("to_layer")) != ("adapter", "effect"):
            failures.append("effect_layer_mismatch")
        if event.get("effect_delta", 0) <= 0:
            failures.append("missing_effect")
        if event.get("acknowledgement_delta") != 0 or event.get("rollback_delta") != 0:
            failures.append("effect_event_mixes_lanes")
        if event.get("rollback_ready") is not True:
            failures.append("effect_without_rollback")
        revoked_at = state.get("revoked_at")
        if revoked_at is not None and event.get("logical_time", 0) >= revoked_at:
            failures.append("effect_at_or_after_revocation")
        if event.get("support_after") != event.get("support_before"):
            failures.append("effect_changes_support")
    elif kind == "acknowledge":
        if (event.get("from_layer"), event.get("to_layer")) != ("effect", "observe"):
            failures.append("observation_layer_mismatch")
        if event.get("effect_delta") != 0 or event.get("rollback_delta") != 0:
            failures.append("observation_mixes_effect_lane")
        delta = event.get("acknowledgement_delta", 0)
        if delta <= 0 or state.get("acknowledged_effects", 0) + delta > state.get("material_effects", 0):
            failures.append("invalid_effect_acknowledgement")
        if event.get("independent_observation") is not True:
            failures.append("observation_not_independent")
        if event.get("support_after") != event.get("support_before"):
            failures.append("observation_changes_support")
    elif kind == "evaluate":
        if (event.get("from_layer"), event.get("to_layer")) != ("observe", "evaluate"):
            failures.append("evaluation_layer_mismatch")
        if not no_effect:
            failures.append("evaluation_has_effect")
        if event.get("independent_evaluator") is not True:
            failures.append("evaluator_not_independent")
        if event.get("support_after") != event.get("support_before"):
            failures.append("evaluation_changes_support")
    elif kind == "evidence":
        if (event.get("from_layer"), event.get("to_layer")) != ("evaluate", "evidence"):
            failures.append("evidence_layer_mismatch")
        if state.get("evaluation_complete") is not True:
            failures.append("evidence_before_evaluation")
        if not no_effect:
            failures.append("evidence_event_has_effect")
        changed = event.get("support_after") != event.get("support_before")
        if changed and not (event.get("evidence_transition_present") is True and event.get("accepted_review") is True):
            failures.append("support_change_without_transition")
    elif kind == "rollback":
        if event.get("to_layer") != "terminal":
            failures.append("rollback_not_terminal")
        if event.get("effect_delta") != 0 or event.get("acknowledgement_delta") != 0:
            failures.append("rollback_mixes_forward_effect")
        if event.get("rollback_delta") != state.get("material_effects"):
            failures.append("effect_incomplete_rollback")
        if event.get("rollback_ready") is not True or event.get("rollback_exact") is not True:
            failures.append("rollback_not_exact")
        if event.get("receipt_present") is not True:
            failures.append("rollback_without_receipt")
        if event.get("support_after") != event.get("support_before"):
            failures.append("rollback_changes_support")
    elif kind == "terminal":
        if (event.get("from_layer"), event.get("to_layer")) != ("evidence", "terminal"):
            failures.append("terminal_layer_mismatch")
        if state.get("observation_complete") is not True or state.get("evaluation_complete") is not True:
            failures.append("terminal_missing_assurance")
        if state.get("material_effects") != state.get("acknowledged_effects"):
            failures.append("terminal_unacknowledged_effect")
        if not no_effect:
            failures.append("terminal_event_has_effect")
        if event.get("receipt_present") is not True:
            failures.append("terminal_without_receipt")
        if event.get("support_after") != event.get("support_before"):
            failures.append("terminal_changes_support")
    elif kind == "quarantine":
        if event.get("to_layer") != "quarantine":
            failures.append("quarantine_layer_mismatch")
        if not no_effect:
            failures.append("quarantine_has_effect")
        if event.get("receipt_present") is not True:
            failures.append("quarantine_without_receipt")
        if event.get("support_after") != event.get("support_before"):
            failures.append("quarantine_changes_support")
    return failures


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    next_state.update({
        "current_layer": event["to_layer"],
        "active_authority": event["requested_authority"],
        "canonical_state": event["state_after"],
        "last_artifact": event["produced_artifact"],
        "open_residuals": state["open_residuals"] + event["residual_created"] - event["residual_discharged"],
        "support_level": event["support_after"],
        "logical_time": event["logical_time"],
    })
    if event["kind"] == "rollback":
        next_state["material_effects"] = 0
        next_state["acknowledged_effects"] = 0
        next_state["rolled_back"] = True
    else:
        next_state["material_effects"] += event["effect_delta"]
        next_state["acknowledged_effects"] += event["acknowledgement_delta"]
    next_state["observation_complete"] = state["observation_complete"] or event["kind"] == "acknowledge"
    next_state["evaluation_complete"] = state["evaluation_complete"] or event["kind"] == "evaluate"
    next_state["terminal_receipt"] = state["terminal_receipt"] or event["receipt_present"]
    return next_state


def run(initial: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    state = copy.deepcopy(initial)
    for index, event in enumerate(events):
        failed = reasons(state, event)
        if failed:
            return {"accepted": False, "rejection_index": index, "reasons": failed, "final_state": state}
        state = apply_event(state, event)
    return {"accepted": True, "rejection_index": None, "reasons": [], "final_state": state}


def validate_source(corpus: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source = ROOT / corpus["source_result_ref"]
    if digest(source) != corpus["source_result_sha256"]:
        errors.append("executed source-result digest drifted")
    data = load(source)
    by_id = {row["scenario_id"]: set(row["governed"]["event_log"]) for row in data["scenario_results"]}
    for scenario, required in corpus["source_scenario_requirements"].items():
        if scenario not in by_id:
            errors.append(f"missing source scenario: {scenario}")
        elif not set(required).issubset(by_id[scenario]):
            errors.append(f"source scenario {scenario} missing events: {sorted(set(required) - by_id[scenario])}")
    for case in corpus["cases"]:
        if case["source_scenario"] not in by_id:
            errors.append(f"{case['id']}: unknown source scenario {case['source_scenario']}")
    return errors


def result_shape_errors(result: dict[str, Any]) -> list[str]:
    schema = load(SCHEMA)
    required = set(schema["required"])
    errors: list[str] = []
    if required - set(result):
        errors.append(f"result missing fields: {sorted(required - set(result))}")
    if set(result) - set(schema["properties"]):
        errors.append(f"result has extra fields: {sorted(set(result) - set(schema['properties']))}")
    if result.get("support_state_effect") != "none":
        errors.append("support-state effect must remain none")
    if not isinstance(result.get("non_claims"), list) or len(result.get("non_claims", [])) < 3:
        errors.append("result requires at least three non-claims")
    return errors


def build_result() -> tuple[dict[str, Any], list[str]]:
    corpus = load(CORPUS)
    errors = validate_source(corpus)
    initial_template = corpus["initial_state"]
    base = corpus["base_event"]
    accepted = 0
    rejected = 0
    accepted_events = 0
    effect_attempts = 0
    net_effects = 0
    acknowledgements = 0
    open_residuals = 0
    terminal_receipts = 0
    rolled_back = 0
    quarantined = 0
    support_transitions = 0
    receipts: list[dict[str, Any]] = []
    accepted_complete_events: list[dict[str, Any]] | None = None

    for case in corpus["cases"]:
        initial = copy.deepcopy(initial_template)
        initial.update(case.get("initial_state_patch", {}))
        prefix = corpus["prefixes"].get(case.get("prefix"), []) if case.get("prefix") else []
        events = expand(base, prefix + case["patches"])
        observed = run(initial, events)
        expected = case["expected"] == "accepted"
        if observed["accepted"] != expected:
            errors.append(f"{case['id']}: expected {case['expected']}, observed {observed}")
        if expected and observed["accepted"]:
            accepted += 1
            accepted_events += len(events)
            effect_attempts += sum(event["effect_delta"] for event in events)
            final = observed["final_state"]
            net_effects += final["material_effects"]
            acknowledgements += final["acknowledged_effects"]
            open_residuals += final["open_residuals"]
            terminal_receipts += int(final["terminal_receipt"])
            rolled_back += int(final["rolled_back"])
            quarantined += int(final["current_layer"] == "quarantine")
            support_transitions += int(final["support_level"] != initial["support_level"])
            if final["current_layer"] != case.get("expected_terminal_layer"):
                errors.append(f"{case['id']}: wrong terminal layer {final['current_layer']}")
            if case["id"] == "approved-complete-join":
                accepted_complete_events = events
        elif not expected and not observed["accepted"]:
            rejected += 1
        receipts.append({
            "case_id": case["id"],
            "source_scenario": case["source_scenario"],
            "expected": case["expected"],
            "observed": "accepted" if observed["accepted"] else "rejected",
            "rejection_index": observed["rejection_index"],
            "reasons": observed["reasons"],
            "final_layer": observed["final_state"]["current_layer"],
            "final_artifact": observed["final_state"]["last_artifact"],
            "final_state": observed["final_state"]["canonical_state"],
            "final_authority": observed["final_state"]["active_authority"],
            "final_effects": observed["final_state"]["material_effects"],
            "final_acknowledged_effects": observed["final_state"]["acknowledged_effects"],
            "final_open_residuals": observed["final_state"]["open_residuals"],
        })

    mutation_rejections = 0
    if accepted_complete_events is None:
        errors.append("missing accepted complete join trace")
    else:
        for index, field, value in MUTATIONS:
            mutated = copy.deepcopy(accepted_complete_events)
            mutated[index][field] = value
            if not run(initial_template, mutated)["accepted"]:
                mutation_rejections += 1
            else:
                errors.append(f"mutation accepted: event {index} {field}={value!r}")

    result = {
        "schema_version": "0.1",
        "experiment_id": corpus["corpus_id"],
        "status": "passed" if not errors else "failed",
        "source_result_sha256": corpus["source_result_sha256"],
        "corpus_sha256": digest(CORPUS),
        "lean_model_sha256": digest(LEAN),
        "case_count": len(corpus["cases"]),
        "accepted_case_count": accepted,
        "rejected_case_count": rejected,
        "accepted_event_count": accepted_events,
        "effect_attempt_count": effect_attempts,
        "final_net_effect_count": net_effects,
        "final_acknowledged_effect_count": acknowledgements,
        "final_open_residual_count": open_residuals,
        "terminal_receipt_count": terminal_receipts,
        "rolled_back_case_count": rolled_back,
        "quarantined_case_count": quarantined,
        "support_transition_count": support_transitions,
        "mutation_count": len(MUTATIONS),
        "mutation_rejection_count": mutation_rejections,
        "source_scenario_count": len({case["source_scenario"] for case in corpus["cases"]}),
        "receipts": receipts,
        "support_state_effect": "none",
        "non_claims": corpus["non_claims"],
    }
    errors.extend(result_shape_errors(result))
    exact = {
        "case_count": 18, "accepted_case_count": 4, "rejected_case_count": 14,
        "accepted_event_count": 35, "effect_attempt_count": 3,
        "final_net_effect_count": 2, "final_acknowledged_effect_count": 1,
        "final_open_residual_count": 3, "terminal_receipt_count": 4,
        "rolled_back_case_count": 1, "quarantined_case_count": 2,
        "support_transition_count": 0, "mutation_count": 15,
        "mutation_rejection_count": 15, "source_scenario_count": 6,
    }
    for field, value in exact.items():
        if result[field] != value:
            errors.append(f"{field}: expected {value}, got {result[field]}")
    return result, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, errors = build_result()
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists():
        errors.append(f"missing {RESULT.relative_to(ROOT)}; run with --write")
    else:
        stored = load(RESULT)
        errors.extend(result_shape_errors(stored))
        if stored != result:
            errors.append("stored result is stale; run with --write")

    for label, patch in (
        ("support promotion", {"support_state_effect": "promotion"}),
        ("inflated acceptance", {"accepted_case_count": result["accepted_case_count"] + 1}),
        ("missing non-claims", {"non_claims": []}),
    ):
        candidate = copy.deepcopy(result)
        candidate.update(patch)
        rejected_record = bool(result_shape_errors(candidate)) or (
            candidate.get("case_count") != candidate.get("accepted_case_count", 0) + candidate.get("rejected_case_count", 0)
        )
        if not rejected_record:
            errors.append(f"result negative control accepted: {label}")

    if errors:
        print("Integrated reference trace consumer validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Integrated reference trace consumer passed: "
        f"{result['case_count']} cases ({result['accepted_case_count']} accepted, "
        f"{result['rejected_case_count']} rejected), {result['accepted_event_count']} accepted events, "
        f"{result['mutation_rejection_count']} mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
