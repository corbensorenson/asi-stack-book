#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "metric_provenance_record.schema.json"
VALID_PATH = ROOT / "tests" / "fixtures" / "protocol_records" / "metric_provenance_record.valid.json"
MUTATION_DIR = ROOT / "experiments" / "metric_provenance" / "fixtures"

INADMISSIBLE_ORIGINS = {"source_reported", "modeled", "fixture", "constant", "declared", "proxy", "vacuous", "unknown"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    metric = record.get("metric", {})
    origin = metric.get("origin_class")
    admissibility = metric.get("admissibility")
    if admissibility == "admissible" and origin in INADMISSIBLE_ORIGINS:
        errors.append("source-reported, modeled, fixture, constant, declared, proxy, vacuous, or unknown metrics cannot be admissible")
    if origin in {"measured", "recomputed"}:
        if not metric.get("observation_ref"):
            errors.append("measured or recomputed metric requires observation_ref")
        if not metric.get("input_refs") or not metric.get("evaluator_ref"):
            errors.append("measured or recomputed metric requires inputs and evaluator identity")
    if origin == "derived" and (not metric.get("formula_ref") or not metric.get("input_refs")):
        errors.append("derived metric requires formula_ref and input_refs")

    if admissibility == "admissible" and metric.get("contamination_state") != "clean_checked":
        errors.append("contaminated, suspected, or unknown metric cannot be admissible")
    capacity = metric.get("target_capacity", {})
    if capacity.get("status") in {"not_expressible", "unknown"} and admissibility == "admissible":
        errors.append("not-expressible or unknown target capacity must block metric admissibility")

    closure = record.get("closure_inheritance", {})
    if "inherited_regression_refs" not in closure or not closure.get("inherited_regression_refs"):
        errors.append("closure inheritance must preserve inherited_regression_refs")
    if "inherited_exclusion_refs" not in closure or not closure.get("inherited_exclusion_refs"):
        errors.append("closure inheritance must preserve inherited_exclusion_refs")

    retry = record.get("retry_lineage", {})
    attempt = retry.get("attempt_index")
    ceiling = retry.get("retry_ceiling")
    if not isinstance(attempt, int) or not isinstance(ceiling, int) or attempt < 1 or ceiling < 0:
        errors.append("retry lineage requires positive integer attempt and nonnegative integer ceiling")
    elif attempt > ceiling and not retry.get("override_ref"):
        errors.append("retry ceiling exceeded without an override reference")

    binding = record.get("checkpoint_output_binding", {})
    if binding.get("complete"):
        for field in ("checkpoint_ref", "tokenizer_ref", "runtime_path_ref", "raw_output_ref", "evaluator_output_ref", "claim_ref"):
            if not binding.get(field):
                errors.append(f"complete checkpoint-output binding requires {field}")
    if admissibility == "admissible" and not binding.get("complete"):
        errors.append("admissible metric requires complete checkpoint-output binding")
    if record.get("support_state_effect") == "eligible_for_bounded_evidence_review" and admissibility != "admissible":
        errors.append("eligible support effect requires an admissible metric")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("metric provenance record must preserve promotion blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    path = mutation["path"]
    for segment in path[:-1]:
        target = target[segment]
    leaf = path[-1]
    if mutation["operation"] == "set":
        target[leaf] = mutation["value"]
    elif mutation["operation"] == "merge":
        target[leaf].update(mutation["value"])
    elif mutation["operation"] == "delete":
        del target[leaf]
    else:
        raise ValueError(f"unsupported mutation operation {mutation['operation']!r}")
    return value


def main() -> None:
    schema = load(SCHEMA_PATH)
    valid = load(VALID_PATH)
    errors = validate_value(valid, schema, str(VALID_PATH.relative_to(ROOT)))
    errors.extend(semantic_errors(valid))
    if errors:
        print("Metric-provenance valid fixture failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    mutations = sorted(MUTATION_DIR.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No expected-invalid metric-provenance mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        candidate_errors = validate_value(candidate, schema, str(path.relative_to(ROOT)))
        candidate_errors.extend(semantic_errors(candidate))
        expected = mutation["expected_error"]
        if not any(expected in error for error in candidate_errors):
            print(f"{path.relative_to(ROOT)} did not produce expected error: {expected}")
            for error in candidate_errors:
                print(f" - {error}")
            raise SystemExit(1)

    print(f"Metric-provenance harness passed: 1 valid blocked record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
