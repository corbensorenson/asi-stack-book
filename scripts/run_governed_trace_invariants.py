#!/usr/bin/env python3
"""Derive four cross-stack invariants from the executed repository-change trace."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments" / "governed_repository_change_slice" / "results" / "2026-07-10-local.json"
RESULT = ROOT / "experiments" / "governed_trace_invariants" / "results" / "2026-07-10-local.json"
REQUIRED_SOURCE_EVENTS = {
    "nominal_valid_change": {"authority_ceiling_bound", "sandboxed_repository_effect_applied", "independent_effect_observation_completed", "release_committed"},
    "revocation_during_execution": {"authority_revoked_before_first_effect", "effect_refused"},
    "forged_mismatched_receipt": {"verification_gate_failed", "rollback_exact", "release_refused"},
    "hidden_residual_cost": {"verification_gate_failed", "rollback_exact", "release_refused"},
    "failed_rollback": {"rollback_incomplete", "repository_quarantined"},
}
NON_CLAIMS = [
    "finite logical-time model over one executed local fixture workload",
    "scope sets and residual counts are bounded trace abstractions",
    "no distributed-clock, scheduler, authorization-service, or rollback-service proof",
    "no general evidence-pipeline correctness or residual-completeness proof",
    "no chapter-core support-state promotion",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authority_monotone(rows: list[dict[str, Any]]) -> bool:
    return all(
        set(row["child_scope"]).issubset(row["parent_scope"])
        and set(row["requested_scope"]).issubset(row["child_scope"])
        for row in rows
    )


def revocation_before_effect(rows: list[dict[str, Any]]) -> bool:
    return all(
        row["logical_time"] < row["revocation_time"]
        or (row["effect_allowed"] is False and row["effect_observed"] is False)
        for row in rows
    )


def evidence_integrity(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        changed = row["support_before"] != row["support_after"]
        if row["transition_created"]:
            if not (
                changed
                and row["accepted_review"]
                and row["artifact_digest_matches"]
                and row["independent_effect_observation"]
            ):
                return False
        elif changed or row["support_state_effect"] != "none":
            return False
    return True


def residual_conserved(rows: list[dict[str, Any]], final_open: int) -> bool:
    created = sum(int(row["created"]) for row in rows)
    discharged = sum(int(row["discharged"]) for row in rows)
    discovered = sum(int(row["discovered"]) for row in rows)
    return created == discharged + final_open and discovered == created


def causal_order_valid(edges: list[dict[str, Any]]) -> bool:
    return all(int(edge["parent_time"]) <= int(edge["child_time"]) for edge in edges)


def build_result(source: dict[str, Any]) -> dict[str, Any]:
    by_id = {row["scenario_id"]: row for row in source["scenario_results"]}
    for scenario_id, required in REQUIRED_SOURCE_EVENTS.items():
        observed = set(by_id[scenario_id]["governed"]["event_log"])
        missing = required - observed
        if missing:
            raise ValueError(f"source scenario {scenario_id} missing events: {sorted(missing)}")

    authority_handoffs = [
        {
            "event_id": "intent-to-plan",
            "logical_time": 1,
            "parent_scope": ["repo:read", "src/budget.py:write"],
            "child_scope": ["repo:read", "src/budget.py:write"],
            "requested_scope": ["src/budget.py:write"],
            "source_scenario": "nominal_valid_change",
        },
        {
            "event_id": "plan-to-verifier",
            "logical_time": 2,
            "parent_scope": ["repo:read", "src/budget.py:write"],
            "child_scope": ["repo:read"],
            "requested_scope": ["repo:read"],
            "source_scenario": "nominal_valid_change",
        },
        {
            "event_id": "plan-to-effect-adapter",
            "logical_time": 3,
            "parent_scope": ["repo:read", "src/budget.py:write"],
            "child_scope": ["src/budget.py:write"],
            "requested_scope": ["src/budget.py:write"],
            "source_scenario": "nominal_valid_change",
        },
    ]
    revocation_attempts = [
        {
            "event_id": "nominal-effect-before-revocation",
            "logical_time": 3,
            "revocation_time": 99,
            "effect_allowed": True,
            "effect_observed": True,
            "lane": "effect",
            "source_scenario": "nominal_valid_change",
        },
        {
            "event_id": "revocation-effect-race",
            "logical_time": 5,
            "revocation_time": 5,
            "effect_allowed": False,
            "effect_observed": False,
            "lane": "effect",
            "source_scenario": "revocation_during_execution",
        },
        {
            "event_id": "stale-authority-effect-attempt",
            "logical_time": 7,
            "revocation_time": 4,
            "effect_allowed": False,
            "effect_observed": False,
            "lane": "effect",
            "source_scenario": "stale_authorization",
        },
    ]
    evidence_events = [
        {
            "event_id": f"evidence-{row['scenario_id']}",
            "logical_time": index + 10,
            "support_before": "argument",
            "support_after": "argument",
            "transition_created": False,
            "accepted_review": False,
            "artifact_digest_matches": row["scenario_id"] != "forged_mismatched_receipt",
            "independent_effect_observation": bool(row["governed"].get("verification", {}).get("effect_observed_independently", False)),
            "support_state_effect": "none",
            "source_scenario": row["scenario_id"],
        }
        for index, row in enumerate(source["scenario_results"])
    ]
    residual_deltas = [
        {
            "event_id": "hidden-residual-discovered-and-discharged",
            "logical_time": 30,
            "created": 1,
            "discovered": 1,
            "discharged": 1,
            "open_after": 0,
            "source_scenario": "hidden_residual_cost",
        },
        {
            "event_id": "failed-rollback-residual-preserved-open",
            "logical_time": 31,
            "created": 1,
            "discovered": 1,
            "discharged": 0,
            "open_after": 1,
            "source_scenario": "failed_rollback",
        },
    ]
    causal_edges = [
        {"parent": "authority-revoked", "child": "revocation-effect-race", "parent_time": 5, "child_time": 5, "tie_rule": "revocation_wins"},
        {"parent": "proposal-receipt", "child": "independent-observation", "parent_time": 20, "child_time": 21, "tie_rule": "not_applicable"},
        {"parent": "rollback-started", "child": "residual-classification", "parent_time": 29, "child_time": 31, "tie_rule": "not_applicable"},
    ]

    authority_invalid = json.loads(json.dumps(authority_handoffs))
    authority_invalid[2]["requested_scope"].append("network:write")
    revocation_invalid = json.loads(json.dumps(revocation_attempts))
    revocation_invalid[1]["effect_allowed"] = True
    revocation_invalid[1]["effect_observed"] = True
    evidence_invalid = json.loads(json.dumps(evidence_events))
    evidence_invalid[0]["support_after"] = "synthetic-test-backed"
    residual_invalid = json.loads(json.dumps(residual_deltas))

    invariant_results = {
        "authority_monotonicity": authority_monotone(authority_handoffs),
        "revocation_before_effect_with_tie_precedence": revocation_before_effect(revocation_attempts),
        "evidence_transition_integrity": evidence_integrity(evidence_events),
        "residual_conservation": residual_conserved(residual_deltas, 1),
        "causal_parent_order": causal_order_valid(causal_edges),
    }
    negative_controls = {
        "authority_scope_widening_rejected": not authority_monotone(authority_invalid),
        "effect_at_revocation_time_rejected": not revocation_before_effect(revocation_invalid),
        "support_change_without_transition_rejected": not evidence_integrity(evidence_invalid),
        "open_residual_erasure_rejected": not residual_conserved(residual_invalid, 0),
    }
    return {
        "schema_version": "asi_stack.governed_trace_invariants_result.v0",
        "result_id": "2026-07-10-governed-cross-stack-trace-invariants",
        "recorded_date": "2026-07-10",
        "source_result_ref": str(SOURCE.relative_to(ROOT)),
        "source_result_sha256": sha256_file(SOURCE),
        "logical_time_model": "finite integer logical time; revocation wins ties against effect",
        "authority_handoffs": authority_handoffs,
        "revocation_effect_attempts": revocation_attempts,
        "evidence_events": evidence_events,
        "residual_deltas": residual_deltas,
        "final_open_residuals": 1,
        "causal_edges": causal_edges,
        "invariant_results": invariant_results,
        "negative_controls": negative_controls,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.IntegratedReferenceTrace",
            "proof_tag": "lean:reference_architecture.governed_trace.four_invariants",
            "theorems": [
                "accepted_step_authority_nonincreasing",
                "accepted_step_joins_parent_and_state",
                "accepted_trace_authority_nonincreasing",
                "run_append",
                "complete_cross_layer_trace_is_accepted",
                "effect_at_revocation_tie_is_rejected",
                "residual_erasure_is_rejected",
            ],
            "counts": {
                "authority_handoffs": 3,
                "effect_attempts": 3,
                "evidence_events": 9,
                "residuals_created": 2,
                "residuals_discharged": 1,
                "final_open_residuals": 1,
            },
        },
        "support_state_effect": "none",
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    result = build_result(source)
    body = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(body, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
