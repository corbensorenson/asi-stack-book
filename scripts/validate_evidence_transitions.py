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
ADMINISTRATIVE_SCHEMA_VERSIONS = {
    "asi_stack.instrument_failure_supersession.v1",
}
ADMINISTRATIVE_TRANSITION_TYPES = {
    "instrument_failure_supersession",
}


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
    transition_count = 0
    administrative_count = 0
    for record_path in records:
        relative = str(record_path.relative_to(ROOT))
        try:
            value = load_json(record_path)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.extend(validate_value(value, schema, relative))
            continue

        is_administrative = (
            value.get("schema_version") in ADMINISTRATIVE_SCHEMA_VERSIONS
            or value.get("transition_type") in ADMINISTRATIVE_TRANSITION_TYPES
        )
        if is_administrative:
            administrative_count += 1
            if value.get("support_state_effect") != "none":
                errors.append(f"{relative}: administrative disposition must have support_state_effect none.")
            non_claims = value.get("non_claims")
            if not isinstance(non_claims, list) or not non_claims:
                errors.append(f"{relative}: administrative disposition must preserve non_claims.")
            if value.get("review_status") == "accepted":
                errors.append(f"{relative}: administrative disposition cannot masquerade as an accepted claim transition.")
            continue

        transition_count += 1
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
            if value.get("transition_effect") == "no_change":
                if value.get("support_state_effect") not in {"argument_only", "blocks_promotion"}:
                    errors.append(f"{relative}: no_change records must be argument_only or blocks_promotion.")
            elif value.get("transition_effect") == "upward":
                if value.get("old_support_state") == value.get("new_support_state"):
                    errors.append(f"{relative}: upward transition must change support state.")
                if value.get("verification_result") != "pass":
                    errors.append(f"{relative}: upward transition must have passing verification_result.")
                if value.get("support_state_effect") != "eligible_for_bounded_evidence_review":
                    errors.append(
                        f"{relative}: upward transition must use support_state_effect eligible_for_bounded_evidence_review."
                    )
                if value.get("acceptance_blockers"):
                    errors.append(f"{relative}: accepted upward transition must not list acceptance_blockers.")
                if not value.get("artifact_refs"):
                    errors.append(f"{relative}: upward transition must name artifact_refs.")
                if not value.get("negative_results"):
                    errors.append(f"{relative}: upward transition must record negative_results.")
            elif value.get("support_state_effect") not in {"blocks_promotion", "record_shape_only"}:
                errors.append(f"{relative}: unsupported transition/support_state_effect combination.")

    if errors:
        print("Evidence transition validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Evidence transition validation passed: "
        f"{transition_count} claim transition record(s), "
        f"{administrative_count} administrative disposition record(s)."
    )


if __name__ == "__main__":
    main()
