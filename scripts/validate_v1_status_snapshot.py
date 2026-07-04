#!/usr/bin/env python3
"""Validate headline counts in docs/v1_0_candidate_status.md.

The v1.0 status page is a public-safe release surface. This script checks
that its snapshot counts still match the current repository artifacts; it does
not strengthen any chapter core claim.
"""

from __future__ import annotations

from collections import Counter
import json
import re
import sys
from pathlib import Path


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
    proof_targets = str(proof_manifest.get("proof_target_count", ""))
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
        f"| Support states | {evidence_counts.get('argument', 0)} chapter core claims at `argument`; the v1.0 claim-state coverage gate records {accepted_core_transitions} accepted no-change transition records plus {accepted_no_promotion} accepted explicit no-promotion decisions, the v1.x disposition ledger records {len(chapters)} per-chapter core-claim dispositions with 0 promoted core claims, and the separate measured/replayed set records four bounded `synthetic-test-backed` transitions for `living-book-methodology.phase5_harness_registry_runner`, `resource-economics.costed_route_budget_slice`, `resource-economics.finite_burst_load_smoothing_selector`, and `compact-generative-systems.compact_gvr_receipt_slice`, one bounded `empirical-test-backed` local selector transition for `resource-economics.scoped_workflow_trace_route_selector`, plus one bounded `prototype-backed` imported Circle receipt transition for `circle-calculus.external_rope_receipt_replay`; no chapter core claim support-state promotion |",
        "`docs/core_claim_transition_coverage.md`",
        "`docs/core_claim_disposition_ledger.md`",
        "`docs/first_measured_replayed_slice.md`",
        "`docs/costed_route_resource_slice.md`",
        "`docs/resource_load_stability_probe.md`",
        "`docs/resource_workload_quality_probe.md`",
        "`docs/circle_external_receipt_slice.md`",
        "`docs/compact_gvr_slice.md`",
        "`evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json`",
        "`python3 scripts/validate_evidence_transitions.py`",
        "`python3 scripts/validate_core_claim_decisions.py`",
        "`python3 scripts/validate_v1_x_core_claim_dispositions.py`",
        "`python3 scripts/validate_costed_route_resource_slice.py`",
        "`python3 scripts/validate_resource_load_stability_probe.py`",
        "`python3 scripts/validate_resource_workload_quality_probe.py`",
        "`python3 scripts/validate_circle_external_receipt_slice.py`",
        "`python3 scripts/validate_compact_gvr_slice.py`",
        "`docs/rankfold_artifact_import.md`",
        "`experiments/rankfold_artifact_import/results/2026-07-02-local.json`",
        "`python3 scripts/validate_rankfold_artifact_import.py`",
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
        "`experiments/resource_ci_cost_profile/results/2026-07-01-main.json`",
        "`lean/AsiStackProofs/ResourceEconomics.lean`",
        "`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`",
        "`python3 scripts/validate_costed_route_resource_slice.py`",
        "`python3 scripts/validate_resource_workflow_trace.py`",
        "`python3 scripts/validate_resource_live_probe.py`",
        "`python3 scripts/validate_resource_workload_quality_probe.py`",
        "`python3 scripts/validate_resource_load_stability_probe.py`",
        "`python3 scripts/validate_resource_ci_cost_profile.py`",
        "| Compact GVR synthetic slice | A bounded Compact Generative Systems receipt slice checks five tracked public-safe compact-generation records, keeps a 368-byte literal baseline, selects a 78-byte exact repeat-generator-plus-repair receipt, rejects lossy exactness, negative-rate/no-fallback, and bounded-search-overrun controls, and checks a finite `AsiStackProofs.CompactGenerativeSystems` Lean fixture bridge",
        "This supports only `compact-generative-systems.compact_gvr_receipt_slice`; it does not promote any chapter core claim",
        "`experiments/compact_gvr_slice/input/v1_x_compact_gvr_records.json`",
        "`experiments/compact_gvr_slice/results/2026-07-01-local.json`",
        "`evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json`",
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
        "`lean/AsiStackProofs/FastGeneration.lean`",
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
        f"| Proof envelope | {proof_targets} proof targets, all implemented as narrow finite-record Lean predicates; current proof adequacy review classifies 13 targets as adequate only for narrow finite-record claims, 107 useful-but-too-narrow, 18 needing richer state or review semantics, 34 needing executable tests first, 18 needing empirical or baseline tests first, and 2 remaining research-agenda until artifact import; follow-through increments add a stack-boundary trace and layer-contract admission envelope, an efficiency route/residual negative-case and claim-admission lifecycle route envelope, a compact-generation/GVR/semantic negative-case, compact-admission-route, and Compact GVR fixture-bridge envelope, an artifact-compression negative-case and admission-lifecycle route envelope, a circle proof-contract receipt/consumer negative-case envelope, a coil-attention memory negative-case envelope plus synthetic cyclic-memory harness, a cyclic-mixer adoption-boundary negative-case envelope, a living-book release-boundary and change-packet boundary negative-case envelope, a project-theseus report-boundary negative-case envelope, a readiness lifecycle negative-case and lifecycle-probe bridge envelope, a proof-envelope artifact authority negative-case envelope, a proof-carrying claim negative-case envelope, a tribunal review negative-case and lifecycle-route envelope, a corrigibility agency-correction lifecycle-route envelope, a governance-right lifecycle-route envelope, a value-conflict lifecycle-admission route envelope, a constitutional lifecycle-admission route envelope, a personal-compute hive approval/lease negative-case envelope, a finite hive-work admission lifecycle route envelope, a runtime-adapter permission, authority-ceiling, confused-deputy, sandbox-escape, dispatch-route, effect-replay fixture bridge, adversarial-boundary fixture bridge, revocation-route bridge envelope, and human-oversight degradation fixture bridge envelope plus synthetic permission and adversarial boundary harnesses, a procedural-memory generated-tool/regression lifecycle-route and synthetic-fixture bridge envelope plus synthetic loop harness, a routing/MoECOT source-boundary negative-case envelope, a finite routing-decision lifecycle route envelope, a synthetic route-lease harness, a record-aware allow/deny/escalate authority decision, lifecycle admission envelope, and authority revocation trace surface bridge, a failure incident-route and recurrence-escalation envelope, a failure-taxonomy detector-probe bridge envelope, a finite intent-resolution route envelope, an execution dispatch-route envelope, an intent-execution handoff-probe bridge envelope, a planning scheduler-state bridge envelope, a planning runtime-replan delta audit bridge envelope, a verification-bandwidth contradiction-probe bridge envelope, a claim-ledger semantic-assumption fixture bridge envelope, an adversarial-review dossier-probe bridge envelope, a command-contract missing-field/hidden-override negative-case and field-confidence route envelope, a bibliography source-record/chapter-assignment negative-case envelope, a resource/simulation budget-fidelity negative-case envelope, a semantic-lowering route envelope, a context-admission route envelope, a certificate-lifecycle route envelope, a context-transaction snapshot/branch/mount/taint/deletion/replay route envelope, a context-transaction sequence fixture bridge envelope, a verification-adequacy route envelope, a job-execution route envelope, a typed-job delivery-probe bridge envelope, a typed-job durable lifecycle probe envelope, a stable-capability lifecycle-route envelope, a replacement transaction-route envelope, a replacement identity-sequence bridge envelope, an intent-governed replacement bridge envelope, a security-kernel authority-use route envelope, a self-improvement transition-route envelope, a record-aware planning control and dispatch-route envelope, evidence-state terminal/downgrade and transition-lifecycle envelopes, a benchmark-ratchet decision envelope, an artifact-steward lifecycle/contribution/federation route envelope, finite claim-ledger record/lifecycle-route and proof-carrying-claim record envelopes, an artifact-graph provenance/replay/link route envelope, synthetic replay harness, receipt-faithfulness fixture bridge envelope, receipt repository audit bridge envelope, an epistemic-TCB fixture bridge envelope, deterministic generation-mode/resource-budget accounting coverage, a finite fast-generation acceptance-accounting negative-case, admission-lifecycle route, Theseus import fixture bridge envelopes, a Theseus report-bundle audit bridge envelope, a Theseus public task-bundle import fixture bridge, a finite fast-generation task-bundle fixture bridge envelope, a finite policy-optimization promotion-boundary and promotion-route negative-case envelope, a deterministic resource-budget ledger harness, a finite costed-route fixture and selector-state trace bridge, a finite resource-workflow trace-property bridge, a reference-trace harness and route envelope, a prototype-roadmap phase-route and phase-gate fixture bridge envelope, a capacity-smoothing toy harness, a substrate-adoption trace bridge envelope, a Theseus/Fast support-lane aggregate bridge, a Resource flagship aggregate invariant bridge, and a bounded Resource governance-tax trade-off bridge without promoting ASI Is a Stack, the Efficient ASI Hypothesis, Compact Generative Systems, Mathematical/Search Substrates, Circle Contracts, Coil Attention, CoilRA/MultiCoil/cyclic mixers, Living Book Methodology, Project Theseus, Readiness Gates, Proof Envelope, System Boundaries, Failure Modes, Human Intent, Command Contracts, Cognitive Compilation, Virtual Context ABI, Verification Bandwidth, Labor OS, Artifact Graphs, Procedural Memory, Routing Heads, Personal Compute Hives, RankFold, Stable Capability Fields, Capability Replacement, Security Kernel, Recursive Self-Improvement, Planning, Evidence States, Benchmark Ratchets, Artifact Steward Agents, Claim Ledgers, Spinoza, Runtime Adapters, Integrated Reference Architecture, Fast Generation, Policy Optimization, Prototype Roadmap, or Resource Economics above `argument` |",
        "`docs/proof_adequacy_review.md`",
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
        f"the reader release has a tracked semantic overlay manifest as the editable delta source, generated reader delta report path as review output with a zero-active-operation note or operation digests and before/after excerpts, embedded live Human-view overlay payload for major-version human-edition deltas, and a generated reader-continuity audit with {reader_high_priority} high-priority and {reader_medium_priority} medium-priority heuristic review rows",
        "The generated-reader chapter-text review queue is complete across all parts, with review records from `docs/reader_opening_full_review_pass.md` through `docs/reader_part_iv_completion_full_review_pass.md` plus first-pass matrix decisions in `docs/reader_part_i_review_pass.md`, `docs/reader_part_ii_review_pass.md`, `docs/reader_part_iii_review_pass.md`, and `docs/reader_part_iv_review_pass.md`, without treating those notes as release approval.",
        f"The synced chapter review matrix records {len(chapters)} reader-review rows with {reader_reviewed} `reviewed`, 0 `spot_checked`, 0 `not_started`, {reader_overlay_active} active-overlay chapters, {reader_no_action} no-immediate-action decisions, {reader_companion} companion-note candidates, {reader_curated} curated-manuscript candidates, and release blockers on every row until future final reader-manuscript packaging, format review, and an edition release record explicitly clear chapter-level release blockers.",
        "`docs/reader_artifact_inspection_manifest.md` records a tracked local HTML/EPUB/DOCX structural-inspection summary for ignored snapshots",
        "`docs/reader_html_artifact_browser_review.md` records a full local browser review of generated reader HTML with 118 of 118 page-view pairs passing and an exact ignored-snapshot directory digest",
        "`docs/curated_reader_format_artifact_probe.md` records the current curated-reader HTML/EPUB/DOCX/PDF structural probe with 49 HTML files, 52 EPUB XHTML entries, 61 DOCX PNG media entries, 0 SVG conversion warnings, and a 524-page PDF sample-page render while preserving release blockers",
        "`docs/reader_epub_probe_manifest.md` records the current 9,078,787-byte EPUB metadata/source-spine probe, `en-US` language metadata, sampled source-card entries, and remaining e-reader application blocker",
        "`docs/reader_docx_probe_manifest.md` records the current 514-page, 8,190,162-byte DOCX LibreOffice conversion probe, expected title/evidence-boundary/source-card text, refreshed sampled source-card pages, and remaining full-format-review blocker",
        "`docs/reader_pdf_probe_manifest.md` records the current 535-page, 8,613,924-byte PDF probe, expected title/evidence-boundary text, refreshed sampled source-card pages, and the remaining full-PDF-layout blocker",
        "`docs/reader_format_review_matrix.md` records the HTML row as release-approved against `release_records/2026-06-29-v1-reader-html-855dc277.json` while EPUB, DOCX, and PDF retain format-specific review blockers.",
        "`release_records/2026-06-29-v1-reader-html-855dc277.json`",
        f"The current v1.0 reader-overlay set carries {reader_overlay_operation_count} active operations across {len(reader_overlay_operation_chapters)} chapters for Human view and generated reader editions only.",
        f"The curated reader-manuscript manifest exists with `{reader_manifest.get('status')}` status and {len(curated_records)} curated chapter records ({curated_status_summary}); its reader handoff contract records the book thesis, part arcs, signature ideas, ten draft key-figure assets with text-equivalent chapter anchors and curated reader-manuscript placements, optional author-enrichment prompts converted into `editions/reader_manuscript/v1_0/author_enrichment_queue.json`, and chapter stakes/payoffs without release approval; retired standalone reader drafts are archived as history, and the active manifest remains a subordinate narrative derivative whose reconciliation report keeps release blockers active until format review and an edition release record exist.",
        "`editions/reader_overlays/v1_0/manifest.json`",
        "`editions/reader_manuscript/v1_0/manifest.json`",
        "`editions/reader_manuscript/v1_0/chapter_review_matrix.json`",
        "`editions/reader_manuscript/v1_0/format_review_matrix.json`",
        "`editions/reader_manuscript/v1_0/artifact_inspection_manifest.json`",
        "`editions/reader_manuscript/v1_0/curated_format_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/epub_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/docx_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/pdf_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/reconciliation_report.md`",
        "`docs/reader_chapter_review_matrix.md`",
        "`docs/reader_format_review_matrix.md`",
        "`docs/reader_artifact_inspection_manifest.md`",
        "`docs/reader_html_artifact_browser_review.md`",
        "`docs/curated_reader_format_artifact_probe.md`",
        "`docs/reader_epub_probe_manifest.md`",
        "`docs/reader_docx_probe_manifest.md`",
        "`docs/reader_pdf_probe_manifest.md`",
        "`docs/reader_opening_full_review_pass.md`",
        "`docs/reader_boundary_full_review_pass.md`",
        "`docs/reader_normative_full_review_pass.md`",
        "`docs/reader_part_i_full_review_completion.md`",
        "`docs/reader_part_ii_contracts_full_review_pass.md`",
        "`docs/reader_part_ii_context_full_review_pass.md`",
        "`docs/reader_part_ii_verification_full_review_pass.md`",
        "`docs/reader_part_ii_full_review_completion.md`",
        "`docs/reader_part_iii_opening_full_review_pass.md`",
        "`docs/reader_part_iii_compression_full_review_pass.md`",
        "`docs/reader_part_iii_representation_full_review_pass.md`",
        "`docs/reader_part_iii_iv_proof_bridge_full_review_pass.md`",
        "`docs/reader_part_iv_evidence_governance_full_review_pass.md`",
        "`docs/reader_part_iv_completion_full_review_pass.md`",
        "`docs/reader_part_i_review_pass.md`",
        "`docs/reader_part_ii_review_pass.md`",
        "`docs/reader_part_iii_review_pass.md`",
        "`docs/reader_part_iv_review_pass.md`",
        "`docs/reader_continuity_audit.md`",
        "`assets/reader-overlays.html`",
        "`python3 scripts/sync_reader_overlay_asset.py --check`",
        "`python3 scripts/validate_reader_overlays.py --check`",
        "`python3 scripts/audit_reader_continuity.py --check`",
        "`python3 scripts/validate_reader_manuscript_manifest.py`",
        "`python3 scripts/validate_reader_artifact_inspection_manifest.py`",
        "`python3 scripts/validate_curated_reader_format_probe_manifest.py`",
        "`python3 scripts/validate_reader_epub_probe_manifest.py`",
        "`python3 scripts/validate_reader_docx_probe_manifest.py`",
        "`python3 scripts/validate_reader_pdf_probe_manifest.py`",
        "`python3 scripts/sync_reader_chapter_review_matrix.py --check`",
        "`python3 scripts/sync_reader_format_review_matrix.py --check`",
        "`node scripts/validate_reader_html_artifact_browser.js --strict`",
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
        "zero-active-operation note or operation digests and before/after excerpts",
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
            "| Test harnesses | Fifty-eight synthetic, deterministic, measured, local replay, local external-project receipt, local artifact-import, or publication-governance checks are wired into book validation; twenty-two are wired into the Phase 5 registry and thirty-six chapter-specific/support checks are book-gate-only:",
            "the Theseus public task-bundle import",
            "The Theseus public task-bundle import checks `theseus_public_task_bundle_import_2026_07_03_local`, 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, 18 benchmark gates, 19 residuals, visible artifact gaps, clean live Theseus replay remains unclaimed, and no model-quality, speed, useful-solution-per-second, support-state, or chapter-core-promotion claim.",
            "`docs/theseus_public_task_bundle_import.md`",
            "`experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`",
            "`python3 scripts/validate_theseus_public_task_bundle_import.py`",
            "the living-book change-packet harness",
            "Authority revocation propagation trace",
            "the epistemic trusted computing base fixture",
            "the Human oversight degradation fixture",
            "the Partitioned authority fixture",
            "experiments/authority_revocation_trace/results/2026-07-03-local.json",
            "revoked authority receipt blocking",
            "expired approval no-mutation evidence",
            "SCIF inactive approval blocking",
            "no deployed revocation propagation",
            "The epistemic trusted computing base fixture checks `experiments/epistemic_tcb/results/2026-07-03-local.json`, 3 valid records, 6 expected-invalid controls, verifier-trust laundering rejection, outside-TCB residual preservation, no verifier-correctness claim, no deployed trust-base claim, and no support-state promotion.",
            "The Human oversight degradation fixture checks `experiments/human_oversight_degradation/results/2026-07-03-local.json`, 3 valid records, 7 expected-invalid controls, approval fatigue, rubber-stamping, alarm fatigue, automation bias, missing reviewer qualification, no approval-service quality claim, no deployed human-factors result, and no support-state promotion.",
            "The Partitioned authority fixture checks `experiments/partitioned_authority/results/2026-07-03-local.json`, 3 valid records, 6 expected-invalid controls, stale grants, revocation-delay quarantine, fresh authority receipt requirements, grant/effect race residual ownership, no-mutation evidence, CAP-style authority consistency boundaries, does not prove deployed partition tolerance, no distributed consensus or availability claim, no revocation propagation claim, and no support-state promotion.",
            "`docs/epistemic_trusted_computing_base_fixture.md`",
            "`experiments/epistemic_tcb/results/2026-07-03-local.json`",
            "`python3 scripts/validate_epistemic_trusted_computing_base.py`",
            "`docs/human_oversight_degradation_fixture.md`",
            "`experiments/human_oversight_degradation/results/2026-07-03-local.json`",
            "`python3 scripts/validate_human_oversight_degradation.py`",
            "`docs/partitioned_authority_fixture.md`",
            "`experiments/partitioned_authority/results/2026-07-03-local.json`",
            "`python3 scripts/validate_partitioned_authority_fixture.py`",
            "Living-book change-packet harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).",
            "the Benchmark anti-Goodhart fixture bridge",
            "2 valid fixtures",
            "5 expected-invalid controls",
            "one promotion-ready synthetic path",
            "one saturated-regression-floor path",
            "missing-checks rejection",
            "blocked-ratchet policy rejection",
            "reward-as-truth rejection",
            "saturated-promotion rejection",
            "release-without-approval rejection",
            "Lean fixture alignment",
            "the Circle cyclic-memory receipt slice",
            "CC-AI-CONTRACT-MEMORY-001",
            "same_residue_events=[7, 15, 23, 31]",
            "same_residue_windings=[0, 1, 2, 3]",
            "max_alias_load=4",
            "a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a",
            "3 passed in 2.51s",
            "the Runtime adapter effect replay probe",
            "valid_low_impact_local_write_effect_replay",
            "rollback-exact temp-file restoration",
            "invalid_missing_permission_no_mutation",
            "invalid_expired_approval_no_mutation",
            "without deployed-adapter, sandbox, approval-service, secret-handle, rollback-service, policy-enforcement, benchmark, or support-state-promotion claims",
            "the Artifact steward lifecycle probe",
            "valid_clean_release_review_proposal",
            "valid_sunset_review_route",
            "invalid_tainted_event_without_review",
            "invalid_over_policy_treasury_spend",
            "invalid_contribution_governance_laundering",
            "invalid_unscoped_federation_contract",
            "invalid_release_without_gate_evidence",
            "invalid_sunset_criteria_ordinary_work",
            "no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim",
            "the VCM resolver/certificate probe",
            "valid_resolver_materialization_receipt",
            "valid_mandatory_miss_typed_fault",
            "invalid_address_mismatch_materialization_denied",
            "invalid_version_mismatch_materialization_denied",
            "invalid_snapshot_mismatch_materialization_denied",
            "invalid_mount_policy_denied",
            "invalid_lease_expired_reuse_blocked",
            "invalid_certificate_source_binding_mismatch_denied",
            "invalid_certificate_authority_escalation_denied",
            "invalid_certificate_truthfulness_overclaim_denied",
            "invalid_summary_fidelity_omission_denied",
            "no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim",
            "the Intent re-contract trigger probe",
            "valid_no_material_delta_continue",
            "valid_publication_surface_delta_recontracts",
            "invalid_authority_delta_without_recontract",
            "invalid_private_source_delta_without_recontract",
            "invalid_stop_condition_erasure_without_recontract",
            "invalid_evidence_bar_weakening_without_recontract",
            "invalid_affected_party_widening_without_recontract",
            "invalid_means_expansion_without_recontract",
            "invalid_support_state_promotion_without_recontract",
            "no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim",
            "the SCIF sanitized commit replay probe",
            "valid_sanitized_commit_replay",
            "valid_prompt_injection_blocked_commit",
            "invalid_unsanitized_secret_commit_blocked",
            "invalid_handle_leak_commit_blocked",
            "invalid_missing_zeroize_commit_blocked",
            "invalid_overbroad_context_commit_blocked",
            "invalid_unapproved_destination_commit_blocked",
            "invalid_missing_residual_commit_blocked",
            "no deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, or support-state-promotion claim",
            "the Fast Generation task-bundle validation",
            "fast_generation_task_bundle_2026_07_02_local",
            "route://fast-template-verified",
            "route://autoregressive-reference",
            "route://latency-only-proxy",
            "no model-speed or deployment claim",
            "no useful-solution-per-second model claim",
            "no support-state promotion",
            "`docs/fast_generation_task_bundle.md`",
            "`experiments/fast_generation_task_bundle/results/2026-07-02-local.json`",
            "`python3 scripts/validate_fast_generation_task_bundle.py`",
            "the Prototype phase gate harness",
            "prototype_phase_gates_2026_07_02_local",
            "valid_phase_acceptance_infrastructure",
            "valid_research_only_phase_debt",
            "invalid_dependency_inversion",
            "invalid_self_improvement_without_evaluator",
            "invalid_promotion_without_transition",
            "missing non-claim boundaries",
            "`docs/prototype_phase_gate_harness.md`",
            "`experiments/prototype_phase_gates/results/2026-07-02-local.json`",
            "`python3 scripts/validate_prototype_phase_gates.py`",
            "Appendix E remains the detailed per-harness source of truth",
            "None of these harnesses promotes chapter core claims",
            "`appendices/E_codex_test_specs.qmd`",
            "`docs/benchmark_antigoodhart_harness.md`",
            "`experiments/benchmark_antigoodhart/results/2026-07-02-fixture-bridge.json`",
            "`python3 scripts/validate_benchmark_fixture_bridge.py`",
            "`docs/cyclic_memory_contract_harness.md`",
            "`docs/circle_cyclic_memory_receipt_slice.md`",
            "`experiments/circle_cyclic_memory_receipt_slice/results/2026-07-02-local.json`",
            "`python3 scripts/validate_cyclic_memory_contracts.py`",
            "`python3 scripts/validate_circle_cyclic_memory_receipt_slice.py`",
            "`docs/runtime_adapter_effect_probe.md`",
            "`experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_runtime_adapter_effect_probe.py`",
            "`docs/vcm_resolver_certificate_probe.md`",
            "`experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_vcm_resolver_certificate_probe.py`",
            "`docs/artifact_steward_lifecycle_probe.md`",
            "`experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_artifact_steward_lifecycle_probe.py`",
            "`docs/intent_recontract_probe.md`",
            "`experiments/intent_recontract_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_intent_recontract_probe.py`",
            "`docs/security_scif_commit_probe.md`",
            "`experiments/security_scif_commit_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_security_scif_commit_probe.py`",
            "`docs/rankfold_public_safe_probe.md`",
            "`experiments/rankfold_public_safe_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_rankfold_public_safe_probe.py`",
            "The RankFold public-safe replay probe records a RAW0 roundtrip-exact pack/verify/list/unpack run over a synthetic public-safe file plus a rejected single-byte archive mutation, without NeuralFold-compression, compression-advantage, codec-correctness, downstream-utility, fallback-execution, deployed-compression, or support-state-promotion claims",
            "the typed job durable lifecycle probe",
            "The Typed job durable lifecycle probe checks two valid synthetic durable lifecycle traces and nine expected-invalid controls for retry idempotency, authority preservation, permission scope, expired-lease dispatch blocking, completion receipts, replay refs, residual ownership, non-claim boundaries, and support-promotion overclaim",
            "`docs/typed_job_durable_lifecycle_probe.md`",
            "`experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json`",
            "`python3 scripts/validate_typed_job_durable_lifecycle_probe.py`",
            "the readiness lifecycle probe",
            "The Readiness lifecycle probe checks six valid synthetic readiness lifecycle transitions and twelve expected-invalid controls for non-forward jumps, missing fresh gate evidence, missing residual escrow, unsafe default readiness, quarantine leakage, missing supersession or retirement records, retired-state reuse, missing non-claim boundaries, and support-promotion overclaim",
            "`docs/readiness_lifecycle_probe.md`",
            "`experiments/readiness_lifecycle_probe/results/2026-07-02-local.json`",
            "`python3 scripts/validate_readiness_lifecycle_probe.py`",
            "`docs/rankfold_artifact_import.md`",
            "`experiments/rankfold_artifact_import/results/2026-07-02-local.json`",
            "`python3 scripts/validate_rankfold_artifact_import.py`",
            "`docs/living_book_change_packet_harness.md`",
            "`experiments/living_book_change_packets/results/2026-07-02-local.md`",
            "`python3 scripts/validate_living_book_change_packets.py`",
        ]
        expected_fragments = expected_fragments[:start] + current_harness_fragments + expected_fragments[end:]

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
