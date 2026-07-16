#!/usr/bin/env python3
"""Independently consume the append-only Claim Ledger lifecycle and legacy suites."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ClaimLedgerRefinement.lean"
SCHEMA = ROOT / "schemas/claim_ledger_refinement.schema.json"
RESULT = ROOT / "experiments/claim_ledger_refinement/results/2026-07-15-local.json"
REVISION_VALIDATOR = ROOT / "scripts/validate_claim_ledger_revision.py"
REVISION_FIXTURES = ROOT / "experiments/claim_ledger_revision/fixtures"
HISTORICAL_VALIDATOR = ROOT / "scripts/validate_contradiction_revision_lifecycle.py"
HISTORICAL_RECORD = ROOT / "tests/fixtures/protocol_records/contradiction_revision_lifecycle_record.valid.json"
HISTORICAL_SCHEMA = ROOT / "schemas/contradiction_revision_lifecycle_record.schema.json"

ROUTES = {
    "reject_wrong_stage", "reject_stale_base", "reject_event_substitution",
    "reject_ledger_authority_leak", "block_open_contradiction", "handoff_to_evidence_owner",
    "request_history_and_non_overwrite", "request_revision_reason", "request_residual_record",
    "request_dependency_closure", "request_ontology_migration", "request_surface_plan",
    "request_surface_acknowledgment", "accept_proposal", "authorize_append",
    "materialize_view", "acknowledge_surfaces",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(directory.glob("*.json")):
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def initial_state() -> dict[str, Any]:
    return {
        "claim_id": 101, "ledger_version": 7, "head_digest": 7001,
        "semantic_version": 3, "ontology_version": 2, "support_rank": 1,
        "stage": "idle", "pending_event_digest": None, "required_surface_acks": 0,
        "observed_surface_acks": 0, "materialized_ledger_version": 7,
        "append_count": 7, "external_effects": 0,
    }


def reference_event(kind: str = "propose") -> dict[str, Any]:
    return {
        "kind": kind, "action": "request_promotion", "event_digest": 8001,
        "claim_id": 101, "base_ledger_version": 7, "prior_head_digest": 7001,
        "prior_semantic_version": 3, "next_semantic_version": 4,
        "prior_ontology_version": 2, "next_ontology_version": 3,
        "prior_support_rank": 1, "next_support_rank": 2,
        "ledger_self_approves_support": False, "external_effect_requested": False,
        "evidence_owner_receipt_present": True, "open_contradiction": False,
        "history_refs_present": True, "non_overwrite_attestation_present": True,
        "revision_reason_present": True, "residual_required": False,
        "residual_refs_present": True, "dependency_closure_complete": True,
        "ontology_migration_receipt_present": True, "surface_plan_complete": True,
        "required_surface_acks": 3, "observed_surface_acks": 0,
        "surface_acknowledgment_receipt_present": False,
    }


def exact_base(state: dict[str, Any], event: dict[str, Any]) -> bool:
    return all((
        event["claim_id"] == state["claim_id"],
        event["base_ledger_version"] == state["ledger_version"],
        event["prior_head_digest"] == state["head_digest"],
        event["prior_semantic_version"] == state["semantic_version"],
        event["prior_ontology_version"] == state["ontology_version"],
        event["prior_support_rank"] == state["support_rank"],
    ))


def route(state: dict[str, Any], event: dict[str, Any]) -> str:
    kind = event["kind"]
    if kind == "propose":
        if state["stage"] != "idle": return "reject_wrong_stage"
        if not exact_base(state, event) or event["next_semantic_version"] != state["semantic_version"] + 1: return "reject_stale_base"
        if event["ledger_self_approves_support"] or event["external_effect_requested"]: return "reject_ledger_authority_leak"
        moves_up = event["prior_support_rank"] < event["next_support_rank"]
        if moves_up and event["open_contradiction"]: return "block_open_contradiction"
        if moves_up and not event["evidence_owner_receipt_present"]: return "handoff_to_evidence_owner"
        if not event["history_refs_present"] or not event["non_overwrite_attestation_present"]: return "request_history_and_non_overwrite"
        if not event["revision_reason_present"]: return "request_revision_reason"
        if event["residual_required"] and not event["residual_refs_present"]: return "request_residual_record"
        if not event["dependency_closure_complete"]: return "request_dependency_closure"
        if event["prior_ontology_version"] != event["next_ontology_version"] and not event["ontology_migration_receipt_present"]: return "request_ontology_migration"
        if not event["surface_plan_complete"] or event["required_surface_acks"] == 0: return "request_surface_plan"
        return "accept_proposal"
    if kind == "append":
        if state["stage"] != "proposed": return "reject_wrong_stage"
        if state["pending_event_digest"] != event["event_digest"]: return "reject_event_substitution"
        if not exact_base(state, event): return "reject_stale_base"
        return "authorize_append"
    if kind == "materialize":
        if state["stage"] != "appended": return "reject_wrong_stage"
        if state["head_digest"] != event["event_digest"] or state["ledger_version"] != event["base_ledger_version"] + 1: return "reject_event_substitution"
        return "materialize_view"
    if kind == "acknowledge":
        if state["stage"] != "materialized": return "reject_wrong_stage"
        if state["head_digest"] != event["event_digest"] or state["materialized_ledger_version"] != state["ledger_version"]: return "reject_event_substitution"
        if not event["surface_acknowledgment_receipt_present"] or event["observed_surface_acks"] != state["required_surface_acks"]: return "request_surface_acknowledgment"
        return "acknowledge_surfaces"
    return "reject_event_substitution"


POSITIVE = {"accept_proposal", "authorize_append", "materialize_view", "acknowledge_surfaces"}


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    nxt = copy.deepcopy(state)
    if event["kind"] == "propose":
        nxt.update(stage="proposed", pending_event_digest=event["event_digest"], required_surface_acks=event["required_surface_acks"], observed_surface_acks=0)
    elif event["kind"] == "append":
        nxt.update(ledger_version=state["ledger_version"] + 1, head_digest=event["event_digest"], semantic_version=event["next_semantic_version"], ontology_version=event["next_ontology_version"], support_rank=event["next_support_rank"], stage="appended", pending_event_digest=None, append_count=state["append_count"] + 1)
    elif event["kind"] == "materialize":
        nxt.update(stage="materialized", materialized_ledger_version=state["ledger_version"])
    elif event["kind"] == "acknowledge":
        nxt.update(stage="acknowledged", observed_surface_acks=event["observed_surface_acks"])
    return nxt


def run(events: list[dict[str, Any]]) -> tuple[dict[str, Any], str]:
    state = initial_state()
    for event in events:
        observed = route(state, event)
        if observed not in POSITIVE:
            return state, observed
        before_identity, before_effects = state["claim_id"], state["external_effects"]
        state = apply_event(state, event)
        if state["claim_id"] != before_identity or state["external_effects"] != before_effects:
            return state, "consumer_invariant_failure"
    return state, "acknowledge_surfaces" if state["stage"] == "acknowledged" else "incomplete_lifecycle"


def reference_events() -> list[dict[str, Any]]:
    rows = [reference_event(kind) for kind in ("propose", "append", "materialize", "acknowledge")]
    rows[-1].update(observed_surface_acks=3, surface_acknowledgment_receipt_present=True)
    return rows


def stage_states() -> list[dict[str, Any]]:
    states = [initial_state()]
    for event in reference_events(): states.append(apply_event(states[-1], event))
    return states


def route_cases() -> list[tuple[str, dict[str, Any], dict[str, Any], str]]:
    states, base = stage_states(), reference_event()
    cases: list[tuple[str, dict[str, Any], dict[str, Any], str]] = []
    def add(case_id: str, state: dict[str, Any], kind: str, patch: dict[str, Any], expected: str) -> None:
        event = reference_event(kind); event.update(patch); cases.append((case_id, state, event, expected))
    add("wrong_stage", states[1], "propose", {}, "reject_wrong_stage")
    add("stale_base", states[0], "propose", {"base_ledger_version": 6}, "reject_stale_base")
    add("event_substitution", states[1], "append", {"event_digest": 9999}, "reject_event_substitution")
    add("ledger_authority_leak", states[0], "propose", {"ledger_self_approves_support": True}, "reject_ledger_authority_leak")
    add("open_contradiction", states[0], "propose", {"open_contradiction": True}, "block_open_contradiction")
    add("evidence_owner_handoff", states[0], "propose", {"evidence_owner_receipt_present": False}, "handoff_to_evidence_owner")
    add("history_missing", states[0], "propose", {"history_refs_present": False}, "request_history_and_non_overwrite")
    add("reason_missing", states[0], "propose", {"revision_reason_present": False}, "request_revision_reason")
    add("residual_missing", states[0], "propose", {"residual_required": True, "residual_refs_present": False}, "request_residual_record")
    add("dependency_open", states[0], "propose", {"dependency_closure_complete": False}, "request_dependency_closure")
    add("migration_missing", states[0], "propose", {"ontology_migration_receipt_present": False}, "request_ontology_migration")
    add("surface_plan_missing", states[0], "propose", {"surface_plan_complete": False}, "request_surface_plan")
    add("surface_ack_missing", states[3], "acknowledge", {}, "request_surface_acknowledgment")
    add("proposal_accepted", states[0], "propose", {}, "accept_proposal")
    add("append_authorized", states[1], "append", {}, "authorize_append")
    add("view_materialized", states[2], "materialize", {}, "materialize_view")
    add("surfaces_acknowledged", states[3], "acknowledge", {"observed_surface_acks": 3, "surface_acknowledgment_receipt_present": True}, "acknowledge_surfaces")
    return cases


def mutations() -> list[tuple[str, list[dict[str, Any]]]]:
    rows: list[tuple[str, list[dict[str, Any]]]] = []
    def event_mutation(name: str, index: int, patch: dict[str, Any]) -> None:
        events = reference_events(); events[index].update(patch); rows.append((name, events))
    for key, value in (("claim_id", 999), ("base_ledger_version", 6), ("prior_head_digest", 999), ("prior_semantic_version", 2), ("next_semantic_version", 3), ("prior_ontology_version", 1), ("prior_support_rank", 0)):
        event_mutation("proposal_" + key, 0, {key: value})
    for key in ("ledger_self_approves_support", "external_effect_requested", "open_contradiction"):
        event_mutation("proposal_" + key, 0, {key: True})
    for key in ("evidence_owner_receipt_present", "history_refs_present", "non_overwrite_attestation_present", "revision_reason_present", "dependency_closure_complete", "ontology_migration_receipt_present", "surface_plan_complete"):
        event_mutation("proposal_missing_" + key, 0, {key: False})
    event_mutation("proposal_missing_residual", 0, {"residual_required": True, "residual_refs_present": False})
    event_mutation("proposal_zero_surfaces", 0, {"required_surface_acks": 0})
    event_mutation("append_substitution", 1, {"event_digest": 9999})
    event_mutation("append_stale_base", 1, {"base_ledger_version": 6})
    event_mutation("materialize_substitution", 2, {"event_digest": 9999})
    event_mutation("materialize_stale_base", 2, {"base_ledger_version": 8})
    event_mutation("ack_substitution", 3, {"event_digest": 9999})
    event_mutation("ack_missing_receipt", 3, {"surface_acknowledgment_receipt_present": False})
    event_mutation("ack_count_short", 3, {"observed_surface_acks": 2})
    for name, indices in (("skip_proposal", (1,2,3)), ("skip_append", (0,2,3)), ("skip_materialize", (0,1,3))):
        base = reference_events(); rows.append((name, [base[i] for i in indices]))
    return rows


def run_suite(name: str, validator: Path, valid: int, invalid: int, issues: list[str]) -> dict[str, Any]:
    completed = subprocess.run(["python3", str(validator)], cwd=ROOT, text=True, capture_output=True)
    if completed.returncode: issues.append(f"{name} failed: {completed.stdout}{completed.stderr}")
    return {"suite_id": name, "valid_count": valid, "expected_invalid_count": invalid, "suite_passed": completed.returncode == 0, "validator_sha256": sha256(validator)}


def build() -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    suites = [
        run_suite("claim_ledger_revision", REVISION_VALIDATOR, 5, 7, issues),
        run_suite("contradiction_revision_lifecycle", HISTORICAL_VALIDATOR, 1, 11, issues),
    ]
    coverage = []
    for case_id, state, event, expected in route_cases():
        observed = route(state, event)
        coverage.append({"case_id": case_id, "expected_route": expected, "observed_route": observed})
        if observed != expected: issues.append(f"{case_id}: expected {expected}, observed {observed}")
    if {row["observed_route"] for row in coverage} != ROUTES: issues.append("route coverage incomplete")

    final, terminal = run(reference_events())
    expected_final = {
        "claim_id": 101, "ledger_version": 8, "head_digest": 8001,
        "semantic_version": 4, "ontology_version": 3, "support_rank": 2,
        "stage": "acknowledged", "pending_event_digest": None,
        "required_surface_acks": 3, "observed_surface_acks": 3,
        "materialized_ledger_version": 8, "append_count": 8, "external_effects": 0,
    }
    if final != expected_final or terminal != "acknowledge_surfaces": issues.append("reference lifecycle did not reach exact acknowledgment")

    receipts = []
    for mutation_id, events in mutations():
        state, failure = run(events)
        rejected = state.get("stage") != "acknowledged" or failure != "acknowledge_surfaces"
        receipts.append({"mutation_id": mutation_id, "rejected": rejected, "terminal_stage": state.get("stage", "unknown"), "failure_route": failure})
        if not rejected: issues.append(mutation_id + ": reached exact acknowledgment")

    result = {
        "schema_version": "asi_stack.claim_ledger_refinement.v1",
        "result_id": "claim-ledger-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha256(LEAN), "revision_fixtures": tree_sha256(REVISION_FIXTURES), "historical_record": sha256(HISTORICAL_RECORD), "historical_schema": sha256(HISTORICAL_SCHEMA)},
        "input_suites": suites,
        "reachable_stage_count": 5,
        "route_case_count": len(coverage),
        "route_coverage": coverage,
        "mutation_count": len(receipts),
        "mutation_rejection_count": sum(row["rejected"] for row in receipts),
        "mutation_receipts": receipts,
        "final_state": {key: value for key, value in final.items() if key != "pending_event_digest"},
        "strongest_effect": "append_materialize_and_acknowledge_evidence_owner_decision",
        "support_state_effect": "none",
        "non_claims": [
            "This finite authored lifecycle does not establish claim truth, evidence validity, reviewer competence, semantic equivalence, assumption completeness, or natural-language claim extraction.",
            "The recorded support rank changes only after an authored evidence-owner receipt; the ledger does not authorize support movement, commit an external effect, approve release, or prove safety or usefulness.",
            "The exact 5/7 revision suite, five-project 1/11 lifecycle, route cases, and mutations do not establish a deployed concurrent event store, causal benefit, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
        ],
    }
    try: jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc: issues.append("schema: " + exc.message)
    if result["mutation_count"] != result["mutation_rejection_count"]: issues.append("not every lifecycle mutation was rejected")
    return result, issues


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result, issues = build()
    if issues: raise SystemExit("Claim Ledger refinement failed:\n - " + "\n - ".join(issues))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("Claim Ledger refinement result stale; run --write")
    print(f"Claim Ledger refinement passed: 5/7 revision fixtures, 1/11 historical lifecycle, {result['route_case_count']} routes, 5 stages, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()
