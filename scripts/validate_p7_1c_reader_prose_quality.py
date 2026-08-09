#!/usr/bin/env python3
"""Validate the machine status for the P7.1c reader-prose quality lane."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "roadmap_records/p7_1c_reader_prose_quality_status.json"
SCHEMA = ROOT / "schemas/p7_1c_reader_prose_quality_status.schema.json"
ROADMAP = ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
REVIEW = ROOT / "docs/round_23_reader_prose_quality_reconciliation_2026_08_02.md"
TRIAGE = ROOT / "docs/chapter_content_triage_2026_08_08.md"
STRUCTURE = ROOT / "book_structure.json"
PACKET_SCHEMA = ROOT / "schemas/p7_1c_reader_prose_quality_packet.schema.json"
PACKET_DIR = ROOT / "evidence_quality/reader_prose_quality_packets"
ROLE_MAP = ROOT / "evidence_quality/current_chapter_role_map.json"
UNIT_MAP = ROOT / "products/narrative_unit_crosswalk.json"


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def packet_errors(
    packet: dict[str, Any],
    packet_schema: dict[str, Any],
    chapters: dict[str, dict[str, Any]],
    roles: dict[str, str],
    units: dict[str, str],
) -> list[str]:
    errors = [
        error.message
        for error in Draft202012Validator(packet_schema).iter_errors(packet)
    ]
    chapter_id = str(packet.get("chapter_id", ""))
    chapter = chapters.get(chapter_id)
    if chapter is None:
        return errors + [f"unknown chapter {chapter_id!r}"]
    if packet.get("chapter_file") != chapter.get("file"):
        errors.append("chapter file does not match manifest")
        return errors
    chapter_path = ROOT / str(chapter["file"])
    chapter_text = chapter_path.read_text()
    digest = hashlib.sha256(chapter_path.read_bytes()).hexdigest()
    if packet.get("chapter_sha256") != digest:
        errors.append("chapter digest is stale")
    if packet.get("chapter_role") != roles.get(chapter_id):
        errors.append("chapter role does not match canonical role map")
    if packet.get("reader_spine_unit") != units.get(chapter_id):
        errors.append("reader-spine unit does not match canonical crosswalk")

    normalized_chapter = normalized(chapter_text)
    scene = packet.get("concrete_scene", {})
    trace = packet.get("worked_trace", {})
    for label, heading in [
        ("concrete scene", scene.get("heading", "")),
        ("worked trace", trace.get("heading", "")),
    ]:
        if heading and f"### {heading}" not in chapter_text:
            errors.append(f"{label} heading is absent from chapter")
    for label, value in [
        ("readable claim", packet.get("readable_claim", "")),
        ("normative rule", packet.get("normative_rule", "")),
        ("formal binding", packet.get("formal_binding", {}).get("anchor", "")),
    ]:
        if value and normalized(str(value)) not in normalized_chapter:
            errors.append(f"{label} is absent from chapter")

    scene_semantics = normalized(" ".join(str(scene.get(field, "")) for field in [
        "actor_or_system",
        "attempted_action",
        "observable_outcome",
        "failed_or_tested_boundary",
        "residual_owner",
        "evidence_boundary",
    ]))
    generic_fragments = (
        "a system does something",
        "an actor takes an action",
        "this chapter explains the mechanism",
        "a generic example",
    )
    if len(scene_semantics) < 300:
        errors.append("concrete scene semantics are too thin")
    if any(fragment in scene_semantics.lower() for fragment in generic_fragments):
        errors.append("concrete scene is generic")
    if not packet.get("caveat_consolidation", {}).get("distinct_limitations_preserved"):
        errors.append("distinct limitations are not preserved")
    for ref in trace.get("source_or_fixture_refs", []):
        if not (ROOT / str(ref)).exists():
            errors.append(f"worked-trace reference does not exist: {ref}")
    return errors


def main() -> int:
    status = json.loads(STATUS.read_text())
    schema = json.loads(SCHEMA.read_text())
    errors = sorted(Draft202012Validator(schema).iter_errors(status), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            print(f"P7.1c status validation failed: {error.message}")
        return 1
    structure = json.loads(STRUCTURE.read_text())
    chapter_rows = [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    ]
    chapter_count = len(chapter_rows)
    if status["canonical_chapter_count"] != chapter_count:
        print(
            "P7.1c status validation failed: canonical chapter count "
            f"{status['canonical_chapter_count']} != manifest {chapter_count}"
        )
        return 1
    if status["scope"]["chapters"] != chapter_count:
        print("P7.1c status validation failed: scope chapter count drifted from manifest")
        return 1
    if status["packet_contract"]["required_chapter_packets"] != chapter_count:
        print("P7.1c status validation failed: required packet count drifted from manifest")
        return 1

    packet_schema = json.loads(PACKET_SCHEMA.read_text())
    role_data = json.loads(ROLE_MAP.read_text())
    unit_data = json.loads(UNIT_MAP.read_text())
    chapters = {str(chapter["id"]): chapter for chapter in chapter_rows}
    roles = {
        chapter_id: role
        for role, chapter_ids in role_data.get("roles", {}).items()
        for chapter_id in chapter_ids
    }
    units = {
        chapter_id: str(unit["unit_id"])
        for unit in unit_data.get("units", [])
        for chapter_id in unit.get("chapter_ids", [])
    }
    packet_paths = sorted(PACKET_DIR.glob("*.json"))
    packets = [json.loads(path.read_text()) for path in packet_paths]
    if status["packet_contract"]["current_packets"] != len(packets):
        print("P7.1c status validation failed: current packet count is stale")
        return 1
    passed_packets = sum(packet.get("review_state") == "digest_bound_editorial_pass" for packet in packets)
    if status["packet_contract"]["current_digest_bound_packets"] != passed_packets:
        print("P7.1c status validation failed: digest-bound packet count is stale")
        return 1
    packet_ids = [str(packet.get("chapter_id", "")) for packet in packets]
    if len(packet_ids) != len(set(packet_ids)):
        print("P7.1c status validation failed: duplicate chapter packet")
        return 1
    for path, packet in zip(packet_paths, packets):
        errors = packet_errors(packet, packet_schema, chapters, roles, units)
        if errors:
            for error in errors:
                print(f"P7.1c packet validation failed ({path.name}): {error}")
            return 1

    if packets:
        controls: list[tuple[str, dict[str, Any]]] = []
        stale = copy.deepcopy(packets[0])
        stale["chapter_sha256"] = "0" * 64
        controls.append(("stale digest", stale))
        generic = copy.deepcopy(packets[0])
        generic["concrete_scene"].update({
            "actor_or_system": "A generic example actor",
            "attempted_action": "A system does something in a generic example.",
            "observable_outcome": "An actor takes an action and sees an outcome.",
        })
        controls.append(("generic scene", generic))
        wrong_role = copy.deepcopy(packets[0])
        wrong_role["chapter_role"] = "thesis-bearing"
        controls.append(("wrong role", wrong_role))
        erased_limit = copy.deepcopy(packets[0])
        erased_limit["caveat_consolidation"]["distinct_limitations_preserved"] = False
        controls.append(("erased limitation", erased_limit))
        missing_heading = copy.deepcopy(packets[0])
        missing_heading["worked_trace"]["heading"] = "Worked trace heading that is not in the chapter"
        controls.append(("missing heading", missing_heading))
        for label, mutation in controls:
            if not packet_errors(mutation, packet_schema, chapters, roles, units):
                print(f"P7.1c status validation failed: {label} negative control was accepted")
                return 1
    for path, marker in [
        (ROADMAP, "P7.1c — Reader-first concreteness, prose, and surface discipline"),
        (REVIEW, "# Round 23 reader-prose quality reconciliation"),
        (TRIAGE, "Codex adjudication status: **accepted as calibrated editorial input"),
    ]:
        if not path.exists() or marker not in path.read_text():
            print(f"P7.1c status validation failed: missing marker {marker!r} in {path}")
            return 1
    print(
        "P7.1c reader-prose quality status validation passed: "
        f"{len(packets)}/{chapter_count} digest-bound packets and five rejecting controls"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
