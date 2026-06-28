#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
TRANSITION_DIR = ROOT / "evidence_transitions"
SCHEMA = ROOT / "schemas" / "evidence_transition_record.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    if not TRANSITION_DIR.exists():
        print("No evidence_transitions directory found.")
        return

    schema = load_json(SCHEMA)
    records = sorted(
        path
        for path in TRANSITION_DIR.rglob("*.json")
        if path.name != "README.json"
    )
    if not records:
        print("No evidence transition records found.")
        return

    errors: list[str] = []
    seen_ids: set[str] = set()
    for record_path in records:
        relative = str(record_path.relative_to(ROOT))
        try:
            value = load_json(record_path)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        errors.extend(validate_value(value, schema, relative))
        transition_id = value.get("transition_id") if isinstance(value, dict) else None
        if isinstance(transition_id, str):
            if transition_id in seen_ids:
                errors.append(f"{relative}: duplicate transition_id {transition_id!r}")
            seen_ids.add(transition_id)
        if isinstance(value, dict):
            if value.get("transition_effect") == "upward" and value.get("review_status") != "accepted":
                errors.append(f"{relative}: upward transition must have accepted review_status.")
            if value.get("new_support_state") != "argument" and value.get("transition_effect") == "no_change":
                errors.append(f"{relative}: no_change transition must keep new_support_state at argument.")
            if value.get("support_state_effect") not in {"argument_only", "blocks_promotion"}:
                errors.append(f"{relative}: pilot records must be argument_only or blocks_promotion.")

    if errors:
        print("Evidence transition validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Evidence transition validation passed: {len(records)} record(s).")


if __name__ == "__main__":
    main()
