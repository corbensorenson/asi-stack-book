#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "capacity_smoothing" / "fixtures"
ALLOWED_MODES = {"regenerative_priority", "priority_defer", "scope_reduce"}
RISK_WORDS = {"high-risk", "safety", "critical"}


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

    previous_ending: float | None = None
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
