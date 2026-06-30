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
    reader_reviewed = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "review_status:reviewed")
    reader_overlay_active = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:reader_overlay_active")
    reader_no_action = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:no_immediate_action")
    reader_companion = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:companion_note_candidate")
    reader_curated = summary_metric(ROOT / "docs" / "reader_chapter_review_matrix.md", "disposition:curated_manuscript_candidate")

    expected_fragments = [
        f"| Book structure | {len(structure.get('parts', []))} parts, {len(chapters)} manifest-driven chapters, {len(appendices)} appendices |",
        f"| Manifest claim contract | {len(chapters)} chapters explicitly declare `claim_label` and `evidence_level`; current distribution is {claim_label_counts.get('Design rationale', 0)} `Design rationale` labels and {evidence_counts.get('argument', 0)} `argument` support states; missing or invalid values fail validation |",
        f"| Manuscript scale | {chapter_file_count} chapter files; {body_words:,} chapter words excluding YAML front matter; {raw_words:,} raw chapter-file words including metadata and live scaffolding |",
        f"| Source inventory | {len(source_records)} public-safe source records, each with a matching public source note;",
        "| Source appendix ownership | Appendix G (`Corben's Own Sources, Papers, and Local Projects`) and Appendix H (`External Sources by Other Authors`) are independent top-level appendices with explicit source-ownership boundary blocks, ownership-rule rows, and appendix-local identity rows: G contains Corben's own papers, Corben-supplied materials, recovered project records, and local project records; H contains external records and third-party literature marked `external_literature`; neither appendix renders the other source class as a second ownership row |",
        f"| Claim/source traceability | {assigned_pairs} assigned source/chapter pairs, {exact_mappings} exact claim-source mappings, {passage_reviewed} passage-reviewed mappings |",
        f"| Support states | {evidence_counts.get('argument', 0)} chapter core claims at `argument`; the v1.0 claim-state coverage gate records {accepted_core_transitions} accepted no-change transition records plus {accepted_no_promotion} accepted explicit no-promotion decisions, and the separate measured/replayed set records two bounded `synthetic-test-backed` transitions for `living-book-methodology.phase5_harness_registry_runner` and `resource-economics.costed_route_budget_slice` plus one bounded `prototype-backed` imported Circle receipt transition for `circle-calculus.external_rope_receipt_replay`; no chapter core claim support-state promotion |",
        "`docs/core_claim_transition_coverage.md`",
        "`docs/first_measured_replayed_slice.md`",
        "`docs/costed_route_resource_slice.md`",
        "`docs/circle_external_receipt_slice.md`",
        "`python3 scripts/validate_evidence_transitions.py`",
        "`python3 scripts/validate_core_claim_decisions.py`",
        "`python3 scripts/validate_costed_route_resource_slice.py`",
        "`python3 scripts/validate_circle_external_receipt_slice.py`",
        f"| External SOTA positioning | Phase 6 placement is machine-tracked and closed for the v1.0 placement gate: {len(chapters)} of {len(chapters)} chapters have `ext_*` positioning before the Source crosswalk, 0 chapters have explicit external-baseline exceptions, 0 chapters need source-target placement, and 0 chapters need an exception or added source-noted baseline |",
        "`docs/external_sota_positioning_audit.md`",
        "`python3 scripts/validate_external_sota_positioning.py`",
        "| Test harnesses | Twenty-one synthetic or deterministic harnesses are wired into book validation and the Phase 5 registry:",
        "the claim ledger revision harness checks 3 valid and 4 expected-invalid claim-ledger/belief-revision fixtures",
        "the proof-carrying claim harness checks 3 valid and 5 expected-invalid proof-carrying-claim fixtures",
        "the tribunal review harness checks 3 valid and 5 expected-invalid tribunal-review fixtures",
        "the value conflict harness checks 3 valid and 5 expected-invalid value-conflict fixtures",
        "the constitutional alignment harness checks 3 valid and 5 expected-invalid constitutional-predicate fixtures",
        "the governance rights harness checks 3 valid and 5 expected-invalid governance-right fixtures",
        "the agency rights harness checks 3 valid and 6 expected-invalid agency-right checklist fixtures",
        "the security kernel harness checks 3 valid and 6 expected-invalid authority-use receipt fixtures",
        "the stable capability fields harness checks 3 valid and 6 expected-invalid stable-capability-field fixtures",
        "the capability replacement harness checks 3 valid and 6 expected-invalid replacement-transaction fixtures",
        "the self-improvement boundary harness checks 3 valid and 7 expected-invalid self-improvement-transition fixtures",
        "the generation mode baseline harness checks 2 valid and 4 expected-invalid generation-mode/resource-budget fixtures",
        "the resource budget ledger harness checks 5 valid and 5 expected-invalid Resource Budget Record fixtures",
        "the capacity smoothing toy harness checks 2 valid and 3 expected-invalid bounded-capacity trace fixtures",
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
        "`docs/plan_execution_contract_harness.md`",
        "`python3 scripts/validate_plan_execution_contracts.py`",
        "`docs/runtime_adapter_permission_harness.md`",
        "`python3 scripts/validate_runtime_adapter_permissions.py`",
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
        "`experiments/resource_budget_ledgers/`",
        "`docs/capacity_smoothing_harness.md`",
        "`python3 scripts/validate_capacity_smoothing.py`",
        "`experiments/capacity_smoothing/`",
        "| Non-infrastructure measured slice | The first bounded non-infrastructure measured/replayed slice checks three Costed Route Records and three Resource Budget Records, rejects the cheaper failed negative control `route://cheap-unverified-transform`, keeps the adequate overkill baseline `route://frontier-manual-review` eligible, and selects `route://bounded-transform-plus-verifier` with a 66.98 percent synthetic cost reduction while preserving fallback, residual, and non-claim boundaries.",
        "`docs/costed_route_resource_slice.md`",
        "`experiments/costed_route_resource_slice/input/v1_0_costed_routes.json`",
        "`experiments/costed_route_resource_slice/results/2026-06-29-local.json`",
        "`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`",
        "`python3 scripts/validate_costed_route_resource_slice.py`",
        "| Imported external prototype slice | The first bounded imported external-prototype receipt slice records a clean local Circle checkout at commit `63b0f511`, a successful `lake build Circle`, a proved and passed rope certification for `CC-AI-CONTRACT-ROPE-001`, a ready digest with 31 fields, 0 missing fields, and 75 theorems, an accepted receipt requiring seven theorem IDs plus `ROPE-USE-D19-MARGIN-FRONTIER`, and a selected receipt/contract pytest batch with 145 passing tests.",
        "`experiments/circle_external_receipt_slice/results/2026-06-29-local.json`",
        "`evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`",
        "`experiments/phase5_harness_registry.json`",
        "`docs/phase5_harness_registry.md`",
        "`python3 scripts/validate_phase5_harness_registry.py`",
        f"| Proof envelope | {proof_targets} proof targets, all implemented as narrow finite-record Lean predicates; current proof adequacy review classifies 8 targets as adequate only for narrow finite-record claims, 29 useful-but-too-narrow, 20 needing richer state or review semantics, 39 needing executable tests first, 10 needing empirical or baseline tests first, and 6 remaining research-agenda until artifact import; follow-through increments add a record-aware allow/deny/escalate authority decision envelope, a record-aware planning control envelope, finite claim-ledger and proof-carrying-claim record envelopes, a synthetic runtime adapter permission harness, deterministic generation-mode/resource-budget accounting coverage, a deterministic resource-budget ledger harness, and a capacity-smoothing toy harness without promoting System Boundaries, Planning, Claim Ledgers, Spinoza, Runtime Adapters, Fast Generation, or Resource Economics above `argument` |",
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
        "the reader release has a tracked semantic overlay manifest as the editable delta source, generated reader delta report path as review output with a zero-active-operation note or operation digests and before/after excerpts, embedded live Human-view overlay payload for major-version human-edition deltas, and a generated reader-continuity audit with 0 high-priority and 3 medium-priority heuristic review rows",
        "The generated-reader chapter-text review queue is complete across all parts, with review records from `docs/reader_opening_full_review_pass.md` through `docs/reader_part_iv_completion_full_review_pass.md` plus first-pass matrix decisions in `docs/reader_part_i_review_pass.md`, `docs/reader_part_ii_review_pass.md`, `docs/reader_part_iii_review_pass.md`, and `docs/reader_part_iv_review_pass.md`, without treating those notes as release approval.",
        f"The synced chapter review matrix records {len(chapters)} reader-review rows with {reader_reviewed} `reviewed`, 0 `spot_checked`, 0 `not_started`, {reader_overlay_active} active-overlay chapters, {reader_no_action} no-immediate-action decisions, {reader_companion} companion-note candidates, {reader_curated} curated-manuscript candidates, and release blockers on every row until future final reader-manuscript packaging explicitly clears chapter-level release blockers.",
        "`docs/reader_artifact_inspection_manifest.md` records a tracked local HTML/EPUB/DOCX structural-inspection summary for ignored snapshots",
        "`docs/reader_html_artifact_browser_review.md` records a full local browser review of generated reader HTML with 118 of 118 page-view pairs passing and an exact ignored-snapshot directory digest",
        "`docs/reader_epub_probe_manifest.md` records the current 9,078,787-byte EPUB metadata/source-spine probe, `en-US` language metadata, sampled source-card entries, and remaining e-reader application blocker",
        "`docs/reader_docx_probe_manifest.md` records the current 514-page, 8,190,162-byte DOCX LibreOffice conversion probe, expected title/evidence-boundary/source-card text, refreshed sampled source-card pages, and remaining full-format-review blocker",
        "`docs/reader_pdf_probe_manifest.md` records the current 535-page, 8,613,924-byte PDF probe, expected title/evidence-boundary text, refreshed sampled source-card pages, and the remaining full-PDF-layout blocker",
        "`docs/reader_format_review_matrix.md` records the HTML row as release-approved against `release_records/2026-06-29-v1-reader-html-855dc277.json` while EPUB, DOCX, and PDF retain format-specific review blockers.",
        "`release_records/2026-06-29-v1-reader-html-855dc277.json`",
        "The current v1.0 reader-overlay set carries 33 active operations across 20 chapters for Human view and generated reader editions only.",
        f"The curated reader-manuscript manifest exists with `{reader_manifest.get('status')}` status and {len(curated_records)} drafting-only curated chapter records after the Part I consolidation; retired standalone Part I reader drafts are archived as history, and the active manifest remains a subordinate narrative derivative whose reconciliation report keeps release blockers active until reconciliation, format review, and an edition release record exist.",
        "`editions/reader_overlays/v1_0/manifest.json`",
        "`editions/reader_manuscript/v1_0/manifest.json`",
        "`editions/reader_manuscript/v1_0/chapter_review_matrix.json`",
        "`editions/reader_manuscript/v1_0/format_review_matrix.json`",
        "`editions/reader_manuscript/v1_0/artifact_inspection_manifest.json`",
        "`editions/reader_manuscript/v1_0/epub_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/docx_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/pdf_probe_manifest.json`",
        "`editions/reader_manuscript/v1_0/reconciliation_report.md`",
        "`docs/reader_chapter_review_matrix.md`",
        "`docs/reader_format_review_matrix.md`",
        "`docs/reader_artifact_inspection_manifest.md`",
        "`docs/reader_html_artifact_browser_review.md`",
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
