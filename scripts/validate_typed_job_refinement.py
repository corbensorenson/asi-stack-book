#!/usr/bin/env python3
"""Validate the reachable typed-job lifecycle and exact bounded input suites."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments/typed_job_refinement/results/2026-07-15-local.json"
SCHEMA = ROOT / "schemas/typed_job_refinement.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/TypedJobRefinement.lean"
DELIVERY_RESULT = ROOT / "experiments/typed_job_delivery/results/2026-07-02-local.json"
DURABLE_RESULT = ROOT / "experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json"

ACCEPTED = {"accept_lock", "accept_authorization", "accept_dispatch", "accept_execution", "accept_adjudication", "accept_closure"}
EXPECTED_KIND = {
    "idle": "lock_job", "locked": "authorize_job", "authorized": "dispatch_job",
    "dispatched": "execute_job", "executed": "adjudicate_job",
    "adjudicated": "close_job", "closed": "close_job",
}
NEXT_STAGE = {
    "idle": "locked", "locked": "authorized", "authorized": "dispatched",
    "dispatched": "executed", "executed": "adjudicated",
    "adjudicated": "closed", "closed": "closed",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet(event_digest: int = 1, **updates: Any) -> dict[str, Any]:
    value = {
        "job_id": 501, "job_version": 3, "contract_digest": 601,
        "plan_node_digest": 602, "authority_digest": 603,
        "permission_digest": 604, "lease_epoch": 7, "scheduler_digest": 605,
        "consumer_digest": 606, "event_digest": event_digest,
        "parent_contract_present": True, "plan_node_present": True,
        "contract_locked": True, "approval_required": True,
        "approval_recorded": True, "permissions_satisfied": True,
        "lease_active": True, "scheduler_slot_available": True,
        "dispatch_requested": True, "retry_attempted": True,
        "idempotency_key_present": True, "retry_authority_unchanged": True,
        "cancellation_requested": False, "cancellation_acknowledged": False,
        "output_delivered": True, "artifact_refs_present": True,
        "audit_trail_present": True, "verification_passed": True,
        "completion_receipt_present": True, "replay_reference_present": True,
        "residual_owner_present": True, "consumer_acknowledgment_present": True,
        "support_assignment_requested": False, "external_effect_requested": False,
    }
    value.update(updates)
    return value


def event(kind: str, digest: int, **updates: Any) -> dict[str, Any]:
    return {"kind": kind, "packet": packet(digest, **updates)}


def initial_state() -> dict[str, Any]:
    return {
        "stage": "idle", "job_id": 501, "job_version": 3,
        "contract_digest": 601, "plan_node_digest": 602,
        "authority_digest": 603, "permission_digest": 604, "lease_epoch": 7,
        "scheduler_digest": 605, "consumer_digest": 606, "last_event_digest": 0,
        "receipt_count": 0, "execution_observation_count": 0,
        "support_assignment_count": 0, "external_effect_count": 0,
    }


def exact_job(state: dict[str, Any], p: dict[str, Any]) -> bool:
    return all(p[key] == state[key] for key in ("job_id", "job_version", "consumer_digest"))


def exact_contract(state: dict[str, Any], p: dict[str, Any]) -> bool:
    return all(p[key] == state[key] for key in (
        "contract_digest", "plan_node_digest", "authority_digest",
        "permission_digest", "lease_epoch", "scheduler_digest"))


def route_for(state: dict[str, Any], evt: dict[str, Any]) -> str:
    p = evt["packet"]
    if evt["kind"] != EXPECTED_KIND[state["stage"]]: return "reject_wrong_stage"
    if not exact_job(state, p): return "reject_job_substitution"
    if not exact_contract(state, p): return "reject_contract_substitution"
    if p["event_digest"] == state["last_event_digest"]: return "reject_event_replay"
    if p["support_assignment_requested"] or p["external_effect_requested"]: return "reject_authority_leak"
    stage = state["stage"]
    if stage == "idle":
        if not p["parent_contract_present"] or not p["plan_node_present"] or not p["contract_locked"]: return "request_locked_contract"
        return "accept_lock"
    if stage == "locked":
        if p["approval_required"] and not p["approval_recorded"]: return "request_approval"
        if not p["permissions_satisfied"]: return "request_permissions"
        if not p["lease_active"]: return "request_active_lease"
        return "accept_authorization"
    if stage == "authorized":
        if not p["lease_active"]: return "request_active_lease"
        if not p["scheduler_slot_available"]: return "request_scheduler_slot"
        if not p["dispatch_requested"]: return "request_dispatch"
        return "accept_dispatch"
    if stage == "dispatched":
        if p["cancellation_requested"] and not p["cancellation_acknowledged"]: return "request_cancellation_acknowledgment"
        if p["cancellation_acknowledged"] and p["output_delivered"]: return "reject_post_cancellation_execution"
        if p["retry_attempted"] and not p["idempotency_key_present"]: return "request_idempotency_key"
        if p["retry_attempted"] and not p["retry_authority_unchanged"]: return "reject_retry_authority_widening"
        if not p["output_delivered"] or not p["artifact_refs_present"]: return "request_output_artifacts"
        if not p["audit_trail_present"]: return "request_audit_trail"
        return "accept_execution"
    if stage == "executed":
        if not p["verification_passed"]: return "request_verification"
        if not p["completion_receipt_present"]: return "request_completion_receipt"
        if not p["replay_reference_present"]: return "request_replay_reference"
        if not p["residual_owner_present"]: return "request_residual_owner"
        return "accept_adjudication"
    if stage == "adjudicated":
        if not p["consumer_acknowledgment_present"]: return "request_consumer_acknowledgment"
        return "accept_closure"
    return "reject_wrong_stage"


def apply_event(state: dict[str, Any], evt: dict[str, Any]) -> tuple[dict[str, Any], str]:
    route = route_for(state, evt)
    if route not in ACCEPTED: return copy.deepcopy(state), route
    updated = copy.deepcopy(state); previous = state["stage"]
    updated["stage"] = NEXT_STAGE[previous]
    updated["last_event_digest"] = evt["packet"]["event_digest"]
    updated["receipt_count"] += 1
    if previous == "dispatched": updated["execution_observation_count"] += 1
    return updated, route


def canonical_events() -> list[dict[str, Any]]:
    return [
        event("lock_job", 1), event("authorize_job", 2), event("dispatch_job", 3),
        event("execute_job", 4), event("adjudicate_job", 5), event("close_job", 6),
    ]


def run(events: list[dict[str, Any]]) -> tuple[dict[str, Any], str]:
    state = initial_state(); route = ""
    for evt in events:
        state, route = apply_event(state, evt)
        if route not in ACCEPTED: return state, route
    return state, route


def states() -> list[dict[str, Any]]:
    rows = [initial_state()]; current = rows[0]
    for evt in canonical_events():
        current, route = apply_event(current, evt)
        if route not in ACCEPTED: raise AssertionError(route)
        rows.append(current)
    return rows


def route_cases() -> list[tuple[str, dict[str, Any], dict[str, Any], str]]:
    idle, locked, authorized, dispatched, executed, adjudicated, closed = states()
    return [
        ("wrong_stage", idle, event("authorize_job", 20), "reject_wrong_stage"),
        ("job_substitution", idle, event("lock_job", 20, job_id=999), "reject_job_substitution"),
        ("contract_substitution", idle, event("lock_job", 20, contract_digest=999), "reject_contract_substitution"),
        ("event_replay", locked, event("authorize_job", 1), "reject_event_replay"),
        ("authority_leak", idle, event("lock_job", 20, support_assignment_requested=True), "reject_authority_leak"),
        ("contract_unlocked", idle, event("lock_job", 20, contract_locked=False), "request_locked_contract"),
        ("approval_missing", locked, event("authorize_job", 20, approval_recorded=False), "request_approval"),
        ("permissions_missing", locked, event("authorize_job", 20, permissions_satisfied=False), "request_permissions"),
        ("lease_missing", locked, event("authorize_job", 20, lease_active=False), "request_active_lease"),
        ("scheduler_missing", authorized, event("dispatch_job", 20, scheduler_slot_available=False), "request_scheduler_slot"),
        ("dispatch_missing", authorized, event("dispatch_job", 20, dispatch_requested=False), "request_dispatch"),
        ("idempotency_missing", dispatched, event("execute_job", 20, idempotency_key_present=False), "request_idempotency_key"),
        ("retry_authority_widened", dispatched, event("execute_job", 20, retry_authority_unchanged=False), "reject_retry_authority_widening"),
        ("cancellation_unacknowledged", dispatched, event("execute_job", 20, cancellation_requested=True), "request_cancellation_acknowledgment"),
        ("post_cancellation_output", dispatched, event("execute_job", 20, cancellation_acknowledged=True), "reject_post_cancellation_execution"),
        ("output_missing", dispatched, event("execute_job", 20, output_delivered=False), "request_output_artifacts"),
        ("audit_missing", dispatched, event("execute_job", 20, audit_trail_present=False), "request_audit_trail"),
        ("verification_missing", executed, event("adjudicate_job", 20, verification_passed=False), "request_verification"),
        ("receipt_missing", executed, event("adjudicate_job", 20, completion_receipt_present=False), "request_completion_receipt"),
        ("replay_missing", executed, event("adjudicate_job", 20, replay_reference_present=False), "request_replay_reference"),
        ("residual_owner_missing", executed, event("adjudicate_job", 20, residual_owner_present=False), "request_residual_owner"),
        ("consumer_ack_missing", adjudicated, event("close_job", 20, consumer_acknowledgment_present=False), "request_consumer_acknowledgment"),
        ("lock_accepted", idle, canonical_events()[0], "accept_lock"),
        ("authorization_accepted", locked, canonical_events()[1], "accept_authorization"),
        ("dispatch_accepted", authorized, canonical_events()[2], "accept_dispatch"),
        ("execution_accepted", dispatched, canonical_events()[3], "accept_execution"),
        ("adjudication_accepted", executed, canonical_events()[4], "accept_adjudication"),
        ("closure_accepted", adjudicated, canonical_events()[5], "accept_closure"),
    ]


def mutated(index: int, **updates: Any) -> list[dict[str, Any]]:
    rows = canonical_events(); rows[index] = copy.deepcopy(rows[index]); rows[index]["packet"].update(updates); return rows


def mutations() -> list[tuple[str, list[dict[str, Any]]]]:
    rows: list[tuple[str, list[dict[str, Any]]]] = []
    for field in ("job_id", "job_version", "contract_digest", "plan_node_digest", "authority_digest", "permission_digest", "lease_epoch", "scheduler_digest", "consumer_digest"):
        rows.append((f"lock_{field}", mutated(0, **{field: 999})))
    rows.extend([
        ("lock_parent_missing", mutated(0, parent_contract_present=False)),
        ("lock_plan_missing", mutated(0, plan_node_present=False)),
        ("lock_unlocked", mutated(0, contract_locked=False)),
        ("lock_support_leak", mutated(0, support_assignment_requested=True)),
        ("lock_external_effect", mutated(0, external_effect_requested=True)),
        ("authorize_approval_missing", mutated(1, approval_recorded=False)),
        ("authorize_permissions_missing", mutated(1, permissions_satisfied=False)),
        ("authorize_lease_missing", mutated(1, lease_active=False)),
        ("authorize_replay", mutated(1, event_digest=1)),
        ("dispatch_lease_missing", mutated(2, lease_active=False)),
        ("dispatch_slot_missing", mutated(2, scheduler_slot_available=False)),
        ("dispatch_request_missing", mutated(2, dispatch_requested=False)),
        ("dispatch_contract_substitution", mutated(2, contract_digest=999)),
        ("dispatch_authority_substitution", mutated(2, authority_digest=999)),
        ("execute_cancel_unacknowledged", mutated(3, cancellation_requested=True)),
        ("execute_post_cancel", mutated(3, cancellation_acknowledged=True)),
        ("execute_idempotency_missing", mutated(3, idempotency_key_present=False)),
        ("execute_authority_widening", mutated(3, retry_authority_unchanged=False)),
        ("execute_output_missing", mutated(3, output_delivered=False)),
        ("execute_artifact_missing", mutated(3, artifact_refs_present=False)),
        ("execute_audit_missing", mutated(3, audit_trail_present=False)),
        ("execute_replay", mutated(3, event_digest=3)),
        ("execute_support_leak", mutated(3, support_assignment_requested=True)),
        ("execute_external_effect", mutated(3, external_effect_requested=True)),
        ("adjudicate_verification_missing", mutated(4, verification_passed=False)),
        ("adjudicate_receipt_missing", mutated(4, completion_receipt_present=False)),
        ("adjudicate_replay_missing", mutated(4, replay_reference_present=False)),
        ("adjudicate_residual_owner_missing", mutated(4, residual_owner_present=False)),
        ("adjudicate_job_substitution", mutated(4, job_id=999)),
        ("close_consumer_missing", mutated(5, consumer_acknowledgment_present=False)),
        ("close_replay", mutated(5, event_digest=5)),
        ("close_support_leak", mutated(5, support_assignment_requested=True)),
        ("close_external_effect", mutated(5, external_effect_requested=True)),
    ])
    return rows


def run_validator(name: str) -> None:
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / name)], cwd=ROOT, capture_output=True, text=True)
    if completed.returncode: raise AssertionError(f"{name} failed: {completed.stdout}{completed.stderr}")


def build_result() -> dict[str, Any]:
    run_validator("validate_typed_job_delivery_probe.py")
    run_validator("validate_typed_job_durable_lifecycle_probe.py")
    delivery = json.loads(DELIVERY_RESULT.read_text()); durable = json.loads(DURABLE_RESULT.read_text())
    coverage = []
    for case_id, state, evt, expected in route_cases():
        observed = route_for(state, evt)
        if observed != expected: raise AssertionError(f"{case_id}: expected {expected}, got {observed}")
        coverage.append({"case_id": case_id, "expected_route": expected, "observed_route": observed})
    receipts = []
    for mutation_id, events in mutations():
        state, failure = run(events)
        rejected = state["stage"] != "closed" and failure not in ACCEPTED
        if not rejected: raise AssertionError(f"mutation accepted: {mutation_id}")
        receipts.append({"mutation_id": mutation_id, "rejected": True, "terminal_stage": state["stage"], "failure_route": failure})
    final, final_route = run(canonical_events())
    if final_route != "accept_closure" or final["stage"] != "closed": raise AssertionError("canonical lifecycle failed")
    return {
        "schema_version": "asi_stack.typed_job_refinement.v1",
        "result_id": "typed-job-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha256(LEAN), "delivery_result": sha256(DELIVERY_RESULT), "durable_result": sha256(DURABLE_RESULT)},
        "input_suites": [
            {"suite_id": "typed_job_delivery", "valid_count": delivery["valid_trace_count"], "expected_invalid_count": delivery["expected_invalid_control_count"], "suite_passed": delivery["verification_result"] == "pass", "validator_sha256": sha256(ROOT / "scripts/validate_typed_job_delivery_probe.py")},
            {"suite_id": "typed_job_durable_lifecycle", "valid_count": durable["valid_trace_count"], "expected_invalid_count": durable["expected_invalid_control_count"], "suite_passed": durable["verification_result"] == "pass", "validator_sha256": sha256(ROOT / "scripts/validate_typed_job_durable_lifecycle_probe.py")},
        ],
        "reachable_stage_count": 7, "route_case_count": len(coverage), "route_coverage": coverage,
        "mutation_count": len(receipts), "mutation_rejection_count": len(receipts), "mutation_receipts": receipts,
        "final_state": {k: final[k] for k in ("stage", "receipt_count", "execution_observation_count", "support_assignment_count", "external_effect_count")},
        "support_state_effect": "none",
        "non_claims": [
            "No scheduler quality, worker or model capability, task success, output truth, or verification soundness is established.",
            "No idempotence in fact, approval-service correctness, permission enforcement, lease service, cancellation efficacy, or retry recovery is established.",
            "No artifact truth, audit completeness, completion-receipt correctness, replay correctness, or consumer behavior is established.",
            "No external effect is executed and no support, evidence, readiness, or release state is assigned.",
            "No natural workload, useful-throughput advantage, cost advantage, causality, safety, deployment, reproduction, or transfer is established.",
            "No chapter-core support state changes; the support-state effect is none.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result = build_result(); jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text())).validate(result)
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n")
    elif not RESULT.exists() or json.loads(RESULT.read_text()) != result:
        raise SystemExit(f"{RESULT.relative_to(ROOT)} is missing or stale; rerun with --write")
    print(f"Typed-job refinement passed: 2/7 delivery, 2/9 durable, 28 routes, 7 stages, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()
