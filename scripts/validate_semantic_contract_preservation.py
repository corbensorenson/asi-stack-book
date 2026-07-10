#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "semantic_contract_preservation_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "semantic_contract_preservation_record.valid.json"
MUTATIONS = ROOT / "experiments" / "semantic_contract_preservation" / "fixtures"
EXPECTED_SOURCES = {
    "cca_project", "moecot_manifest_project", "corbens_best_model_possible_project",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("semantic preservation lineage must name the three historical-project sources exactly")

    source = record.get("source_contract", {})
    source_fields = set(source.get("fields", []))
    requirements = set(source.get("requirements", []))
    source_authority = set(source.get("authority_refs", []))
    target = record.get("target_contract", {})
    target_fields = set(target.get("fields", []))
    target_requirements = set(target.get("requirement_refs", []))
    target_authority = set(target.get("authority_refs", []))
    ir = record.get("semantic_ir", {})

    lineage = record.get("field_lineage", [])
    covered_fields = {entry.get("source_field") for entry in lineage}
    if covered_fields != source_fields:
        errors.append("field lineage must cover every source field without omission or invention")
    ambiguity_ids = {entry.get("ambiguity_id") for entry in record.get("ambiguity_ledger", [])}
    for entry in lineage:
        if entry.get("transform") == "omitted":
            errors.append("field lineage cannot mark a source field omitted in an accepted compilation")
        if entry.get("source_field") not in source_fields or entry.get("target_field") not in target_fields:
            errors.append("field lineage endpoints must resolve in the source and target contracts")
        if not source_authority.issubset(set(entry.get("authority_refs", []))):
            errors.append("field lineage must retain the source authority binding")
        if not set(entry.get("ambiguity_refs", [])).issubset(ambiguity_ids):
            errors.append("field lineage ambiguity references must resolve in the ambiguity ledger")

    accepted = record.get("decision", {}).get("compile_state") == "accepted"
    for ambiguity in record.get("ambiguity_ledger", []):
        if ambiguity.get("source_field") not in source_fields:
            errors.append("ambiguity ledger entries must bind a source field")
        if ambiguity.get("state") == "resolved" and not ambiguity.get("resolution_ref"):
            errors.append("resolved ambiguity requires a resolution reference")
        if ambiguity.get("state") in {"unresolved", "deferred"} and ambiguity.get("strict_compile_effect") == "allow":
            errors.append("unresolved ambiguity cannot allow strict compilation")
        if accepted and ambiguity.get("state") in {"unresolved", "deferred"}:
            errors.append("accepted compilation cannot conceal unresolved ambiguity")

    if set(ir.get("obligation_refs", [])) != requirements:
        errors.append("semantic IR must carry every source preservation obligation")
    if not source_authority.issubset(set(ir.get("authority_refs", []))):
        errors.append("semantic IR must preserve source authority")
    if not set(ir.get("ambiguity_refs", [])).issubset(ambiguity_ids):
        errors.append("semantic IR ambiguity references must resolve in the ledger")
    if target_requirements != requirements:
        errors.append("target contract must retain every source requirement")
    if not source_authority.issubset(target_authority):
        errors.append("target contract lost source authority")

    obligations = record.get("preservation_obligations", [])
    obligation_refs = {entry.get("requirement_ref") for entry in obligations}
    if obligation_refs != requirements:
        errors.append("preservation obligations must cover every source requirement exactly")
    semantic_claim_valid = True
    for entry in obligations:
        if entry.get("ir_node_ref") not in set(ir.get("node_ids", [])):
            errors.append("preservation obligation must bind a semantic IR node")
        if entry.get("target_field") not in target_fields:
            errors.append("preservation obligation must bind a target field")
        if entry.get("status") != "preserved" or not entry.get("semantic_validator_ref"):
            semantic_claim_valid = False
    if accepted and not semantic_claim_valid:
        errors.append("accepted compilation requires every source requirement to remain semantically preserved")

    pass_bundle = record.get("pass_bundle", {})
    if accepted and (
        pass_bundle.get("validator_result") != "pass"
        or not pass_bundle.get("semantic_validator_ref")
        or not pass_bundle.get("authority_preserved")
    ):
        errors.append("accepted pass bundle requires passing semantic validation and preserved authority")
    if accepted and not pass_bundle.get("failure_refs"):
        errors.append("accepted pass bundle cannot erase the known failure bundle")

    repair = record.get("repair", {})
    declared = set(repair.get("declared_scope", []))
    actual = set(repair.get("actual_mutation_refs", []))
    blast = set(repair.get("blast_radius_refs", []))
    if not actual.issubset(declared) or not blast.issubset(declared):
        errors.append("localized repair mutated outside its declared scope")
    if actual != blast:
        errors.append("repair blast-radius receipt must equal the observed mutation set")
    if not set(repair.get("failed_node_refs", [])).issubset(set(ir.get("node_ids", []))):
        errors.append("repair failure references must bind stable semantic IR node identities")
    if accepted and repair.get("post_repair_validator_result") != "pass":
        errors.append("accepted repair requires a passing post-repair semantic validator")

    digest = record.get("digest_parity", {})
    if digest.get("semantic_preservation_claim_allowed") and (
        not digest.get("semantic_validator_ref") or not semantic_claim_valid
    ):
        errors.append("digest parity cannot establish semantic preservation without semantic validators")

    decision = record.get("decision", {})
    if decision.get("strict_execution_allowed"):
        errors.append("fixture-only compilation cannot authorize strict execution")
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("fixture-only semantic preservation cannot promote support")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("semantic preservation record must retain promotion blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    leaf = mutation["path"][-1]
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
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid semantic contract record failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No expected-invalid semantic contract mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(
                f"{path.relative_to(ROOT)} did not produce expected error "
                f"{mutation['expected_error']!r}: {found}"
            )
    print(
        "Semantic contract preservation harness passed: "
        f"1 blocked three-project lineage record and {len(mutations)} expected-invalid mutations."
    )


if __name__ == "__main__":
    main()
