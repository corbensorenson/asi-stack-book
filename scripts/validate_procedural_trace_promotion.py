#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
from typing import Any
from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/procedural_trace_promotion_record.schema.json"
VALID = ROOT / "tests/fixtures/protocol_records/procedural_trace_promotion_record.valid.json"
MUTATIONS = ROOT / "experiments/procedural_trace_promotion/fixtures"
SOURCES = {"cca_project", "moecot_manifest_project", "beastbrain_project", "corbens_trainer_project"}
LIFECYCLE = ["candidate", "verified", "routable", "quarantined", "retired"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != SOURCES:
        errors.append("promotion record must name the four historical-project sources exactly")
    domains = record.get("memory_domains", {})
    facts = set(domains.get("semantic_fact_refs", []))
    procedural = set(domains.get("procedural_trace_refs", []))
    if domains.get("domains_conflated") or facts & procedural:
        errors.append("semantic facts and procedural traces must remain separate")
    traces = record.get("candidate_traces", [])
    ids = {item.get("trace_id") for item in traces}
    if ids != procedural:
        errors.append("procedural trace inventory must exactly match candidate traces")
    if {item.get("source_id") for item in traces} != SOURCES:
        errors.append("candidate traces must cover every historical source")
    shapes = {item.get("procedure_shape_digest") for item in traces}
    if len(shapes) != 1:
        errors.append("candidate traces must share one procedure shape")
    if any(not item.get("source_receipt_ref") for item in traces):
        errors.append("every trace requires a source receipt")
    if any(not item.get("effect_receipt_ref") for item in traces):
        errors.append("every trace requires an effect receipt")
    successes = {item.get("trace_id") for item in traces if item.get("outcome") == "success"}
    failures = {item.get("trace_id") for item in traces if item.get("outcome") in {"failure", "near_miss"}}
    gate = record.get("promotion_gate", {})
    if not failures:
        errors.append("promotion must retain at least one failed attempt or near miss")
    if set(gate.get("negative_example_trace_ids", [])) != failures:
        errors.append("promotion gate must preserve every failed attempt as a negative example")
    if gate.get("observed_successes") != len(successes) or len(successes) < gate.get("minimum_successes", 0):
        errors.append("promotion success count must be exact and meet the declared minimum")
    if not gate.get("regression_suite_ref") or gate.get("regression_passed") is not True or gate.get("failed_tests"):
        errors.append("routable promotion requires passing regression evidence")
    rollback = record.get("rollback", {})
    if gate.get("rollback_plan_ref") != "rollback://bounded-procedure/v1" or not rollback.get("prepromotion_snapshot_ref") or not rollback.get("restore_route_ref") or rollback.get("rehearsal_observed") is not True:
        errors.append("promotion requires a bound and rehearsed rollback route")
    retirement = record.get("retirement", {})
    if retirement.get("lifecycle_path") != LIFECYCLE or not retirement.get("criteria") or not retirement.get("retirement_receipt_ref"):
        errors.append("promotion must preserve the complete quarantine and retirement path")
    decision = record.get("decision", {})
    if decision.get("procedure_state") != "routable" or decision.get("support_state_effect") != "none" or decision.get("historical_runtime_claimed") is not False:
        errors.append("fixture procedure promotion cannot promote chapter support or claim historical runtime behavior")
    return errors


def mutate(value: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = deepcopy(value)
    target: Any = candidate
    for segment in mutation["path"][:-1]:
        target = target[segment]
    target[mutation["path"][-1]] = mutation["value"]
    return candidate


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    found = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if found:
        raise SystemExit("Valid procedural trace promotion failed:\n - " + "\n - ".join(found))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    for path in mutations:
        mutation = load(path)
        candidate = mutate(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in item for item in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(f"Procedural trace-promotion harness passed: 1 bounded four-project record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
