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
