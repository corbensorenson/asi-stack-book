#!/usr/bin/env python3
"""Validate structured external-review intake records.

The validator separates public requests from accepted review input. It prevents
request-update records from being misread as source evidence, support-state
movement, artifact approval, or authorization to merge chapters.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


from schema_validation import validate_value


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "external_review_intake_record.schema.json"
RECORD_DIR = ROOT / "external_reviews"
STATUS = ROOT / "docs" / "external_review_status.md"
ISSUE_URL = "https://github.com/corbensorenson/asi-stack-book/issues/1"
CONSOLIDATION_COMMENT_URL = (
    "https://github.com/corbensorenson/asi-stack-book/issues/1#issuecomment-4835627101"
)
FULL_CONSOLIDATION_COMMENT_URL = (
    "https://github.com/corbensorenson/asi-stack-book/issues/1#issuecomment-4837313658"
)
CURRENT_BLOCKER_ID = "no-named-external-reviewer-2026-07-01"
CURRENT_BLOCKER_PATH = "external_reviews/blockers/no_named_external_reviewer_2026-07-01.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    print("External review intake validation failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


def semantic_errors(path: Path, value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    relative = str(path.relative_to(ROOT))
    record_type = value.get("record_type")
    status = value.get("review_status")

    if record_type == "accepted_review":
        if status != "accepted":
            errors.append(f"{relative}: accepted_review must have review_status accepted.")
        if "not_applicable" in str(value.get("reviewer_background", "")):
            errors.append(f"{relative}: accepted_review must name reviewer background or anonymized expertise.")
        if not value.get("review_scope_refs"):
            errors.append(f"{relative}: accepted_review must list reviewed scope.")
        if value.get("support_state_effect") != "review_input_only":
            errors.append(f"{relative}: accepted_review must remain review_input_only for support_state_effect.")
    elif record_type == "review_blocker":
        if status != "blocked":
            errors.append(f"{relative}: review_blocker must have review_status blocked.")
        if not value.get("acceptance_blockers"):
            errors.append(f"{relative}: review_blocker must list acceptance_blockers.")
        if value.get("attribution_boundary") not in {"public_request", "not_applicable"}:
            errors.append(f"{relative}: review_blocker must use public_request or not_applicable attribution boundary.")
    else:
        if status == "accepted":
            errors.append(f"{relative}: only accepted_review records may have review_status accepted.")
        for key in ["support_state_effect", "artifact_release_effect", "evidence_effect"]:
            if value.get(key) != "none":
                errors.append(f"{relative}: non-accepted review records must keep {key} at none.")

    joined = json.dumps(value, sort_keys=True)
    forbidden = [
        "review proves",
        "review validates the architecture",
        "review promotes",
        "artifact approved by reviewer",
        "support-state promotion",
    ]
    for phrase in forbidden:
        if phrase in joined:
            errors.append(f"{relative}: contains forbidden overclaim phrase {phrase!r}.")

    if "This request update does not create an accepted external-review result." not in value.get(
        "non_claims", []
    ) and record_type == "request_update":
        errors.append(f"{relative}: request_update missing accepted-review non-claim.")

    return errors


def main() -> None:
    errors: list[str] = []
    schema = load_json(SCHEMA)
    records = sorted(RECORD_DIR.rglob("*.json")) if RECORD_DIR.exists() else []
    if not records:
        errors.append("No external review intake records found.")

    accepted_records: list[Path] = []
    request_update_records: list[Path] = []
    blocker_records: list[Path] = []
    saw_consolidation_request = False
    saw_full_consolidation_request = False
    saw_current_blocker = False

    for record_path in records:
        value = load_json(record_path)
        relative = str(record_path.relative_to(ROOT))
        errors.extend(validate_value(value, schema, relative))
        if isinstance(value, dict):
            errors.extend(semantic_errors(record_path, value))
            if value.get("record_type") == "accepted_review":
                accepted_records.append(record_path)
            if value.get("record_type") == "request_update":
                request_update_records.append(record_path)
            if value.get("record_type") == "review_blocker":
                blocker_records.append(record_path)
            if (
                str(record_path.relative_to(ROOT)) == CURRENT_BLOCKER_PATH
                and value.get("record_id") == CURRENT_BLOCKER_ID
                and value.get("review_status") == "blocked"
            ):
                saw_current_blocker = True
            refs = value.get("public_request_refs", [])
            if ISSUE_URL in refs and CONSOLIDATION_COMMENT_URL in refs:
                saw_consolidation_request = True
            if ISSUE_URL in refs and FULL_CONSOLIDATION_COMMENT_URL in refs:
                saw_full_consolidation_request = True

    status_text = STATUS.read_text(encoding="utf-8")
    if accepted_records and "no independent external review has been accepted yet" in status_text:
        errors.append("external_review_status.md still says no review accepted, but accepted records exist.")
    if not accepted_records and "no independent external review has been accepted yet" not in status_text:
        errors.append("external_review_status.md must preserve no-accepted-review status.")
    if CONSOLIDATION_COMMENT_URL not in status_text:
        errors.append("external_review_status.md does not record the consolidation issue comment URL.")
    if FULL_CONSOLIDATION_COMMENT_URL not in status_text:
        errors.append("external_review_status.md does not record the full consolidation issue comment URL.")
    if not saw_consolidation_request:
        errors.append("No intake record preserves the consolidation issue comment URL.")
    if not saw_full_consolidation_request:
        errors.append("No intake record preserves the full consolidation issue comment URL.")
    if not saw_current_blocker:
        errors.append("No intake record preserves the current dated no-named-reviewer blocker.")
    if CURRENT_BLOCKER_PATH not in status_text:
        errors.append("external_review_status.md does not reference the current external-review blocker record.")
    if "no named independent reviewer response or approved direct outreach target" not in status_text:
        errors.append("external_review_status.md does not explain the current outreach blocker.")

    if errors:
        fail(errors)

    print(
        "External review intake validation passed: "
        f"{len(records)} record(s), {len(request_update_records)} request update(s), "
        f"{len(blocker_records)} blocker(s), {len(accepted_records)} accepted review(s)."
    )


if __name__ == "__main__":
    main()
