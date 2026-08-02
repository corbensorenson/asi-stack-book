#!/usr/bin/env python3
"""Independently consume the Verification Bandwidth lifecycle and legacy suites."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/VerificationBandwidthRefinement.lean"
SCHEMA = ROOT / "schemas/verification_bandwidth_refinement.schema.json"
ADEQUACY_SCHEMA = ROOT / "schemas/context_adequacy_record.schema.json"
RESULT = ROOT / "experiments/verification_bandwidth_refinement/results/2026-07-15-local.json"
ADMISSION_VALIDATOR = ROOT / "scripts/validate_context_admission_adequacy.py"
PROBE_VALIDATOR = ROOT / "scripts/validate_verification_bandwidth_probe.py"
CAPACITY_VALIDATOR = ROOT / "scripts/validate_verification_bandwidth_capacity_model.py"
PROBE_RESULT = ROOT / "experiments/verification_bandwidth/results/2026-07-02-local.json"
CAPACITY_RESULT = ROOT / "experiments/verification_bandwidth_capacity/results/2026-07-03-local.json"

ROUTES = (
    "reject_malformed",
    "request_context",
    "require_obligation_plan",
    "block_unauthorized_promotion",
    "block_inconsistent_counts",
    "block_contradiction",
    "record_residual",
    "require_independent_evaluator",
    "require_negative_search",
    "require_artifacts",
    "allow_draft",
    "handoff_to_evidence_gate",
)

EXPECTED_THEOREMS = {
    "accepted_verification_step_is_valid",
    "accepted_verification_step_applies_event",
    "accepted_verification_step_preserves_identity",
    "accepted_verification_step_preserves_support_authority",
    "accepted_verification_step_preserves_external_effect_authority",
    "successful_verification_run_preserves_identity",
    "successful_verification_run_preserves_support_authority",
    "successful_verification_run_preserves_external_effect_authority",
    "successful_verification_run_has_valid_trace",
    "verification_runs_compose",
    "successful_verification_run_preserves_complete_custody",
    "accepted_execution_event_binds_valid_execution",
    "accepted_adjudication_requires_evidence_gate_route",
    "accepted_handoff_cannot_request_support",
    "accepted_handoff_cannot_request_external_effect",
    "reference_verification_run_closes",
    "reference_verification_run_preserves_identity",
    "reference_verification_run_has_zero_authority",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plan() -> dict[str, Any]:
    return {
        "plan_id": 101,
        "claim_id": 201,
        "claim_version": 1,
        "packet_digest": 301,
        "packet_admitted": True,
        "transaction_valid": True,
        "risk_tier": "high",
        "requested_effect": "evidence_review",
        "obligation_count": 4,
        "authority_valid": True,
        "rights_valid": True,
        "budget_declared": True,
        "horizon_declared": True,
        "stop_rule_declared": True,
    }


def execution() -> dict[str, Any]:
    return {
        "plan_id": 101,
        "claim_id": 201,
        "claim_version": 1,
        "packet_digest": 301,
        "passed": 4,
        "failed": 0,
        "contradicted": 0,
        "disputed": 0,
        "unknown": 0,
        "infeasible": 0,
        "blocked": 0,
        "unattempted": 0,
        "negative_search_attempted": True,
        "independent_evaluator": True,
        "verification_artifacts_present": True,
        "residuals_recorded": False,
        "expiry_declared": True,
    }


def attempted_count(value: dict[str, Any]) -> int:
    return sum(int(value[key]) for key in ("passed", "failed", "contradicted", "disputed", "unknown"))


def disposition_count(value: dict[str, Any]) -> int:
    return attempted_count(value) + sum(int(value[key]) for key in ("infeasible", "blocked", "unattempted"))


def open_count(value: dict[str, Any]) -> int:
    return sum(int(value[key]) for key in ("failed", "disputed", "unknown", "infeasible", "blocked", "unattempted"))


def bound(current_plan: dict[str, Any], current_execution: dict[str, Any]) -> bool:
    return all(current_plan[key] == current_execution[key] for key in ("plan_id", "claim_id", "claim_version", "packet_digest"))


def plan_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("plan_id", "claim_id", "claim_version", "packet_digest", "obligation_count"):
        if not isinstance(value.get(key), int) or value[key] <= 0:
            errors.append(key)
    for key in (
        "packet_admitted",
        "transaction_valid",
        "authority_valid",
        "rights_valid",
        "budget_declared",
        "horizon_declared",
        "stop_rule_declared",
    ):
        if value.get(key) is not True:
            errors.append(key)
    if value.get("risk_tier") not in {"low", "medium", "high", "critical"}:
        errors.append("risk_tier")
    if value.get("requested_effect") not in {"drafting_only", "evidence_review", "promote_chapter_core"}:
        errors.append("requested_effect")
    return errors


def execution_errors(current_plan: dict[str, Any], value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not bound(current_plan, value):
        errors.append("binding")
    for key in ("passed", "failed", "contradicted", "disputed", "unknown", "infeasible", "blocked", "unattempted"):
        if not isinstance(value.get(key), int) or value[key] < 0:
            errors.append(key)
    if not errors and disposition_count(value) != current_plan["obligation_count"]:
        errors.append("disposition_count")
    if value.get("expiry_declared") is not True:
        errors.append("expiry_declared")
    if open_count(value) + int(value.get("contradicted", 0)) > 0 and value.get("residuals_recorded") is not True:
        errors.append("residuals_recorded")
    return errors


def route(current_plan: dict[str, Any], current_execution: dict[str, Any]) -> str:
    if any(current_plan.get(key, 0) == 0 for key in ("plan_id", "claim_id", "claim_version", "packet_digest")):
        return "reject_malformed"
    if current_plan.get("packet_admitted") is not True or current_plan.get("transaction_valid") is not True:
        return "request_context"
    if current_plan.get("obligation_count", 0) == 0:
        return "require_obligation_plan"
    if any(current_plan.get(key) is not True for key in ("authority_valid", "rights_valid", "budget_declared", "horizon_declared", "stop_rule_declared")):
        return "reject_malformed"
    if current_plan.get("requested_effect") == "promote_chapter_core":
        return "block_unauthorized_promotion"
    if not bound(current_plan, current_execution) or disposition_count(current_execution) != current_plan["obligation_count"] or current_execution.get("expiry_declared") is not True:
        return "block_inconsistent_counts"
    if current_execution.get("contradicted", 0) > 0:
        return "block_contradiction"
    if open_count(current_execution) > 0:
        return "record_residual"
    if current_plan.get("risk_tier") in {"high", "critical"} and current_execution.get("independent_evaluator") is not True:
        return "require_independent_evaluator"
    if current_execution.get("negative_search_attempted") is not True:
        return "require_negative_search"
    if current_execution.get("verification_artifacts_present") is not True:
        return "require_artifacts"
    if current_plan.get("requested_effect") == "evidence_review":
        return "handoff_to_evidence_gate"
    return "allow_draft"


def route_cases() -> list[tuple[str, dict[str, Any], dict[str, Any], str]]:
    cases: list[tuple[str, dict[str, Any], dict[str, Any], str]] = []
    def add(case_id: str, plan_patch: dict[str, Any], execution_patch: dict[str, Any], expected: str) -> None:
        p, e = plan(), execution(); p.update(plan_patch); e.update(execution_patch); cases.append((case_id, p, e, expected))
    add("malformed_claim", {"claim_id": 0}, {}, "reject_malformed")
    add("unadmitted_packet", {"packet_admitted": False}, {}, "request_context")
    add("missing_obligation_plan", {"obligation_count": 0}, {"passed": 0}, "require_obligation_plan")
    add("promotion_authority_leak", {"requested_effect": "promote_chapter_core"}, {}, "block_unauthorized_promotion")
    add("count_mismatch", {}, {"passed": 3}, "block_inconsistent_counts")
    add("contradiction", {}, {"passed": 3, "contradicted": 1, "residuals_recorded": True}, "block_contradiction")
    add("open_failure", {}, {"passed": 3, "failed": 1, "residuals_recorded": True}, "record_residual")
    add("correlated_high_risk_evaluator", {}, {"independent_evaluator": False}, "require_independent_evaluator")
    add("negative_search_missing", {"risk_tier": "medium"}, {"negative_search_attempted": False}, "require_negative_search")
    add("artifact_missing", {"risk_tier": "medium"}, {"verification_artifacts_present": False}, "require_artifacts")
    add("draft_only_complete", {"risk_tier": "medium", "requested_effect": "drafting_only"}, {}, "allow_draft")
    add("evidence_gate_handoff", {}, {}, "handoff_to_evidence_gate")
    return cases


def mutations() -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    def add(name: str, plan_patch: dict[str, Any] | None = None, execution_patch: dict[str, Any] | None = None) -> None:
        p, e = plan(), execution(); p.update(plan_patch or {}); e.update(execution_patch or {}); rows.append((name, p, e))
    for key in ("plan_id", "claim_id", "claim_version", "packet_digest", "obligation_count"):
        add("zero_" + key, {key: 0})
    for key in ("packet_admitted", "transaction_valid", "authority_valid", "rights_valid", "budget_declared", "horizon_declared", "stop_rule_declared"):
        add("false_" + key, {key: False})
    add("unauthorized_promotion", {"requested_effect": "promote_chapter_core"})
    for key in ("plan_id", "claim_id", "claim_version", "packet_digest"):
        add("substitute_" + key, execution_patch={key: 999})
    add("count_short", execution_patch={"passed": 3})
    add("count_long", execution_patch={"passed": 5})
    for key in ("failed", "contradicted", "disputed", "unknown", "infeasible", "blocked", "unattempted"):
        add("open_" + key, execution_patch={"passed": 3, key: 1, "residuals_recorded": True})
    add("open_failure_without_residual", execution_patch={"passed": 3, "failed": 1})
    add("correlated_evaluator", execution_patch={"independent_evaluator": False})
    add("negative_search_missing", execution_patch={"negative_search_attempted": False})
    add("artifacts_missing", execution_patch={"verification_artifacts_present": False})
    add("expiry_missing", execution_patch={"expiry_declared": False})
    return rows


def initial_state() -> dict[str, Any]:
    return {
        "stage": "proposed",
        "plan": plan(),
        "execution": execution(),
        "authority_ceiling": 1,
        "plan_freeze_receipt": False,
        "execution_receipt": False,
        "adjudication_receipt": False,
        "evidence_gate_receipt": False,
        "support_authority": False,
        "external_effect_authority": False,
        "logical_time": 0,
    }


def lifecycle_events() -> list[dict[str, Any]]:
    common = {
        "plan_id": 101,
        "claim_id": 201,
        "claim_version": 1,
        "packet_digest": 301,
        "authority_ceiling": 1,
        "execution": execution(),
        "plan_freeze_receipt": False,
        "execution_receipt": False,
        "adjudication_receipt": False,
        "evidence_gate_receipt": False,
        "support_promotion_requested": False,
        "external_effect_requested": False,
    }
    events: list[dict[str, Any]] = []
    for kind, from_stage, to_stage, logical_time in (
        ("freeze_plan", "proposed", "frozen", 1),
        ("record_execution", "frozen", "executed", 2),
        ("adjudicate", "executed", "adjudicated", 3),
        ("handoff", "adjudicated", "handed_off", 4),
    ):
        event = copy.deepcopy(common)
        event.update({
            "kind": kind,
            "from_stage": from_stage,
            "to_stage": to_stage,
            "logical_time": logical_time,
        })
        events.append(event)
    events[0]["plan_freeze_receipt"] = True
    events[1]["execution_receipt"] = True
    events[2]["adjudication_receipt"] = True
    events[3]["evidence_gate_receipt"] = True
    return events


def event_errors(state: dict[str, Any], event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state["stage"] != event.get("from_stage"):
        errors.append("stage_order")
    if event.get("logical_time", 0) <= state["logical_time"]:
        errors.append("logical_time")
    for key in ("plan_id", "claim_id", "claim_version", "packet_digest"):
        if event.get(key) != state["plan"][key]:
            errors.append(key)
    if event.get("authority_ceiling") != state["authority_ceiling"]:
        errors.append("authority_ceiling")
    if event.get("support_promotion_requested") is not False:
        errors.append("support_promotion_requested")
    if event.get("external_effect_requested") is not False:
        errors.append("external_effect_requested")

    kind = event.get("kind")
    if kind == "freeze_plan":
        if event.get("from_stage") != "proposed" or event.get("to_stage") != "frozen":
            errors.append("freeze_route")
        errors.extend("plan." + value for value in plan_errors(state["plan"]))
        if event.get("plan_freeze_receipt") is not True:
            errors.append("plan_freeze_receipt")
    elif kind == "record_execution":
        if event.get("from_stage") != "frozen" or event.get("to_stage") != "executed":
            errors.append("execution_route")
        if state.get("plan_freeze_receipt") is not True:
            errors.append("prior_plan_freeze_receipt")
        errors.extend("execution." + value for value in execution_errors(state["plan"], event["execution"]))
        if event.get("execution_receipt") is not True:
            errors.append("execution_receipt")
    elif kind == "adjudicate":
        if event.get("from_stage") != "executed" or event.get("to_stage") != "adjudicated":
            errors.append("adjudication_route")
        if state.get("plan_freeze_receipt") is not True or state.get("execution_receipt") is not True:
            errors.append("prior_execution_custody")
        if event.get("execution") != state.get("execution"):
            errors.append("execution_substitution")
        if route(state["plan"], state["execution"]) != "handoff_to_evidence_gate":
            errors.append("evidence_gate_route")
        if event.get("adjudication_receipt") is not True:
            errors.append("adjudication_receipt")
    elif kind == "handoff":
        if event.get("from_stage") != "adjudicated" or event.get("to_stage") != "handed_off":
            errors.append("handoff_route")
        if not all(state.get(key) is True for key in (
            "plan_freeze_receipt", "execution_receipt", "adjudication_receipt"
        )):
            errors.append("prior_adjudication_custody")
        if event.get("execution") != state.get("execution"):
            errors.append("execution_substitution")
        if event.get("evidence_gate_receipt") is not True:
            errors.append("evidence_gate_receipt")
    else:
        errors.append("event_kind")
    return sorted(set(errors))


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    next_state["stage"] = event["to_stage"]
    if event["kind"] == "record_execution":
        next_state["execution"] = copy.deepcopy(event["execution"])
    for key in (
        "plan_freeze_receipt", "execution_receipt", "adjudication_receipt",
        "evidence_gate_receipt",
    ):
        next_state[key] = bool(state[key] or event[key])
    next_state["logical_time"] = event["logical_time"]
    return next_state


def run_lifecycle(events: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, list[str]]:
    state = initial_state()
    errors: list[str] = []
    for index, event in enumerate(events):
        current_errors = event_errors(state, event)
        if current_errors:
            errors.extend(f"event_{index}.{value}" for value in current_errors)
            return None, errors
        state = apply_event(state, event)
    if state["stage"] != "handed_off":
        errors.append("terminal_stage")
    if not all(state[key] is True for key in (
        "plan_freeze_receipt", "execution_receipt", "adjudication_receipt",
        "evidence_gate_receipt",
    )):
        errors.append("terminal_custody")
    if state["support_authority"] is not False:
        errors.append("support_authority")
    if state["external_effect_authority"] is not False:
        errors.append("external_effect_authority")
    return (state if not errors else None), errors


def lifecycle_mutations() -> list[tuple[str, list[dict[str, Any]]]]:
    rows: list[tuple[str, list[dict[str, Any]]]] = []

    def add(name: str, mutate: Any) -> None:
        events = lifecycle_events()
        mutate(events)
        rows.append((name, events))

    for index in range(4):
        add(f"drop_event_{index}", lambda events, index=index: events.pop(index))
        add(f"duplicate_event_{index}", lambda events, index=index: events.insert(index, copy.deepcopy(events[index])))
        add(f"substitute_ceiling_{index}", lambda events, index=index: events[index].update(authority_ceiling=2))
        add(f"nonmonotone_time_{index}", lambda events, index=index: events[index].update(logical_time=0))
        add(f"request_support_{index}", lambda events, index=index: events[index].update(support_promotion_requested=True))
        add(f"request_external_effect_{index}", lambda events, index=index: events[index].update(external_effect_requested=True))
        for key in ("plan_id", "claim_id", "claim_version", "packet_digest"):
            add(f"substitute_{key}_{index}", lambda events, index=index, key=key: events[index].update({key: 999}))
    for index in range(3):
        add(f"swap_adjacent_{index}", lambda events, index=index: events.__setitem__(slice(index, index + 2), [events[index + 1], events[index]]))
    for index, key in enumerate((
        "plan_freeze_receipt", "execution_receipt", "adjudication_receipt",
        "evidence_gate_receipt",
    )):
        add(f"missing_{key}", lambda events, index=index, key=key: events[index].update({key: False}))
    for key in ("plan_id", "claim_id", "claim_version", "packet_digest"):
        add(f"execution_substitute_{key}", lambda events, key=key: events[1]["execution"].update({key: 999}))
    add("execution_count_short", lambda events: events[1]["execution"].update(passed=3))
    add("execution_expiry_missing", lambda events: events[1]["execution"].update(expiry_declared=False))
    add("adjudication_payload_substitution", lambda events: events[2]["execution"].update(passed=3))
    add("handoff_payload_substitution", lambda events: events[3]["execution"].update(passed=3))
    add("contradiction_blocks_adjudication", lambda events: events[1]["execution"].update(passed=3, contradicted=1, residuals_recorded=True))
    return rows


def lean_surface(issues: list[str]) -> tuple[int, list[str]]:
    completed = subprocess.run(
        ["lake", "env", "lean", str(LEAN.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if completed.returncode:
        issues.append("Lean compilation failed: " + completed.stdout + completed.stderr)
    names = re.findall(r"^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8"), re.MULTILINE)
    missing = sorted(EXPECTED_THEOREMS - set(names))
    if len(names) != 35:
        issues.append(f"Lean theorem count drift: expected 35, observed {len(names)}")
    if missing:
        issues.append("Lean lifecycle theorem surface missing: " + ", ".join(missing))
    return len(names), missing


def run_suite(name: str, validator: Path, expected_valid: int, expected_invalid: int, issues: list[str]) -> dict[str, Any]:
    completed = subprocess.run(["python3", str(validator)], cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        issues.append(f"{name} failed: {completed.stdout}{completed.stderr}")
    return {
        "suite_id": name,
        "valid_count": expected_valid,
        "expected_invalid_count": expected_invalid,
        "suite_passed": completed.returncode == 0,
        "validator_sha256": sha256(validator),
    }


def build() -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    theorem_count, missing_theorems = lean_surface(issues)
    suites = [
        run_suite("context_admission_adequacy", ADMISSION_VALIDATOR, 3, 5, issues),
        run_suite("verification_bandwidth_probe", PROBE_VALIDATOR, 2, 7, issues),
        run_suite("verification_bandwidth_capacity", CAPACITY_VALIDATOR, 3, 5, issues),
    ]
    probe, capacity = load(PROBE_RESULT), load(CAPACITY_RESULT)
    if (probe.get("valid_trace_count"), probe.get("expected_invalid_control_count")) != (2, 7):
        issues.append("verification bandwidth probe result count drift")
    if (capacity.get("valid_trace_count"), capacity.get("expected_invalid_control_count")) != (3, 5):
        issues.append("verification bandwidth capacity result count drift")

    coverage: list[dict[str, str]] = []
    for case_id, p, e, expected in route_cases():
        observed = route(p, e)
        coverage.append({"case_id": case_id, "expected_route": expected, "observed_route": observed})
        if observed != expected:
            issues.append(f"{case_id}: expected {expected}, observed {observed}")
    if {row["observed_route"] for row in coverage} != set(ROUTES):
        issues.append("route coverage incomplete")

    p, e = plan(), execution()
    if plan_errors(p) or execution_errors(p, e) or route(p, e) != "handoff_to_evidence_gate":
        issues.append("reference lifecycle rejected")

    mutation_receipts: list[dict[str, Any]] = []
    for mutation_id, mp, me in mutations():
        errors = [*plan_errors(mp), *execution_errors(mp, me)]
        observed = route(mp, me)
        rejected = bool(errors) or observed != "handoff_to_evidence_gate"
        mutation_receipts.append({
            "mutation_id": mutation_id,
            "rejected": rejected,
            "observed_route": observed,
            "semantic_errors": sorted(set(errors)),
        })
        if not rejected:
            issues.append(mutation_id + ": reached evidence gate")

    final_state, lifecycle_errors = run_lifecycle(lifecycle_events())
    if lifecycle_errors or final_state is None:
        issues.append("reference transaction rejected: " + ", ".join(lifecycle_errors))
    else:
        expected_identity = (101, 201, 1, 301, 1)
        observed_identity = (
            final_state["plan"]["plan_id"],
            final_state["plan"]["claim_id"],
            final_state["plan"]["claim_version"],
            final_state["plan"]["packet_digest"],
            final_state["authority_ceiling"],
        )
        if observed_identity != expected_identity:
            issues.append("reference transaction identity drift")

    lifecycle_receipts: list[dict[str, Any]] = []
    for mutation_id, mutated_events in lifecycle_mutations():
        mutated_final, errors = run_lifecycle(mutated_events)
        rejected = mutated_final is None and bool(errors)
        lifecycle_receipts.append({
            "mutation_id": "lifecycle_" + mutation_id,
            "rejected": rejected,
            "observed_route": "lifecycle_rejected" if rejected else "handed_off",
            "semantic_errors": sorted(set(errors)),
        })
        if not rejected:
            issues.append("lifecycle_" + mutation_id + ": reached handoff")
    mutation_receipts.extend(lifecycle_receipts)

    result = {
        "schema_version": "asi_stack.verification_bandwidth_refinement.v2",
        "result_id": "verification-bandwidth-refinement-2026-07-15-local",
        "source_sha256": {
            "lean_model": sha256(LEAN),
            "context_adequacy_schema": sha256(ADEQUACY_SCHEMA),
            "probe_result": sha256(PROBE_RESULT),
            "capacity_result": sha256(CAPACITY_RESULT),
        },
        "input_suites": suites,
        "lean_theorem_count": theorem_count,
        "lean_required_theorems_missing": missing_theorems,
        "reachable_stage_count": 5,
        "lifecycle_event_count": len(lifecycle_events()),
        "lifecycle_mutation_count": len(lifecycle_receipts),
        "lifecycle_mutation_rejection_count": sum(row["rejected"] for row in lifecycle_receipts),
        "terminal_stage": final_state["stage"] if final_state else "rejected",
        "terminal_support_authority": final_state["support_authority"] if final_state else True,
        "terminal_external_effect_authority": final_state["external_effect_authority"] if final_state else True,
        "reference_route": route(p, e),
        "route_case_count": len(coverage),
        "route_coverage": coverage,
        "mutation_count": len(mutation_receipts),
        "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts),
        "mutation_receipts": mutation_receipts,
        "strongest_effect": "handoff_to_independent_evidence_gate",
        "support_state_effect": "none",
        "non_claims": [
            "This finite authored lifecycle does not measure model verification bandwidth, natural-claim adequacy, contradiction discovery, distractor resistance, evaluator competence, or evaluator independence.",
            "A handoff_to_evidence_gate route is not a support transition, truth judgment, release authorization, safety result, or permission to promote the chapter core.",
            "The consumed suites and mutations do not establish a universal capacity law, deployed ledger or escalation behavior, usefulness, causal advantage, reproduction, transfer, SOTA, AGI, or ASI.",
        ],
    }
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc:
        issues.append("schema: " + exc.message)
    return result, issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, issues = build()
    if issues:
        raise SystemExit("Verification bandwidth refinement failed:\n - " + "\n - ".join(issues))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("Verification bandwidth refinement result stale; run --write")
    print(
        "Verification bandwidth refinement passed: "
        f"3/5 admission, 2/7 contradiction, 3/5 capacity, {result['route_case_count']} routes, "
        f"5 stages, {result['lean_theorem_count']} Lean theorems, "
        f"{result['lifecycle_event_count']} lifecycle events, "
        f"{result['mutation_rejection_count']} mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
