#!/usr/bin/env python3
"""Validate protocol fixtures and release records against their full schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from schema_validation import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "protocol_records"
RELEASE_RECORD_DIR = ROOT / "release_records"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def release_schema_for(value: Any) -> Path:
    custom_schemas = {
        "asi_stack.p8_terminal_release_record.v1": "p8_terminal_release_record.schema.json",
        "asi_stack.x_article_release_disposition.v1": "x_article_release_disposition.schema.json",
        "asi_stack.roadmap_terminal_disposition.v1": "roadmap_terminal_disposition.schema.json",
    }
    if isinstance(value, dict) and value.get("schema_version") in custom_schemas:
        return SCHEMA_DIR / custom_schemas[value["schema_version"]]
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
