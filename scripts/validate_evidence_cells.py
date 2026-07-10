#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "evidence_cell.schema.json"
VALID_PATH = ROOT / "tests" / "fixtures" / "protocol_records" / "evidence_cell.valid.json"
MUTATION_DIR = ROOT / "experiments" / "evidence_cell" / "fixtures"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(cell: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_stages = (
        "data",
        "objective",
        "code",
        "updated_state",
        "runtime_output",
        "independent_evaluation",
        "claim_binding",
    )
    chain = cell.get("causal_capability_chain", {})
    for stage in required_stages:
        if stage not in chain:
            errors.append(f"causal_capability_chain must contain stage {stage}")

    demonstrated_effect = cell.get("demonstrated_effect")
    if demonstrated_effect in {"runtime_effect_observed", "direct_support"}:
        incomplete = [stage for stage in required_stages if chain.get(stage, {}).get("status") != "observed"]
        if incomplete:
            errors.append("runtime/direct support requires an observed end-to-end causal chain: " + ", ".join(incomplete))

    for entry in cell.get("missingness", []):
        if entry.get("disposition") not in {"unknown", "not_attempted", "not_required", "waived"}:
            errors.append("missingness disposition must remain honest")
        if not entry.get("reason") or not entry.get("blocker_or_authority_ref"):
            errors.append("missingness requires a reason and blocker or waiver authority")

    for state in cell.get("trainable_state_manifest", []):
        if state.get("updated") and (
            state.get("state_class") != "trainable" or not state.get("update_receipt_ref")
        ):
            errors.append("updated state requires trainable classification and an update receipt")

    receipt = cell.get("response_causality_receipt", {})
    if receipt.get("complete"):
        for field in ("checkpoint_ref", "request_ref", "decode_path_ref", "final_response_ref"):
            if not receipt.get(field):
                errors.append(f"complete response-causality receipt requires {field}")

    separation = cell.get("ownership_capability_separation", {})
    if separation.get("conflated") is not False:
        errors.append("ownership must not be treated as capability evidence")

    for method in cell.get("verification_methods", []):
        if method.get("independence") in {"independent_local", "independent_external"}:
            if method.get("producer_id") == method.get("verifier_id") or not method.get("independence_basis_refs"):
                errors.append("independent verification requires a distinct verifier and basis")

    if cell.get("origin_class") == "local_project_lineage" and cell.get("support_state_effect") not in {
        "argument_only",
        "blocks_promotion",
    }:
        errors.append("local project lineage cannot directly promote a support state")
    if not cell.get("promotion_blockers") or not cell.get("non_claims"):
        errors.append("evidence cell must preserve promotion blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    path = mutation["path"]
    target: Any = value
    for segment in path[:-1]:
        target = target[segment]
    leaf = path[-1]
    operation = mutation["operation"]
    if operation == "delete":
        del target[leaf]
    elif operation == "set":
        target[leaf] = mutation["value"]
    elif operation == "merge":
        target[leaf].update(mutation["value"])
    else:
        raise ValueError(f"unsupported mutation operation {operation!r}")
    return value


def main() -> None:
    schema = load(SCHEMA_PATH)
    valid = load(VALID_PATH)
    errors = validate_value(valid, schema, str(VALID_PATH.relative_to(ROOT)))
    errors.extend(semantic_errors(valid))
    if errors:
        print("Evidence-cell valid fixture failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    mutations = sorted(MUTATION_DIR.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No expected-invalid evidence-cell mutations found.")
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

    print(f"Evidence-cell harness passed: 1 valid fixture and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
