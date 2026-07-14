#!/usr/bin/env python3
"""Validate JSON example fixtures against the local schema subset.

This intentionally supports only the JSON Schema features used in this repo's
draft protocol schemas, so it remains dependency-free in GitHub Actions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "protocol_records"
RELEASE_RECORD_DIR = ROOT / "release_records"


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
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value {value!r} does not equal const {schema['const']!r}")

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


def release_schema_for(value: Any) -> Path:
    if (
        isinstance(value, dict)
        and value.get("schema_version") == "asi_stack.post_v2_3_cycle_no_release.v0"
    ):
        return SCHEMA_DIR / "post_v2_3_cycle_no_release_record.schema.json"
    if (
        isinstance(value, dict)
        and value.get("schema_version")
        == "asi_stack.post_v2_3_handoff_reader_formats_evidence_renewal_terminal.v0"
    ):
        return SCHEMA_DIR / "post_v2_3_handoff_reader_formats_evidence_renewal_terminal_record.schema.json"
    if isinstance(value, dict) and value.get("record_type") == "edition_release":
        return SCHEMA_DIR / "edition_release_record.schema.json"
    return SCHEMA_DIR / "living_book_release_record.schema.json"


def main() -> None:
    errors: list[str] = []
    fixtures = sorted(FIXTURE_DIR.glob("*.valid.json"))
    if not fixtures:
        raise SystemExit("No protocol example fixtures found.")

    for fixture in fixtures:
        schema_name = fixture.name.removesuffix(".valid.json")
        schema_path = SCHEMA_DIR / f"{schema_name}.schema.json"
        if not schema_path.exists():
            errors.append(f"{fixture.relative_to(ROOT)}: missing schema {schema_path.relative_to(ROOT)}")
            continue
        schema = load_json(schema_path)
        value = load_json(fixture)
        errors.extend(validate_value(value, schema, str(fixture.relative_to(ROOT))))

    release_records = sorted(RELEASE_RECORD_DIR.glob("*.json")) if RELEASE_RECORD_DIR.exists() else []
    for record_path in release_records:
        value = load_json(record_path)
        release_schema_path = release_schema_for(value)
        if not release_schema_path.exists():
            errors.append(f"{record_path.relative_to(ROOT)}: missing schema {release_schema_path.relative_to(ROOT)}")
            continue
        release_schema = load_json(release_schema_path)
        errors.extend(validate_value(value, release_schema, str(record_path.relative_to(ROOT))))

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(
        "Protocol example validation passed for "
        f"{len(fixtures)} fixtures and {len(release_records)} release records."
    )


if __name__ == "__main__":
    main()
