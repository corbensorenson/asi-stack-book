#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "theseus_generation_mode_import.schema.json"
VALID_DIR = ROOT / "experiments" / "theseus_generation_mode_import" / "fixtures" / "valid"
INVALID_DIR = ROOT / "experiments" / "theseus_generation_mode_import" / "fixtures" / "invalid"
RESULT = ROOT / "experiments" / "theseus_generation_mode_import" / "results" / "2026-07-01-local.json"
SUMMARY = ROOT / "docs" / "theseus_generation_mode_import_slice.md"

EXPECTED_REPORT_ID = "theseus.generation_mode_gate.20260701.public_static_import"
EXPECTED_SOURCE_SHA256 = "a711d0dbca9779f26d4b0a63db18ce1fc574ade47a262f5140a9a7b6d325e90b"
EXPECTED_CONFIG_SHA256 = "eebf96a7cf0a6c30c9203d2f11377c953973694a34dec8f095c8b76e378114c7"
EXPECTED_TOOL_SHA256 = "e99477a1b9546c14c60dc8e2b442f1437274d7ba367e717c23b608fb41fd290b"
EXPECTED_BOUNDARY_GATES = {
    "public_benchmark_training_forbidden",
    "runtime_external_inference_forbidden",
    "fallback_template_router_tool_credit_forbidden",
    "raw_throughput_only_promotion_forbidden",
    "mixed_metric_overclaim_forbidden",
}
EXPECTED_COMPARISONS = {
    "broad8_no_plan_vs_semantic_head_v1",
    "broad4_plan_aux_no_head_vs_semantic_head_v1",
    "broad4_plan_aux_head_vs_body_semantics_v1",
    "broad4_body_semantics_vs_plan_semantic_slots_v1",
    "broad4_plan_semantic_slots_vs_update_contract_v1",
    "broad4_update_contract_vs_plan_subspace_v1",
    "broad4_plan_subspace_vs_body_action_v1",
    "broad4_plan_subspace_vs_algorithmic_replay_v1",
    "broad4_algorithmic_replay_vs_escape_replay_v1",
    "broad4_escape_replay_vs_statement_slots_v1",
    "broad4_statement_slots_vs_action_trace_pairwise_v1",
    "broad4_action_trace_pairwise_vs_source_slot_head_v1",
    "broad4_source_slot_head_vs_expression_vocab_guard_v1",
}
REQUIRED_CHAPTERS = {
    "fast-generation-architectures",
    "resource-economics-and-token-budgets",
    "project-theseus-as-report-first-implementation-reference",
}
REQUIRED_NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not prove generation speed",
    "does not authorize heavy training",
    "does not copy private task rows",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Project Theseus generation-mode import validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def set_path(value: dict[str, Any], path: str, new_value: Any) -> None:
    cursor: Any = value
    parts = path.split(".")
    for part in parts[:-1]:
        if isinstance(cursor, list):
            cursor = cursor[int(part)]
        elif isinstance(cursor, dict) and part in cursor:
            cursor = cursor[part]
        else:
            raise KeyError(path)
    final = parts[-1]
    if isinstance(cursor, list):
        cursor[int(final)] = new_value
    elif isinstance(cursor, dict):
        cursor[final] = new_value
    else:
        raise KeyError(path)


def validate_non_claims(owner: str, non_claims: Any, errors: list[str]) -> None:
    if not isinstance(non_claims, list) or not non_claims:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    blob = text_blob(non_claims)
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing boundary phrase {phrase!r}.")


def artifact_digest(report: dict[str, Any], role: str) -> str:
    for artifact in report.get("source_artifacts", []):
        if isinstance(artifact, dict) and artifact.get("artifact_role") == role:
            return str(artifact.get("source_artifact_sha256") or "")
    return ""


def validate_report(report: dict[str, Any], schema: dict[str, Any], owner: str) -> list[str]:
    errors = validate_value(report, schema, owner)
    if errors:
        return errors

    if report.get("report_id") != EXPECTED_REPORT_ID:
        errors.append(f"{owner}: report_id must be {EXPECTED_REPORT_ID}.")
    if report.get("trace_class") != "generation_mode_gate":
        errors.append(f"{owner}: trace_class must be generation_mode_gate.")

    source_project = report.get("source_project", {})
    if source_project.get("git_commit") != "1ad88a22":
        errors.append(f"{owner}: source_project.git_commit must be 1ad88a22.")
    if source_project.get("worktree_state") != "dirty_at_import_review":
        errors.append(f"{owner}: worktree_state must record dirty_at_import_review.")

    if artifact_digest(report, "report") != EXPECTED_SOURCE_SHA256:
        errors.append(f"{owner}: generation-mode report digest mismatch.")
    if artifact_digest(report, "config") != EXPECTED_CONFIG_SHA256:
        errors.append(f"{owner}: generation-mode config digest mismatch.")
    if artifact_digest(report, "tool") != EXPECTED_TOOL_SHA256:
        errors.append(f"{owner}: generation-mode tool digest mismatch.")

    public_safety = report.get("public_safety", {})
    if public_safety.get("redaction_state") != "public_safe_static_summary":
        errors.append(f"{owner}: redaction state must be public_safe_static_summary.")
    if public_safety.get("private_payload_copied") is not False:
        errors.append(f"{owner}: private payload copied.")
    redactions = public_safety.get("redactions", [])
    if not isinstance(redactions, list) or len(redactions) < 5:
        errors.append(f"{owner}: redactions must name at least five excluded private surfaces.")

    summary = report.get("gate_summary", {})
    expected_summary = {
        "policy": "project_theseus_generation_mode_gate_v1",
        "trigger_state": "YELLOW",
        "mode_count": 18,
        "comparison_count": 13,
        "hard_gap_count": 0,
        "warning_count": 13,
        "promotable_comparison_count": 0,
        "modes_with_task_pass_evidence": 0,
        "modes_with_missing_report_refs": 0,
        "modes_with_fallback_burden": 0,
        "mean_accepted_span_per_second": 0.209103,
        "mean_useful_solution_per_second": 0.0,
        "boundary_gate_count": 5,
        "boundary_gates_passed": 5,
        "warnings_with_accepted_speed_lift": 5,
        "warnings_with_zero_candidate_task_pass": 13,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"{owner}: gate_summary.{key} must be {expected!r}.")
    if summary.get("mean_useful_solution_per_second") != 0.0:
        errors.append(f"{owner}: mean useful solution per second must remain zero.")

    gates = report.get("boundary_gates", [])
    if not isinstance(gates, list) or len(gates) != len(EXPECTED_BOUNDARY_GATES):
        errors.append(f"{owner}: boundary_gates must contain exactly {len(EXPECTED_BOUNDARY_GATES)} gates.")
        gates = []
    observed_gates = {row.get("id") for row in gates if isinstance(row, dict)}
    if observed_gates != EXPECTED_BOUNDARY_GATES:
        errors.append(f"{owner}: boundary gate set does not match expected generation-mode gates.")
    for row in gates:
        if not isinstance(row, dict):
            continue
        if row.get("passed") is not True or row.get("severity") != "hard":
            errors.append(f"{owner}: all imported boundary gates must be passing hard gates.")

    comparisons = report.get("negative_comparisons", [])
    if not isinstance(comparisons, list) or len(comparisons) != len(EXPECTED_COMPARISONS):
        errors.append(f"{owner}: negative_comparisons must contain exactly {len(EXPECTED_COMPARISONS)} rows.")
        comparisons = []
    observed_comparisons = {row.get("id") for row in comparisons if isinstance(row, dict)}
    if observed_comparisons != EXPECTED_COMPARISONS:
        errors.append(f"{owner}: comparison set does not match expected generation-mode comparisons.")
    accepted_speed_lifts = 0
    for row in comparisons:
        if not isinstance(row, dict):
            continue
        if row.get("promotable") is not False:
            errors.append(f"{owner}: all imported comparisons must remain non-promotable.")
        if row.get("useful_speed_lift") is not False:
            errors.append(f"{owner}: useful speed lift must remain false for imported comparisons.")
        if row.get("candidate_task_pass_count") != 0:
            errors.append(f"{owner}: candidate task pass count must remain zero for imported comparisons.")
        if "not_promotable" not in str(row.get("promotion_decision") or ""):
            errors.append(f"{owner}: promotion decisions must preserve not_promotable boundary.")
        if row.get("accepted_speed_lift") is True:
            accepted_speed_lifts += 1
    if accepted_speed_lifts != 5:
        errors.append(f"{owner}: exactly five warning comparisons must show accepted-span speed lift.")

    rules = text_blob(report.get("rules", {}))
    for phrase in (
        "accepted spans per second",
        "useful verified solutions per second",
        "not promotable",
        "does not bypass candidate-integrity",
    ):
        if phrase not in rules:
            errors.append(f"{owner}: rules missing phrase {phrase!r}.")

    failed_attempt_text = text_blob(report.get("failed_attempts", []))
    if "live_theseus_generation_mode_rerun_blocked_dirty_checkout" not in failed_attempt_text:
        errors.append(f"{owner}: failed_attempts must record the blocked dirty-checkout generation-mode rerun.")

    replay = report.get("replay", {})
    if replay.get("mode") != "digest_verification" or replay.get("ci_verifiable") is not True:
        errors.append(f"{owner}: replay must be CI-verifiable digest_verification.")
    if replay.get("command") != "python3 scripts/validate_theseus_generation_mode_import.py":
        errors.append(f"{owner}: replay.command must name this validator.")
    if replay.get("expected_source_artifact_sha256") != EXPECTED_SOURCE_SHA256:
        errors.append(f"{owner}: replay source artifact digest mismatch.")

    connected = set(report.get("connected_chapter_ids", []))
    if not REQUIRED_CHAPTERS.issubset(connected):
        errors.append(f"{owner}: connected_chapter_ids missing {sorted(REQUIRED_CHAPTERS - connected)}.")
    if report.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append(f"{owner}: support state effect must remain no_chapter_core_claim_promotion.")

    boundaries = text_blob(report.get("claim_boundaries", []))
    for phrase in (
        "18 modes, 13 comparisons",
        "negative evidence against raw-throughput promotion",
        "cannot by itself promote",
        "accepted evidence-transition record",
    ):
        if phrase not in boundaries:
            errors.append(f"{owner}: claim_boundaries missing phrase {phrase!r}.")
    validate_non_claims(owner, report.get("non_claims"), errors)
    return errors


def validate_invalid_fixture(path: Path, schema: dict[str, Any], errors: list[str]) -> None:
    spec = load_json(path)
    owner = rel(path)
    if not isinstance(spec, dict):
        errors.append(f"{owner}: expected object.")
        return
    for key in ("case_id", "base_report", "mutation", "expected_error_fragment"):
        if key not in spec:
            errors.append(f"{owner}: missing {key}.")
            return
    base_path = ROOT / str(spec["base_report"])
    if not base_path.exists():
        errors.append(f"{owner}: base_report does not exist.")
        return
    report = load_json(base_path)
    if not isinstance(report, dict):
        errors.append(f"{owner}: base_report must contain object.")
        return
    mutation = spec["mutation"]
    if not isinstance(mutation, dict) or not isinstance(mutation.get("path"), str) or "value" not in mutation:
        errors.append(f"{owner}: mutation must contain path and value.")
        return
    mutated = copy.deepcopy(report)
    try:
        set_path(mutated, mutation["path"], mutation["value"])
    except (KeyError, IndexError, ValueError):
        errors.append(f"{owner}: mutation path {mutation['path']!r} does not exist.")
        return
    observed_errors = validate_report(mutated, schema, owner)
    if not observed_errors:
        errors.append(f"{owner}: expected invalid mutation passed validation.")
        return
    expected_fragment = str(spec["expected_error_fragment"])
    if expected_fragment not in "\n".join(observed_errors):
        errors.append(f"{owner}: expected error fragment {expected_fragment!r}; got {observed_errors}.")


def validate_result(expected: dict[str, Any], errors: list[str]) -> None:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}.")
        return
    result = load_json(RESULT)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain an object.")
        return
    for key, expected_value in expected.items():
        if result.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    validate_non_claims(rel(RESULT), result.get("non_claims"), errors)


def validate_summary(expected_digest: str, errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required = (
        "Project Theseus Generation Mode Import Slice",
        EXPECTED_REPORT_ID,
        EXPECTED_SOURCE_SHA256,
        expected_digest,
        "18 modes",
        "13 comparisons",
        "zero promotable comparisons",
        "live_theseus_generation_mode_rerun_blocked_dirty_checkout",
        "Does not promote any chapter core claim above `argument`.",
        "Does not prove generation speed",
        "python3 scripts/validate_theseus_generation_mode_import.py",
    )
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def main() -> None:
    schema = load_json(SCHEMA)
    valid_paths = sorted(VALID_DIR.glob("*.valid.json"))
    invalid_paths = sorted(INVALID_DIR.glob("*.invalid.json"))
    errors: list[str] = []

    if len(valid_paths) != 1:
        errors.append(f"{rel(VALID_DIR)} must contain exactly one valid report fixture.")
    if len(invalid_paths) != 4:
        errors.append(f"{rel(INVALID_DIR)} must contain exactly four expected-invalid mutation fixtures.")

    report_digest = ""
    for path in valid_paths:
        value = load_json(path)
        if not isinstance(value, dict):
            errors.append(f"{rel(path)} must contain an object.")
            continue
        report_errors = validate_report(value, schema, rel(path))
        errors.extend(report_errors)
        if not report_errors:
            report_digest = stable_hash(value)

    for path in invalid_paths:
        validate_invalid_fixture(path, schema, errors)

    if report_digest:
        expected_result = {
            "schema_version": "0.1",
            "result_id": "2026-07-01-theseus-generation-mode-public-import",
            "slice_id": "theseus_generation_mode_import",
            "validation_result": "pass",
            "accepted_report_id": EXPECTED_REPORT_ID,
            "accepted_public_report_sha256": report_digest,
            "source_artifact_sha256": EXPECTED_SOURCE_SHA256,
            "valid_report_count": len(valid_paths),
            "expected_invalid_count": len(invalid_paths),
            "accepted_mode_count": 18,
            "accepted_comparison_count": 13,
            "accepted_hard_gap_count": 0,
            "accepted_promotable_comparison_count": 0,
            "accepted_useful_solution_per_second": 0.0,
            "warnings_with_accepted_speed_lift": 5,
            "support_state_effect": "no_chapter_core_claim_promotion",
            "ci_verification_command": "python3 scripts/validate_theseus_generation_mode_import.py",
        }
        validate_result(expected_result, errors)
        validate_summary(report_digest, errors)

    if errors:
        fail(errors)

    print(
        "Project Theseus generation-mode import validation passed: "
        f"{len(valid_paths)} valid report, {len(invalid_paths)} expected-invalid controls, "
        f"digest {report_digest}."
    )


if __name__ == "__main__":
    main()
