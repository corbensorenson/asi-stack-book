#!/usr/bin/env python3
"""Validate implemented author title and delayed-opening decisions."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "author_decision_packet.schema.json"
TITLE = ROOT / "governance" / "title_positioning_decision.json"
LICENSE_DECISION = ROOT / "governance" / "licensing_decision.json"
LICENSE_FILE = ROOT / "LICENSE.md"
STRUCTURE = ROOT / "book_structure.json"
CITATION = ROOT / "CITATION.cff"
CURRENT_TITLE = "The ASI Stack"
CURRENT_SUBTITLE = "A Governed Systems Architecture for Advanced AI, with ASI as the Stress Case"
EXPECTED_TITLE_SELECTION = "retain_brand_reframe_subtitle"
EXPECTED_LICENSE_SELECTION = "delayed_opening"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(title: dict[str, Any], licensing: dict[str, Any]) -> list[str]:
    schema = load(SCHEMA)
    errors = validate_against_schema(title, schema, "title_decision")
    errors.extend(validate_against_schema(licensing, schema, "licensing_decision"))
    if title.get("decision_id") == licensing.get("decision_id"):
        errors.append("author decision IDs must be distinct")
    for label, packet in (("title", title), ("licensing", licensing)):
        option_ids = [row.get("id") for row in packet.get("options", [])]
        if len(option_ids) < 3 or len(set(option_ids)) != len(option_ids):
            errors.append(f"{label}: options must contain at least three unique choices")
        if packet.get("status") != "decided":
            errors.append(f"{label}: author decision must be recorded as decided")
        if packet.get("selected_option_id") not in option_ids:
            errors.append(f"{label}: selected option must resolve to one recorded option")
        if packet.get("support_state_effect") != "none":
            errors.append(f"{label}: author decision must not change support")
    if title.get("selected_option_id") != EXPECTED_TITLE_SELECTION:
        errors.append("title: retain-brand/reframed-subtitle selection is not locked")
    if licensing.get("selected_option_id") != EXPECTED_LICENSE_SELECTION:
        errors.append("licensing: delayed-opening selection is not locked")
    structure = load(STRUCTURE)
    if structure.get("title") != CURRENT_TITLE or structure.get("subtitle") != CURRENT_SUBTITLE:
        errors.append("book_structure does not implement the selected active title")
    citation = CITATION.read_text(encoding="utf-8", errors="ignore")
    if f'title: "{CURRENT_TITLE}: {CURRENT_SUBTITLE}"' not in citation:
        errors.append("CITATION.cff does not implement the selected active title")
    license_text = LICENSE_FILE.read_text(encoding="utf-8", errors="ignore")
    for phrase in ("All rights reserved", "no license is granted", "not a present license grant"):
        if phrase not in license_text:
            errors.append(f"LICENSE.md does not preserve delayed-opening boundary: missing {phrase!r}")
    for premature in ("SPDX-License-Identifier:", "Apache License\nVersion 2.0", "CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM"):
        if premature in license_text:
            errors.append(f"LICENSE.md contains premature open-license signal: {premature}")
    return errors


def negative_controls(title: dict[str, Any], licensing: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    selected = copy.deepcopy(title)
    selected["selected_option_id"] = "retain_current"
    selected_license = copy.deepcopy(licensing)
    selected_license["selected_option_id"] = "permissive_split"
    for label, t, l in (
        ("title selection drift", selected, licensing),
        ("license selection drift", title, selected_license),
    ):
        if not semantic_errors(t, l):
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    title = load(TITLE)
    licensing = load(LICENSE_DECISION)
    errors = semantic_errors(title, licensing)
    errors.extend(negative_controls(title, licensing))
    if errors:
        print("Author decision-packet validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Author decision-packet validation passed: reframed title and delayed-opening policy are locked, 8 options remain recorded, and 2 selection-drift controls reject.")


if __name__ == "__main__":
    main()
