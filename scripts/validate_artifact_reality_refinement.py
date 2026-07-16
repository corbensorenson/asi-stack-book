#!/usr/bin/env python3
"""Validate the reachable artifact record-reality lifecycle and exact bounded suites."""

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
RESULT = ROOT / "experiments/artifact_reality_refinement/results/2026-07-15-local.json"
SCHEMA = ROOT / "schemas/artifact_reality_refinement.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/ArtifactRealityRefinement.lean"
SUITES = [
    ("artifact_graph_replay", "validate_artifact_graph_replay.py", None, 2, 6),
    ("record_reality_sequence", "validate_artifact_graph_record_reality_sequence.py", "experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json", 1, 4),
    ("receipt_faithfulness", "validate_receipt_faithfulness.py", "experiments/receipt_faithfulness/results/2026-07-03-local.json", 3, 6),
    ("receipt_repository_audit", "validate_receipt_repository_audit.py", "experiments/receipt_repository_audit/results/2026-07-03-local.json", 4, 5),
    ("receipt_repository_challenge", "validate_receipt_repository_challenge.py", "experiments/receipt_repository_audit/results/2026-07-04-challenge.json", 4, 5),
    ("artifact_live_attestation", "validate_artifact_live_attestation_probe.py", "experiments/artifact_live_attestation/results/2026-07-04-local.json", 1, 7),
    ("artifact_randomized_attestation", "validate_artifact_randomized_attestation_audit.py", "experiments/artifact_randomized_attestation/results/2026-07-04-local.json", 4, 8),
    ("epistemic_tcb", "validate_epistemic_trusted_computing_base.py", "experiments/epistemic_tcb/results/2026-07-03-local.json", 3, 6),
]
ACCEPTED = {"accept_registration", "accept_provenance_binding", "accept_replay_validation", "accept_reality_cross_check", "accept_trust_binding", "accept_admission"}
EXPECTED_KIND = {
    "idle": "register_artifact", "registered": "bind_provenance",
    "provenance_bound": "validate_replay", "replay_validated": "cross_check_reality",
    "reality_cross_checked": "bind_trust_base", "trust_bound": "admit_artifact",
    "admitted": "admit_artifact",
}
NEXT_STAGE = {
    "idle": "registered", "registered": "provenance_bound",
    "provenance_bound": "replay_validated", "replay_validated": "reality_cross_checked",
    "reality_cross_checked": "trust_bound", "trust_bound": "admitted", "admitted": "admitted",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet(event_digest: int = 1, **updates: Any) -> dict[str, Any]:
    value = {
        "artifact_id": 801, "artifact_version": 5, "content_digest": 901,
        "parent_job_digest": 902, "source_digest": 903, "context_digest": 904,
        "transaction_digest": 905, "certificate_digest": 906, "tool_digest": 907,
        "claim_digest": 908, "test_digest": 909, "policy_digest": 910,
        "consumer_digest": 911, "event_digest": event_digest,
        "artifact_present": True, "produced_artifact": True, "parent_job_present": True,
        "source_refs_present": True, "context_refs_present": True,
        "transaction_refs_present": True, "certificate_refs_present": True,
        "tool_refs_present": True, "claim_links_present": True, "test_links_present": True,
        "audit_trail_present": True, "replay_metadata_present": True,
        "replay_grade_sufficient": True, "replay_limits_present": True,
        "certificate_active": True, "replay_validated": True,
        "observed_artifact_present": True, "independent_cross_check_matched": True,
        "trap_challenge_passed": True, "attestation_limits_present": True,
        "trusted_core_present": True, "root_of_trust_present": True,
        "independent_verifier_present": True, "recursion_stop_present": True,
        "outside_tcb_residual_present": True, "revocation_closure_complete": True,
        "consumer_acknowledgment_present": True, "support_assignment_requested": False,
        "external_effect_requested": False,
    }
    value.update(updates)
    return value


def event(kind: str, digest: int, **updates: Any) -> dict[str, Any]:
    return {"kind": kind, "packet": packet(digest, **updates)}


def initial_state() -> dict[str, Any]:
    return {
        "stage": "idle", "artifact_id": 801, "artifact_version": 5,
        "content_digest": 901, "parent_job_digest": 902, "source_digest": 903,
        "context_digest": 904, "transaction_digest": 905, "certificate_digest": 906,
        "tool_digest": 907, "claim_digest": 908, "test_digest": 909,
        "policy_digest": 910, "consumer_digest": 911, "last_event_digest": 0,
        "receipt_count": 0, "reality_observation_count": 0,
        "support_assignment_count": 0, "external_effect_count": 0,
    }


def exact_artifact(state: dict[str, Any], p: dict[str, Any]) -> bool:
    return all(p[k] == state[k] for k in ("artifact_id", "artifact_version", "content_digest", "policy_digest", "consumer_digest"))


def exact_lineage(state: dict[str, Any], p: dict[str, Any]) -> bool:
    return all(p[k] == state[k] for k in ("parent_job_digest", "source_digest", "context_digest", "transaction_digest", "certificate_digest", "tool_digest", "claim_digest", "test_digest"))


def route_for(state: dict[str, Any], evt: dict[str, Any]) -> str:
    p = evt["packet"]
    if evt["kind"] != EXPECTED_KIND[state["stage"]]: return "reject_wrong_stage"
    if not exact_artifact(state, p): return "reject_artifact_substitution"
    if not exact_lineage(state, p): return "reject_lineage_substitution"
    if p["event_digest"] == state["last_event_digest"]: return "reject_event_replay"
    if p["support_assignment_requested"] or p["external_effect_requested"]: return "reject_authority_leak"
    stage = state["stage"]
    if stage == "idle":
        if not p["artifact_present"] or not p["produced_artifact"]: return "request_artifact_record"
        if not p["parent_job_present"]: return "request_parent_job"
        return "accept_registration"
    if stage == "registered":
        if not p["source_refs_present"] or not p["context_refs_present"]: return "request_source_and_context"
        if not p["transaction_refs_present"] or not p["certificate_refs_present"]: return "request_transaction_and_certificate"
        if not p["tool_refs_present"] or not p["claim_links_present"] or not p["test_links_present"]: return "request_tool_claim_and_test_links"
        if not p["audit_trail_present"]: return "request_audit_trail"
        return "accept_provenance_binding"
    if stage == "provenance_bound":
        if not p["replay_metadata_present"]: return "request_replay_metadata"
        if not p["replay_grade_sufficient"]: return "request_replay_grade"
        if not p["replay_limits_present"]: return "request_replay_limits"
        if not p["certificate_active"]: return "request_active_certificate"
        if not p["replay_validated"]: return "request_replay_validation"
        return "accept_replay_validation"
    if stage == "replay_validated":
        if not p["observed_artifact_present"]: return "request_observed_artifact"
        if not p["independent_cross_check_matched"]: return "request_independent_cross_check"
        if not p["trap_challenge_passed"]: return "request_trap_challenge"
        if not p["attestation_limits_present"]: return "request_attestation_limits"
        return "accept_reality_cross_check"
    if stage == "reality_cross_checked":
        if not p["trusted_core_present"]: return "request_trusted_core"
        if not p["root_of_trust_present"]: return "request_root_of_trust"
        if not p["independent_verifier_present"]: return "request_independent_verifier"
        if not p["recursion_stop_present"]: return "request_recursion_stop"
        if not p["outside_tcb_residual_present"]: return "request_outside_tcb_residual"
        return "accept_trust_binding"
    if stage == "trust_bound":
        if not p["revocation_closure_complete"]: return "request_revocation_closure"
        if not p["consumer_acknowledgment_present"]: return "request_consumer_acknowledgment"
        return "accept_admission"
    return "reject_wrong_stage"


def apply_event(state: dict[str, Any], evt: dict[str, Any]) -> tuple[dict[str, Any], str]:
    route = route_for(state, evt)
    if route not in ACCEPTED: return copy.deepcopy(state), route
    updated = copy.deepcopy(state); previous = state["stage"]
    updated["stage"] = NEXT_STAGE[previous]
    updated["last_event_digest"] = evt["packet"]["event_digest"]
    updated["receipt_count"] += 1
    if previous == "replay_validated": updated["reality_observation_count"] += 1
    return updated, route


def canonical_events() -> list[dict[str, Any]]:
    return [event("register_artifact", 1), event("bind_provenance", 2), event("validate_replay", 3), event("cross_check_reality", 4), event("bind_trust_base", 5), event("admit_artifact", 6)]


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
    idle, registered, provenance, replay, reality, trust, final = states()
    return [
        ("wrong_stage", idle, event("bind_provenance", 20), "reject_wrong_stage"),
        ("artifact_substitution", idle, event("register_artifact", 20, artifact_id=999), "reject_artifact_substitution"),
        ("lineage_substitution", idle, event("register_artifact", 20, source_digest=999), "reject_lineage_substitution"),
        ("event_replay", registered, event("bind_provenance", 1), "reject_event_replay"),
        ("authority_leak", idle, event("register_artifact", 20, support_assignment_requested=True), "reject_authority_leak"),
        ("artifact_missing", idle, event("register_artifact", 20, artifact_present=False), "request_artifact_record"),
        ("parent_missing", idle, event("register_artifact", 20, parent_job_present=False), "request_parent_job"),
        ("source_missing", registered, event("bind_provenance", 20, source_refs_present=False), "request_source_and_context"),
        ("transaction_missing", registered, event("bind_provenance", 20, transaction_refs_present=False), "request_transaction_and_certificate"),
        ("tool_missing", registered, event("bind_provenance", 20, tool_refs_present=False), "request_tool_claim_and_test_links"),
        ("audit_missing", registered, event("bind_provenance", 20, audit_trail_present=False), "request_audit_trail"),
        ("metadata_missing", provenance, event("validate_replay", 20, replay_metadata_present=False), "request_replay_metadata"),
        ("grade_insufficient", provenance, event("validate_replay", 20, replay_grade_sufficient=False), "request_replay_grade"),
        ("limits_missing", provenance, event("validate_replay", 20, replay_limits_present=False), "request_replay_limits"),
        ("certificate_stale", provenance, event("validate_replay", 20, certificate_active=False), "request_active_certificate"),
        ("replay_unvalidated", provenance, event("validate_replay", 20, replay_validated=False), "request_replay_validation"),
        ("observation_missing", replay, event("cross_check_reality", 20, observed_artifact_present=False), "request_observed_artifact"),
        ("cross_check_missing", replay, event("cross_check_reality", 20, independent_cross_check_matched=False), "request_independent_cross_check"),
        ("trap_failed", replay, event("cross_check_reality", 20, trap_challenge_passed=False), "request_trap_challenge"),
        ("attestation_unbounded", replay, event("cross_check_reality", 20, attestation_limits_present=False), "request_attestation_limits"),
        ("core_missing", reality, event("bind_trust_base", 20, trusted_core_present=False), "request_trusted_core"),
        ("root_missing", reality, event("bind_trust_base", 20, root_of_trust_present=False), "request_root_of_trust"),
        ("verifier_not_independent", reality, event("bind_trust_base", 20, independent_verifier_present=False), "request_independent_verifier"),
        ("recursion_stop_missing", reality, event("bind_trust_base", 20, recursion_stop_present=False), "request_recursion_stop"),
        ("outside_residual_missing", reality, event("bind_trust_base", 20, outside_tcb_residual_present=False), "request_outside_tcb_residual"),
        ("revocation_incomplete", trust, event("admit_artifact", 20, revocation_closure_complete=False), "request_revocation_closure"),
        ("consumer_unacknowledged", trust, event("admit_artifact", 20, consumer_acknowledgment_present=False), "request_consumer_acknowledgment"),
        ("registration_accepted", idle, canonical_events()[0], "accept_registration"),
        ("provenance_accepted", registered, canonical_events()[1], "accept_provenance_binding"),
        ("replay_accepted", provenance, canonical_events()[2], "accept_replay_validation"),
        ("reality_accepted", replay, canonical_events()[3], "accept_reality_cross_check"),
        ("trust_accepted", reality, canonical_events()[4], "accept_trust_binding"),
        ("admission_accepted", trust, canonical_events()[5], "accept_admission"),
    ]


def mutated(index: int, **updates: Any) -> list[dict[str, Any]]:
    rows = canonical_events(); rows[index] = copy.deepcopy(rows[index]); rows[index]["packet"].update(updates); return rows


def mutations() -> list[tuple[str, list[dict[str, Any]]]]:
    rows: list[tuple[str, list[dict[str, Any]]]] = []
    for field in ("artifact_id", "artifact_version", "content_digest", "parent_job_digest", "source_digest", "context_digest", "transaction_digest", "certificate_digest", "tool_digest", "claim_digest", "test_digest", "policy_digest", "consumer_digest"):
        rows.append((f"register_{field}", mutated(0, **{field: 999})))
    rows.extend([
        ("register_artifact_missing", mutated(0, artifact_present=False)), ("register_not_produced", mutated(0, produced_artifact=False)),
        ("register_parent_missing", mutated(0, parent_job_present=False)), ("register_support_leak", mutated(0, support_assignment_requested=True)),
        ("register_external_effect", mutated(0, external_effect_requested=True)), ("bind_source_missing", mutated(1, source_refs_present=False)),
        ("bind_context_missing", mutated(1, context_refs_present=False)), ("bind_transaction_missing", mutated(1, transaction_refs_present=False)),
        ("bind_certificate_missing", mutated(1, certificate_refs_present=False)), ("bind_tool_missing", mutated(1, tool_refs_present=False)),
        ("bind_claim_missing", mutated(1, claim_links_present=False)), ("bind_test_missing", mutated(1, test_links_present=False)),
        ("bind_audit_missing", mutated(1, audit_trail_present=False)), ("bind_event_replay", mutated(1, event_digest=1)),
        ("replay_metadata_missing", mutated(2, replay_metadata_present=False)), ("replay_grade_insufficient", mutated(2, replay_grade_sufficient=False)),
        ("replay_limits_missing", mutated(2, replay_limits_present=False)), ("replay_certificate_stale", mutated(2, certificate_active=False)),
        ("replay_unvalidated", mutated(2, replay_validated=False)), ("replay_content_substitution", mutated(2, content_digest=999)),
        ("replay_support_leak", mutated(2, support_assignment_requested=True)), ("replay_external_effect", mutated(2, external_effect_requested=True)),
        ("reality_observation_missing", mutated(3, observed_artifact_present=False)), ("reality_cross_check_missing", mutated(3, independent_cross_check_matched=False)),
        ("reality_trap_failed", mutated(3, trap_challenge_passed=False)), ("reality_limits_missing", mutated(3, attestation_limits_present=False)),
        ("reality_event_replay", mutated(3, event_digest=3)), ("reality_support_leak", mutated(3, support_assignment_requested=True)),
        ("reality_external_effect", mutated(3, external_effect_requested=True)), ("trust_core_missing", mutated(4, trusted_core_present=False)),
        ("trust_root_missing", mutated(4, root_of_trust_present=False)), ("trust_self_verifier", mutated(4, independent_verifier_present=False)),
        ("trust_recursion_stop_missing", mutated(4, recursion_stop_present=False)), ("trust_outside_residual_missing", mutated(4, outside_tcb_residual_present=False)),
        ("trust_lineage_substitution", mutated(4, certificate_digest=999)), ("admit_revocation_incomplete", mutated(5, revocation_closure_complete=False)),
        ("admit_consumer_missing", mutated(5, consumer_acknowledgment_present=False)), ("admit_event_replay", mutated(5, event_digest=5)),
        ("admit_support_leak", mutated(5, support_assignment_requested=True)), ("admit_external_effect", mutated(5, external_effect_requested=True)),
    ])
    return rows


def run_validator(name: str) -> None:
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / name)], cwd=ROOT, capture_output=True, text=True)
    if completed.returncode: raise AssertionError(f"{name} failed: {completed.stdout}{completed.stderr}")


def build_result() -> dict[str, Any]:
    suite_rows = []
    for suite_id, script, result_path, valid_count, invalid_count in SUITES:
        run_validator(script)
        if result_path:
            value = json.loads((ROOT / result_path).read_text())
            if value.get("support_state_effect") != "none": raise AssertionError(f"{suite_id}: support effect drifted")
        suite_rows.append({"suite_id": suite_id, "valid_count": valid_count, "expected_invalid_count": invalid_count, "suite_passed": True, "validator_sha256": sha256(ROOT / "scripts" / script)})
    coverage = []
    for case_id, state, evt, expected in route_cases():
        observed = route_for(state, evt)
        if observed != expected: raise AssertionError(f"{case_id}: expected {expected}, got {observed}")
        coverage.append({"case_id": case_id, "expected_route": expected, "observed_route": observed})
    receipts = []
    for mutation_id, events in mutations():
        state, failure = run(events)
        if state["stage"] == "admitted" or failure in ACCEPTED: raise AssertionError(f"mutation accepted: {mutation_id}")
        receipts.append({"mutation_id": mutation_id, "rejected": True, "terminal_stage": state["stage"], "failure_route": failure})
    final, final_route = run(canonical_events())
    if final_route != "accept_admission" or final["stage"] != "admitted": raise AssertionError("canonical lifecycle failed")
    return {
        "schema_version": "asi_stack.artifact_reality_refinement.v1", "result_id": "artifact-reality-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha256(LEAN)}, "input_suites": suite_rows,
        "reachable_stage_count": 7, "route_case_count": len(coverage), "route_coverage": coverage,
        "mutation_count": len(receipts), "mutation_rejection_count": len(receipts), "mutation_receipts": receipts,
        "final_state": {k: final[k] for k in ("stage", "receipt_count", "reality_observation_count", "support_assignment_count", "external_effect_count")},
        "support_state_effect": "none",
        "non_claims": [
            "No open-world provenance completeness, causal provenance, artifact truth, content correctness, or source truth is established.",
            "No replay determinism, semantic equivalence, replay-engine correctness, receipt faithfulness in general, or verifier correctness is established.",
            "No external independence, root-of-trust security, compromise absence, repository completeness, or revocation propagation is established.",
            "No support, evidence, readiness, release, or external-effect authority is assigned by the artifact lifecycle.",
            "No natural workload, usefulness, causal advantage, safety, deployment, reproduction, transfer, SOTA, AGI, or ASI is established.",
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
    print(f"Artifact-reality refinement passed: eight exact suites, 33 routes, 7 stages, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()
