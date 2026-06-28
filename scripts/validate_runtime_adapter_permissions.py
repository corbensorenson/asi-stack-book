#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "runtime_adapter_permissions" / "fixtures"

SCHEMAS = {
    "typed_job": ROOT / "schemas" / "typed_job.schema.json",
    "runtime_adapter_invocation": ROOT / "schemas" / "runtime_adapter_invocation.schema.json",
    "authority_use_receipt": ROOT / "schemas" / "authority_use_receipt.schema.json",
}

ACTIVE_INVOCATION_STATES = {"approved", "executed"}
HIGH_IMPACT_CLASSES = {"high_impact", "irreversible", "unknown"}
HIGH_RISK_TIERS = {"high", "critical", "unknown"}
NO_APPROVAL_VALUES = {"", "none", "not_required"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemas() -> dict[str, Any]:
    return {name: load_json(path) for name, path in SCHEMAS.items()}


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("typed_job", "runtime_adapter_invocation"):
        if field not in value:
            errors.append(f"{relative}: missing {field}.")
            continue
        errors.extend(validate_value(value[field], schemas[field], f"{relative}:{field}"))
    if "authority_use_receipt" in value:
        errors.extend(
            validate_value(value["authority_use_receipt"], schemas["authority_use_receipt"], f"{relative}:authority_use_receipt")
        )
    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    if not nonempty_list(value.get("non_claims")):
        errors.append(f"{relative}: non_claims must be a non-empty list.")
    if errors:
        return errors

    job = value["typed_job"]
    invocation = value["runtime_adapter_invocation"]
    authority_receipt = value.get("authority_use_receipt")

    job_id = str(job["job_id"])
    if invocation["job_id"] != job_id:
        errors.append(f"{relative}: invocation.job_id must match typed_job.job_id.")
    if invocation["adapter_id"] != job["runtime_adapter"]:
        errors.append(f"{relative}: invocation.adapter_id must match typed_job.runtime_adapter.")

    permissions = {str(permission) for permission in job.get("permissions", [])}
    for required in (invocation["capability"], invocation["permission_required"]):
        if str(required) not in permissions:
            errors.append(f"{relative}: typed_job.permissions must include {required!r}.")

    state = str(invocation["invocation_state"])
    high_impact = invocation["impact_class"] in HIGH_IMPACT_CLASSES or invocation["risk_tier"] in HIGH_RISK_TIERS
    approval_record = str(invocation.get("approval_record", ""))
    approval_scope = str(invocation.get("approval_scope", ""))
    approval_expiry = str(invocation.get("approval_expiry", ""))

    if job.get("approval_state") in {"denied", "expired"} and state in ACTIVE_INVOCATION_STATES:
        errors.append(f"{relative}: active invocation cannot use a denied or expired typed-job approval_state.")

    if high_impact and invocation.get("approval_required") is not True:
        errors.append(f"{relative}: high-impact or high-risk invocation must set approval_required true.")
    if invocation.get("approval_required") is True:
        if not approval_record.startswith("approval://"):
            errors.append(f"{relative}: approval_required invocation must carry approval:// approval_record.")
        if not approval_scope or approval_scope in NO_APPROVAL_VALUES:
            errors.append(f"{relative}: approval_required invocation must carry a scoped approval_scope.")
        if approval_expiry in NO_APPROVAL_VALUES or approval_expiry.startswith("expired"):
            errors.append(f"{relative}: approval_required invocation must carry a non-expired approval_expiry marker.")
        if job.get("approval_state") != "approved":
            errors.append(f"{relative}: approval_required invocation needs typed_job.approval_state == approved.")
    else:
        if approval_record not in NO_APPROVAL_VALUES:
            errors.append(f"{relative}: no-approval invocation must not carry a positive approval_record.")

    if state in ACTIVE_INVOCATION_STATES:
        if not str(invocation.get("authority_handle", "")).startswith("handle://"):
            errors.append(f"{relative}: active invocation must carry a handle:// authority_handle.")
        if not str(invocation.get("effect_lease", "")).startswith("lease://"):
            errors.append(f"{relative}: active invocation must carry a lease:// effect_lease.")

    if state == "executed":
        if not str(invocation.get("effect_receipt", "")).startswith("receipt://"):
            errors.append(f"{relative}: executed invocation must carry a receipt:// effect_receipt.")
        if not str(invocation.get("pre_state_ref", "")).startswith("state://"):
            errors.append(f"{relative}: executed invocation must carry a state:// pre_state_ref.")
        if not str(invocation.get("post_state_ref", "")).startswith("state://"):
            errors.append(f"{relative}: executed invocation must carry a state:// post_state_ref.")
        if not nonempty_list(invocation.get("verification_refs")):
            errors.append(f"{relative}: executed invocation must carry verification_refs.")
        if not nonempty_list(invocation.get("audit_refs")):
            errors.append(f"{relative}: executed invocation must carry audit_refs.")

    external_effect = nonempty_list(invocation.get("external_side_effects"))
    rollback_handle = str(invocation.get("rollback_handle", ""))
    irreversible_residuals = invocation.get("irreversible_residuals", [])
    if state == "executed" and (external_effect or high_impact):
        has_rollback = rollback_handle.startswith("rollback://")
        has_residuals = nonempty_list(irreversible_residuals)
        if not has_rollback and not has_residuals:
            errors.append(f"{relative}: executed external or high-impact invocation needs rollback_handle or irreversible_residuals.")
    if invocation["impact_class"] == "irreversible" and not nonempty_list(irreversible_residuals):
        errors.append(f"{relative}: irreversible invocation must record irreversible_residuals.")

    if invocation.get("support_state_effect") not in {"record_shape_only", "argument_only", "blocks_promotion"}:
        errors.append(f"{relative}: support_state_effect must stay in a non-promoting state.")

    scenario_non_claims = " ".join(str(item).lower() for item in value.get("non_claims", []))
    invocation_non_claims = " ".join(str(item).lower() for item in invocation.get("non_claims", []))
    if "does not" not in scenario_non_claims or "does not" not in invocation_non_claims:
        errors.append(f"{relative}: scenario and invocation non_claims must include explicit non-claim boundaries.")
    if "promote" not in scenario_non_claims and "support state" not in scenario_non_claims:
        errors.append(f"{relative}: scenario non_claims must mention support-state non-promotion.")

    if str(invocation.get("authority_handle", "")).startswith("handle://"):
        if not isinstance(authority_receipt, dict):
            errors.append(f"{relative}: authority_handle requires authority_use_receipt.")
        else:
            if authority_receipt.get("handle_id") != invocation.get("authority_handle"):
                errors.append(f"{relative}: authority_use_receipt.handle_id must match invocation.authority_handle.")
            if authority_receipt.get("allowed_action") != invocation.get("capability"):
                errors.append(f"{relative}: authority_use_receipt.allowed_action must match invocation.capability.")
            if invocation.get("approval_required") is True and authority_receipt.get("approval_record") != approval_record:
                errors.append(f"{relative}: authority_use_receipt.approval_record must match invocation approval_record.")
            lifecycle = authority_receipt.get("scif_lifecycle", [])
            for required_state in ("spawn", "execute", "audit"):
                if required_state not in lifecycle:
                    errors.append(f"{relative}: authority_use_receipt.scif_lifecycle missing {required_state!r}.")

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
        raise SystemExit(f"No runtime adapter permission fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
            errors.append(f"{relative}: scenario must contain a JSON object.")
            continue
        scenario_errors = schema_errors_for_scenario(value, schemas, relative)
        if not scenario_errors:
            scenario_errors.extend(semantic_errors(value, relative))
        if expect_valid:
            valid_count += 1
            errors.extend(scenario_errors)
        else:
            invalid_count += 1
            if not scenario_errors:
                errors.append(f"{relative}: invalid fixture unexpectedly passed runtime-adapter checks.")

    if errors:
        print("Runtime adapter permission harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Runtime adapter permission harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
