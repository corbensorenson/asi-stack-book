#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "capacity_smoothing" / "fixtures"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"
ALLOWED_MODES = {"regenerative_priority", "priority_defer", "scope_reduce"}
RISK_WORDS = {"high-risk", "safety", "critical"}
REVIEW_ACCOUNTING_FIELDS = {
    "starting_review_capacity",
    "review_refill",
    "review_minutes_admitted",
    "ending_review_capacity",
    "protected_review_minutes",
    "admitted_low_risk_review_minutes",
    "blocked_protected_review_minutes",
    "displaced_review_cost_residualized",
    "residual_refs",
}
REQUIRED_LEAN_THEOREMS = (
    "capacity_smoothing_reviewer_trace_fixture_valid",
    "capacity_smoothing_reviewer_trace_preserves_review_capacity",
    "capacity_smoothing_reviewer_trace_preserves_protected_review_overhead",
    "capacity_smoothing_reviewer_trace_residualizes_displaced_review_costs",
    "capacity_smoothing_reviewer_trace_has_no_support_promotion",
    "blocked_protected_review_rejects_low_risk_review_dispatch",
    "high_risk_review_without_protected_overhead_rejected",
    "blocked_protected_review_requires_displaced_cost_residual",
)


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


def require_number(record: dict[str, Any], field: str, errors: list[str], relative: str) -> float:
    value = record.get(field)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append(f"{relative}: {field} must be a number.")
        return 0.0
    return float(value)


def require_bool(record: dict[str, Any], field: str, errors: list[str], relative: str) -> bool:
    value = record.get(field)
    if not isinstance(value, bool):
        errors.append(f"{relative}: {field} must be a boolean.")
        return False
    return value


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def trace_uses_review_accounting(trace: list[Any]) -> bool:
    return any(
        isinstance(step, dict) and any(field in step for field in REVIEW_ACCOUNTING_FIELDS)
        for step in trace
    )


def lean_bridge_errors() -> list[str]:
    if not LEAN_FIXTURE.exists():
        return [f"{LEAN_FIXTURE.relative_to(ROOT)} is missing."]
    lean_text = LEAN_FIXTURE.read_text(encoding="utf-8", errors="ignore")
    return [
        f"{LEAN_FIXTURE.relative_to(ROOT)} is missing theorem {name}."
        for name in REQUIRED_LEAN_THEOREMS
        if name not in lean_text
    ]


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")

    mode = value.get("capacity_mode")
    if mode not in ALLOWED_MODES:
        errors.append(f"{relative}: capacity_mode must be one of {sorted(ALLOWED_MODES)}.")

    capacity_limit = require_number(value, "capacity_limit", errors, relative)
    if capacity_limit <= 0:
        errors.append(f"{relative}: capacity_limit must be positive.")

    trace = require_nonempty_list(value, "trace", errors, relative)
    non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors
    review_accounting = trace_uses_review_accounting(trace)
    review_limit = 0.0
    if review_accounting:
        review_limit = require_number(value, "review_capacity_limit", errors, relative)
        if review_limit <= 0:
            errors.append(f"{relative}: review_capacity_limit must be positive when review accounting is present.")

    previous_ending: float | None = None
    previous_review_ending: float | None = None
    overload_steps = 0
    for index, step in enumerate(trace):
        step_path = f"{relative}:trace[{index}]"
        if not isinstance(step, dict):
            errors.append(f"{step_path}: step must be an object.")
            continue
        starting = require_number(step, "starting_capacity", errors, step_path)
        refill = require_number(step, "refill", errors, step_path)
        admitted = require_number(step, "admitted_cost", errors, step_path)
        ending = require_number(step, "ending_capacity", errors, step_path)
        deferred = require_number(step, "deferred_cost", errors, step_path)
        blocked_high_risk = require_number(step, "blocked_high_risk_cost", errors, step_path)
        admitted_low_risk = require_number(step, "admitted_low_risk_cost", errors, step_path)
        require_nonempty_list(step, "decision_refs", errors, step_path)
        if errors:
            continue

        if previous_ending is not None and abs(starting - previous_ending) > 1e-9:
            errors.append(f"{step_path}: starting_capacity must equal prior ending_capacity.")

        available = min(capacity_limit, starting + refill)
        expected_ending = available - admitted
        if abs(ending - expected_ending) > 1e-9:
            errors.append(f"{step_path}: ending_capacity must equal min(limit, starting + refill) - admitted_cost.")
        if ending < -1e-9:
            overload_steps += 1
            errors.append(f"{step_path}: admitted cost exceeds available capacity.")
        if deferred < 0:
            errors.append(f"{step_path}: deferred_cost cannot be negative.")
        if blocked_high_risk > 0 and admitted_low_risk > 0:
            errors.append(f"{step_path}: low-risk work cannot consume capacity while high-risk work is blocked.")

        if review_accounting:
            starting_review = require_number(step, "starting_review_capacity", errors, step_path)
            review_refill = require_number(step, "review_refill", errors, step_path)
            review_admitted = require_number(step, "review_minutes_admitted", errors, step_path)
            ending_review = require_number(step, "ending_review_capacity", errors, step_path)
            protected_review = require_number(step, "protected_review_minutes", errors, step_path)
            low_risk_review = require_number(step, "admitted_low_risk_review_minutes", errors, step_path)
            blocked_protected_review = require_number(step, "blocked_protected_review_minutes", errors, step_path)
            displaced_residualized = require_bool(step, "displaced_review_cost_residualized", errors, step_path)
            residual_refs = require_nonempty_list(step, "residual_refs", errors, step_path)
            if errors:
                continue
            if previous_review_ending is not None and abs(starting_review - previous_review_ending) > 1e-9:
                errors.append(f"{step_path}: starting_review_capacity must equal prior ending_review_capacity.")
            available_review = min(review_limit, starting_review + review_refill)
            expected_review_ending = available_review - review_admitted
            if abs(ending_review - expected_review_ending) > 1e-9:
                errors.append(
                    f"{step_path}: ending_review_capacity must equal min(review limit, starting_review_capacity + review_refill) - review_minutes_admitted."
                )
            if ending_review < -1e-9:
                errors.append(f"{step_path}: review_minutes_admitted exceeds available reviewer capacity.")
            if protected_review > review_admitted:
                errors.append(f"{step_path}: protected_review_minutes cannot exceed review_minutes_admitted.")
            if blocked_protected_review > 0 and low_risk_review > 0:
                errors.append(f"{step_path}: low-risk review cannot consume reviewer capacity while protected review is blocked.")
            step_text = text_blob(step)
            if any(term in step_text for term in RISK_WORDS) and admitted > 0 and protected_review <= 0:
                errors.append(f"{step_path}: high-risk admitted work must pay protected review overhead.")
            if (deferred > 0 or blocked_high_risk > 0 or blocked_protected_review > 0) and not residual_refs:
                errors.append(f"{step_path}: deferred or blocked work must have residual_refs.")
            if blocked_protected_review > 0 and not displaced_residualized:
                errors.append(f"{step_path}: blocked protected review must residualize displaced review cost.")
            previous_review_ending = ending_review
        previous_ending = ending

    conclusion_text = text_blob(value.get("conclusion", ""), non_claims)
    if "support" not in conclusion_text or "does not promote" not in conclusion_text:
        errors.append(f"{relative}: non_claims must state support-state non-promotion.")
    if "does not prove" not in conclusion_text:
        errors.append(f"{relative}: non_claims must deny stronger proof.")
    if not any(term in conclusion_text for term in ("load", "scheduler", "tokenmana", "economic", "runtime")):
        errors.append(f"{relative}: non_claims must deny load, scheduler, TokenMana, economic, or runtime claims.")
    if "proves load stability" in conclusion_text or "proves tokenmana" in conclusion_text:
        errors.append(f"{relative}: fixture must not claim it proves load stability or TokenMana behavior.")
    if review_accounting:
        for term in ("review", "protected", "displaced"):
            if term not in conclusion_text:
                errors.append(f"{relative}: review-accounting non_claims must mention {term}.")

    scenario_text = text_blob(value)
    if any(term in scenario_text for term in RISK_WORDS) and "decision_refs" not in scenario_text:
        errors.append(f"{relative}: risk-bearing traces must include decision refs.")
    if overload_steps and value.get("conclusion") == "pass":
        errors.append(f"{relative}: overloaded traces cannot conclude pass.")

    return errors


def main() -> None:
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No capacity-smoothing fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

    errors: list[str] = lean_bridge_errors()
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

        fixture_errors = semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Capacity smoothing toy harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Capacity smoothing toy harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
