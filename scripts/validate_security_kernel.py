#!/usr/bin/env python3
"""Validate synthetic security-kernel authority-use receipt fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "security_kernel" / "fixtures"
SCHEMA = ROOT / "schemas" / "authority_use_receipt.schema.json"

REQUIRED_LIFECYCLE = {"spawn", "inject", "execute", "sanitize", "zeroize", "commit", "audit"}
SCOPING_BAD_TERMS = {
    "all destinations",
    "all tools",
    "ambient",
    "any action",
    "any destination",
    "do anything",
    "unbounded",
}
SECRET_LEAK_TERMS = {
    "api_key=",
    "credential bytes:",
    "handle://vault/",
    "password=",
    "raw_secret",
    "secret_value",
    "sk-live",
}
SANITIZED_TERMS = {"no secret", "redacted", "sanitized", "status only", "summary only"}
REVOCATION_TERMS = {"delete", "expire", "lease", "revoke", "zeroize"}


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


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    handle_id = str(record.get("handle_id", "")).lower()
    purpose = str(record.get("purpose", "")).lower()
    destination = str(record.get("destination", "")).lower()
    allowed_action = str(record.get("allowed_action", "")).lower()
    clearance = str(record.get("clearance", "")).lower()
    approval = str(record.get("approval_record", "")).lower()
    lifecycle = record.get("scif_lifecycle", [])
    sanitized_output = str(record.get("sanitized_output", "")).lower()
    residual_text = as_text(record.get("residual_leak_risk", [])).lower()
    revocation = str(record.get("revocation_path", "")).lower()
    scoped_text = f"{purpose} {destination} {allowed_action}"

    if not handle_id.startswith("handle://"):
        errors.append(f"{relative}: handle_id must be a handle URI, not model-visible secret material.")

    if any(term in scoped_text for term in SCOPING_BAD_TERMS):
        errors.append(f"{relative}: purpose, destination, and allowed_action must not create ambient authority.")

    if not any(term in allowed_action for term in ("execute", "query", "sign", "substitute")):
        errors.append(f"{relative}: allowed_action must name a bounded executable action.")

    if clearance in {"", "none", "public", "unrestricted"}:
        errors.append(f"{relative}: clearance must preserve a protected or SCIF-scoped boundary.")

    if approval in {"", "none", "missing", "pending"} or not approval.startswith("approval://"):
        errors.append(f"{relative}: approval_record must reference a concrete approval artifact.")

    if not isinstance(lifecycle, list):
        errors.append(f"{relative}: scif_lifecycle must be an array.")
    else:
        missing = sorted(REQUIRED_LIFECYCLE - set(lifecycle))
        if missing:
            errors.append(f"{relative}: scif_lifecycle missing required event(s): {', '.join(missing)}.")

    if contains_any(sanitized_output, SECRET_LEAK_TERMS):
        errors.append(f"{relative}: sanitized_output must not expose secret bytes, live handles, or credentials.")
    if not contains_any(sanitized_output, SANITIZED_TERMS):
        errors.append(f"{relative}: sanitized_output must explicitly mark redaction or sanitization.")

    if "prompt" in scoped_text or "injection" in scoped_text:
        if not any(term in sanitized_output for term in ("blocked", "refusal", "redacted", "sanitized")):
            errors.append(f"{relative}: prompt-injection probes must return a blocked, refused, redacted, or sanitized result.")

    if not isinstance(record.get("residual_leak_risk"), list) or not record["residual_leak_risk"]:
        errors.append(f"{relative}: residual_leak_risk must preserve at least one residual or non-claim boundary.")
    if "does not" not in residual_text:
        errors.append(f"{relative}: residual_leak_risk must include explicit does-not boundaries.")
    for term in ("runtime", "support"):
        if term not in residual_text:
            errors.append(f"{relative}: residual_leak_risk must mention {term}.")

    if not contains_any(revocation, REVOCATION_TERMS):
        errors.append(f"{relative}: revocation_path must name expiry, revocation, deletion, lease closure, or zeroization.")

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
        raise SystemExit(f"No security-kernel fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Security kernel harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Security kernel harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
