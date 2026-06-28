#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "authority_transitions" / "fixtures"
SCHEMA = ROOT / "schemas" / "authority_transition_record.schema.json"

AUTHORITY_RANK = {
    "public_read": 1,
    "public_transform": 2,
    "tracked_file_write": 3,
    "local_fixture_execute": 4,
    "external_effect": 5,
    "governance_approval": 6,
}

PERMISSION_MINIMUM = {
    "read": "public_read",
    "transform": "public_transform",
    "disclose": "external_effect",
    "write": "tracked_file_write",
    "execute": "local_fixture_execute",
    "approve": "governance_approval",
}

ALLOW_STATES = {"granted", "used", "receipted"}
ESCALATE_STATES = {"requested", "delegated"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rank(record: dict[str, Any], field: str, errors: list[str], relative: str) -> int:
    value = str(record.get(field, ""))
    if value not in AUTHORITY_RANK:
        errors.append(
            f"{relative}: {field} {value!r} is not one of {sorted(AUTHORITY_RANK)}."
        )
        return -1
    return AUTHORITY_RANK[value]


def has_audit(record: dict[str, Any]) -> bool:
    return isinstance(record.get("audit_refs"), list) and bool(record["audit_refs"])


def has_non_claims(record: dict[str, Any]) -> bool:
    return isinstance(record.get("non_claims"), list) and bool(record["non_claims"])


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    permission_class = str(record.get("permission_class", ""))
    grant_state = str(record.get("grant_lifecycle_state", ""))
    decision = str(record.get("decision", ""))
    effect_receipt = str(record.get("effect_receipt", ""))
    denial_reason = str(record.get("denial_reason", ""))
    delegation_chain = record.get("delegation_chain", [])

    if permission_class not in PERMISSION_MINIMUM:
        errors.append(f"{relative}: unsupported permission_class {permission_class!r}.")
        minimum_rank = -1
    else:
        minimum_rank = AUTHORITY_RANK[PERMISSION_MINIMUM[permission_class]]

    caller_rank = rank(record, "caller_ceiling", errors, relative)
    active_rank = rank(record, "authority_ceiling", errors, relative)
    target_rank = rank(record, "target_required_authority", errors, relative)

    if target_rank != -1 and minimum_rank != -1 and target_rank < minimum_rank:
        errors.append(
            f"{relative}: permission_class {permission_class!r} requires at least "
            f"{PERMISSION_MINIMUM[permission_class]!r}, but target_required_authority is "
            f"{record.get('target_required_authority')!r}."
        )

    if not has_audit(record):
        errors.append(f"{relative}: audit_refs must be non-empty.")
    if not has_non_claims(record):
        errors.append(f"{relative}: non_claims must be non-empty.")

    if decision == "allow":
        if grant_state not in ALLOW_STATES:
            errors.append(f"{relative}: allow requires grant_lifecycle_state in {sorted(ALLOW_STATES)}.")
        if target_rank > active_rank:
            errors.append(
                f"{relative}: allow cannot target {record.get('target_required_authority')!r} "
                f"above authority_ceiling {record.get('authority_ceiling')!r}."
            )
        if active_rank > caller_rank:
            errors.append(
                f"{relative}: allow cannot widen authority_ceiling {record.get('authority_ceiling')!r} "
                f"above caller_ceiling {record.get('caller_ceiling')!r}."
            )
        if not effect_receipt.startswith("receipt://"):
            errors.append(f"{relative}: allow requires an effect_receipt with a receipt:// id.")
        if denial_reason:
            errors.append(f"{relative}: allow must not carry a denial_reason.")
        if "expired" in str(record.get("expiry_or_review", "")).lower():
            errors.append(f"{relative}: allow cannot use an expired grant.")
        if "revoked" in str(record.get("revocation_epoch", "")).lower() and str(record.get("revocation_epoch")) != "not_revoked":
            errors.append(f"{relative}: allow cannot use a revoked grant.")

    elif decision == "deny":
        if grant_state != "denied":
            errors.append(f"{relative}: deny requires grant_lifecycle_state == denied.")
        if not denial_reason:
            errors.append(f"{relative}: deny requires a denial_reason.")
        if effect_receipt:
            errors.append(f"{relative}: deny must not carry an effect_receipt.")

    elif decision == "escalate":
        if grant_state not in ESCALATE_STATES:
            errors.append(f"{relative}: escalate requires grant_lifecycle_state in {sorted(ESCALATE_STATES)}.")
        if effect_receipt:
            errors.append(f"{relative}: escalate must not carry an effect_receipt.")
        if not denial_reason:
            errors.append(f"{relative}: escalate requires a reason for review.")
        chain_text = " ".join(str(item).lower() for item in delegation_chain if isinstance(item, str))
        if "review" not in chain_text and "approval" not in chain_text:
            errors.append(f"{relative}: escalate must route to review or approval in delegation_chain.")

    else:
        errors.append(f"{relative}: unsupported decision {decision!r}.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No authority transition fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
        schema_errors = validate_value(value, schema, relative)
        if schema_errors:
            errors.extend(schema_errors)
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: fixture must contain a JSON object.")
            continue

        semantic = semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(semantic)
        else:
            invalid_count += 1
            if not semantic:
                errors.append(f"{relative}: invalid fixture unexpectedly passed semantic authority checks.")

    if errors:
        print("Authority transition harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Authority transition harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
