#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "generation_mode_baselines" / "fixtures"
SCHEMAS = {
    "generation_mode_record": ROOT / "schemas" / "generation_mode_record.schema.json",
    "resource_budget_record": ROOT / "schemas" / "resource_budget_record.schema.json",
}
NON_AUTOREGRESSIVE_MODES = {
    "speculative",
    "multi_token_prediction",
    "multi_head_internal",
    "feature_draft",
    "lookahead_retrieval",
    "diffusion",
    "multi_seed_diffusion",
    "hybrid",
    "early_exit",
    "state_space",
    "kv_cache_serving",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemas() -> dict[str, Any]:
    return {name: load_json(path) for name, path in SCHEMAS.items()}


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


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


def has_prefixed_ref(values: list[Any], prefix: str) -> bool:
    return any(str(value).lower().startswith(prefix) for value in values)


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("generation_mode_record", "resource_budget_record"):
        if field not in value:
            errors.append(f"{relative}: missing {field}.")
            continue
        errors.extend(validate_value(value[field], schemas[field], f"{relative}:{field}"))
    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    generation = value["generation_mode_record"]
    budget = value["resource_budget_record"]
    if generation["task_id"] != budget["task_id"]:
        errors.append(f"{relative}: generation_mode_record.task_id must match resource_budget_record.task_id.")
    if generation["risk_tier"] != budget["risk_class"]:
        errors.append(f"{relative}: generation risk_tier must match resource budget risk_class.")

    evidence_refs = require_nonempty_list(generation, "evidence_refs", errors, f"{relative}:generation_mode_record")
    metric_definitions = require_nonempty_list(
        generation,
        "metric_definitions",
        errors,
        f"{relative}:generation_mode_record",
    )
    require_nonempty_list(budget, "verification_tax", errors, f"{relative}:resource_budget_record")
    require_nonempty_list(budget, "protected_overhead", errors, f"{relative}:resource_budget_record")
    require_nonempty_list(budget, "safety_gates", errors, f"{relative}:resource_budget_record")
    require_nonempty_list(budget, "residuals", errors, f"{relative}:resource_budget_record")
    require_nonempty_list(generation, "non_claims", errors, f"{relative}:generation_mode_record")

    metric_text = text_blob(metric_definitions)
    result_text = text_blob(generation["quality_or_pass_result"], generation["accepted_output_accounting"])
    fallback_text = text_blob(generation["repair_or_fallback"])
    non_claim_text = text_blob(generation["non_claims"], value["non_claims"])

    if generation["measurement_status"] == "run":
        for prefix in ("run:", "baseline:", "negative_control:"):
            if not has_prefixed_ref(evidence_refs, prefix):
                errors.append(f"{relative}: run measurement requires an evidence ref with prefix {prefix}.")
    if generation["measurement_status"] != "run" and generation["promotion_decision"] != "not_evaluated":
        errors.append(f"{relative}: non-run measurement cannot make an evaluated promotion decision.")

    for term in ("useful_solution_per_second", "quality", "residual"):
        if term not in metric_text:
            errors.append(f"{relative}: metric_definitions must include {term}.")

    if "failed" in result_text and generation["promotion_decision"] not in {"reject", "fallback_only", "quarantine"}:
        errors.append(f"{relative}: failed quality/pass result must reject, quarantine, or use fallback_only.")
    if "not measured" in result_text or "latency only" in result_text:
        errors.append(f"{relative}: latency-only or unmeasured quality cannot pass the baseline harness.")
    if generation["promotion_decision"] == "promote":
        errors.append(f"{relative}: generation-mode baseline fixtures cannot promote support or release state.")
    if generation["generation_mode"] in NON_AUTOREGRESSIVE_MODES and generation["risk_tier"] in {"medium", "high", "critical"}:
        if "fallback" not in fallback_text or "none" in fallback_text:
            errors.append(f"{relative}: medium-or-higher non-autoregressive candidates must name fallback behavior.")
    if budget["budget_decision"] == "dispatch" and generation["promotion_decision"] in {"reject", "quarantine"}:
        errors.append(f"{relative}: rejected or quarantined generation modes cannot have dispatch budget_decision.")
    if "does not" not in non_claim_text or "support" not in non_claim_text:
        errors.append(f"{relative}: non_claims must state support-state non-promotion.")
    if "model" not in non_claim_text and "runtime" not in non_claim_text:
        errors.append(f"{relative}: non_claims must deny model or runtime behavior claims.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schemas = load_schemas()
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No generation-mode baseline fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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

        fixture_errors = schema_errors_for_scenario(value, schemas, relative)
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
        print("Generation mode baseline harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Generation mode baseline harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
