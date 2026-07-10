#!/usr/bin/env python3
"""Validate deferred specialist packets and the no-prepublication-outreach policy."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "governance" / "external_review_program.json"
SCHEMA = ROOT / "schemas" / "external_review_program.schema.json"
CAPACITY = ROOT / "governance" / "reviewer_capacity_registry.json"
EXPECTED = {
    "formal_methods": "formal_methods_reviewer",
    "safety_governance": "safety_governance_reviewer",
    "systems_editorial": "systems_editorial_reviewer",
}
PACKET_HEADINGS = (
    "## Reviewer capacity and independence",
    "## Review boundary",
    "## Required artifacts",
    "## Required questions",
    "## Adversarial review prompts",
    "## Severity and disposition rubric",
    "## Required response record",
    "## Non-claims",
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(program: dict[str, Any]) -> list[str]:
    errors = validate_against_schema(program, load(SCHEMA), "external_review_program")
    tracks = {row.get("id"): row for row in program.get("tracks", [])}
    if set(tracks) != set(EXPECTED) or len(program.get("tracks", [])) != 3:
        errors.append(f"external review tracks must be exactly {sorted(EXPECTED)}")
    capacity = {row["role_id"]: row for row in load(CAPACITY)["records"]}
    for track_id, role in EXPECTED.items():
        row = tracks.get(track_id, {})
        if row.get("capacity_role") != role:
            errors.append(f"{track_id}: wrong capacity role")
        if capacity.get(role, {}).get("assignment_state") != "deferred_postpublication":
            errors.append(f"{track_id}: specialist reviewer must remain deferred until author-declared completion")
        packet = ROOT / row.get("packet", "")
        if not packet.exists():
            errors.append(f"{track_id}: missing packet {row.get('packet')}")
            continue
        text = packet.read_text(encoding="utf-8", errors="ignore")
        for heading in PACKET_HEADINGS:
            if heading not in text:
                errors.append(f"{track_id}: packet missing {heading}")
        for phrase in ("finding ID", "severity", "attribution boundary", "not independent review"):
            if phrase.lower() not in text.lower():
                errors.append(f"{track_id}: packet missing response boundary {phrase!r}")
        for scope in row.get("scope_refs", []):
            if not (ROOT / scope).exists():
                errors.append(f"{track_id}: missing scope artifact {scope}")
        if row.get("support_state_effect") != "none":
            errors.append(f"{track_id}: packet readiness must have no support effect")
        if row.get("solicitation_state") != "no_prepublication_outreach_packets_preserved_for_optional_postpublication_use":
            errors.append(f"{track_id}: prepublication solicitation is forbidden by author policy")
    if program.get("program_state") != "deferred_until_author_declared_complete":
        errors.append("external review program must remain deferred until author-declared completion")
    return errors


def negative_controls(program: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    fake_state = copy.deepcopy(program)
    fake_state["program_state"] = "specialist_packets_ready_reviewers_unassigned"
    fake_effect = copy.deepcopy(program)
    fake_effect["tracks"][0]["support_state_effect"] = "review_input_only"
    for label, mutation in (("false accepted state", fake_state), ("support effect", fake_effect)):
        if not semantic_errors(mutation):
            failures.append(f"negative control was incorrectly accepted: {label}")
    packet_text = (ROOT / program["tracks"][0]["packet"]).read_text(encoding="utf-8")
    if "## Severity and disposition rubric" not in packet_text:
        failures.append("formal packet lacks rubric before negative control")
    else:
        mutated = packet_text.replace("## Severity and disposition rubric", "## Removed rubric", 1)
        if all(heading in mutated for heading in PACKET_HEADINGS):
            failures.append("negative control was incorrectly accepted: missing severity rubric")
    return failures


def main() -> None:
    program = load(PROGRAM)
    errors = semantic_errors(program)
    errors.extend(negative_controls(program))
    if errors:
        print("External-review program validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("External-review program validation passed: 3 specialist packets preserved, 3 roles deferred until post-publication, no prepublication outreach, and 3 rejecting negative controls.")


if __name__ == "__main__":
    main()
