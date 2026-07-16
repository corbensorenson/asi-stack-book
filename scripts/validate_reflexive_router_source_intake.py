#!/usr/bin/env python3
"""Validate the conservative Reflexive Router source intake and roadmap route."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "reflexive_router_whitepaper"
MARKDOWN = ROOT / "sources/raw/reflexive_router/the_reflexive_router_white_paper_v1_2.md"
DOCX = ROOT / "sources/raw/reflexive_router/the_reflexive_router_white_paper_v1_2.docx"
MARKDOWN_DIGEST = "003a693741c40ca96ec3aece5b76ee90ec95a1d6c27ec81a970cff175f509068"
DOCX_DIGEST = "52bc04a1bfedaa0fe3a7e530570703bd973849f46b806529f2534509101ace9b"
NOTE = ROOT / "sources/source_notes/reflexive_router_whitepaper.md"
BACKLOG = ROOT / "research_backlog_records/reflexive_router_whitepaper_2026_07_16.json"
TRIAGE = ROOT / "new_paper_triage_scenarios/reflexive_router_whitepaper_2026_07_16.json"
ROADMAP = ROOT / "docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md"
TARGETS = {
    "routing-heads-and-specialist-cores",
    "intent-to-execution-contracts",
    "planning-as-a-control-layer",
    "stable-capability-fields",
    "virtual-context-abi",
    "context-transactions-snapshots-mounts-and-taint",
    "claim-ledgers-and-belief-revision",
    "runtime-adapters-tool-permissions-and-human-approval",
    "procedural-memory-and-cognitive-loop-closure",
    "resource-economics-and-token-budgets",
    "benchmark-ratchets-and-anti-goodhart-evidence",
    "integrated-reference-architecture",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    for path, digest in [(MARKDOWN, MARKDOWN_DIGEST), (DOCX, DOCX_DIGEST)]:
        if not path.exists():
            errors.append(f"missing local source: {path.relative_to(ROOT)}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"local source digest drifted: {path.relative_to(ROOT)}")

    inventory = load(ROOT / "sources/source_inventory.json")
    rows = [row for row in inventory if row.get("id") == SOURCE_ID]
    if len(rows) != 1:
        errors.append("source inventory must contain exactly one Reflexive Router record")
    else:
        row = rows[0]
        if row.get("priority") != "must_use" or row.get("source_type") != "author_whitepaper":
            errors.append("Reflexive Router inventory classification drifted")
        if set(row.get("chapter_targets", [])) != TARGETS:
            errors.append("Reflexive Router chapter-target set drifted")
        if MARKDOWN_DIGEST not in row.get("url", ""):
            errors.append("Reflexive Router inventory lost the canonical Markdown digest")

    note = NOTE.read_text(encoding="utf-8") if NOTE.exists() else ""
    for phrase in [
        "architectural proposal and research agenda",
        "update existing chapters; do not add a Reflexive Router chapter",
        "bypass inference, never enforcement",
        "ReflexBench-derived",
        "No current chapter support state changes",
    ]:
        if phrase.casefold() not in note.casefold():
            errors.append(f"source note missing boundary: {phrase}")

    backlog = load(BACKLOG)
    backlog_schema = load(ROOT / "schemas/research_backlog_record.schema.json")
    triage = load(TRIAGE)
    triage_schema = load(ROOT / "schemas/new_paper_triage_scenario.schema.json")
    for label, record, schema in [
        ("backlog", backlog, backlog_schema),
        ("triage", triage, triage_schema),
    ]:
        try:
            jsonschema.Draft202012Validator(schema).validate(record)
        except jsonschema.ValidationError as exc:
            errors.append(f"{label} schema: {exc.message}")
    if backlog.get("insertion_decision") != "update_existing_chapter" or backlog.get("support_state_effect") != "argument_only":
        errors.append("backlog must preserve existing-chapter and argument-only boundaries")
    if set(backlog.get("assigned_chapters", [])) != TARGETS:
        errors.append("backlog chapter owners drifted")
    cases = triage.get("cases", [])
    if [case.get("candidate_decision") for case in cases] != ["update_existing_chapter", "defer"]:
        errors.append("triage must retain existing-owner integration and conditional chapter deferral")

    structure = load(ROOT / "book_structure.json")
    chapters = [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]
    assigned = {chapter.get("id") for chapter in chapters if SOURCE_ID in chapter.get("source_ids", [])}
    if assigned != TARGETS:
        errors.append("source is not assigned to exactly the twelve receiving chapter owners")
    if backlog.get("triage_state") != "integrated" or backlog.get("claim_mapping_state") != "complete":
        errors.append("backlog does not record completed argument-only chapter integration")
    if any(chapter.get("id") == "pre-deliberative-reflexive-control-plane" for chapter in chapters):
        errors.append("source intake unexpectedly created the deferred chapter")
    if any(chapter.get("evidence_level") != "argument" for chapter in chapters):
        errors.append("source intake coincides with an unsupported chapter-core promotion")

    roadmap = ROADMAP.read_text(encoding="utf-8")
    for phrase in [
        "Accepted source integration — The Reflexive Router v1.2",
        "fails the new-chapter test",
        "eight separately scored task tracks",
        "observed distinct-interface gate",
    ]:
        if phrase not in roadmap:
            errors.append(f"roadmap missing source-integration obligation: {phrase}")

    if errors:
        print("Reflexive Router source intake validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Reflexive Router source intake passed: two digest-bound local source forms, "
        "one public-safe source note, twelve manifest-assigned existing chapter owners, "
        "one completed argument-only/deferred-chapter decision, roadmap campaign integration, "
        "and no support-state or raw-publication effect."
    )


if __name__ == "__main__":
    main()
