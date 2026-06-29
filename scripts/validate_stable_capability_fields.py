#!/usr/bin/env python3
"""Validate synthetic stable-capability-field fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "stable_capability_fields" / "fixtures"
SCHEMA = ROOT / "schemas" / "stable_capability_field.schema.json"

AUTHORITY_BAD_TERMS = {
    "all authority",
    "all destinations",
    "all tools",
    "ambient",
    "any action",
    "any tool",
    "root",
    "unbounded",
    "unrestricted",
}
INDEPENDENCE_BAD_TERMS = {
    "candidate validates itself",
    "same implementation",
    "self-attested",
    "self-judged",
}
ROLLBACK_TERMS = {"fallback", "preserve", "retain", "restore", "rollback"}
SCOPE_TERMS = {"canary", "field", "qualified", "shadow"}


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


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    field_id = str(record.get("field_id", "")).lower()
    lifecycle_state = str(record.get("lifecycle_state", "")).lower()
    qualification_status = str(record.get("qualification_status", "")).lower()
    lease_status = str(record.get("qualification_lease_status", "")).lower()
    authority_ceiling = str(record.get("authority_ceiling", "")).lower()
    evaluator_policy = str(record.get("evaluator_policy", "")).lower()
    evaluator_independence = str(record.get("evaluator_independence", "")).lower()
    route_validity = str(record.get("route_validity", "")).lower()
    route_scope = str(record.get("route_scope", "")).lower()
    route_permission_effect = str(record.get("route_permission_effect", "")).lower()
    consumer_policy = str(record.get("consumer_policy", "")).lower()
    rollback_text = f"{record.get('rollback_plan', '')} {as_text(record.get('rollback_obligations', []))}".lower()
    blocker_text = as_text(record.get("default_route_blockers", [])).lower()
    non_claim_text = as_text(record.get("non_claims", [])).lower()

    if not field_id.startswith("field://"):
        errors.append(f"{relative}: field_id must be a field:// identifier.")

    if contains_any(authority_ceiling, AUTHORITY_BAD_TERMS):
        errors.append(f"{relative}: authority_ceiling must not grant ambient or unbounded authority.")

    if qualification_status in {"evidence_mapped", "qualified_for_scope"}:
        for key in ("qualification_predicates", "evidence_refs", "regression_suite"):
            if not nonempty_list(record, key):
                errors.append(f"{relative}: {qualification_status} fields require non-empty {key}.")

    if lifecycle_state in {"canary", "qualified", "default"}:
        if route_validity not in {"valid", "residual"}:
            errors.append(f"{relative}: routed lifecycle states require valid or residual route_validity.")
        if not nonempty_list(record, "readiness_gate_refs"):
            errors.append(f"{relative}: routed lifecycle states require readiness_gate_refs.")

    if route_permission_effect in {"canary_only", "qualified_for_scope", "default_allowed"}:
        if not contains_any(route_scope, SCOPE_TERMS):
            errors.append(f"{relative}: route_scope must name the canary, shadow, field, or qualification boundary.")
        if "default" not in consumer_policy and route_permission_effect == "default_allowed":
            errors.append(f"{relative}: default_allowed routes must name default consumer policy.")

    if route_permission_effect in {"canary_only", "shadow_only", "qualified_for_scope"}:
        if not nonempty_list(record, "default_route_blockers"):
            errors.append(f"{relative}: non-default route effects must preserve default_route_blockers.")

    if route_permission_effect == "default_allowed":
        if route_validity != "valid":
            errors.append(f"{relative}: default_allowed routes require valid route_validity.")
        if lease_status in {"fixture_only", "expired", "revoked", "blocked", "review_due"}:
            errors.append(f"{relative}: default_allowed routes require an active non-fixture lease.")
        if blocker_text.strip():
            errors.append(f"{relative}: default_allowed routes must not carry unresolved default blockers.")

    if contains_any(evaluator_policy, INDEPENDENCE_BAD_TERMS) or contains_any(evaluator_independence, INDEPENDENCE_BAD_TERMS):
        errors.append(f"{relative}: evaluator policy cannot rely on self-attestation by the candidate.")
    if not any(term in evaluator_independence for term in ("external", "independent", "separate", "review")):
        errors.append(f"{relative}: evaluator_independence must name a separate review boundary.")

    if not contains_any(rollback_text, ROLLBACK_TERMS):
        errors.append(f"{relative}: rollback_plan and rollback_obligations must preserve rollback or fallback duties.")
    if not nonempty_list(record, "rollback_obligations"):
        errors.append(f"{relative}: rollback_obligations must not be empty.")

    if not nonempty_list(record, "review_triggers"):
        errors.append(f"{relative}: review_triggers must not be empty.")

    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must include explicit does-not boundaries.")
    for term in ("runtime", "support"):
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
        raise SystemExit(f"No stable-capability-field fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Stable capability fields harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Stable capability fields harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
