#!/usr/bin/env python3
"""Validate the reachable Proof-Carrying Claims refinement and exact legacy inputs."""

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
RESULT = ROOT / "experiments/proof_carrying_claims_refinement/results/2026-07-15-local.json"
SCHEMA = ROOT / "schemas/proof_carrying_claims_refinement.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean"
PROOF_SCHEMA = ROOT / "schemas/proof_carrying_claim.schema.json"
DOSSIER_RESULT = ROOT / "experiments/adversarial_review_dossier/results/2026-07-02-local.json"
PROOF_FIXTURES = ROOT / "experiments/proof_carrying_claims/fixtures"

ACCEPTED = {
    "accept_target_freeze", "accept_artifact_binding", "accept_verifier_execution",
    "accept_adjudication", "accept_write_back",
}
NEGATIVE = {"failed", "timeout", "mismatch"}
NEXT_STAGE = {
    "idle": "frozen", "frozen": "artifact_bound", "artifact_bound": "executed",
    "executed": "adjudicated", "adjudicated": "written_back", "written_back": "written_back",
}
EXPECTED_KIND = {
    "idle": "freeze_target", "frozen": "bind_artifact", "artifact_bound": "execute_verifier",
    "executed": "adjudicate", "adjudicated": "write_back", "written_back": "write_back",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_packet(event_digest: int = 1, **updates: Any) -> dict[str, Any]:
    packet = {
        "claim_id": 41, "claim_version": 7, "target_digest": 101,
        "interpretation_digest": 102, "scope_digest": 103, "assumptions_digest": 104,
        "artifact_digest": 201, "verifier_id": 301, "verifier_version": 3,
        "trusted_base_digest": 401, "event_digest": event_digest,
        "artifact_present": True, "interpretation_mapping_present": True,
        "scope_present": True, "assumptions_present": True, "trusted_base_present": True,
        "verifier_executed": True, "verifier_artifact_refs_present": True,
        "attempt_history_present": True, "artifact_verified": True,
        "semantic_mapping_reviewed": True, "high_risk": True,
        "independent_review_present": True, "dossier_present": True,
        "dissent_present": True, "dissent_preserved": True,
        "limitations_present": True, "residual_present": True,
        "owner_handoff_present": True, "support_assignment_requested": False,
        "external_effect_requested": False, "verifier_result": "passed",
        "claim_effect": "scoped_proposal",
    }
    packet.update(updates)
    return packet


def initial_state() -> dict[str, Any]:
    return {
        "stage": "idle", "claim_id": 41, "claim_version": 7, "target_digest": 101,
        "interpretation_digest": 102, "scope_digest": 103, "assumptions_digest": 104,
        "artifact_digest": 201, "verifier_id": 301, "verifier_version": 3,
        "trusted_base_digest": 401, "last_event_digest": 0, "verifier_result": "not_run",
        "claim_effect": "no_change", "receipt_count": 0,
        "support_assignment_count": 0, "external_effect_count": 0,
    }


def event(kind: str, digest: int, **updates: Any) -> dict[str, Any]:
    return {"kind": kind, "packet": canonical_packet(digest, **updates)}


def exact_target(state: dict[str, Any], packet: dict[str, Any]) -> bool:
    return all(packet[key] == state[key] for key in (
        "claim_id", "claim_version", "target_digest", "interpretation_digest",
        "scope_digest", "assumptions_digest",
    ))


def exact_artifact(state: dict[str, Any], packet: dict[str, Any]) -> bool:
    return all(packet[key] == state[key] for key in (
        "artifact_digest", "verifier_id", "verifier_version", "trusted_base_digest",
    ))


def route_for(state: dict[str, Any], evt: dict[str, Any]) -> str:
    packet = evt["packet"]
    if evt["kind"] != EXPECTED_KIND[state["stage"]]:
        return "reject_wrong_stage"
    if not exact_target(state, packet):
        return "reject_target_substitution"
    if state["stage"] != "idle" and not exact_artifact(state, packet):
        return "reject_event_substitution"
    if packet["event_digest"] == state["last_event_digest"]:
        return "reject_event_substitution"
    if packet["support_assignment_requested"] or packet["external_effect_requested"]:
        return "reject_authority_leak"
    stage = state["stage"]
    if stage == "idle":
        if not packet["interpretation_mapping_present"]:
            return "request_interpretation_mapping"
        if not packet["scope_present"] or not packet["assumptions_present"]:
            return "request_scope_and_assumptions"
        return "accept_target_freeze"
    if stage == "frozen":
        if not packet["artifact_present"]:
            return "request_artifact"
        if not packet["trusted_base_present"]:
            return "request_trusted_base"
        return "accept_artifact_binding"
    if stage == "artifact_bound":
        if not packet["verifier_executed"] or packet["verifier_result"] == "not_run":
            return "request_verifier_execution"
        if packet["verifier_result"] == "passed" and not packet["verifier_artifact_refs_present"]:
            return "request_verifier_artifact_refs"
        if packet["verifier_result"] in NEGATIVE and not packet["attempt_history_present"]:
            return "request_attempt_history"
        return "accept_verifier_execution"
    if stage == "executed":
        if packet["verifier_result"] != state["verifier_result"]:
            return "reject_event_substitution"
        if packet["verifier_result"] == "passed" and (
            not packet["artifact_verified"] or not packet["semantic_mapping_reviewed"]
        ):
            return "block_unverified_pass"
        if packet["verifier_result"] in NEGATIVE and packet["claim_effect"] == "scoped_proposal":
            return "block_negative_promotion"
        if packet["verifier_result"] == "mismatch" and packet["claim_effect"] != "tribunal":
            return "route_mismatch_to_tribunal"
        if packet["high_risk"] and (
            not packet["independent_review_present"] or not packet["dossier_present"]
        ):
            return "request_independent_dossier"
        if packet["dissent_present"] and not packet["dissent_preserved"]:
            return "request_dissent_preservation"
        if not packet["limitations_present"] or not packet["residual_present"]:
            return "request_limits_and_residual"
        return "accept_adjudication"
    if stage == "adjudicated":
        if packet["verifier_result"] != state["verifier_result"] or packet["claim_effect"] != state["claim_effect"]:
            return "reject_event_substitution"
        if not packet["owner_handoff_present"]:
            return "request_owner_handoff"
        return "accept_write_back"
    return "reject_wrong_stage"


def apply_event(state: dict[str, Any], evt: dict[str, Any]) -> tuple[dict[str, Any], str]:
    route = route_for(state, evt)
    if route not in ACCEPTED:
        return copy.deepcopy(state), route
    updated = copy.deepcopy(state)
    previous_stage = state["stage"]
    updated["stage"] = NEXT_STAGE[previous_stage]
    updated["last_event_digest"] = evt["packet"]["event_digest"]
    updated["receipt_count"] += 1
    if previous_stage == "artifact_bound":
        updated["verifier_result"] = evt["packet"]["verifier_result"]
    if previous_stage == "executed":
        updated["claim_effect"] = evt["packet"]["claim_effect"]
    return updated, route


def canonical_events() -> list[dict[str, Any]]:
    return [
        event("freeze_target", 1), event("bind_artifact", 2),
        event("execute_verifier", 3), event("adjudicate", 4), event("write_back", 5),
    ]


def run(events: list[dict[str, Any]]) -> tuple[dict[str, Any], str]:
    state = initial_state()
    route = ""
    for evt in events:
        state, route = apply_event(state, evt)
        if route not in ACCEPTED:
            return state, route
    return state, route


def prefix_states() -> list[dict[str, Any]]:
    states = [initial_state()]
    current = states[0]
    for evt in canonical_events():
        current, route = apply_event(current, evt)
        if route not in ACCEPTED:
            raise AssertionError(route)
        states.append(current)
    return states


def route_cases() -> list[tuple[str, dict[str, Any], dict[str, Any], str]]:
    states = prefix_states()
    idle, frozen, bound, executed, adjudicated, written = states
    failed_bound = copy.deepcopy(bound)
    failed_execute = event("execute_verifier", 30, verifier_result="failed")
    failed_executed, _ = apply_event(failed_bound, failed_execute)
    mismatch_execute = event("execute_verifier", 31, verifier_result="mismatch")
    mismatch_executed, _ = apply_event(bound, mismatch_execute)
    return [
        ("wrong_stage", idle, event("bind_artifact", 10), "reject_wrong_stage"),
        ("target_substitution", idle, event("freeze_target", 10, claim_id=99), "reject_target_substitution"),
        ("event_substitution", frozen, event("bind_artifact", 1), "reject_event_substitution"),
        ("authority_leak", idle, event("freeze_target", 10, support_assignment_requested=True), "reject_authority_leak"),
        ("interpretation_missing", idle, event("freeze_target", 10, interpretation_mapping_present=False), "request_interpretation_mapping"),
        ("scope_missing", idle, event("freeze_target", 10, scope_present=False), "request_scope_and_assumptions"),
        ("artifact_missing", frozen, event("bind_artifact", 10, artifact_present=False), "request_artifact"),
        ("trusted_base_missing", frozen, event("bind_artifact", 10, trusted_base_present=False), "request_trusted_base"),
        ("verifier_not_executed", bound, event("execute_verifier", 10, verifier_executed=False), "request_verifier_execution"),
        ("pass_refs_missing", bound, event("execute_verifier", 10, verifier_artifact_refs_present=False), "request_verifier_artifact_refs"),
        ("attempt_history_missing", bound, event("execute_verifier", 10, verifier_result="failed", attempt_history_present=False), "request_attempt_history"),
        ("unverified_pass", executed, event("adjudicate", 10, artifact_verified=False), "block_unverified_pass"),
        ("negative_promotion", failed_executed, event("adjudicate", 32, verifier_result="failed"), "block_negative_promotion"),
        ("mismatch_no_tribunal", mismatch_executed, event("adjudicate", 33, verifier_result="mismatch", claim_effect="block"), "route_mismatch_to_tribunal"),
        ("independent_dossier_missing", executed, event("adjudicate", 10, dossier_present=False), "request_independent_dossier"),
        ("dissent_erased", executed, event("adjudicate", 10, dissent_preserved=False), "request_dissent_preservation"),
        ("limits_missing", executed, event("adjudicate", 10, limitations_present=False), "request_limits_and_residual"),
        ("owner_handoff_missing", adjudicated, event("write_back", 10, owner_handoff_present=False), "request_owner_handoff"),
        ("target_frozen", idle, canonical_events()[0], "accept_target_freeze"),
        ("artifact_bound", frozen, canonical_events()[1], "accept_artifact_binding"),
        ("verifier_executed", bound, canonical_events()[2], "accept_verifier_execution"),
        ("adjudicated", executed, canonical_events()[3], "accept_adjudication"),
        ("written_back", adjudicated, canonical_events()[4], "accept_write_back"),
    ]


def mutated_sequence(index: int, **updates: Any) -> list[dict[str, Any]]:
    events = canonical_events()
    events[index] = copy.deepcopy(events[index])
    events[index]["packet"].update(updates)
    return events


def mutation_sequences() -> list[tuple[str, list[dict[str, Any]]]]:
    rows: list[tuple[str, list[dict[str, Any]]]] = []
    for field in ("claim_id", "claim_version", "target_digest", "interpretation_digest", "scope_digest", "assumptions_digest"):
        rows.append((f"freeze_{field}", mutated_sequence(0, **{field: 999})))
    rows.extend([
        ("freeze_interpretation_missing", mutated_sequence(0, interpretation_mapping_present=False)),
        ("freeze_scope_missing", mutated_sequence(0, scope_present=False)),
        ("freeze_assumptions_missing", mutated_sequence(0, assumptions_present=False)),
        ("freeze_support_authority_leak", mutated_sequence(0, support_assignment_requested=True)),
        ("freeze_external_effect_leak", mutated_sequence(0, external_effect_requested=True)),
        ("bind_artifact_missing", mutated_sequence(1, artifact_present=False)),
        ("bind_trusted_base_missing", mutated_sequence(1, trusted_base_present=False)),
        ("bind_artifact_substitution", mutated_sequence(1, artifact_digest=999)),
        ("bind_verifier_substitution", mutated_sequence(1, verifier_id=999)),
        ("bind_verifier_version_substitution", mutated_sequence(1, verifier_version=999)),
        ("bind_trusted_base_substitution", mutated_sequence(1, trusted_base_digest=999)),
        ("execute_not_run", mutated_sequence(2, verifier_executed=False)),
        ("execute_result_not_run", mutated_sequence(2, verifier_result="not_run")),
        ("execute_pass_refs_missing", mutated_sequence(2, verifier_artifact_refs_present=False)),
        ("execute_event_replay", mutated_sequence(2, event_digest=2)),
        ("adjudicate_result_substitution", mutated_sequence(3, verifier_result="failed")),
        ("adjudicate_artifact_unverified", mutated_sequence(3, artifact_verified=False)),
        ("adjudicate_mapping_unreviewed", mutated_sequence(3, semantic_mapping_reviewed=False)),
        ("adjudicate_independent_review_missing", mutated_sequence(3, independent_review_present=False)),
        ("adjudicate_dossier_missing", mutated_sequence(3, dossier_present=False)),
        ("adjudicate_dissent_erased", mutated_sequence(3, dissent_preserved=False)),
        ("adjudicate_limits_missing", mutated_sequence(3, limitations_present=False)),
        ("adjudicate_residual_missing", mutated_sequence(3, residual_present=False)),
        ("writeback_result_substitution", mutated_sequence(4, verifier_result="failed")),
        ("writeback_effect_substitution", mutated_sequence(4, claim_effect="block")),
        ("writeback_owner_missing", mutated_sequence(4, owner_handoff_present=False)),
        ("writeback_support_authority_leak", mutated_sequence(4, support_assignment_requested=True)),
        ("writeback_external_effect_leak", mutated_sequence(4, external_effect_requested=True)),
    ])
    failed = canonical_events()
    failed[2] = event("execute_verifier", 3, verifier_result="failed")
    failed[3] = event("adjudicate", 4, verifier_result="failed", claim_effect="scoped_proposal")
    rows.append(("negative_result_scoped_proposal", failed))
    mismatch = canonical_events()
    mismatch[2] = event("execute_verifier", 3, verifier_result="mismatch")
    mismatch[3] = event("adjudicate", 4, verifier_result="mismatch", claim_effect="block")
    rows.append(("mismatch_without_tribunal", mismatch))
    return rows


def run_validator(script: str) -> None:
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT, capture_output=True, text=True)
    if completed.returncode:
        raise AssertionError(f"{script} failed: {completed.stdout}{completed.stderr}")


def build_result() -> dict[str, Any]:
    run_validator("validate_proof_carrying_claims.py")
    run_validator("validate_adversarial_review_dossier_probe.py")
    proof_valid = len(list(PROOF_FIXTURES.glob("valid_*.json")))
    proof_invalid = len(list(PROOF_FIXTURES.glob("invalid_*.json")))
    dossier = json.loads(DOSSIER_RESULT.read_text(encoding="utf-8"))
    coverage = []
    for case_id, state, evt, expected in route_cases():
        observed = route_for(state, evt)
        if observed != expected:
            raise AssertionError(f"{case_id}: expected {expected}, got {observed}")
        coverage.append({"case_id": case_id, "expected_route": expected, "observed_route": observed})
    mutation_receipts = []
    for mutation_id, events in mutation_sequences():
        state, failure = run(events)
        rejected = state["stage"] != "written_back" and failure not in ACCEPTED
        if not rejected:
            raise AssertionError(f"mutation accepted: {mutation_id}")
        mutation_receipts.append({
            "mutation_id": mutation_id, "rejected": True,
            "terminal_stage": state["stage"], "failure_route": failure,
        })
    final_state, final_route = run(canonical_events())
    if final_route != "accept_write_back" or final_state["stage"] != "written_back":
        raise AssertionError("canonical lifecycle did not reach writeback")
    return {
        "schema_version": "asi_stack.proof_carrying_claims_refinement.v1",
        "result_id": "proof-carrying-claims-refinement-2026-07-15-local",
        "source_sha256": {
            "lean_model": sha256(LEAN), "proof_claim_schema": sha256(PROOF_SCHEMA),
            "adversarial_dossier_result": sha256(DOSSIER_RESULT),
        },
        "input_suites": [
            {"suite_id": "proof_carrying_claims", "valid_count": proof_valid,
             "expected_invalid_count": proof_invalid, "suite_passed": True,
             "validator_sha256": sha256(ROOT / "scripts/validate_proof_carrying_claims.py")},
            {"suite_id": "adversarial_review_dossier", "valid_count": dossier["valid_dossier_count"],
             "expected_invalid_count": dossier["expected_invalid_control_count"], "suite_passed": True,
             "validator_sha256": sha256(ROOT / "scripts/validate_adversarial_review_dossier_probe.py")},
        ],
        "reachable_stage_count": 6, "route_case_count": len(coverage), "route_coverage": coverage,
        "mutation_count": len(mutation_receipts), "mutation_rejection_count": len(mutation_receipts),
        "mutation_receipts": mutation_receipts,
        "final_state": {key: final_state[key] for key in (
            "stage", "receipt_count", "verifier_result", "claim_effect",
            "support_assignment_count", "external_effect_count",
        )},
        "support_state_effect": "none",
        "non_claims": [
            "No natural-language target identification or semantic-equivalence result is established.",
            "No proof, citation, procedure, replay, benchmark, or verifier is shown sound beyond its authored record.",
            "No trusted-base correctness, reviewer competence, independence, or verdict-quality result is established.",
            "No claim truth, evidence adequacy, support assignment, action authority, or release authority is established.",
            "No natural workload, model-backed review, debate, tribunal, or contestability outcome is measured.",
            "No usefulness, causal advantage, safety, or total-cost advantage is established.",
            "No concurrent persistence, deployment, reproduction, or transfer is established.",
            "No chapter-core support state changes; the support-state effect is none.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build_result()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(result)
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or json.loads(RESULT.read_text(encoding="utf-8")) != result:
        raise SystemExit(f"{RESULT.relative_to(ROOT)} is missing or stale; rerun with --write")
    print(
        "Proof-Carrying Claims refinement passed: 3/5 proof fixtures, 2/7 dossier cases, "
        f"23 routes, 6 stages, {result['mutation_rejection_count']} mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
