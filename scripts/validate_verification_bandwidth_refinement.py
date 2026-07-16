#!/usr/bin/env python3
"""Independently consume the Verification Bandwidth lifecycle and legacy suites."""
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

    result = {
        "schema_version": "asi_stack.verification_bandwidth_refinement.v1",
        "result_id": "verification-bandwidth-refinement-2026-07-15-local",
        "source_sha256": {
            "lean_model": sha256(LEAN),
            "context_adequacy_schema": sha256(ADEQUACY_SCHEMA),
            "probe_result": sha256(PROBE_RESULT),
            "capacity_result": sha256(CAPACITY_RESULT),
        },
        "input_suites": suites,
        "reachable_stage_count": 5,
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
        f"5 stages, {result['mutation_rejection_count']} mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
