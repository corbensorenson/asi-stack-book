#!/usr/bin/env python3
"""Synchronize generated book structure from `book_structure.json`.

The manifest is the ordering source of truth. `_quarto.yml`, Appendix A, and
Appendix C are generated from it. Chapter files are created only when missing
unless `--rewrite-chapters` is passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-24"

STRUCTURE_PATH = ROOT / "book_structure.json"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"


GLOSSARY = [
    ("ASI stack", "A proposed governed cognitive architecture made of alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and improvement layers."),
    ("Stable Capability Field", "A stable capability boundary with replaceable implementations, bounded authority, qualification evidence, and rollback rules."),
    ("Virtual Context Memory", "A governed memory/context layer that compiles evidence-carrying context packets from durable sources."),
    ("Artifact graph", "A traceable graph of produced objects, source handles, jobs, claims, and evidence records."),
    ("Claim ledger", "A structured record of claims, support states, sources, uncertainty, contradiction links, and review status."),
    ("Context packet", "The active, compiled context supplied to an agent or job, including source handles, summaries, authority labels, and adequacy status."),
    ("Authority ceiling", "The maximum action authority a layer, field, tool, or implementation may exercise."),
    ("Readiness gate", "An evidence and regression checkpoint that must pass before a module or field can be promoted."),
    ("Residual escrow", "A visible backlog of unresolved failures, uncertainty, or residual complexity left by a route, compression, or benchmark result."),
    ("Benchmark ratchet", "A process that uses tests, regressions, hidden checks, and residuals to move capability claims without erasing failure cases."),
]

TEST_SPECS = {
    "Alignment": ["Constitutional consistency", "Value conflict classification", "Self-modification ethics scenario", "Power-seeking / agency-dominance scenario"],
    "SCF": ["Qualification predicates", "Route validity", "Mutation", "Authority non-escalation", "Rollback and recovery"],
    "Planning": ["Decomposition accuracy", "Dependency ordering", "Constraint preservation", "Runtime replanning", "Tool selection", "Budget and risk allocation", "Scope creep prevention"],
    "VCM": ["Context packet adequacy", "Distractor resistance", "Authority label preservation", "Proof-carrying summary fidelity", "Planner-guided prefetch accuracy", "Privacy / behavioral authority checks"],
    "Talos / execution": ["Typed job lifecycle", "Tool permission enforcement", "Audit log reconstruction", "Replay determinism", "Human approval gates", "Adversarial job injection"],
    "Spinoza / verification": ["Claim extraction", "Contradiction detection", "Belief revision", "Evidence tier assignment", "Uncertainty calibration", "Refusal or silence when evidence is insufficient"],
    "Routing / modularity": ["Specialist routing accuracy", "Readiness gate enforcement", "Benchmark promotion", "Quarantine", "Regression preservation", "Residual escrow"],
    "Compression": ["Reconstruction quality", "Residual burden", "Probe-and-route fallback", "Compression ratio", "Latency cost", "Downstream utility preservation"],
    "Benchmark ratchets": ["Saturation detection", "Hidden benchmark transfer", "Regression generation", "Anti-Goodhart checks", "Residual backlog integrity"],
}


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def read_inventory() -> list[dict]:
    records = read_json(SOURCE_INVENTORY)
    if not isinstance(records, list):
        raise TypeError("sources/source_inventory.json must contain a list")
    return records


def read_structure() -> dict:
    structure = read_json(STRUCTURE_PATH)
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    return structure


def inventory_by_id(records: list[dict]) -> dict[str, dict]:
    return {record["id"]: record for record in records}


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part_index, part in enumerate(structure.get("parts", []), start=1):
        for chapter_index, chapter in enumerate(part.get("chapters", []), start=1):
            merged = dict(chapter)
            merged["_part_id"] = part["id"]
            merged["_part_title"] = part["title"]
            merged["_part_index"] = part_index
            merged["_chapter_index_in_part"] = chapter_index
            chapters.append(merged)
    return chapters


def qmd_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def yaml_string(value: object) -> str:
    return json.dumps("" if value is None else str(value))


def yaml_list(items: list[str]) -> str:
    if not items:
        return " []"
    return "\n" + "\n".join(f"  - {yaml_string(item)}" for item in items)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- TBD"


def write_quarto(structure: dict) -> None:
    lines = [
        "# This file is generated by scripts/sync_scaffold.py.",
        "# Edit book_structure.json, then rerun the sync script.",
        "",
        "project:",
        "  type: book",
        "  output-dir: _site",
        "",
        "book:",
        f"  title: {yaml_string(structure.get('title', 'Untitled'))}",
        f"  subtitle: {yaml_string(structure.get('subtitle', ''))}",
        f"  author: {yaml_string(structure.get('author', ''))}",
        f"  site-url: {yaml_string(structure.get('site_url', ''))}",
        f"  repo-url: {yaml_string(structure.get('repo_url', ''))}",
        "  repo-actions: [issue, source]",
        "  chapters:",
    ]
    for item in structure.get("front_matter", []):
        lines.append(f"    - {item}")
    for part in structure.get("parts", []):
        lines.append(f"    - part: {yaml_string(part['title'])}")
        lines.append("      chapters:")
        for chapter in part.get("chapters", []):
            lines.append(f"        - {chapter['file']}")
    lines.append("  appendices:")
    for appendix in structure.get("appendices", []):
        lines.append(f"    - {appendix['file']}")
    lines.extend([
        "",
        "format:",
        "  html:",
        "    toc: true",
        "    number-sections: true",
        "    code-fold: true",
        "    theme: cosmo",
        "    link-external-newwindow: true",
        "  pdf:",
        "    toc: true",
        "    number-sections: true",
        "",
        "execute:",
        "  freeze: auto",
        "",
    ])
    (ROOT / "_quarto.yml").write_text("\n".join(lines), encoding="utf-8")


def source_ids_for(chapter: dict) -> list[str]:
    return list(dict.fromkeys(chapter.get("source_ids", [])))


def write_chapter_stub(chapter: dict, records: list[dict], rewrite: bool = False) -> bool:
    path = ROOT / chapter["file"]
    if path.exists() and not rewrite:
        return False

    by_id = inventory_by_id(records)
    source_ids = [source_id for source_id in source_ids_for(chapter) if source_id in by_id]
    source_label = ", ".join(f"`{source_id}`" for source_id in source_ids) or "None assigned yet"
    gaps = [
        "Assigned source texts have not yet been ingested or summarized.",
        "No Codex tests have been implemented or run.",
        "Chapter prose is a scaffold, not a completed manuscript draft.",
    ]
    crosswalk_rows = []
    for source_id in source_ids:
        source = by_id[source_id]
        crosswalk_rows.append(
            f"| `{source_id}` | {qmd_escape(source['title'])} | Planned use from inventory/manifest: {qmd_escape(source.get('notes', ''))} |"
        )
    if not crosswalk_rows:
        crosswalk_rows.append("| TBD | TBD | No source assigned yet. |")

    tests = chapter.get("codex_tests") or ["TBD"]
    test_rows = "\n".join(f"| {qmd_escape(test)} | Support or falsify this chapter's layer claim. | planned; not run |" for test in tests)
    claim_id = f"{chapter['id']}.core"
    text = f"""---
title: "{chapter['title']}"
chapter_id: "{chapter['id']}"
part_id: "{chapter['_part_id']}"
status: "{chapter.get('status', 'conceptual')}"
last_updated: "{TODAY}"
primary_sources:{yaml_list(source_ids)}
evidence_level: "{chapter.get('evidence_level', 'argument')}"
open_evidence_gaps:{yaml_list(gaps)}
---

# {chapter['title']}

## Chapter status

| Field | Value |
|---|---|
| Chapter ID | `{chapter['id']}` |
| Part | {qmd_escape(chapter['_part_title'])} |
| Status | {qmd_escape(chapter.get('status', 'conceptual'))} |
| Last updated | {TODAY} |
| Primary source records | {source_label} |
| Evidence level | {qmd_escape(chapter.get('evidence_level', 'argument'))} |
| Source ingestion state | Source records assigned; source texts not yet ingested. |
| Test state | Planned only; no tests have been run. |

## Drafting guardrail

This stub is derived from `book_structure.json` and the source inventory only. It does not claim that the listed source documents have been ingested, summarized, or independently verified.

## Problem

{chapter.get('problem', 'TBD.')}

## Why existing approaches are insufficient

{chapter.get('insufficient', 'TBD.')}

## Core claim

[{claim_id}, support: {chapter.get('evidence_level', 'argument')}] {chapter.get('core_claim', 'TBD.')}

## Mechanism

{bullet_list(chapter.get('mechanism', []))}

## Interfaces

{bullet_list(chapter.get('interfaces', []))}

## Invariants

{bullet_list(chapter.get('invariants', []))}

## Failure modes

{bullet_list(chapter.get('failure_modes', []))}

## Minimal implementation

{chapter.get('minimal_implementation', 'TBD.')}

## Codex test plan

| Test | Purpose | Status |
|---|---|---|
{test_rows}

## Source crosswalk

| Source ID | Title | Planned use |
|---|---|---|
{chr(10).join(crosswalk_rows)}

## Summary

This chapter currently establishes the structural slot for this layer of the ASI stack. The next drafting pass should ingest assigned sources, separate source-derived claims from design hypotheses, and update Appendix C when support states change.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def write_chapters(structure: dict, records: list[dict], rewrite: bool = False) -> int:
    written = 0
    for chapter in flatten_chapters(structure):
        if write_chapter_stub(chapter, records, rewrite=rewrite):
            written += 1
    return written


def chapter_assignments(structure: dict) -> dict[str, list[str]]:
    assignments: dict[str, list[str]] = {}
    for chapter in flatten_chapters(structure):
        label = f"{chapter['id']} ({chapter['title']})"
        for source_id in source_ids_for(chapter):
            assignments.setdefault(source_id, []).append(label)
    return assignments


def write_source_matrix(records: list[dict], structure: dict) -> None:
    assignments = chapter_assignments(structure)
    rows = []
    for record in records:
        original_targets = ", ".join(str(target).zfill(2) for target in record.get("chapter_targets", []))
        current_targets = "; ".join(assignments.get(record["id"], [])) or "Unassigned in current structure"
        rows.append(
            "| `{id}` | {title} | `{priority}` | `{layer}` | {current_targets} | {original_targets} | [source]({url}) | inventory-recorded; text not ingested | {notes} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                priority=qmd_escape(record.get("priority", "")),
                layer=qmd_escape(record.get("layer", "")),
                current_targets=qmd_escape(current_targets),
                original_targets=qmd_escape(original_targets),
                url=qmd_escape(record.get("url", "")),
                notes=qmd_escape(record.get("notes", "")),
            )
        )
    text = f"""# Source Matrix

This matrix is generated from `sources/source_inventory.json` and dynamic chapter assignments in `book_structure.json`.

Source text status is deliberately conservative: the records are inventoried, but the source documents themselves have not yet been exported, ingested, summarized, or verified in this repository.

| ID | Title | Priority | Layer | Current dynamic assignments | Original packet targets | URL | Current status | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""
    (ROOT / "appendices" / "A_source_matrix.qmd").write_text(text, encoding="utf-8")


def write_claim_matrix(structure: dict) -> None:
    rows = []
    for chapter in flatten_chapters(structure):
        source_label = ", ".join(f"`{source_id}`" for source_id in source_ids_for(chapter)) or "TBD"
        claim_id = f"{chapter['id']}.core"
        rows.append(
            f"| `{claim_id}` | `{chapter['id']}` | {qmd_escape(chapter.get('core_claim', 'TBD'))} | {qmd_escape(chapter.get('evidence_level', 'argument'))} | {source_label} | Outline-level architecture claim only. | Ingest sources; define and run tests before raising support state. |"
        )
    text = f"""# Claim/Evidence Matrix

This initial matrix contains one core placeholder claim per dynamic chapter.

No claim is marked `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` yet. Those labels require source ingestion, prototype inspection, or actual test execution.

| Claim ID | Chapter ID | Claim | Current support state | Assigned sources | Current evidence | Open gap |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Support States

| State | Meaning |
|---|---|
| unsupported | Not yet supported; likely remove or mark as speculative. |
| argument | Supported by reasoning only. |
| source-derived | Derived from supplied source papers. |
| prototype-backed | Implemented in a prototype but not robustly tested. |
| synthetic-test-backed | Supported by controlled synthetic tests. |
| empirical-test-backed | Supported by external or realistic tests. |
| external-literature-backed | Supported by third-party literature. |
"""
    (ROOT / "appendices" / "C_claim_evidence_matrix.qmd").write_text(text, encoding="utf-8")


def ensure_glossary() -> None:
    path = ROOT / "appendices" / "B_glossary.qmd"
    if path.exists():
        return
    rows = "\n".join(f"| {qmd_escape(term)} | {qmd_escape(definition)} | initial; refine after source ingestion |" for term, definition in GLOSSARY)
    path.write_text(f"# Glossary\n\n| Term | Working definition | Status |\n|---|---|---|\n{rows}\n", encoding="utf-8")


def ensure_protocol_schemas() -> None:
    path = ROOT / "appendices" / "D_protocol_schemas.qmd"
    if path.exists():
        return
    path.write_text("# Protocol Schemas\n\nDraft protocol schema placeholders go here.\n", encoding="utf-8")


def ensure_test_specs() -> None:
    path = ROOT / "appendices" / "E_codex_test_specs.qmd"
    if path.exists():
        return
    rows = []
    for layer, tests in TEST_SPECS.items():
        for test in tests:
            rows.append(f"| {qmd_escape(layer)} | {qmd_escape(test)} | planned | not run |")
    path.write_text(
        f"# Codex Test Specs\n\nNo result is recorded here unless a test has actually been implemented and run.\n\n| Layer | Test spec | Implementation status | Result status |\n|---|---|---|---|\n{chr(10).join(rows)}\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rewrite-chapters", action="store_true", help="Rewrite chapter stubs from book_structure.json.")
    args = parser.parse_args()

    records = read_inventory()
    structure = read_structure()
    write_quarto(structure)
    written = write_chapters(structure, records, rewrite=args.rewrite_chapters)
    write_source_matrix(records, structure)
    write_claim_matrix(structure)
    ensure_glossary()
    ensure_protocol_schemas()
    ensure_test_specs()
    print(f"Synchronized book structure: {len(flatten_chapters(structure))} chapters, {written} chapter files written.")


if __name__ == "__main__":
    main()
