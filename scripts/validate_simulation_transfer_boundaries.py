#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "simulation_transfer_boundaries" / "fixtures"
SCHEMA = ROOT / "schemas" / "simulation_contract_record.schema.json"

TRANSFER_WITH_SUPPORT = {"transfer_within_boundary", "reduced_scope", "residualized"}
BLOCKING_TRANSFERS = {"blocked", "scenario_only", "speculative_only", "not_evaluated"}
PROMOTION_LANGUAGE = {"promotes_core_claim", "synthetic-test-backed", "empirical-test-backed", "prototype-backed"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


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


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    contract = value.get("simulation_contract_record")
    if not isinstance(contract, dict):
        errors.append(f"{relative}: simulation_contract_record must be an object.")
    review = value.get("transfer_review")
    if not isinstance(review, dict):
        errors.append(f"{relative}: transfer_review must be an object.")
    non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    for field in (
        "input_assumptions",
        "demand_estimate",
        "resource_bill",
        "capacity_bottlenecks",
        "omitted_variables",
        "approximation_liberties",
        "instrumentation_effects",
        "residual_risks",
        "evidence_refs",
        "non_claims",
    ):
        require_nonempty_list(contract, field, errors, f"{relative}:simulation_contract_record")

    fidelity_declared = require_bool(review, "fidelity_declared", errors, f"{relative}:transfer_review")
    resources_declared = require_bool(review, "resources_declared", errors, f"{relative}:transfer_review")
    bottlenecks_declared = require_bool(review, "bottlenecks_declared", errors, f"{relative}:transfer_review")
    omissions_declared = require_bool(review, "omissions_declared", errors, f"{relative}:transfer_review")
    instrumentation_recorded = require_bool(review, "instrumentation_recorded", errors, f"{relative}:transfer_review")
    boundary_respected = require_bool(review, "boundary_respected", errors, f"{relative}:transfer_review")
    residual_or_downgrade_recorded = require_bool(
        review,
        "residual_or_downgrade_recorded",
        errors,
        f"{relative}:transfer_review",
    )
    overclaim_requested = require_bool(review, "overclaim_requested", errors, f"{relative}:transfer_review")
    support_promotion_requested = require_bool(
        review,
        "support_promotion_requested",
        errors,
        f"{relative}:transfer_review",
    )
    if errors:
        return errors

    transfer_decision = str(contract["transfer_decision"])
    claim_class = str(contract["claim_class"])
    support_state_effect = str(contract["support_state_effect"])
    failure_text = str(contract["failure_behavior"]).lower()
    residual_text = text_blob(contract["residual_risks"])
    boundary_text = text_blob(
        contract["supported_claim_boundary"],
        contract["observed_result_boundary"],
        review.get("requested_claim_boundary", ""),
        review.get("result_use", ""),
    )
    non_claim_text = text_blob(non_claims, contract["non_claims"])

    if transfer_decision in TRANSFER_WITH_SUPPORT:
        if contract["fidelity_state"] != "declared" or not fidelity_declared:
            errors.append(f"{relative}: transferred or reduced-scope simulation claims require declared fidelity.")
        if not resources_declared:
            errors.append(f"{relative}: transferred or reduced-scope simulation claims require a declared resource bill.")
        if not bottlenecks_declared:
            errors.append(f"{relative}: transferred or reduced-scope simulation claims require capacity bottlenecks.")
        if not omissions_declared:
            errors.append(f"{relative}: transferred or reduced-scope simulation claims require omitted-variable disclosure.")
        if not instrumentation_recorded:
            errors.append(f"{relative}: transferred or reduced-scope simulation claims require instrumentation effects.")

    if transfer_decision == "transfer_within_boundary":
        if not boundary_respected or overclaim_requested:
            errors.append(f"{relative}: transfer_within_boundary requires respected boundaries and no overclaim.")
        if "world" in boundary_text or "deployment" in boundary_text:
            errors.append(f"{relative}: transfer_within_boundary cannot silently become world or deployment evidence.")

    if transfer_decision in {"reduced_scope", "residualized", "blocked"}:
        if not residual_or_downgrade_recorded:
            errors.append(f"{relative}: reduced, residualized, or blocked transfer requires residual or downgrade record.")
        if "residual" not in residual_text and "downgrade" not in failure_text and "blocked" not in failure_text:
            errors.append(f"{relative}: reduced, residualized, or blocked transfer must name residual, downgrade, or blocked behavior.")

    if claim_class in {"scenario_exploration", "speculative_thought_experiment"}:
        if transfer_decision == "transfer_within_boundary":
            errors.append(f"{relative}: scenario or speculative simulations cannot become transfer_within_boundary evidence.")
        if "scenario" not in boundary_text and "speculative" not in boundary_text:
            errors.append(f"{relative}: scenario/speculative simulations must keep scenario or speculative boundaries visible.")

    if not boundary_respected and transfer_decision not in BLOCKING_TRANSFERS | {"reduced_scope", "residualized"}:
        errors.append(f"{relative}: boundary violations must block, reduce scope, or residualize transfer.")
    if overclaim_requested and transfer_decision not in {"blocked", "reduced_scope", "residualized"}:
        errors.append(f"{relative}: overclaim requests must block, reduce scope, or residualize transfer.")

    if support_promotion_requested or support_state_effect in PROMOTION_LANGUAGE:
        errors.append(f"{relative}: simulation-transfer fixtures cannot promote support state.")
    if support_state_effect == "eligible_for_bounded_evidence_review" and transfer_decision != "transfer_within_boundary":
        errors.append(f"{relative}: bounded evidence review eligibility requires transfer within boundary.")

    if "does not promote" not in non_claim_text or "support" not in non_claim_text:
        errors.append(f"{relative}: non_claims must state support-state non-promotion.")
    for term in ("physical", "simulator", "transfer"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must deny {term} claims or results.")

    return errors


def fixture_errors(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    contract = value.get("simulation_contract_record")
    if not isinstance(contract, dict):
        return [f"{relative}: simulation_contract_record must be an object."]
    errors = validate_value(contract, schema, f"{relative}:simulation_contract_record")
    if not errors:
        errors.extend(semantic_errors(value, relative))
    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No simulation-transfer fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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

        current_errors = fixture_errors(value, schema, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Simulation transfer boundary harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Simulation transfer boundary harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
