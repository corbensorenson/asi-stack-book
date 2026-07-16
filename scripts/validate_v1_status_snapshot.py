#!/usr/bin/env python3
"""Validate headline counts in docs/v1_0_candidate_status.md.

The v1.0 status page is a public-safe release surface. This script checks
that its snapshot counts still match the current repository artifacts; it does
not strengthen any chapter core claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import sys
from pathlib import Path

import validate_release_surface_status_ledger as release_surface_ledger
import validate_test_harness_status_ledger as test_harness_ledger
import validate_non_infrastructure_measured_slice_status_ledger as non_infra_ledger
import validate_project_theseus_static_import_status_ledger as theseus_static_ledger
import validate_live_human_view_status_ledger as live_human_ledger
import validate_compact_gvr_status_ledger as compact_gvr_ledger


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n?", re.DOTALL)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
HUMAN_BLOCK_RE = re.compile(r"::: \{\.asi-human-only\}\n## Human Reading Path\n\n(.*?)\n:::", re.DOTALL)
TEMPLATE_BRIDGE_PHRASES = (
    "The useful",
    "The practical",
    "The point is",
    "useful only when",
    "The mature test",
    "The mature version is",
    "the book",
    "this book",
    "Part I",
    "Part II",
    "Part III",
    "Part IV",
    "previous chapter",
    "previous chapters",
    "previous layers",
    "first two chapters",
    "first half",
    "closing move",
    "begins by",
    "ended by",
)
ADEQUACY_ORDER = [
    "adequate finite-record invariant",
    "useful but too narrow",
    "needs richer state-machine or review semantics",
    "needs executable tests first",
    "needs empirical or baseline tests first",
    "research-agenda until artifact import",
]


def fail(errors: list[str]) -> None:
    print("v1.0 status snapshot validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def chapter_word_counts() -> tuple[int, int, int]:
    chapter_files = sorted((ROOT / "chapters").glob("*.qmd"))
    body_words = 0
    raw_words = 0
    for path in chapter_files:
        text = path.read_text(encoding="utf-8")
        raw_words += len(WORD_RE.findall(text))
        body_words += len(WORD_RE.findall(FRONT_MATTER_RE.sub("", text, count=1)))
    return len(chapter_files), body_words, raw_words


def summary_metric(path: Path, metric: str) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"^\|\s*{re.escape(metric)}\s*\|\s*(.*?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section(text: str, start: str, end: str) -> str:
    if start not in text:
        return ""
    body = text.split(start, 1)[1]
    if end in body:
        body = body.split(end, 1)[0]
    return body


def sync_dynamic_table_rows(status_text: str, expected_fragments: list[str]) -> str:
    """Replace calculated count cells without disturbing static evidence cells."""
    dynamic_labels = {
        "Book structure",
        "Manifest claim contract",
        "Manuscript scale",
        "Source inventory",
        "Claim/source traceability",
        "Support states",
        "External SOTA positioning",
        "Proof envelope",
        "Schemas and fixtures",
        "Implementation horizons",
        "Chapter handoffs",
        "Live Human view",
    }
    updated = status_text
    for fragment in expected_fragments:
        if not fragment.startswith("|"):
            continue
        cells = table_cells(fragment)
        if len(cells) < 2:
            continue
        label = cells[0]
        if label not in dynamic_labels:
            continue
        state = cells[1]
        pattern = re.compile(
            rf"^(\|\s*{re.escape(label)}\s*\|)\s*[^|]*(\|.*)$",
            re.MULTILINE,
        )
        updated, count = pattern.subn(rf"\1 {state} \2", updated, count=1)
        if count != 1:
            raise ValueError(
                f"{STATUS.relative_to(ROOT)}: expected one dynamic table state cell labelled {label!r}, found {count}"
            )
    return updated


def parse_proof_adequacy_counts() -> Counter[str]:
    text = (ROOT / "docs" / "proof_adequacy_review.md").read_text(encoding="utf-8")
    counts: Counter[str] = Counter()
    body = section(text, "## Summary", "The reviewed targets")
    for line in body.splitlines():
        if not line.startswith("| ") or line.startswith("|---") or "Adequacy class" in line:
            continue
        cells = table_cells(line)
        if len(cells) < 2:
            continue
        try:
            counts[cells[0]] = int(cells[1].replace(",", ""))
        except ValueError:
            continue
    return counts


def proof_adequacy_phrase(counts: Counter[str]) -> str:
    parts = [f"{counts.get(adequacy_class, 0)} `{adequacy_class}`" for adequacy_class in ADEQUACY_ORDER]
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def leading_count(value: str | None) -> str:
    if value is None:
        return "missing"
    match = re.search(r"\d+", value)
    return match.group(0) if match else "missing"


def human_bridge_metrics(chapters: list[dict]) -> tuple[int, int, int, int]:
    values: list[int] = []
    opening_values: list[int] = []
    closing_values: list[int] = []
    template_phrase_hits = 0
    for chapter in chapters:
        path = ROOT / str(chapter.get("file", ""))
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = HUMAN_BLOCK_RE.search(text)
        if not match:
            continue
        bridge_text = re.sub(r"\s+", " ", match.group(1).strip())
        normalized_bridge = bridge_text.lower()
        template_phrase_hits += sum(normalized_bridge.count(phrase.lower()) for phrase in TEMPLATE_BRIDGE_PHRASES)
        values.append(len(WORD_RE.findall(bridge_text)))
        sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", bridge_text) if sentence.strip()]
        if sentences:
            opening_values.append(len(WORD_RE.findall(sentences[0])))
            closing_values.append(len(WORD_RE.findall(sentences[-1])))
    return (
        min(values) if values else 0,
        min(opening_values) if opening_values else 0,
        min(closing_values) if closing_values else 0,
        template_phrase_hits,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="refresh calculated dynamic table rows in the public status snapshot",
    )
    args = parser.parse_args()
    errors: list[str] = []
    status_text = STATUS.read_text(encoding="utf-8")
    structure = load_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    appendices = structure.get("appendices", [])
    front_matter = structure.get("front_matter", [])
    book_page_count = len(front_matter) + len(chapters) + len(appendices)
    source_records = load_json(ROOT / "sources" / "source_inventory.json")
    proof_manifest = load_json(ROOT / "proofs" / "proof_manifest.json")
    reader_manifest = load_json(ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json")
    if not isinstance(source_records, list):
        fail(["sources/source_inventory.json must contain a list."])
    if not isinstance(proof_manifest, dict):
        fail(["proofs/proof_manifest.json must contain an object."])
    if not isinstance(reader_manifest, dict):
        fail(["editions/reader_manuscript/v1_0/manifest.json must contain an object."])

    chapter_file_count, body_words, raw_words = chapter_word_counts()
    source_note_ids = {
        path.stem
        for path in (ROOT / "sources" / "source_notes").glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    source_ids = {str(record.get("id", "")) for record in source_records}
    missing_notes = sorted(source_ids - source_note_ids)
    evidence_counts = Counter(str(chapter.get("evidence_level", "")) for chapter in chapters)
    claim_label_counts = Counter(str(chapter.get("claim_label", "")) for chapter in chapters)
    schema_count = len(list((ROOT / "schemas").glob("*.schema.json")))
    fixture_count = len(list((ROOT / "tests" / "fixtures" / "protocol_records").glob("*.json")))
    release_count = len(list((ROOT / "release_records").glob("*.json")))
    (
        human_min_words,
        human_min_opening_words,
        human_min_closing_words,
        human_template_phrase_hits,
    ) = human_bridge_metrics(chapters)

    assigned_pairs = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Assigned source/chapter pairs")
    exact_mappings = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Exact claim-source mappings")
    passage_reviewed = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Passage-reviewed mappings recorded")
    accepted_core_transitions = summary_metric(
        ROOT / "docs" / "core_claim_transition_coverage.md",
        "Accepted core evidence-transition records",
    )
    accepted_no_promotion = summary_metric(
        ROOT / "docs" / "core_claim_transition_coverage.md",
        "Accepted explicit no-promotion decisions",
    )
    accepted_non_core_upward = leading_count(
        summary_metric(ROOT / "docs" / "non_core_evidence_ledger.md", "Accepted non-core upward transitions")
    )
    accepted_side_lane_blocks = leading_count(
        summary_metric(ROOT / "docs" / "non_core_evidence_ledger.md", "Accepted no-promotion side-lane decisions")
    )
    proof_targets = str(proof_manifest.get("proof_target_count", ""))
    proof_status_counts = proof_manifest.get("status_counts", {})
    implemented_proof_targets = int(proof_status_counts.get("implemented", 0))
    planned_proof_targets = int(proof_status_counts.get("planned", 0))
    proof_adequacy_counts = parse_proof_adequacy_counts()
    proof_adequacy_summary = proof_adequacy_phrase(proof_adequacy_counts)
    curated_records = reader_manifest.get("chapter_records", [])
    if not isinstance(curated_records, list):
        fail(["reader manuscript manifest chapter_records must contain a list."])
    curated_status_counts = Counter(
        str(record.get("reconciliation_status", "missing"))
        for record in curated_records
        if isinstance(record, dict)
    )
    curated_status_parts = [
        f"{curated_status_counts.get('drafting', 0)} drafting",
        f"{curated_status_counts.get('reconciled', 0)} reconciled",
    ]
    curated_status_parts.extend(
        f"{curated_status_counts[status]} {status}"
        for status in ("blocked", "not_started", "missing")
        if curated_status_counts.get(status)
    )
    curated_status_summary = ", ".join(curated_status_parts)
    reader_reviewed = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "review_status:reviewed")
    reader_overlay_active = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:reader_overlay_active")
    reader_no_action = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:no_immediate_action")
    reader_companion = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:companion_note_candidate")
    reader_curated = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:curated_manuscript_candidate")
    reader_high_priority = summary_metric(
        ROOT / "docs" / "reader_continuity_audit.md",
        "High-priority heuristic review chapters",
    )
    reader_medium_priority = summary_metric(
        ROOT / "docs" / "reader_continuity_audit.md",
        "Medium-priority heuristic review chapters",
    )
    reader_overlay_operation_count = 0
    reader_overlay_operation_chapters: set[str] = set()
    overlay_dir = ROOT / "editions" / "reader_overlays" / "v1_0" / "chapters"
    for overlay_path in sorted(overlay_dir.glob("*.json")):
        overlay_record = load_json(overlay_path)
        target_file = str(overlay_record.get("target_file", ""))
        operations = overlay_record.get("operations", [])
        if not isinstance(operations, list):
            continue
        active_count = sum(1 for op in operations if isinstance(op, dict) and op.get("status") == "active")
        if active_count:
            reader_overlay_operation_count += active_count
            reader_overlay_operation_chapters.add(target_file)

    expected_fragments = [
        f"| Book structure | {len(structure.get('parts', []))} parts, {len(chapters)} manifest-driven chapters, {len(appendices)} appendices |",
        f"| Manifest claim contract | {len(chapters)} chapters explicitly declare `claim_label` and `evidence_level`; current distribution is {claim_label_counts.get('Design rationale', 0)} `Design rationale` labels and {evidence_counts.get('argument', 0)} `argument` support states; missing or invalid values fail validation |",
        f"| Manuscript scale | {chapter_file_count} chapter files; {body_words:,} chapter words excluding YAML front matter; {raw_words:,} raw chapter-file words including metadata and live scaffolding |",
        f"| Source inventory | {len(source_records)} public-safe source records, each with a matching public source note;",
        "| Source appendix ownership | Appendix G (`Corben's Own Sources, Papers, and Local Projects`) and Appendix H (`External Sources by Other Authors`) are independent top-level appendices with explicit source-ownership boundary blocks, ownership-rule rows, and appendix-local identity rows: G contains Corben's own papers, Corben-supplied materials, recovered project records, and local project records; H contains external records and third-party literature marked `external_literature`; neither appendix renders the other source class as a second ownership row |",
        f"| Claim/source traceability | {assigned_pairs} assigned source/chapter pairs, {exact_mappings} exact claim-source mappings, {passage_reviewed} passage-reviewed mappings |",
        f"| Support states | All {evidence_counts.get('argument', 0)} chapter core claims remain at `argument`; detailed core coverage, disposition, non-core upward transitions, and no-promotion side-lane decisions live in generated ledgers. Current counts: {accepted_core_transitions} accepted core no-change records, {accepted_no_promotion} accepted explicit core no-promotion decisions, {accepted_non_core_upward} accepted narrow non-core upward transitions, {accepted_side_lane_blocks} accepted `blocks_promotion` side-lane decisions, 0 promoted core claims, and no chapter core claim support-state promotion. |",
        "`docs/core_claim_transition_coverage.md`",
        "`docs/core_claim_disposition_ledger.md`",
        "`docs/non_core_evidence_ledger.md`",
        "`python3 scripts/validate_evidence_transitions.py`",
        "`python3 scripts/validate_core_claim_decisions.py`",
        "`python3 scripts/validate_v1_x_core_claim_dispositions.py`",
        "`python3 scripts/validate_non_core_evidence_ledger.py`",
        f"| External SOTA positioning | Phase 6 placement is machine-tracked and closed for the v1.0 placement gate: {len(chapters)} of {len(chapters)} chapters have `ext_*` positioning before the Source crosswalk, 0 chapters have explicit external-baseline exceptions, 0 chapters need source-target placement, and 0 chapters need an exception or added source-noted baseline |",
        "`docs/external_sota_positioning_audit.md`",
        "`python3 scripts/validate_external_sota_positioning.py`",
        "| Test harnesses | Thirty-eight synthetic, deterministic, measured, local replay, or local artifact-import checks are wired into book validation; twenty-two are wired into the Phase 5 registry and sixteen chapter-specific/support checks are book-gate-only: the stack layer traceability audit, the artifact graph replay harness, the procedural memory loop harness, the routing decision lease harness, the cyclic memory contract harness, the context transaction memory-store harness, the simulation transfer boundary harness, the resource workflow trace harness, the resource live probe harness, the resource workload-quality probe, the resource load-stability probe, the Theseus support replay probe, the Compact GVR synthetic slice, the hive admission harness, the cognitive compilation trace harness, and the RankFold artifact import;",
        "the claim ledger revision harness checks 5 valid and 7 expected-invalid claim-ledger/belief-revision fixtures",
        "the proof-carrying claim harness checks 3 valid and 5 expected-invalid proof-carrying-claim fixtures",
        "the tribunal review harness checks 3 valid and 5 expected-invalid tribunal-review fixtures",
        "the value conflict harness checks 3 valid and 5 expected-invalid value-conflict fixtures",
        "the constitutional alignment harness checks 3 valid and 5 expected-invalid constitutional-predicate fixtures",
        "the governance rights harness checks 3 valid and 5 expected-invalid governance-right fixtures",
        "the agency rights harness checks 3 valid and 6 expected-invalid agency-right checklist fixtures",
        "the security kernel harness checks 3 valid and 8 expected-invalid authority-use receipt fixtures",
        "the stable capability fields harness checks 3 valid and 6 expected-invalid stable-capability-field fixtures",
        "the capability replacement harness checks 5 valid and 9 expected-invalid replacement-transaction fixtures",
        "the self-improvement boundary harness checks 3 valid and 10 expected-invalid self-improvement-transition fixtures",
        "the stack layer traceability audit checks 1 layer-boundary fixture, 6 mapped source(s), and 44 claim row(s)",
        "the plan-execution contract harness checks 3 valid and 10 expected-invalid command-contract, plan-graph, DAG, semantic-atom, typed-job, optional intent-origin, field-confidence, and inferred-authority fixtures",
        "the cognitive compilation trace harness checks 2 valid and 4 expected-invalid Cognitive Compilation trace fixtures",
        "the artifact graph replay harness checks 2 valid and 6 expected-invalid artifact-graph replay fixtures",
        "the procedural memory loop harness checks 3 valid and 6 expected-invalid procedural-memory fixtures",
        "the routing decision lease harness checks 3 valid and 7 expected-invalid routing lease fixtures",
        "the cyclic memory contract harness checks 3 valid and 6 expected-invalid cyclic-memory contract fixtures",
        "the context transaction memory-store harness checks 3 valid and 6 expected-invalid context-transaction memory-store fixtures",
        "the generation mode baseline harness checks 2 valid and 4 expected-invalid generation-mode/resource-budget fixtures",
        "the resource budget ledger harness checks 6 valid and 7 expected-invalid Resource Budget Record fixtures",
        "the resource workflow trace harness checks 1 valid and 5 expected-invalid multi-step Resource Economics workflow fixtures",
        "the resource live probe harness checks 5 local Resource Economics validator replays",
        "the resource workload-quality probe checks 3 local route candidates across 5 measured samples each",
        "the resource load-stability probe checks a 10-task local synthetic burst-review workload",
        "the Theseus support replay probe checks 2 local Project Theseus validator replays",
        "the Compact GVR synthetic slice checks 5 compact-generation receipt records",
        "the RankFold artifact import checks 3 existing local RankFold `.rfa` archive observations over a 100,000,000-byte decoded artifact digest",
        "the hive admission harness checks 2 valid and 8 expected-invalid Personal Compute Hive admission fixtures",
        "the simulation transfer boundary harness checks 3 valid and 6 expected-invalid simulation-transfer fixtures",
        "the reference trace harness checks 2 valid and 6 expected-invalid reference-trace fixtures",
        "the capacity smoothing toy harness checks 3 valid and 6 expected-invalid bounded-capacity trace fixtures",
        "`docs/claim_ledger_revision_harness.md`",
        "`python3 scripts/validate_claim_ledger_revision.py`",
        "`experiments/claim_ledger_revision/`",
        "`docs/proof_carrying_claim_harness.md`",
        "`python3 scripts/validate_proof_carrying_claims.py`",
        "`experiments/proof_carrying_claims/`",
        "`docs/tribunal_review_harness.md`",
        "`python3 scripts/validate_tribunal_review.py`",
        "`experiments/tribunal_review/`",
        "`docs/value_conflict_harness.md`",
        "`python3 scripts/validate_value_conflicts.py`",
        "`experiments/value_conflicts/`",
        "`docs/constitutional_alignment_harness.md`",
        "`python3 scripts/validate_constitutional_alignment.py`",
        "`experiments/constitutional_alignment/`",
        "`docs/governance_rights_harness.md`",
        "`python3 scripts/validate_governance_rights.py`",
        "`experiments/governance_rights/`",
        "`docs/agency_rights_harness.md`",
        "`python3 scripts/validate_agency_rights.py`",
        "`experiments/agency_rights/`",
        "`docs/support_state_transition_harness.md`",
        "`python3 scripts/validate_support_state_transitions.py`",
        "`docs/authority_transition_harness.md`",
        "`python3 scripts/validate_authority_transitions.py`",
        "`docs/security_kernel_harness.md`",
        "`python3 scripts/validate_security_kernel.py`",
        "`experiments/security_kernel/`",
        "`docs/stable_capability_field_harness.md`",
        "`python3 scripts/validate_stable_capability_fields.py`",
        "`experiments/stable_capability_fields/`",
        "`docs/capability_replacement_harness.md`",
        "`python3 scripts/validate_capability_replacement.py`",
        "`experiments/capability_replacement/`",
        "`docs/self_improvement_boundary_harness.md`",
        "`python3 scripts/validate_self_improvement_boundaries.py`",
        "`experiments/self_improvement_boundaries/`",
        "`docs/stack_layer_traceability_audit.md`",
        "`python3 scripts/validate_stack_layer_traceability.py`",
        "`experiments/stack_layer_traceability/`",
        "`docs/plan_execution_contract_harness.md`",
        "`python3 scripts/validate_plan_execution_contracts.py`",
        "`docs/cognitive_compilation_trace_harness.md`",
        "`python3 scripts/validate_cognitive_compilation_traces.py`",
        "`experiments/cognitive_compilation_traces/`",
        "`docs/runtime_adapter_permission_harness.md`",
        "`python3 scripts/validate_runtime_adapter_permissions.py`",
        "`docs/artifact_graph_replay_harness.md`",
        "`docs/procedural_memory_loop_harness.md`",
        "`docs/routing_decision_lease_harness.md`",
        "`docs/cyclic_memory_contract_harness.md`",
        "`python3 scripts/validate_artifact_graph_replay.py`",
        "`python3 scripts/validate_procedural_memory_loop.py`",
        "`python3 scripts/validate_routing_decision_lease.py`",
        "`python3 scripts/validate_cyclic_memory_contracts.py`",
        "`experiments/artifact_graph_replay/`",
        "`experiments/procedural_memory_loop/`",
        "`experiments/routing_decision_lease/`",
        "`experiments/cyclic_memory_contracts/`",
        "`experiments/context_transaction_memory_store/`",
        "`docs/context_transaction_memory_store_harness.md`",
        "`python3 scripts/validate_context_transaction_memory_store.py`",
        "`docs/context_admission_adequacy_harness.md`",
        "`python3 scripts/validate_context_admission_adequacy.py`",
        "`docs/readiness_residual_harness.md`",
        "`python3 scripts/validate_readiness_residual_gates.py`",
        "`docs/benchmark_antigoodhart_harness.md`",
        "`python3 scripts/validate_benchmark_antigoodhart.py`",
        "`docs/generation_mode_baseline_harness.md`",
        "`python3 scripts/validate_generation_mode_baselines.py`",
        "`experiments/generation_mode_baselines/`",
        "`docs/resource_budget_ledger_harness.md`",
        "`python3 scripts/validate_resource_budget_ledgers.py`",
        "`docs/resource_live_probe.md`",
        "`python3 scripts/validate_resource_live_probe.py`",
        "`docs/resource_load_stability_probe.md`",
        "`python3 scripts/validate_resource_load_stability_probe.py`",
        "`docs/theseus_support_replay_probe.md`",
        "`experiments/theseus_support_replay_probe/results/2026-07-01-local.json`",
        "`python3 scripts/run_theseus_support_replay_probe.py --write-result`",
        "`python3 scripts/validate_theseus_support_replay_probe.py`",
        "`docs/simulation_transfer_boundary_harness.md`",
        "`python3 scripts/validate_simulation_transfer_boundaries.py`",
        "`docs/reference_trace_harness.md`",
        "`python3 scripts/validate_reference_trace.py`",
        "`experiments/resource_budget_ledgers/`",
        "`experiments/resource_live_probe/`",
        "`experiments/resource_load_stability_probe/`",
        "`experiments/simulation_transfer_boundaries/`",
        "`experiments/reference_trace/`",
        "`docs/capacity_smoothing_harness.md`",
        "`python3 scripts/validate_capacity_smoothing.py`",
        "`experiments/capacity_smoothing/`",
        "`docs/resource_workload_quality_probe.md`",
        "`python3 scripts/validate_resource_workload_quality_probe.py`",
        "`experiments/resource_workload_quality_probe/`",
        "`docs/resource_load_stability_probe.md`",
        "`python3 scripts/validate_resource_load_stability_probe.py`",
        "`experiments/resource_load_stability_probe/`",
        "`docs/hive_admission_harness.md`",
        "`python3 scripts/validate_hive_admission.py`",
        "`experiments/hive_admission/`",
        "| Non-infrastructure measured slice | The first bounded non-infrastructure measured/replayed slice checks four Costed Route Records and four Resource Budget Records, rejects the cheaper failed-verification negative control `route://cheap-unverified-transform`, rejects the cheaper hidden-residual negative control `route://hidden-residual-auto-merge`, keeps the adequate overkill baseline `route://frontier-manual-review` eligible, and selects `route://bounded-transform-plus-verifier` with a 66.98 percent synthetic cost reduction while preserving fallback, residual, and non-claim boundaries. The same validator checks that the finite `AsiStackProofs.ResourceEconomics` Lean fixture matches the public JSON costs, selected route, negative controls, eligibility fields, and selector-state trace theorem `costed_route_fixture_trace_selects_lowest_eligible_route`.",
        "The local Resource live probe replays five Resource Economics validators",
        "The Resource workload-quality probe records three local route candidates across five samples each",
        "The Resource load-stability probe records a 10-task local synthetic burst-review workload",
        "The Resource CI cost profile records eight actual GitHub Pages runs",
        "`docs/costed_route_resource_slice.md`",
        "`docs/resource_workflow_trace.md`",
        "`docs/resource_live_probe.md`",
        "`docs/resource_workload_quality_probe.md`",
        "`docs/resource_load_stability_probe.md`",
        "`docs/resource_ci_cost_profile.md`",
        "`experiments/costed_route_resource_slice/input/v1_0_costed_routes.json`",
        "`experiments/costed_route_resource_slice/results/2026-06-29-local.json`",
        "`experiments/resource_workflow_trace/results/2026-07-01-local.json`",
        "`experiments/resource_live_probe/results/2026-07-01-local.json`",
        "`experiments/resource_workload_quality_probe/results/2026-07-01-local.json`",
        "`experiments/resource_load_stability_probe/results/2026-07-01-local.json`",
        "`experiments/resource_ci_cost_profile/results/2026-07-04-main.json`",
        "`lean/AsiStackProofs/ResourceEconomics.lean`",
        "`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`",
        "`python3 scripts/validate_costed_route_resource_slice.py`",
        "`python3 scripts/validate_resource_workflow_trace.py`",
        "`python3 scripts/validate_resource_live_probe.py`",
        "`python3 scripts/validate_resource_workload_quality_probe.py`",
        "`python3 scripts/validate_resource_load_stability_probe.py`",
        "`python3 scripts/validate_resource_ci_cost_profile.py`",
        compact_gvr_ledger.compact_status_row(),
        "`docs/compact_gvr_status_ledger.md`",
        "`docs/compact_gvr_slice.md`",
        "`experiments/compact_gvr_slice/input/v1_x_compact_gvr_records.json`",
        "`experiments/compact_gvr_slice/results/2026-07-01-local.json`",
        "`evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json`",
        "`python3 scripts/validate_compact_gvr_status_ledger.py`",
        "`python3 scripts/validate_compact_gvr_slice.py`",
        "| Imported external prototype slice | The first bounded imported external-prototype receipt slice records a clean local Circle checkout at commit `63b0f511`, a successful `lake build Circle`, a proved and passed rope certification for `CC-AI-CONTRACT-ROPE-001`, a ready digest with 31 fields, 0 missing fields, and 75 theorems, an accepted receipt requiring seven theorem IDs plus `ROPE-USE-D19-MARGIN-FRONTIER`, and a selected receipt/contract pytest batch with 145 passing tests.",
        "`experiments/circle_external_receipt_slice/results/2026-06-29-local.json`",
        "`evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`",
        "| Project Theseus static import lane | The public-safe Project Theseus import lane now records two sanitized static report fixtures",
        "18 imported generation modes, 13 generation-mode comparisons, 0 hard gaps, 0 modes with missing report refs, 0 promotable comparisons, 0 useful-solution-per-second",
        "The support replay probe reruns both Theseus validators, records command-output digests and tracked artifact hashes, and preserves support-state effect `none`.",
        "`docs/theseus_report_import_slice.md`",
        "`experiments/theseus_import/results/2026-06-29-local.json`",
        "`python3 scripts/validate_theseus_report.py`",
        "`docs/theseus_generation_mode_import_slice.md`",
        "`schemas/theseus_generation_mode_import.schema.json`",
        "`experiments/theseus_generation_mode_import/results/2026-07-01-local.json`",
        "`lean/AsiStackProofs/FastGenerationRefinement.lean`",
        "`python3 scripts/validate_theseus_generation_mode_import.py`",
        "`docs/theseus_support_replay_probe.md`",
        "`experiments/theseus_support_replay_probe/results/2026-07-01-local.json`",
        "`python3 scripts/run_theseus_support_replay_probe.py --write-result`",
        "`python3 scripts/validate_theseus_support_replay_probe.py`",
        "The public task-bundle import records `theseus_public_task_bundle_import_2026_07_03_local`, 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 external inference calls, 12 of 12 operator gates passed, 18 of 18 benchmark gates passed, 19 residuals, 0 task-level regressions, seven expected-invalid controls, visible artifact gaps, a dirty-checkout boundary, and no clean-live-replay, model-quality, speed, useful-solution-per-second, support-state, or chapter-core-promotion claim.",
        "`docs/theseus_public_task_bundle_import.md`",
        "`experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`",
        "`python3 scripts/validate_theseus_public_task_bundle_import.py`",
        "`experiments/phase5_harness_registry.json`",
        "`docs/phase5_harness_registry.md`",
        "`python3 scripts/validate_phase5_harness_registry.py`",
        f"| Proof envelope | {proof_targets} proof targets are registered: {implemented_proof_targets} implemented as bounded finite-record Lean predicates and {planned_proof_targets} planned without a claimed theorem. The generated proof envelope ledger records traceability, adequacy classes, proof-depth metrics, and non-claim boundaries. Current adequacy: {proof_adequacy_summary}. No proof-envelope artifact promotes any chapter core claim above `argument`. |",
        "`proofs/proof_manifest.json`",
        "`docs/proof_envelope_status_ledger.md`",
        "`docs/proof_artifact_audit.md`",
        "`docs/proof_adequacy_review.md`",
        "`docs/proof_depth_classification.md`",
        "`lake build`",
        f"| Schemas and fixtures | {schema_count} JSON Schemas, {fixture_count} valid protocol fixtures, {release_count} public release records |",
        f"| Implementation horizons | {len(chapters)} generated chapter build horizons with manifest-sourced minimum viable implementation and beyond-state-of-the-art endpoint fields |",
        "browser Human-view gate checks rendered Mermaid SVG visibility; dense Mermaid diagrams keep mobile labels readable through contained diagram-block scrolling without page-level horizontal overflow",
        "| Public-site accessibility readiness | Phase 7 accessibility readiness is recorded without claiming compliance: the live-site review checks reading-mode assistive hooks, focus-visible and mobile-containment CSS, landing-image alt text, diagram walkthrough coverage, compact progress-ledger rows, residuals, and non-claims.",
        "`docs/public_site_accessibility_review.md`",
        "`docs/v1_progress_ledger.md`",
        "`python3 scripts/validate_public_site_accessibility.py`",
        "| v1.0 release gate audit | The release-gate audit records all eleven Definition-of-Done gates, the v1.0.0 source tag, source commit, GitHub Release, living-book release record, current evidence, residuals, and non-claims without creating a DOI, archive, or chapter support-state promotion.",
        "`docs/v1_0_release_gate_audit.md`",
        "`release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`",
        "`python3 scripts/validate_v1_release_gate_audit.py`",
        "| Architecture red-team | Phase 7A desk review covers six composed-system attacks: authority ladder, SCIF/context leakage, evaluator capture, support-state inflation, benchmark gaming, and reader-release laundering.",
        "`docs/architecture_red_team_review.md`",
        "`python3 scripts/validate_architecture_red_team.py`",
        "| Release reproducibility | v1.0.0 toolchain and citation metadata are now explicit: CI pins Quarto `1.9.38`, Python `3.11`, Node `22`, and Lean through `lean/lean-toolchain`; `CITATION.cff` records version `1.0.0` and DOI-pending status;",
        "source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`",
        "how to cite v1.0.0 without implying DOI, Zenodo archive, or additional approved reader artifacts",
        "`docs/release_reproducibility.md`",
        "`python3 scripts/validate_release_reproducibility.py`",
        f"| Chapter handoffs | All {len(chapters)} manifest chapters now end with reader-facing `Handoff` sections: non-final chapters name the next manifest chapter title and avoid numbered chapter references, while the final chapter closes the book-level arc; generated reader chapters must preserve the same single Handoff continuity after live-only stripping |",
        release_surface_ledger.compact_status_row(),
        "`docs/release_surface_status_ledger.md`",
        "`python3 scripts/validate_release_surface_status_ledger.py`",
        "`The book needs a place`",
        "`The book needs`",
        "`The stack needs`",
        "`The ASI Stack needs`",
        "`The problem is`",
        "`The insufficiency is`",
        "`The stack should`",
        "`The record should`",
        "`The response is`",
        "`The minimum should`",
        "`Operating mechanism:`",
        "`Failure closure:`",
        "`detect and route failure modes such as`",
        "`This is a target architecture, not a current-result claim`",
        "`remains a target architecture, not a current-result claim`",
        "`It remains beyond the chapter's present support state`",
        "`The interface is the`",
        "`The interface is a`",
        "`The interface is an`",
        "`The public schema now records`",
        "`The interface should`",
        "`The interface should also record`",
        "`The interface should distinguish`",
        "`The interface should expose`",
        "`The interface should carry`",
        "`The interface should also`",
        "`The contract should also`",
        "`None of those passages show`",
        "`The reviewed passages sharpen the`",
        "`The evidence map is narrower now`",
        "`The Lean coverage stays at`",
        "`The support state remains argument`",
        "`The passage-reviewed mappings support discussion`",
        "`The practical point is`",
        "`The practical test is`",
        "`The practical rule is`",
        "`The practical purpose is`",
        "`The practical problem is`",
        "`The subtle failure is`",
        "`The subtle failure mode is`",
        "`Another failure is`",
        "`Each failure should`",
        "`The fixture validates`",
        "`The fixture is not`",
        "`The fixture is only`",
        "`The result is`",
        "`This is why`",
        "`This matters because`",
        "`Another invariant is`",
        "`A second invariant is`",
        "`The strongest invariant is`",
        "`The key invariant is`",
        "`The invariant is`",
        "The repeated-prose guard now rejects `This is why`, so causal transitions must name the specific layer, record, authority change, or consequence directly.",
        "The repeated-prose guard now rejects `This matters because`, so causal explanations must be integrated into chapter-specific prose rather than attached as reusable explanatory scaffolding.",
        "The repeated-prose guard now rejects `The result is`, so summaries and transitions must name the actual bridge, discipline, lifecycle, or artifact path directly.",
        "The repeated-prose guard now rejects `Operating mechanism:`, the exact `remains a target architecture, not a current-result claim` disclaimer, and the reusable `keeps ... honest` cadence",
        f"All {book_page_count} rendered book pages carry the persistent and shareable `AI view` / `Human view` switch",
        "generated reader chapters strip raw live core-claim markers and repeated support boilerplate while preserving claim text and compact inline plain-language support-state boundaries",
        "all rendered pages embed the current reader-overlay payload before the reading-mode toggle and expose runtime overlay operation-count attributes after processing",
        "reader-overlay payload availability and runtime operation-count processing",
        "generated reader chapter prose rejects `this chapter`, `the chapter`, and repeated evidence-boundary paragraph openers after live-only stripping",
        "while attaching the compact evidence boundary to the visible claim text",
        "raw marker and support-boilerplate hiding/restoration",
        "generated reader chapters preserve one chapter-specific Handoff after `Summary` and now must clear section-level word-count and substantial prose-paragraph floors after stripping",
        "browser smoke validation can exercise every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports`, including reading-mode control visibility, reader-overlay payload availability and runtime operation-count processing, raw marker and support-boilerplate hiding/restoration, and horizontal-overflow checks, when Playwright/Chrome is available",
        f"bridge prose is guarded against meta-reader and meta-book scaffolding and must be at least 170 words excluding the source-only heading, must open with at least 11 words, must close with at least 11 words, must avoid known repeated bridge formulas, with the current bridge minimum at {human_min_words} words, opening-sentence minimum at {human_min_opening_words} words, closing-sentence minimum at {human_min_closing_words} words, and targeted template-phrase count at {human_template_phrase_hits}",
    ]

    old_harness_start = (
        "| Test harnesses | Thirty-eight synthetic, deterministic, measured, local replay, or local artifact-import checks are wired into book validation; "
        "twenty-two are wired into the Phase 5 registry and sixteen chapter-specific/support checks are book-gate-only: the stack layer traceability audit, "
        "the artifact graph replay harness, the procedural memory loop harness, the routing decision lease harness, the cyclic memory contract harness, "
        "the context transaction memory-store harness, the simulation transfer boundary harness, the resource workflow trace harness, the resource live probe harness, "
        "the resource workload-quality probe, the resource load-stability probe, the Theseus support replay probe, the Compact GVR synthetic slice, "
        "the hive admission harness, the cognitive compilation trace harness, and the RankFold artifact import;"
    )
    non_infra_start = (
        "| Non-infrastructure measured slice | The first bounded non-infrastructure measured/replayed slice checks four Costed Route Records and four Resource Budget Records, "
        "rejects the cheaper failed-verification negative control `route://cheap-unverified-transform`, rejects the cheaper hidden-residual negative control `route://hidden-residual-auto-merge`, "
        "keeps the adequate overkill baseline `route://frontier-manual-review` eligible, and selects `route://bounded-transform-plus-verifier` with a 66.98 percent synthetic cost reduction while preserving fallback, residual, and non-claim boundaries. "
        "The same validator checks that the finite `AsiStackProofs.ResourceEconomics` Lean fixture matches the public JSON costs, selected route, negative controls, eligibility fields, and selector-state trace theorem `costed_route_fixture_trace_selects_lowest_eligible_route`."
    )
    if old_harness_start in expected_fragments and non_infra_start in expected_fragments:
        start = expected_fragments.index(old_harness_start)
        end = expected_fragments.index(non_infra_start)
        current_harness_fragments = [
            test_harness_ledger.compact_status_row(),
            "`docs/test_harness_status_ledger.md`",
            "`python3 scripts/validate_test_harness_status_ledger.py`",
        ]
        expected_fragments = expected_fragments[:start] + current_harness_fragments + expected_fragments[end:]

    compact_gvr_start = compact_gvr_ledger.compact_status_row()
    compact_gvr_index = next(
        (index for index, fragment in enumerate(expected_fragments) if fragment.startswith(compact_gvr_start)),
        None,
    )
    if non_infra_start in expected_fragments and compact_gvr_index is not None:
        start = expected_fragments.index(non_infra_start)
        end = compact_gvr_index
        current_non_infra_fragments = [
            non_infra_ledger.compact_status_row(),
            "`docs/non_infrastructure_measured_slice_status_ledger.md`",
            "`python3 scripts/validate_non_infrastructure_measured_slice_status_ledger.py`",
        ]
        expected_fragments = expected_fragments[:start] + current_non_infra_fragments + expected_fragments[end:]

    theseus_start = "| Project Theseus static import lane | The public-safe Project Theseus import lane now records two sanitized static report fixtures"
    phase5_start = "`experiments/phase5_harness_registry.json`"
    if theseus_start in expected_fragments:
        start = expected_fragments.index(theseus_start)
        end = next(
            (index for index, fragment in enumerate(expected_fragments[start + 1 :], start + 1) if fragment == phase5_start),
            None,
        )
        if end is not None:
            current_theseus_fragments = [
                theseus_static_ledger.compact_status_row(),
                "`docs/project_theseus_static_import_status_ledger.md`",
                "`python3 scripts/validate_project_theseus_static_import_status_ledger.py`",
            ]
            expected_fragments = expected_fragments[:start] + current_theseus_fragments + expected_fragments[end:]

    live_human_start = f"All {book_page_count} rendered book pages carry the persistent and shareable `AI view` / `Human view` switch"
    live_human_index = next(
        (index for index, fragment in enumerate(expected_fragments) if fragment.startswith(live_human_start)),
        None,
    )
    if live_human_index is not None:
        current_live_human_fragments = [
            live_human_ledger.compact_status_row(),
            "`docs/live_human_view_status_ledger.md`",
            "`python3 scripts/validate_live_human_view_status_ledger.py`",
        ]
        expected_fragments = expected_fragments[:live_human_index] + current_live_human_fragments

    if args.write:
        status_text = sync_dynamic_table_rows(status_text, expected_fragments)
        STATUS.write_text(status_text, encoding="utf-8")

    if len(chapters) != chapter_file_count:
        errors.append(f"Manifest has {len(chapters)} chapters but chapters/ has {chapter_file_count} .qmd files.")
    if missing_notes:
        errors.append(f"Source inventory records missing source notes: {missing_notes}")
    if assigned_pairs is None or exact_mappings is None or passage_reviewed is None:
        errors.append("docs/source_evidence_audit.md is missing required summary metrics.")
    if not proof_targets:
        errors.append("proofs/proof_manifest.json is missing proof_target_count.")
    if human_min_words < 170:
        errors.append(f"Human Reading Path prose minimum is {human_min_words}, below 170.")
    if human_min_opening_words < 11:
        errors.append(f"Human Reading Path opening-sentence minimum is {human_min_opening_words}, below 11.")
    if human_min_closing_words < 11:
        errors.append(f"Human Reading Path closing-sentence minimum is {human_min_closing_words}, below 11.")
    if human_template_phrase_hits != 0:
        errors.append(f"Human Reading Path targeted template-phrase count is {human_template_phrase_hits}, expected 0.")

    for fragment in expected_fragments:
        if fragment not in status_text:
            errors.append(f"docs/v1_0_candidate_status.md is missing current fragment: {fragment}")

    if errors:
        fail(errors)

    print(
        "v1.0 status snapshot validation passed: "
        f"{len(chapters)} chapters, {body_words:,} body words, "
        f"{len(source_records)} sources, {proof_targets} proof targets."
    )


if __name__ == "__main__":
    main()
