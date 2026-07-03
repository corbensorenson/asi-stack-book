#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURE = ROOT / "experiments" / "theseus_public_task_bundle_import" / "fixtures" / "valid" / "public_task_bundle_import.valid.json"
INVALID_DIR = ROOT / "experiments" / "theseus_public_task_bundle_import" / "fixtures" / "invalid"
RESULT = ROOT / "experiments" / "theseus_public_task_bundle_import" / "results" / "2026-07-03-local.json"
DECISION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_public_task_bundle_import_no_change.json"
DOC = ROOT / "docs" / "theseus_public_task_bundle_import.md"
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
FAST_CHAPTER = ROOT / "chapters" / "fast-generation-architectures.qmd"
FAST_READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "fast-generation-architectures.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
LEAN = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"

COMMAND = "python3 scripts/validate_theseus_public_task_bundle_import.py"
IMPORT_ID = "theseus_public_task_bundle_import_2026_07_03_local"

EXPECTED_REPORTS = {
    "operator_execute",
    "planner",
    "capacity",
    "cli_smoke",
    "benchmark_result",
    "readiness_packet",
    "metadata_case_manifest",
}

EXPECTED_NON_CLAIMS = [
    "Does not prove clean live Project Theseus replay.",
    "Does not prove model quality, benchmark superiority, generation speed, or useful-solution-per-second improvement.",
    "Does not copy public prompts, tests, solutions, traces, scores, or candidate code into this repository.",
    "Does not promote any chapter core claim above argument.",
    "The import result itself records support-state effect none; the separate accepted no-promotion decision blocks promotion without creating an upward support-state transition.",
]

SURFACE_PHRASES = [
    IMPORT_ID,
    "evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json",
    "64 public BigCodeBench metadata-only tasks",
    "0 public training rows",
    "0 task-level regressions",
    "clean live Theseus replay remains unclaimed",
    "does not prove model quality",
]

LEAN_THEOREMS = [
    "theseus_public_task_bundle_import_fixture_public_safe",
    "theseus_public_task_bundle_import_fixture_gates_complete",
    "theseus_public_task_bundle_import_fixture_preserves_no_promotion_boundary",
    "theseus_public_task_bundle_import_clean_replay_overclaim_rejected",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus public task-bundle import validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def set_path(value: dict[str, Any], path: str, new_value: Any) -> None:
    cursor: Any = value
    parts = path.split(".")
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    last = parts[-1]
    if isinstance(cursor, list):
        cursor[int(last)] = new_value
    else:
        cursor[last] = new_value


def require_bool(record: dict[str, Any], owner: str, field: str, expected: bool, errors: list[str]) -> None:
    if record.get(field) is not expected:
        errors.append(f"{owner}: {field} must be {expected}.")


def validate_source_reports(record: dict[str, Any], owner: str, errors: list[str]) -> int:
    reports = record.get("source_reports")
    if not isinstance(reports, list):
        errors.append(f"{owner}: source_reports must be a list.")
        return 0
    ids = {row.get("report_id") for row in reports if isinstance(row, dict)}
    missing = EXPECTED_REPORTS - ids
    if missing:
        errors.append(f"{owner}: source_reports missing {sorted(missing)}.")
    sha_re = re.compile(r"^[0-9a-f]{64}$")
    for row in reports:
        if not isinstance(row, dict):
            errors.append(f"{owner}: source_reports contains a non-object row.")
            continue
        report_id = row.get("report_id", "<missing>")
        if not isinstance(row.get("path"), str) or not row["path"].startswith("reports/"):
            errors.append(f"{owner}: source report {report_id} must use a reports/ relative path.")
        if not isinstance(row.get("sha256"), str) or not sha_re.match(row["sha256"]):
            errors.append(f"{owner}: source report {report_id} must have a 64-hex sha256.")
        if not isinstance(row.get("bytes"), int) or row["bytes"] <= 0:
            errors.append(f"{owner}: source report {report_id} must record positive byte length.")
    return len(reports)


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    expected_scalars = {
        "schema_version": "0.1",
        "record_kind": "theseus_public_task_bundle_import",
        "import_id": IMPORT_ID,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            errors.append(f"{owner}: {key} must be {expected!r}.")

    source = record.get("source_project", {})
    if not isinstance(source, dict):
        errors.append(f"{owner}: source_project must be an object.")
        source = {}
    if source.get("commit") != "1ad88a22b28e9228a67a4779176aeef5c41d2544":
        errors.append(f"{owner}: source_project.commit must pin 1ad88a22b28e9228a67a4779176aeef5c41d2544.")
    if source.get("working_tree_dirty_at_import") is not True:
        errors.append(f"{owner}: working_tree_dirty_at_import must remain true.")
    if source.get("clean_live_replay_claimed") is not False:
        errors.append(f"{owner}: clean live replay must remain false.")
    if source.get("source_reports_imported_as_summary_only") is not True:
        errors.append(f"{owner}: source reports must be imported as summary only.")

    report_count = validate_source_reports(record, owner, errors)

    public_boundary = record.get("public_boundary", {})
    if not isinstance(public_boundary, dict):
        errors.append(f"{owner}: public_boundary must be an object.")
        public_boundary = {}
    expected_boundary = {
        "public_calibration_only": True,
        "case_manifest_metadata_only": True,
        "prompts_exported": False,
        "tests_exported": False,
        "solutions_exported": False,
        "candidate_code_exported": False,
        "traces_exported": False,
        "score_labels_exported": False,
        "public_training_rows_written": 0,
        "external_inference_calls": 0,
    }
    for key, expected in expected_boundary.items():
        if public_boundary.get(key) != expected:
            errors.append(f"{owner}: public_boundary.{key} must be {expected!r}.")

    operator = record.get("operator_execution", {})
    if not isinstance(operator, dict):
        errors.append(f"{owner}: operator_execution must be an object.")
        operator = {}
    for field in ("executed", "command_safe", "output_exists_after", "trace_exists_after", "run_registry_allowed"):
        require_bool(operator, owner, field, True, errors)
    if operator.get("run_returncode") != 0:
        errors.append(f"{owner}: operator_execution.run_returncode must be 0.")
    if operator.get("operator_gate_count") != 12 or operator.get("operator_gates_passed") != 12:
        errors.append(f"{owner}: all 12 operator gates must be passed.")

    bundle = record.get("task_bundle", {})
    if not isinstance(bundle, dict):
        errors.append(f"{owner}: task_bundle must be an object.")
        bundle = {}
    expected_bundle = {
        "run_id": "public_transfer_measurement_partial_diagnostic_seed9_1x64",
        "source_card": "source_bigcodebench",
        "selected_task_count": 64,
        "manifest_row_count": 64,
        "available_after_exclusions": 708,
        "public_training_rows": 0,
        "private_eval_rows": 320,
        "packet_state": "GREEN",
        "selector_state": "GREEN",
    }
    for key, expected in expected_bundle.items():
        if bundle.get(key) != expected:
            errors.append(f"{owner}: task_bundle.{key} must be {expected!r}.")

    result = record.get("benchmark_result", {})
    if not isinstance(result, dict):
        errors.append(f"{owner}: benchmark_result must be an object.")
        result = {}
    expected_result = {
        "public_task_count": 64,
        "case_manifest_selected_count": 64,
        "single_stream_pass_rate": 0.6875,
        "multi_stream_pass_rate": 0.703125,
        "real_public_task_pass_rate": 0.703125,
        "pass_rate_delta": 0.015625,
        "task_level_improvements_over_single_stream": 1,
        "task_level_regressions_vs_single_stream": 0,
        "transfer_artifacts_loaded": 14,
        "student_candidate_count": 512,
        "template_like_candidate_count": 0,
        "loop_closure_candidate_count": 0,
        "deterministic_guardrail_failed_candidate_count": 0,
        "benchmark_gate_count": 18,
        "benchmark_gates_passed": 18,
        "residual_count": 19,
    }
    for key, expected in expected_result.items():
        if result.get(key) != expected:
            errors.append(f"{owner}: benchmark_result.{key} must be {expected!r}.")
    for field in ("case_manifest_enabled", "student_candidate_provenance_valid", "student_candidate_benchmark_integrity_valid", "token_level_code_generation_learned"):
        require_bool(result, owner, field, True, errors)

    quality = record.get("quality_boundary", {})
    if not isinstance(quality, dict):
        errors.append(f"{owner}: quality_boundary must be an object.")
        quality = {}
    for key, expected in {
        "candidate_attempts": 197,
        "raw_test_pass_count": 45,
        "quality_pass_count": 45,
        "quality_blocked_test_pass_count": 0,
        "rank1_quality_pass_count": 45,
        "verification_workers": 8,
        "verification_stage_count": 6,
    }.items():
        if quality.get(key) != expected:
            errors.append(f"{owner}: quality_boundary.{key} must be {expected!r}.")
    if "public calibration pass" not in str(quality.get("score_semantics", "")):
        errors.append(f"{owner}: quality_boundary.score_semantics must preserve public calibration wording.")

    gaps = record.get("artifact_gaps", [])
    if not isinstance(gaps, list) or len(gaps) < 4:
        errors.append(f"{owner}: artifact_gaps must contain at least four visible gaps.")
        gaps = []
    for row in gaps:
        if not isinstance(row, dict):
            errors.append(f"{owner}: artifact_gaps contains a non-object row.")
            continue
        gap = row.get("gap", "<missing>")
        if row.get("visible") is not True or row.get("blocks_support_movement") is not True:
            errors.append(f"{owner}: artifact gap {gap} must stay visible and block support movement.")

    non_claims = record.get("non_claims")
    if non_claims != EXPECTED_NON_CLAIMS:
        errors.append(f"{owner}: non_claims must exactly preserve expected boundaries.")

    metrics = {
        "source_report_count": report_count,
        "artifact_gap_count": len(gaps),
        "public_task_count": int(result.get("public_task_count", 0) or 0),
        "benchmark_gate_count": int(result.get("benchmark_gate_count", 0) or 0),
        "residual_count": int(result.get("residual_count", 0) or 0),
    }
    return errors, metrics


def validate_invalid_fixture(path: Path, base: dict[str, Any], errors: list[str]) -> None:
    spec = load_json(path)
    owner = rel(path)
    if not isinstance(spec, dict):
        errors.append(f"{owner}: expected object.")
        return
    for key in ("case_id", "base_report", "mutation", "expected_error_fragment"):
        if key not in spec:
            errors.append(f"{owner}: missing {key}.")
            return
    if spec["base_report"] != rel(VALID_FIXTURE):
        errors.append(f"{owner}: base_report must be {rel(VALID_FIXTURE)}.")
    mutation = spec.get("mutation", {})
    if not isinstance(mutation, dict) or not isinstance(mutation.get("path"), str) or "value" not in mutation:
        errors.append(f"{owner}: mutation must contain path and value.")
        return
    mutated = copy.deepcopy(base)
    try:
        set_path(mutated, mutation["path"], mutation["value"])
    except (KeyError, IndexError, ValueError):
        errors.append(f"{owner}: mutation path {mutation['path']!r} does not exist.")
        return
    observed, _metrics = validate_record(mutated, owner)
    if not observed:
        errors.append(f"{owner}: expected invalid mutation passed validation.")
        return
    fragment = str(spec["expected_error_fragment"])
    if fragment not in "\n".join(observed):
        errors.append(f"{owner}: expected error fragment {fragment!r}; got {observed}.")


def build_result(record: dict[str, Any], metrics: dict[str, int], invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "result_id": "2026-07-03-theseus-public-task-bundle-import",
        "import_id": IMPORT_ID,
        "validation_result": "pass",
        "valid_fixture_count": 1,
        "expected_invalid_count": invalid_count,
        "valid_fixture_sha256": stable_hash(record),
        **metrics,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "ci_verification_command": COMMAND,
        "artifact_refs": [
            rel(VALID_FIXTURE),
            rel(DOC),
            rel(RESULT),
            "docs/theseus_report_import_slice.md",
            "docs/theseus_generation_mode_import_slice.md",
            "docs/theseus_report_bundle_audit.md",
            "docs/theseus_support_replay_probe.md",
            "lean/AsiStackProofs/TheseusReference.lean",
        ],
        "lean_bridge": {
            "lean_module": "lean/AsiStackProofs/TheseusReference.lean",
            "checked_theorem_names": LEAN_THEOREMS,
        },
        "non_claims": record["non_claims"],
    }


def validate_result(expected: dict[str, Any], errors: list[str]) -> None:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}. Run `{COMMAND} --write-result`.")
        return
    observed = load_json(RESULT)
    if observed != expected:
        errors.append(f"{rel(RESULT)} is out of date. Run `{COMMAND} --write-result`.")


def validate_decision(errors: list[str]) -> None:
    if not DECISION.exists():
        errors.append(f"Missing {rel(DECISION)}.")
        return
    decision = load_json(DECISION)
    if not isinstance(decision, dict):
        errors.append(f"{rel(DECISION)} must contain an object.")
        return
    expected = {
        "transition_id": "v1_x_measured.theseus_public_task_bundle_import.no_change",
        "claim_id": "project-theseus-as-report-first-implementation-reference.public_task_bundle_import_summary",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "support_state_effect": "blocks_promotion",
        "verification_result": "pass",
    }
    for field, expected_value in expected.items():
        if decision.get(field) != expected_value:
            errors.append(f"{rel(DECISION)}: {field} must be {expected_value!r}.")
    for field, phrase in (
        ("artifact_refs", rel(RESULT)),
        ("artifact_refs", rel(VALID_FIXTURE)),
        ("artifact_refs", "scripts/validate_theseus_public_task_bundle_import.py"),
        ("negative_results", "clean live Project Theseus replay remains unclaimed"),
        ("negative_results", "source checkout was dirty at import time"),
        ("downgrade_triggers", "clean-live-replay overclaim accepted"),
        ("acceptance_blockers", "no clean public-safe Theseus replay"),
        ("non_claims", "does not promote the Project Theseus chapter core claim"),
    ):
        if phrase.lower() not in text_blob(decision.get(field, [])).lower():
            errors.append(f"{rel(DECISION)}: {field} missing {phrase!r}.")
    reason = str(decision.get("transition_reason", "")).lower()
    for phrase in ("model quality", "benchmark superiority", "generation speed", "useful-solution-per-second"):
        if phrase not in reason:
            errors.append(f"{rel(DECISION)}: transition_reason missing {phrase!r} boundary.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): DOC,
        rel(CHAPTER): CHAPTER,
        rel(READER): READER,
        rel(FAST_CHAPTER): FAST_CHAPTER,
        rel(FAST_READER): FAST_READER,
        rel(OUTLINE): OUTLINE,
        rel(ROADMAP): ROADMAP,
        rel(ACTIVE_CYCLE): ACTIVE_CYCLE,
    }
    for label, path in surfaces.items():
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        for phrase in SURFACE_PHRASES:
            if phrase not in text:
                errors.append(f"{label} missing phrase {phrase!r}.")
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore")
    for theorem in LEAN_THEOREMS:
        if theorem not in lean_text:
            errors.append(f"{rel(LEAN)} missing theorem {theorem}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Write deterministic result JSON.")
    args = parser.parse_args()

    errors: list[str] = []
    if not VALID_FIXTURE.exists():
        fail([f"Missing {rel(VALID_FIXTURE)}."])
    record = load_json(VALID_FIXTURE)
    if not isinstance(record, dict):
        fail([f"{rel(VALID_FIXTURE)} must contain an object."])
    record_errors, metrics = validate_record(record, rel(VALID_FIXTURE))
    errors.extend(record_errors)

    invalid_fixtures = sorted(INVALID_DIR.glob("*.invalid.json"))
    if len(invalid_fixtures) != 7:
        errors.append(f"{rel(INVALID_DIR)} must contain exactly 7 expected-invalid fixtures.")
    for path in invalid_fixtures:
        validate_invalid_fixture(path, record, errors)

    expected_result = build_result(record, metrics, len(invalid_fixtures))
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(expected_result, indent=2) + "\n", encoding="utf-8")
    else:
        validate_result(expected_result, errors)
    validate_decision(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print(
        "Theseus public task-bundle import validation passed: "
        f"{metrics['public_task_count']} public metadata-only tasks, "
        f"{metrics['benchmark_gate_count']} benchmark gates, "
        f"{metrics['residual_count']} residuals, support-state effect none."
    )


if __name__ == "__main__":
    main()
