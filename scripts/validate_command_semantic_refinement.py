#!/usr/bin/env python3
"""Independently consume the reachable command-semantic refinement model."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/CommandSemanticRefinement.lean"
COMMAND_SCHEMA = ROOT / "schemas/command_contract.schema.json"
PLAN_FIXTURES = ROOT / "experiments/plan_execution_contracts/fixtures"
HANDOFF = ROOT / "experiments/intent_execution_handoff/results/2026-07-02-local.json"
VERTICAL = ROOT / "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json"
RESULT = ROOT / "experiments/command_semantic_refinement/results/2026-07-15-local.json"
SCHEMA = ROOT / "schemas/command_semantic_refinement.schema.json"

SLOTS = ("objective", "constraints", "output_contract", "verification", "failure_behavior", "authority")
REQUIRED_SLOTS = SLOTS[:-1]
ACTIVE_PLAN_STATES = {"dispatchable", "running", "complete"}
INTERFACE_VIOLATIONS = {
    "invalid_ambiguity_dispatched.json": "unresolved_ambiguity_dispatched",
    "invalid_authority_widened_from_intent.json": "authority_widened_from_intent",
    "invalid_hidden_override_applied.json": "hidden_override_applied",
    "invalid_inferred_authority_dispatched.json": "inferred_authority_dispatched",
    "invalid_inferred_field_confidence_dispatched.json": "inferred_required_field_dispatched",
}
CORRECT_BLOCKS = {
    "valid_authority_inferred_blocked.json": "inferred_authority_blocked",
    "valid_blocked_authority_plan.json": "authority_boundary_blocked",
}
INTERFACE_ADMISSIBLE = {
    "invalid_approval_bypass.json",
    "invalid_contract_mismatch.json",
    "invalid_cycle_in_dag.json",
    "invalid_dispatch_without_receipt.json",
    "invalid_requirement_lost.json",
    "valid_dispatchable_linear_plan.json",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_inventory_digest(paths: list[Path]) -> str:
    body = "\n".join(f"{path.name}:{sha(path)}" for path in paths) + "\n"
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def slot(value_hash: int, provenance: str, confidence: str) -> dict[str, Any]:
    return {"value_hash": value_hash, "provenance": provenance, "confidence": confidence}


def empty_state() -> dict[str, Any]:
    empty = slot(0, "untrusted_data", "missing")
    return {
        "stage": "raw", "root_intent": 101, "command_version": 1,
        **{name: copy.deepcopy(empty) for name in SLOTS},
        "authority_ceiling": 3, "approved_authority": 0,
        "hidden_override_seen": False, "planning_validation_receipt": False,
        "dispatch_receipt": False, "blocked": False, "logical_time": 0,
    }


def reference_slots() -> dict[str, dict[str, Any]]:
    return {
        "objective": slot(501, "human_intent", "confirmed"),
        "constraints": slot(502, "policy", "policy_imposed"),
        "output_contract": slot(503, "human_intent", "confirmed"),
        "verification": slot(504, "policy", "policy_imposed"),
        "failure_behavior": slot(505, "policy", "policy_imposed"),
        "authority": slot(506, "human_intent", "confirmed"),
    }


def event(kind: str, from_stage: str, to_stage: str, logical_time: int) -> dict[str, Any]:
    return {
        "kind": kind, "from_stage": from_stage, "to_stage": to_stage,
        "root_intent": 101, "input_version": 1, "output_version": 1,
        **copy.deepcopy(reference_slots()),
        "requested_authority": 3, "constraint_source_hash": 502,
        "hidden_override_applied": False, "blocker_count": 0,
        "approval_receipt": False, "planning_validation_receipt": False,
        "dispatch_receipt": False, "block_receipt": False,
        "logical_time": logical_time,
    }


def reference_trace() -> list[dict[str, Any]]:
    bind = event("bind_fields", "raw", "fields_bound", 1)
    precedence = event("check_precedence", "fields_bound", "precedence_checked", 2)
    authority = event("bind_authority", "precedence_checked", "authority_bound", 3)
    authority["approval_receipt"] = True
    planning = event("validate_planning", "authority_bound", "planning_validated", 4)
    planning["planning_validation_receipt"] = True
    dispatch = event("request_dispatch", "planning_validated", "dispatch_ready", 5)
    dispatch["approval_receipt"] = True
    dispatch["dispatch_receipt"] = True
    return [bind, precedence, authority, planning, dispatch]


def dispatch_eligible(confidence: str) -> bool:
    return confidence in {"confirmed", "policy_imposed", "source_derived", "defaulted"}


def authority_eligible(confidence: str) -> bool:
    return confidence in {"confirmed", "policy_imposed"}


def control_eligible(provenance: str) -> bool:
    return provenance in {"human_intent", "policy", "source", "bounded_default"}


def required_eligible(value: dict[str, Any]) -> bool:
    return value["value_hash"] > 0 and control_eligible(value["provenance"]) and dispatch_eligible(value["confidence"])


def authority_ready(value: dict[str, Any]) -> bool:
    return value["value_hash"] > 0 and control_eligible(value["provenance"]) and authority_eligible(value["confidence"])


def slots_match(state: dict[str, Any], row: dict[str, Any]) -> bool:
    return all(row[name] == state[name] for name in SLOTS)


def transition_errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state["stage"] != row["from_stage"]:
        errors.append("stage_mismatch")
    if state["root_intent"] != row["root_intent"]:
        errors.append("root_intent_mismatch")
    if state["command_version"] != row["input_version"]:
        errors.append("command_version_mismatch")
    if state["logical_time"] >= row["logical_time"]:
        errors.append("non_monotonic_time")

    kind = row["kind"]
    if kind == "bind_fields":
        if row["from_stage"] != "raw" or row["to_stage"] != "fields_bound":
            errors.append("invalid_bind_stage")
        if not all(required_eligible(row[name]) for name in REQUIRED_SLOTS):
            errors.append("required_slot_not_dispatch_eligible")
        if row["authority"]["value_hash"] <= 0:
            errors.append("authority_slot_missing")
    elif kind == "check_precedence":
        if row["from_stage"] != "fields_bound" or row["to_stage"] != "precedence_checked":
            errors.append("invalid_precedence_stage")
        if not slots_match(state, row):
            errors.append("slot_substitution")
        if row["constraint_source_hash"] != state["constraints"]["value_hash"]:
            errors.append("constraint_source_mismatch")
        if row["hidden_override_applied"]:
            errors.append("hidden_override_applied")
    elif kind == "bind_authority":
        if row["from_stage"] != "precedence_checked" or row["to_stage"] != "authority_bound":
            errors.append("invalid_authority_stage")
        if not slots_match(state, row):
            errors.append("slot_substitution")
        if not authority_ready(row["authority"]):
            errors.append("authority_not_ready")
        if row["requested_authority"] > state["authority_ceiling"]:
            errors.append("authority_widening")
        if not row["approval_receipt"]:
            errors.append("approval_receipt_missing")
    elif kind == "validate_planning":
        if row["from_stage"] != "authority_bound" or row["to_stage"] != "planning_validated":
            errors.append("invalid_planning_stage")
        if not slots_match(state, row):
            errors.append("slot_substitution")
        if row["requested_authority"] != state["approved_authority"]:
            errors.append("approved_authority_mismatch")
        if row["hidden_override_applied"]:
            errors.append("hidden_override_applied")
        if row["blocker_count"] != 0:
            errors.append("open_blockers")
        if not row["planning_validation_receipt"]:
            errors.append("planning_validation_receipt_missing")
    elif kind == "request_dispatch":
        if row["from_stage"] != "planning_validated" or row["to_stage"] != "dispatch_ready":
            errors.append("invalid_dispatch_stage")
        if not slots_match(state, row):
            errors.append("slot_substitution")
        if not state["planning_validation_receipt"]:
            errors.append("prior_planning_validation_missing")
        if row["requested_authority"] != state["approved_authority"]:
            errors.append("approved_authority_mismatch")
        if not row["approval_receipt"]:
            errors.append("approval_receipt_missing")
        if row["blocker_count"] != 0:
            errors.append("open_blockers")
        if not row["dispatch_receipt"]:
            errors.append("dispatch_receipt_missing")
    elif kind == "block":
        if row["to_stage"] != "blocked" or not row["block_receipt"]:
            errors.append("invalid_block")
    else:
        errors.append("unknown_event")
    return errors


def apply_event(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    next_state["stage"] = row["to_stage"]
    next_state["command_version"] = row["output_version"]
    if row["kind"] == "bind_fields":
        for name in SLOTS:
            next_state[name] = copy.deepcopy(row[name])
    if row["kind"] == "bind_authority":
        next_state["approved_authority"] = row["requested_authority"]
    next_state["hidden_override_seen"] |= row["hidden_override_applied"]
    next_state["planning_validation_receipt"] |= row["planning_validation_receipt"]
    next_state["dispatch_receipt"] |= row["dispatch_receipt"]
    next_state["blocked"] |= row["block_receipt"]
    next_state["logical_time"] = row["logical_time"]
    return next_state


def run(rows: list[dict[str, Any]]) -> tuple[bool, int | None, list[str], dict[str, Any]]:
    state = empty_state()
    for index, row in enumerate(rows):
        errors = transition_errors(state, row)
        if errors:
            return False, index, errors, state
        state = apply_event(state, row)
    return True, None, [], state


def mutated_traces(base: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    mutations: list[tuple[str, list[dict[str, Any]]]] = []

    def replace(name: str, index: int, path: tuple[str, ...], value: Any) -> None:
        rows = copy.deepcopy(base)
        cursor: Any = rows[index]
        for part in path[:-1]:
            cursor = cursor[part]
        cursor[path[-1]] = value
        mutations.append((name, rows))

    for name in REQUIRED_SLOTS:
        replace(f"bind_{name}_hash_zero", 0, (name, "value_hash"), 0)
    for name in REQUIRED_SLOTS:
        replace(f"bind_{name}_confidence_inferred", 0, (name, "confidence"), "inferred")
    replace("bind_constraint_hidden_provenance", 0, ("constraints", "provenance"), "hidden_instruction")
    replace("bind_authority_hash_zero", 0, ("authority", "value_hash"), 0)
    replace("bind_root_mismatch", 0, ("root_intent",), 999)

    replace("precedence_hidden_override", 1, ("hidden_override_applied",), True)
    replace("precedence_source_hash_mismatch", 1, ("constraint_source_hash",), 999)
    replace("precedence_constraint_substitution", 1, ("constraints", "value_hash"), 999)
    replace("precedence_time_regression", 1, ("logical_time",), 1)

    replace("authority_confidence_inferred", 2, ("authority", "confidence"), "inferred")
    replace("authority_confidence_source_derived", 2, ("authority", "confidence"), "source_derived")
    replace("authority_hidden_provenance", 2, ("authority", "provenance"), "hidden_instruction")
    replace("authority_widening", 2, ("requested_authority",), 4)
    replace("authority_approval_missing", 2, ("approval_receipt",), False)
    replace("authority_slot_substitution", 2, ("authority", "value_hash"), 999)
    replace("authority_time_regression", 2, ("logical_time",), 2)

    for name in SLOTS:
        replace(f"planning_{name}_substitution", 3, (name, "value_hash"), 900 + SLOTS.index(name))
    replace("planning_authority_mismatch", 3, ("requested_authority",), 2)
    replace("planning_hidden_override", 3, ("hidden_override_applied",), True)
    replace("planning_open_blocker", 3, ("blocker_count",), 1)
    replace("planning_receipt_missing", 3, ("planning_validation_receipt",), False)

    replace("dispatch_approval_missing", 4, ("approval_receipt",), False)
    replace("dispatch_receipt_missing", 4, ("dispatch_receipt",), False)
    replace("dispatch_open_blocker", 4, ("blocker_count",), 1)
    replace("dispatch_authority_mismatch", 4, ("requested_authority",), 2)
    return mutations


def fixture_reason(path: Path, record: dict[str, Any]) -> str:
    command = record["command_contract"]
    plan = record["plan_graph"]
    origin = record.get("intent_origin") or {}
    active = plan.get("dispatch_state") in ACTIVE_PLAN_STATES
    if path.name == "invalid_ambiguity_dispatched.json":
        assert active and origin.get("clarification_status") == "unresolved"
    elif path.name == "invalid_authority_widened_from_intent.json":
        assert active and origin.get("explicit_authority_ceiling") != command.get("authority_ceiling")
    elif path.name == "invalid_hidden_override_applied.json":
        assert active and origin.get("hidden_override_disposition") == "accepted"
    elif path.name == "invalid_inferred_authority_dispatched.json":
        assert active and any("authority:inferred" in str(item).lower() for item in command["field_provenance"])
    elif path.name == "invalid_inferred_field_confidence_dispatched.json":
        assert active and "inferred" in {str(item).lower() for item in command["field_confidence"]}
    elif path.name in CORRECT_BLOCKS:
        assert not active and (plan.get("blocked_nodes") or command.get("validation_state") != "validated_for_planning")
    return INTERFACE_VIOLATIONS.get(path.name) or CORRECT_BLOCKS.get(path.name) or "downstream_owned_or_valid"


def build() -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    fixtures = sorted(PLAN_FIXTURES.glob("*.json"))
    expected_names = set(INTERFACE_VIOLATIONS) | set(CORRECT_BLOCKS) | INTERFACE_ADMISSIBLE
    if {path.name for path in fixtures} != expected_names:
        issues.append("plan fixture inventory drift")
    command_schema = load(COMMAND_SCHEMA)
    fixture_receipts: list[dict[str, Any]] = []
    for path in fixtures:
        record = load(path)
        schema_valid = True
        try:
            jsonschema.Draft202012Validator(command_schema).validate(record["command_contract"])
        except (KeyError, jsonschema.ValidationError):
            schema_valid = False
            issues.append(f"{path.name}: command contract schema validation failed")
        try:
            reason = fixture_reason(path, record)
        except (AssertionError, KeyError):
            reason = "classification_evidence_drift"
            issues.append(f"{path.name}: classification evidence drift")
        if path.name in INTERFACE_VIOLATIONS:
            classification = "command_interface_violation"
        elif path.name in CORRECT_BLOCKS:
            classification = "correctly_blocked_at_command_interface"
        else:
            classification = "command_interface_admissible"
        fixture_receipts.append({
            "fixture": path.name, "command_schema_valid": schema_valid,
            "classification": classification, "reason": reason,
            "whole_fixture_acceptance_inferred": False,
        })

    handoff = load(HANDOFF)
    if {
        "trace_count": handoff.get("trace_count"),
        "valid_trace_count": handoff.get("valid_trace_count"),
        "expected_invalid_control_count": handoff.get("expected_invalid_control_count"),
        "accepted_handoff_path_count": handoff.get("accepted_handoff_path_count"),
        "blocked_handoff_path_count": handoff.get("blocked_handoff_path_count"),
        "support_state_effect": handoff.get("support_state_effect"),
    } != {"trace_count": 9, "valid_trace_count": 2, "expected_invalid_control_count": 7,
          "accepted_handoff_path_count": 1, "blocked_handoff_path_count": 1, "support_state_effect": "none"}:
        issues.append("handoff result drift")
    if not all(handoff.get("transition_coverage", {}).values()):
        issues.append("handoff transition coverage drift")

    vertical = load(VERTICAL)
    vertical_expected = {
        "scenario_count": 9, "accepted_event_count": 89, "release_count": 3,
        "pre_effect_refusal_count": 3, "material_effect_count": 6,
        "independently_observed_effect_count": 6, "exact_rollback_count": 2,
        "exact_rollback_refusal_count": 2, "failed_rollback_quarantine_count": 1,
        "open_residual_scenario_count": 2, "mutation_count": 30,
        "mutation_rejection_count": 30, "support_state_effect": "none",
    }
    if any(vertical.get(key) != value for key, value in vertical_expected.items()):
        issues.append("vertical execution result drift")

    base = reference_trace()
    accepted, _, _, final = run(base)
    if not accepted or final["stage"] != "dispatch_ready" or not final["dispatch_receipt"]:
        issues.append("reference semantic trace rejected")
    mutation_receipts: list[dict[str, Any]] = []
    for mutation_id, rows in mutated_traces(base):
        mutation_accepted, index, reasons, _ = run(rows)
        mutation_receipts.append({
            "mutation_id": mutation_id, "rejected": not mutation_accepted,
            "failed_event_index": index, "reasons": reasons,
        })
        if mutation_accepted:
            issues.append(f"{mutation_id}: mutation accepted")

    counts = {name: sum(row["classification"] == name for row in fixture_receipts) for name in {
        "command_interface_violation", "correctly_blocked_at_command_interface", "command_interface_admissible"
    }}
    result = {
        "schema_version": "asi_stack.command_semantic_refinement.v1",
        "result_id": "command-semantic-refinement-2026-07-15-local",
        "source_sha256": {
            "lean_model": sha(LEAN), "command_schema": sha(COMMAND_SCHEMA),
            "plan_fixture_inventory": fixture_inventory_digest(fixtures),
            "handoff_result": sha(HANDOFF), "vertical_execution_result": sha(VERTICAL),
        },
        "plan_fixture_count": len(fixtures),
        "command_schema_valid_fixture_count": sum(row["command_schema_valid"] for row in fixture_receipts),
        "command_interface_violation_count": counts["command_interface_violation"],
        "correctly_blocked_at_command_interface_count": counts["correctly_blocked_at_command_interface"],
        "command_interface_admissible_count": counts["command_interface_admissible"],
        "fixture_receipts": fixture_receipts,
        "handoff_trace_count": 9, "handoff_invalid_control_count": 7,
        "vertical_scenario_count": 9, "vertical_accepted_event_count": 89,
        "reachable_trace_event_count": len(base),
        "reference_trace_final_state": final,
        "mutation_count": len(mutation_receipts),
        "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts),
        "mutation_receipts": mutation_receipts,
        "support_state_effect": "none",
        "non_claims": [
            "Hash equality is a finite identity check, not proof of natural-language semantic equivalence or completeness.",
            "Provenance, confidence, authority, approval, validation, and dispatch labels are trusted inputs; this packet does not establish their authentic extraction.",
            "Command-interface admissibility does not imply that the whole fixture is valid: approval, graph, receipt, contract-lineage, and requirement-preservation failures remain owned downstream.",
            "The packet does not establish deployed parsing or dispatch, prompt-injection resistance, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.",
        ],
    }
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc:
        issues.append(f"result schema: {exc.message}")
    return result, issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, issues = build()
    if issues:
        raise SystemExit("Command semantic refinement failed:\n - " + "\n - ".join(issues))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("Command semantic refinement result stale; run --write")
    print(
        "Command semantic refinement passed: "
        f"{result['plan_fixture_count']} fixtures classified, "
        f"{result['reachable_trace_event_count']} reachable events, "
        f"{result['mutation_rejection_count']} mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
