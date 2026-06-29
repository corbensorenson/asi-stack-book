#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "protocols" / "v1_critical_protocol_crosswalk.json"
REPORT = ROOT / "docs" / "protocol_record_crosswalk.md"
STRUCTURE = ROOT / "book_structure.json"
HARNESS_REGISTRY = ROOT / "experiments" / "phase5_harness_registry.json"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

REQUIRED_FIELDS = {
    "id",
    "schema",
    "fixture_dir",
    "harness_script",
    "harness_doc",
    "result_record",
    "phase5_registry_id",
    "appendix_e_markers",
    "primary_chapters",
    "lean_module",
    "lean_structures",
    "lean_mapped_fields",
    "harness_only_fields",
    "abstracted_fields",
    "abstraction_note",
}


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def flatten_chapter_ids(structure: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("id"), str):
                ids.add(chapter["id"])
    return ids


def schema_fields(path: Path) -> set[str]:
    schema = read_json(path)
    if not isinstance(schema, dict):
        raise TypeError(f"{rel(path)} must contain an object.")
    properties = schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        raise TypeError(f"{rel(path)} must contain non-empty properties.")
    return set(properties)


def fixture_counts(path: Path) -> tuple[int, int]:
    valid = len([item for item in path.glob("valid_*.json") if item.is_file()])
    invalid = len([item for item in path.glob("invalid_*.json") if item.is_file()])
    return valid, invalid


def parse_lean_structures(path: Path) -> dict[str, set[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    structures: dict[str, set[str]] = {}
    for match in re.finditer(
        r"^structure\s+(\w+)\s+where\n(.*?)(?=^deriving|^def|^theorem|^structure|^inductive|^end)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    ):
        fields: set[str] = set()
        for line in match.group(2).splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("--") or ":" not in stripped:
                continue
            fields.add(stripped.split(":", 1)[0].strip())
        structures[match.group(1)] = fields
    return structures


def field_refs(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value)
    raise TypeError("Lean field mapping values must be strings or lists of strings.")


def require_mapping_object(record: dict[str, Any], field: str, errors: list[str]) -> dict[str, Any]:
    value = record.get(field)
    if not isinstance(value, dict):
        errors.append(f"{record.get('id', '<missing>')}: {field} must be an object.")
        return {}
    return value


def build_report() -> tuple[str, list[str]]:
    crosswalk = read_json(CROSSWALK)
    structure = read_json(STRUCTURE)
    registry = read_json(HARNESS_REGISTRY)
    appendix_text = APPENDIX_E.read_text(encoding="utf-8", errors="ignore")
    if not isinstance(crosswalk, dict) or not isinstance(crosswalk.get("records"), list):
        raise TypeError("protocol crosswalk must contain a records list.")
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object.")
    if not isinstance(registry, list):
        raise TypeError("phase5_harness_registry.json must contain a list.")

    records = [record for record in crosswalk["records"] if isinstance(record, dict)]
    registry_by_id = {str(item.get("id")): item for item in registry if isinstance(item, dict)}
    chapter_ids = flatten_chapter_ids(structure)
    errors: list[str] = []
    record_rows: list[str] = []
    field_rows: list[str] = []

    ids = [record.get("id") for record in records]
    duplicate_ids = sorted(str(item) for item, count in Counter(ids).items() if item and count > 1)
    for item in duplicate_ids:
        errors.append(f"Duplicate protocol crosswalk id: {item}")

    for record in records:
        record_id = str(record.get("id", "<missing>"))
        missing = sorted(REQUIRED_FIELDS - set(record))
        if missing:
            errors.append(f"{record_id}: missing required fields: {missing}")
            continue

        for field in ("id", "schema", "fixture_dir", "harness_script", "harness_doc", "result_record", "phase5_registry_id", "lean_module", "abstraction_note"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{record_id}: {field} must be a non-empty string.")

        for field in ("appendix_e_markers", "primary_chapters", "lean_structures"):
            if not isinstance(record.get(field), list) or not record[field]:
                errors.append(f"{record_id}: {field} must be a non-empty list.")

        schema_path = ROOT / str(record.get("schema", ""))
        fixture_dir = ROOT / str(record.get("fixture_dir", ""))
        harness_script = ROOT / str(record.get("harness_script", ""))
        harness_doc = ROOT / str(record.get("harness_doc", ""))
        result_record = ROOT / str(record.get("result_record", ""))
        lean_module = ROOT / str(record.get("lean_module", ""))

        for path in (schema_path, fixture_dir, harness_script, harness_doc, result_record, lean_module):
            if not path.exists():
                errors.append(f"{record_id}: missing path {rel(path)}")

        props: set[str] = set()
        if schema_path.exists():
            try:
                props = schema_fields(schema_path)
            except Exception as exc:
                errors.append(f"{record_id}: schema read failed: {exc}")

        lean_mapped = require_mapping_object(record, "lean_mapped_fields", errors)
        harness_only = require_mapping_object(record, "harness_only_fields", errors)
        abstracted = require_mapping_object(record, "abstracted_fields", errors)
        covered = set(lean_mapped) | set(harness_only) | set(abstracted)
        if props:
            missing_props = sorted(props - covered)
            extra_props = sorted(covered - props)
            if missing_props:
                errors.append(f"{record_id}: schema fields not reconciled: {missing_props}")
            if extra_props:
                errors.append(f"{record_id}: crosswalk lists non-schema fields: {extra_props}")

        if lean_module.exists():
            structures = parse_lean_structures(lean_module)
            for structure_name in record.get("lean_structures", []):
                if structure_name not in structures:
                    errors.append(f"{record_id}: Lean structure {structure_name} not found in {rel(lean_module)}.")
            for schema_field, ref_value in lean_mapped.items():
                try:
                    refs = field_refs(ref_value)
                except TypeError as exc:
                    errors.append(f"{record_id}: {schema_field}: {exc}")
                    continue
                for ref in refs:
                    if "." not in ref:
                        errors.append(f"{record_id}: {schema_field}: Lean ref {ref!r} must be Structure.field.")
                        continue
                    structure_name, field_name = ref.split(".", 1)
                    if structure_name not in structures:
                        errors.append(f"{record_id}: {schema_field}: Lean structure {structure_name} not found.")
                    elif field_name not in structures[structure_name]:
                        errors.append(f"{record_id}: {schema_field}: Lean field {ref} not found.")

        registry_id = str(record.get("phase5_registry_id", ""))
        registry_entry = registry_by_id.get(registry_id)
        registry_status = "registry ok"
        if registry_entry is None:
            errors.append(f"{record_id}: phase5 registry id {registry_id!r} not found.")
            registry_status = "registry missing"
        else:
            comparisons = {
                "script": "harness_script",
                "doc": "harness_doc",
                "fixture_dir": "fixture_dir",
                "result_record": "result_record",
            }
            for registry_field, record_field in comparisons.items():
                if registry_entry.get(registry_field) != record.get(record_field):
                    errors.append(
                        f"{record_id}: {record_field} {record.get(record_field)!r} does not match registry {registry_field} {registry_entry.get(registry_field)!r}."
                    )
            if set(registry_entry.get("primary_chapters", [])) != set(record.get("primary_chapters", [])):
                errors.append(f"{record_id}: primary_chapters do not match the Phase 5 harness registry.")

        for chapter_id in record.get("primary_chapters", []):
            if chapter_id not in chapter_ids:
                errors.append(f"{record_id}: unknown primary chapter {chapter_id!r}.")

        for marker in record.get("appendix_e_markers", []):
            if marker not in appendix_text:
                errors.append(f"{record_id}: Appendix E marker missing: {marker}")

        if "does not" not in str(record.get("abstraction_note", "")).lower():
            errors.append(f"{record_id}: abstraction_note must include an explicit non-claim boundary.")

        valid_count, invalid_count = fixture_counts(fixture_dir) if fixture_dir.exists() else (0, 0)
        if fixture_dir.exists() and valid_count == 0:
            errors.append(f"{record_id}: fixture_dir has no valid_*.json fixtures.")
        if fixture_dir.exists() and invalid_count == 0:
            errors.append(f"{record_id}: fixture_dir has no invalid_*.json fixtures.")

        lean_route = f"{record.get('lean_module')} ({', '.join(record.get('lean_structures', []))})"
        status = "ok" if record_id not in " ".join(errors) else "check errors"
        record_rows.append(
            f"| `{qmd_escape(record_id)}` | `{qmd_escape(record.get('schema'))}` | {len(props)} | "
            f"{valid_count}/{invalid_count} | `{qmd_escape(record.get('harness_script'))}` | "
            f"{qmd_escape(lean_route)} | {len(lean_mapped)} | {len(harness_only)} | {len(abstracted)} | {qmd_escape(registry_status)} | {qmd_escape(status)} |"
        )

        for schema_field in sorted(covered):
            if schema_field in lean_mapped:
                route = "Lean"
                detail = field_refs(lean_mapped[schema_field])
            elif schema_field in harness_only:
                route = "Harness"
                detail = [str(harness_only[schema_field])]
            else:
                route = "Intentional abstraction"
                detail = [str(abstracted[schema_field])]
            field_rows.append(
                f"| `{qmd_escape(record_id)}` | `{qmd_escape(schema_field)}` | {route} | {qmd_escape('; '.join(detail))} |"
            )

    summary_rows = [
        f"| V1-critical protocol records | {len(records)} |",
        f"| Phase 5 registry entries referenced | {len({record.get('phase5_registry_id') for record in records})} |",
        f"| Schema fields reconciled | {sum(len(require_mapping_object(record, 'lean_mapped_fields', [])) + len(require_mapping_object(record, 'harness_only_fields', [])) + len(require_mapping_object(record, 'abstracted_fields', [])) for record in records)} |",
        f"| Validation errors | {len(errors)} |",
    ]
    error_text = "\n".join(f"- {qmd_escape(error)}" for error in errors) if errors else "- None."

    report = f"""# Protocol Record Crosswalk

Generated by `python3 scripts/validate_protocol_crosswalk.py --write`.

This report is the v1.0 source-of-truth hardening pass for critical protocol records. It crosswalks JSON Schemas, synthetic fixtures, harness validators, result records, Appendix E markers, primary chapters, and Lean structures where a Lean abstraction exists.

It does **not** treat any protocol record as verified merely because one lane passes. Schema validation checks shape, fixtures check synthetic examples, harnesses check deterministic fixture rules, and Lean checks narrow finite abstractions. Field mismatches are either mapped to a Lean structure field, routed to the Python harness, or recorded as an intentional abstraction.

## Summary

| Metric | Value |
|---|---:|
{chr(10).join(summary_rows)}

## Record Crosswalk

| Protocol record | Schema | Schema fields | Valid/invalid fixtures | Harness | Lean route | Lean fields | Harness-only fields | Abstracted fields | Registry | Status |
|---|---|---:|---:|---|---|---:|---:|---:|---|---|
{chr(10).join(record_rows)}

## Field Reconciliation

| Protocol record | Schema field | Route | Detail |
|---|---|---|---|
{chr(10).join(field_rows)}

## Validation Errors

{error_text}
"""
    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write docs/protocol_record_crosswalk.md.")
    args = parser.parse_args()

    try:
        report, errors = build_report()
    except Exception as exc:
        print(f"Protocol crosswalk validation failed: {exc}")
        sys.exit(1)

    if args.write:
        REPORT.write_text(report, encoding="utf-8")
    elif not REPORT.exists():
        print(f"{REPORT.relative_to(ROOT)} is missing; run scripts/validate_protocol_crosswalk.py --write")
        sys.exit(1)
    else:
        current = REPORT.read_text(encoding="utf-8")
        if current != report:
            print(f"{REPORT.relative_to(ROOT)} is out of date; run scripts/validate_protocol_crosswalk.py --write")
            sys.exit(1)

    if errors:
        print("Protocol crosswalk validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Protocol crosswalk validation passed: {len(read_json(CROSSWALK)['records'])} v1-critical record(s).")


if __name__ == "__main__":
    main()
