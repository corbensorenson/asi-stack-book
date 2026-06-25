#!/usr/bin/env python3
"""Synchronize generated book structure from `book_structure.json`.

The manifest is the ordering source of truth. `_quarto.yml`, Appendix A, and
Appendix C are generated from it. Chapter files are created only when missing
unless `--rewrite-chapters` is passed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-24"

STRUCTURE_PATH = ROOT / "book_structure.json"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"
SOURCE_NOTES = ROOT / "sources" / "source_notes"
CONNECTOR_READINESS = ROOT / "sources" / "connector_readiness.json"
CACHE_MANIFEST = ROOT / "sources" / "cache" / "cache_manifest.json"
PROOF_TRIAGE = ROOT / "proofs" / "proof_triage.json"


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

CLAIM_LABELS = [
    ("Demonstrated", "Shown by a recorded artifact, derivation, implementation, or source-backed example in scope."),
    ("Measured", "Quantified by a recorded measurement or benchmark result."),
    ("Mechanized", "Expressed as runnable code, an executable schema, or a formal proof target."),
    ("Hypothesized", "Proposed as a testable claim that still needs evidence."),
    ("Design rationale", "An architectural choice supported by reasoning and constraints."),
    ("Speculative", "Exploratory or conjectural; do not use as a deployed system guarantee."),
]

SUPPORT_STATES = [
    ("unsupported", "Not yet supported; likely remove or mark as speculative."),
    ("argument", "Supported by reasoning only."),
    ("source-derived", "Derived from supplied source papers."),
    ("prototype-backed", "Implemented in a prototype but not robustly tested."),
    ("synthetic-test-backed", "Supported by controlled synthetic tests."),
    ("empirical-test-backed", "Supported by external or realistic tests."),
    ("external-literature-backed", "Supported by third-party literature."),
    ("deprecated", "Superseded, merged, or retired; retained for lineage and review."),
    ("refuted", "Contradicted by later evidence or tests; retained to preserve negative results."),
]


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def read_inventory() -> list[dict]:
    records = read_json(SOURCE_INVENTORY)
    if not isinstance(records, list):
        raise TypeError("sources/source_inventory.json must contain a list")
    return records


def read_optional_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    return read_json(path)


def read_connector_records() -> dict[str, dict]:
    data = read_optional_json(CONNECTOR_READINESS, {"records": {}})
    if not isinstance(data, dict):
        return {}
    records = data.get("records", {})
    return records if isinstance(records, dict) else {}


def read_cache_records() -> dict[str, dict]:
    data = read_optional_json(CACHE_MANIFEST, {"records": []})
    if not isinstance(data, dict):
        return {}
    records = data.get("records", [])
    if not isinstance(records, list):
        return {}
    return {str(record.get("id", "")): record for record in records if isinstance(record, dict)}


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


def test_name(test: object) -> str:
    if isinstance(test, dict):
        return str(test.get("name", "Unnamed test"))
    return str(test)


def test_purpose_text(test: object, chapter: dict) -> str:
    if isinstance(test, dict) and test.get("purpose"):
        return str(test["purpose"])
    return scaffold_test_purpose(test_name(test), chapter)


def test_status_summary(test: object) -> str:
    if isinstance(test, dict):
        return str(test.get("status", "planned; not run"))
    return "planned; not run"


def test_implementation_status(test: object) -> str:
    if isinstance(test, dict):
        return str(test.get("implementation_status", "planned"))
    return "planned"


def test_result_status(test: object) -> str:
    if isinstance(test, dict):
        return str(test.get("result_status", "not run"))
    return "not run"


def yaml_string(value: object) -> str:
    return json.dumps("" if value is None else str(value))


def yaml_list(items: list[str]) -> str:
    if not items:
        return " []"
    return "\n" + "\n".join(f"  - {yaml_string(item)}" for item in items)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- No manifest items declared yet."


def scaffold_test_purpose(test: str, chapter: dict) -> str:
    name = test.lower()
    if "validation" in name or "schema" in name or "fixture" in name:
        return "Validate the declared record shape without promoting the chapter claim."
    if "authority" in name or "approval" in name or "permission" in name:
        return "Check that execution cannot exceed the declared authority, approval, or permission boundary."
    if "proof" in name or "theorem" in name:
        return "Check that formal references resolve before any proof-backed claim is promoted."
    if "benchmark" in name or "quality" in name or "regression" in name:
        return "Check the claim against declared baselines, metrics, contamination notes, and negative-result handling."
    return f"Check the {chapter['title']} boundary against the named acceptance condition and record any missing artifact or failed predicate."


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
        "    theme:",
        "      - cosmo",
        "      - assets/styles.scss",
        "    link-external-newwindow: true",
        "",
        "execute:",
        "  freeze: auto",
        "",
    ])
    (ROOT / "_quarto.yml").write_text("\n".join(lines), encoding="utf-8")


def source_ids_for(chapter: dict) -> list[str]:
    return list(dict.fromkeys(chapter.get("source_ids", [])))


def claim_source_mapping_text(chapter: dict) -> str:
    mappings = chapter.get("claim_source_mappings", [])
    if not mappings:
        return "No exact claim-level source-note mapping recorded yet."
    parts = []
    for mapping in mappings:
        source_id = mapping.get("source_id", "")
        support = mapping.get("mapped_support", "")
        limits = mapping.get("limits", "")
        parts.append(f"`{source_id}`: {support} Limits: {limits}")
    return "; ".join(parts)


def write_chapter_stub(chapter: dict, records: list[dict], rewrite: bool = False) -> bool:
    path = ROOT / chapter["file"]
    if path.exists() and not rewrite:
        return False

    by_id = inventory_by_id(records)
    source_ids = [source_id for source_id in source_ids_for(chapter) if source_id in by_id]
    source_label = ", ".join(f"`{source_id}`" for source_id in source_ids) or "None assigned yet"
    gaps = [
        "Chapter is a generated starting point; source-note coverage and claim-level mapping must be checked before support-state promotion.",
        "No chapter-level Codex tests have been implemented or run unless separately recorded in Appendix E.",
        "No support-state promotion is implied by this generated chapter.",
    ]
    crosswalk_rows = []
    for source_id in source_ids:
        source = by_id[source_id]
        crosswalk_rows.append(
            f"| `{source_id}` | {qmd_escape(source['title'])} | Planned use from inventory/manifest: {qmd_escape(source.get('notes', ''))} |"
        )
    if not crosswalk_rows:
        crosswalk_rows.append("| None assigned yet | None assigned yet | Add source records before using this chapter for source-derived claims. |")

    tests = chapter.get("codex_tests") or ["No chapter-level test declared yet"]
    test_rows = "\n".join(
        f"| {qmd_escape(test_name(test))} | {qmd_escape(test_purpose_text(test, chapter))} | {qmd_escape(test_status_summary(test))} |"
        for test in tests
    )
    claim_id = f"{chapter['id']}.core"
    text = f"""---
title: "{chapter['title']}"
chapter_id: "{chapter['id']}"
part_id: "{chapter['_part_id']}"
status: "{chapter.get('status', 'conceptual')}"
draft_maturity: "generated starting point"
last_updated: "{TODAY}"
primary_sources:{yaml_list(source_ids)}
evidence_level: "{chapter.get('evidence_level', 'argument')}"
claim_label: "{chapter.get('claim_label', 'Design rationale')}"
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
| Claim label | {qmd_escape(chapter.get('claim_label', 'Design rationale'))} |
| Evidence level | {qmd_escape(chapter.get('evidence_level', 'argument'))} |
| Source loading state | Source records assigned; source notes and raw-cache readiness must be checked before support-state promotion. |
| Test state | Chapter-level tests remain planned unless Appendix E records an implemented command and result. |

## Drafting guardrail

This generated chapter is derived from `book_structure.json` and the source inventory only. It does not claim that the listed source documents have been ingested, summarized, or independently verified. Run `python3 scripts/draft_v02_from_manifest.py` only when intentionally regenerating the full v0.2 manuscript baseline.

## Problem

{chapter.get('problem', 'No manifest problem statement declared yet.')}

## Why existing approaches are insufficient

{chapter.get('insufficient', 'No manifest insufficiency statement declared yet.')}

## Core Claim

[{claim_id}, label: {chapter.get('claim_label', 'Design rationale')}, support: {chapter.get('evidence_level', 'argument')}] {chapter.get('core_claim', 'No manifest core claim declared yet.')}

## Mechanism

{bullet_list(chapter.get('mechanism', []))}

## Interfaces

{bullet_list(chapter.get('interfaces', []))}

## Invariants

{bullet_list(chapter.get('invariants', []))}

## Failure modes

{bullet_list(chapter.get('failure_modes', []))}

## Minimal implementation

{chapter.get('minimal_implementation', 'No manifest minimal implementation statement declared yet.')}

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


def source_status(record: dict, connector_records: dict[str, dict], cache_records: dict[str, dict]) -> str:
    source_id = str(record.get("id", ""))
    has_note = (SOURCE_NOTES / f"{source_id}.md").exists()
    connector = source_id in connector_records
    cache_status = str(cache_records.get(source_id, {}).get("status", ""))
    url = str(record.get("url", ""))

    if has_note and connector:
        return "source note available; connector-readable; raw text not published"
    if has_note:
        return "source note available; raw/cache text not published"
    if connector:
        return "connector-readable; source note pending"
    if "github.com/" in url:
        return "public project source; source note pending"
    if cache_status == "cached_existing":
        return "local raw cache available; source note pending"
    if cache_status == "connector_required":
        return "connector required; source note pending"
    return "inventory-recorded; source note pending"


def bibliography_status(record: dict, connector_records: dict[str, dict], cache_records: dict[str, dict]) -> str:
    status = source_status(record, connector_records, cache_records)
    if record.get("citation_label") and record.get("arxiv_id"):
        if status.startswith("source note available"):
            return "source note available; citation metadata recorded from primary arXiv record"
        return f"{status}; citation metadata recorded from primary arXiv record"
    if status.startswith("source note available"):
        return "source note available; citation not normalized"
    return f"{status}; citation not normalized"


def external_citation_rows(records: list[dict], structure: dict) -> list[str]:
    assignments = chapter_assignments(structure)
    rows = []
    for record in records:
        if record.get("priority") != "external_literature":
            continue
        citation = record.get("citation_label")
        arxiv_id = record.get("arxiv_id")
        if not citation or not arxiv_id:
            continue
        current_targets = "; ".join(assignments.get(record["id"], [])) or "Unassigned in current structure"
        doi = record.get("doi", "")
        link = f"[arXiv:{qmd_escape(arxiv_id)}]({qmd_escape(record.get('url', ''))})"
        if doi:
            link = f"{link}; DOI `{qmd_escape(doi)}`"
        note_status = "source note available" if (SOURCE_NOTES / f"{record['id']}.md").exists() else "source note pending"
        rows.append(
            "| `{id}` | {citation} | {link} | {targets} | {note_status} |".format(
                id=qmd_escape(record.get("id", "")),
                citation=qmd_escape(citation),
                link=link,
                targets=qmd_escape(current_targets),
                note_status=qmd_escape(note_status),
            )
        )
    return rows


def write_source_matrix(records: list[dict], structure: dict) -> None:
    assignments = chapter_assignments(structure)
    connector_records = read_connector_records()
    cache_records = read_cache_records()
    rows = []
    for record in records:
        original_targets = ", ".join(str(target).zfill(2) for target in record.get("chapter_targets", []))
        current_targets = "; ".join(assignments.get(record["id"], [])) or "Unassigned in current structure"
        status = source_status(record, connector_records, cache_records)
        rows.append(
            "| `{id}` | {title} | `{priority}` | `{layer}` | {current_targets} | {original_targets} | [source]({url}) | {status} | {notes} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                priority=qmd_escape(record.get("priority", "")),
                layer=qmd_escape(record.get("layer", "")),
                current_targets=qmd_escape(current_targets),
                original_targets=qmd_escape(original_targets),
                url=qmd_escape(record.get("url", "")),
                status=qmd_escape(status),
                notes=qmd_escape(record.get("notes", "")),
            )
        )
    text = f"""# Source Matrix

This matrix is generated from `sources/source_inventory.json` and dynamic chapter assignments in `book_structure.json`.

Source status is deliberately conservative. A source note means the source has been mined for drafting context; it does not by itself promote any chapter claim above `argument`.

| ID | Title | Priority | Layer | Current dynamic assignments | Original packet targets | URL | Current status | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""
    (ROOT / "appendices" / "A_source_matrix.qmd").write_text(text, encoding="utf-8")


def write_bibliography(records: list[dict], structure: dict) -> None:
    assignments = chapter_assignments(structure)
    connector_records = read_connector_records()
    cache_records = read_cache_records()
    rows = []
    for record in records:
        current_targets = "; ".join(assignments.get(record["id"], [])) or "Unassigned in current structure"
        status = bibliography_status(record, connector_records, cache_records)
        rows.append(
            "| `{id}` | {title} | `{priority}` | `{layer}` | [source]({url}) | {current_targets} | {status} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                priority=qmd_escape(record.get("priority", "")),
                layer=qmd_escape(record.get("layer", "")),
                url=qmd_escape(record.get("url", "")),
                current_targets=qmd_escape(current_targets),
                status=qmd_escape(status),
            )
        )
    external_rows = external_citation_rows(records, structure)
    external_section = ""
    if external_rows:
        external_section = f"""
## Source-Noted External Literature Records

These records have stable source IDs and primary arXiv metadata. This section does not claim reproduced experiments, local benchmark results, or support-state promotion.

| Source ID | Citation label | Primary record | Current use | Source-note state |
|---|---|---|---|---|
{chr(10).join(external_rows)}
"""
    text = f"""# Bibliography and Source Corpus

This appendix is generated from `sources/source_inventory.json` and current chapter assignments in `book_structure.json`.

It is a working bibliography for the supplied ASI Stack source corpus. It is not a claim that every source has been ingested, summarized, citation-normalized, or independently verified. Source-derived claims should not be promoted until the relevant source has a source note and Appendix C has been updated.

## Primary ASI Stack Source Corpus

| Source ID | Title | Priority | Layer | Link | Current use | Bibliographic status |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}
{external_section}

## External Literature Queue

Third-party references should be added only when bibliographic metadata is recorded and the source is actually used.

| Area | Expected role | Status |
|---|---|---|
| AI alignment and corrigibility | External comparison for the alignment and constitution layer. | queued; no citation recorded |
| AI governance, evals, and deployment policy | External comparison for authority ceilings, readiness gates, and release governance. | queued; no citation recorded |
| Planning, task decomposition, and agent control | External comparison for PlanForge-style planning/control. | queued; no citation recorded |
| Retrieval, memory, and context engineering | External comparison for VCM and context-packet discipline. | queued; no citation recorded |
| Formal methods, verification, and proof assistants | External comparison for claim ledgers, Lean proofs, and protocol invariants. | queued; no citation recorded |
| Modular systems, routing, and mixture-of-experts | External comparison for routing and specialist promotion. | queued; no citation recorded |
| Compression, representation learning, and program synthesis | External comparison for compact generative systems and residual accounting. | queued; no citation recorded |
| Fast generation, decoding substrates, and serving acceleration | External comparison for MTP, speculative decoding, internal draft heads, diffusion LLMs, early exit, state-space alternatives, KV-cache memory, and useful-solution-per-second metrics. | initial source records and source notes added; no local reproduction or support-state promotion |
| Policy optimization and learning from feedback | External comparison for PPO/RLHF, GRPO/RLVR, DPO-style preference optimization, verifier rewards, reward hacking, reasoning-budget RL, and control-policy RL for planners, routers, VCM, execution, and generation modes. | initial source records and source notes added; no local reproduction or support-state promotion |
| Benchmarks, evaluation science, and anti-Goodhart methods | External comparison for evidence ratchets and regression preservation. | queued; no citation recorded |

## Citation Policy

- Use stable source IDs for supplied corpus references until full citation metadata exists.
- Do not infer authors, dates, venues, versions, or publication status from titles alone.
- Do not cite a source as supporting a claim until its text has been ingested and a source note exists.
- Keep speculative or design-synthesis claims labeled as `argument` until source, prototype, or test evidence justifies promotion.
"""
    (ROOT / "appendices" / "G_bibliography.qmd").write_text(text, encoding="utf-8")


def write_claim_matrix(structure: dict) -> None:
    source_note_texts = {
        path.stem: path.read_text(encoding="utf-8")
        for path in SOURCE_NOTES.glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    source_note_ids = set(source_note_texts)
    rows = []
    for chapter in flatten_chapters(structure):
        chapter_source_ids = source_ids_for(chapter)
        source_label = ", ".join(f"`{source_id}`" for source_id in chapter_source_ids) or "None assigned yet"
        noted_sources = [source_id for source_id in chapter_source_ids if source_id in source_note_ids]
        missing_notes = [source_id for source_id in chapter_source_ids if source_id not in source_note_ids]
        chapter_mapped_sources = [
            source_id
            for source_id in noted_sources
            if f"`{chapter['id']}`" in source_note_texts.get(source_id, "")
            or chapter["id"] in source_note_texts.get(source_id, "")
            or chapter["title"] in source_note_texts.get(source_id, "")
        ]
        if not chapter_source_ids:
            current_evidence = "No assigned source records yet."
            source_mapping = "No chapter-level source-note mapping yet."
            open_gap = "Assign source records, create source notes, then map exact claim support before raising support state."
        elif missing_notes:
            current_evidence = (
                "Partial source-note coverage: "
                f"{len(noted_sources)} of {len(chapter_source_ids)} assigned sources have notes; "
                f"missing notes for {', '.join(f'`{source_id}`' for source_id in missing_notes)}."
            )
            source_mapping = (
                f"{len(chapter_mapped_sources)} of {len(chapter_source_ids)} assigned sources explicitly list this chapter in their source notes; "
                f"missing source notes for {', '.join(f'`{source_id}`' for source_id in missing_notes)}."
            )
            open_gap = "Create missing source notes, then map exact claim support and tests before raising support state."
        else:
            claim_mappings = chapter.get("claim_source_mappings", [])
            current_evidence = (
                f"Source notes available for all {len(chapter_source_ids)} assigned sources; "
                + (
                    f"{len(claim_mappings)} exact claim-level source-note mappings recorded; "
                    if claim_mappings
                    else ""
                )
                + "support remains at the recorded state until an accepted evidence transition, proof, test, or source-derived promotion justifies movement."
            )
            if len(chapter_mapped_sources) == len(chapter_source_ids):
                source_mapping = (
                    f"All {len(chapter_source_ids)} assigned source notes explicitly list this chapter; "
                    "mapping remains chapter-level, not claim-level support."
                )
            else:
                missing_mapping = [
                    source_id for source_id in chapter_source_ids if source_id not in chapter_mapped_sources
                ]
                source_mapping = (
                    f"{len(chapter_mapped_sources)} of {len(chapter_source_ids)} assigned source notes explicitly list this chapter; "
                    f"chapter-listing gap for {', '.join(f'`{source_id}`' for source_id in missing_mapping)}."
                )
            if claim_mappings:
                open_gap = "Review the mapped source-note support against source passages, evidence transitions, and tests before raising support state."
            else:
                open_gap = "Map the exact claim text to specific source-note mechanisms/evidence and define or run tests before raising support state."
        claim_id = f"{chapter['id']}.core"
        claim_label = chapter.get("claim_label", "Design rationale")
        claim_mapping = claim_source_mapping_text(chapter)
        rows.append(
            f"| `{claim_id}` | `{chapter['id']}` | {qmd_escape(chapter.get('core_claim', 'No manifest core claim declared.'))} | {qmd_escape(claim_label)} | {qmd_escape(chapter.get('evidence_level', 'argument'))} | {source_label} | {qmd_escape(current_evidence)} | {qmd_escape(source_mapping)} | {qmd_escape(claim_mapping)} | {qmd_escape(open_gap)} |"
        )
    label_rows = "\n".join(f"| {qmd_escape(label)} | {qmd_escape(meaning)} |" for label, meaning in CLAIM_LABELS)
    support_rows = "\n".join(f"| {qmd_escape(state)} | {qmd_escape(meaning)} |" for state, meaning in SUPPORT_STATES)
    text = f"""# Claim/Evidence Matrix

This matrix contains one core claim per dynamic chapter and records the conservative evidence state used by the current manuscript.

Each claim has two separate classifications: a claim label that describes what kind of statement it is, and a support state that describes what currently supports it.

No claim is marked `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` yet. A source note means the source has been mined for drafting context; it does not by itself promote the claim.

| Claim ID | Chapter ID | Claim | Claim label | Current support state | Assigned sources | Current evidence | Source-note chapter mapping | Claim-source mapping | Open gap |
|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Claim Labels

| Label | Meaning |
|---|---|
{label_rows}

## Support States

| State | Meaning |
|---|---|
{support_rows}
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
    path.write_text(
        "# Protocol Schemas\n\nProtocol schema records are added here when concrete schema files exist under `schemas/`.\n",
        encoding="utf-8",
    )


def proof_target_coverage_markdown() -> str:
    if not PROOF_TRIAGE.exists():
        return (
            "## Proof Target Coverage Audit\n\n"
            "`proofs/proof_triage.json` is not present, so no generated proof-target coverage summary is available.\n"
        )

    data = read_json(PROOF_TRIAGE)
    if not isinstance(data, dict):
        raise TypeError("proofs/proof_triage.json must contain an object")
    records = data.get("records", [])
    if not isinstance(records, list):
        raise TypeError("proofs/proof_triage.json records must contain a list")
    proof_records = [record for record in records if isinstance(record, dict)]

    status_counts = Counter(str(record.get("target_status", "missing")) for record in proof_records)
    triage_counts = Counter(
        (
            str(record.get("target_status", "missing")),
            str(record.get("triage", "missing")),
            str(record.get("recommended_route", "missing")),
        )
        for record in proof_records
    )

    status_rows = "\n".join(
        f"| {qmd_escape(status)} | {count} |" for status, count in sorted(status_counts.items())
    )
    triage_rows = "\n".join(
        f"| {qmd_escape(status)} | {qmd_escape(triage)} | {qmd_escape(route)} | {count} |"
        for (status, triage, route), count in sorted(triage_counts.items())
    )

    return f"""## Proof Target Coverage Audit

This section is generated from `proofs/proof_triage.json`. It records coverage and routing state only: it does not prove broad chapter claims, source interpretation, model quality, deployed enforcement, or benchmark performance.

`python3 scripts/validate_proof_readiness.py` checks that these triage records stay aligned with `proofs/proof_manifest.json`, imported Lean modules, and implemented target statuses.

| Metric | Count |
|---|---:|
| Proof targets covered by triage | {len(proof_records)} |

### Coverage by Status

| Target status | Count |
|---|---:|
{status_rows}

### Coverage by Route

| Target status | Triage class | Recommended route | Count |
|---|---|---|---:|
{triage_rows}
"""


def write_test_specs(structure: dict) -> None:
    path = ROOT / "appendices" / "E_codex_test_specs.qmd"
    rows = []
    for chapter in flatten_chapters(structure):
        tests = chapter.get("codex_tests") or []
        if not tests:
            rows.append(
                f"| `{chapter['id']}` | {qmd_escape(chapter['title'])} | No chapter-level test declared yet | planned | not run |"
            )
            continue
        for test in tests:
            rows.append(
                f"| `{chapter['id']}` | {qmd_escape(chapter['title'])} | {qmd_escape(test_name(test))} | {qmd_escape(test_implementation_status(test))} | {qmd_escape(test_result_status(test))} |"
            )
    proof_coverage = proof_target_coverage_markdown()
    body = f"""# Codex Test Specs

This appendix is generated from chapter-level `codex_tests` in `book_structure.json`.

No result is recorded here unless a test has actually been implemented and run.

| Chapter ID | Chapter | Test spec | Implementation status | Result status |
|---|---|---|---|---|
{chr(10).join(rows)}

## Repository-Level Implemented Checks

| Check | Command | Scope | Result policy |
|---|---|---|---|
| Protocol schema and release-record validation | `python3 scripts/validate_protocol_examples.py` | Validates example records in `tests/fixtures/protocol_records/` and public release records in `release_records/` against matching schemas in `schemas/`. | Passing this check proves fixture/release-record schema consistency only; it does not promote chapter claims or replace the chapter-level tests above. |
| Proof-readiness validation | `python3 scripts/validate_proof_readiness.py` | Checks that proof triage tags, modules, root imports, formal targets, and target statuses stay aligned with the generated proof manifest. | Passing this check proves manifest/triage/import consistency only; theorem status still requires implemented Lean modules and a passing Lean build. |
| Proof artifact traceability audit | `python3 scripts/validate_proof_artifact_audit.py` | Checks that implemented proof targets are traceable from manifest and triage to Lean modules, root imports, chapter hooks, limitation prose, and Appendix E coverage. | Passing this check proves traceability and explicit non-claim coverage only; it does not prove semantic adequacy, source interpretation, deployed enforcement, or benchmark performance. |
| Proof target coverage summary | Generated by `python3 scripts/sync_scaffold.py` from `proofs/proof_triage.json`; checked by `python3 scripts/validate_proof_readiness.py`. | Publishes the current count of proof targets by status, triage class, and recommended route. | Passing the validator proves coverage/accounting consistency only; it does not prove broad chapter claims, source interpretation, model quality, deployed enforcement, or benchmark performance. |
| Repeated prose validation | `python3 scripts/validate_repeated_prose.py` | Checks chapter files for exact repeated long prose paragraphs that indicate template-shaped drafting. | Passing this check proves only that exact repeated long paragraphs are absent; it is not a full editorial review. |
| Visual coverage validation | `python3 scripts/validate_visual_coverage.py` | Checks that every chapter has at least one Mermaid diagram and that the landing page references the hero image asset. | Passing this check proves visual coverage only; it does not prove the diagrams are complete or promote chapter claims. |

{proof_coverage.rstrip()}
"""
    path.write_text(body, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rewrite-chapters", action="store_true", help="Rewrite chapter stubs from book_structure.json.")
    args = parser.parse_args()

    records = read_inventory()
    structure = read_structure()
    write_quarto(structure)
    written = write_chapters(structure, records, rewrite=args.rewrite_chapters)
    write_source_matrix(records, structure)
    write_bibliography(records, structure)
    write_claim_matrix(structure)
    ensure_glossary()
    ensure_protocol_schemas()
    write_test_specs(structure)
    print(f"Synchronized book structure: {len(flatten_chapters(structure))} chapters, {written} chapter files written.")


if __name__ == "__main__":
    main()
