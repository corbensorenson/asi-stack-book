#!/usr/bin/env python3
"""Shared checks for retired Project Theseus repository-summary proof mirrors."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
LEDGER = ROOT / "proofs" / "proof_semantic_rationalization_ledger.json"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"


RETIRED_THEOREMS_BY_TARGET: dict[str, tuple[str, ...]] = {
    "lean:theseus.reference.public_task_bundle_import.fixture_bridge": (
        "theseus_public_task_bundle_import_fixture_public_safe",
        "theseus_public_task_bundle_import_fixture_gates_complete",
        "theseus_public_task_bundle_import_fixture_preserves_no_promotion_boundary",
        "theseus_public_task_bundle_import_fixture_valid",
        "theseus_public_task_bundle_import_clean_replay_overclaim_rejected",
    ),
    "lean:theseus.reference.fast_support_aggregate.fixture_bridge": (
        "theseus_fast_support_aggregate_fixture_valid",
        "theseus_fast_support_aggregate_preserves_no_promotion",
        "theseus_fast_support_aggregate_carries_task_and_control_counts",
        "theseus_fast_support_aggregate_clean_replay_overclaim_rejected",
    ),
    "lean:theseus.reference.artifact_retention_replay_import.fixture_bridge": (
        "theseus_artifact_retention_replay_import_fixture_valid",
        "theseus_artifact_retention_replay_import_hash_mismatch_rejected",
        "theseus_artifact_retention_replay_import_core_promotion_rejected",
    ),
    "lean:theseus.reference.module_definition_of_done_import.fixture_bridge": (
        "theseus_module_definition_of_done_import_fixture_valid",
        "theseus_module_definition_of_done_import_core_promotion_rejected",
        "theseus_module_definition_of_done_import_capability_overclaim_rejected",
    ),
    "lean:theseus.reference.project_registry_import.fixture_bridge": (
        "theseus_project_registry_import_fixture_valid",
        "theseus_project_registry_import_unregistered_sources_rejected",
        "theseus_project_registry_import_clean_replay_overclaim_rejected",
        "theseus_project_registry_import_core_promotion_rejected",
        "theseus_project_registry_import_private_payload_rejected",
    ),
    "lean:theseus.reference.assistant_reference_trace_import.fixture_bridge": (
        "theseus_assistant_reference_trace_import_fixture_valid",
        "theseus_assistant_reference_trace_import_requires_all_hops",
        "theseus_assistant_reference_trace_import_private_payload_rejected",
        "theseus_assistant_reference_trace_import_core_promotion_rejected",
        "theseus_assistant_reference_trace_import_model_quality_overclaim_rejected",
        "theseus_assistant_reference_trace_import_clean_replay_overclaim_rejected",
    ),
    "lean:theseus.reference.accelerator_parity_manifest_import.fixture_bridge": (
        "theseus_accelerator_parity_manifest_import_fixture_valid",
        "theseus_accelerator_parity_manifest_import_full_parity_overclaim_rejected",
        "theseus_accelerator_parity_manifest_import_production_routing_overclaim_rejected",
        "theseus_accelerator_parity_manifest_import_model_promotion_overclaim_rejected",
        "theseus_accelerator_parity_manifest_import_core_promotion_rejected",
    ),
    "lean:theseus.reference.book_crosswalk.pointer_boundary": (
        "theseus_book_crosswalk_import_fixture_valid",
        "theseus_book_crosswalk_import_pointer_only_preserves_argument",
        "theseus_book_crosswalk_import_source_sync_failure_rejected",
        "theseus_book_crosswalk_import_public_safety_failure_rejected",
        "theseus_book_crosswalk_import_core_promotion_rejected",
        "theseus_book_crosswalk_import_clean_replay_overclaim_rejected",
    ),
    "lean:theseus.reference.work_board_import.metadata_boundary": (
        "theseus_work_board_import_fixture_valid",
        "theseus_work_board_import_stale_snapshot_blocks_currentness",
        "theseus_work_board_import_clean_replay_overclaim_rejected",
        "theseus_work_board_import_private_payload_rejected",
        "theseus_work_board_import_core_promotion_rejected",
        "theseus_work_board_import_public_training_rows_rejected",
    ),
}


def validate_retired_formal_mirror(target: str, errors: list[str]) -> None:
    """Require physical retirement while preserving the executable validator lane."""
    names = RETIRED_THEOREMS_BY_TARGET[target]
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore")
    for name in names:
        if re.search(rf"(?m)^theorem\s+{re.escape(name)}\b", lean_text):
            errors.append(f"{LEAN.relative_to(ROOT)} still declares retired theorem {name}.")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    retired = {
        row.get("retired_theorem_id")
        for row in ledger.get("actions", [])
        if row.get("action") == "retire_repository_import_fixture_mirror"
    }
    for name in names:
        theorem_id = f"lean/AsiStackProofs/TheseusReference.lean::{name}"
        if theorem_id not in retired:
            errors.append(f"{LEDGER.relative_to(ROOT)} lacks retirement action for {theorem_id}.")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_tags = {row.get("tag") for row in manifest.get("targets", [])}
    if target in manifest_tags:
        errors.append(f"{MANIFEST.relative_to(ROOT)} still exposes retired target {target}.")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    triage_tags = {row.get("tag") for row in triage.get("records", [])}
    if target in triage_tags:
        errors.append(f"{TRIAGE.relative_to(ROOT)} still exposes retired target {target}.")
