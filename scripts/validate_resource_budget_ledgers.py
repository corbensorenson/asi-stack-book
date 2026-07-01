#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "resource_budget_ledgers" / "fixtures"
SCHEMA = ROOT / "schemas" / "resource_budget_record.schema.json"

BLOCKING_STATES = {"underfunded", "escalated", "deferred", "scope_reduced", "rejected", "residualized"}
HIGH_RISK = {"high", "critical"}
NON_DISPATCH_DECISIONS = {"escalate", "defer", "shrink_scope", "reject", "residual"}
PROTECTED_TERMS = {"approval", "audit", "rollback", "replay", "security", "scif", "human review", "verification"}
SAFETY_TERMS = {"support", "verification", "approval", "audit", "rollback", "security", "safety"}
VERIFICATION_SUFFICIENT_TERMS = {"sufficient", "paid", "covered", "budgeted", "available"}
DISPLACED_COST_TERMS = {
    "future debugging",
    "human repair",
    "reviewer burden",
    "evidence loss",
    "privacy",
    "rollback difficulty",
    "hidden context",
}
REVIEW_CAPACITY_TERMS = {"human review", "reviewer", "review capacity", "manual review", "verifier"}
SCARCE_CAPACITY_TERMS = {"scarce", "exhausted", "saturated", "limited", "protected"}
SERVING_MEMORY_TERMS = {"kv-cache", "kv cache", "serving memory", "pagedattention"}
SERVING_THROUGHPUT_TERMS = {"batch", "batching", "throughput"}
SINGLE_REQUEST_TERMS = {"single-request", "single request"}
VERIFIED_OUTPUT_TERMS = {"verified output", "verified-output", "verifier output"}
SERVING_MEMORY_OVERCLAIM_TERMS = {
    "aggregate throughput proves",
    "throughput proves",
    "kv-cache proves",
    "kv cache proves",
    "serving throughput proves",
    "serving memory proves",
    "proves model quality",
    "proves lower single-request risk",
    "proves lower single request risk",
    "no separate single-request verified output",
    "no separate single request verified output",
}
SECURITY_OVERHEAD_ERASURE_TERMS = {
    "drop scif",
    "drop security",
    "dropped scif",
    "dropped security",
    "remove approval",
    "remove audit",
    "remove isolation",
    "remove logging",
    "remove redaction",
    "remove sanitization",
    "removed approval",
    "removed audit",
    "removed isolation",
    "removed logging",
    "removed redaction",
    "removed sanitization",
    "security overhead removed",
    "skip approval",
    "skip audit",
    "skip isolation",
    "skip logging",
    "skip redaction",
    "skip sanitization",
    "without approval",
    "without audit",
    "without isolation",
    "without logging",
    "without redaction",
    "without sanitization",
    "without scif",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(*values: Any) -> str:
    pieces: list[str] = []
    for value in values:
        if isinstance(value, list):
            pieces.extend(str(item) for item in value)
        elif isinstance(value, dict):
            pieces.extend(f"{key}: {child}" for key, child in value.items())
        else:
            pieces.append(str(value))
    return "\n".join(pieces).lower()


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def has_suspicious_displaced_cost(text: str) -> bool:
    return any(term in text for term in DISPLACED_COST_TERMS)


def schema_errors_for_scenario(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    if "resource_budget_record" not in value:
        return [f"{relative}: missing resource_budget_record."]
    return validate_value(value["resource_budget_record"], schema, f"{relative}:resource_budget_record")


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    top_non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    record = value["resource_budget_record"]
    for field in (
        "cost_estimate",
        "verification_tax",
        "protected_overhead",
        "displaced_costs",
        "safety_gates",
        "residuals",
        "evidence_refs",
    ):
        require_nonempty_list(record, field, errors, f"{relative}:resource_budget_record")
    if errors:
        return errors

    risk = str(record["risk_class"])
    state = str(record["budget_state"])
    decision = str(record["budget_decision"])
    verification_text = text_blob(record["verification_tax"])
    protected_text = text_blob(record["protected_overhead"])
    safety_text = text_blob(record["safety_gates"])
    displaced_text = text_blob(record["displaced_costs"], record["cost_estimate"])
    residual_text = text_blob(record["residuals"])
    non_claim_text = text_blob(top_non_claims)
    capacity_context = value.get("capacity_context")
    capacity_text = text_blob(capacity_context) if isinstance(capacity_context, dict) else ""
    blocked_high_risk_refs = []
    if isinstance(capacity_context, dict) and isinstance(capacity_context.get("blocked_high_risk_refs"), list):
        blocked_high_risk_refs = capacity_context["blocked_high_risk_refs"]

    if decision == "dispatch" and state in BLOCKING_STATES:
        errors.append(f"{relative}: dispatch cannot proceed from blocking budget_state {state}.")

    if risk in HIGH_RISK and state in {"underfunded", "protected_overhead_required"} and decision == "dispatch":
        errors.append(f"{relative}: high-risk underfunded or overhead-required work cannot dispatch.")

    if risk in HIGH_RISK and decision == "dispatch":
        if not contains_any(verification_text, VERIFICATION_SUFFICIENT_TERMS):
            errors.append(f"{relative}: high-risk dispatch must say verification budget is sufficient, paid, or covered.")
        if not contains_any(protected_text, PROTECTED_TERMS):
            errors.append(f"{relative}: high-risk dispatch must name protected overhead such as approval, audit, rollback, SCIF, or human review.")
        if not contains_any(safety_text, SAFETY_TERMS):
            errors.append(f"{relative}: high-risk dispatch must keep safety gates explicit.")

    if decision in NON_DISPATCH_DECISIONS and not residual_text:
        errors.append(f"{relative}: non-dispatch decisions must record residuals.")

    if has_suspicious_displaced_cost(displaced_text):
        if decision == "dispatch" and not re.search(r"\b(measured|accepted evidence|bounded)\b", residual_text):
            errors.append(f"{relative}: dispatch with displaced costs requires measured, bounded, or accepted-evidence residual handling.")
        if "none" in residual_text:
            errors.append(f"{relative}: displaced costs cannot have no residuals.")

    review_text = text_blob(
        record["cost_estimate"],
        record["verification_tax"],
        record["protected_overhead"],
        record["safety_gates"],
    )
    security_budget_text = text_blob(
        record["value_hypothesis"],
        record["cost_estimate"],
        record["protected_overhead"],
        record["quality_predicate"],
        record["safety_gates"],
        record["escalation_rule"],
        record["residuals"],
    )
    if decision == "dispatch" and contains_any(security_budget_text, SECURITY_OVERHEAD_ERASURE_TERMS):
        errors.append(f"{relative}: dispatch cannot claim savings by removing security, SCIF, approval, audit, logging, redaction, or sanitization overhead.")

    record_text = text_blob(record, capacity_context)
    if contains_any(record_text, SERVING_MEMORY_TERMS):
        serving_cost_text = text_blob(record["capacity_pool"], record["cost_estimate"])
        serving_boundary_text = text_blob(
            record["quality_predicate"],
            record["safety_gates"],
            record["residuals"],
            top_non_claims,
        )
        if not contains_any(serving_cost_text, SERVING_MEMORY_TERMS):
            errors.append(f"{relative}: serving-memory records must keep KV-cache or serving-memory cost visible.")
        if not contains_any(serving_cost_text, SERVING_THROUGHPUT_TERMS):
            errors.append(f"{relative}: serving-memory records must separate batching or throughput from ordinary task cost.")
        if not contains_any(serving_boundary_text, SINGLE_REQUEST_TERMS):
            errors.append(f"{relative}: serving-memory records must name the single-request boundary.")
        if not contains_any(serving_boundary_text, VERIFIED_OUTPUT_TERMS):
            errors.append(f"{relative}: serving-memory records must keep verified output separate from aggregate throughput.")
        if contains_any(record_text, SERVING_MEMORY_OVERCLAIM_TERMS):
            errors.append(
                f"{relative}: aggregate serving throughput, KV-cache reuse, or serving-memory savings cannot prove model quality or lower single-request risk."
            )
        if not contains_any(non_claim_text, {"serving", "throughput", "kv-cache"}):
            errors.append(f"{relative}: serving-memory non_claims must deny serving, throughput, or KV-cache behavior claims.")

    if contains_any(capacity_text, SCARCE_CAPACITY_TERMS) and blocked_high_risk_refs:
        if risk in {"low", "medium"} and decision == "dispatch" and contains_any(review_text, REVIEW_CAPACITY_TERMS):
            errors.append(
                f"{relative}: low- or medium-risk dispatch cannot consume scarce review capacity while high-risk work is blocked."
            )
        if risk in {"low", "medium"} and decision in {"defer", "shrink_scope"}:
            if not contains_any(residual_text, {"reserved", "protected", "high-risk", "review capacity"}):
                errors.append(
                    f"{relative}: scarce review-capacity deferral must record the protected high-risk capacity residual."
                )

    if "does not promote" not in non_claim_text or "support" not in non_claim_text:
        errors.append(f"{relative}: non_claims must state support-state non-promotion.")
    if "does not prove" not in non_claim_text:
        errors.append(f"{relative}: non_claims must deny stronger proof.")
    if not contains_any(non_claim_text, {"scheduler", "runtime", "economic", "load", "kv-cache"}):
        errors.append(f"{relative}: non_claims must deny scheduler, runtime, economic, load, or KV-cache claims.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No resource-budget ledger fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = str(fixture.relative_to(ROOT))
        expect_valid = fixture_expectation(fixture)
        if expect_valid is None:
            errors.append(f"{relative}: fixture name must start with valid_ or invalid_.")
            continue
        try:
            value = load_json(fixture)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: top-level fixture must be an object.")
            continue

        fixture_errors = schema_errors_for_scenario(value, schema, relative)
        if not fixture_errors:
            fixture_errors.extend(semantic_errors(value, relative))

        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Resource budget ledger harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Resource budget ledger harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
