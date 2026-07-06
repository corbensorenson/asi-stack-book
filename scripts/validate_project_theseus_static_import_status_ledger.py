#!/usr/bin/env python3
"""Generate and validate the Project Theseus static-import status ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
LEDGER = ROOT / "docs" / "project_theseus_static_import_status_ledger.md"

ARCH_RESULT = ROOT / "experiments" / "theseus_import" / "results" / "2026-06-29-local.json"
ARCH_FIXTURE = ROOT / "experiments" / "theseus_import" / "fixtures" / "valid" / "architecture_gate_public_report.valid.json"
GEN_RESULT = ROOT / "experiments" / "theseus_generation_mode_import" / "results" / "2026-07-01-local.json"
GEN_FIXTURE = ROOT / "experiments" / "theseus_generation_mode_import" / "fixtures" / "valid" / "generation_mode_gate_public_summary.valid.json"
SUPPORT_REPLAY = ROOT / "experiments" / "theseus_support_replay_probe" / "results" / "2026-07-01-local.json"
TASK_RESULT = ROOT / "experiments" / "theseus_public_task_bundle_import" / "results" / "2026-07-03-local.json"
TASK_FIXTURE = ROOT / "experiments" / "theseus_public_task_bundle_import" / "fixtures" / "valid" / "public_task_bundle_import.valid.json"
NO_PROMOTION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_public_task_bundle_import_no_change.json"
ARTIFACT_RESULT = (
    ROOT
    / "experiments"
    / "theseus_artifact_retention_replay_import"
    / "results"
    / "2026-07-05-local.json"
)
ARTIFACT_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_artifact_retention_replay_import"
    / "fixtures"
    / "valid"
    / "artifact_retention_replay_import.valid.json"
)
ARTIFACT_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_artifact_retention_replay_import_prototype_backed.json"
)
GOVERNANCE_RESULT = (
    ROOT
    / "experiments"
    / "theseus_governance_rights_receipt_suite_import"
    / "results"
    / "2026-07-05-local.json"
)
GOVERNANCE_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_governance_rights_receipt_suite_import"
    / "fixtures"
    / "valid"
    / "governance_rights_receipt_suite_import.valid.json"
)
GOVERNANCE_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_governance_rights_receipt_suite_import_prototype_backed.json"
)
SIMULATION_RESULT = (
    ROOT
    / "experiments"
    / "theseus_simulation_fidelity_receipt_suite_import"
    / "results"
    / "2026-07-05-local.json"
)
SIMULATION_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_simulation_fidelity_receipt_suite_import"
    / "fixtures"
    / "valid"
    / "simulation_fidelity_receipt_suite_import.valid.json"
)
SIMULATION_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_simulation_fidelity_receipt_suite_import_prototype_backed.json"
)
RLDS_MINARI_RESULT = (
    ROOT
    / "experiments"
    / "theseus_rlds_minari_trace_export_import"
    / "results"
    / "2026-07-05-local.json"
)
RLDS_MINARI_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_rlds_minari_trace_export_import"
    / "fixtures"
    / "valid"
    / "rlds_minari_trace_export_import.valid.json"
)
RLDS_MINARI_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_rlds_minari_trace_export_import_prototype_backed.json"
)
MODULE_DOD_RESULT = (
    ROOT
    / "experiments"
    / "theseus_module_definition_of_done_import"
    / "results"
    / "2026-07-05-local.json"
)
MODULE_DOD_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_module_definition_of_done_import"
    / "fixtures"
    / "valid"
    / "module_definition_of_done_import.valid.json"
)
MODULE_DOD_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_module_definition_of_done_import_prototype_backed.json"
)
PROJECT_REGISTRY_RESULT = (
    ROOT
    / "experiments"
    / "theseus_project_registry_import"
    / "results"
    / "2026-07-05-local.json"
)
PROJECT_REGISTRY_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_project_registry_import"
    / "fixtures"
    / "valid"
    / "project_registry_import.valid.json"
)
PROJECT_REGISTRY_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_project_registry_import_prototype_backed.json"
)
BOOK_CROSSWALK_RESULT = (
    ROOT
    / "experiments"
    / "theseus_book_crosswalk_import"
    / "results"
    / "2026-07-05-local.json"
)
BOOK_CROSSWALK_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_book_crosswalk_import"
    / "fixtures"
    / "valid"
    / "book_to_theseus_crosswalk_import.valid.json"
)
BOOK_CROSSWALK_TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_book_crosswalk_import_no_change.json"
)

DOCS = (
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/theseus_public_task_bundle_import.md",
    "docs/theseus_artifact_retention_replay_import.md",
    "docs/theseus_governance_rights_receipt_suite_import.md",
    "docs/theseus_simulation_fidelity_receipt_suite_import.md",
    "docs/theseus_rlds_minari_trace_export_import.md",
    "docs/theseus_module_definition_of_done_import.md",
    "docs/theseus_project_registry_import.md",
    "docs/theseus_book_crosswalk_import.md",
)
VALIDATORS = (
    "python3 scripts/validate_theseus_report.py",
    "python3 scripts/validate_theseus_generation_mode_import.py",
    "python3 scripts/run_theseus_support_replay_probe.py --write-result",
    "python3 scripts/validate_theseus_support_replay_probe.py",
    "python3 scripts/validate_theseus_public_task_bundle_import.py",
    "python3 scripts/validate_theseus_artifact_retention_replay_import.py",
    "python3 scripts/validate_theseus_governance_rights_receipt_suite_import.py",
    "python3 scripts/validate_theseus_simulation_fidelity_receipt_suite_import.py",
    "python3 scripts/validate_theseus_rlds_minari_trace_export_import.py",
    "python3 scripts/validate_theseus_module_definition_of_done_import.py",
    "python3 scripts/validate_theseus_project_registry_import.py",
    "python3 scripts/validate_theseus_book_crosswalk_import.py",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect_metrics()
        if errors:
            raise RuntimeError("; ".join(errors))
    return (
        "| Project Theseus static import lane | "
        f"Project Theseus detail is generated in `docs/project_theseus_static_import_status_ledger.md`: "
        f"{metrics['static_report_imports']} sanitized static report imports, "
        f"{metrics['support_replay_count']} support replay probe, "
        f"{metrics['artifact_retention_replay_imports']} artifact-retention replay import, "
        f"{metrics['governance_rights_receipt_imports']} governance-rights receipt import, "
        f"{metrics['simulation_fidelity_receipt_imports']} simulation-fidelity receipt import, "
        f"{metrics['rlds_minari_trace_export_imports']} RLDS/Minari trace-export import, "
        f"{metrics['module_dod_imports']} module definition-of-done import, "
        f"{metrics['project_registry_imports']} project-registry import, "
        f"{metrics['book_crosswalk_imports']} book-to-Theseus crosswalk pointer import, "
        f"{metrics['public_task_count']} metadata-only public tasks, "
        f"{metrics['public_training_rows']} public training rows, "
        f"{metrics['generation_mode_count']} generation modes, "
        f"{metrics['generation_comparison_count']} comparisons, "
        f"{metrics['promotable_comparison_count']} promotable comparisons, "
        f"{metrics['expected_invalid_total']} expected-invalid controls, "
        f"{metrics['no_promotion_decisions']} accepted no-promotion decisions, "
        f"{metrics['artifact_upward_transitions']} accepted bounded artifact-retention transition, "
        f"{metrics['governance_rights_upward_transitions']} accepted bounded governance-rights transition, "
        f"{metrics['simulation_fidelity_upward_transitions']} accepted bounded simulation-fidelity transition, "
        f"{metrics['rlds_minari_upward_transitions']} accepted bounded RLDS/Minari trace-export transition, "
        f"{metrics['module_dod_upward_transitions']} accepted bounded module definition-of-done transition, "
        f"and {metrics['project_registry_upward_transitions']} accepted bounded project-registry transition; "
        f"{metrics['book_crosswalk_pointer_rows']} public-safe pointer rows; "
        "clean live replay remains unclaimed. "
        "| `docs/project_theseus_static_import_status_ledger.md`; "
        "`python3 scripts/validate_project_theseus_static_import_status_ledger.py` |"
    )


def collect_metrics() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    required = [
        ARCH_RESULT,
        ARCH_FIXTURE,
        GEN_RESULT,
        GEN_FIXTURE,
        SUPPORT_REPLAY,
        TASK_RESULT,
        TASK_FIXTURE,
        NO_PROMOTION,
        ARTIFACT_RESULT,
        ARTIFACT_FIXTURE,
        ARTIFACT_TRANSITION,
        GOVERNANCE_RESULT,
        GOVERNANCE_FIXTURE,
        GOVERNANCE_TRANSITION,
        SIMULATION_RESULT,
        SIMULATION_FIXTURE,
        SIMULATION_TRANSITION,
        RLDS_MINARI_RESULT,
        RLDS_MINARI_FIXTURE,
        RLDS_MINARI_TRANSITION,
        MODULE_DOD_RESULT,
        MODULE_DOD_FIXTURE,
        MODULE_DOD_TRANSITION,
        PROJECT_REGISTRY_RESULT,
        PROJECT_REGISTRY_FIXTURE,
        PROJECT_REGISTRY_TRANSITION,
        BOOK_CROSSWALK_RESULT,
        BOOK_CROSSWALK_FIXTURE,
        BOOK_CROSSWALK_TRANSITION,
        *(ROOT / path for path in DOCS),
    ]
    for path in required:
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return {}, errors

    arch_result = load_json(ARCH_RESULT)
    arch_fixture = load_json(ARCH_FIXTURE)
    gen_result = load_json(GEN_RESULT)
    gen_fixture = load_json(GEN_FIXTURE)
    support_replay = load_json(SUPPORT_REPLAY)
    task_result = load_json(TASK_RESULT)
    task_fixture = load_json(TASK_FIXTURE)
    no_promotion = load_json(NO_PROMOTION)
    artifact_result = load_json(ARTIFACT_RESULT)
    artifact_fixture = load_json(ARTIFACT_FIXTURE)
    artifact_transition = load_json(ARTIFACT_TRANSITION)
    governance_result = load_json(GOVERNANCE_RESULT)
    governance_fixture = load_json(GOVERNANCE_FIXTURE)
    governance_transition = load_json(GOVERNANCE_TRANSITION)
    simulation_result = load_json(SIMULATION_RESULT)
    simulation_fixture = load_json(SIMULATION_FIXTURE)
    simulation_transition = load_json(SIMULATION_TRANSITION)
    rlds_minari_result = load_json(RLDS_MINARI_RESULT)
    rlds_minari_fixture = load_json(RLDS_MINARI_FIXTURE)
    rlds_minari_transition = load_json(RLDS_MINARI_TRANSITION)
    module_dod_result = load_json(MODULE_DOD_RESULT)
    module_dod_fixture = load_json(MODULE_DOD_FIXTURE)
    module_dod_transition = load_json(MODULE_DOD_TRANSITION)
    project_registry_result = load_json(PROJECT_REGISTRY_RESULT)
    project_registry_fixture = load_json(PROJECT_REGISTRY_FIXTURE)
    project_registry_transition = load_json(PROJECT_REGISTRY_TRANSITION)
    book_crosswalk_result = load_json(BOOK_CROSSWALK_RESULT)
    book_crosswalk_fixture = load_json(BOOK_CROSSWALK_FIXTURE)
    book_crosswalk_transition = load_json(BOOK_CROSSWALK_TRANSITION)

    if arch_result.get("validation_result") != "pass":
        errors.append("architecture-gate import result must pass.")
    if arch_result.get("accepted_gate_count") != 14 or arch_result.get("accepted_passed_count") != 14:
        errors.append("architecture-gate import must keep 14/14 accepted gates.")
    if arch_result.get("expected_invalid_count") != 3:
        errors.append("architecture-gate import must keep three expected-invalid controls.")
    if arch_result.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append("architecture-gate import support_state_effect drifted.")
    if arch_fixture.get("source_project", {}).get("worktree_state") != "dirty_at_import_review":
        errors.append("architecture-gate import must preserve dirty-at-import boundary.")
    if arch_fixture.get("decision_summary", {}).get("external_inference_calls") != 0:
        errors.append("architecture-gate import must preserve zero external inference calls.")

    if gen_result.get("validation_result") != "pass":
        errors.append("generation-mode import result must pass.")
    if gen_result.get("accepted_mode_count") != 18 or gen_result.get("accepted_comparison_count") != 13:
        errors.append("generation-mode import must keep 18 modes and 13 comparisons.")
    if gen_result.get("accepted_hard_gap_count") != 0 or gen_result.get("accepted_promotable_comparison_count") != 0:
        errors.append("generation-mode import hard-gap/promotable counts drifted.")
    if gen_result.get("accepted_useful_solution_per_second") != 0.0:
        errors.append("generation-mode import useful-solution-per-second must remain 0.0.")
    if gen_result.get("expected_invalid_count") != 6:
        errors.append("generation-mode import must keep six expected-invalid controls.")
    if gen_result.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append("generation-mode import support_state_effect drifted.")
    if gen_fixture.get("source_project", {}).get("worktree_state") != "dirty_at_import_review":
        errors.append("generation-mode import must preserve dirty-at-import boundary.")

    if support_replay.get("pass") is not True:
        errors.append("Theseus support replay probe must record pass true.")
    if len(support_replay.get("replay_commands", [])) != 2:
        errors.append("Theseus support replay probe must keep two replayed validators.")
    if support_replay.get("support_state_effect") != "none":
        errors.append("Theseus support replay support_state_effect must remain none.")
    if support_replay.get("chapter_core_support_effect") != "none":
        errors.append("Theseus support replay chapter_core_support_effect must remain none.")

    public_boundary = task_fixture.get("public_boundary", {})
    operator = task_fixture.get("operator_execution", {})
    task_bundle = task_fixture.get("task_bundle", {})
    benchmark = task_fixture.get("benchmark_result", {})
    quality = task_fixture.get("quality_boundary", {})
    source_project = task_fixture.get("source_project", {})

    if task_result.get("validation_result") != "pass":
        errors.append("Theseus public task-bundle import result must pass.")
    if task_result.get("expected_invalid_count") != 7:
        errors.append("Theseus public task-bundle import must keep seven expected-invalid controls.")
    if task_result.get("source_report_count") != 7 or task_result.get("artifact_gap_count") != 5:
        errors.append("Theseus public task-bundle source report/artifact gap counts drifted.")
    if task_result.get("public_task_count") != 64 or benchmark.get("public_task_count") != 64:
        errors.append("Theseus public task-bundle import must keep 64 public metadata-only tasks.")
    if public_boundary.get("public_training_rows_written") != 0 or task_bundle.get("public_training_rows") != 0:
        errors.append("Theseus public task-bundle import must keep zero public training rows.")
    if public_boundary.get("external_inference_calls") != 0:
        errors.append("Theseus public task-bundle import must keep zero external inference calls.")
    if operator.get("operator_gate_count") != 12 or operator.get("operator_gates_passed") != 12:
        errors.append("Theseus public task-bundle import must keep 12/12 operator gates.")
    if task_result.get("benchmark_gate_count") != 18 or benchmark.get("benchmark_gates_passed") != 18:
        errors.append("Theseus public task-bundle import must keep 18/18 benchmark gates.")
    if task_result.get("residual_count") != 19 or benchmark.get("residual_count") != 19:
        errors.append("Theseus public task-bundle import must keep 19 residuals.")
    if benchmark.get("task_level_regressions_vs_single_stream") != 0:
        errors.append("Theseus public task-bundle import must keep zero task-level regressions.")
    if quality.get("quality_pass_count") != 45:
        errors.append("Theseus public task-bundle import must keep 45 quality-passing candidates.")
    if benchmark.get("student_candidate_count") != 512:
        errors.append("Theseus public task-bundle import must keep 512 student candidates in the public summary.")
    if source_project.get("working_tree_dirty_at_import") is not True or source_project.get("clean_live_replay_claimed") is not False:
        errors.append("Theseus public task-bundle import must preserve dirty-checkout/no-clean-live-replay boundary.")
    if task_result.get("support_state_effect") != "none" or task_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus public task-bundle import support effects must remain none.")

    if no_promotion.get("review_status") != "accepted":
        errors.append("Theseus public task-bundle no-promotion decision must remain accepted.")
    if no_promotion.get("transition_effect") != "no_change":
        errors.append("Theseus public task-bundle transition_effect must remain no_change.")
    if no_promotion.get("support_state_effect") != "blocks_promotion":
        errors.append("Theseus public task-bundle decision must keep blocks_promotion.")
    no_promotion_text = " ".join(
        [
            str(no_promotion.get("scope_boundary", "")),
            str(no_promotion.get("transition_reason", "")),
            " ".join(str(item) for item in no_promotion.get("non_claims", [])),
        ]
    )
    for fragment in ("clean live", "model quality", "chapter-core"):
        if fragment not in no_promotion_text:
            errors.append(f"Theseus no-promotion decision missing boundary fragment: {fragment}")

    artifact_counts = artifact_result.get("record_counts", {})
    artifact_replay = artifact_fixture.get("sanitized_replay_check", {})
    artifact_boundary = artifact_fixture.get("claim_boundary", {})
    artifact_safety = artifact_fixture.get("public_safety_boundary", {})
    if artifact_result.get("validation_result") != "pass":
        errors.append("Theseus artifact-retention replay import result must pass.")
    if artifact_result.get("expected_invalid_count") != 7:
        errors.append("Theseus artifact-retention replay import must keep seven expected-invalid controls.")
    if artifact_result.get("payload_bytes") != 41943527 or artifact_replay.get("payload_bytes") != 41943527:
        errors.append("Theseus artifact-retention replay import must keep 41,943,527 replayed payload bytes.")
    if artifact_result.get("archived_bytes") != 2389576 or artifact_replay.get("archived_bytes") != 2389576:
        errors.append("Theseus artifact-retention replay import must keep 2,389,576 archived bytes.")
    if artifact_result.get("new_support_state") != "prototype-backed":
        errors.append("Theseus artifact-retention replay import must remain prototype-backed.")
    if artifact_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus artifact-retention replay import must preserve chapter_core_support_effect none.")
    if artifact_boundary.get("chapter_core_promotion_claimed") is not False:
        errors.append("Theseus artifact-retention replay import must not claim chapter-core promotion.")
    if artifact_safety.get("public_training_rows_written") != 0 or artifact_safety.get("external_inference_calls") != 0:
        errors.append("Theseus artifact-retention replay import must keep zero public training rows and external inference calls.")
    for field in (
        "compressed_artifact_records",
        "compression_receipts",
        "proof_contract_receipt_records",
        "claim_records",
        "artifact_graph_records",
        "evidence_transition_records",
        "defeater_records",
    ):
        if artifact_counts.get(field) != 1:
            errors.append(f"Theseus artifact-retention replay import record count drifted for {field}.")
    if artifact_transition.get("review_status") != "accepted":
        errors.append("Theseus artifact-retention replay transition must remain accepted.")
    if artifact_transition.get("transition_effect") != "upward":
        errors.append("Theseus artifact-retention replay transition_effect must remain upward.")
    if artifact_transition.get("new_support_state") != "prototype-backed":
        errors.append("Theseus artifact-retention replay transition must remain prototype-backed.")
    if "does not prove clean live Project Theseus replay" not in " ".join(
        str(item) for item in artifact_transition.get("non_claims", [])
    ):
        errors.append("Theseus artifact-retention replay transition missing clean-live-replay non-claim.")

    governance_summary = governance_fixture.get("summary", {})
    governance_counts = governance_result.get("record_counts", {})
    governance_boundary = governance_fixture.get("claim_boundary", {})
    governance_safety = governance_fixture.get("public_safety_boundary", {})
    if governance_result.get("validation_result") != "pass":
        errors.append("Theseus governance-rights receipt suite import result must pass.")
    if governance_result.get("expected_invalid_count") != 7:
        errors.append("Theseus governance-rights receipt suite import must keep seven expected-invalid controls.")
    if governance_result.get("governance_scenario_count") != 4 or governance_summary.get("passed_fixture_count") != 4:
        errors.append("Theseus governance-rights receipt suite import must keep 4/4 governance-right fixtures.")
    if (
        governance_result.get("constitutional_scenario_count") != 4
        or governance_summary.get("passed_constitutional_fixture_count") != 4
    ):
        errors.append("Theseus governance-rights receipt suite import must keep 4/4 constitutional fixtures.")
    if governance_result.get("new_support_state") != "prototype-backed":
        errors.append("Theseus governance-rights receipt suite import must remain prototype-backed.")
    if governance_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus governance-rights receipt suite import must preserve chapter_core_support_effect none.")
    if governance_fixture.get("source_checkout_state") != "dirty_at_import_review":
        errors.append("Theseus governance-rights receipt suite import must preserve dirty-at-import boundary.")
    for field in (
        "chapter_core_promotion_claimed",
        "constitutional_chapter_core_promotion_claimed",
        "legal_rights_claimed",
        "institutional_governance_claimed",
        "moral_correctness_claimed",
        "reviewer_independence_claimed",
        "deployed_runtime_enforcement_claimed",
        "clean_live_theseus_replay_claimed",
    ):
        if governance_boundary.get(field) is not False:
            errors.append(f"Theseus governance-rights receipt suite import must not overclaim {field}.")
    if (
        governance_safety.get("public_training_rows_written") != 0
        or governance_safety.get("external_inference_calls") != 0
        or governance_safety.get("fallback_return_count") != 0
    ):
        errors.append("Theseus governance-rights receipt suite import must keep zero public training rows, external inference calls, and fallbacks.")
    for field, expected in (
        ("governance_right_records", 4),
        ("constitutional_predicate_records", 4),
        ("evidence_transition_records", 8),
        ("artifact_graph_records", 8),
        ("failure_boundary_records", 8),
    ):
        if governance_counts.get(field) != expected:
            errors.append(f"Theseus governance-rights receipt suite import record count drifted for {field}.")
    if governance_transition.get("review_status") != "accepted":
        errors.append("Theseus governance-rights receipt suite transition must remain accepted.")
    if governance_transition.get("transition_effect") != "upward":
        errors.append("Theseus governance-rights receipt suite transition_effect must remain upward.")
    if governance_transition.get("new_support_state") != "prototype-backed":
        errors.append("Theseus governance-rights receipt suite transition must remain prototype-backed.")
    transition_nonclaims = " ".join(str(item) for item in governance_transition.get("non_claims", []))
    if "does not prove legal rights" not in transition_nonclaims:
        errors.append("Theseus governance-rights receipt suite transition missing legal-rights non-claim.")

    simulation_summary = simulation_fixture.get("summary", {})
    simulation_counts = simulation_result.get("record_counts", {})
    simulation_boundary = simulation_fixture.get("claim_boundary", {})
    simulation_safety = simulation_fixture.get("public_safety_boundary", {})
    if simulation_result.get("validation_result") != "pass":
        errors.append("Theseus simulation-fidelity receipt suite import result must pass.")
    if simulation_result.get("expected_invalid_count") != 7:
        errors.append("Theseus simulation-fidelity receipt suite import must keep seven expected-invalid controls.")
    if simulation_result.get("fixture_scenario_count") != 5 or simulation_summary.get("passed_fixture_count") != 5:
        errors.append("Theseus simulation-fidelity receipt suite import must keep 5/5 fixture scenarios.")
    if simulation_result.get("world_adapter_receipt_count") != 6 or simulation_summary.get("world_adapter_receipt_count") != 6:
        errors.append("Theseus simulation-fidelity receipt suite import must keep six world-adapter receipts.")
    if simulation_result.get("new_support_state") != "prototype-backed":
        errors.append("Theseus simulation-fidelity receipt suite import must remain prototype-backed.")
    if simulation_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus simulation-fidelity receipt suite import must preserve chapter_core_support_effect none.")
    if simulation_fixture.get("source_checkout_state") != "dirty_at_import_review":
        errors.append("Theseus simulation-fidelity receipt suite import must preserve dirty-at-import boundary.")
    for field in (
        "chapter_core_promotion_claimed",
        "simulation_adequacy_claimed",
        "physical_feasibility_claimed",
        "benchmark_transfer_claimed",
        "native_kv_parity_claimed",
        "deployment_claimed",
        "live_simulator_claimed",
        "learned_generation_claimed",
        "model_quality_claimed",
        "economic_outcome_claimed",
        "clean_live_theseus_replay_claimed",
    ):
        if simulation_boundary.get(field) is not False:
            errors.append(f"Theseus simulation-fidelity receipt suite import must not overclaim {field}.")
    if (
        simulation_safety.get("public_training_rows_written") != 0
        or simulation_safety.get("external_inference_calls") != 0
        or simulation_safety.get("fallback_return_count") != 0
    ):
        errors.append("Theseus simulation-fidelity receipt suite import must keep zero public training rows, external inference calls, and fallbacks.")
    for field, expected in (
        ("claim_records", 6),
        ("simulation_contract_records", 6),
        ("fidelity_records", 6),
        ("world_adapter_receipts", 6),
        ("evidence_transition_records", 6),
        ("failure_boundary_records", 6),
    ):
        if simulation_counts.get(field) != expected:
            errors.append(f"Theseus simulation-fidelity receipt suite import record count drifted for {field}.")
    if simulation_transition.get("review_status") != "accepted":
        errors.append("Theseus simulation-fidelity receipt suite transition must remain accepted.")
    if simulation_transition.get("transition_effect") != "upward":
        errors.append("Theseus simulation-fidelity receipt suite transition_effect must remain upward.")
    if simulation_transition.get("new_support_state") != "prototype-backed":
        errors.append("Theseus simulation-fidelity receipt suite transition must remain prototype-backed.")
    simulation_nonclaims = " ".join(str(item) for item in simulation_transition.get("non_claims", []))
    if "does not prove simulator adequacy" not in simulation_nonclaims:
        errors.append("Theseus simulation-fidelity receipt suite transition missing simulator-adequacy non-claim.")

    rlds_minari_summary = rlds_minari_fixture.get("summary", {})
    rlds_minari_export = rlds_minari_fixture.get("export_manifest", {})
    rlds_minari_boundary = rlds_minari_fixture.get("claim_boundary", {})
    rlds_minari_safety = rlds_minari_fixture.get("public_safety_boundary", {})
    if rlds_minari_result.get("validation_result") != "pass":
        errors.append("Theseus RLDS/Minari trace-export import result must pass.")
    if rlds_minari_result.get("expected_invalid_control_count") != 7:
        errors.append("Theseus RLDS/Minari trace-export import must keep seven expected-invalid controls.")
    if rlds_minari_result.get("export_count") != 1 or rlds_minari_summary.get("export_count") != 1:
        errors.append("Theseus RLDS/Minari trace-export import must keep one export.")
    if rlds_minari_result.get("ready_count") != 1 or rlds_minari_summary.get("ready_count") != 1:
        errors.append("Theseus RLDS/Minari trace-export import must keep one READY export.")
    if rlds_minari_result.get("format_count") != 3 or len(rlds_minari_export.get("formats", [])) != 3:
        errors.append("Theseus RLDS/Minari trace-export import must keep three formats.")
    if rlds_minari_result.get("field_count") != 7 or len(rlds_minari_export.get("fields", [])) != 7:
        errors.append("Theseus RLDS/Minari trace-export import must keep seven fields.")
    if rlds_minari_result.get("license_metadata_required") is not True:
        errors.append("Theseus RLDS/Minari trace-export import must require license metadata.")
    if rlds_minari_result.get("replay_smoke_required") is not True:
        errors.append("Theseus RLDS/Minari trace-export import must require replay smoke.")
    if rlds_minari_result.get("new_support_state") != "prototype-backed":
        errors.append("Theseus RLDS/Minari trace-export import must remain prototype-backed.")
    if rlds_minari_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus RLDS/Minari trace-export import must preserve chapter_core_support_effect none.")
    if rlds_minari_fixture.get("source_checkout_state") != "dirty_at_import_review":
        errors.append("Theseus RLDS/Minari trace-export import must preserve dirty-at-import boundary.")
    for field in (
        "chapter_core_promotion_claimed",
        "rlds_dataset_correctness_claimed",
        "minari_dataset_quality_claimed",
        "simulator_adequacy_claimed",
        "replay_success_claimed",
        "training_data_publication_claimed",
        "model_quality_claimed",
        "economic_outcome_claimed",
        "clean_live_theseus_replay_claimed",
    ):
        if rlds_minari_boundary.get(field) is not False:
            errors.append(f"Theseus RLDS/Minari trace-export import must not overclaim {field}.")
    if (
        rlds_minari_safety.get("public_training_rows_written") != 0
        or rlds_minari_safety.get("external_inference_calls") != 0
        or rlds_minari_safety.get("raw_episode_payload_copied") is not False
    ):
        errors.append("Theseus RLDS/Minari trace-export import must keep zero public training rows, external inference calls, and copied episode payloads.")
    if rlds_minari_transition.get("review_status") != "accepted":
        errors.append("Theseus RLDS/Minari trace-export transition must remain accepted.")
    if rlds_minari_transition.get("transition_effect") != "upward":
        errors.append("Theseus RLDS/Minari trace-export transition_effect must remain upward.")
    if rlds_minari_transition.get("new_support_state") != "prototype-backed":
        errors.append("Theseus RLDS/Minari trace-export transition must remain prototype-backed.")
    rlds_minari_nonclaims = " ".join(str(item) for item in rlds_minari_transition.get("non_claims", []))
    if "does not prove RLDS dataset correctness" not in rlds_minari_nonclaims:
        errors.append("Theseus RLDS/Minari trace-export transition missing dataset-correctness non-claim.")

    module_dod_summary = module_dod_fixture.get("summary", {})
    module_dod_boundary = module_dod_fixture.get("claim_boundary", {})
    module_dod_safety = module_dod_result.get("public_safety", {})
    if module_dod_result.get("verification_result") != "pass":
        errors.append("Theseus module definition-of-done import result must pass.")
    if module_dod_result.get("expected_invalid_control_count") != 7:
        errors.append("Theseus module definition-of-done import must keep seven expected-invalid controls.")
    if module_dod_fixture.get("source_checkout_state") != "dirty_at_import_review":
        errors.append("Theseus module definition-of-done import must preserve dirty-at-import boundary.")
    if module_dod_result.get("trigger_state") != "GREEN":
        errors.append("Theseus module definition-of-done import must keep GREEN trigger state.")
    if module_dod_summary.get("module_records_ready") != 22 or module_dod_summary.get("module_record_count") != 22:
        errors.append("Theseus module definition-of-done import must keep 22/22 ready module records.")
    if module_dod_summary.get("hard_gap_count") != 0 or module_dod_summary.get("warning_count") != 0:
        errors.append("Theseus module definition-of-done import must keep zero hard gaps and warnings.")
    if module_dod_summary.get("source_backlog_work_card_count") != 20:
        errors.append("Theseus module definition-of-done import must keep 20 source-backlog work cards.")
    if module_dod_summary.get("source_backlog_route_smoke_passed") is not True:
        errors.append("Theseus module definition-of-done import must keep route smoke pass.")
    if module_dod_result.get("support_state_effect") != "bounded_non_core_transition_only":
        errors.append("Theseus module definition-of-done import support_state_effect drifted.")
    if module_dod_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus module definition-of-done import must preserve chapter_core_support_effect none.")
    if module_dod_boundary.get("chapter_core_claim_promotion") is not False:
        errors.append("Theseus module definition-of-done import must not claim chapter-core promotion.")
    if module_dod_boundary.get("capability_claim") is not False:
        errors.append("Theseus module definition-of-done import must not claim module capability.")
    if (
        module_dod_safety.get("raw_report_copied") is not False
        or module_dod_safety.get("private_payload_copied") is not False
        or module_dod_safety.get("private_path_fields_redacted") is not True
    ):
        errors.append("Theseus module definition-of-done import must keep raw-report/private-payload redaction boundary.")
    if module_dod_transition.get("review_status") != "accepted":
        errors.append("Theseus module definition-of-done transition must remain accepted.")
    if module_dod_transition.get("transition_effect") != "upward":
        errors.append("Theseus module definition-of-done transition_effect must remain upward.")
    if module_dod_transition.get("new_support_state") != "prototype-backed":
        errors.append("Theseus module definition-of-done transition must remain prototype-backed.")
    module_dod_nonclaims = " ".join(str(item) for item in module_dod_transition.get("non_claims", []))
    if "does not prove clean live Project Theseus replay" not in module_dod_nonclaims:
        errors.append("Theseus module definition-of-done transition missing clean-live-replay non-claim.")

    project_registry_summary = project_registry_fixture.get("summary", {})
    project_registry_boundary = project_registry_fixture.get("claim_boundary", {})
    project_registry_safety = project_registry_result.get("public_safety", {})
    if project_registry_result.get("verification_result") != "pass":
        errors.append("Theseus project-registry import result must pass.")
    if project_registry_result.get("expected_invalid_control_count") != 9:
        errors.append("Theseus project-registry import must keep nine expected-invalid controls.")
    if project_registry_fixture.get("source_checkout_state") != "dirty_at_import_review":
        errors.append("Theseus project-registry import must preserve dirty-at-import boundary.")
    if project_registry_result.get("trigger_state") != "GREEN":
        errors.append("Theseus project-registry import must keep GREEN trigger state.")
    if project_registry_result.get("surface_count") != 24:
        errors.append("Theseus project-registry import must keep 24 owned lifecycle surfaces.")
    if project_registry_summary.get("entry_count") != 5662 or project_registry_summary.get("registered_path_count") != 5662:
        errors.append("Theseus project-registry import must keep 5,662 registered paths.")
    if project_registry_summary.get("coverage_ratio") != 1.0:
        errors.append("Theseus project-registry import must keep full coverage ratio.")
    for field in (
        "unregistered_active_source_count",
        "unclassified_duplicate_family_count",
        "stale_report_output_count",
        "missing_report_output_count",
        "generated_source_artifact_count",
        "registry_governance_violation_count",
        "registry_hard_governance_violation_count",
    ):
        if project_registry_summary.get(field) != 0:
            errors.append(f"Theseus project-registry import field drifted for {field}.")
    if project_registry_result.get("support_state_effect") != "bounded_non_core_transition_only":
        errors.append("Theseus project-registry import support_state_effect drifted.")
    if project_registry_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus project-registry import must preserve chapter_core_support_effect none.")
    for field in (
        "chapter_core_claim_promotion",
        "clean_live_replay_claim",
        "deployment_claim",
        "model_quality_claim",
        "capability_claim",
    ):
        if project_registry_boundary.get(field) is not False:
            errors.append(f"Theseus project-registry import must not overclaim {field}.")
    if (
        project_registry_safety.get("raw_report_copied") is not False
        or project_registry_safety.get("private_payload_copied") is not False
        or project_registry_safety.get("private_path_fields_redacted") is not True
    ):
        errors.append("Theseus project-registry import must keep raw-report/private-payload redaction boundary.")
    if project_registry_transition.get("review_status") != "accepted":
        errors.append("Theseus project-registry transition must remain accepted.")
    if project_registry_transition.get("transition_effect") != "upward":
        errors.append("Theseus project-registry transition_effect must remain upward.")
    if project_registry_transition.get("new_support_state") != "prototype-backed":
        errors.append("Theseus project-registry transition must remain prototype-backed.")
    project_registry_nonclaims = " ".join(str(item) for item in project_registry_transition.get("non_claims", []))
    if "does not prove clean live Project Theseus replay" not in project_registry_nonclaims:
        errors.append("Theseus project-registry transition missing clean-live-replay non-claim.")

    book_crosswalk_summary = book_crosswalk_fixture.get("summary", {})
    book_crosswalk_boundary = book_crosswalk_fixture.get("claim_boundary", {})
    book_crosswalk_safety = book_crosswalk_fixture.get("public_safety_boundary", {})
    if book_crosswalk_result.get("verification_result") != "pass":
        errors.append("Theseus book-to-Theseus crosswalk import result must pass.")
    if book_crosswalk_result.get("expected_invalid_control_count") != 10:
        errors.append("Theseus book-to-Theseus crosswalk import must keep ten expected-invalid controls.")
    if book_crosswalk_fixture.get("source_checkout_state") != "dirty_at_import_review":
        errors.append("Theseus book-to-Theseus crosswalk import must preserve dirty-at-import boundary.")
    if book_crosswalk_result.get("trigger_state") != "GREEN":
        errors.append("Theseus book-to-Theseus crosswalk import must keep GREEN trigger state.")
    if book_crosswalk_summary.get("theseus_to_book_evidence_count") != 53:
        errors.append("Theseus book-to-Theseus crosswalk import must keep 53 public-safe pointer rows.")
    if book_crosswalk_summary.get("roadmap_backlog_item_count") != 20:
        errors.append("Theseus book-to-Theseus crosswalk import must keep 20 backlog cards.")
    if book_crosswalk_summary.get("source_sync_review_decision_count") != 134:
        errors.append("Theseus book-to-Theseus crosswalk import must keep 134 source-sync review decisions.")
    for field in (
        "removed_source_file_count",
        "stale_phase_count",
        "missing_source_basis_count",
        "done_phase_missing_evidence_count",
    ):
        if book_crosswalk_summary.get(field) != 0:
            errors.append(f"Theseus book-to-Theseus crosswalk import field drifted for {field}.")
    if book_crosswalk_result.get("support_state_effect") != "blocks_promotion":
        errors.append("Theseus book-to-Theseus crosswalk import support_state_effect must remain blocks_promotion.")
    if book_crosswalk_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus book-to-Theseus crosswalk import must preserve chapter_core_support_effect none.")
    for field in (
        "chapter_core_claim_promotion",
        "clean_live_replay_claim",
        "deployment_claim",
        "model_quality_claim",
        "capability_claim",
    ):
        if book_crosswalk_boundary.get(field) is not False:
            errors.append(f"Theseus book-to-Theseus crosswalk import must not overclaim {field}.")
    if book_crosswalk_boundary.get("new_support_state") != "argument":
        errors.append("Theseus book-to-Theseus crosswalk import must remain argument support.")
    if (
        book_crosswalk_safety.get("raw_report_copied") is not False
        or book_crosswalk_safety.get("private_payload_copied") is not False
        or book_crosswalk_safety.get("private_path_fields_redacted") is not True
        or book_crosswalk_safety.get("public_training_rows_written") != 0
        or book_crosswalk_safety.get("external_inference_calls") != 0
    ):
        errors.append("Theseus book-to-Theseus crosswalk import must keep raw-report/private-payload/public-safety boundary.")
    if book_crosswalk_transition.get("review_status") != "accepted":
        errors.append("Theseus book-to-Theseus crosswalk no-promotion decision must remain accepted.")
    if book_crosswalk_transition.get("transition_effect") != "no_change":
        errors.append("Theseus book-to-Theseus crosswalk transition_effect must remain no_change.")
    if book_crosswalk_transition.get("new_support_state") != "argument":
        errors.append("Theseus book-to-Theseus crosswalk transition must remain argument.")
    if book_crosswalk_transition.get("support_state_effect") != "blocks_promotion":
        errors.append("Theseus book-to-Theseus crosswalk transition must keep blocks_promotion.")
    book_crosswalk_nonclaims = " ".join(str(item) for item in book_crosswalk_transition.get("non_claims", []))
    if "does not prove clean live Project Theseus replay" not in book_crosswalk_nonclaims:
        errors.append("Theseus book-to-Theseus crosswalk transition missing clean-live-replay non-claim.")

    metrics = {
        "static_report_imports": 2,
        "support_replay_count": 1,
        "artifact_retention_replay_imports": 1,
        "governance_rights_receipt_imports": 1,
        "simulation_fidelity_receipt_imports": 1,
        "rlds_minari_trace_export_imports": 1,
        "module_dod_imports": 1,
        "project_registry_imports": 1,
        "book_crosswalk_imports": 1,
        "support_replay_commands": len(support_replay.get("replay_commands", [])),
        "support_replay_tracked_artifacts": len(support_replay.get("tracked_artifacts", [])),
        "architecture_gate_count": arch_result.get("accepted_gate_count"),
        "architecture_gate_passed": arch_result.get("accepted_passed_count"),
        "architecture_expected_invalid": arch_result.get("expected_invalid_count"),
        "architecture_source_sha": arch_result.get("source_artifact_sha256"),
        "architecture_public_sha": arch_result.get("accepted_public_report_sha256"),
        "generation_mode_count": gen_result.get("accepted_mode_count"),
        "generation_comparison_count": gen_result.get("accepted_comparison_count"),
        "generation_hard_gap_count": gen_result.get("accepted_hard_gap_count"),
        "promotable_comparison_count": gen_result.get("accepted_promotable_comparison_count"),
        "useful_solution_per_second": gen_result.get("accepted_useful_solution_per_second"),
        "generation_expected_invalid": gen_result.get("expected_invalid_count"),
        "generation_source_sha": gen_result.get("source_artifact_sha256"),
        "generation_public_sha": gen_result.get("accepted_public_report_sha256"),
        "public_task_count": task_result.get("public_task_count"),
        "public_training_rows": public_boundary.get("public_training_rows_written"),
        "external_inference_calls": public_boundary.get("external_inference_calls"),
        "operator_gate_count": operator.get("operator_gate_count"),
        "operator_gate_passed": operator.get("operator_gates_passed"),
        "benchmark_gate_count": task_result.get("benchmark_gate_count"),
        "benchmark_gate_passed": benchmark.get("benchmark_gates_passed"),
        "residual_count": task_result.get("residual_count"),
        "task_regression_count": benchmark.get("task_level_regressions_vs_single_stream"),
        "artifact_gap_count": task_result.get("artifact_gap_count"),
        "source_report_count": task_result.get("source_report_count"),
        "student_candidate_count": benchmark.get("student_candidate_count"),
        "quality_pass_count": quality.get("quality_pass_count"),
        "public_calibration_pass_rate": benchmark.get("real_public_task_pass_rate"),
        "task_expected_invalid": task_result.get("expected_invalid_count"),
        "artifact_payload_bytes": artifact_result.get("payload_bytes"),
        "artifact_archived_bytes": artifact_result.get("archived_bytes"),
        "artifact_compression_ratio": artifact_result.get("compression_ratio_observed_not_benchmarked"),
        "artifact_expected_invalid": artifact_result.get("expected_invalid_count"),
        "artifact_upward_transitions": 1,
        "governance_rights_expected_invalid": governance_result.get("expected_invalid_count"),
        "governance_rights_scenarios": governance_result.get("governance_scenario_count"),
        "governance_rights_constitutional_scenarios": governance_result.get("constitutional_scenario_count"),
        "governance_rights_records": governance_counts.get("governance_right_records"),
        "governance_rights_predicate_records": governance_counts.get("constitutional_predicate_records"),
        "governance_rights_evidence_transition_records": governance_counts.get("evidence_transition_records"),
        "governance_rights_artifact_graph_records": governance_counts.get("artifact_graph_records"),
        "governance_rights_failure_boundary_records": governance_counts.get("failure_boundary_records"),
        "governance_rights_upward_transitions": 1,
        "simulation_fidelity_expected_invalid": simulation_result.get("expected_invalid_count"),
        "simulation_fidelity_fixture_scenarios": simulation_result.get("fixture_scenario_count"),
        "simulation_fidelity_contract_records": simulation_counts.get("simulation_contract_records"),
        "simulation_fidelity_world_adapter_receipts": simulation_counts.get("world_adapter_receipts"),
        "simulation_fidelity_evidence_transition_records": simulation_counts.get("evidence_transition_records"),
        "simulation_fidelity_failure_boundary_records": simulation_counts.get("failure_boundary_records"),
        "simulation_fidelity_blocked_transfers": simulation_summary.get("blocked_transfer_count"),
        "simulation_fidelity_downgraded_claims": simulation_summary.get("downgraded_claim_count"),
        "simulation_fidelity_upward_transitions": 1,
        "rlds_minari_expected_invalid": rlds_minari_result.get("expected_invalid_control_count"),
        "rlds_minari_export_count": rlds_minari_result.get("export_count"),
        "rlds_minari_ready_count": rlds_minari_result.get("ready_count"),
        "rlds_minari_manifest_count": rlds_minari_result.get("manifest_count"),
        "rlds_minari_format_count": rlds_minari_result.get("format_count"),
        "rlds_minari_field_count": rlds_minari_result.get("field_count"),
        "rlds_minari_license_metadata_required": rlds_minari_result.get("license_metadata_required"),
        "rlds_minari_replay_smoke_required": rlds_minari_result.get("replay_smoke_required"),
        "rlds_minari_upward_transitions": 1,
        "module_dod_expected_invalid": module_dod_result.get("expected_invalid_control_count"),
        "module_dod_ready_records": module_dod_summary.get("module_records_ready"),
        "module_dod_total_records": module_dod_summary.get("module_record_count"),
        "module_dod_hard_gaps": module_dod_summary.get("hard_gap_count"),
        "module_dod_warnings": module_dod_summary.get("warning_count"),
        "module_dod_source_backlog_work_cards": module_dod_summary.get("source_backlog_work_card_count"),
        "module_dod_upward_transitions": 1,
        "project_registry_expected_invalid": project_registry_result.get("expected_invalid_control_count"),
        "project_registry_registered_paths": project_registry_summary.get("registered_path_count"),
        "project_registry_entry_count": project_registry_summary.get("entry_count"),
        "project_registry_surface_count": project_registry_result.get("surface_count"),
        "project_registry_unregistered_active_sources": project_registry_summary.get("unregistered_active_source_count"),
        "project_registry_unclassified_duplicates": project_registry_summary.get("unclassified_duplicate_family_count"),
        "project_registry_stale_report_outputs": project_registry_summary.get("stale_report_output_count"),
        "project_registry_missing_report_outputs": project_registry_summary.get("missing_report_output_count"),
        "project_registry_generated_source_artifacts": project_registry_summary.get("generated_source_artifact_count"),
        "project_registry_governance_violations": project_registry_summary.get("registry_governance_violation_count"),
        "project_registry_hard_governance_violations": project_registry_summary.get("registry_hard_governance_violation_count"),
        "project_registry_upward_transitions": 1,
        "book_crosswalk_expected_invalid": book_crosswalk_result.get("expected_invalid_control_count"),
        "book_crosswalk_pointer_rows": book_crosswalk_summary.get("theseus_to_book_evidence_count"),
        "book_crosswalk_backlog_cards": book_crosswalk_summary.get("roadmap_backlog_item_count"),
        "book_crosswalk_source_sync_decisions": book_crosswalk_summary.get("source_sync_review_decision_count"),
        "book_crosswalk_changed_source_files": book_crosswalk_summary.get("changed_source_file_count"),
        "book_crosswalk_no_promotion_decisions": 1,
        "expected_invalid_total": arch_result.get("expected_invalid_count", 0)
        + gen_result.get("expected_invalid_count", 0)
        + task_result.get("expected_invalid_count", 0)
        + artifact_result.get("expected_invalid_count", 0)
        + governance_result.get("expected_invalid_count", 0)
        + simulation_result.get("expected_invalid_count", 0)
        + rlds_minari_result.get("expected_invalid_control_count", 0)
        + module_dod_result.get("expected_invalid_control_count", 0)
        + project_registry_result.get("expected_invalid_control_count", 0)
        + book_crosswalk_result.get("expected_invalid_control_count", 0),
        "no_promotion_decisions": 2,
        "source_commit_short": str(source_project.get("commit", ""))[:8],
    }
    return metrics, errors


def build_report(metrics: dict[str, Any], errors: list[str]) -> str:
    validation_lines = ["- None."] if not errors else [f"- {error}" for error in errors]
    return "\n".join(
        [
            "# Project Theseus Static Import Status Ledger",
            "",
            "Generated by `python3 scripts/validate_project_theseus_static_import_status_ledger.py --write`.",
            "",
            "This ledger replaces the former long `Project Theseus static import lane` cell in `docs/v1_0_candidate_status.md`. It records public-safe Project Theseus import evidence, replay probes, and no-promotion boundaries without claiming a clean live Theseus replay, model quality, benchmark superiority, speed, useful-solution-per-second improvement, deployment readiness, self-evolution, or chapter-core support movement.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Sanitized static report imports | {metrics['static_report_imports']} |",
            f"| Support replay probes | {metrics['support_replay_count']} |",
            f"| Artifact-retention replay imports | {metrics['artifact_retention_replay_imports']} |",
            f"| Governance-rights receipt imports | {metrics['governance_rights_receipt_imports']} |",
            f"| Simulation-fidelity receipt imports | {metrics['simulation_fidelity_receipt_imports']} |",
            f"| RLDS/Minari trace-export imports | {metrics['rlds_minari_trace_export_imports']} |",
            f"| Module definition-of-done imports | {metrics['module_dod_imports']} |",
            f"| Project-registry imports | {metrics['project_registry_imports']} |",
            f"| Book-to-Theseus crosswalk pointer imports | {metrics['book_crosswalk_imports']} |",
            f"| Replayed validators in support probe | {metrics['support_replay_commands']} |",
            f"| Support replay tracked artifacts | {metrics['support_replay_tracked_artifacts']} |",
            f"| Architecture gates passed | {metrics['architecture_gate_passed']} / {metrics['architecture_gate_count']} |",
            f"| Generation modes / comparisons | {metrics['generation_mode_count']} / {metrics['generation_comparison_count']} |",
            f"| Promotable comparisons | {metrics['promotable_comparison_count']} |",
            f"| Useful solution per second | {metrics['useful_solution_per_second']} |",
            f"| Metadata-only public tasks | {metrics['public_task_count']} |",
            f"| Public training rows | {metrics['public_training_rows']} |",
            f"| External inference calls | {metrics['external_inference_calls']} |",
            f"| Operator gates passed | {metrics['operator_gate_passed']} / {metrics['operator_gate_count']} |",
            f"| Benchmark gates passed | {metrics['benchmark_gate_passed']} / {metrics['benchmark_gate_count']} |",
            f"| Residuals / artifact gaps | {metrics['residual_count']} / {metrics['artifact_gap_count']} |",
            f"| Expected-invalid controls | {metrics['expected_invalid_total']} |",
            f"| Accepted no-promotion decisions | {metrics['no_promotion_decisions']} |",
            f"| Accepted bounded artifact-retention transitions | {metrics['artifact_upward_transitions']} |",
            f"| Accepted bounded governance-rights transitions | {metrics['governance_rights_upward_transitions']} |",
            f"| Accepted bounded simulation-fidelity transitions | {metrics['simulation_fidelity_upward_transitions']} |",
            f"| Accepted bounded RLDS/Minari trace-export transitions | {metrics['rlds_minari_upward_transitions']} |",
            f"| Accepted bounded module definition-of-done transitions | {metrics['module_dod_upward_transitions']} |",
            f"| Accepted bounded project-registry transitions | {metrics['project_registry_upward_transitions']} |",
            f"| Book-to-Theseus public-safe pointer rows | {metrics['book_crosswalk_pointer_rows']} |",
            "",
            "## Status-Page Row",
            "",
            compact_status_row(metrics),
            "",
            "## Imported Evidence Surfaces",
            "",
            f"- `docs/theseus_report_import_slice.md` records source commit `{metrics['source_commit_short']}`, a dirty-at-import-review boundary, source SHA-256 `{metrics['architecture_source_sha']}`, public fixture SHA-256 `{metrics['architecture_public_sha']}`, and {metrics['architecture_gate_passed']}/{metrics['architecture_gate_count']} architecture gates passed with {metrics['architecture_expected_invalid']} expected-invalid controls.",
            f"- `docs/theseus_generation_mode_import_slice.md` records source SHA-256 `{metrics['generation_source_sha']}`, public fixture SHA-256 `{metrics['generation_public_sha']}`, {metrics['generation_mode_count']} modes, {metrics['generation_comparison_count']} comparisons, {metrics['generation_hard_gap_count']} hard gaps, {metrics['promotable_comparison_count']} promotable comparisons, {metrics['useful_solution_per_second']} useful-solution-per-second evidence, and {metrics['generation_expected_invalid']} expected-invalid controls.",
            f"- `docs/theseus_support_replay_probe.md` records {metrics['support_replay_commands']} local validator replays and {metrics['support_replay_tracked_artifacts']} tracked artifact hashes with support-state effect `none`.",
            f"- `docs/theseus_public_task_bundle_import.md` records {metrics['source_report_count']} source reports, {metrics['public_task_count']} metadata-only public tasks, {metrics['public_training_rows']} public training rows, {metrics['external_inference_calls']} external inference calls, {metrics['operator_gate_passed']}/{metrics['operator_gate_count']} operator gates, {metrics['benchmark_gate_passed']}/{metrics['benchmark_gate_count']} benchmark gates, {metrics['residual_count']} residuals, {metrics['task_regression_count']} task-level regressions, {metrics['student_candidate_count']} student candidates in the public summary, {metrics['quality_pass_count']} quality-passing candidates, {metrics['artifact_gap_count']} artifact gaps, and {metrics['task_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json` is the accepted no-promotion decision: it blocks clean-live-replay, model-quality, benchmark-superiority, generation-speed, useful-solution-per-second, support-state, deployment, self-evolution, and chapter-core promotion claims.",
            f"- `docs/theseus_artifact_retention_replay_import.md` records one sanitized artifact-retention replay import with {metrics['artifact_payload_bytes']} replayed payload bytes, {metrics['artifact_archived_bytes']} archived bytes, observed ratio {metrics['artifact_compression_ratio']} not benchmarked, one compressed-artifact record, one proof-contract receipt, one artifact-graph record, one storage evidence-transition record, and {metrics['artifact_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_artifact_retention_replay_import_prototype_backed.json` is the accepted bounded upward transition for `project-theseus-as-report-first-implementation-reference.artifact_retention_replay_gate_import`; it does not prove clean live Project Theseus replay and does not promote the Project Theseus chapter core claim.",
            f"- `docs/theseus_governance_rights_receipt_suite_import.md` records one sanitized governance-rights receipt suite import with {metrics['governance_rights_scenarios']} governance scenarios, {metrics['governance_rights_constitutional_scenarios']} constitutional-predicate scenarios, {metrics['governance_rights_records']} governance-right records, {metrics['governance_rights_predicate_records']} constitutional-predicate records, {metrics['governance_rights_evidence_transition_records']} evidence-transition records, {metrics['governance_rights_artifact_graph_records']} artifact-graph records, {metrics['governance_rights_failure_boundary_records']} failure-boundary records, and {metrics['governance_rights_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_governance_rights_receipt_suite_import_prototype_backed.json` is the accepted bounded upward transition for `moral-uncertainty-and-value-conflict.theseus_governance_rights_receipt_suite_import`; it does not prove legal rights, institutional governance, moral correctness, reviewer independence, deployed governance, clean live Project Theseus replay, or any chapter core claim.",
            f"- `docs/theseus_simulation_fidelity_receipt_suite_import.md` records one sanitized simulation-fidelity receipt suite import with {metrics['simulation_fidelity_fixture_scenarios']} passed fixture scenarios, {metrics['simulation_fidelity_contract_records']} simulation contract records, {metrics['simulation_fidelity_world_adapter_receipts']} world-adapter receipts, {metrics['simulation_fidelity_evidence_transition_records']} evidence-transition records, {metrics['simulation_fidelity_failure_boundary_records']} failure-boundary records, {metrics['simulation_fidelity_blocked_transfers']} blocked transfer, {metrics['simulation_fidelity_downgraded_claims']} downgraded claim, and {metrics['simulation_fidelity_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_simulation_fidelity_receipt_suite_import_prototype_backed.json` is the accepted bounded upward transition for `resource-economics.simulation_fidelity_receipt_suite_import`; it does not prove simulator adequacy, physical feasibility, benchmark transfer, native KV parity, deployment, model quality, economic outcome, clean live Project Theseus replay, or any chapter core claim.",
            f"- `docs/theseus_rlds_minari_trace_export_import.md` records one sanitized RLDS/Minari trace-export import with {metrics['rlds_minari_export_count']} READY export, {metrics['rlds_minari_manifest_count']} manifest, {metrics['rlds_minari_format_count']} declared formats, {metrics['rlds_minari_field_count']} declared fields, license metadata required `{metrics['rlds_minari_license_metadata_required']}`, replay smoke required `{metrics['rlds_minari_replay_smoke_required']}`, and {metrics['rlds_minari_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_rlds_minari_trace_export_import_prototype_backed.json` is the accepted bounded upward transition for `resource-economics.theseus_rlds_minari_trace_export_import`; it does not prove RLDS dataset correctness, Minari dataset quality, simulator adequacy, replay success, model quality, economic outcome, clean live Project Theseus replay, or any chapter core claim.",
            f"- `docs/theseus_module_definition_of_done_import.md` records one sanitized module definition-of-done gate import with {metrics['module_dod_ready_records']}/{metrics['module_dod_total_records']} ready module records, {metrics['module_dod_hard_gaps']} hard gaps, {metrics['module_dod_warnings']} warnings, {metrics['module_dod_source_backlog_work_cards']} source-backlog work cards, and {metrics['module_dod_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_module_definition_of_done_import_prototype_backed.json` is the accepted bounded upward transition for `project-theseus-as-report-first-implementation-reference.module_definition_of_done_gate_import`; it does not prove module capability, clean live Project Theseus replay, deployed behavior, model quality, or any chapter core claim.",
            f"- `docs/theseus_project_registry_import.md` records one sanitized project-registry import with {metrics['project_registry_registered_paths']} registered paths out of {metrics['project_registry_entry_count']} entries, {metrics['project_registry_surface_count']} surfaces, {metrics['project_registry_unregistered_active_sources']} unregistered active sources, {metrics['project_registry_unclassified_duplicates']} unclassified duplicate families, {metrics['project_registry_stale_report_outputs']} stale report outputs, {metrics['project_registry_missing_report_outputs']} missing report outputs, {metrics['project_registry_generated_source_artifacts']} generated source artifacts, {metrics['project_registry_governance_violations']} registry-governance violations, {metrics['project_registry_hard_governance_violations']} hard governance violations, and {metrics['project_registry_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_project_registry_import_prototype_backed.json` is the accepted bounded upward transition for `project-theseus-as-report-first-implementation-reference.project_registry_reality_import`; it does not prove clean live Project Theseus replay, deployment, model quality, self-evolution safety, or any chapter core claim.",
            f"- `docs/theseus_book_crosswalk_import.md` records one sanitized book-to-Theseus crosswalk pointer import with {metrics['book_crosswalk_pointer_rows']} public-safe pointer rows, {metrics['book_crosswalk_backlog_cards']} backlog cards, {metrics['book_crosswalk_source_sync_decisions']} source-sync review decisions, {metrics['book_crosswalk_changed_source_files']} changed AI-book source files, and {metrics['book_crosswalk_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_book_crosswalk_import_no_change.json` is the accepted no-promotion decision for `project-theseus-as-report-first-implementation-reference.book_to_theseus_crosswalk_pointer`; it keeps the crosswalk pointer at `argument` and blocks clean-live-replay, model-quality, deployment, support-state, and chapter-core promotion claims.",
            "",
            "## Non-Claim Boundary",
            "",
            "- This ledger does not prove clean live Project Theseus replay.",
            "- This ledger does not prove model quality, benchmark superiority, generation speed, useful-solution-per-second improvement, deployment readiness, self-evolution, transfer, safety, or ASI.",
            "- This ledger does not copy private Project Theseus payloads, prompts, tests, solutions, candidate code, traces, score labels, checkpoints, or training rows into this repository.",
            "- This ledger does not promote any chapter core claim above `argument` and does not create a chapter-core upward support-state transition.",
            "- The artifact-retention replay import creates only a bounded non-core support transition; it does not prove deployed residual-ledger storage, deployed artifact-graph behavior, clean live Project Theseus replay, model quality, benchmark performance, safety, alignment, deployment readiness, or ASI.",
            "- The governance-rights receipt suite import creates only a bounded non-core support transition; it does not prove legal rights, institutional governance, moral correctness, reviewer independence, export usability, safe fork execution, deployed governance, clean live Project Theseus replay, safety, alignment, deployment readiness, or ASI.",
            "- The simulation-fidelity receipt suite import creates only a bounded non-core support transition; it does not prove simulator adequacy, physical feasibility, benchmark transfer, native KV parity, deployment, live simulator behavior, model quality, economic outcome, learned generation, clean live Project Theseus replay, safety, alignment, deployment readiness, or ASI.",
            "- The RLDS/Minari trace-export import creates only a bounded non-core support transition; it does not prove RLDS dataset correctness, Minari dataset quality, simulator adequacy, replay success, physical feasibility, benchmark transfer, model quality, economic outcome, clean live Project Theseus replay, deployment readiness, safety, alignment, transfer, or ASI.",
            "- The module definition-of-done import creates only a bounded non-core support transition; it does not prove module capability, deployed Theseus behavior, model quality, benchmark performance, clean live Project Theseus replay, safety, alignment, deployment readiness, or ASI.",
            "- The project-registry import creates only a bounded non-core support transition; it does not prove clean live Project Theseus replay, deployment, model quality, generation speed, self-evolution safety, or any chapter core claim.",
            "- The book-to-Theseus crosswalk import is pointer-only and creates no upward support-state transition; it does not prove clean live Project Theseus replay, deployment, model quality, generation speed, self-evolution safety, artifact truth for referenced rows, or any chapter core claim.",
            "",
            "## Validation Errors",
            "",
            *validation_lines,
            "",
        ]
    )


def write_status_row(row: str) -> None:
    lines = STATUS.read_text(encoding="utf-8").splitlines()
    matches = [index for index, line in enumerate(lines) if line.startswith("| Project Theseus static import lane |")]
    if len(matches) != 1:
        fail([f"{rel(STATUS)} must contain exactly one Project Theseus static import lane row; found {len(matches)}."])
    lines[matches[0]] = row
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fail(errors: list[str]) -> None:
    print("Project Theseus static import status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def validate(args: argparse.Namespace) -> list[str]:
    metrics, errors = collect_metrics()
    if not metrics:
        return errors
    report = build_report(metrics, errors)
    row = compact_status_row(metrics)

    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
    if args.write_status_row:
        write_status_row(row)
    if args.write or args.write_status_row:
        return errors

    if not LEDGER.exists():
        errors.append(f"{rel(LEDGER)} is missing; run with --write.")
    elif LEDGER.read_text(encoding="utf-8") != report:
        errors.append(f"{rel(LEDGER)} is out of date; run with --write.")

    status_text = STATUS.read_text(encoding="utf-8")
    if row not in status_text:
        errors.append(f"{rel(STATUS)} is missing the compact Project Theseus static import row.")
    stale_fragments = (
        "The public-safe Project Theseus import lane now records two sanitized static report fixtures",
        "The public task-bundle import records `theseus_public_task_bundle_import_2026_07_03_local`",
    )
    for stale in stale_fragments:
        if stale in status_text:
            errors.append(f"{rel(STATUS)} still contains stale expanded Project Theseus text: {stale}")
    for line in status_text.splitlines():
        if line.startswith("| Project Theseus static import lane |") and len(line) > 1400:
            errors.append(f"{rel(STATUS)} Project Theseus static import row is still too long: {len(line)} characters.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="rewrite the tracked ledger")
    parser.add_argument("--write-status-row", action="store_true", help="rewrite the compact status row")
    args = parser.parse_args()
    errors = validate(args)
    if errors:
        fail(errors)
    action = "wrote" if args.write or args.write_status_row else "validated"
    metrics, _ = collect_metrics()
    print(
        f"Project Theseus static import status ledger {action}: "
        f"{metrics['static_report_imports']} static imports, "
        f"{metrics['project_registry_imports']} project-registry imports, "
        f"{metrics['public_task_count']} public tasks, "
        f"{metrics['expected_invalid_total']} expected-invalid controls."
    )


if __name__ == "__main__":
    main()
