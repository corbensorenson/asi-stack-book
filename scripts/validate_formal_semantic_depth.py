#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "formal_semantic_depth_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "formal_semantic_depth_record.valid.json"
MUTATIONS = ROOT / "experiments" / "formal_semantic_depth" / "fixtures"
EXPECTED_SOURCES = {"cca_project", "moecot_manifest_project", "corbens_best_model_possible_project"}
EXPECTED_LANES = {"field_presence", "finite_route", "derived_invariant", "executable_model_bridge", "implementation_binding"}
REQUIRED_ASSUMPTIONS = {"clock", "concurrency", "event_completeness", "adversarial_log"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("semantic-depth lineage must name the three historical-project sources exactly")
    abstraction = record.get("abstraction_map", [])
    if any(not row.get("losses") for row in abstraction):
        errors.append("every abstraction mapping must disclose semantic losses")
    assumptions = record.get("assumptions", [])
    assumption_classes = {row.get("class") for row in assumptions}
    if not REQUIRED_ASSUMPTIONS.issubset(assumption_classes):
        errors.append("clock, concurrency, event-completeness, and adversarial-log assumptions are required")

    lanes = record.get("depth_lanes", [])
    lane_names = [row.get("lane") for row in lanes]
    if set(lane_names) != EXPECTED_LANES or len(lane_names) != len(EXPECTED_LANES):
        errors.append("semantic-depth record must contain each depth lane exactly once")
    lane_map = {row.get("lane"): row for row in lanes}
    for lane in ("finite_route", "derived_invariant", "executable_model_bridge"):
        row = lane_map.get(lane, {})
        if row.get("result") == "passed" and (not row.get("artifact_refs") or not row.get("verifier_ref")):
            errors.append("passing formal or executable lanes require artifacts and verifier identity")
    if lane_map.get("field_presence", {}).get("authorized_statement", "").lower().find("runtime") >= 0:
        errors.append("field presence cannot authorize a runtime statement")
    if lane_map.get("finite_route", {}).get("authorized_statement", "").lower().find("deployed") >= 0:
        errors.append("a finite route cannot authorize deployed behavior")
    if lane_map.get("derived_invariant", {}).get("result") == "passed" and lane_map.get("finite_route", {}).get("result") != "passed":
        errors.append("derived invariant cannot pass when its finite route dependency does not pass")

    excluded = record.get("excluded_runtime_behavior", [])
    for required in ("distributed clocks", "concurrent revocation races", "log completeness", "deployed denial"):
        if required not in excluded:
            errors.append("excluded runtime behavior must name clocks, concurrency, log completeness, and deployment")
            break
    binding = record.get("implementation_binding", {})
    binding_lane = lane_map.get("implementation_binding", {})
    if binding.get("state") == "unbound":
        if binding.get("artifact_refs") or binding.get("verifier_ref") or binding.get("observed_runtime_refs"):
            errors.append("unbound implementation cannot carry implementation or runtime evidence")
        if binding_lane.get("result") != "absent" or binding_lane.get("semantic_binding") != "absent":
            errors.append("unbound implementation must remain absent in the depth lane")
    if binding.get("state") == "bound_and_observed" and (not binding.get("artifact_refs") or not binding.get("verifier_ref") or not binding.get("observed_runtime_refs")):
        errors.append("observed implementation binding requires artifact, verifier, and runtime references")

    decision = record.get("consumer_decision", {})
    if binding.get("state") != "bound_and_observed" and decision.get("runtime_claim_allowed"):
        errors.append("runtime claims require a bound and observed implementation")
    absent_semantics = [row for row in lanes if row.get("semantic_binding") == "absent"]
    if absent_semantics and decision.get("semantic_adequacy") == "adequate_for_finite_predicate" and decision.get("runtime_claim_allowed"):
        errors.append("absent semantic binding cannot be laundered into runtime adequacy")
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("hand-authored semantic-depth fixtures cannot promote support")
    if not record.get("by_construction_properties") or not excluded or not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("semantic-depth record must preserve construction properties, exclusions, blockers, and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    changes = mutation.get("changes") if mutation["operation"] == "batch_set" else [mutation]
    for change in changes:
        target: Any = value
        for segment in change["path"][:-1]:
            target = target[segment]
        leaf = change["path"][-1]
        if change.get("operation", "set") == "delete":
            del target[leaf]
        else:
            target[leaf] = change["value"]
    return value


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid formal semantic-depth record failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No formal semantic-depth mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(f"Formal semantic-depth harness passed: 1 blocked three-project record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
