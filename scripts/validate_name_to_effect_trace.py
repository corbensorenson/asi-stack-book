#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "name_to_effect_trace_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "name_to_effect_trace_record.valid.json"
MUTATIONS = ROOT / "experiments" / "name_to_effect_trace" / "fixtures"
STAGES = ["request_derived_input", "policy", "canonical_state_selection", "effect", "receipt", "evaluator", "claim_boundary"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    request = record.get("request", {})
    policy = record.get("policy_decision", {})
    state = record.get("state_selection", {})
    effect = record.get("effect", {})
    receipt = record.get("receipt", {})
    evaluator = record.get("evaluator", {})
    mapping = record.get("name_to_effect_map", [])
    stages = [row.get("stage") for row in mapping]
    if stages != STAGES:
        errors.append("name-to-effect map must contain the seven ordered stages exactly once")
    if policy.get("request_id") != request.get("request_id"):
        errors.append("policy decision must bind the request id")
    if receipt.get("request_id") != request.get("request_id") or receipt.get("request_digest") != request.get("request_digest"):
        errors.append("request-to-effect receipt must bind the request id and digest")
    if receipt.get("decision_id") != policy.get("decision_id"):
        errors.append("request-to-effect receipt must bind the policy decision")
    if receipt.get("canonical_state_digest") != state.get("canonical_state_digest"):
        errors.append("request-to-effect receipt must bind the canonical state digest")
    if receipt.get("effect_id") != effect.get("effect_id") or receipt.get("effect_digest") != effect.get("observed_digest"):
        errors.append("request-to-effect receipt must bind the observed effect id and digest")
    if effect.get("terminal_state") in {"completed", "failed", "denied"} and receipt.get("acknowledged_terminal_state") is not True:
        errors.append("terminal effect requires an acknowledged request-to-effect receipt")
    if evaluator.get("effect_id") != effect.get("effect_id") or evaluator.get("receipt_id") != receipt.get("receipt_id"):
        errors.append("evaluator must bind the observed effect and request-to-effect receipt")
    if evaluator.get("independence") in {"separate_route", "independent_external"} and evaluator.get("producer_id") == evaluator.get("verifier_id"):
        errors.append("separate or external evaluator cannot share the producer identity")
    if len(mapping) >= 7:
        expected_outputs = [request.get("derived_input_ref"), policy.get("decision_id"), state.get("canonical_state_ref"), effect.get("effect_id"), receipt.get("receipt_id"), evaluator.get("evaluation_id"), record.get("claim_boundary", {}).get("claim_ref")]
        if [row.get("output_ref") for row in mapping] != expected_outputs:
            errors.append("name-to-effect map outputs must bind the record's actual request, policy, state, effect, receipt, evaluator, and claim refs")
        if mapping[2].get("authority") != "canonical":
            errors.append("canonical state selection cannot delegate authority to a projection")
    claim = record.get("claim_boundary", {})
    if claim.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("fixture-only name-to-effect trace cannot promote or enter bounded evidence review")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("name-to-effect trace must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    leaf = mutation["path"][-1]
    if mutation["operation"] == "set":
        target[leaf] = mutation["value"]
    elif mutation["operation"] == "delete":
        del target[leaf]
    else:
        raise ValueError(f"unsupported mutation operation {mutation['operation']!r}")
    return value


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid name-to-effect trace failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No expected-invalid name-to-effect mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce expected error {mutation['expected_error']!r}: {found}")
    print(f"Name-to-effect trace harness passed: 1 blocked five-project lineage trace and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
