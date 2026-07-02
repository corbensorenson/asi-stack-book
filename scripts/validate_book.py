#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "_quarto.yml",
    "book_structure.json",
    "index.qmd",
    "preface.qmd",
    "sources/source_inventory.json",
    "sources/source_inventory.md",
    "scripts/sync_scaffold.py",
    "scripts/sync_proof_manifest.py",
    "scripts/sync_reader_overlay_asset.py",
    "scripts/audit_reader_continuity.py",
    "scripts/validate_publication.py",
    "scripts/validate_architecture_red_team.py",
    "scripts/validate_release_reproducibility.py",
    "scripts/validate_public_site_accessibility.py",
    "scripts/validate_v1_release_gate_audit.py",
    "scripts/validate_release_profiles.py",
    "scripts/validate_reader_spine.py",
    "scripts/validate_reading_mode_toggle.py",
    "scripts/validate_human_reading_paths.py",
    "scripts/validate_reader_evidence_boundaries.py",
    "scripts/validate_reader_overlays.py",
    "scripts/validate_reader_manuscript_manifest.py",
    "scripts/validate_reader_artifact_inspection_manifest.py",
    "scripts/validate_reader_epub_probe_manifest.py",
    "scripts/validate_reader_docx_probe_manifest.py",
    "scripts/validate_reader_pdf_probe_manifest.py",
    "scripts/validate_reader_audio_script_probe_manifest.py",
    "scripts/sync_reader_chapter_review_matrix.py",
    "scripts/sync_reader_format_review_matrix.py",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_chapter_handoffs.py",
    "scripts/validate_source_appendices.py",
    "scripts/validate_v1_status_snapshot.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_proof_artifact_audit.py",
    "scripts/validate_source_evidence_audit.py",
    "scripts/validate_evidence_transitions.py",
    "scripts/validate_non_core_evidence_ledger.py",
    "scripts/validate_claim_revision_records.py",
    "scripts/validate_external_review_status.py",
    "scripts/validate_external_review_intake.py",
    "scripts/validate_defended_contribution_tracks.py",
    "scripts/validate_defended_contribution_prior_art.py",
    "scripts/validate_evidence_laundering_case_studies.py",
    "scripts/validate_core_claim_decisions.py",
    "scripts/validate_core_claim_promotion_paths.py",
    "scripts/validate_v1_x_active_evidence_cycle.py",
    "scripts/validate_chapter_review_burndown.py",
    "scripts/validate_chapter_consolidation_pilot_plan.py",
    "scripts/validate_chapter_consolidation_sequence.py",
    "scripts/build_chapter_external_grounding_status.py",
    "scripts/validate_chapter_external_grounding_status.py",
    "scripts/validate_external_sota_positioning.py",
    "scripts/validate_claim_ledger_revision.py",
    "scripts/validate_proof_carrying_claims.py",
    "scripts/validate_tribunal_review.py",
    "scripts/validate_value_conflicts.py",
    "scripts/validate_constitutional_alignment.py",
    "scripts/validate_governance_rights.py",
    "scripts/validate_agency_rights.py",
    "scripts/validate_support_state_transitions.py",
    "scripts/validate_authority_transitions.py",
    "scripts/validate_security_kernel.py",
    "scripts/validate_stable_capability_fields.py",
    "scripts/validate_capability_replacement.py",
    "scripts/validate_self_improvement_boundaries.py",
    "scripts/validate_plan_execution_contracts.py",
    "scripts/validate_cognitive_compilation_traces.py",
    "scripts/validate_hive_admission.py",
    "scripts/validate_runtime_adapter_permissions.py",
    "scripts/validate_artifact_graph_replay.py",
    "scripts/validate_procedural_memory_loop.py",
    "scripts/validate_routing_decision_lease.py",
    "scripts/validate_cyclic_memory_contracts.py",
    "scripts/validate_context_transaction_memory_store.py",
    "scripts/validate_context_admission_adequacy.py",
    "scripts/validate_readiness_residual_gates.py",
    "scripts/validate_benchmark_antigoodhart.py",
    "scripts/validate_generation_mode_baselines.py",
    "scripts/validate_compact_gvr_slice.py",
    "scripts/validate_resource_budget_ledgers.py",
    "scripts/validate_simulation_transfer_boundaries.py",
    "scripts/validate_reference_trace.py",
    "scripts/validate_capacity_smoothing.py",
    "scripts/validate_costed_route_resource_slice.py",
    "scripts/validate_resource_workflow_trace.py",
    "scripts/run_resource_live_probe.py",
    "scripts/validate_resource_live_probe.py",
    "scripts/run_resource_workload_quality_probe.py",
    "scripts/validate_resource_workload_quality_probe.py",
    "scripts/run_resource_load_stability_probe.py",
    "scripts/validate_resource_load_stability_probe.py",
    "scripts/build_resource_ci_cost_profile.py",
    "scripts/validate_resource_ci_cost_profile.py",
    "scripts/run_resource_flagship_lane.py",
    "scripts/validate_resource_flagship_lane.py",
    "scripts/validate_circle_external_receipt_slice.py",
    "scripts/validate_circle_public_replay.py",
    "scripts/validate_circle_concrete_evidence_surface.py",
    "scripts/validate_theseus_report.py",
    "scripts/validate_theseus_generation_mode_import.py",
    "scripts/run_theseus_support_replay_probe.py",
    "scripts/validate_theseus_support_replay_probe.py",
    "scripts/validate_phase5_harness_registry.py",
    "scripts/build_reader_edition.py",
    "scripts/build_curated_reader_edition.py",
    "scripts/build_source_matrix.py",
    "schemas/book_structure.schema.json",
    "docs/book_outline.md",
    "docs/architecture_red_team_review.md",
    "docs/release_reproducibility.md",
    "docs/public_site_accessibility_review.md",
    "docs/v1_progress_ledger.md",
    "docs/v1_0_release_gate_audit.md",
    "docs/proof_artifact_audit.md",
    "docs/source_evidence_audit.md",
    "docs/core_claim_transition_coverage.md",
    "docs/v1_x_active_evidence_cycle.md",
    "docs/CHAPTER_REVIEWS.md",
    "docs/chapter_consolidation_sequence.md",
    "docs/chapter_consolidation_pilot_plan.md",
    "docs/chapter_consolidation_dry_run_constitutional_alignment.md",
    "docs/non_core_evidence_ledger.md",
    "docs/external_review_packet.md",
    "docs/external_review_status.md",
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
    "external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json",
    "docs/chapter_consolidation_full_review_packet.md",
    "docs/defended_contribution_tracks.md",
    "docs/defended_contribution_prior_art_positioning.md",
    "docs/evidence_laundering_prevention_case_studies.md",
    "docs/chapter_external_grounding_status.md",
    "docs/external_sota_positioning_audit.md",
    "docs/support_state_transition_harness.md",
    "docs/authority_transition_harness.md",
    "docs/plan_execution_contract_harness.md",
    "docs/cognitive_compilation_trace_harness.md",
    "docs/hive_admission_harness.md",
    "docs/runtime_adapter_permission_harness.md",
    "docs/artifact_graph_replay_harness.md",
    "docs/procedural_memory_loop_harness.md",
    "docs/routing_decision_lease_harness.md",
    "docs/cyclic_memory_contract_harness.md",
    "docs/context_transaction_memory_store_harness.md",
    "docs/context_admission_adequacy_harness.md",
    "docs/readiness_residual_harness.md",
    "docs/benchmark_antigoodhart_harness.md",
    "docs/generation_mode_baseline_harness.md",
    "docs/compact_gvr_slice.md",
    "docs/resource_budget_ledger_harness.md",
    "docs/reference_trace_harness.md",
    "docs/capacity_smoothing_harness.md",
    "docs/costed_route_resource_slice.md",
    "docs/resource_workflow_trace.md",
    "docs/resource_live_probe.md",
    "docs/resource_workload_quality_probe.md",
    "docs/resource_load_stability_probe.md",
    "docs/resource_ci_cost_profile.md",
    "docs/resource_flagship_lane_run.md",
    "docs/circle_external_receipt_slice.md",
    "docs/circle_public_replay_consumer_gate.md",
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/phase5_harness_registry.md",
    "docs/claim_ledger_revision_harness.md",
    "docs/proof_carrying_claim_harness.md",
    "docs/tribunal_review_harness.md",
    "docs/value_conflict_harness.md",
    "docs/constitutional_alignment_harness.md",
    "docs/governance_rights_harness.md",
    "docs/agency_rights_harness.md",
    "docs/security_kernel_harness.md",
    "docs/stable_capability_field_harness.md",
    "docs/capability_replacement_harness.md",
    "docs/self_improvement_boundary_harness.md",
    "docs/reader_continuity_audit.md",
    "docs/reader_chapter_review_matrix.md",
    "docs/reader_format_review_matrix.md",
    "docs/reader_part_i_review_pass.md",
    "docs/reader_part_ii_review_pass.md",
    "docs/reader_part_iii_review_pass.md",
    "docs/reader_part_iv_review_pass.md",
    "experiments/phase5_harness_registry.json",
    "experiments/claim_ledger_revision/results/2026-06-28-local.md",
    "experiments/proof_carrying_claims/results/2026-06-28-local.md",
    "experiments/tribunal_review/results/2026-06-28-local.md",
    "experiments/value_conflicts/results/2026-06-28-local.md",
    "experiments/constitutional_alignment/results/2026-06-28-local.md",
    "experiments/governance_rights/results/2026-06-28-local.md",
    "experiments/agency_rights/results/2026-06-28-local.md",
    "experiments/security_kernel/results/2026-06-28-local.md",
    "experiments/stable_capability_fields/results/2026-06-28-local.md",
    "experiments/capability_replacement/results/2026-06-28-local.md",
    "experiments/self_improvement_boundaries/results/2026-06-28-local.md",
    "experiments/cognitive_compilation_traces/results/2026-07-02-local.md",
    "experiments/generation_mode_baselines/results/2026-06-28-local.md",
    "experiments/compact_gvr_slice/results/2026-07-01-local.json",
    "experiments/resource_budget_ledgers/results/2026-07-01-local.md",
    "experiments/reference_trace/results/2026-06-30-local.md",
    "experiments/capacity_smoothing/results/2026-06-28-local.md",
    "experiments/artifact_graph_replay/results/2026-06-30-local.md",
    "experiments/procedural_memory_loop/results/2026-06-30-local.md",
    "experiments/routing_decision_lease/results/2026-07-01-local.md",
    "experiments/cyclic_memory_contracts/results/2026-06-30-local.md",
    "experiments/context_transaction_memory_store/results/2026-07-01-local.md",
    "experiments/hive_admission/results/2026-07-01-local.md",
    "experiments/costed_route_resource_slice/results/2026-06-29-local.json",
    "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "experiments/resource_live_probe/results/2026-07-01-local.json",
    "experiments/resource_workload_quality_probe/results/2026-07-01-local.json",
    "experiments/resource_load_stability_probe/results/2026-07-01-local.json",
    "experiments/resource_ci_cost_profile/results/2026-07-01-main.json",
    "experiments/resource_flagship_lane/results/2026-07-01-local.json",
    "experiments/circle_external_receipt_slice/results/2026-06-29-local.json",
    "experiments/circle_public_replay/results/2026-06-29-local.json",
    "experiments/theseus_import/results/2026-06-29-local.json",
    "experiments/theseus_generation_mode_import/results/2026-07-01-local.json",
    "experiments/theseus_support_replay_probe/results/2026-07-01-local.json",
    "evidence_transitions/README.md",
    "claim_decisions/v1_0_core_claim_no_promotion.json",
    "editions/release_profiles.json",
    "editions/reader_overlays/README.md",
    "editions/reader_overlays/v1_0/manifest.json",
    "editions/reader_manuscript/README.md",
    "editions/reader_manuscript/v1_0/manifest.json",
    "editions/reader_manuscript/v1_0/curation_contract.json",
    "editions/reader_manuscript/v1_0/artifact_inspection_manifest.json",
    "editions/reader_manuscript/v1_0/epub_probe_manifest.json",
    "editions/reader_manuscript/v1_0/docx_probe_manifest.json",
    "editions/reader_manuscript/v1_0/pdf_probe_manifest.json",
    "editions/reader_manuscript/v1_0/audio_script_probe_manifest.json",
    "editions/reader_manuscript/v1_0/chapter_review_matrix.json",
    "editions/reader_manuscript/v1_0/format_review_matrix.json",
    "editions/reader_manuscript/v1_0/companion_note_routing.json",
    "editions/reader_manuscript/v1_0/reconciliation_report.md",
    "docs/curated_reader_source_contract.md",
    "docs/reader_artifact_inspection_manifest.md",
    "docs/reader_epub_probe_manifest.md",
    "docs/reader_docx_probe_manifest.md",
    "docs/reader_pdf_probe_manifest.md",
    "docs/reader_audio_script_probe_manifest.md",
    "docs/reader_companion_note_routing_review.md",
    "assets/reader-overlays.html",
    "proofs/proof_manifest.json",
    "appendices/A_source_matrix.qmd",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/E_codex_test_specs.qmd",
    "appendices/F_changelog.qmd",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/H_external_sources.qmd",
    "appendices/J_release_editions.qmd",
    "appendices/K_implementation_horizons.qmd",
]

BAD_PHRASES = [
    "solves ASI",
    "guarantees safety",
    "proves alignment",
    "obviously safe",
    "replaces all existing methods",
]

STALE_GENERATED_PHRASES = [
    "Probe whether the chapter claim holds under the relevant",
    "Chapter is a v0.2 manuscript draft; v1.0 still needs source-note substantiation",
    "No Codex tests have been implemented or run for this chapter unless separately recorded",
    "| Test state | Planned only; no tests have been run",
    "Support or falsify this chapter's layer claim",
]

ALLOWED_SUPPORT_STATES = {
    "unsupported",
    "argument",
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
    "deprecated",
    "refuted",
}

ALLOWED_CLAIM_LABELS = {
    "Demonstrated",
    "Measured",
    "Mechanized",
    "Hypothesized",
    "Design rationale",
    "Speculative",
}


def fail(message: str) -> None:
    print(message)
    sys.exit(1)


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def type_ok(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate_schema_value(value: object, schema: dict, path: str) -> list[str]:
    errors: list[str] = []
    any_of = schema.get("anyOf")
    if isinstance(any_of, list):
        option_errors = []
        for option in any_of:
            if not isinstance(option, dict):
                continue
            candidate_errors = validate_schema_value(value, option, path)
            if not candidate_errors:
                return []
            option_errors.append(candidate_errors[0])
        if option_errors:
            return [f"{path}: does not match anyOf options ({'; '.join(option_errors)})"]
        return [f"{path}: anyOf has no valid schema options"]

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not type_ok(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']!r}")

    if expected_type == "string":
        min_length = schema.get("minLength", 0)
        if isinstance(value, str) and isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path}: string shorter than minLength {min_length}")

    if expected_type == "array" and isinstance(value, list):
        min_items = schema.get("minItems", 0)
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(f"{path}: array shorter than minItems {min_items}")
        item_schema = schema.get("items", {})
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_schema_value(item, item_schema, f"{path}[{index}]"))

    if expected_type == "object" and isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    errors.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        errors.append(f"{path}: unexpected key {key!r}")
            for key, child_schema in properties.items():
                if key in value and isinstance(child_schema, dict):
                    errors.extend(validate_schema_value(value[key], child_schema, f"{path}.{key}"))

    return errors


def validate_structure_schema() -> None:
    structure = read_json(ROOT / "book_structure.json")
    schema = read_json(ROOT / "schemas" / "book_structure.schema.json")
    if not isinstance(schema, dict):
        fail("schemas/book_structure.schema.json must contain an object.")
    errors = validate_schema_value(structure, schema, "book_structure.json")
    if errors:
        print("book_structure.json does not match schemas/book_structure.schema.json:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)


def flatten_chapters(structure: dict) -> list[dict]:
    chapters = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            chapters.append(chapter)
    return chapters


def validate_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f" - {path}")
        sys.exit(1)


def validate_inventory() -> set[str]:
    records = read_json(ROOT / "sources" / "source_inventory.json")
    if not isinstance(records, list):
        fail("sources/source_inventory.json must contain a list.")
    required_keys = {"id", "title", "priority", "layer", "chapter_targets", "url", "notes"}
    bad_records = []
    seen = set()
    duplicates = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or not required_keys.issubset(record):
            bad_records.append(index)
            continue
        source_id = record["id"]
        if source_id in seen:
            duplicates.add(source_id)
        seen.add(source_id)
    if bad_records:
        fail(f"Source inventory records missing required keys: {bad_records}")
    if duplicates:
        fail(f"Duplicate source IDs: {sorted(duplicates)}")
    return seen


def validate_structure(source_ids: set[str]) -> list[dict]:
    structure = read_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        fail("book_structure.json must contain an object.")
    chapters = flatten_chapters(structure)
    if not chapters:
        fail("book_structure.json has no chapters.")

    ids = set()
    files = set()
    duplicate_ids = set()
    duplicate_files = set()
    unknown_sources = []
    missing_files = []

    for chapter in chapters:
        chapter_id = chapter.get("id")
        file_path = chapter.get("file")
        if not chapter_id or not file_path:
            fail(f"Chapter entry missing id or file: {chapter}")
        if chapter_id in ids:
            duplicate_ids.add(chapter_id)
        ids.add(chapter_id)
        if file_path in files:
            duplicate_files.add(file_path)
        files.add(file_path)
        if not (ROOT / file_path).exists():
            missing_files.append(file_path)
        claim_label = chapter.get("claim_label")
        if not isinstance(claim_label, str) or not claim_label.strip():
            fail(f"{chapter_id}: missing explicit claim_label in book_structure.json.")
        if claim_label not in ALLOWED_CLAIM_LABELS:
            fail(f"{chapter_id}: invalid claim_label {claim_label!r}.")
        evidence_level = chapter.get("evidence_level")
        if not isinstance(evidence_level, str) or not evidence_level.strip():
            fail(f"{chapter_id}: missing explicit evidence_level in book_structure.json.")
        if evidence_level not in ALLOWED_SUPPORT_STATES:
            fail(f"{chapter_id}: invalid evidence_level {evidence_level!r}.")
        for source_id in chapter.get("source_ids", []):
            if source_id not in source_ids:
                unknown_sources.append((chapter_id, source_id))
        chapter_source_ids = set(chapter.get("source_ids", []))
        for index, mapping in enumerate(chapter.get("claim_source_mappings", [])):
            if not isinstance(mapping, dict):
                fail(f"{chapter_id}: claim_source_mappings[{index}] must be an object.")
            mapping_source = mapping.get("source_id")
            if mapping_source not in chapter_source_ids:
                fail(f"{chapter_id}: claim_source_mappings[{index}] uses unassigned source {mapping_source!r}.")
            for field in ("mapped_support", "limits"):
                if not isinstance(mapping.get(field), str) or not mapping[field].strip():
                    fail(f"{chapter_id}: claim_source_mappings[{index}] missing non-empty {field}.")

    if duplicate_ids:
        fail(f"Duplicate chapter IDs in book_structure.json: {sorted(duplicate_ids)}")
    if duplicate_files:
        fail(f"Duplicate chapter files in book_structure.json: {sorted(duplicate_files)}")
    if missing_files:
        print("Chapter files listed in book_structure.json are missing:")
        for path in missing_files:
            print(f" - {path}")
        sys.exit(1)
    if unknown_sources:
        print("Unknown source IDs in book_structure.json:")
        for chapter_id, source_id in unknown_sources:
            print(f" - {chapter_id}: {source_id}")
        sys.exit(1)

    return chapters


def validate_chapter_frontmatter(chapters: list[dict]) -> None:
    stale = []
    for chapter in chapters:
        path = ROOT / chapter["file"]
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'last_updated: "YYYY-MM-DD"' in text:
            stale.append(path.relative_to(ROOT))
        if f'chapter_id: "{chapter["id"]}"' not in text:
            stale.append(path.relative_to(ROOT))
        if "Source loading state" not in text:
            stale.append(path.relative_to(ROOT))
    if stale:
        print("Chapter files need dynamic scaffold status updates:")
        for path in sorted(set(stale)):
            print(f" - {path}")
        sys.exit(1)


def validate_quarto_generated() -> None:
    text = (ROOT / "_quarto.yml").read_text(encoding="utf-8", errors="ignore")
    if "generated by scripts/sync_scaffold.py" not in text:
        fail("_quarto.yml should be generated by scripts/sync_scaffold.py.")
    if "\nlang: en-US\n" not in text:
        fail("_quarto.yml must declare `lang: en-US` so EPUB/PDF metadata does not inherit the shell locale.")


def validate_overclaims() -> None:
    violations = []
    targets = list((ROOT / "chapters").glob("*.qmd")) + list((ROOT / "appendices").glob("*.qmd"))
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in BAD_PHRASES:
            if phrase.lower() in text:
                violations.append((path.relative_to(ROOT), phrase))
    if violations:
        print("Potential overclaim phrases found:")
        for path, phrase in violations:
            print(f" - {path}: {phrase}")
        sys.exit(2)


def validate_stale_generated_language() -> None:
    violations = []
    targets = (
        list((ROOT / "chapters").glob("*.qmd"))
        + [
            ROOT / "scripts" / "draft_v02_from_manifest.py",
            ROOT / "scripts" / "sync_scaffold.py",
        ]
    )
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in STALE_GENERATED_PHRASES:
            if phrase in text:
                violations.append((path.relative_to(ROOT), phrase))
    if violations:
        print("Stale generated manuscript language found:")
        for path, phrase in violations:
            print(f" - {path}: {phrase}")
        sys.exit(2)


def validate_claim_states() -> None:
    text = (ROOT / "appendices" / "C_claim_evidence_matrix.qmd").read_text(encoding="utf-8", errors="ignore")
    missing = [state for state in ALLOWED_SUPPORT_STATES if state not in text]
    if missing:
        fail(f"Claim/evidence matrix is missing support-state definitions: {sorted(missing)}")
    missing_labels = [label for label in ALLOWED_CLAIM_LABELS if label not in text]
    if missing_labels:
        fail(f"Claim/evidence matrix is missing claim-label definitions: {sorted(missing_labels)}")


def validate_structure_proof_statuses(chapters: list[dict]) -> None:
    manifest = read_json(ROOT / "proofs" / "proof_manifest.json")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("records"), list):
        fail("proofs/proof_manifest.json must contain a records list.")

    manifest_records = {
        record.get("tag"): record
        for record in manifest["records"]
        if isinstance(record, dict) and isinstance(record.get("tag"), str)
    }
    errors: list[str] = []
    for chapter in chapters:
        chapter_id = chapter.get("id", "<missing>")
        for target in chapter.get("proof_targets", []):
            if not isinstance(target, dict):
                errors.append(f"{chapter_id}: proof_targets entry must be an object.")
                continue
            tag = target.get("tag")
            if not isinstance(tag, str) or not tag:
                errors.append(f"{chapter_id}: proof target missing tag.")
                continue
            manifest_record = manifest_records.get(tag)
            if manifest_record is None:
                errors.append(f"{chapter_id}: proof target {tag!r} missing from proofs/proof_manifest.json.")
                continue
            if manifest_record.get("chapter_id") != chapter_id:
                errors.append(
                    f"{chapter_id}: proof target {tag!r} manifest chapter is "
                    f"{manifest_record.get('chapter_id')!r}."
                )
            if manifest_record.get("status") != target.get("status"):
                errors.append(
                    f"{chapter_id}: proof target {tag!r} status "
                    f"{target.get('status')!r} does not match manifest "
                    f"{manifest_record.get('status')!r}."
                )

    if errors:
        print("book_structure.json proof targets disagree with proofs/proof_manifest.json:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)


def validate_proof_manifest() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_proof_manifest.py"), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def validate_publication_surface() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_publication.py")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def run_validator(script_name: str, *args: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def main() -> None:
    validate_required_files()
    validate_structure_schema()
    source_ids = validate_inventory()
    chapters = validate_structure(source_ids)
    validate_quarto_generated()
    validate_chapter_frontmatter(chapters)
    validate_overclaims()
    validate_stale_generated_language()
    validate_claim_states()
    validate_proof_manifest()
    validate_structure_proof_statuses(chapters)
    run_validator("validate_validator_coverage.py")
    run_validator("validate_proof_depth.py")
    run_validator("validate_architecture_red_team.py")
    run_validator("validate_release_reproducibility.py")
    run_validator("validate_public_site_accessibility.py")
    run_validator("validate_v1_release_gate_audit.py")
    run_validator("validate_release_profiles.py")
    validate_publication_surface()
    run_validator("validate_reading_mode_toggle.py")
    run_validator("validate_human_reading_paths.py")
    run_validator("validate_reader_evidence_boundaries.py", "--check")
    run_validator("audit_reader_continuity.py", "--check")
    run_validator("validate_reader_manuscript_manifest.py")
    run_validator("build_curated_reader_edition.py", "--check")
    run_validator("validate_reader_artifact_inspection_manifest.py")
    run_validator("validate_reader_epub_probe_manifest.py")
    run_validator("validate_reader_docx_probe_manifest.py")
    run_validator("validate_reader_pdf_probe_manifest.py")
    run_validator("validate_reader_audio_script_probe_manifest.py")
    run_validator("sync_reader_format_review_matrix.py", "--check")
    run_validator("validate_source_appendices.py")
    run_validator("validate_v1_status_snapshot.py")
    run_validator("validate_outline_consistency.py")
    run_validator("validate_implementation_horizons.py")
    run_validator("validate_reader_spine.py", "--check")
    run_validator("validate_chapter_dod.py")
    run_validator("validate_chapter_handoffs.py")
    run_validator("validate_visual_coverage.py")
    run_validator("validate_repeated_prose.py")
    run_validator("validate_source_notes.py")
    run_validator("validate_proof_readiness.py")
    run_validator("validate_proof_artifact_audit.py")
    run_validator("validate_protocol_crosswalk.py")
    run_validator("validate_source_evidence_audit.py")
    run_validator("validate_evidence_transitions.py")
    run_validator("validate_non_core_evidence_ledger.py")
    run_validator("validate_claim_revision_records.py")
    run_validator("validate_core_claim_decisions.py")
    run_validator("validate_external_review_intake.py")
    run_validator("validate_defended_contribution_tracks.py")
    run_validator("validate_defended_contribution_prior_art.py")
    run_validator("validate_evidence_laundering_case_studies.py")
    run_validator("validate_core_claim_promotion_paths.py")
    run_validator("validate_v1_x_active_evidence_cycle.py")
    run_validator("validate_chapter_review_burndown.py")
    run_validator("validate_chapter_consolidation_sequence.py")
    run_validator("validate_chapter_consolidation_pilot_plan.py")
    run_validator("validate_chapter_external_grounding_status.py")
    run_validator("validate_external_sota_positioning.py")
    run_validator("validate_claim_ledger_revision.py")
    run_validator("validate_proof_carrying_claims.py")
    run_validator("validate_tribunal_review.py")
    run_validator("validate_value_conflicts.py")
    run_validator("validate_constitutional_alignment.py")
    run_validator("validate_governance_rights.py")
    run_validator("validate_agency_rights.py")
    run_validator("validate_support_state_transitions.py")
    run_validator("validate_authority_transitions.py")
    run_validator("validate_security_kernel.py")
    run_validator("validate_stable_capability_fields.py")
    run_validator("validate_capability_replacement.py")
    run_validator("validate_self_improvement_boundaries.py")
    run_validator("validate_plan_execution_contracts.py")
    run_validator("validate_cognitive_compilation_traces.py")
    run_validator("validate_hive_admission.py")
    run_validator("validate_runtime_adapter_permissions.py")
    run_validator("validate_artifact_graph_replay.py")
    run_validator("validate_procedural_memory_loop.py")
    run_validator("validate_routing_decision_lease.py")
    run_validator("validate_cyclic_memory_contracts.py")
    run_validator("validate_context_transaction_memory_store.py")
    run_validator("validate_context_admission_adequacy.py")
    run_validator("validate_readiness_residual_gates.py")
    run_validator("validate_benchmark_antigoodhart.py")
    run_validator("validate_generation_mode_baselines.py")
    run_validator("validate_compact_gvr_slice.py")
    run_validator("validate_resource_budget_ledgers.py")
    run_validator("validate_simulation_transfer_boundaries.py")
    run_validator("validate_reference_trace.py")
    run_validator("validate_capacity_smoothing.py")
    run_validator("validate_costed_route_resource_slice.py")
    run_validator("validate_resource_workflow_trace.py")
    run_validator("validate_resource_live_probe.py")
    run_validator("validate_resource_workload_quality_probe.py")
    run_validator("validate_resource_load_stability_probe.py")
    run_validator("validate_resource_ci_cost_profile.py")
    run_validator("validate_resource_flagship_lane.py")
    run_validator("validate_circle_external_receipt_slice.py")
    run_validator("validate_circle_public_replay.py")
    run_validator("validate_circle_concrete_evidence_surface.py")
    run_validator("validate_theseus_report.py")
    run_validator("validate_theseus_generation_mode_import.py")
    run_validator("validate_theseus_support_replay_probe.py")
    run_validator("validate_phase5_harness_registry.py")
    run_validator("run_phase5_harnesses.py")
    print("Book validation passed.")


if __name__ == "__main__":
    main()
