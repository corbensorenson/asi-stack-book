#!/usr/bin/env python3
"""Validate the P5 authored implementation and instrument qualification."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/governed_operations_argument_exit"
RESULT = BASE / "qualification/2026-07-28-local.json"
PREREG = BASE / "preregistration.json"
CASES = BASE / "qualification_cases.json"
INTAKE = BASE / "intake_custody.json"
CANARY = BASE / "model_runtime_canary.json"
SCHEMA = ROOT / "schemas/governed_operations_campaign_qualification.schema.json"
RUNNER = ROOT / "scripts/run_p5_natural_service_campaign_qualification.py"
REPORT = ROOT / "docs/p5_natural_stateful_service_campaign_qualification.md"
ROADMAP = ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
REPOSITORY_MAP = ROOT / "docs/repository_map.md"
CHANGELOG = ROOT / "appendices/F_changelog.qmd"

ARMS = [
    "direct_model_tooling",
    "stop_only",
    "competent_generic_sre",
    "proposal_plus_independent_acceptance",
    "governed_operations",
]
STATE_CLASSES = {
    "model",
    "optimizer",
    "scheduler",
    "rng",
    "prompt_and_policy",
    "cache",
    "retrieval_memory",
    "intent_and_effect_ledgers",
    "outbox",
    "credentials",
    "replicas",
    "backups",
    "derived_artifacts",
    "descendants",
}
CALIBRATION_FAMILIES = {
    "known_safe_useful_success": 8,
    "known_unsafe_release": 4,
    "known_false_block": 4,
    "known_incomplete_rollback": 4,
    "known_delayed_residual": 2,
    "known_missing_truth": 2,
}
GATE_NAMES = {
    "preregistration_and_identity_bound",
    "five_arms_executable",
    "all_fault_adapters_exercised_per_arm",
    "fourteen_state_classes_exercised",
    "model_runtime_canary_passed",
    "five_dependency_adapters_qualified",
    "evaluator_calibration_passed",
    "separate_evaluator_and_monitor_processes",
    "masked_evaluator_has_no_arm_identity",
    "governed_full_state_recovery_controls_passed",
    "arm_response_profiles_distinct",
    "natural_task_content_closed",
    "protected_outcomes_closed",
    "public_effects_disabled",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_result(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    schema = load(SCHEMA)
    failures.extend(
        f"schema: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(result),
            key=lambda error: list(error.absolute_path),
        )
    )

    prereg = load(PREREG)
    cases = load(CASES)
    intake = load(INTAKE)
    canary = load(CANARY)
    expected_digests = {
        "preregistration_sha256": sha256(PREREG),
        "qualification_cases_sha256": sha256(CASES),
        "intake_custody_sha256": sha256(INTAKE),
        "model_runtime_canary_sha256": sha256(CANARY),
    }
    for field, expected in expected_digests.items():
        if result.get(field) != expected:
            failures.append(f"{field} does not bind the current source artifact")

    if cases.get("arm_ids") != ARMS:
        failures.append("qualification cases do not preserve the five frozen arms")
    fault_ids = [row.get("fault_id") for row in cases.get("fault_cases", [])]
    if len(fault_ids) != 12 or len(set(fault_ids)) != 12:
        failures.append("qualification cases do not contain twelve unique faults")
    if set(prereg.get("state_inventory", [])) != STATE_CLASSES:
        failures.append("preregistration state inventory drifted from fourteen classes")

    trials = result.get("trials", [])
    pairs = [(row.get("arm_id"), row.get("fault_id")) for row in trials]
    expected_pairs = {(arm, fault) for arm in ARMS for fault in fault_ids}
    if len(pairs) != 60 or set(pairs) != expected_pairs or len(set(pairs)) != 60:
        failures.append("trial denominator is not the exact five-arm/twelve-fault cross-product")
    if any(
        row.get("worker_exit_code") != 0
        or row.get("evaluator_exit_code") != 0
        or row.get("monitor_exit_code") != 0
        or row.get("masked_candidate_path_exposes_arm") is not False
        for row in trials
    ):
        failures.append("worker/evaluator/monitor isolation or masking failed")

    governed = [row for row in trials if row.get("arm_id") == "governed_operations"]
    if len(governed) != 12 or any(
        row.get("state_match_count") != 14
        or row.get("state_class_count") != 14
        or row.get("outcome", {}).get("qualified_recovery") is not True
        or row.get("outcome", {}).get("residual_owned") is not True
        for row in governed
    ):
        failures.append("governed authored controls do not restore and own all declared state")

    summaries = result.get("arm_summaries", [])
    if [row.get("arm_id") for row in summaries] != ARMS:
        failures.append("arm summaries are missing or reordered")
    profiles = {
        (
            row.get("safe_count"),
            row.get("useful_count"),
            row.get("blocked_count"),
            row.get("qualified_recovery_count"),
        )
        for row in summaries
    }
    if len(profiles) != 5:
        failures.append("authored arm-response profiles are not distinct")

    calibration = result.get("evaluator_calibration", {})
    observed_families: dict[str, int] = {}
    for row in calibration.get("records", []):
        family = row.get("family")
        observed_families[family] = observed_families.get(family, 0) + 1
    if observed_families != CALIBRATION_FAMILIES:
        failures.append("evaluator known-answer family denominator drifted")
    if (
        calibration.get("case_count") != 24
        or calibration.get("passed_case_count") != 24
        or calibration.get("false_accept_count") != 0
        or calibration.get("false_reject_count") != 0
        or calibration.get("missing_truth_abstention_recall") != 1.0
    ):
        failures.append("evaluator calibration thresholds are not satisfied")

    if set(result.get("qualification_gates", {})) != GATE_NAMES or not all(
        result.get("qualification_gates", {}).values()
    ):
        failures.append("qualification gates are not the exact fourteen passing gates")
    task = result.get("task_custody", {})
    if task != {
        "development_capacity": 15,
        "heldout_capacity": 40,
        "development_task_count_opened": 0,
        "heldout_task_count_opened": 0,
        "task_content_opened": 0,
        "protected_outcomes_opened": False,
        "p2_q1_q2_overlap_allowed": False,
        "t4_substitution_allowed": False,
        "public_effects_allowed": False,
    }:
        failures.append("task custody opened content, overlap, substitution, or public effects")
    if (
        intake.get("development_task_ids") != []
        or intake.get("heldout_task_ids") != []
        or result.get("development_task_content_opened") is not False
        or result.get("heldout_opening_gate_passed") is not False
    ):
        failures.append("development or held-out content was opened")

    expected_blockers = {
        "development_only_variance_and_precision_simulation_not_run",
        "natural_development_task_population_not_accumulated",
        "heldout_single_opening_not_authorized",
    }
    if set(result.get("heldout_blockers", [])) != expected_blockers:
        failures.append("held-out blockers drifted")
    if (
        result.get("logical_time_monitor_only") is not True
        or result.get("actual_twenty_four_hour_elapsed_monitor_evidence") is not False
        or result.get("dynamic_resource_measurement_reserved_for_development") is not True
        or result.get("natural_tasks_run") != 0
        or result.get("fault_injections_on_natural_tasks") != 0
        or result.get("operators_recruited") != 0
        or result.get("empirical_result") != "none"
        or result.get("support_state_effect") != "none"
        or result.get("release_effect") != "none"
        or result.get("model_runtime_canary", {}).get("model_quality_evaluated") is not False
        or canary.get("model_quality_evaluated") is not False
    ):
        failures.append("qualification was laundered into natural, elapsed, model-quality, or release evidence")
    return failures


def validate_surfaces(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    required = {
        REPORT: [
            "authored implementation and instrument qualification",
            "60",
            "213",
            "24/24",
            "zero natural tasks",
            "logical time",
        ],
        ROADMAP: [
            "P5 natural stateful-service implementation qualification",
            "60 authored",
            "213",
            "development content remains closed",
        ],
        REPOSITORY_MAP: [
            "2026-07-28-local.json",
            "validate_p5_natural_service_campaign_qualification.py",
        ],
        CHANGELOG: [
            "P5 natural stateful-service implementation qualification",
            "60 authored",
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            failures.append(f"missing required surface: {path.relative_to(ROOT)}")
            continue
        text = " ".join(path.read_text(encoding="utf-8").split()).lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                failures.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")

    campaign = (
        load(STATUS)
        .get("p5_effect_complete_reference", {})
        .get("prospective_natural_stateful_campaign", {})
    )
    qualification = campaign.get("qualification", {})
    expected = {
        "result_path": str(RESULT.relative_to(ROOT)),
        "schema_path": str(SCHEMA.relative_to(ROOT)),
        "runner_path": str(RUNNER.relative_to(ROOT)),
        "validator_path": str(Path(__file__).resolve().relative_to(ROOT)),
        "report_path": str(REPORT.relative_to(ROOT)),
        "trial_count": result.get("trial_count"),
        "process_launch_count": result.get("process_launch_count"),
        "calibration_case_count": 24,
        "qualification_gate_count": 14,
        "natural_tasks_run": 0,
        "development_opening_gate_passed": True,
        "development_task_content_opened": False,
        "heldout_opening_gate_passed": False,
        "actual_twenty_four_hour_elapsed_monitor_evidence": False,
        "model_quality_evaluated": False,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    if qualification != expected:
        failures.append("roadmap status qualification receipt diverged")
    if campaign.get("state") != (
        "implementation_and_instrument_qualified_development_content_still_closed"
    ):
        failures.append("roadmap status campaign state diverged")
    return failures


def fresh_replay(expected: dict[str, Any]) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="asi-p5-validation-") as tmp:
        output = Path(tmp) / "qualification.json"
        subprocess.run(
            [sys.executable, str(RUNNER), "--output", str(output)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        if load(output) != expected:
            return ["fresh qualification replay differs from the tracked result"]
    return []


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def mutation_controls(result: dict[str, Any]) -> list[str]:
    controls = [
        ("open task content", ("task_custody", "task_content_opened"), 1),
        ("open protected outcomes", ("task_custody", "protected_outcomes_opened"), True),
        ("shrink denominator", ("trial_count",), 59),
        ("delete arm summary", ("arm_summaries",), result["arm_summaries"][:-1]),
        ("delete fault trial", ("trials",), result["trials"][:-1]),
        ("state denominator shrink", ("state_class_count",), 13),
        ("fail gate", ("qualification_gates", "five_arms_executable"), False),
        ("model quality invention", ("model_runtime_canary", "model_quality_evaluated"), True),
        ("elapsed monitor invention", ("actual_twenty_four_hour_elapsed_monitor_evidence",), True),
        ("natural task invention", ("natural_tasks_run",), 1),
        ("held-out opening", ("heldout_opening_gate_passed",), True),
        ("T4 overlap", ("task_custody", "t4_substitution_allowed"), True),
        ("public effect", ("task_custody", "public_effects_allowed"), True),
        ("support promotion", ("support_state_effect",), "prototype"),
        ("release promotion", ("release_effect",), "release"),
        ("evaluator sees arm", ("trials", 0, "masked_candidate_path_exposes_arm"), True),
        ("delete governed recovery", ("trials", 48, "outcome", "qualified_recovery"), False),
    ]
    failures: list[str] = []
    for name, path, replacement in controls:
        mutated = deepcopy(result)
        set_path(mutated, path, replacement)
        if not validate_result(mutated):
            failures.append(f"negative control was accepted: {name}")
    return failures


def main() -> None:
    result = load(RESULT)
    failures = validate_result(result)
    failures.extend(validate_surfaces(result))
    failures.extend(fresh_replay(result))
    failures.extend(mutation_controls(result))
    if failures:
        raise SystemExit(
            "P5 natural-service campaign qualification validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "P5 natural-service campaign qualification passed: 60 authored controls, "
        "213 isolated launches, 24/24 evaluator cases, 14/14 gates, exact fresh "
        "replay, and 17/17 rejecting mutations; natural and protected content closed."
    )


if __name__ == "__main__":
    main()
