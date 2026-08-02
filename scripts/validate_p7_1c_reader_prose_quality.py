#!/usr/bin/env python3
"""Validate the machine status for the P7.1c reader-prose quality lane."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "roadmap_records/p7_1c_reader_prose_quality_status.json"
SCHEMA = ROOT / "schemas/p7_1c_reader_prose_quality_status.schema.json"
ROADMAP = ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
REVIEW = ROOT / "docs/round_23_reader_prose_quality_reconciliation_2026_08_02.md"


def main() -> int:
    status = json.loads(STATUS.read_text())
    schema = json.loads(SCHEMA.read_text())
    errors = sorted(Draft202012Validator(schema).iter_errors(status), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            print(f"P7.1c status validation failed: {error.message}")
        return 1
    for path, marker in [
        (ROADMAP, "P7.1c — Reader-first concreteness, prose, and surface discipline"),
        (REVIEW, "# Round 23 reader-prose quality reconciliation"),
    ]:
        if not path.exists() or marker not in path.read_text():
            print(f"P7.1c status validation failed: missing marker {marker!r} in {path}")
            return 1
    print("P7.1c reader-prose quality status validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
