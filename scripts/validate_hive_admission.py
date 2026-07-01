#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "hive_admission" / "fixtures"

SCHEMAS = {
    "device_resource_card": ROOT / "schemas" / "device_resource_card.schema.json",
    "portal_card": ROOT / "schemas" / "portal_card.schema.json",
    "hive_approval_receipt": ROOT / "schemas" / "hive_approval_receipt.schema.json",
    "hive_job_bid": ROOT / "schemas" / "hive_job_bid.schema.json",
    "hive_job_contract": ROOT / "schemas" / "hive_job_contract.schema.json",
    "hive_scheduling_decision": ROOT / "schemas" / "hive_scheduling_decision.schema.json",
    "hive_federation_lease": ROOT / "schemas" / "hive_federation_lease.schema.json",
}

PRIVATE_DATA_TERMS = {"private", "family", "guardian", "secret", "credential"}
FEDERATED_SCOPES = {"project", "rented", "public"}
APPROVAL_REQUIRED_RISK = {"medium", "high", "prohibited"}
BAD_APPROVAL_TERMS = {"expired", "revoked", "stale", "reused", "superseded"}
BAD_NETWORK_TERMS = {"all network", "ambient", "home lan", "private network", "unbounded"}
BAD_SUPPORT_OVERCLAIMS = {
    "chapter core promoted",
    "promotes support state",
    "proves deployed hive",
    "proves family governance",
    "proves privacy",
    "proves scheduler",
    "support-state promoted",
    "synthetic-test-backed chapter core",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemas() -> dict[str, Any]:
    return {name: load_json(path) for name, path in SCHEMAS.items()}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def text_blob(*values: Any) -> str:
    pieces: list[str] = []
    for value in values:
        if isinstance(value, dict):
            pieces.extend(f"{key}: {text_blob(child)}" for key, child in value.items())
        elif isinstance(value, list):
            pieces.extend(text_blob(item) for item in value)
        else:
            pieces.append(str(value))
    return " ".join(pieces).lower()


def require_list(record: dict[str, Any], field: str, errors: list[str], relative: str, *, nonempty: bool = False) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or (nonempty and not value):
        kind = "a non-empty list" if nonempty else "a list"
        errors.append(f"{relative}: {field} must be {kind}.")
        return []
    return value


def require_object(record: dict[str, Any], field: str, errors: list[str], relative: str) -> dict[str, Any]:
    value = record.get(field)
    if not isinstance(value, dict):
        errors.append(f"{relative}: {field} must be an object.")
        return {}
    return value


def require_non_claim_boundary(items: Any, errors: list[str], relative: str) -> None:
    if not isinstance(items, list) or not items:
        errors.append(f"{relative}: non_claims must be a non-empty list.")
        return
    blob = text_blob(items)
    if "does not" not in blob:
        errors.append(f"{relative}: non_claims must include explicit does-not boundaries.")
    if "support" not in blob or "promot" not in blob:
        errors.append(f"{relative}: non_claims must deny support-state promotion.")
    if not any(term in blob for term in ("deployed", "runtime", "scheduler", "hive")):
        errors.append(f"{relative}: non_claims must deny deployed/runtime hive behavior.")


def schema_errors(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for index, record in enumerate(value.get("device_resource_cards", [])):
        errors.extend(validate_value(record, schemas["device_resource_card"], f"{relative}:device_resource_cards[{index}]"))
    for index, record in enumerate(value.get("job_bids", [])):
        errors.extend(validate_value(record, schemas["hive_job_bid"], f"{relative}:job_bids[{index}]"))
    for index, record in enumerate(value.get("approval_receipts", [])):
        errors.extend(validate_value(record, schemas["hive_approval_receipt"], f"{relative}:approval_receipts[{index}]"))
    for index, record in enumerate(value.get("federation_leases", [])):
        errors.extend(validate_value(record, schemas["hive_federation_lease"], f"{relative}:federation_leases[{index}]"))
    for field, schema_name in (
        ("portal_card", "portal_card"),
        ("job_contract", "hive_job_contract"),
        ("scheduling_decision", "hive_scheduling_decision"),
    ):
        record = value.get(field)
        if not isinstance(record, dict):
            errors.append(f"{relative}: {field} must be an object.")
            continue
        errors.extend(validate_value(record, schemas[schema_name], f"{relative}:{field}"))
    return errors


def id_map(records: list[Any], key: str) -> dict[str, dict[str, Any]]:
    return {
        str(record.get(key)): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get(key), str)
    }


def data_is_private(data_classes: list[Any]) -> bool:
    return any(any(term in str(item).lower() for term in PRIVATE_DATA_TERMS) for item in data_classes)


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    devices = require_list(value, "device_resource_cards", errors, relative, nonempty=True)
    bids = require_list(value, "job_bids", errors, relative, nonempty=True)
    approvals = require_list(value, "approval_receipts", errors, relative)
    leases = require_list(value, "federation_leases", errors, relative)
    job = require_object(value, "job_contract", errors, relative)
    decision = require_object(value, "scheduling_decision", errors, relative)
    portal = require_object(value, "portal_card", errors, relative)
    require_non_claim_boundary(value.get("non_claims"), errors, f"{relative}:non_claims")
    if errors:
        return errors

    for name, record in (
        ("job_contract", job),
        ("scheduling_decision", decision),
        ("portal_card", portal),
    ):
        require_non_claim_boundary(record.get("non_claims"), errors, f"{relative}:{name}.non_claims")
    for index, record in enumerate(bids):
        require_non_claim_boundary(record.get("non_claims"), errors, f"{relative}:job_bids[{index}].non_claims")
    for index, record in enumerate(approvals):
        require_non_claim_boundary(record.get("non_claims"), errors, f"{relative}:approval_receipts[{index}].non_claims")
    for index, record in enumerate(leases):
        require_non_claim_boundary(record.get("non_claims"), errors, f"{relative}:federation_leases[{index}].non_claims")

    if any(term in text_blob(value) for term in BAD_SUPPORT_OVERCLAIMS):
        errors.append(f"{relative}: synthetic hive fixtures cannot claim deployed behavior or support-state promotion.")

    devices_by_id = id_map(devices, "device_id")
    bids_by_device = id_map(bids, "bidder_device_id")
    approvals_by_id = id_map(approvals, "approval_id")
    job_id = str(job.get("job_id", ""))
    selected = str(decision.get("selected_node_id", ""))
    eligible_nodes = {str(item) for item in decision.get("eligible_nodes", [])}
    rejected_nodes = {
        str(item.get("node_id"))
        for item in decision.get("rejected_nodes", [])
        if isinstance(item, dict)
    }

    if decision.get("job_id") != job_id:
        errors.append(f"{relative}: scheduling_decision.job_id must match job_contract.job_id.")
    if selected not in devices_by_id:
        errors.append(f"{relative}: selected_node_id must have a DeviceResourceCard.")
    if selected not in bids_by_device:
        errors.append(f"{relative}: selected_node_id must have a HiveJobBid.")
    if selected not in eligible_nodes:
        errors.append(f"{relative}: selected_node_id must be listed in eligible_nodes.")
    if selected in rejected_nodes:
        errors.append(f"{relative}: selected_node_id cannot also be listed in rejected_nodes.")
    for bid in bids:
        if bid.get("job_id") != job_id:
            errors.append(f"{relative}: every HiveJobBid.job_id must match the job contract.")

    selected_device = devices_by_id.get(selected, {})
    selected_bid = bids_by_device.get(selected, {})
    if selected_device:
        if selected_device.get("enrollment_status") != "active":
            errors.append(f"{relative}: selected device must be actively enrolled.")
        missing_data = sorted(set(job.get("data_classes", [])) - set(selected_device.get("allowed_data_classes", [])))
        missing_tools = sorted(set(job.get("tool_classes", [])) - set(selected_device.get("allowed_tool_classes", [])))
        if missing_data:
            errors.append(f"{relative}: selected device lacks allowed data class(es): {missing_data}.")
        if missing_tools:
            errors.append(f"{relative}: selected device lacks allowed tool class(es): {missing_tools}.")
    if selected_bid:
        if selected_bid.get("bid_status") != "eligible":
            errors.append(f"{relative}: selected bid must be eligible after policy filtering.")
        if selected_bid.get("privacy_fit") in {"blocked", "low"}:
            errors.append(f"{relative}: selected bid cannot have blocked or low privacy fit.")
        if selected_bid.get("capability_fit") in {"blocked", "low"}:
            errors.append(f"{relative}: selected bid cannot have blocked or low capability fit.")
        if selected_bid.get("thermal_risk") == "high":
            errors.append(f"{relative}: selected bid with high thermal risk must not be admitted by this harness.")
        if "over budget" in text_blob(selected_bid.get("estimated_energy"), decision.get("estimated_energy")):
            errors.append(f"{relative}: selected bid cannot exceed the recorded energy budget.")
        if selected_bid.get("interruption_risk") == "high" and not any(
            term in text_blob(decision.get("residuals")) for term in ("dropout", "requeue", "recover")
        ):
            errors.append(f"{relative}: high interruption risk requires an explicit dropout/requeue residual.")

    for bid in bids:
        device_id = str(bid.get("bidder_device_id", ""))
        if bid.get("bid_status") == "policy_blocked":
            if device_id == selected:
                errors.append(f"{relative}: policy-blocked bid cannot be selected.")
            if device_id not in rejected_nodes:
                errors.append(f"{relative}: policy-blocked bid {device_id} must appear in rejected_nodes.")

    federation_scope = str(job.get("federation_scope", ""))
    selected_is_rented = selected_device.get("trust_tier") == "rented_public" or selected_device.get("locality_class") == "rented_region"
    private_data = data_is_private(job.get("data_classes", []))
    if selected_is_rented and private_data:
        errors.append(f"{relative}: private, family, guardian, secret, or credential data cannot be selected for a rented/public node.")
    federation_required = selected_is_rented or federation_scope in FEDERATED_SCOPES
    if federation_required:
        if not leases:
            errors.append(f"{relative}: federated or rented scheduling requires a HiveFederationLease.")
        for lease in leases:
            if lease.get("job_contract_ref") != job_id:
                errors.append(f"{relative}: federation lease must reference the scheduled job contract.")
            if not set(job.get("data_classes", [])).issubset(set(lease.get("allowed_data_classes", []))):
                errors.append(f"{relative}: federation lease must bound every job data class.")
            if not set(job.get("tool_classes", [])).issubset(set(lease.get("allowed_tool_classes", []))):
                errors.append(f"{relative}: federation lease must bound every job tool class.")
            if any(term in text_blob(lease.get("network_scope")) for term in BAD_NETWORK_TERMS):
                errors.append(f"{relative}: federation lease network_scope must not grant ambient or private-network access.")
            if text_blob(lease.get("sandbox_manifest_ref")) in {"", "none", "sandbox none"}:
                errors.append(f"{relative}: federation lease requires a sandbox manifest reference.")
            evidence_text = text_blob(lease.get("evidence_obligations"))
            if "artifact" not in evidence_text or "validator" not in evidence_text:
                errors.append(f"{relative}: federation lease evidence_obligations must include artifact and validator evidence.")

    approval_required = str(job.get("physical_risk_tier", "")) in APPROVAL_REQUIRED_RISK or bool(job.get("required_approvals"))
    approval_refs = [str(item) for item in decision.get("approval_receipt_refs", [])]
    if approval_required and not approval_refs:
        errors.append(f"{relative}: approval-required hive jobs need approval_receipt_refs.")
    for approval_ref in approval_refs:
        receipt = approvals_by_id.get(approval_ref)
        if receipt is None:
            errors.append(f"{relative}: approval receipt ref {approval_ref!r} has no matching HiveApprovalReceipt.")
            continue
        if receipt.get("job_id") != job_id:
            errors.append(f"{relative}: HiveApprovalReceipt.job_id must match the scheduled job.")
        if any(term in text_blob(receipt.get("valid_until"), receipt.get("approval_scope")) for term in BAD_APPROVAL_TERMS):
            errors.append(f"{relative}: approval receipt must not be expired, revoked, stale, reused, or superseded.")

    family_or_child = any(term in text_blob(job.get("objective"), job.get("data_classes"), portal) for term in ("child", "guardian", "family_sensitive"))
    if family_or_child:
        if portal.get("authority_level") not in {"guardian_surface", "admin_surface"}:
            errors.append(f"{relative}: child/family-sensitive work must route through a guardian or admin portal surface.")
        if not approval_refs:
            errors.append(f"{relative}: child/family-sensitive work requires a bound approval receipt.")

    evidence_text = text_blob(decision.get("evidence_refs"), decision.get("residuals"))
    if "scripts/validate_hive_admission.py" not in evidence_text:
        errors.append(f"{relative}: scheduling evidence_refs must include scripts/validate_hive_admission.py.")
    if "docs/hive_admission_harness.md" not in evidence_text:
        errors.append(f"{relative}: scheduling evidence_refs must include docs/hive_admission_harness.md.")
    if "audit" not in evidence_text:
        errors.append(f"{relative}: scheduling evidence/residuals must preserve audit replay context.")

    return errors


def main() -> None:
    schemas = load_schemas()
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No hive admission fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = rel(fixture)
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

        fixture_errors = schema_errors(value, schemas, relative) + semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Hive admission harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Hive admission harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
