#!/usr/bin/env python3
"""Synchronize generated book structure from `book_structure.json`.

The manifest is the ordering source of truth. `_quarto.yml` and generated
appendices are derived from it. Chapter files are created only when missing
unless `--rewrite-chapters` is passed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from sync_chapter_source_crosswalks import synchronize_chapter_source_crosswalks
from sync_outline_source_queues import synchronize_outline_source_queues
from sync_public_trust_metrics import sync_public_trust_metrics

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-24"

STRUCTURE_PATH = ROOT / "book_structure.json"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"
SOURCE_NOTES = ROOT / "sources" / "source_notes"
CONNECTOR_READINESS = ROOT / "sources" / "connector_readiness.json"
CACHE_MANIFEST = ROOT / "sources" / "cache" / "cache_manifest.json"
PROOF_TRIAGE = ROOT / "proofs" / "proof_triage.json"
PER_CHAPTER_EVIDENCE_PLAN = ROOT / "docs" / "per_chapter_evidence_plan.md"


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
    ("Training Run Transaction", "A prospectively frozen, identity-bound record joining architecture, data order, objective, optimizer, numerical and topology policy, execution failures, full checkpoint state, resume evidence, checkpoint-family selection, and independent qualification handoff."),
    ("Resume equivalence class", "The prospectively declared strength of a checkpoint-continuation claim: bitwise, operation-order-bounded, or statistical, each with its own comparison and inference ceiling."),
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


def read_core_claim_promotion_paths() -> dict[str, str]:
    """Read Appendix C promotion criteria from the per-chapter evidence plan."""
    paths: dict[str, str] = {}
    if not PER_CHAPTER_EVIDENCE_PLAN.exists():
        return paths
    for line in PER_CHAPTER_EVIDENCE_PLAN.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 6:
            continue
        chapter_cell = cells[1]
        if not (chapter_cell.startswith("`") and chapter_cell.endswith("`")):
            continue
        chapter_id = chapter_cell.strip("`")
        acceptance_bar = cells[5]
        if chapter_id and acceptance_bar and chapter_id not in {"Chapter"}:
            paths[chapter_id] = acceptance_bar
    return paths


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


HISTORICAL_CHAPTER_STUBS = (
    "chapters/agency-dignity-and-corrigibility.html",
    "chapters/governance-rights-fork-exit-and-audit.html",
    "chapters/generate-verify-repair-compression.html",
    "chapters/command-contracts-and-semantic-interfaces.html",
    "chapters/moecot-runtime-and-multi-core-orchestration.html",
    "chapters/simulation-fidelity-and-physical-constraints.html",
    "chapters/semantic-pages-context-cells-and-certificates.html",
    "chapters/unified-adaptive-tribunal-and-adversarial-review.html",
    "chapters/planforge-dags-and-intelligence-arbitrage.html",
    "chapters/semantic-representation-and-tree-structured-models.html",
)

GENERATED_HTML_RESOURCE_EXCLUSIONS = (
    "!chapters/*.html",
    "!appendices/*.html",
)


def write_quarto(structure: dict) -> None:
    lines = [
        "# This file is generated by scripts/sync_scaffold.py.",
        "# Edit book_structure.json, then rerun the sync script.",
        "",
        "project:",
        "  type: book",
        "  output-dir: _site",
        "  resources:",
        "",
        "lang: en-US",
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
    resource_index = lines.index("  resources:") + 1
    for exclusion in GENERATED_HTML_RESOURCE_EXCLUSIONS:
        lines.insert(resource_index, f"    - {yaml_string(exclusion)}")
        resource_index += 1
    for stub in HISTORICAL_CHAPTER_STUBS:
        lines.insert(resource_index, f"    - {stub}")
        resource_index += 1
    render_files = list(structure.get("front_matter", []))
    for part in structure.get("parts", []):
        render_files.extend(chapter["file"] for chapter in part.get("chapters", []))
    render_files.extend(appendix["file"] for appendix in structure.get("appendices", []))
    lines.insert(resource_index, "  render:")
    resource_index += 1
    for render_file in render_files:
        lines.insert(resource_index, f"    - {render_file}")
        resource_index += 1
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
        "    include-before-body:",
        "      - assets/skip-link.html",
        "    include-after-body:",
        "      - assets/reader-overlays.html",
        "      - assets/reading-mode.html",
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

## Minimum Viable Implementation

{chapter.get('minimal_implementation', 'No manifest minimal implementation statement declared yet.')}

## Beyond the State of the Art

{chapter.get('beyond_state_of_art', 'No manifest beyond-state-of-the-art statement declared yet.')}

Treat this endpoint as a target architecture, not a current result. It remains bounded by the support state recorded above until the necessary source mappings, schemas, proofs, tests, runtime traces, review artifacts, or governance records exist.

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


def is_external_literature(record: dict) -> bool:
    return record.get("priority") == "external_literature"


def public_source_ref(record: dict, label: str = "source") -> str:
    """Render public links while keeping local project locators non-clickable."""
    url = str(record.get("url", ""))
    if url.startswith("local-project:"):
        return "local project reference (not publicly linked)"
    if url.startswith("local-source:"):
        return "local source reference (not publicly linked)"
    return f"[{label}]({qmd_escape(url)})"


def external_literature_rows(records: list[dict], structure: dict) -> list[str]:
    assignments = chapter_assignments(structure)
    chapter_titles = {
        chapter["id"]: chapter["title"]
        for chapter in flatten_chapters(structure)
        if chapter.get("id") and chapter.get("title")
    }
    rows = []
    for record in records:
        if not is_external_literature(record):
            continue
        citation = record.get("citation_label")
        arxiv_id = record.get("arxiv_id")
        current_targets = "; ".join(assignments.get(record["id"], []))
        if not current_targets:
            target_labels = []
            for target in record.get("chapter_targets", []):
                if target in chapter_titles:
                    target_labels.append(f"{target} ({chapter_titles[target]})")
                elif target:
                    target_labels.append(str(target))
            if target_labels:
                current_targets = "; ".join(target_labels) + " (inventory chapter target; not Appendix C support mapping)"
            else:
                current_targets = "Unassigned in current structure"
        doi = record.get("doi", "")
        if citation and arxiv_id:
            record_ref = f"{qmd_escape(citation)}; {public_source_ref(record, f'arXiv:{qmd_escape(arxiv_id)}')}"
        elif citation:
            record_ref = f"{qmd_escape(citation)}; {public_source_ref(record)}"
        elif arxiv_id:
            record_ref = public_source_ref(record, f"arXiv:{qmd_escape(arxiv_id)}")
        else:
            record_ref = public_source_ref(record)
        if doi:
            record_ref = f"{record_ref}; DOI `{qmd_escape(doi)}`"
        note_status = "source note available" if (SOURCE_NOTES / f"{record['id']}.md").exists() else "source note pending"
        rows.append(
            "| `{id}` | {title} | {record_ref} | `{layer}` | {targets} | {note_status} | {notes} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                record_ref=record_ref,
                layer=qmd_escape(record.get("layer", "")),
                targets=qmd_escape(current_targets),
                note_status=qmd_escape(note_status),
                notes=qmd_escape(record.get("notes", "")),
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
            "| `{id}` | {title} | `{priority}` | `{layer}` | {current_targets} | {original_targets} | {source_ref} | {status} | {notes} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                priority=qmd_escape(record.get("priority", "")),
                layer=qmd_escape(record.get("layer", "")),
                current_targets=qmd_escape(current_targets),
                original_targets=qmd_escape(original_targets),
                source_ref=public_source_ref(record),
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
        if is_external_literature(record):
            continue
        current_targets = "; ".join(assignments.get(record["id"], [])) or "Unassigned in current structure"
        status = bibliography_status(record, connector_records, cache_records)
        rows.append(
            "| `{id}` | {title} | `{priority}` | `{layer}` | {source_ref} | {current_targets} | {status} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                priority=qmd_escape(record.get("priority", "")),
                layer=qmd_escape(record.get("layer", "")),
                source_ref=public_source_ref(record),
                current_targets=qmd_escape(current_targets),
                status=qmd_escape(status),
            )
        )
    text = f"""# Corben's Own Sources, Papers, and Local Projects

This appendix is generated from `sources/source_inventory.json` and current chapter assignments in `book_structure.json`.

This is an independent top-level appendix for Corben's own papers, Corben-supplied source material, recovered project history, and local project references. It is not a combined "sources used" appendix, and it is not split into internal Corben/external parts. It contains only material on the Corben/local-project side of the corpus: Corben-authored papers, Corben-supplied source material, local-project source routes, recovered architecture notes, implementation references, variants, and public-safe source records that are not marked as third-party external literature.

It is not a claim that every source has been ingested, summarized, citation-normalized, or independently verified. Source-derived claims should not be promoted until the relevant source has a source note and Appendix C has been updated.

External and third-party sources are not the second half of Appendix G. They live in their own top-level appendix: [Appendix H, External Sources by Other Authors](H_external_sources.qmd).

## Source Ownership Boundary

This page is the Corben-side source appendix. It should be read as Appendix G only; the external-source appendix is Appendix H.

## Appendix Identity

| Field | Boundary |
|---|---|
| This appendix contains | Corben-authored papers, Corben-supplied materials, recovered project records, and local project source records. |
| This appendix excludes | Third-party papers, documentation, outside projects, and other non-Corben references; those live in the separate Appendix H. |

## Appendix Scope

| Field | Boundary |
|---|---|
| Appendix identity | Appendix G: Corben's own sources, papers, and local projects |
| Ownership rule | If Corben wrote it, supplied it, recovered it from his project history, or built it in a local project, it belongs here; if another author, organization, or outside project produced it, it belongs in Appendix H. |
| Contains | Source material supplied by Corben, including authored ASI Stack papers, local-project source routes, implementation references, recovered notes, variants, and public-safe corpus records. |
| Excludes | Third-party literature records marked `external_literature`; those belong in Appendix H. |
| Evidence effect | Organizes Corben-side architecture material; it does not promote any claim unless the source note, Appendix C mapping, and evidence transition support that move. |

| Source ID | Title | Priority | Layer | Link | Current use | Bibliographic status |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Citation Policy

- Use stable source IDs for supplied corpus references until full citation metadata exists.
- Do not infer authors, dates, venues, versions, or publication status from titles alone.
- Do not cite a source as supporting a claim until its text has been ingested and a source note exists.
- Keep speculative or design-synthesis claims labeled as `argument` until source, prototype, or test evidence justifies promotion.
"""
    (ROOT / "appendices" / "G_corben_source_corpus.qmd").write_text(text, encoding="utf-8")

    external_rows = external_literature_rows(records, structure)
    external_text = f"""# External Sources by Other Authors

This appendix is generated from source records marked `external_literature` in `sources/source_inventory.json`.

This is an independent top-level appendix for external sources by other authors and organizations. It is not a subsection, second half, or continuation of Appendix G. It contains only third-party papers, documentation records, outside benchmarks, and non-Corben references used for comparison, grounding, or future literature review. Corben's own papers, Corben-supplied materials, recovered project records, and local project records live in their own top-level appendix: [Appendix G, Corben's Own Sources, Papers, and Local Projects](G_corben_source_corpus.qmd).

A listed external source does not claim reproduced experiments, local benchmark results, support-state promotion, or complete literature coverage.

## Source Ownership Boundary

This page is the external-source appendix. It should be read as Appendix H only; Corben-side records stay in Appendix G.

## Appendix Identity

| Field | Boundary |
|---|---|
| This appendix contains | Third-party papers, documentation, outside projects, and other external sources by authors other than Corben. |
| This appendix excludes | Corben's own papers, Corben-supplied materials, recovered project records, and local project source records; those live in the separate Appendix G. |

## Appendix Scope

| Field | Boundary |
|---|---|
| Appendix identity | Appendix H: external sources by other authors |
| Ownership rule | If another author, organization, or outside project produced it, it belongs here; Corben-authored papers, Corben-supplied materials, recovered project history, and local-project records stay in Appendix G. |
| Contains | Third-party papers, official documentation, outside benchmarks, and other non-Corben references by other authors or organizations used for comparison or grounding. |
| Excludes | Corben's own papers, Corben-supplied materials, recovered project records, and local project records; those belong in Appendix G. |
| Evidence effect | Organizes outside context; it does not claim reproduced results or support-state promotion without a reproduction or accepted evidence transition. |

## Chapter-Level External Grounding Policy

Future citation backfill should start from the sources already attached to each
chapter. Mine the linked Corben papers for bibliographies, footnotes, named
algorithms, standards, benchmarks, outside systems, and adjacent research terms
before broad search. Accepted third-party sources must be recorded in
`sources/source_inventory.json` with `priority: external_literature`, receive a
source note before prose use, and then appear here through scaffold generation.

External citation can establish relation, prior art, vocabulary, and comparison.
It does not by itself claim reproduced experiments, local verification, Lean
proof, Project Theseus replay, Circle receipt, support-state promotion, or
complete literature coverage.

## Source-Noted External Literature Records

| Source ID | Title | Citation or primary record | Layer | Current use | Source-note state | Notes |
|---|---|---|---|---|---|---|
{chr(10).join(external_rows)}

## External Literature Queue

Third-party references should be added only when bibliographic metadata is recorded and the source is actually used.

| Area | Expected role | Status |
|---|---|---|
| AI alignment and corrigibility | External comparison for the alignment and constitution layer. | initial source records and source notes added; no local reproduction or support-state promotion |
| AI governance, evals, and deployment policy | External comparison for authority ceilings, readiness gates, and release governance. | initial source records and source notes added; no local reproduction, compliance claim, or support-state promotion |
| Planning, task decomposition, and agent control | External comparison for PlanForge-style planning/control. | initial source records and source notes added; no local reproduction or support-state promotion |
| Retrieval, memory, and context engineering | External comparison for VCM and context-packet discipline. | initial source records and source notes added; no local reproduction or support-state promotion |
| Formal methods, verification, and proof assistants | External comparison for claim ledgers, Lean proofs, and protocol invariants. | initial source records and source notes added; no imported formal artifact or support-state promotion |
| Modular systems, routing, and mixture-of-experts | External comparison for routing and specialist promotion. | initial source records and source notes added; no local reproduction or support-state promotion |
| Compression, representation learning, and program synthesis | External comparison for compact generative systems and residual accounting. | initial source records and source notes added; no compression experiment or support-state promotion |
| Fast generation, decoding substrates, and serving acceleration | External comparison for MTP, speculative decoding, internal draft heads, diffusion LLMs, early exit, state-space alternatives, KV-cache memory, and useful-solution-per-second metrics. | initial source records and source notes added; no local reproduction or support-state promotion |
| Policy optimization and learning from feedback | External comparison for PPO/RLHF, GRPO/RLVR, DPO-style preference optimization, verifier rewards, reward hacking, reasoning-budget RL, and control-policy RL for planners, routers, VCM, execution, and generation modes. | initial source records and source notes added; no local reproduction or support-state promotion |
| Benchmarks, evaluation science, and anti-Goodhart methods | External comparison for evidence ratchets and regression preservation. | initial source records and source notes added; no local benchmark run or support-state promotion |

## External Citation Policy

- Keep outside literature separate from Corben's own papers, Corben-supplied materials, recovered project records, and local project records.
- Do not cite an external source as supporting a claim until the source text has been read and a source note or equivalent review artifact exists.
- Do not report reproduced external results unless the reproduction artifact, command, environment, and result record exist.
- Keep third-party documentation, papers, and benchmarks at their recorded support boundary.
"""
    (ROOT / "appendices" / "H_external_sources.qmd").write_text(external_text, encoding="utf-8")


def write_claim_matrix(structure: dict) -> None:
    promotion_paths = read_core_claim_promotion_paths()
    source_note_texts = {
        path.stem: path.read_text(encoding="utf-8")
        for path in SOURCE_NOTES.glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    source_note_ids = set(source_note_texts)
    rows = []
    post_v2_path = ROOT / "claim_decisions" / "post_v2_empirical_dispositions.json"
    post_v2_1_path = ROOT / "claim_decisions" / "post_v2_1_empirical_dispositions.json"
    post_v2_by_chapter = {}
    if post_v2_path.exists():
        post_v2_data = read_json(post_v2_path)
        if isinstance(post_v2_data, dict):
            post_v2_by_chapter = {
                str(row.get("chapter_id")): row
                for row in post_v2_data.get("decisions", [])
                if isinstance(row, dict) and row.get("chapter_id")
            }
    if post_v2_1_path.exists():
        post_v2_1_data = read_json(post_v2_1_path)
        if isinstance(post_v2_1_data, dict):
            post_v2_by_chapter.update({
                str(row.get("chapter_id")): row
                for row in post_v2_1_data.get("decisions", [])
                if isinstance(row, dict) and row.get("chapter_id")
            })
    chapters = flatten_chapters(structure)
    total_claim_mappings = sum(len(chapter.get("claim_source_mappings", [])) for chapter in chapters)
    total_passage_reviewed = sum(
        1
        for chapter in chapters
        for mapping in chapter.get("claim_source_mappings", [])
        if mapping.get("passage_review_state") in {"reviewed", "accepted", "complete"}
        and (mapping.get("passage_refs") or mapping.get("passage_references"))
    )
    for chapter in chapters:
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
        post_v2 = post_v2_by_chapter.get(chapter["id"])
        if post_v2:
            current_evidence = (
                "Current adjacent local evidence is recorded in the affected chapter and accepted "
                f"no-change core disposition; core support remains argument. Result: `{post_v2.get('result_ref')}`."
            )
            remaining = post_v2.get("remaining_burden", [])
            if isinstance(remaining, list) and remaining:
                open_gap = "; ".join(str(item) for item in remaining)
        claim_id = f"{chapter['id']}.core"
        claim_label = chapter.get("claim_label", "Design rationale")
        claim_mapping = claim_source_mapping_text(chapter)
        promotion_path = promotion_paths.get(
            chapter["id"],
            "No reviewer-facing promotion path is recorded yet; update docs/per_chapter_evidence_plan.md before any support-state movement.",
        )
        rows.append(
            f"| `{claim_id}` | `{chapter['id']}` | {qmd_escape(chapter.get('core_claim', 'No manifest core claim declared.'))} | {qmd_escape(claim_label)} | {qmd_escape(chapter.get('evidence_level', 'argument'))} | {source_label} | {qmd_escape(current_evidence)} | {qmd_escape(source_mapping)} | {qmd_escape(claim_mapping)} | {qmd_escape(open_gap)} | {qmd_escape(promotion_path)} |"
        )
    label_rows = "\n".join(f"| {qmd_escape(label)} | {qmd_escape(meaning)} |" for label, meaning in CLAIM_LABELS)
    support_rows = "\n".join(f"| {qmd_escape(state)} | {qmd_escape(meaning)} |" for state, meaning in SUPPORT_STATES)
    disposition_summary = ""
    disposition_path = ROOT / "claim_decisions" / "v1_x_core_claim_dispositions.json"
    if disposition_path.exists():
        disposition_data = read_json(disposition_path)
        if isinstance(disposition_data, dict) and isinstance(disposition_data.get("summary"), dict):
            summary = disposition_data["summary"]
            disposition_summary = (
                "\nThe current per-chapter core-claim dispositions are summarized in "
                "`docs/core_claim_disposition_ledger.md`: "
                f"{summary.get('accepted_core_transition_dispositions', 0)} accepted core-transition dispositions, "
                f"{summary.get('accepted_no_promotion_dispositions', 0)} accepted no-promotion dispositions, "
                f"{summary.get('promoted_core_claims', 0)} promoted core claims, and "
                f"{summary.get('chapter_core_claims_remaining_at_argument', len(chapters))} chapter core claims remaining at `argument`."
            )

    qcsa_reconciliation = """## QCSA P2–P3 Evidence Reconciliation (2026-07-13)

This overlay supersedes pre-implementation QCSA limits in earlier snapshots.
The exact local result is bounded synthetic/internal evidence; every chapter-
core state below remains `argument`.

| Chapter owner | Bounded repository evidence | Negative result or remaining boundary | Core state |
|---|---|---|---|
| `cognitive-compilation-and-semantic-ir` | Twelve typed lanes and one 13-stage vertical replay. | Active questions added no held-out accuracy; no natural compiler or learned question policy was tested. | `argument` |
| `virtual-context-abi` | Full object accuracy was `1.000000`; no-plural and no-indirection ablations fell to `0.916667` and `0.900000`. | Synthetic fixtures do not establish context adequacy, retrieval quality, or deployed VCM behavior. | `argument` |
| `claim-ledgers-and-belief-revision` | Typed evidence stayed separate from identity/truth/authority; the internal observer recorded zero structural loss. | Internal labels and graph integrity do not establish truth or independent construct validity. | `argument` |
| `runtime-adapters-tool-permissions-and-human-approval` | Removing authority fields caused 9 unsafe releases; one temporary-file write was separately authorized, observed, receipted, and rolled back. | One reversible local effect is not deployed adapter, approval-service, or security evidence. | `argument` |
| `inter-stack-protocols-identity-and-economic-exchange` | Same-SOID compatibility was `1.000000`; no-indirection compatibility fell to `0.400000`. | No peer federation, credential, dispute, payment, or settlement ran. | `argument` |
| `routing-heads-and-specialist-cores` | Object accuracy and prevention were `1.000000`; Brier was `0.082026`; all 10 vertical attacks failed closed. | Task accuracy tied at `1.000000`, operation ratio was `1.913386`, and no learned router or trained specialist ran. | `argument` |
| `compact-generative-systems-and-residual-honesty` | Exact structural round trip had zero observer disagreement and preserved residuals. | No compression, semantic-utility, repair, or latency advantage was established. | `argument` |
| `data-engines-continual-learning-and-unlearning` | Full migration compatibility was `1.000000`; no-compatibility task accuracy fell to `0.833333` and compatibility to zero. | No learning, forgetting, influence removal, privacy, or storage erasure ran. | `argument` |
| `integrated-reference-architecture` | One 13-stage path crossed intent through a real temporary effect, observation, receipts, same-SOID migration, and exact rollback. | The path is hand-authored, local, internally observed, zero-model, and not deployment, AGI, or ASI evidence. | `argument` |

Canonical records: `experiments/qcsa_reference/results/evaluation_results.json`,
`claim_decisions/qcsa_reference_evaluation_dispositions.json`,
`docs/qcsa_reference_evaluation_report.md`,
`experiments/qcsa_vertical_reference/results/vertical_result.json`, and
`docs/qcsa_governed_vertical_reference_report.md`. Five exact non-core
mechanism findings are marked `promote` for bounded evidence review, but no
automatic support-state transition has occurred.
"""

    p4_reconciliation = """## P4/M5 Governed-Usefulness Reconciliation (2026-07-16)

The prospectively frozen confirmatory campaign reached an informative bounded
local regime after preserving two instrument failures and a separate tuning
stage. On the fresh 16-task held-out denominator, 15 candidate decisions were
schema-admissible. Full governance released 9 useful and 0 unsafe decisions;
the simple baseline released 0 useful and 0 unsafe decisions; removing evidence
freshness exposed 1 unsafe release. Two independent evaluator implementations
agreed on all scored cases, and all six preregistered co-primary checks passed.

This accepts only the non-core claim
`governed-usefulness.held-out-local-policy-effect` at bounded
`synthetic-test-backed` scope. The campaign used a local model, authored tasks,
an internal policy, synthetic effects, and no independent external evaluator or
transfer setting. It does not promote a chapter-core claim, establish broad
usefulness, acceptable governance cost, deployment safety, model generality,
SOTA, AGI, or ASI. The exact protocol, failures, exclusions, arm results, and
claim ceiling are recorded in `docs/p4_governed_usefulness_campaign.md` and
`experiments/p4_governed_usefulness/results/confirmatory_result.json`.
"""

    text = f"""# Claim/Evidence Matrix

This matrix contains one core claim per dynamic chapter and records the conservative evidence state used by the current manuscript.

The support state is the compact authoritative summary, not a complete quality score. The separate [evidence-quality vector contract](../docs/evidence_quality_vectors.md) tracks independence, reproducibility, recency, coverage, adversarial strength, validity, artifact access, and transfer distance for every chapter-core claim without aggregating them or changing support.

Each claim has two separate classifications: a claim label that describes what kind of statement it is, and a support state that describes what currently supports it.

No chapter core claim is marked `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` yet. A source note means the source has been mined for drafting context; it does not by itself promote the claim.

Current generated coverage: {len(chapters)} chapter core claims, {total_claim_mappings} exact claim-source mappings, {total_passage_reviewed} passage-reviewed mappings, and {len(promotion_paths)} reviewer-facing promotion-path rows from `docs/per_chapter_evidence_plan.md`. Unreviewed mappings remain source-note mappings until passage review, accepted evidence transitions, or validated artifacts justify narrower support-state movement.

The current accepted non-core upward transitions are summarized in `docs/non_core_evidence_ledger.md`. They do not promote any chapter core claim above `argument`.

The accepted-transition identity graph in `evidence_quality/claim_identity_graph.json` resolves all 115 accepted transition records through 25 exact atom, 61 bounded subclaim, and 29 proxy relations. Indirect relations do not move their parent atom or chapter-core support state. The competence ledger classifies all 90 accepted negative/no-change records as 1 N0, 15 N1, 74 N2, and 0 N3–N5; broader prose and historical `blocked_after_full_attempt` interpretation remains under audit.
{disposition_summary}

| Claim ID | Chapter ID | Claim | Claim label | Current support state | Assigned sources | Current evidence | Source-note chapter mapping | Claim-source mapping | Open gap | What would promote this |
|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

{qcsa_reconciliation}

{p4_reconciliation}

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


def write_implementation_horizons(structure: dict) -> None:
    sections: list[str] = []
    total = 0
    for part in structure.get("parts", []):
        rows = []
        for chapter in part.get("chapters", []):
            total += 1
            rows.append(
                "| `{id}` | {title} | {minimum} | {beyond} | `{support}` |".format(
                    id=qmd_escape(chapter.get("id", "")),
                    title=qmd_escape(chapter.get("title", "")),
                    minimum=qmd_escape(
                        chapter.get(
                            "minimal_implementation",
                            "No manifest minimal implementation statement declared yet.",
                        )
                    ),
                    beyond=qmd_escape(
                        chapter.get(
                            "beyond_state_of_art",
                            "No manifest beyond-state-of-the-art statement declared yet.",
                        )
                    ),
                    support=qmd_escape(chapter.get("evidence_level", "argument")),
                )
            )
        sections.append(
            "## {title}\n\n"
            "| Chapter ID | Chapter | Minimum viable implementation | Beyond the state of the art | Support state |\n"
            "|---|---|---|---|---|\n"
            "{rows}\n".format(title=qmd_escape(part.get("title", "")), rows="\n".join(rows))
        )

    text = f"""# Implementation Horizons

This appendix is generated from `book_structure.json`. It is the book-wide build horizon: each chapter has one smallest honest implementation slice and one mature product-level endpoint.

The minimum viable implementation column is not a claim that the implementation already exists. The beyond-state-of-the-art column is a target architecture, not a current-result claim. Support-state movement still requires the source mappings, schemas, proofs, tests, benchmark records, runtime traces, review receipts, or governance artifacts recorded elsewhere in the book.

Current generated coverage: {total} chapter implementation horizons.

{chr(10).join(sections)}
"""
    (ROOT / "appendices" / "K_implementation_horizons.qmd").write_text(text, encoding="utf-8")


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
| Claim ledger revision harness | `python3 scripts/validate_claim_ledger_revision.py` | Checks synthetic claim-ledger and belief-revision fixtures for no-change boundaries, contradiction quarantine, claim splitting, support-state promotion blockers, revision-history preservation, surface propagation, review routing, residuals, and non-claim boundaries. | Passing this check proves synthetic claim-ledger record discipline only; it does not prove source interpretation, runtime behavior, verifier quality, open-domain claim extraction, or belief-engine correctness. |
| Proof-carrying claim harness | `python3 scripts/validate_proof_carrying_claims.py` | Checks synthetic proof-carrying-claim fixtures for verifier artifact refs, tier/justification alignment, bounded review eligibility, failed-attempt preservation, mismatch escalation, and non-claim boundaries. | Passing this check proves synthetic proof-carrying record discipline only; it does not prove theorem validity, semantic equivalence, citation accuracy, verifier quality, runtime behavior, or open-domain formalization. |
| Tribunal review harness | `python3 scripts/validate_tribunal_review.py` | Checks synthetic tribunal-review fixtures for dossier refs, reviewer roles, adversarial probes, evidence-backed accept verdicts, dissent preservation, prior-review guards, required actions, constraint effects, and non-claim boundaries. | Passing this check proves synthetic tribunal-review record discipline only; it does not prove reviewer independence, adversarial-review quality, consensus quality, verdict correctness, runtime behavior, or source interpretation. |
| Value conflict harness | `python3 scripts/validate_value_conflicts.py` | Checks synthetic value-conflict fixtures for multi-axis classification, stakeholder and evidence requirements, high-stakes review routing, residual uncertainty preservation, authority narrowing, dissent payloads, and bounded-decision revisit conditions. | Passing this check proves synthetic value-conflict record discipline only; it does not prove moral correctness, classification quality, reviewer independence, human-review quality, tribunal quality, runtime policy behavior, or source interpretation. |
| Constitutional alignment harness | `python3 scripts/validate_constitutional_alignment.py` | Checks synthetic constitutional-predicate fixtures for protected scope, operational tests, conflict routing, review routes, self-modification weakening rules, migration policies, least-sufficient-power behavior, uncertainty preservation, and non-claim boundaries. | Passing this check proves synthetic constitutional-predicate record discipline only; it does not prove deployed constitutional alignment, moral correctness, runtime policy behavior, source interpretation, self-modification safety, predicate-translation adequacy, or review quality. |
| Governance rights harness | `python3 scripts/validate_governance_rights.py` | Checks synthetic governance-right fixtures for audit material and receipts, denied/redacted appeal paths, materially usable exit and fork access paths, fork safety constraints, preservation obligations, durable record paths, and non-claim boundaries. | Passing this check proves synthetic governance-right record discipline only; it does not prove institutional governance rights, legal rights, runtime right enforcement, deployed fork/exit usability, reviewer independence, or source interpretation. |
| Agency rights harness | `python3 scripts/validate_agency_rights.py` | Checks synthetic agency-right checklist fixtures for affected parties, bounded delegation, material usability, timing-before-effect review, review and appeal channels, corrigibility paths, high-impact approval, residual dependency risk, degradation reasons, and accountable principals. | Passing this check proves synthetic agency-right checklist discipline only; it does not prove deployed agency preservation, dignity preservation, manipulation resistance, consent quality, reviewer independence, runtime policy behavior, or source interpretation. |
| Support-state transition harness | `python3 scripts/validate_support_state_transitions.py` | Checks synthetic valid and expected-invalid evidence-transition records for no-change conservatism, upward-transition review gates, downward demotion records, terminal refutation records, required evidence refs, and failed-verification blockers. | Passing this check proves transition-gate behavior for synthetic fixtures only; it does not promote, demote, deprecate, or refute Appendix C claims, prove source interpretation, or validate AI runtime behavior. |
| Authority transition harness | `python3 scripts/validate_authority_transitions.py` | Checks synthetic authority-transition records for non-escalation, permission separation, denial receipts, review escalation, and expected-invalid confused-deputy shortcuts. | Passing this check proves authority-gate behavior for synthetic fixtures only; it does not prove deployed permission enforcement, runtime adapter safety, secret handling, or revocation propagation. |
| Security kernel harness | `python3 scripts/validate_security_kernel.py` | Checks synthetic authority-use receipt fixtures for handle mediation, approval artifacts, bounded action scope, SCIF lifecycle completeness, sanitization, residual leak-risk notes, revocation paths, and prompt-injection non-disclosure boundaries. | Passing this check proves synthetic security-kernel receipt discipline only; it does not prove kernel security, sandbox isolation, side-channel safety, prompt-injection containment, secret-handle safety, least-privilege context behavior, runtime policy behavior, or source interpretation. |
| Stable capability fields harness | `python3 scripts/validate_stable_capability_fields.py` | Checks synthetic stable-capability-field fixtures for qualification predicates, evidence refs, readiness refs, authority ceilings, route permission effects, evaluator independence, rollback obligations, default-route blockers, and non-claim boundaries. | Passing this check proves synthetic stable-capability-field record discipline only; it does not prove runtime route validity, capability identity, evaluator integrity, authority enforcement, replacement safety, rollback execution, or source interpretation. |
| Capability replacement harness | `python3 scripts/validate_capability_replacement.py` | Checks synthetic replacement-transaction fixtures for field identity, qualification evidence, regression results, non-widening authority checks, evaluator separation, residual escrow, rollback receipts, approvals, monitor state, promotion blockers, model-rollout gates, irreversible-effect ownership, and non-claim boundaries. | Passing this check proves synthetic replacement-transaction record discipline only; it does not prove deployed replacement behavior, runtime route quality, evaluator integrity, authority enforcement, rollback execution, regression quality, source interpretation, production model rollout, model quality, or model-monitor behavior. |
| Self-improvement boundary harness | `python3 scripts/validate_self_improvement_boundaries.py` | Checks synthetic self-improvement transition fixtures for protected invariants, evaluator separation, cheaper-intervention ordering, authority non-widening, governance review, monitor windows, rollback paths, and no-promotion language. | Passing this check proves synthetic self-improvement transition-record discipline only; it does not prove deployed self-improvement behavior, runtime optimization, evaluator integrity, authority enforcement, rollback execution, regression quality, recursive self-improvement safety, or source interpretation. |
| Plan-execution contract harness | `python3 scripts/validate_plan_execution_contracts.py` | Checks synthetic command-contract, plan-graph, DAG, semantic-atom, typed-job, intent-origin, field-confidence, and inferred-authority scenarios for cross-record consistency, acyclic dependency order, dispatch receipts, requirement preservation, artifact traceability, approval gating, explicit intent preservation, authority-ceiling preservation, field-confidence dispatch blocking, and inferred-authority dispatch blocking. | Passing this check proves synthetic cross-record gate behavior only; it does not prove planner quality, scheduler behavior, deployed execution, runtime adapter safety, parser quality, semantic extraction quality, authority extraction quality, approval-service behavior, side-effect enforcement, or benchmark performance. |
| Runtime adapter permission harness | `python3 scripts/validate_runtime_adapter_permissions.py` | Checks synthetic typed-job, runtime-adapter-invocation, authority-use-receipt, and authority-probe scenarios for permission coverage, high-impact approval gating, approval expiry markers, effect receipts, rollback handles, irreversible residuals, authority receipt alignment, ambient-authority confused-deputy rejection, and revoked-receipt blocking. | Passing this check proves synthetic adapter-record gate behavior only; it does not prove deployed adapter behavior, sandbox isolation, approval-service quality, secret-handle safety, rollback execution, confused-deputy resistance, revocation propagation, or runtime behavior. |
| Runtime adapter effect replay probe | `python3 scripts/validate_runtime_adapter_effect_probe.py` | Checks a public-safe local temp-file effect replay for `valid_low_impact_local_write_effect_replay`, pre/post/rollback hashes, rollback-exact restoration, missing-permission no-mutation denial, and expired-approval no-mutation denial. | Passing this check proves only one local toy effect/rollback trace and two no-mutation controls; it does not prove deployed adapter behavior, sandbox isolation, approval-service behavior, secret-handle safety, revocation propagation, policy-enforcement correctness, rollback-service behavior, benchmark performance, or chapter-core support-state promotion. |
| Context admission/adequacy harness | `python3 scripts/validate_context_admission_adequacy.py` | Checks synthetic context ABI, packet, semantic-page certificate, transaction, and adequacy scenarios for admission/adequacy separation, conflict blocking, stale certificate rejection, deletion closure, escalation, and mode-confusion gates. | Passing this check proves synthetic context-record gate behavior only; it does not prove VCM resolver behavior, context compiler behavior, memory-store correctness, summary fidelity, model verification bandwidth, or benchmark performance. |
| Context transaction memory-store harness | `python3 scripts/validate_context_transaction_memory_store.py` | Checks bounded context-transaction and synthetic memory-event fixtures for committed-read visibility, mount faults, branch isolation, deletion-closure/materialization blocking, taint/declassification, replay boundaries, and support-state non-promotion. | Passing this check proves bounded fixture behavior only; it does not prove deployed memory-store correctness, VCM resolver behavior, runtime branch isolation, mount enforcement outside the fixture, side-channel safety, VCM-Bench performance, or support-state promotion. |
| Readiness/residual gate harness | `python3 scripts/validate_readiness_residual_gates.py` | Checks synthetic costed-route, readiness-gate, and replacement-transaction scenarios for promotion gates, residual escrow custody, quarantine, authority bounds, expired-evidence reruns, fallback, and rollback readiness. | Passing this check proves synthetic cross-record gate behavior only; it does not prove routing accuracy, readiness-engine behavior, residual-ledger storage, rollback execution, runtime monitoring, MoECOT replay, or benchmark performance. |
| Benchmark anti-Goodhart harness | `python3 scripts/validate_benchmark_antigoodhart.py` | Checks synthetic benchmark-ratchet, policy-optimization, and steward-action scenarios for holdout/contamination/mutation or transfer checks, saturated-benchmark regression floors, blocked-ratchet policy promotion, reward-as-truth confusion, and release approval evidence. | Passing this check proves synthetic cross-record gate behavior only; it does not prove benchmark quality, hidden-holdout integrity, policy-training quality, reward-hacking resistance, steward-agent behavior, release safety, or runtime behavior. |
| Generation mode baseline harness | `python3 scripts/validate_generation_mode_baselines.py` | Checks deterministic generation-mode and resource-budget scenarios for run, baseline, and negative-control refs, useful-solution-per-second plus quality and residual metrics, fallback behavior, resource-budget alignment, latency-only proxy rejection, and no-promotion boundaries. | Passing this check proves deterministic fixture-accounting behavior only; it does not prove generation speed, speculative decoding quality, diffusion generation quality, KV-cache throughput, routing quality, model quality, useful-solution-per-second performance, or runtime behavior. |
| Fast generation task-bundle validation | `python3 scripts/validate_fast_generation_task_bundle.py` | Recomputes a public-safe local fast-generation task bundle with an autoregressive reference baseline, verified fast-template candidate, latency-only negative control, quality checks, verifier/fallback/residual records, deterministic cost units, output digests, and useful-solution-per-cost accounting. | Passing this check proves deterministic task-bundle accounting and no-promotion boundaries only; it does not prove model generation speed, speculative decoding, MTP, diffusion, KV-cache, serving throughput, route-selector adequacy, model quality, useful-solution-per-second improvement for an AI model, or deployment behavior. |
| Project Theseus generation-mode import validation | `python3 scripts/validate_theseus_generation_mode_import.py` | Checks a public-safe static Project Theseus generation-mode gate import with 18 modes, 13 comparisons, zero hard gaps, zero modes with missing report refs, zero promotable comparisons, pinned source/report/tool digests, and expected-invalid controls for hard boundary-gate failure, private-payload copying, missing-report-ref overclaim, support-promotion overclaim, raw-speed promotion, and useful-speed overclaim. | Passing this check proves only the imported report-boundary discipline and negative promotion decision; it does not rerun Theseus, prove generation speed, prove useful-solution-per-second improvement, prove model quality, or promote chapter support states. |
| Compact GVR synthetic slice | `python3 scripts/validate_compact_gvr_slice.py` | Recomputes a public-safe compact generate-verify-repair receipt slice with a literal baseline, selected exact compact generator-plus-repair receipt, lossy exactness control, negative-rate/no-fallback control, bounded-search-overrun control, accepted non-core evidence transition, and Lean fixture bridge. | Passing this check proves bounded synthetic receipt discipline only; it does not prove compression utility, codec correctness, semantic utility, model quality, deployed fallback execution, benchmark performance, or chapter-core support-state promotion. |
| Circle concrete evidence-surface validation | `python3 scripts/validate_circle_concrete_evidence_surface.py` | Checks that the concrete Circle external receipt facts are visible in the Circle and CoilRA chapters, outline, and manifest test rows while preserving chapter-core, model-quality, context-length, runtime, transfer, deployment, and ASI non-claims. | Passing this check proves only public-surface traceability for an already-recorded structural receipt lane; it does not rerun Circle, vendor contract packs, prove model quality, promote chapter support states, or create a downstream workload result. |
| Circle cyclic memory receipt-slice validation | `python3 scripts/validate_circle_cyclic_memory_receipt_slice.py` | Checks that the Circle cyclic-memory receipt slice surfaces `CC-AI-CONTRACT-MEMORY-001`, theorem IDs, same-residue events, winding fields, alias load, receipt fingerprint, Circle CLI test output, and non-claim boundaries in the Coil chapter, reader manuscript, outline, roadmap, manifest, and result record. | Passing this check proves only structural residue/winding receipt traceability for one local external-project import; it does not rerun Circle from this repo, prove retrieval quality, prove model quality, prove long-context behavior, promote support state, or create a downstream workload result. |
| RankFold public-safe replay probe | `python3 scripts/validate_rankfold_public_safe_probe.py` | Checks a fresh local RankFold pack/verify/list/unpack replay over a generated public-safe synthetic text fixture, including RAW0 codec observation, roundtrip-exact digest preservation, no compression advantage, license-disabled NeuralFold boundary, and a single-byte corrupt-archive negative control. | Passing this check proves only one synthetic local replay and public-surface traceability; it does not prove RankFold codec correctness, NeuralFold compression, compression advantage, benchmark performance, downstream utility, fallback execution, deployed compression behavior, or chapter-core support-state promotion. |
| RankFold artifact import validation | `python3 scripts/validate_rankfold_artifact_import.py` | Checks a public-safe local RankFold artifact import for three existing `.rfa` archive observations over a 100,000,000-byte decoded artifact digest, archive ratios up to 2.76634019 decoded/archive, `rfa verify` summaries of 1 OK, 0 failed, `NEURAL0` inspect metadata, and non-claim boundaries. | Passing this check proves only recorded local artifact metadata consistency and public-surface traceability; it does not rerun compression, prove codec correctness, prove benchmark performance, prove downstream utility, prove fallback execution, prove deployed compression behavior, or promote chapter-core support state. |
| Chapter-review burn-down validation | `python3 scripts/validate_chapter_review_burndown.py` | Checks that the calibrated 44-chapter review input is represented as roadmap work for every current manifest chapter, without stale IDs, placeholder rows, lost calibration notes, or unverified Circle wording. | Passing this check proves only roadmap coverage for reviewer-input follow-up; it does not prove chapter quality, source interpretation, external review, proof adequacy, test execution, or support-state promotion. |
| Resource budget ledger harness | `python3 scripts/validate_resource_budget_ledgers.py` | Checks deterministic Resource Budget Record scenarios for dispatch, high-risk escalation, protected overhead, security-overhead erasure rejection, displaced-cost residualization, review-capacity hoarding, KV-cache/serving-memory accounting separation, throughput-to-quality overclaim rejection, evidence refs, and no-promotion boundaries. | Passing this check proves deterministic budget-ledger fixture behavior only; it does not prove scheduler behavior, load stability, verification-tax optimization, KV-cache behavior, serving throughput, single-request quality, runtime budget enforcement, or economic outcomes. |
| Capacity smoothing toy harness | `python3 scripts/validate_capacity_smoothing.py` | Checks deterministic toy capacity traces for bounded regeneration arithmetic, priority deferral under blocked high-risk work, scope reduction, reviewer-capacity accounting, protected-review overhead, displaced-review-cost residualization, overload rejection, Lean bridge coverage, and no-promotion boundaries. | Passing this check proves toy trace consistency only; it does not prove TokenMana behavior, scheduler behavior, load stability, review-queue optimization, reviewer-capacity optimization, protected-overhead adequacy, displaced-cost measurement, runtime behavior, human outcomes, or economic outcomes. |
| Phase 5 harness registry validation | `python3 scripts/validate_phase5_harness_registry.py` | Checks that the Phase 5 harness set has commands, scripts, docs, fixture counts, result records, Appendix E rows, public status references, main-validation wiring, primary chapter mappings, and explicit non-claim boundaries. | Passing this check proves harness traceability only; it does not run the harnesses, prove runtime behavior, promote support states, or validate benchmark quality. |
| Reader continuity audit | `python3 scripts/audit_reader_continuity.py --check` | Derives the reader edition in a temporary workspace and checks that the tracked Phase 2 continuity audit is current, including reader word counts, overlay counts, density signals, table/code/diagram counts, repeated-opening heuristics, and a priority queue for human review. | Passing this check proves the audit report is current only; it is not a manual reader review, reader release, ebook/document/PDF artifact, audio artifact, or support-state promotion. |
| Proof-readiness validation | `python3 scripts/validate_proof_readiness.py` | Checks that proof triage tags, modules, root imports, formal targets, and target statuses stay aligned with the generated proof manifest. | Passing this check proves manifest/triage/import consistency only; theorem status still requires implemented Lean modules and a passing Lean build. |
| Proof artifact traceability audit | `python3 scripts/validate_proof_artifact_audit.py` | Checks that implemented proof targets are traceable from manifest and triage to Lean modules, root imports, chapter hooks, limitation prose, and Appendix E coverage. | Passing this check proves traceability and explicit non-claim coverage only; it does not prove semantic adequacy, source interpretation, deployed enforcement, or benchmark performance. |
| Source evidence traceability audit | `python3 scripts/validate_source_evidence_audit.py` | Checks that assigned source/chapter pairs, source notes, chapter listings, and claim-source mappings stay aligned, and reports passage-review coverage. | Passing this check proves source-note/mapping consistency only; it does not quote private passages or promote any support state. |
| Proof target coverage summary | Generated by `python3 scripts/sync_scaffold.py` from `proofs/proof_triage.json`; checked by `python3 scripts/validate_proof_readiness.py`. | Publishes the current count of proof targets by status, triage class, and recommended route. | Passing the validator proves coverage/accounting consistency only; it does not prove broad chapter claims, source interpretation, model quality, deployed enforcement, or benchmark performance. |
| Repeated prose validation | `python3 scripts/validate_repeated_prose.py` | Checks chapter files for exact repeated long prose paragraphs and known formulaic chapter phrases that indicate template-shaped drafting. | Passing this check proves only that exact repeated long paragraphs and known formulaic phrases are absent; it is not a full editorial review. |
| Visual coverage validation | `python3 scripts/validate_visual_coverage.py` | Checks that every chapter has at least one substantive Mermaid diagram with enough lines, edges, nodes, and labeled transitions, and that the landing page references the hero image asset. | Passing this check proves visual coverage only; it does not prove the diagrams are complete or promote chapter claims. |

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
    write_implementation_horizons(structure)
    ensure_glossary()
    ensure_protocol_schemas()
    write_test_specs(structure)
    source_queue_rows = synchronize_outline_source_queues(write=True)
    source_crosswalk_files = synchronize_chapter_source_crosswalks(write=True)
    sync_public_trust_metrics()
    print(
        f"Synchronized book structure: {len(flatten_chapters(structure))} chapters, "
        f"{written} chapter files written, {source_queue_rows} source-queue row(s) updated, "
        f"{source_crosswalk_files} source-crosswalk file(s) updated."
    )


if __name__ == "__main__":
    main()
