#!/usr/bin/env python3
"""Validate synthetic constitutional-predicate fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "constitutional_alignment" / "fixtures"
SCHEMA = ROOT / "schemas" / "constitutional_predicate_record.schema.json"

TEST_TERMS = {
    "block",
    "check",
    "deny",
    "reject",
    "require",
    "route",
    "satisfy",
    "test",
}
CONFLICT_TERMS = {"block", "defer", "deny", "narrow", "residual", "review", "route", "tribunal"}
REVIEW_TERMS = {"governance", "human", "review", "tribunal"}
SELF_MOD_TERMS = {"cannot", "deny", "governance", "reject", "review", "weaken", "without"}
MIGRATION_TERMS = {"diff", "migration", "record", "review", "rollback"}
POWER_TERMS = {"least sufficient power", "lower-power", "minimal", "power"}
BAD_POWER_TERMS = {"highest power", "maximum power", "unbounded power"}


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
    status = str(record.get("translation_status", ""))
    operational_test = str(record.get("operational_test", "")).lower()
    conflict = str(record.get("conflict_behavior", "")).lower()
    review = str(record.get("review_route", "")).lower()
    self_mod = str(record.get("self_modification_rule", "")).lower()
    migration = str(record.get("migration_policy", "")).lower()
    commitment = str(record.get("commitment", "")).lower()
    predicate_id = str(record.get("predicate_id", "")).lower()
    non_claim_text = as_text(record.get("non_claims", [])).lower()

    if not nonempty_list(record, "protected_scope"):
        errors.append(f"{relative}: protected_scope must be non-empty.")

    if status in {"operational", "partial"}:
        if not contains_any(operational_test, TEST_TERMS):
            errors.append(f"{relative}: operational or partial predicates require an executable-style operational_test.")
        if not contains_any(review, REVIEW_TERMS):
            errors.append(f"{relative}: operational or partial predicates require a usable review_route.")

    if status == "speculative_lineage":
        if "not authorize" not in operational_test and "not operational" not in operational_test:
            errors.append(f"{relative}: speculative_lineage predicates must say they do not authorize action.")
        if not nonempty_list(record, "uncertainty"):
            errors.append(f"{relative}: speculative_lineage predicates must preserve uncertainty.")

    if not contains_any(conflict, CONFLICT_TERMS):
        errors.append(f"{relative}: conflict_behavior must route, narrow, defer, block, deny, preserve residuals, or use review.")

    if not contains_any(self_mod, SELF_MOD_TERMS):
        errors.append(f"{relative}: self_modification_rule must block, reject, deny, or route weakening to governance review.")
    if "without review" in self_mod and not any(term in self_mod for term in ("cannot", "deny", "reject", "block")):
        errors.append(f"{relative}: self_modification_rule cannot allow weakening without review.")

    if not contains_any(migration, MIGRATION_TERMS):
        errors.append(f"{relative}: migration_policy must preserve migration diff, record, review, or rollback semantics.")
    if "ordinary refactor" in migration or "no record" in migration:
        errors.append(f"{relative}: migration_policy cannot treat protected predicate changes as ordinary unrecorded refactors.")

    if contains_any(f"{predicate_id} {commitment} {operational_test}", POWER_TERMS):
        if contains_any(operational_test, BAD_POWER_TERMS):
            errors.append(f"{relative}: power predicates cannot select maximum or unbounded power by default.")
        if not any(term in operational_test for term in ("least", "lower-power", "minimal", "reject", "block", "deny")):
            errors.append(f"{relative}: power predicates must prefer or enforce least-sufficient-power behavior.")

    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must contain explicit does-not boundaries.")
    for term in ("runtime", "source", "support"):
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
        raise SystemExit(f"No constitutional-alignment fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Constitutional alignment harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Constitutional alignment harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
