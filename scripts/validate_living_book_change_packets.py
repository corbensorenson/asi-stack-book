#!/usr/bin/env python3
"""Validate synthetic living-book change-packet records.

The harness checks record discipline only. It does not approve releases,
manuscript quality, source interpretation, reader artifacts, or support-state
movement.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "living_book_change_packet.schema.json"
FIXTURE_DIR = ROOT / "experiments" / "living_book_change_packets" / "fixtures"

PUBLIC_SURFACE_PACKET_TYPES = {
    "chapter_revision",
    "outline_only",
    "proof_manifest_shift",
    "reader_edition_generation",
    "source_ingestion",
    "schema_fixture_update",
    "evidence_transition_review",
}
DERIVED_RELEASE_TARGETS = {"reader_source", "reader_format", "audio_script"}
CHANGELOG_PACKET_TYPES = {
    "chapter_revision",
    "outline_only",
    "proof_manifest_shift",
    "reader_edition_generation",
    "source_ingestion",
    "schema_fixture_update",
    "evidence_transition_review",
}
PROMOTION_EFFECTS = {"eligible_for_review", "upward_transition"}
BOUNDARY_REQUIRED_TERMS = {"not equal authority", "derived", "projection", "not approved", "not release"}
NON_CLAIM_TERMS = {"no support-state promotion", "does not promote", "not support-state promotion"}
RENDER_COMMAND_TERMS = {"quarto render", "validate_live_human_view"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate_value(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not type_ok(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']!r}")

    if expected_type == "string" and schema.get("minLength", 0) > len(value):
        errors.append(f"{path}: string shorter than minLength {schema['minLength']}")

    if expected_type == "array":
        item_schema = schema.get("items", {})
        for index, item in enumerate(value):
            errors.extend(validate_value(item, item_schema, f"{path}[{index}]"))

    if expected_type == "object":
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected key {key!r}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_value(value[key], child_schema, f"{path}.{key}"))

    return errors


def has_any(text: str, needles: set[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def joined(values: list[str]) -> str:
    return " ".join(str(value) for value in values)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []

    packet_id = str(record.get("packet_id", ""))
    packet_type = str(record.get("packet_type", ""))
    release_target = str(record.get("release_target", ""))
    validation_status = str(record.get("validation_status", ""))
    render_result = str(record.get("render_result", ""))
    support_state_effect = str(record.get("support_state_effect", ""))
    boundary = str(record.get("derived_artifact_boundary", ""))
    commands = record.get("validation_commands", [])
    changelog_refs = record.get("changelog_refs", [])
    evidence_refs = record.get("evidence_transition_refs", [])
    residuals = record.get("residuals", [])
    non_claims = record.get("non_claims", [])

    commands_text = joined(commands).lower() if isinstance(commands, list) else ""
    non_claims_text = joined(non_claims).lower() if isinstance(non_claims, list) else ""
    residuals_text = joined(residuals).lower() if isinstance(residuals, list) else ""

    if not packet_id.startswith("change-packet://"):
        errors.append(f"{relative}: packet_id must use change-packet:// identity.")

    if packet_type in PUBLIC_SURFACE_PACKET_TYPES and not changelog_refs:
        errors.append(f"{relative}: public-surface change packets must name changelog_refs.")

    if validation_status == "pass" and not commands:
        errors.append(f"{relative}: passing change packets must record validation_commands.")

    if render_result == "pass" and not has_any(commands_text, RENDER_COMMAND_TERMS):
        errors.append(f"{relative}: render_result pass requires a render or live-view validation command.")

    if release_target in DERIVED_RELEASE_TARGETS:
        if not has_any(boundary, BOUNDARY_REQUIRED_TERMS):
            errors.append(f"{relative}: derived reader/audio targets must state a non-equal-authority or non-approval boundary.")
        if "equal authority" in boundary.lower() and "not equal authority" not in boundary.lower():
            errors.append(f"{relative}: reader/audio derivatives cannot be equal authority to the live book.")

    if support_state_effect in PROMOTION_EFFECTS and not evidence_refs:
        errors.append(f"{relative}: promotion-eligible effects require evidence_transition_refs.")

    if support_state_effect == "upward_transition" and "accepted evidence transition" not in joined(evidence_refs).lower():
        errors.append(f"{relative}: upward transitions require an accepted evidence transition reference.")

    if not non_claims:
        errors.append(f"{relative}: change packets must preserve explicit non_claims.")
    elif not has_any(non_claims_text, NON_CLAIM_TERMS) and support_state_effect != "blocks_promotion":
        errors.append(f"{relative}: non_claims must state the support-state promotion boundary.")

    if validation_status in {"fail", "blocked", "partial", "pending"} and not residuals:
        errors.append(f"{relative}: incomplete or blocked change packets must name residuals.")

    if validation_status == "blocked" and "blocked" not in residuals_text:
        errors.append(f"{relative}: blocked change packets must name the blocked condition in residuals.")

    return errors


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    errors: list[str] = []
    valid_count = 0
    invalid_count = 0

    fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixture_paths:
        raise SystemExit("No living-book change-packet fixtures found.")

    for path in fixture_paths:
        relative = str(path.relative_to(ROOT))
        record = load_json(path)
        record_errors = validate_value(record, schema, relative)
        if not record_errors:
            record_errors.extend(semantic_errors(record, relative))

        expect_invalid = path.name.startswith("invalid_")
        if expect_invalid:
            invalid_count += 1
            if not record_errors:
                errors.append(f"{relative}: expected-invalid fixture unexpectedly passed.")
        else:
            valid_count += 1
            errors.extend(record_errors)

    if valid_count != 3:
        errors.append(f"Expected exactly 3 valid fixtures, found {valid_count}.")
    if invalid_count != 6:
        errors.append(f"Expected exactly 6 expected-invalid fixtures, found {invalid_count}.")

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(
        "Living-book change-packet harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
