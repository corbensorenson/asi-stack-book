#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "theseus_rlds_minari_trace_export_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "rlds_minari_trace_export_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-05-local.json"
DOC = ROOT / "docs" / "theseus_rlds_minari_trace_export_import.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_rlds_minari_trace_export_import_prototype_backed.json"
)
CHAPTER = ROOT / "chapters" / "resource-economics-and-token-budgets.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "resource-economics-and-token-budgets.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "SimulationFidelity.lean"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
NON_CORE = ROOT / "docs" / "non_core_evidence_ledger.md"
PROJECT_THESEUS_LEDGER = ROOT / "docs" / "project_theseus_static_import_status_ledger.md"
TEST_LEDGER = ROOT / "docs" / "test_harness_status_ledger.md"

COMMAND = "python3 scripts/validate_theseus_rlds_minari_trace_export_import.py"
IMPORT_ID = "theseus-rlds-minari-trace-export-import-2026-07-05"
CLAIM_ID = "resource-economics.theseus_rlds_minari_trace_export_import"
PROOF_TAG = "lean:resource.simulation_fidelity.theseus_rlds_minari_trace_export.fixture_bridge"
EXPECTED_SOURCE_SHA = "989b413f887d76e29bb0b57f0656e670c2e6bb9657603aa7f5545b26f5936ccc"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_POLICY = "trainer_rlds_minari_trace_export_v0"
EXPECTED_CREATED = "2026-06-18T21:58:35.101322+00:00"
EXPECTED_EXPORT_ID = "rlds_8e527a30014ee580"
EXPECTED_SOURCE_POINTER = "reports/pressure_source_gym_pybullet_drones_seed1.json"
EXPECTED_FORMATS = ["theseus_episode_jsonl", "rlds_manifest", "minari_manifest"]
EXPECTED_FIELDS = ["observation_ref", "action", "reward", "done", "truncated", "info", "seed"]
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "private_train/",
    "data/training_data/high_transfer",
    "checkpoints/",
    ".npz",
    "personality-documents",
)
REQUIRED_NON_CLAIMS = (
    "does not copy the raw Project Theseus report, episode payload, private traces, checkpoints, prompts, tests, solutions, score labels, or training rows into this public repository",
    "does not prove RLDS dataset correctness, Minari dataset quality, simulator adequacy, replay success, physical feasibility, benchmark transfer, model quality, economic outcome, clean live Project Theseus replay, deployment readiness, safety, alignment, transfer, or ASI",
    "does not promote any chapter core claim above argument",
)
LEAN_THEOREMS = (
    "theseus_rlds_minari_trace_export_import_fixture_valid",
    "theseus_rlds_minari_trace_export_import_core_promotion_rejected",
    "theseus_rlds_minari_trace_export_import_dataset_quality_overclaim_rejected",
    "theseus_rlds_minari_trace_export_import_replay_success_overclaim_rejected",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus RLDS/Minari trace export import validation failed:")
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


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if record.get("schema_version") != "asi_stack.theseus_rlds_minari_trace_export_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_report_sha256") != EXPECTED_SOURCE_SHA:
        errors.append(f"{owner}: source_report_sha256 mismatch.")
    if not isinstance(record.get("source_report_sha256"), str) or not SHA_RE.match(record["source_report_sha256"]):
        errors.append(f"{owner}: source_report_sha256 must be a SHA-256 hex digest.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("source_report_path") != "reports/rlds_minari_trace_export.json":
        errors.append(f"{owner}: source_report_path mismatch.")
    if record.get("source_policy") != EXPECTED_POLICY:
        errors.append(f"{owner}: source_policy mismatch.")
    if record.get("source_created_utc") != EXPECTED_CREATED:
        errors.append(f"{owner}: source_created_utc mismatch.")
    if record.get("source_status") != "READY":
        errors.append(f"{owner}: source_status must be READY.")
    for field in ("raw_report_copied", "episode_payload_copied", "private_payload_copied"):
        if record.get(field) is not False:
            errors.append(f"{owner}: {field} must remain false.")
    for field in ("private_path_fields_redacted", "sanitized_for_public_repo"):
        if record.get(field) is not True:
            errors.append(f"{owner}: {field} must remain true.")

    public_text = text_blob(record)
    for forbidden in FORBIDDEN_PUBLIC_TEXT:
        if forbidden in public_text:
            errors.append(f"{owner}: sanitized fixture leaks forbidden private fragment {forbidden!r}.")

    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{owner}: summary must be an object.")
        summary = {}
    expected_summary = {
        "export_count": 1,
        "ready_count": 1,
        "manifest_count": 1,
        "ready_manifest_count": 1,
        "required_format_count": 3,
        "required_field_count": 7,
        "expected_invalid_control_count": 7,
    }
    for field, expected in expected_summary.items():
        if summary.get(field) != expected:
            errors.append(f"{owner}: summary.{field} must be {expected}.")

    export_manifest = record.get("export_manifest")
    if not isinstance(export_manifest, dict):
        errors.append(f"{owner}: export_manifest must be an object.")
        export_manifest = {}
    if export_manifest.get("episode_source_report") != EXPECTED_SOURCE_POINTER:
        errors.append(f"{owner}: export manifest source pointer mismatch.")
    if export_manifest.get("export_id") != EXPECTED_EXPORT_ID:
        errors.append(f"{owner}: export_id mismatch.")
    if export_manifest.get("formats") != EXPECTED_FORMATS:
        errors.append(f"{owner}: formats must preserve {EXPECTED_FORMATS!r}.")
    if export_manifest.get("fields") != EXPECTED_FIELDS:
        errors.append(f"{owner}: fields must preserve {EXPECTED_FIELDS!r}.")
    if export_manifest.get("license_metadata_required") is not True:
        errors.append(f"{owner}: license_metadata_required must remain true.")
    if export_manifest.get("replay_smoke_required") is not True:
        errors.append(f"{owner}: replay_smoke_required must remain true.")
    if export_manifest.get("ready") is not True:
        errors.append(f"{owner}: export manifest must remain ready.")

    safety = record.get("public_safety_boundary")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety_boundary must be an object.")
        safety = {}
    for field in ("public_training_rows_written", "external_inference_calls", "fallback_return_count"):
        if safety.get(field) != 0:
            errors.append(f"{owner}: public_safety_boundary.{field} must be 0.")
    for field in ("raw_episode_payload_copied", "training_rows_published"):
        if safety.get(field) is not False:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain false.")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    for field in (
        "chapter_core_promotion_claimed",
        "rlds_dataset_correctness_claimed",
        "minari_dataset_quality_claimed",
        "simulator_adequacy_claimed",
        "replay_success_claimed",
        "training_data_publication_claimed",
        "physical_feasibility_claimed",
        "benchmark_transfer_claimed",
        "deployment_claimed",
        "model_quality_claimed",
        "economic_outcome_claimed",
        "clean_live_theseus_replay_claimed",
        "safety_claimed",
        "asi_claimed",
    ):
        if boundary.get(field) is not False:
            errors.append(f"{owner}: claim_boundary.{field} must remain false.")

    if record.get("support_state_effect") != "bounded_non_core_transition_only":
        errors.append(f"{owner}: support_state_effect mismatch.")
    if record.get("chapter_core_support_effect") != "none":
        errors.append(f"{owner}: chapter_core_support_effect must remain none.")

    non_claims = record.get("non_claims")
    if not isinstance(non_claims, list):
        errors.append(f"{owner}: non_claims must be a list.")
        non_claims = []
    non_claim_text = "\n".join(str(item) for item in non_claims)
    for required in REQUIRED_NON_CLAIMS:
        if required not in non_claim_text:
            errors.append(f"{owner}: missing non-claim {required!r}.")

    result_summary = {
        "source_report_sha256": record.get("source_report_sha256"),
        "source_commit": record.get("source_commit"),
        "source_checkout_state": record.get("source_checkout_state"),
        "source_policy": record.get("source_policy"),
        "source_status": record.get("source_status"),
        "export_count": summary.get("export_count"),
        "ready_count": summary.get("ready_count"),
        "manifest_count": summary.get("manifest_count"),
        "ready_manifest_count": summary.get("ready_manifest_count"),
        "format_count": len(export_manifest.get("formats", [])) if isinstance(export_manifest.get("formats"), list) else 0,
        "field_count": len(export_manifest.get("fields", [])) if isinstance(export_manifest.get("fields"), list) else 0,
        "license_metadata_required": export_manifest.get("license_metadata_required"),
        "replay_smoke_required": export_manifest.get("replay_smoke_required"),
        "expected_invalid_control_count": summary.get("expected_invalid_control_count"),
        "fixture_sha256": stable_hash(record),
    }
    return errors, result_summary


def expected_result(record: dict[str, Any], invalid_count: int) -> dict[str, Any]:
    record_errors, summary = validate_record(record, rel(VALID_FIXTURE))
    if record_errors:
        fail(record_errors)
    safety = record["public_safety_boundary"]
    return {
        "schema_version": "asi_stack.theseus_rlds_minari_trace_export_import.result.v0",
        "import_id": IMPORT_ID,
        "claim_id": CLAIM_ID,
        "validation_result": "pass",
        **summary,
        "expected_invalid_control_count": invalid_count,
        "new_support_state": "prototype-backed",
        "support_state_effect": "bounded_non_core_transition_only",
        "chapter_core_support_effect": "none",
        "public_safety": {
            "public_training_rows_written": safety["public_training_rows_written"],
            "external_inference_calls": safety["external_inference_calls"],
            "fallback_return_count": safety["fallback_return_count"],
            "raw_episode_payload_copied": safety["raw_episode_payload_copied"],
            "training_rows_published": safety["training_rows_published"],
        },
        "non_claims": record["non_claims"],
    }


def validate_invalid_controls(errors: list[str]) -> int:
    invalid_paths = sorted(INVALID_DIR.glob("*.invalid.json"))
    if len(invalid_paths) != 7:
        errors.append(f"{rel(INVALID_DIR)} must contain seven expected-invalid controls.")
    rejected = 0
    for path in invalid_paths:
        value = load_json(path)
        if not isinstance(value, dict):
            errors.append(f"{rel(path)} must contain an object.")
            continue
        control_errors, _ = validate_record(value, rel(path))
        if control_errors:
            rejected += 1
        else:
            errors.append(f"{rel(path)} unexpectedly validated.")
    return rejected


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing transition record {rel(TRANSITION)}.")
        return
    transition = load_json(TRANSITION)
    expected = {
        "transition_id": "v1_x_measured.theseus_rlds_minari_trace_export_import.prototype_backed",
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "verification_result": "pass",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for field, value in expected.items():
        if transition.get(field) != value:
            errors.append(f"{rel(TRANSITION)} field {field} must be {value!r}.")
    if transition.get("acceptance_blockers"):
        errors.append(f"{rel(TRANSITION)} accepted upward transition must not list acceptance blockers.")
    non_claims = "\n".join(str(item) for item in transition.get("non_claims", []))
    for required in REQUIRED_NON_CLAIMS:
        if required not in non_claims:
            errors.append(f"{rel(TRANSITION)} missing non-claim {required!r}.")
    required_refs = [
        rel(DOC),
        rel(VALID_FIXTURE),
        rel(RESULT),
        "scripts/validate_theseus_rlds_minari_trace_export_import.py",
        "lean/AsiStackProofs/SimulationFidelity.lean",
    ]
    joined = text_blob(transition)
    for ref in required_refs:
        if ref not in joined:
            errors.append(f"{rel(TRANSITION)} missing artifact/reference {ref}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in LEAN_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Theseus RLDS/Minari Trace Export Import",
            rel(RESULT),
            "1 READY export",
            "license metadata",
            "replay smoke",
            "prototype-backed",
        ],
        CHAPTER: [
            "Theseus RLDS/Minari trace-export import",
            CLAIM_ID,
            rel(RESULT),
            "does not prove RLDS dataset correctness",
        ],
        READER: [
            "Theseus RLDS/Minari trace-export import",
            "one READY export manifest",
            "not dataset quality",
        ],
        OUTLINE: [CLAIM_ID, PROOF_TAG, "validate_theseus_rlds_minari_trace_export_import.py"],
        CHANGELOG: ["Import Theseus RLDS/Minari trace export", rel(RESULT), CLAIM_ID],
        NON_CORE: [CLAIM_ID, "docs/theseus_rlds_minari_trace_export_import.md", "14 narrow transitions"],
        PROJECT_THESEUS_LEDGER: ["RLDS/Minari trace-export imports", "docs/theseus_rlds_minari_trace_export_import.md"],
        TEST_LEDGER: ["Theseus RLDS/Minari trace export import", "scripts/validate_theseus_rlds_minari_trace_export_import.py"],
        VALIDATE_BOOK: [
            "scripts/validate_theseus_rlds_minari_trace_export_import.py",
            "docs/theseus_rlds_minari_trace_export_import.md",
            rel(RESULT),
            'run_validator("validate_theseus_rlds_minari_trace_export_import.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{rel(path)} missing required phrase: {phrase}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not VALID_FIXTURE.exists():
        fail([f"Missing valid fixture {rel(VALID_FIXTURE)}."])
    valid = load_json(VALID_FIXTURE)
    if not isinstance(valid, dict):
        fail([f"{rel(VALID_FIXTURE)} must contain an object."])
    record_errors, _ = validate_record(valid, rel(VALID_FIXTURE))
    errors.extend(record_errors)
    invalid_count = validate_invalid_controls(errors)
    expected = expected_result(valid, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_transition(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    action = "wrote" if args.write_result else "validated"
    print(
        "Theseus RLDS/Minari trace export import "
        f"{action}: {expected['export_count']} READY export, "
        f"{expected['format_count']} formats, {expected['field_count']} fields, "
        f"{expected['expected_invalid_control_count']} rejected controls."
    )


if __name__ == "__main__":
    main()
