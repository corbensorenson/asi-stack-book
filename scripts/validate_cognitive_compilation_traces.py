#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "cognitive_compilation_traces" / "fixtures"
SEMANTIC_ATOM_SCHEMA = ROOT / "schemas" / "semantic_atom.schema.json"

BAD_OBLIGATION_STATES = {"deferred", "rejected", "unknown", "blocked"}
EXPECTED_RESULTS = {"eligible_for_trace_review", "blocks_promotion"}
VALID_SUPPORT_EFFECTS = {
    "none",
    "record_shape_only",
    "argument_only",
    "eligible_for_trace_review",
    "blocks_promotion",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def require_object(value: dict[str, Any], field: str, errors: list[str], relative: str) -> dict[str, Any]:
    item = value.get(field)
    if not isinstance(item, dict):
        errors.append(f"{relative}: {field} must be an object.")
        return {}
    return item


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value if str(item).strip()}


def require_text_boundary(items: list[Any], errors: list[str], relative: str) -> None:
    text = " ".join(str(item).lower() for item in items)
    if "does not" not in text:
        errors.append(f"{relative}: non_claims must include explicit 'does not' boundaries.")
    if "promote" not in text and "support state" not in text:
        errors.append(f"{relative}: non_claims must mention support-state non-promotion.")


def schema_errors_for_scenario(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    atoms = value.get("semantic_atoms")
    if not isinstance(atoms, list) or not atoms:
        errors.append(f"{relative}: semantic_atoms must be a non-empty list.")
        return errors
    for index, atom in enumerate(atoms):
        errors.extend(validate_value(atom, schema, f"{relative}:semantic_atoms[{index}]"))
    return errors


def validate_source_plan(plan: dict[str, Any], errors: list[str], relative: str) -> tuple[str, set[str], set[str], set[str]]:
    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str) or not plan_id.strip():
        errors.append(f"{relative}:source_plan.plan_id must be a non-empty string.")
        plan_id = ""
    requirements = string_set(require_nonempty_list(plan, "requirements", errors, f"{relative}:source_plan"))
    constraints = string_set(require_nonempty_list(plan, "constraints", errors, f"{relative}:source_plan"))
    artifacts = string_set(require_nonempty_list(plan, "expected_artifacts", errors, f"{relative}:source_plan"))
    if not isinstance(plan.get("authority_ceiling"), str) or not plan["authority_ceiling"].strip():
        errors.append(f"{relative}:source_plan.authority_ceiling must be a non-empty string.")
    return str(plan_id), requirements, constraints, artifacts


def validate_atoms(
    atoms: list[dict[str, Any]],
    plan_id: str,
    requirements: set[str],
    constraints: set[str],
    expected_artifacts: set[str],
    expected_result: str,
    errors: list[str],
    relative: str,
) -> tuple[set[str], set[str]]:
    atom_ids: set[str] = set()
    receipt_refs: set[str] = set()
    observed_obligations: set[str] = set()
    observed_constraints: set[str] = set()
    observed_artifacts: set[str] = set()

    for index, atom in enumerate(atoms):
        atom_relative = f"{relative}:semantic_atoms[{index}]"
        atom_id = str(atom.get("atom_id", ""))
        if not atom_id:
            errors.append(f"{atom_relative}: atom_id must be non-empty.")
        elif atom_id in atom_ids:
            errors.append(f"{atom_relative}: duplicate atom_id {atom_id!r}.")
        atom_ids.add(atom_id)

        non_claims = require_nonempty_list(atom, "non_claims", errors, atom_relative)
        if non_claims:
            require_text_boundary(non_claims, errors, f"{atom_relative}.non_claims")

        if atom.get("source_plan_ref") != plan_id:
            errors.append(f"{atom_relative}: source_plan_ref must match source_plan.plan_id.")

        obligations = string_set(require_nonempty_list(atom, "obligation_refs", errors, atom_relative))
        observed_obligations.update(obligations)
        observed_constraints.update(string_set(atom.get("constraints")))
        observed_artifacts.update(string_set(atom.get("outputs")))
        target_artifact = str(atom.get("target_artifact_ref", ""))
        if target_artifact:
            observed_artifacts.add(target_artifact)

        status_rows = atom.get("obligation_status")
        if not isinstance(status_rows, list) or not status_rows:
            errors.append(f"{atom_relative}: obligation_status must be a non-empty list.")
        else:
            status_refs = {str(row.get("obligation_ref", "")) for row in status_rows if isinstance(row, dict)}
            missing_status = sorted(obligations - status_refs)
            extra_status = sorted(status_refs - obligations)
            if missing_status:
                errors.append(f"{atom_relative}: obligation_status missing refs {missing_status}.")
            if extra_status:
                errors.append(f"{atom_relative}: obligation_status has refs outside obligation_refs {extra_status}.")
            if expected_result == "eligible_for_trace_review":
                bad_statuses = sorted(
                    {
                        str(row.get("status", ""))
                        for row in status_rows
                        if isinstance(row, dict) and row.get("status") in BAD_OBLIGATION_STATES
                    }
                )
                if bad_statuses:
                    errors.append(f"{atom_relative}: eligible traces cannot carry bad obligation states {bad_statuses}.")

        if atom.get("lowering_state") == "lowered":
            if atom.get("ir_validity_state") != "well_formed":
                errors.append(f"{atom_relative}: lowered atoms require ir_validity_state well_formed.")
            if atom.get("validator_status") != "passed":
                errors.append(f"{atom_relative}: lowered atoms require validator_status passed.")

        receipt_ref = str(atom.get("lowering_receipt", ""))
        if not receipt_ref.startswith("receipt://"):
            errors.append(f"{atom_relative}: lowering_receipt must start with receipt://.")
        else:
            receipt_refs.add(receipt_ref)

        if not string_set(atom.get("source_refs")):
            errors.append(f"{atom_relative}: source_refs must be non-empty.")
        support_effect = str(atom.get("support_state_effect", ""))
        if support_effect not in VALID_SUPPORT_EFFECTS:
            errors.append(f"{atom_relative}: unsupported support_state_effect {support_effect!r}.")

    missing_requirements = sorted(requirements - observed_obligations)
    if missing_requirements:
        errors.append(f"{relative}: semantic atoms dropped source requirements {missing_requirements}.")
    missing_constraints = sorted(constraints - observed_constraints)
    if missing_constraints:
        errors.append(f"{relative}: semantic atoms dropped source constraints {missing_constraints}.")
    missing_artifacts = sorted(expected_artifacts - observed_artifacts)
    if missing_artifacts:
        errors.append(f"{relative}: semantic atoms do not cover expected artifacts {missing_artifacts}.")

    return atom_ids, receipt_refs


def validate_receipts(
    receipts: list[dict[str, Any]],
    plan_id: str,
    requirements: set[str],
    expected_artifacts: set[str],
    atom_ids: set[str],
    atom_receipts: set[str],
    expected_result: str,
    errors: list[str],
    relative: str,
) -> set[str]:
    receipt_ids: set[str] = set()
    preserved: set[str] = set()

    for index, receipt in enumerate(receipts):
        receipt_relative = f"{relative}:lowering_receipts[{index}]"
        receipt_id = str(receipt.get("receipt_id", ""))
        if not receipt_id.startswith("receipt://"):
            errors.append(f"{receipt_relative}: receipt_id must start with receipt://.")
        elif receipt_id in receipt_ids:
            errors.append(f"{receipt_relative}: duplicate receipt_id {receipt_id!r}.")
        receipt_ids.add(receipt_id)

        if receipt.get("source_plan_ref") != plan_id:
            errors.append(f"{receipt_relative}: source_plan_ref must match source_plan.plan_id.")
        receipt_atoms = string_set(require_nonempty_list(receipt, "atom_refs", errors, receipt_relative))
        unknown_atoms = sorted(receipt_atoms - atom_ids)
        if unknown_atoms:
            errors.append(f"{receipt_relative}: atom_refs include unknown atoms {unknown_atoms}.")
        target_artifact = str(receipt.get("target_artifact_ref", ""))
        if target_artifact not in expected_artifacts:
            errors.append(f"{receipt_relative}: target_artifact_ref must be one of source_plan.expected_artifacts.")
        preserved_obligations = string_set(require_nonempty_list(receipt, "preserved_obligations", errors, receipt_relative))
        preserved.update(preserved_obligations)
        require_nonempty_list(receipt, "validator_refs", errors, receipt_relative)
        if not isinstance(receipt.get("introduced_assumptions"), list):
            errors.append(f"{receipt_relative}: introduced_assumptions must be a list.")
        if not isinstance(receipt.get("residuals"), list):
            errors.append(f"{receipt_relative}: residuals must be a list.")
        non_claims = require_nonempty_list(receipt, "non_claims", errors, receipt_relative)
        if non_claims:
            require_text_boundary(non_claims, errors, f"{receipt_relative}.non_claims")

    missing_receipts = sorted(atom_receipts - receipt_ids)
    if missing_receipts:
        errors.append(f"{relative}: atom lowering_receipts not represented by lowering_receipts {missing_receipts}.")
    if expected_result == "eligible_for_trace_review":
        missing_preserved = sorted(requirements - preserved)
        if missing_preserved:
            errors.append(f"{relative}: lowering receipts did not preserve required obligations {missing_preserved}.")

    return receipt_ids


def validate_target_audit(
    audit: dict[str, Any],
    plan_id: str,
    expected_artifacts: set[str],
    receipt_ids: set[str],
    expected_result: str,
    errors: list[str],
    relative: str,
) -> None:
    if audit.get("source_plan_ref") != plan_id:
        errors.append(f"{relative}:target_audit.source_plan_ref must match source_plan.plan_id.")
    if audit.get("target_artifact_ref") not in expected_artifacts:
        errors.append(f"{relative}:target_audit.target_artifact_ref must be one of source_plan.expected_artifacts.")
    audit_receipts = string_set(require_nonempty_list(audit, "lowering_receipt_refs", errors, f"{relative}:target_audit"))
    unknown_receipts = sorted(audit_receipts - receipt_ids)
    if unknown_receipts:
        errors.append(f"{relative}:target_audit.lowering_receipt_refs include unknown receipts {unknown_receipts}.")

    non_claims = require_nonempty_list(audit, "non_claims", errors, f"{relative}:target_audit")
    if non_claims:
        require_text_boundary(non_claims, errors, f"{relative}:target_audit.non_claims")
    support_effect = str(audit.get("support_state_effect", ""))
    if support_effect not in VALID_SUPPORT_EFFECTS:
        errors.append(f"{relative}:target_audit.support_state_effect has unsupported value {support_effect!r}.")

    if expected_result == "eligible_for_trace_review":
        if audit.get("validator_status") != "passed":
            errors.append(f"{relative}: eligible target audits require validator_status passed.")
        if audit.get("obligation_preservation") != "all_required_obligations_preserved":
            errors.append(
                f"{relative}: eligible target audits require all_required_obligations_preserved."
            )
    if expected_result == "blocks_promotion":
        if audit.get("validator_status") == "passed" and audit.get("obligation_preservation") == "all_required_obligations_preserved":
            errors.append(f"{relative}: blocks_promotion target audits must identify a failed validator or lost obligation.")


def validate_repair_trace(
    repair: dict[str, Any],
    atom_ids: set[str],
    expected_result: str,
    errors: list[str],
    relative: str,
) -> None:
    scope = str(repair.get("repair_scope", ""))
    failed_atom = str(repair.get("failed_atom_ref", ""))
    if failed_atom not in atom_ids:
        errors.append(f"{relative}:repair_trace.failed_atom_ref must name a semantic atom.")
    require_nonempty_list(repair, "repair_actions", errors, f"{relative}:repair_trace")
    before = string_set(require_nonempty_list(repair, "before_obligations", errors, f"{relative}:repair_trace"))
    after = string_set(require_nonempty_list(repair, "after_obligations", errors, f"{relative}:repair_trace"))
    changed_atoms = string_set(require_nonempty_list(repair, "changed_atoms", errors, f"{relative}:repair_trace"))
    if not isinstance(repair.get("ledger_update_ref"), str) or not repair["ledger_update_ref"].strip():
        errors.append(f"{relative}:repair_trace.ledger_update_ref must be a non-empty string.")
    non_claims = require_nonempty_list(repair, "non_claims", errors, f"{relative}:repair_trace")
    if non_claims:
        require_text_boundary(non_claims, errors, f"{relative}:repair_trace.non_claims")

    if scope == "same_atom":
        outside_scope = sorted(changed_atoms - {failed_atom})
        if outside_scope:
            errors.append(f"{relative}: same_atom repair changed atoms outside the failed atom {outside_scope}.")
    elif scope == "dependent_atoms":
        if failed_atom not in changed_atoms:
            errors.append(f"{relative}: dependent_atoms repair must include the failed atom.")
    elif scope == "whole_graph":
        if expected_result == "eligible_for_trace_review":
            errors.append(f"{relative}: eligible traces cannot use whole_graph repair scope.")
    elif scope != "human_review":
        errors.append(f"{relative}:repair_trace.repair_scope has unsupported value {scope!r}.")

    if expected_result == "eligible_for_trace_review":
        missing_after = sorted(before - after)
        if missing_after:
            errors.append(f"{relative}: repair trace dropped obligations after repair {missing_after}.")


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    expected_result = str(value.get("expected_result", ""))
    if expected_result not in EXPECTED_RESULTS:
        errors.append(f"{relative}: expected_result must be one of {sorted(EXPECTED_RESULTS)}.")
    non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if non_claims:
        require_text_boundary(non_claims, errors, f"{relative}:non_claims")

    source_plan = require_object(value, "source_plan", errors, relative)
    atoms = value.get("semantic_atoms")
    receipts = value.get("lowering_receipts")
    target_audit = require_object(value, "target_audit", errors, relative)
    repair_trace = require_object(value, "repair_trace", errors, relative)
    if not isinstance(atoms, list) or not atoms:
        errors.append(f"{relative}: semantic_atoms must be a non-empty list.")
        atoms = []
    if not isinstance(receipts, list) or not receipts:
        errors.append(f"{relative}: lowering_receipts must be a non-empty list.")
        receipts = []
    if errors:
        return errors

    plan_id, requirements, constraints, expected_artifacts = validate_source_plan(source_plan, errors, relative)
    atom_ids, atom_receipts = validate_atoms(
        atoms,
        plan_id,
        requirements,
        constraints,
        expected_artifacts,
        expected_result,
        errors,
        relative,
    )
    receipt_ids = validate_receipts(
        receipts,
        plan_id,
        requirements,
        expected_artifacts,
        atom_ids,
        atom_receipts,
        expected_result,
        errors,
        relative,
    )
    validate_target_audit(target_audit, plan_id, expected_artifacts, receipt_ids, expected_result, errors, relative)
    validate_repair_trace(repair_trace, atom_ids, expected_result, errors, relative)

    return errors


def main() -> None:
    schema = load_json(SEMANTIC_ATOM_SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No cognitive compilation trace fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0

    for fixture in fixtures:
        expectation = fixture_expectation(fixture)
        relative = str(fixture.relative_to(ROOT))
        if expectation is None:
            errors.append(f"{relative}: fixture name must start with valid_ or invalid_.")
            continue
        value = load_json(fixture)
        if not isinstance(value, dict):
            errors.append(f"{relative}: fixture root must be an object.")
            continue
        scenario_errors = schema_errors_for_scenario(value, schema, relative)
        scenario_errors.extend(semantic_errors(value, relative))
        if expectation:
            valid_count += 1
            errors.extend(scenario_errors)
        else:
            invalid_count += 1
            if not scenario_errors:
                errors.append(f"{relative}: expected-invalid fixture passed validation.")

    if errors:
        print("Cognitive compilation trace harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Cognitive compilation trace harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
