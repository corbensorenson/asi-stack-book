#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "support_state_transitions" / "fixtures"
SCHEMA = ROOT / "schemas" / "evidence_transition_record.schema.json"

SUPPORT_RANK = {
    "unsupported": 0,
    "argument": 1,
    "source-derived": 2,
    "external-literature-backed": 2,
    "prototype-backed": 3,
    "synthetic-test-backed": 4,
    "empirical-test-backed": 5,
}
TERMINAL_STATES = {"deprecated", "refuted"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_effect(old_state: str, new_state: str) -> str | None:
    if new_state in TERMINAL_STATES:
        return new_state
    if old_state == new_state:
        return "no_change"
    if old_state in SUPPORT_RANK and new_state in SUPPORT_RANK:
        if SUPPORT_RANK[new_state] > SUPPORT_RANK[old_state]:
            return "upward"
        if SUPPORT_RANK[new_state] < SUPPORT_RANK[old_state]:
            return "downward"
    return None


def require_nonempty(record: dict[str, Any], field: str, errors: list[str], relative: str) -> None:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be non-empty for this transition.")


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    old_state = str(record.get("old_support_state", ""))
    new_state = str(record.get("new_support_state", ""))
    transition_effect = str(record.get("transition_effect", ""))
    expected = expected_effect(old_state, new_state)
    if expected is None:
        errors.append(f"{relative}: unsupported support-state movement {old_state!r} -> {new_state!r}.")
    elif transition_effect != expected:
        errors.append(
            f"{relative}: transition_effect is {transition_effect!r}; expected {expected!r} "
            f"for {old_state!r} -> {new_state!r}."
        )

    if transition_effect == "no_change":
        if old_state != new_state:
            errors.append(f"{relative}: no_change transition must keep old_support_state and new_support_state equal.")
        if record.get("support_state_effect") not in {"argument_only", "blocks_promotion", "record_shape_only", "none"}:
            errors.append(f"{relative}: no_change transition must not be eligible for bounded evidence review.")

    if transition_effect == "upward":
        if old_state == new_state:
            errors.append(f"{relative}: upward transition must change the support state.")
        if record.get("review_status") != "accepted":
            errors.append(f"{relative}: upward transition requires review_status == accepted.")
        if record.get("transition_validity_state") != "review_accepted":
            errors.append(f"{relative}: upward transition requires transition_validity_state == review_accepted.")
        if record.get("verification_result") != "pass":
            errors.append(f"{relative}: upward transition requires verification_result == pass.")
        if record.get("support_state_effect") != "eligible_for_bounded_evidence_review":
            errors.append(
                f"{relative}: upward transition requires support_state_effect == "
                "eligible_for_bounded_evidence_review."
            )
        if record.get("acceptance_blockers"):
            errors.append(f"{relative}: upward transition cannot have acceptance_blockers.")
        for field in ("artifact_refs", "evidence_packet_refs", "source_mapping_refs", "reviewer_refs"):
            require_nonempty(record, field, errors, relative)

    if transition_effect == "downward":
        if old_state == new_state:
            errors.append(f"{relative}: downward transition must change the support state.")
        if record.get("review_status") != "accepted":
            errors.append(f"{relative}: downward transition requires review_status == accepted.")
        if record.get("support_state_effect") != "blocks_promotion":
            errors.append(f"{relative}: downward transition requires support_state_effect == blocks_promotion.")
        for field in ("negative_evidence_refs", "downgrade_triggers", "reviewer_refs"):
            require_nonempty(record, field, errors, relative)

    if transition_effect in {"deprecated", "refuted"}:
        if record.get("review_status") != "accepted":
            errors.append(f"{relative}: terminal transition requires accepted review.")
        if record.get("support_state_effect") != "blocks_promotion":
            errors.append(f"{relative}: terminal transition requires support_state_effect == blocks_promotion.")
        for field in ("negative_evidence_refs", "reviewer_refs"):
            require_nonempty(record, field, errors, relative)

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
        raise SystemExit(f"No support-state transition fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
                errors.append(f"{relative}: invalid fixture unexpectedly passed semantic transition checks.")

    if errors:
        print("Support-state transition harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Support-state transition harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
