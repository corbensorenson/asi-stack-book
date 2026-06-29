#!/usr/bin/env python3
"""Validate synthetic governance-right fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "governance_rights" / "fixtures"
SCHEMA = ROOT / "schemas" / "governance_right_record.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {as_text(child)}" for key, child in value.items())
    return str(value)


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    right_type = str(record.get("right_type", ""))
    request_state = str(record.get("request_state", ""))
    denial_reason = str(record.get("denial_or_redaction_reason", "")).strip()
    appeal_path = str(record.get("appeal_path", "")).lower()
    access_path = str(record.get("access_path", "")).lower()
    independence = str(record.get("challenged_party_independence", "")).lower()
    preservation = f"{record.get('preservation_rule', '')} {record.get('preservation_obligation', '')}".lower()
    revisit = str(record.get("expiry_or_revisit", "")).lower()
    non_claim_text = as_text(record.get("non_claims", [])).lower()

    if right_type == "audit":
        if request_state in {"granted", "partially_granted", "redacted", "preserved"}:
            if not nonempty_list(record, "material_available"):
                errors.append(f"{relative}: audit rights require material_available when access is not denied.")
            if not nonempty_list(record, "receipt_refs"):
                errors.append(f"{relative}: audit rights require receipt_refs.")

    if right_type in {"exit", "fork"}:
        if not any(term in access_path for term in ("export", "repository", "snapshot", "portable", "bundle")):
            errors.append(f"{relative}: exit/fork rights require a usable access_path.")
        if "preserve" not in preservation and "retain" not in preservation:
            errors.append(f"{relative}: exit/fork rights require preservation_rule or preservation_obligation.")
        if "never" in revisit or revisit.strip() == "none":
            errors.append(f"{relative}: exit/fork rights require expiry_or_revisit.")

    if right_type == "fork" and request_state in {"granted", "partially_granted", "preserved"}:
        if not nonempty_list(record, "safety_constraints"):
            errors.append(f"{relative}: fork rights require safety_constraints.")
        if not nonempty_list(record, "material_available"):
            errors.append(f"{relative}: fork rights require material_available.")

    if request_state in {"denied", "redacted", "partially_granted"}:
        if not denial_reason:
            errors.append(f"{relative}: denied/redacted/partially_granted rights require denial_or_redaction_reason.")
        if not any(term in appeal_path for term in ("appeal", "review", "issue", "tribunal", "human")):
            errors.append(f"{relative}: denied/redacted/partially_granted rights require a usable appeal_path.")

    if "same party" in independence or "challenged runtime only" in independence:
        errors.append(f"{relative}: challenged_party_independence cannot depend only on the challenged party.")
    if not any(term in independence for term in ("independent", "git", "log", "repository", "review", "workflow")):
        errors.append(f"{relative}: challenged_party_independence must name an independent or durable record path.")

    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must contain explicit does-not boundaries.")
    for term in ("institutional", "runtime", "legal", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must mention {term}.")

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
        raise SystemExit(f"No governance-right fixtures found in {rel(FIXTURE_DIR)}.")

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

        fixture_errors = validate_value(value, schema, relative) + semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Governance rights harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Governance rights harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
