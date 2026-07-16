#!/usr/bin/env python3
"""Validate the reachable Tribunal lifecycle and exact bounded input suites."""

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
RESULT = ROOT / "experiments/tribunal_refinement/results/2026-07-15-local.json"
SCHEMA = ROOT / "schemas/tribunal_refinement.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/TribunalRefinement.lean"
TRIBUNAL_SCHEMA = ROOT / "schemas/tribunal_review_record.schema.json"
METHOD_RECORD = ROOT / "tests/fixtures/protocol_records/tribunal_method_independence_record.valid.json"
TRIBUNAL_FIXTURES = ROOT / "experiments/tribunal_review/fixtures"
METHOD_MUTATIONS = ROOT / "experiments/tribunal_method_independence/fixtures"

ACCEPTED = {"accept_review_request", "accept_dossier_binding", "accept_panel_run", "accept_verdict", "accept_acknowledgment", "accept_appeal_resolution"}
EXPECTED_KIND = {
    "idle": "request_review", "requested": "bind_dossier", "dossier_bound": "run_panel",
    "panel_run": "issue_verdict", "verdict_issued": "acknowledge_verdict",
    "acknowledged": "resolve_appeal", "appeal_resolved": "resolve_appeal",
}
NEXT_STAGE = {
    "idle": "requested", "requested": "dossier_bound", "dossier_bound": "panel_run",
    "panel_run": "verdict_issued", "verdict_issued": "acknowledged",
    "acknowledged": "appeal_resolved", "appeal_resolved": "appeal_resolved",
}
ACTION_VERDICTS = {"revise", "reject", "block"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet(event_digest: int = 1, **updates: Any) -> dict[str, Any]:
    value = {
        "case_id": 71, "case_version": 4, "target_digest": 101,
        "evidence_version": 9, "evidence_digest": 201, "dossier_digest": 202,
        "panel_digest": 203, "policy_digest": 301, "consumer_digest": 401,
        "verdict_version": 2, "event_digest": event_digest,
        "review_required": True, "review_requested": True,
        "dossier_present": True, "evidence_refs_present": True,
        "high_risk": True, "adversarial_probe_present": True,
        "reviewer_count": 3, "independence_group_count": 3,
        "independence_graph_acyclic": True, "shared_evidence_risk_recorded": True,
        "falsification_attempted": True, "abstention_present": True,
        "abstention_preserved": True, "veto_present": True, "veto_preserved": True,
        "prior_verdict_reused": True, "evidence_unchanged": True,
        "reuse_guard_present": True, "default_approval_used": False,
        "dissent_present": True, "dissent_preserved": True,
        "action_required": True, "required_actions_present": True,
        "constraints_present": True, "residual_present": True,
        "appeal_available": True, "appeal_requested": True, "appeal_recorded": True,
        "support_change_requested": True, "evidence_owner_handoff_present": True,
        "consumer_acknowledgment_present": True,
        "support_assignment_requested": False, "external_effect_requested": False,
        "verdict": "revise",
    }
    value.update(updates)
    return value


def event(kind: str, digest: int, **updates: Any) -> dict[str, Any]:
    return {"kind": kind, "packet": packet(digest, **updates)}


def initial_state() -> dict[str, Any]:
    return {
        "stage": "idle", "case_id": 71, "case_version": 4, "target_digest": 101,
        "evidence_version": 9, "evidence_digest": 201, "dossier_digest": 202,
        "panel_digest": 203, "policy_digest": 301, "consumer_digest": 401,
        "verdict_version": 2, "last_event_digest": 0, "panel_accepted": False,
        "verdict": "none", "receipt_count": 0,
        "support_assignment_count": 0, "external_effect_count": 0,
    }


def exact_case(state: dict[str, Any], p: dict[str, Any]) -> bool:
    return all(p[k] == state[k] for k in ("case_id", "case_version", "target_digest", "policy_digest", "consumer_digest", "verdict_version"))


def exact_evidence(state: dict[str, Any], p: dict[str, Any]) -> bool:
    return all(p[k] == state[k] for k in ("evidence_version", "evidence_digest", "dossier_digest", "panel_digest"))


def route_for(state: dict[str, Any], evt: dict[str, Any]) -> str:
    p = evt["packet"]
    if evt["kind"] != EXPECTED_KIND[state["stage"]]: return "reject_wrong_stage"
    if not exact_case(state, p): return "reject_case_substitution"
    if state["stage"] != "idle" and not exact_evidence(state, p): return "reject_evidence_substitution"
    if p["event_digest"] == state["last_event_digest"]: return "reject_event_replay"
    if p["support_assignment_requested"] or p["external_effect_requested"]: return "reject_authority_leak"
    stage = state["stage"]
    if stage == "idle":
        if p["review_required"] and not p["review_requested"]: return "request_review"
        return "accept_review_request"
    if stage == "requested":
        if not p["dossier_present"] or not p["evidence_refs_present"]: return "request_dossier_and_evidence"
        return "accept_dossier_binding"
    if stage == "dossier_bound":
        if p["high_risk"] and not p["adversarial_probe_present"]: return "request_adversarial_probe"
        if p["high_risk"] and p["reviewer_count"] < 3: return "request_independent_panel"
        if p["independence_group_count"] != p["reviewer_count"] or not p["independence_graph_acyclic"] or not p["shared_evidence_risk_recorded"]: return "request_independence_graph"
        if not p["falsification_attempted"]: return "request_falsification"
        if p["abstention_present"] and not p["abstention_preserved"]: return "preserve_abstention"
        if p["veto_present"] and not p["veto_preserved"]: return "preserve_veto"
        return "accept_panel_run"
    if stage == "panel_run":
        if p["prior_verdict_reused"] and (not p["evidence_unchanged"] or not p["reuse_guard_present"]): return "reject_changed_evidence_reuse"
        if p["default_approval_used"]: return "reject_default_approval"
        if p["dissent_present"] and not p["dissent_preserved"]: return "preserve_dissent"
        if (p["action_required"] or p["verdict"] in ACTION_VERDICTS) and (not p["required_actions_present"] or not p["constraints_present"]): return "request_actions_and_constraints"
        if not p["residual_present"]: return "request_residual"
        if not p["appeal_available"]: return "request_appeal_path"
        if p["support_change_requested"] and not p["evidence_owner_handoff_present"]: return "handoff_to_evidence_owner"
        if p["verdict"] == "none": return "reject_default_approval"
        return "accept_verdict"
    if stage == "verdict_issued":
        if p["verdict"] != state["verdict"]: return "reject_case_substitution"
        if not p["consumer_acknowledgment_present"]: return "request_consumer_acknowledgment"
        return "accept_acknowledgment"
    if stage == "acknowledged":
        if p["verdict"] != state["verdict"]: return "reject_case_substitution"
        if p["appeal_requested"] and not p["appeal_recorded"]: return "request_appeal_resolution"
        return "accept_appeal_resolution"
    return "reject_wrong_stage"


def apply_event(state: dict[str, Any], evt: dict[str, Any]) -> tuple[dict[str, Any], str]:
    route = route_for(state, evt)
    if route not in ACCEPTED: return copy.deepcopy(state), route
    updated = copy.deepcopy(state); previous = state["stage"]
    updated["stage"] = NEXT_STAGE[previous]
    updated["last_event_digest"] = evt["packet"]["event_digest"]
    updated["receipt_count"] += 1
    if previous == "dossier_bound": updated["panel_accepted"] = True
    if previous == "panel_run": updated["verdict"] = evt["packet"]["verdict"]
    return updated, route


def canonical_events() -> list[dict[str, Any]]:
    return [event("request_review", 1), event("bind_dossier", 2), event("run_panel", 3), event("issue_verdict", 4), event("acknowledge_verdict", 5), event("resolve_appeal", 6)]


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
    idle, requested, dossier, panel, verdict, ack, final = states()
    return [
        ("wrong_stage", idle, event("bind_dossier", 20), "reject_wrong_stage"),
        ("case_substitution", idle, event("request_review", 20, case_id=99), "reject_case_substitution"),
        ("evidence_substitution", requested, event("bind_dossier", 20, evidence_digest=99), "reject_evidence_substitution"),
        ("event_replay", requested, event("bind_dossier", 1), "reject_event_replay"),
        ("authority_leak", idle, event("request_review", 20, support_assignment_requested=True), "reject_authority_leak"),
        ("review_missing", idle, event("request_review", 20, review_requested=False), "request_review"),
        ("dossier_missing", requested, event("bind_dossier", 20, dossier_present=False), "request_dossier_and_evidence"),
        ("probe_missing", dossier, event("run_panel", 20, adversarial_probe_present=False), "request_adversarial_probe"),
        ("panel_too_small", dossier, event("run_panel", 20, reviewer_count=2, independence_group_count=2), "request_independent_panel"),
        ("independence_graph_bad", dossier, event("run_panel", 20, independence_graph_acyclic=False), "request_independence_graph"),
        ("falsification_missing", dossier, event("run_panel", 20, falsification_attempted=False), "request_falsification"),
        ("abstention_erased", dossier, event("run_panel", 20, abstention_preserved=False), "preserve_abstention"),
        ("veto_erased", dossier, event("run_panel", 20, veto_preserved=False), "preserve_veto"),
        ("changed_evidence_reuse", panel, event("issue_verdict", 20, evidence_unchanged=False), "reject_changed_evidence_reuse"),
        ("default_approval", panel, event("issue_verdict", 20, default_approval_used=True), "reject_default_approval"),
        ("dissent_erased", panel, event("issue_verdict", 20, dissent_preserved=False), "preserve_dissent"),
        ("actions_missing", panel, event("issue_verdict", 20, required_actions_present=False), "request_actions_and_constraints"),
        ("residual_missing", panel, event("issue_verdict", 20, residual_present=False), "request_residual"),
        ("appeal_missing", panel, event("issue_verdict", 20, appeal_available=False), "request_appeal_path"),
        ("owner_handoff_missing", panel, event("issue_verdict", 20, evidence_owner_handoff_present=False), "handoff_to_evidence_owner"),
        ("consumer_ack_missing", verdict, event("acknowledge_verdict", 20, consumer_acknowledgment_present=False), "request_consumer_acknowledgment"),
        ("appeal_resolution_missing", ack, event("resolve_appeal", 20, appeal_recorded=False), "request_appeal_resolution"),
        ("review_requested", idle, canonical_events()[0], "accept_review_request"),
        ("dossier_bound", requested, canonical_events()[1], "accept_dossier_binding"),
        ("panel_run", dossier, canonical_events()[2], "accept_panel_run"),
        ("verdict_issued", panel, canonical_events()[3], "accept_verdict"),
        ("verdict_acknowledged", verdict, canonical_events()[4], "accept_acknowledgment"),
        ("appeal_resolved", ack, canonical_events()[5], "accept_appeal_resolution"),
    ]


def mutated(index: int, **updates: Any) -> list[dict[str, Any]]:
    rows = canonical_events(); rows[index] = copy.deepcopy(rows[index]); rows[index]["packet"].update(updates); return rows


def mutations() -> list[tuple[str, list[dict[str, Any]]]]:
    rows: list[tuple[str, list[dict[str, Any]]]] = []
    for field in ("case_id", "case_version", "target_digest", "policy_digest", "consumer_digest", "verdict_version"):
        rows.append((f"request_{field}", mutated(0, **{field: 999})))
    rows.extend([
        ("request_review_missing", mutated(0, review_requested=False)),
        ("request_support_leak", mutated(0, support_assignment_requested=True)),
        ("request_external_effect", mutated(0, external_effect_requested=True)),
        ("bind_evidence_version", mutated(1, evidence_version=999)),
        ("bind_evidence_digest", mutated(1, evidence_digest=999)),
        ("bind_dossier_digest", mutated(1, dossier_digest=999)),
        ("bind_panel_digest", mutated(1, panel_digest=999)),
        ("bind_dossier_missing", mutated(1, dossier_present=False)),
        ("bind_evidence_refs_missing", mutated(1, evidence_refs_present=False)),
        ("panel_probe_missing", mutated(2, adversarial_probe_present=False)),
        ("panel_reviewer_count", mutated(2, reviewer_count=2, independence_group_count=2)),
        ("panel_shared_group", mutated(2, independence_group_count=2)),
        ("panel_independence_cycle", mutated(2, independence_graph_acyclic=False)),
        ("panel_shared_evidence_risk", mutated(2, shared_evidence_risk_recorded=False)),
        ("panel_falsification_missing", mutated(2, falsification_attempted=False)),
        ("panel_abstention_erased", mutated(2, abstention_preserved=False)),
        ("panel_veto_erased", mutated(2, veto_preserved=False)),
        ("panel_event_replay", mutated(2, event_digest=2)),
        ("verdict_changed_evidence", mutated(3, evidence_unchanged=False)),
        ("verdict_reuse_guard_missing", mutated(3, reuse_guard_present=False)),
        ("verdict_default_approval", mutated(3, default_approval_used=True)),
        ("verdict_dissent_erased", mutated(3, dissent_preserved=False)),
        ("verdict_actions_missing", mutated(3, required_actions_present=False)),
        ("verdict_constraints_missing", mutated(3, constraints_present=False)),
        ("verdict_explicit_action_required", mutated(3, verdict="accept_scoped", action_required=True, required_actions_present=False)),
        ("verdict_residual_missing", mutated(3, residual_present=False)),
        ("verdict_appeal_missing", mutated(3, appeal_available=False)),
        ("verdict_owner_handoff_missing", mutated(3, evidence_owner_handoff_present=False)),
        ("verdict_none", mutated(3, verdict="none")),
        ("verdict_support_leak", mutated(3, support_assignment_requested=True)),
        ("verdict_external_effect", mutated(3, external_effect_requested=True)),
        ("ack_verdict_substitution", mutated(4, verdict="reject")),
        ("ack_consumer_missing", mutated(4, consumer_acknowledgment_present=False)),
        ("ack_evidence_substitution", mutated(4, evidence_digest=999)),
        ("appeal_verdict_substitution", mutated(5, verdict="reject")),
        ("appeal_record_missing", mutated(5, appeal_recorded=False)),
        ("appeal_event_replay", mutated(5, event_digest=5)),
        ("appeal_support_leak", mutated(5, support_assignment_requested=True)),
        ("appeal_external_effect", mutated(5, external_effect_requested=True)),
    ])
    return rows


def run_validator(name: str) -> None:
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / name)], cwd=ROOT, capture_output=True, text=True)
    if completed.returncode: raise AssertionError(f"{name} failed: {completed.stdout}{completed.stderr}")


def build_result() -> dict[str, Any]:
    run_validator("validate_tribunal_review.py"); run_validator("validate_tribunal_method_independence.py")
    valid_count = len(list(TRIBUNAL_FIXTURES.glob("valid_*.json")))
    invalid_count = len(list(TRIBUNAL_FIXTURES.glob("invalid_*.json")))
    method_invalid = len(list(METHOD_MUTATIONS.glob("invalid_*.json")))
    coverage = []
    for case_id, state, evt, expected in route_cases():
        observed = route_for(state, evt)
        if observed != expected: raise AssertionError(f"{case_id}: expected {expected}, got {observed}")
        coverage.append({"case_id": case_id, "expected_route": expected, "observed_route": observed})
    receipts = []
    for mutation_id, events in mutations():
        state, failure = run(events)
        rejected = state["stage"] != "appeal_resolved" and failure not in ACCEPTED
        if not rejected: raise AssertionError(f"mutation accepted: {mutation_id}")
        receipts.append({"mutation_id": mutation_id, "rejected": True, "terminal_stage": state["stage"], "failure_route": failure})
    final, final_route = run(canonical_events())
    if final_route != "accept_appeal_resolution" or final["stage"] != "appeal_resolved": raise AssertionError("canonical lifecycle failed")
    return {
        "schema_version": "asi_stack.tribunal_refinement.v1",
        "result_id": "tribunal-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha256(LEAN), "tribunal_review_schema": sha256(TRIBUNAL_SCHEMA), "method_independence_record": sha256(METHOD_RECORD)},
        "input_suites": [
            {"suite_id": "tribunal_review", "valid_count": valid_count, "expected_invalid_count": invalid_count, "suite_passed": True, "validator_sha256": sha256(ROOT / "scripts/validate_tribunal_review.py")},
            {"suite_id": "tribunal_method_independence", "valid_count": 1, "expected_invalid_count": method_invalid, "suite_passed": True, "validator_sha256": sha256(ROOT / "scripts/validate_tribunal_method_independence.py")},
        ],
        "reachable_stage_count": 7, "route_case_count": len(coverage), "route_coverage": coverage,
        "mutation_count": len(receipts), "mutation_rejection_count": len(receipts), "mutation_receipts": receipts,
        "final_state": {k: final[k] for k in ("stage", "receipt_count", "panel_accepted", "verdict", "support_assignment_count", "external_effect_count")},
        "support_state_effect": "none",
        "non_claims": [
            "No reviewer competence, independence in fact, or error decorrelation is established.",
            "No dossier completeness, evidence truth, falsification quality, or probe efficacy is established.",
            "No verdict correctness, consensus quality, institutional legitimacy, or fair process is established.",
            "No action adequacy, constraint efficacy, appeal quality, or consumer behavior is established.",
            "No claim truth, evidence adequacy, support assignment, external effect, or release authority is established.",
            "No natural workload, model judge, debate system, live tribunal, or affected-party outcome is measured.",
            "No usefulness, causal advantage, safety, cost advantage, deployment, reproduction, or transfer is established.",
            "No chapter-core support state changes; the support-state effect is none.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result = build_result(); schema = json.loads(SCHEMA.read_text()); jsonschema.Draft202012Validator(schema).validate(result)
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n")
    elif not RESULT.exists() or json.loads(RESULT.read_text()) != result:
        raise SystemExit(f"{RESULT.relative_to(ROOT)} is missing or stale; rerun with --write")
    print(f"Tribunal refinement passed: 3/5 review fixtures, 1/11 method-independence lifecycle, 28 routes, 7 stages, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()
