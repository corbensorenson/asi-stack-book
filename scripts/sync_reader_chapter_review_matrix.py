#!/usr/bin/env python3
"""Sync the v1.0 human-reader chapter review matrix.

The matrix is a review-control surface for the normal reader manuscript. It is
allowed to track reader-only prose decisions, but it must stay manifest-aligned
and subordinate to the live AI/research book for claims, support states, source
boundaries, proof/test status, implementation horizons, and release records.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_review_matrix.json"
DOC_PATH = ROOT / "docs" / "reader_chapter_review_matrix.md"
FORMAT_MATRIX_PATH = ROOT / "editions" / "reader_manuscript" / "v1_0" / "format_review_matrix.json"
STRUCTURE_PATH = ROOT / "book_structure.json"
OVERLAY_CHAPTER_DIR = ROOT / "editions" / "reader_overlays" / "v1_0" / "chapters"
MANUSCRIPT_REVIEW = ROOT / "docs" / "reader_manuscript_review.md"
CONTINUITY_REVIEW = ROOT / "docs" / "reader_continuity_review.md"

ALLOWED_REVIEW_STATUS = {
    "not_started",
    "spot_checked",
    "reviewed",
    "blocked",
}
ALLOWED_REVIEW_DEPTH = {
    "none",
    "representative_spot_check",
    "medium_priority_manual_review",
    "full_chapter_review",
}
ALLOWED_DISPOSITIONS = {
    "none",
    "no_immediate_action",
    "reader_overlay_active",
    "reader_overlay_needed",
    "canonical_edit_needed",
    "companion_note_candidate",
    "curated_manuscript_candidate",
}
ALLOWED_RELEASE_BLOCKERS = {
    "full_chapter_review_not_recorded",
    "reader_release_record_not_created",
    "curated_reconciliation_not_recorded",
    "format_artifact_not_reviewed",
}

SPECIAL_REVIEW_DEFAULTS = {
    "planning-as-a-control-layer": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_ii_contracts_full_review_pass.md#decisions",
            "docs/curated_reader_planning_control_prose_pass.md",
            "docs/chapter_consolidation_release_stability_review.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter-text review recorded for the planning "
            "chapter. Existing overlay is accepted for the reader path; proposed, "
            "blocked, dispatchable, replanned, stopped, and residual work remain "
            "distinct without claiming planner quality or dispatch safety. First "
            "curated reader prose pass and drafting companion note are recorded "
            "under the planning/DAG release-stability consolidation caveat; the "
            "companion note is for e-reader/audio density support only, while "
            "command-contract inheritance, plan-node lifecycle states, "
            "DAG/dependency boundaries, adequacy contracts, dispatch receipts, "
            "replanning deltas, residual registers, and planner-quality "
            "non-claims remain in the reader spine. Release blockers remain "
            "active and no support-state movement or merge decision is implied."
        ),
    },
    "routing-heads-and-specialist-cores": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "companion_note_candidate",
            "no_immediate_action",
            "curated_manuscript_candidate",
        ],
        "review_refs": [
            "docs/reader_part_iii_opening_full_review_pass.md#decisions",
            "docs/curated_reader_routing_heads_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter-text review recorded for the routing "
            "chapter. First drafting-only curated reader prose pass and drafting "
            "companion note recorded; the companion note is for e-reader/audio "
            "density support only, while route-as-lease framing, specialist "
            "registry, routing decision record, route receipt, rejected "
            "alternatives, selected authority subsets, authority/readiness "
            "boundaries, residual ownership, proof/test limits, route-quality "
            "non-claims, and deferred MoECOT fold caveat remain intact. Not "
            "release-approved."
        ),
    },
    "personal-compute-hives-and-federated-edge-intelligence": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iii_opening_full_review_pass.md#decisions",
            "docs/curated_reader_personal_compute_hives_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter-text review recorded for the Personal "
            "Compute Hives chapter. Existing overlays are accepted for the reader "
            "path; consent, privacy, rented-node, family/project mediation, "
            "scheduler, and implementation non-claim boundaries remain visible. "
            "First curated reader prose pass and drafting companion note are "
            "recorded; the companion note is for e-reader/audio density support "
            "only, while policy-first scheduling, device and portal authority "
            "boundaries, consent, privacy, family/project mediation, rented-node "
            "limits, revocation, evidence return, and implementation non-claims "
            "remain in the reader spine. Release blockers remain active and no "
            "hive scheduler, federation, rented-node, family-governance, or "
            "reader-artifact claim is approved."
        ),
    },
    "compact-generative-systems-and-residual-honesty": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iii_compression_full_review_pass.md#decisions",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Drafting-only curated reader manuscript file and companion note now "
            "exist; the companion note is for e-reader/audio density support only, "
            "while compactness-as-claim, verifier separation, repair residuals, "
            "fallback, semantic representation leases, cost ownership, and "
            "non-claim boundaries remain in the reader spine. The 2026-07-03 "
            "alignment surfaces the existing Compact GVR synthetic slice and "
            "preserves no-core-claim-promotion boundaries. Release blockers "
            "remain active and this row is not a release approval."
        ),
    },
    "fast-generation-architectures": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iii_compression_full_review_pass.md#decisions",
            "docs/curated_reader_fast_generation_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter review recorded; existing overlays "
            "convert dense metric and taxonomy material into prose while "
            "preserving proposed/accepted output separation, verifier cost, "
            "fallback, memory pressure, task success, and promotion evidence. "
            "First curated reader prose pass and drafting companion note are "
            "recorded; the 2026-07-03 alignment surfaces the existing "
            "task-bundle replay and Project Theseus generation-mode import as "
            "bounded accounting/no-promotion evidence. The companion note is "
            "for e-reader/audio density support only, while proposed-versus-"
            "accepted output, verifier cost, fallback, repair, memory pressure, "
            "task success, route promotion, benchmark, serving, and "
            "no-speed-claim boundaries remain in the reader spine. Release "
            "blockers remain active and no speed, quality, serving, benchmark, "
            "route-promotion, support-promotion, or reader-artifact claim is "
            "approved."
        ),
    },
    "resource-economics-and-token-budgets": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iii_representation_full_review_pass.md#decisions",
            "docs/curated_reader_resource_economics_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter review recorded. Budgets remain framed "
            "as policy objects that preserve verification tax, protected overhead, "
            "displaced costs, serving pressure, rejected savings, and "
            "no-cost-cutting-of-governance boundaries. First curated reader prose "
            "pass and drafting companion note are recorded; the 2026-07-03 "
            "alignment surfaces the workload-quality probe, load-stability "
            "probe, CI-cost profile, and aggregate flagship replay as bounded "
            "local or synthetic no-promotion evidence. The companion note is for "
            "e-reader/audio density support only, while verification tax, route "
            "eligibility, residual ownership, no-change sublane decisions, "
            "serving-memory separation, scheduler non-claims, and economic "
            "non-claims remain in the reader spine. Release blockers remain "
            "active and no scheduler, economics, serving, welfare, cost-quality, "
            "workload-quality, load-stability, support-promotion, or "
            "reader-artifact claim is approved."
        ),
    },
    "coilra-multicoil-rope-and-cyclic-mixers": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iii_iv_proof_bridge_full_review_pass.md#decisions",
            "docs/curated_reader_coilra_cyclic_mixers_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter review recorded. First curated reader "
            "prose pass and drafting companion note now reframe the chapter "
            "around cyclic-substrate adoption discipline, structural receipts, "
            "alias/load diagnostics, parameter and hardware ledgers, baseline "
            "symmetry, negative controls, tradeoff packets, and canary-route "
            "non-claims while preserving the argument-level support boundary. "
            "The companion note is for e-reader/audio density support only, "
            "while quality, performance, context-length, memory, training, "
            "hardware, deployment, and support-state boundaries remain in the "
            "reader spine."
        ),
    },
    "executable-specifications-and-lean-proof-envelope": {
        "review_status": "spot_checked",
        "review_depth": "medium_priority_manual_review",
        "dispositions": ["reader_overlay_active", "companion_note_candidate", "no_immediate_action"],
        "review_refs": ["docs/reader_continuity_review.md#medium-priority-queue-decisions"],
        "review_notes": (
            "Medium-priority density row read; no additional overlay now. Future "
            "reader release work may route proof-envelope vocabulary through "
            "companion notes or glossary treatment."
        ),
    },
    "circle-calculus-and-proof-carrying-ai-contracts": {
        "review_status": "spot_checked",
        "review_depth": "medium_priority_manual_review",
        "dispositions": ["reader_overlay_active", "companion_note_candidate", "no_immediate_action"],
        "review_refs": ["docs/reader_continuity_review.md#medium-priority-queue-decisions"],
        "review_notes": (
            "Medium-priority density row read; no additional overlay now. The "
            "theorem-linked receipt boundary should stay visible, with possible "
            "companion-note or glossary treatment later."
        ),
    },
    "policy-optimization-and-learning-from-feedback": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iv_evidence_governance_full_review_pass.md#decisions",
            "docs/curated_reader_policy_optimization_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "Full generated-reader chapter review recorded. Existing overlays "
            "keep method-family material readable, and a first drafting-only "
            "curated prose pass plus drafting companion note now foreground "
            "policy updates as governed behavior-change leases: target policy, "
            "feedback admissibility, reward boundary, drift bounds, holdouts, "
            "regressions, reward-hacking probes, authority conservation, "
            "rollback, promotion gates, method-family nonclaims, proof/test "
            "limits, and no local training-result boundaries without approving "
            "release. The companion note is for e-reader/audio density support "
            "only, while reward, authority, rollback, training-result, "
            "deployment, and support-state boundaries remain in the reader spine."
        ),
    },
    "artifact-steward-agents-and-living-project-governance": {
        "review_status": "spot_checked",
        "review_depth": "medium_priority_manual_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": ["docs/reader_continuity_review.md#medium-priority-queue-decisions"],
        "review_notes": (
            "Medium-priority length row read; retained for now because the "
            "governance, treasury, worker-federation, contribution-ledger, "
            "event-taint, and sunset concepts are central. Future curated reader "
            "work may compress examples or move the implementation ladder to "
            "companion material."
        ),
    },
    "project-theseus-as-report-first-implementation-reference": {
        "review_status": "reviewed",
        "review_depth": "full_chapter_review",
        "dispositions": [
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": [
            "docs/reader_part_iv_completion_full_review_pass.md#decisions",
            "docs/curated_reader_project_theseus_prose_pass.md",
            "docs/reader_companion_note_routing_review.md#chapter-decisions",
        ],
        "review_notes": (
            "First curated reader prose pass and drafting companion note recorded. "
            "The pass keeps Theseus as report-first implementation-reference "
            "context, preserves source-note, imported-report, replay-readiness, "
            "missing-artifact, public/non-public, currentness, dashboard, "
            "benchmark, runtime, model-quality, deployment, and support-state "
            "boundaries, and does not claim reproduced benchmark, clean live "
            "replay, current dashboard state, runtime evidence, model quality, "
            "deployment readiness, or support-state movement. The companion note "
            "is for e-reader/audio density support only."
        ),
    },
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def flatten_manifest() -> list[dict[str, str]]:
    structure = load_json(STRUCTURE_PATH, {})
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    rows: list[dict[str, str]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        part_id = str(part.get("id", ""))
        part_title = str(part.get("title", ""))
        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            chapter_id = chapter.get("id")
            title = chapter.get("title")
            file_path = chapter.get("file")
            if not all(isinstance(value, str) and value for value in (chapter_id, title, file_path)):
                raise SystemExit(f"Invalid chapter record in {part_id}: {chapter!r}")
            rows.append(
                {
                    "part_id": part_id,
                    "part_title": part_title,
                    "chapter_id": chapter_id,
                    "title": title,
                    "live_file": file_path,
                    "generated_reader_file": f"build/reader_edition/{file_path}",
                }
            )
    return rows


def active_overlay_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in sorted(OVERLAY_CHAPTER_DIR.glob("*.json")):
        data = load_json(path, {})
        if not isinstance(data, dict):
            continue
        target = data.get("target_file")
        if not isinstance(target, str):
            continue
        for operation in data.get("operations", []):
            if isinstance(operation, dict) and operation.get("status") == "active":
                counts[target] += 1
    return counts


def blocked_reader_formats() -> list[str]:
    matrix = load_json(FORMAT_MATRIX_PATH, {})
    if not isinstance(matrix, dict):
        return ["format_review_matrix_invalid"]
    blockers: list[str] = []
    if matrix.get("release_record_status") != "created":
        blockers.append("reader_release_record_not_created")
    records = matrix.get("records")
    if not isinstance(records, list) or not records:
        blockers.append("format_review_matrix_empty")
        return sorted(set(blockers))
    for record in records:
        if not isinstance(record, dict):
            blockers.append("format_review_matrix_invalid_record")
            continue
        fmt = str(record.get("format", "unknown"))
        if record.get("release_approved") is not True or record.get("release_blockers"):
            blockers.append(fmt)
    return sorted(set(blockers))


def initial_review_defaults(row: dict[str, str], overlay_count: int) -> dict[str, object]:
    chapter_id = row["chapter_id"]
    if chapter_id in SPECIAL_REVIEW_DEFAULTS:
        special = dict(SPECIAL_REVIEW_DEFAULTS[chapter_id])
        special["release_blockers"] = [
            "full_chapter_review_not_recorded",
            "reader_release_record_not_created",
            "format_artifact_not_reviewed",
        ]
        return special

    manuscript_text = read_text(MANUSCRIPT_REVIEW)
    generated_path = row["generated_reader_file"]
    spot_checked = generated_path in manuscript_text
    dispositions = ["reader_overlay_active"] if overlay_count else ["none"]
    return {
        "review_status": "spot_checked" if spot_checked else "not_started",
        "review_depth": "representative_spot_check" if spot_checked else "none",
        "dispositions": dispositions,
        "review_refs": ["docs/reader_manuscript_review.md#generated-baseline"] if spot_checked else [],
        "review_notes": (
            "Representative generated-reader spot check recorded; still needs full chapter review."
            if spot_checked
            else "Awaiting full human-reader continuity review."
        ),
        "release_blockers": [
            "full_chapter_review_not_recorded",
            "reader_release_record_not_created",
            "format_artifact_not_reviewed",
        ],
    }


def merge_row(
    row: dict[str, str],
    existing_by_id: dict[str, dict[str, object]],
    overlay_count: int,
) -> dict[str, object]:
    existing = existing_by_id.get(row["chapter_id"], {})
    defaults = initial_review_defaults(row, overlay_count)

    dispositions = existing.get("dispositions", defaults["dispositions"])
    if isinstance(dispositions, list):
        dispositions = [str(item) for item in dispositions]
    else:
        dispositions = list(defaults["dispositions"])
    if overlay_count and "reader_overlay_active" not in dispositions:
        if dispositions == ["none"]:
            dispositions = []
        dispositions.insert(0, "reader_overlay_active")
    if not dispositions:
        dispositions = ["none"]

    review_refs = existing.get("review_refs", defaults["review_refs"])
    if not isinstance(review_refs, list):
        review_refs = list(defaults["review_refs"])

    release_blockers = existing.get("release_blockers", defaults["release_blockers"])
    if not isinstance(release_blockers, list):
        release_blockers = list(defaults["release_blockers"])

    synced: dict[str, object] = {
        **row,
        "overlay_operation_count": overlay_count,
        "review_status": existing.get("review_status", defaults["review_status"]),
        "review_depth": existing.get("review_depth", defaults["review_depth"]),
        "dispositions": dispositions,
        "review_refs": review_refs,
        "review_notes": existing.get("review_notes", defaults["review_notes"]),
        "release_blockers": release_blockers,
    }
    return synced


def build_matrix() -> dict[str, object]:
    manifest_rows = flatten_manifest()
    existing = load_json(MATRIX_PATH, {})
    existing_rows: list[dict[str, object]] = []
    if isinstance(existing, dict) and isinstance(existing.get("chapters"), list):
        existing_rows = [row for row in existing["chapters"] if isinstance(row, dict)]
    existing_by_id = {
        str(row.get("chapter_id")): row
        for row in existing_rows
        if isinstance(row.get("chapter_id"), str)
    }

    overlay_counts = active_overlay_counts()
    chapters = [
        merge_row(row, existing_by_id, overlay_counts[row["live_file"]])
        for row in manifest_rows
    ]

    status_counts = Counter(str(row["review_status"]) for row in chapters)
    disposition_counts: Counter[str] = Counter()
    release_blocker_counts: Counter[str] = Counter()
    for row in chapters:
        for disposition in row["dispositions"]:
            disposition_counts[str(disposition)] += 1
        for blocker in row["release_blockers"]:
            release_blocker_counts[str(blocker)] += 1

    last_updated = "2026-06-28"
    if isinstance(existing, dict) and isinstance(existing.get("last_updated"), str):
        last_updated = existing["last_updated"]
    elif MATRIX_PATH.exists():
        last_updated = date.today().isoformat()

    return {
        "schema_version": "0.1",
        "major_version": "v1.0",
        "status": "active_review_queue",
        "last_updated": last_updated,
        "source_of_truth": "book_structure.json",
        "generated_reader_baseline": {
            "command": "python3 scripts/build_reader_edition.py",
            "workspace": "build/reader_edition",
            "policy": "Review generated reader source and overlays before graduating any curated reader manuscript chapter.",
        },
        "format_review_matrix": {
            "path": "editions/reader_manuscript/v1_0/format_review_matrix.json",
            "summary": "docs/reader_format_review_matrix.md",
            "check_command": "python3 scripts/sync_reader_format_review_matrix.py --check",
            "policy": "Keep chapter format-artifact blockers until every required reader format row is approved and an edition release record exists.",
        },
        "review_status_counts": dict(sorted(status_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "release_blocker_counts": dict(sorted(release_blocker_counts.items())),
        "release_rule": (
            "No reader, ebook, document, PDF, audio, or curated manuscript release "
            "can use a chapter until its review status and blockers are reconciled "
            "in a release record."
        ),
        "chapters": chapters,
        "non_claims": [
            "This matrix is a reader-review queue, not a reviewed reader release.",
            "This matrix does not create EPUB, PDF, DOCX, HTML, audio, or audio-embedded EPUB artifacts.",
            "This matrix does not promote any claim support state.",
            "This matrix does not supersede the live Quarto book for claims, source boundaries, proof/test status, implementation horizons, or release records.",
        ],
    }


def validate_matrix(matrix: dict[str, object]) -> list[str]:
    errors: list[str] = []
    manifest_rows = flatten_manifest()
    manifest_ids = [row["chapter_id"] for row in manifest_rows]
    manifest_by_id = {row["chapter_id"]: row for row in manifest_rows}
    overlay_counts = active_overlay_counts()

    if matrix.get("schema_version") != "0.1":
        errors.append("chapter_review_matrix.schema_version must be 0.1.")
    if matrix.get("major_version") != "v1.0":
        errors.append("chapter_review_matrix.major_version must be v1.0.")
    if matrix.get("status") != "active_review_queue":
        errors.append("chapter_review_matrix.status must be active_review_queue.")
    if matrix.get("source_of_truth") != "book_structure.json":
        errors.append("chapter_review_matrix.source_of_truth must be book_structure.json.")
    format_ref = matrix.get("format_review_matrix")
    if not isinstance(format_ref, dict):
        errors.append("chapter_review_matrix.format_review_matrix must be an object.")
    else:
        expected_format_ref = {
            "path": "editions/reader_manuscript/v1_0/format_review_matrix.json",
            "summary": "docs/reader_format_review_matrix.md",
            "check_command": "python3 scripts/sync_reader_format_review_matrix.py --check",
        }
        for key, expected in expected_format_ref.items():
            if format_ref.get(key) != expected:
                errors.append(f"chapter_review_matrix.format_review_matrix.{key} must be {expected}.")
        policy = format_ref.get("policy")
        if not isinstance(policy, str) or "format-artifact blockers" not in policy or "edition release record" not in policy:
            errors.append("chapter_review_matrix.format_review_matrix.policy must mention format-artifact blockers and edition release record.")
    for phrase in ("does not promote", "does not supersede", "does not create"):
        if phrase not in " ".join(str(item) for item in matrix.get("non_claims", [])).lower():
            errors.append(f"chapter_review_matrix.non_claims must include phrase: {phrase}")

    chapters = matrix.get("chapters")
    if not isinstance(chapters, list):
        errors.append("chapter_review_matrix.chapters must be a list.")
        return errors
    format_blockers = blocked_reader_formats()

    ids = [row.get("chapter_id") for row in chapters if isinstance(row, dict)]
    if ids != manifest_ids:
        errors.append("chapter_review_matrix chapter order must exactly match book_structure.json.")
    if len(ids) != len(set(ids)):
        errors.append("chapter_review_matrix has duplicate chapter_id values.")

    for index, row in enumerate(chapters):
        owner = f"chapters[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{owner} must be an object.")
            continue
        chapter_id = row.get("chapter_id")
        if not isinstance(chapter_id, str) or chapter_id not in manifest_by_id:
            errors.append(f"{owner}.chapter_id must reference a manifest chapter.")
            continue
        manifest_row = manifest_by_id[chapter_id]
        for key in ("part_id", "part_title", "title", "live_file", "generated_reader_file"):
            if row.get(key) != manifest_row[key]:
                errors.append(f"{owner}.{key} must match book_structure.json-derived value.")
        expected_overlay_count = overlay_counts[manifest_row["live_file"]]
        if row.get("overlay_operation_count") != expected_overlay_count:
            errors.append(f"{owner}.overlay_operation_count must be {expected_overlay_count}.")
        if row.get("review_status") not in ALLOWED_REVIEW_STATUS:
            errors.append(f"{owner}.review_status must be one of {sorted(ALLOWED_REVIEW_STATUS)}.")
        if row.get("review_depth") not in ALLOWED_REVIEW_DEPTH:
            errors.append(f"{owner}.review_depth must be one of {sorted(ALLOWED_REVIEW_DEPTH)}.")
        dispositions = row.get("dispositions")
        if not isinstance(dispositions, list) or not dispositions:
            errors.append(f"{owner}.dispositions must be a non-empty list.")
        else:
            unknown = sorted(set(str(item) for item in dispositions) - ALLOWED_DISPOSITIONS)
            if unknown:
                errors.append(f"{owner}.dispositions has unknown values: {unknown}")
            if "none" in dispositions and len(dispositions) > 1:
                errors.append(f"{owner}.dispositions cannot combine none with other dispositions.")
            if expected_overlay_count and "reader_overlay_active" not in dispositions:
                errors.append(f"{owner}.dispositions must include reader_overlay_active.")
        for list_key in ("review_refs", "release_blockers"):
            values = row.get(list_key)
            if not isinstance(values, list):
                errors.append(f"{owner}.{list_key} must be a list.")
                continue
            if list_key == "release_blockers":
                unknown = sorted(set(str(item) for item in values) - ALLOWED_RELEASE_BLOCKERS)
                if unknown:
                    errors.append(f"{owner}.release_blockers has unknown values: {unknown}")
                if format_blockers and "format_artifact_not_reviewed" not in values:
                    errors.append(
                        f"{owner}.release_blockers must include format_artifact_not_reviewed "
                        f"while reader format blockers remain: {format_blockers}"
                    )
        notes = row.get("review_notes")
        if not isinstance(notes, str) or not notes.strip():
            errors.append(f"{owner}.review_notes must be a non-empty string.")
        if row.get("review_status") == "reviewed" and "full_chapter_review_not_recorded" in row.get("release_blockers", []):
            errors.append(f"{owner} cannot be reviewed while full_chapter_review_not_recorded remains.")

    if isinstance(chapters, list):
        actual_status_counts = Counter(
            str(row.get("review_status"))
            for row in chapters
            if isinstance(row, dict)
        )
        actual_disposition_counts: Counter[str] = Counter()
        actual_release_blocker_counts: Counter[str] = Counter()
        for row in chapters:
            if not isinstance(row, dict):
                continue
            for disposition in row.get("dispositions", []):
                actual_disposition_counts[str(disposition)] += 1
            for blocker in row.get("release_blockers", []):
                actual_release_blocker_counts[str(blocker)] += 1
        expected_counts = {
            "review_status_counts": dict(sorted(actual_status_counts.items())),
            "disposition_counts": dict(sorted(actual_disposition_counts.items())),
            "release_blocker_counts": dict(sorted(actual_release_blocker_counts.items())),
        }
        for key, expected in expected_counts.items():
            if matrix.get(key) != expected:
                errors.append(f"chapter_review_matrix.{key} must equal {expected}.")

    return errors


def markdown_table(matrix: dict[str, object]) -> str:
    chapters = matrix.get("chapters", [])
    status_counts = matrix.get("review_status_counts", {})
    disposition_counts = matrix.get("disposition_counts", {})
    release_blocker_counts = matrix.get("release_blocker_counts", {})
    lines = [
        "# Reader Chapter Review Matrix",
        "",
        f"Last updated: {matrix.get('last_updated')}",
        "",
        "This document is generated from `editions/reader_manuscript/v1_0/chapter_review_matrix.json` by `python3 scripts/sync_reader_chapter_review_matrix.py --write`.",
        "",
        "It is a Phase 2 review-control surface for the normal human-reader manuscript. It is not a reader release, not an ebook/document/PDF/audio release, and not a support-state promotion.",
        "",
        "Format-artifact blockers are reconciled against `editions/reader_manuscript/v1_0/format_review_matrix.json`; chapter rows cannot clear `format_artifact_not_reviewed` while reader formats or the edition release record remain blocked.",
        "",
        "## Counts",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    if isinstance(status_counts, dict):
        for key, value in sorted(status_counts.items()):
            lines.append(f"| review_status:{key} | {value} |")
    if isinstance(disposition_counts, dict):
        for key, value in sorted(disposition_counts.items()):
            lines.append(f"| disposition:{key} | {value} |")
    if isinstance(release_blocker_counts, dict):
        for key, value in sorted(release_blocker_counts.items()):
            lines.append(f"| release_blocker:{key} | {value} |")

    lines.extend(
        [
            "",
            "## Chapter Queue",
            "",
            "| Part | Chapter | Review status | Depth | Overlays | Dispositions | Release blockers |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for row in chapters if isinstance(chapters, list) else []:
        if not isinstance(row, dict):
            continue
        dispositions = ", ".join(str(item) for item in row.get("dispositions", []))
        blockers = ", ".join(str(item) for item in row.get("release_blockers", []))
        lines.append(
            "| "
            f"{row.get('part_title')} | "
            f"`{row.get('chapter_id')}` | "
            f"{row.get('review_status')} | "
            f"{row.get('review_depth')} | "
            f"{row.get('overlay_operation_count')} | "
            f"{dispositions} | "
            f"{blockers} |"
        )

    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
        ]
    )
    for item in matrix.get("non_claims", []):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(matrix: dict[str, object]) -> None:
    MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    MATRIX_PATH.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(markdown_table(matrix), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write synced JSON and Markdown outputs")
    parser.add_argument("--check", action="store_true", help="fail if synced outputs differ")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.write and args.check:
        raise SystemExit("Use either --write or --check, not both.")
    matrix = build_matrix()
    errors = validate_matrix(matrix)
    if errors:
        print("Reader chapter review matrix validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    if args.write:
        write_outputs(matrix)
        print(
            "Reader chapter review matrix synced: "
            f"{len(matrix['chapters'])} chapters, "
            f"{matrix['review_status_counts']}"
        )
        return

    if args.check:
        current_matrix = MATRIX_PATH.read_text(encoding="utf-8") if MATRIX_PATH.exists() else ""
        expected_matrix = json.dumps(matrix, indent=2) + "\n"
        current_doc = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else ""
        expected_doc = markdown_table(matrix)
        if current_matrix != expected_matrix or current_doc != expected_doc:
            print("Reader chapter review matrix is out of sync. Run:")
            print("  python3 scripts/sync_reader_chapter_review_matrix.py --write")
            sys.exit(1)
        print(
            "Reader chapter review matrix validation passed: "
            f"{len(matrix['chapters'])} chapters, "
            f"{matrix['review_status_counts']}"
        )
        return

    print(json.dumps(matrix, indent=2))


if __name__ == "__main__":
    main()
