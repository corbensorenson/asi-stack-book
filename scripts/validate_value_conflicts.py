#!/usr/bin/env python3
"""Validate synthetic value-conflict fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "value_conflicts" / "fixtures"
SCHEMA = ROOT / "schemas" / "value_conflict_record.schema.json"
HIGH_STAKES_TERMS = {"high", "irreversible", "safety", "rights", "public", "self-modification"}
REVIEW_TERMS = {"review", "tribunal", "human", "appeal"}
NARROWING_TERMS = {"narrow", "block", "defer", "deny", "escalate", "limit", "until", "reversible"}


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


def is_high_stakes(record: dict[str, Any]) -> bool:
    text = f"{record.get('stakes', '')} {record.get('reversibility', '')} {as_text(record.get('value_axes', []))}".lower()
    return any(term in text for term in HIGH_STAKES_TERMS)


def requires_residual(record: dict[str, Any]) -> bool:
    return str(record.get("decision_state", "")) in {
        "unresolved",
        "bounded_decision",
        "escalated_review",
        "deferred_action",
        "denied_action",
    }


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    decision_state = str(record.get("decision_state", ""))
    review_route = str(record.get("review_route", "")).lower()
    authority_effect = str(record.get("authority_effect", "")).lower()
    revisit = str(record.get("expiry_or_revisit_condition", "")).lower()

    if len(record.get("value_axes", [])) < 2:
        errors.append(f"{relative}: value conflict classification requires at least two value_axes.")
    if not nonempty_list(record, "stakeholders"):
        errors.append(f"{relative}: value conflict classification requires stakeholders.")
    if not nonempty_list(record, "evidence_required"):
        errors.append(f"{relative}: value conflict classification requires evidence_required.")

    if is_high_stakes(record):
        if not any(term in review_route for term in REVIEW_TERMS):
            errors.append(f"{relative}: high-stakes or irreversible conflicts require a review_route.")
        if decision_state == "bounded_decision" and "review" not in review_route and "tribunal" not in review_route:
            errors.append(f"{relative}: high-stakes bounded decisions require review-backed bounds.")

    if requires_residual(record) and not nonempty_list(record, "residual_uncertainty"):
        errors.append(f"{relative}: unresolved or bounded decisions must preserve residual_uncertainty.")

    if decision_state in {"bounded_decision", "deferred_action", "denied_action", "escalated_review"}:
        if not any(term in authority_effect for term in NARROWING_TERMS):
            errors.append(f"{relative}: bounded/deferred/escalated decisions must narrow, block, deny, defer, limit, or escalate authority.")

    if decision_state == "bounded_decision":
        if "never" in revisit or "none" == revisit.strip():
            errors.append(f"{relative}: bounded decisions require a real expiry_or_revisit_condition.")
        if not nonempty_list(record, "dissent_payload"):
            errors.append(f"{relative}: bounded decisions must preserve dissent_payload, even if dissent is scoped.")

    if decision_state == "deprecated_premise":
        if "deprecated" not in authority_effect and "block" not in authority_effect:
            errors.append(f"{relative}: deprecated premises must block or mark authority_effect as deprecated.")

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
        raise SystemExit(f"No value-conflict fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Value conflict harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Value conflict harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
