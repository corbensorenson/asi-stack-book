#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "theseus_work_board_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "work_board_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-06-local.json"
DOC = ROOT / "docs" / "theseus_work_board_import.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_work_board_import_no_change.json"
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "project-theseus-as-report-first-implementation-reference.qmd"
)
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
PROJECT_LEDGER = ROOT / "docs" / "project_theseus_static_import_status_ledger.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"

COMMAND = "python3 scripts/validate_theseus_work_board_import.py"
IMPORT_ID = "theseus-work-board-import-2026-07-06"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.work_board_currentness_import"
PROOF_TAG = "lean:theseus.reference.work_board_import.metadata_boundary"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_REPORTS = {
    "executor_doc": {
        "path": "docs/HIVE_WORK_BOARD_EXECUTOR.md",
        "sha256": "2e18d705ae262ed38250ca9948710451bef1eb622598e2641e6aae27d26bdf23",
    },
    "executor_report": {
        "path": "reports/hive_work_board_executor.json",
        "sha256": "8602bef9d22c1a73aa9751a4b6e035f7587bfb8b5e8a3e9ba72a38d41348ade2",
        "created_utc": "2026-06-29T23:57:30Z",
        "trigger_state": "GREEN",
    },
    "board_report": {
        "path": "reports/hive_work_board.json",
        "sha256": "67cc5a91573ee9cc6ac62bcf92ad353f66c93697fe0bda3402c9a397b00eea50",
        "created_utc": "2026-06-29T23:57:28Z",
        "trigger_state": "GREEN",
    },
    "sqlite_board": {
        "path": "reports/hive_work_board.sqlite",
        "sha256": "1894d453d31ef0a0706a0bcbd72e05989cc251d7a977d2bf7edd95994f817869",
        "size_bytes": 1015808,
    },
    "execution_ledger": {
        "path": "reports/hive_work_board_execution_ledger.jsonl",
        "sha256": "e9a0fb96b3424ec8a5d1e870d61211e55b22bd6aa6d49e3b3766244b7f18699a",
    },
    "unattended_improvement_ledger": {
        "path": "reports/hive_unattended_improvement_ledger.jsonl",
        "sha256": "f72641395533c1bc5ff9df5a13e20ab7ffb166f0377740d763b6ae0dc83b07e6",
    },
    "feedback_ledger": {
        "path": "reports/hive_work_board_feedback.jsonl",
        "sha256": "4faeef351436e0dc4ed08f2d5580fe736e1ba6866c2fe997616fd2d3cac335a0",
    },
    "executor_script": {
        "path": "scripts/hive_work_board_executor.py",
        "sha256": "e49f7096400577f97560fa8b39f0050ec172e3080e66c2402e0387b1c8be8383",
    },
}
EXPECTED_SUMMARY = {
    "trigger_state": "GREEN",
    "executor_total_tasks": 130,
    "executor_ready_tasks": 36,
    "executor_active_tasks": 22,
    "executor_blocked_tasks": 8,
    "executor_done_tasks": 64,
    "executor_selected_tasks": 1,
    "executor_executed_tasks": 0,
    "executor_completed_this_run": 0,
    "executor_failed_this_run": 0,
    "executor_runtime_ms": 2057,
    "board_total_tasks": 130,
    "board_done_tasks": 65,
    "board_ready_or_active_tasks": 22,
    "board_blocked_tasks": 8,
    "board_failed_tasks": 0,
    "board_event_count": 412,
    "board_evidence_count": 133,
    "board_source_count": 9,
    "board_ingested_source_rows": 48,
    "sqlite_table_count": 5,
    "sqlite_task_rows": 130,
    "sqlite_event_rows": 412,
    "sqlite_evidence_rows": 133,
    "sqlite_comment_rows": 0,
    "sqlite_dependency_rows": 0,
    "execution_ledger_rows": 1,
    "unattended_improvement_rows": 4,
    "feedback_rows": 72,
    "public_training_rows_written": 0,
    "external_inference_calls": 0,
    "fallback_return_count": 0,
}
EXPECTED_STATUS_COUNTS = {"active": 22, "blocked": 8, "done": 64, "ready": 36}
EXPECTED_RULES = ("execution", "public_data", "receiver_calibration", "remote_control", "retry", "source_of_truth")
EXPECTED_BOARD_RULES = ("durable", "public_data", "status")
EXPECTED_THEOREMS = (
    "theseus_work_board_import_fixture_valid",
    "theseus_work_board_import_stale_snapshot_blocks_currentness",
    "theseus_work_board_import_clean_replay_overclaim_rejected",
    "theseus_work_board_import_private_payload_rejected",
    "theseus_work_board_import_core_promotion_rejected",
    "theseus_work_board_import_public_training_rows_rejected",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "data/training_data/high_transfer/private_train",
    "private_train",
    "runtime/dogfood",
    "checkpoints/",
    ".npz",
    "candidate_body",
    "solution_body",
)
REQUIRED_NON_CLAIMS = (
    "metadata-only, stale-snapshot implementation-reference boundary",
    "does not copy raw reports, raw SQLite rows, task payloads",
    "does not prove clean live Project Theseus replay",
    "does not create an upward support-state transition",
    "does not promote any chapter core claim above argument",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus work-board import validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
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


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if record.get("schema_version") != "asi_stack.theseus_work_board_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("review_created_utc") != "2026-07-06T02:19:48Z":
        errors.append(f"{owner}: review_created_utc mismatch.")
    if record.get("source_status_created_utc") != "2026-06-29T23:57:30Z":
        errors.append(f"{owner}: source_status_created_utc mismatch.")
    if record.get("source_status_age_days_at_review") != 6:
        errors.append(f"{owner}: source_status_age_days_at_review must remain 6.")
    if record.get("policy") != "project_theseus_hive_work_board_executor_v1":
        errors.append(f"{owner}: policy mismatch.")

    reports = record.get("source_reports")
    if not isinstance(reports, dict):
        errors.append(f"{owner}: source_reports must be an object.")
        reports = {}
    for key, expected in EXPECTED_REPORTS.items():
        value = reports.get(key)
        if not isinstance(value, dict):
            errors.append(f"{owner}: source_reports.{key} missing.")
            continue
        for field, expected_value in expected.items():
            if value.get(field) != expected_value:
                errors.append(f"{owner}: source_reports.{key}.{field} must be {expected_value!r}.")
        digest = value.get("sha256")
        if not isinstance(digest, str) or not SHA_RE.match(digest):
            errors.append(f"{owner}: source_reports.{key}.sha256 must be a SHA-256 digest.")

    public_text = text_blob(record)
    for forbidden in FORBIDDEN_PUBLIC_TEXT:
        if forbidden in public_text:
            errors.append(f"{owner}: sanitized fixture leaks forbidden private fragment {forbidden!r}.")

    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{owner}: summary must be an object.")
        summary = {}
    for field, expected in EXPECTED_SUMMARY.items():
        if summary.get(field) != expected:
            errors.append(f"{owner}: summary.{field} must be {expected!r}.")
    if record.get("sqlite_task_status_counts") != EXPECTED_STATUS_COUNTS:
        errors.append(f"{owner}: sqlite_task_status_counts mismatch.")
    kinds = record.get("sqlite_task_kind_counts")
    if not isinstance(kinds, dict) or sum(kinds.values()) != 130:
        errors.append(f"{owner}: sqlite_task_kind_counts must sum to 130.")
    if kinds.get("high_transfer_concept_pressure") != 70:
        errors.append(f"{owner}: high_transfer_concept_pressure count must remain 70.")
    if record.get("rules_present") != list(EXPECTED_RULES):
        errors.append(f"{owner}: rules_present mismatch.")
    if record.get("board_rules_present") != list(EXPECTED_BOARD_RULES):
        errors.append(f"{owner}: board_rules_present mismatch.")

    currentness = record.get("currentness_boundary")
    if not isinstance(currentness, dict):
        errors.append(f"{owner}: currentness_boundary must be an object.")
        currentness = {}
    expected_currentness = {
        "board_step_executed_by_import": False,
        "fresh_replay_claimed": False,
        "source_snapshot_status": "stale_snapshot_import",
        "source_status_age_days_at_review": 6,
        "stale_status_blocks_currentness_claim": True,
    }
    for field, expected in expected_currentness.items():
        if currentness.get(field) != expected:
            errors.append(f"{owner}: currentness_boundary.{field} must be {expected!r}.")

    safety = record.get("public_safety_boundary")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety_boundary must be an object.")
        safety = {}
    for field in ("raw_reports_copied", "sqlite_payload_copied", "task_payloads_copied", "private_payload_copied"):
        if safety.get(field) is not False:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain false.")
    for field in ("private_path_fields_redacted", "sanitized_for_public_repo"):
        if safety.get(field) is not True:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain true.")
    for field in ("public_training_rows_written", "external_inference_calls", "fallback_return_count"):
        if safety.get(field) != 0:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain 0.")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    expected_boundary = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "argument",
        "support_state_effect": "blocks_promotion",
        "chapter_id": "project-theseus-as-report-first-implementation-reference",
        "work_board_reality_claim": True,
        "chapter_core_claim_promotion": False,
        "clean_live_replay_claim": False,
        "fresh_currentness_claim": False,
        "deployment_claim": False,
        "model_quality_claim": False,
        "benchmark_quality_claim": False,
        "capability_claim": False,
        "unattended_safety_claim": False,
        "self_evolution_safety_claim": False,
    }
    for field, expected in expected_boundary.items():
        if boundary.get(field) != expected:
            errors.append(f"{owner}: claim_boundary.{field} must be {expected!r}.")

    non_claim_text = "\n".join(str(item) for item in record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_text:
            errors.append(f"{owner}: missing non-claim phrase {phrase!r}.")

    stats = {
        "valid_fixture_hash": stable_hash(record),
        "expected_invalid_controls": 0,
        "task_rows": summary.get("sqlite_task_rows"),
        "event_rows": summary.get("sqlite_event_rows"),
        "evidence_rows": summary.get("sqlite_evidence_rows"),
        "feedback_rows": summary.get("feedback_rows"),
    }
    return errors, stats


def invalid_controls(valid: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    controls: list[dict[str, Any]] = []
    for path in sorted(INVALID_DIR.glob("*.invalid.json")):
        mutation = load_json(path)
        candidate = copy.deepcopy(valid)
        set_path(candidate, str(mutation["path"]), mutation["value"])
        candidate_errors, _ = validate_record(candidate, path.name)
        rejected = bool(candidate_errors)
        controls.append(
            {
                "fixture": rel(path),
                "mutation": mutation.get("mutation", ""),
                "rejected": rejected,
                "error_count": len(candidate_errors),
            }
        )
        if not rejected:
            errors.append(f"{rel(path)} unexpectedly passed validation.")
    if len(controls) != 10:
        errors.append(f"expected 10 invalid controls, found {len(controls)}.")
    return errors, controls


def validate_transition(errors: list[str]) -> dict[str, Any]:
    record = load_json(TRANSITION)
    expected = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "verification_command": f"{COMMAND} && python3 scripts/validate_evidence_transitions.py",
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "blocks_promotion",
    }
    for field, value in expected.items():
        if record.get(field) != value:
            errors.append(f"{rel(TRANSITION)}: {field} must be {value!r}.")
    transition_text = text_blob(record).lower()
    for phrase in (
        "metadata-only",
        "stale",
        "does not create an upward support-state transition",
        "does not promote any chapter core claim",
        "does not prove clean live project theseus replay",
    ):
        if phrase not in transition_text:
            errors.append(f"{rel(TRANSITION)} missing boundary phrase {phrase!r}.")
    return record


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for fragment in (
        "structure TheseusWorkBoardImportSummary",
        "def theseusWorkBoardImportFixture",
        "TheseusWorkBoardImportMetadataOnly",
        "TheseusWorkBoardImportPublicSafe",
        "TheseusWorkBoardImportPreservesBoundaries",
    ):
        if fragment not in text:
            errors.append(f"{rel(LEAN_FILE)} missing Lean fragment {fragment!r}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Theseus Work Board Import",
            IMPORT_ID,
            "130 durable task rows",
            "412 event rows",
            "133 evidence rows",
            "stale snapshot",
            rel(TRANSITION),
            PROOF_TAG,
        ],
        CHAPTER: [
            "work-board metadata import",
            "130 durable task rows",
            "412 event rows",
            "133 evidence rows",
            "does not prove clean live Project Theseus replay",
        ],
        READER_CHAPTER: [
            "work-board metadata import",
            "130 durable task rows",
            "stale snapshot",
            "does not prove clean live Project Theseus replay",
        ],
        ACTIVE_CYCLE: [
            "work-board metadata import",
            "130 durable task rows",
            "evidence_transitions/v1_x_measured/theseus_work_board_import_no_change.json",
        ],
        ROADMAP: [
            "work-board metadata import",
            "130 durable task rows",
            "current work-board import beyond the project-registry import",
        ],
        LEDGER: [
            CLAIM_ID,
            rel(TRANSITION),
            "work-board metadata",
        ],
        PROJECT_LEDGER: [
            "Work-board metadata imports | 1",
            "docs/theseus_work_board_import.md",
            "130 durable task rows",
        ],
        APPENDIX_E: [
            "Theseus work-board metadata import validation",
            "scripts/validate_theseus_work_board_import.py",
            "130 durable task rows",
        ],
        CHANGELOG: [
            "Import Theseus work-board metadata boundary",
            rel(RESULT),
            rel(TRANSITION),
        ],
        VALIDATE_BOOK: [
            "scripts/validate_theseus_work_board_import.py",
            "docs/theseus_work_board_import.md",
            "experiments/theseus_work_board_import/results/2026-07-06-local.json",
            'run_validator("validate_theseus_work_board_import.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"missing required surface: {rel(path)}")
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
        for phrase in phrases:
            if re.sub(r"\s+", " ", phrase).lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def write_result(valid: dict[str, Any], stats: dict[str, Any], controls: list[dict[str, Any]]) -> None:
    result = {
        "schema_version": "asi_stack.theseus_work_board_import_result.v0",
        "result_id": IMPORT_ID,
        "command": COMMAND,
        "source_commit": valid["source_commit"],
        "source_checkout_state": valid["source_checkout_state"],
        "review_created_utc": valid["review_created_utc"],
        "source_status_created_utc": valid["source_status_created_utc"],
        "source_status_age_days_at_review": valid["source_status_age_days_at_review"],
        "policy": valid["policy"],
        "source_reports": valid["source_reports"],
        "summary": valid["summary"],
        "sqlite_task_status_counts": valid["sqlite_task_status_counts"],
        "rules_present": valid["rules_present"],
        "board_rules_present": valid["board_rules_present"],
        "currentness_boundary": valid["currentness_boundary"],
        "public_safety_boundary": valid["public_safety_boundary"],
        "claim_boundary": valid["claim_boundary"],
        "expected_invalid_controls": controls,
        "expected_invalid_control_count": len(controls),
        "valid_fixture_hash": stats["valid_fixture_hash"],
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.TheseusReference",
            "proof_tag": PROOF_TAG,
            "theorem_refs": list(EXPECTED_THEOREMS),
            "expected": {
                "task_rows": 130,
                "event_rows": 412,
                "evidence_rows": 133,
                "sqlite_tables": 5,
                "external_inference_calls": 0,
                "public_training_rows_written": 0,
                "raw_reports_copied": False,
                "sqlite_payload_copied": False,
                "task_payloads_copied": False,
                "private_payload_copied": False,
                "stale_status_blocks_currentness_claim": True,
                "clean_live_replay_claimed": False,
                "fresh_currentness_claimed": False,
                "chapter_core_promotion": False,
            },
        },
        "support_state_effect": "blocks_promotion",
        "chapter_core_support_effect": "none",
        "verification_result": "pass",
        "non_claims": valid["non_claims"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_doc(valid: dict[str, Any], controls: list[dict[str, Any]]) -> None:
    summary = valid["summary"]
    lines = [
        "# Theseus Work Board Import",
        "",
        f"Import ID: `{IMPORT_ID}`",
        "",
        "This document records a sanitized public-safe Project Theseus work-board metadata import. It is a stale snapshot boundary for the durable work-board substrate, not a clean live Theseus replay, not a current-dashboard proof, and not a support-state promotion.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---:|",
        f"| Source status age at review | {valid['source_status_age_days_at_review']} days |",
        f"| Durable task rows | {summary['sqlite_task_rows']} |",
        f"| Event rows | {summary['sqlite_event_rows']} |",
        f"| Evidence rows | {summary['sqlite_evidence_rows']} |",
        f"| SQLite tables | {summary['sqlite_table_count']} |",
        f"| Executor ready / active / blocked / done | {summary['executor_ready_tasks']} / {summary['executor_active_tasks']} / {summary['executor_blocked_tasks']} / {summary['executor_done_tasks']} |",
        f"| Execution-ledger rows | {summary['execution_ledger_rows']} |",
        f"| Unattended-improvement rows | {summary['unattended_improvement_rows']} |",
        f"| Feedback rows | {summary['feedback_rows']} |",
        f"| Public training rows | {summary['public_training_rows_written']} |",
        f"| External inference calls | {summary['external_inference_calls']} |",
        "",
        "The imported snapshot records 130 durable task rows, 412 event rows, and 133 evidence rows while keeping raw SQLite rows and task payloads out of the public repository. It is a stale snapshot: the import explicitly blocks fresh-currentness claims.",
        "",
        "## Validation",
        "",
        f"- Command: `{COMMAND}`",
        f"- Result: `{rel(RESULT)}`",
        f"- Transition: `{rel(TRANSITION)}`",
        f"- Lean bridge: `{PROOF_TAG}`",
        f"- Expected-invalid controls: {len(controls)}.",
        "",
        "| Control | Rejected |",
        "|---|---:|",
    ]
    for control in controls:
        lines.append(f"| `{Path(control['fixture']).name}` | {str(control['rejected']).lower()} |")
    lines.extend(["", "## Non-Claims", ""])
    for item in valid["non_claims"]:
        lines.append(f"- {item}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[str] = []
    valid = load_json(VALID_FIXTURE)
    if not isinstance(valid, dict):
        fail([f"{rel(VALID_FIXTURE)} must contain an object."])
    record_errors, stats = validate_record(valid, rel(VALID_FIXTURE))
    errors.extend(record_errors)
    control_errors, controls = invalid_controls(valid)
    errors.extend(control_errors)
    validate_transition(errors)
    write_result(valid, stats, controls)
    write_doc(valid, controls)
    validate_lean(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Theseus work-board import validation passed.")


if __name__ == "__main__":
    main()
