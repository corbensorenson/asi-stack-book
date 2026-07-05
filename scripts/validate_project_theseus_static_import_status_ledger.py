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

DOCS = (
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/theseus_public_task_bundle_import.md",
    "docs/theseus_artifact_retention_replay_import.md",
    "docs/theseus_governance_rights_receipt_suite_import.md",
    "docs/theseus_simulation_fidelity_receipt_suite_import.md",
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
        f"{metrics['public_task_count']} metadata-only public tasks, "
        f"{metrics['public_training_rows']} public training rows, "
        f"{metrics['generation_mode_count']} generation modes, "
        f"{metrics['generation_comparison_count']} comparisons, "
        f"{metrics['promotable_comparison_count']} promotable comparisons, "
        f"{metrics['expected_invalid_total']} expected-invalid controls, "
        f"{metrics['no_promotion_decisions']} accepted no-promotion decision, "
        f"{metrics['artifact_upward_transitions']} accepted bounded artifact-retention transition, "
        f"{metrics['governance_rights_upward_transitions']} accepted bounded governance-rights transition, "
        f"and {metrics['simulation_fidelity_upward_transitions']} accepted bounded simulation-fidelity transition; "
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

    metrics = {
        "static_report_imports": 2,
        "support_replay_count": 1,
        "artifact_retention_replay_imports": 1,
        "governance_rights_receipt_imports": 1,
        "simulation_fidelity_receipt_imports": 1,
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
        "expected_invalid_total": arch_result.get("expected_invalid_count", 0)
        + gen_result.get("expected_invalid_count", 0)
        + task_result.get("expected_invalid_count", 0)
        + artifact_result.get("expected_invalid_count", 0)
        + governance_result.get("expected_invalid_count", 0)
        + simulation_result.get("expected_invalid_count", 0),
        "no_promotion_decisions": 1,
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
        f"{metrics['public_task_count']} public tasks, "
        f"{metrics['expected_invalid_total']} expected-invalid controls."
    )


if __name__ == "__main__":
    main()
