#!/usr/bin/env python3
"""Validate synthetic tribunal-review fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "tribunal_review" / "fixtures"
SCHEMA = ROOT / "schemas" / "tribunal_review_record.schema.json"
HIGH_RISK = {"high", "critical"}
ACTION_VERDICTS = {"revise", "reject", "escalate", "blocked"}


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


def substantive_dissent(record: dict[str, Any]) -> bool:
    dissent = record.get("dissent", [])
    if not isinstance(dissent, list):
        return False
    text = as_text(dissent).lower()
    return bool(text.strip()) and "no dissent" not in text


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    risk = str(record.get("risk_class", ""))
    verdict = str(record.get("verdict", ""))
    review_state = str(record.get("review_state", ""))
    guard_text = str(record.get("unchanged_evidence_guard", "")).lower()
    non_claim_text = as_text(record.get("non_claims", [])).lower()

    if risk in HIGH_RISK:
        if len(record.get("reviewer_roles", [])) < 3:
            errors.append(f"{relative}: high-risk tribunal reviews require at least three reviewer_roles.")
        if not nonempty_list(record, "adversarial_probes"):
            errors.append(f"{relative}: high-risk tribunal reviews require adversarial_probes.")
        if not nonempty_list(record, "dossier_refs"):
            errors.append(f"{relative}: high-risk tribunal reviews require dossier_refs.")

    if verdict == "accept":
        if not nonempty_list(record, "evidence_refs"):
            errors.append(f"{relative}: accept verdict requires evidence_refs.")
        if not nonempty_list(record, "findings"):
            errors.append(f"{relative}: accept verdict requires findings.")
        if review_state not in {"verdict_issued", "actions_recorded"}:
            errors.append(f"{relative}: accept verdict requires verdict_issued or actions_recorded review_state.")

    if verdict in ACTION_VERDICTS:
        if not nonempty_list(record, "required_actions"):
            errors.append(f"{relative}: {verdict} verdict requires required_actions.")
        if not nonempty_list(record, "constraint_effects"):
            errors.append(f"{relative}: {verdict} verdict requires constraint_effects.")

    if substantive_dissent(record):
        if not nonempty_list(record, "unresolved_issues"):
            errors.append(f"{relative}: substantive dissent requires unresolved_issues.")
        if "dissent" not in as_text(record.get("constraint_effects", [])).lower() and verdict == "accept":
            errors.append(f"{relative}: accept verdict with dissent must preserve dissent in constraint_effects.")

    if nonempty_list(record, "prior_review_refs"):
        if not any(term in guard_text for term in ("new evidence", "corrected mapping", "cannot promote", "block")):
            errors.append(f"{relative}: prior_review_refs require an unchanged_evidence_guard that blocks laundering or requires new evidence/corrected mapping.")

    if verdict == "accept" and nonempty_list(record, "unresolved_issues"):
        if "scope" not in as_text(record.get("constraint_effects", [])).lower():
            errors.append(f"{relative}: accept verdict with unresolved_issues must constrain scope.")

    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must contain explicit does-not boundaries.")
    for term in ("reviewer independence", "verdict correctness", "runtime", "support"):
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
        raise SystemExit(f"No tribunal-review fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Tribunal review harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Tribunal review harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
