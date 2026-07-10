#!/usr/bin/env python3
"""Validate the three defended contributions and all-chapter focus map."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from build_canonical_public_status import validate_against_schema
from build_contribution_focus_contract import OUTPUT, ROOT, build_contract


SCHEMA = ROOT / "schemas" / "contribution_focus_contract.schema.json"
DOC = ROOT / "docs" / "three_defended_contributions.md"
TRACKS = ROOT / "docs" / "defended_contribution_tracks.md"
REMEDIATION = ROOT / "docs" / "external_ai_review_remediation_program.md"
EXPECTED = {
    "governed-cognition-interface-contracts",
    "claim-state-transition-discipline",
    "record-reality-residual-honesty",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    for path in (OUTPUT, SCHEMA, DOC, TRACKS, REMEDIATION):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        fail(errors)
    tracked = load(OUTPUT)
    expected = build_contract()
    errors.extend(validate_against_schema(tracked, load(SCHEMA), str(OUTPUT.relative_to(ROOT))))
    if tracked != expected:
        errors.append(f"{OUTPUT.relative_to(ROOT)} is stale; run python3 scripts/build_contribution_focus_contract.py")
    contributions = tracked.get("contributions", [])
    if {row.get("id") for row in contributions} != EXPECTED or len(contributions) != 3:
        errors.append("program must contain exactly the three defended contributions")
    assignments = tracked.get("chapter_assignments", [])
    ids = [row.get("chapter_id") for row in assignments]
    if len(ids) != 54 or len(set(ids)) != 54:
        errors.append("chapter focus map must contain 54 unique manifest chapters")
    if any(row.get("contribution_id") not in EXPECTED for row in assignments):
        errors.append("chapter assignment uses an unknown contribution")
    if any(row.get("independent_flagship_claim") is not False for row in assignments):
        errors.append("no chapter may be marked as an independent flagship claim")
    roles = {row.get("contribution_role") for row in assignments}
    if roles != {"primary_owner", "supporting_or_integration"}:
        errors.append(f"unexpected contribution roles: {roles}")
    summary = tracked.get("summary", {})
    expected_summary = {
        "contribution_count": 3,
        "chapter_count": 54,
        "primary_owner_count": 11,
        "supporting_or_integration_count": 43,
        "independent_flagship_chapter_count": 0,
    }
    if summary != expected_summary:
        errors.append(f"summary mismatch: {summary!r}")
    doc = DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        "## Governed-cognition interface contracts",
        "## Public claim-state transition discipline",
        "## Record/reality reconciliation and residual honesty",
        "all 54 manifest chapters",
        "Eleven are primary owners",
        "other 43 are supporting or integration chapters",
        "not novelty proof",
    ):
        if phrase not in doc:
            errors.append(f"{DOC.relative_to(ROOT)} missing {phrase!r}")
    tracks = TRACKS.read_text(encoding="utf-8", errors="ignore")
    for phrase in ("three program-level defended contributions", "five subordinate work tracks", "products/contribution_focus_contract.json"):
        if phrase not in tracks:
            errors.append(f"{TRACKS.relative_to(ROOT)} missing {phrase!r}")
    remediation = REMEDIATION.read_text(encoding="utf-8", errors="ignore")
    if "products/contribution_focus_contract.json" not in remediation:
        errors.append("remediation program does not name the contribution focus contract")
    fail(errors)
    print("Contribution focus validation passed: 3 contributions, 54 unique chapter assignments, 11 primary owners, 43 supporting/integration roles, 0 independent chapter flagships.")


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Contribution focus validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
