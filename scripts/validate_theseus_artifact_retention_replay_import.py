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
VALID_FIXTURE = (
    ROOT
    / "experiments"
    / "theseus_artifact_retention_replay_import"
    / "fixtures"
    / "valid"
    / "artifact_retention_replay_import.valid.json"
)
INVALID_DIR = (
    ROOT
    / "experiments"
    / "theseus_artifact_retention_replay_import"
    / "fixtures"
    / "invalid"
)
RESULT = (
    ROOT
    / "experiments"
    / "theseus_artifact_retention_replay_import"
    / "results"
    / "2026-07-05-local.json"
)
DOC = ROOT / "docs" / "theseus_artifact_retention_replay_import.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_artifact_retention_replay_import_prototype_backed.json"
)
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "project-theseus-as-report-first-implementation-reference.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

COMMAND = "python3 scripts/validate_theseus_artifact_retention_replay_import.py"
IMPORT_ID = "theseus-artifact-retention-replay-import-2026-07-05"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.artifact_retention_replay_gate_import"
PROOF_TAG = "lean:theseus.reference.artifact_retention_replay_import.fixture_bridge"
EXPECTED_SOURCE_SHA = "a3d35452ec3a8f0db233f5985d5d0824a1d9f571ee9012970d52303bfece9759"
EXPECTED_REPLAY_SHA = "5d26d57612479e1b5a0547af49e34d8ae779aef41e91b3eb2e676ad415a99da3"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "student_code_lm_checkpoint",
    "decoder_v2_private_ablation_gate",
    "archive/report_artifacts/",
    "reports/report_snapshots/",
)
REQUIRED_NON_CLAIMS = (
    "does not copy the raw Project Theseus report or private payloads into this public repository",
    "does not prove clean live Project Theseus replay",
    "does not prove deployed residual-ledger storage or deployed artifact-graph behavior",
    "does not prove model quality, benchmark performance, generation speed, safety, alignment, transfer, deployment readiness, or ASI",
    "does not promote any chapter core claim above argument",
)
LEAN_THEOREMS = (
    "theseus_artifact_retention_replay_import_fixture_valid",
    "theseus_artifact_retention_replay_import_hash_mismatch_rejected",
    "theseus_artifact_retention_replay_import_core_promotion_rejected",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus artifact-retention replay import validation failed:")
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
        if isinstance(cursor, dict):
            cursor = cursor[part]
        elif isinstance(cursor, list):
            cursor = cursor[int(part)]
        else:
            raise KeyError(path)
    last = parts[-1]
    if isinstance(cursor, dict):
        cursor[last] = new_value
    elif isinstance(cursor, list):
        cursor[int(last)] = new_value
    else:
        raise KeyError(path)


def require_bool(record: dict[str, Any], owner: str, field: str, expected: bool, errors: list[str]) -> None:
    if record.get(field) is not expected:
        errors.append(f"{owner}: {field} must remain {str(expected).lower()}.")


def require_count(owner: str, value: Any, expected: int, field: str, errors: list[str]) -> None:
    if value != expected:
        errors.append(f"{owner}: {field} must be {expected}.")


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if record.get("schema_version") != "asi_stack.theseus_artifact_retention_replay_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_report_sha256") != EXPECTED_SOURCE_SHA:
        errors.append(f"{owner}: source_report_sha256 mismatch.")
    if record.get("policy") != "project_theseus_artifact_retention_replay_gate_v1":
        errors.append(f"{owner}: policy mismatch.")
    if record.get("trigger_state") != "GREEN":
        errors.append(f"{owner}: trigger_state must be GREEN.")
    for field in ("raw_report_copied", "private_payload_copied"):
        require_bool(record, owner, field, False, errors)
    for field in ("private_path_fields_redacted", "sanitized_for_public_repo"):
        require_bool(record, owner, field, True, errors)

    public_text = text_blob(record)
    for forbidden in FORBIDDEN_PUBLIC_TEXT:
        if forbidden in public_text:
            errors.append(f"{owner}: sanitized fixture leaks forbidden private path fragment {forbidden!r}.")

    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{owner}: summary must be an object.")
        summary = {}
    for field, expected in {
        "eligible_action_count": 1,
        "passed_replay_count": 1,
        "failed_replay_count": 0,
        "pointer_verified_count": 1,
        "defeater_verified_count": 1,
        "json_parse_verified_count": 1,
        "hard_gap_count": 0,
        "runtime_ms": 391,
    }.items():
        require_count(owner, summary.get(field), expected, f"summary.{field}", errors)

    replay = record.get("sanitized_replay_check")
    if not isinstance(replay, dict):
        errors.append(f"{owner}: sanitized_replay_check must be an object.")
        replay = {}
    if replay.get("expected_sha256") != EXPECTED_REPLAY_SHA:
        errors.append(f"{owner}: expected_sha256 mismatch.")
    if replay.get("decoded_sha256") != replay.get("expected_sha256"):
        errors.append(f"{owner}: decoded_sha256 must equal expected_sha256.")
    for field in (
        "passed",
        "path_fields_redacted",
        "archive_exists",
        "pointer_verified",
        "resolver_verified",
        "hash_verified",
        "json_parse_verified",
        "defeater_verified",
        "compression_record_verified",
    ):
        if replay.get(field) is not True:
            errors.append(f"{owner}: sanitized_replay_check.{field} must be true.")
    for field, expected in {
        "payload_bytes": 41943527,
        "archived_bytes": 2389576,
        "public_training_rows_written": 0,
        "external_inference_calls": 0,
        "fallback_return_count": 0,
    }.items():
        require_count(owner, replay.get(field), expected, f"sanitized_replay_check.{field}", errors)
    if not isinstance(record.get("source_report_sha256"), str) or not SHA_RE.match(record["source_report_sha256"]):
        errors.append(f"{owner}: source_report_sha256 must be a SHA-256 hex digest.")

    counts = record.get("record_counts")
    if not isinstance(counts, dict):
        errors.append(f"{owner}: record_counts must be an object.")
        counts = {}
    for field in (
        "compressed_artifact_records",
        "compression_receipts",
        "proof_contract_receipt_records",
        "claim_records",
        "artifact_graph_records",
        "evidence_transition_records",
        "defeater_records",
    ):
        require_count(owner, counts.get(field), 1, f"record_counts.{field}", errors)

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    expected_boundary = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "transition_effect": "upward",
        "chapter_core_support_effect": "none",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for field, expected in expected_boundary.items():
        if boundary.get(field) != expected:
            errors.append(f"{owner}: claim_boundary.{field} must be {expected!r}.")
    for field in (
        "chapter_core_promotion_claimed",
        "model_quality_claimed",
        "benchmark_performance_claimed",
        "clean_live_theseus_replay_claimed",
        "deployed_residual_ledger_claimed",
        "deployed_artifact_graph_claimed",
    ):
        if boundary.get(field) is not False:
            errors.append(f"{owner}: {field} must remain false.")

    safety = record.get("public_safety_boundary")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety_boundary must be an object.")
        safety = {}
    for field in ("public_training_rows_written", "external_inference_calls", "fallback_return_count"):
        require_count(owner, safety.get(field), 0, field, errors)
    for field in ("raw_private_payloads_exported", "public_prompts_tests_solutions_traces_or_score_labels_exported"):
        if safety.get(field) is not False:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain false.")

    non_claim_blob = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_blob:
            errors.append(f"{owner}: non_claims missing {phrase!r}.")

    metrics = {
        "fixture_sha256": stable_hash(record),
        "payload_bytes": replay.get("payload_bytes"),
        "archived_bytes": replay.get("archived_bytes"),
        "compression_ratio": round(replay.get("payload_bytes", 0) / replay.get("archived_bytes", 1), 3),
        "record_counts": counts,
    }
    return errors, metrics


def validate_invalid_fixture(path: Path, base_record: dict[str, Any], errors: list[str]) -> None:
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
    mutation = spec.get("mutation")
    if not isinstance(mutation, dict) or not isinstance(mutation.get("path"), str) or "value" not in mutation:
        errors.append(f"{owner}: mutation must contain path and value.")
        return
    mutated = copy.deepcopy(base_record)
    try:
        set_path(mutated, mutation["path"], mutation["value"])
    except (KeyError, IndexError, ValueError):
        errors.append(f"{owner}: mutation path {mutation['path']!r} does not exist.")
        return
    observed, _metrics = validate_record(mutated, owner)
    if not observed:
        errors.append(f"{owner}: expected invalid mutation passed validation.")
        return
    expected_fragment = str(spec["expected_error_fragment"])
    if expected_fragment not in "\n".join(observed):
        errors.append(f"{owner}: expected error fragment {expected_fragment!r}; got {observed}.")


def build_result(record: dict[str, Any], metrics: dict[str, Any], invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.theseus_artifact_retention_replay_import.result.v0",
        "result_id": "2026-07-05-theseus-artifact-retention-replay-import",
        "import_id": IMPORT_ID,
        "validation_result": "pass",
        "command": COMMAND,
        "valid_fixture_count": 1,
        "expected_invalid_count": invalid_count,
        "fixture_sha256": metrics["fixture_sha256"],
        "source_report_sha256": record["source_report_sha256"],
        "payload_bytes": metrics["payload_bytes"],
        "archived_bytes": metrics["archived_bytes"],
        "compression_ratio_observed_not_benchmarked": metrics["compression_ratio"],
        "record_counts": metrics["record_counts"],
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "chapter_core_support_effect": "none",
        "artifact_refs": [
            rel(VALID_FIXTURE),
            rel(RESULT),
            rel(DOC),
            rel(TRANSITION),
            rel(LEAN_FILE),
        ],
        "lean_alignment": {
            "module": "AsiStackProofs.TheseusReference",
            "proof_tag": PROOF_TAG,
            "fixture_def": "theseusArtifactRetentionReplayImportFixture",
            "checked_theorem_names": list(LEAN_THEOREMS),
        },
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def require_text(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"required path missing: {rel(path)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    normalized = re.sub(r"\s+", " ", text)
    for phrase in phrases:
        haystack = normalized if " " in phrase else text
        if phrase not in haystack:
            errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def validate_surfaces(errors: list[str]) -> None:
    require_text(
        DOC,
        [
            "Project Theseus Artifact-Retention Replay Import",
            IMPORT_ID,
            EXPECTED_SOURCE_SHA,
            "prototype-backed",
            "does not prove clean live Project Theseus replay",
        ],
        errors,
    )
    require_text(
        TRANSITION,
        [CLAIM_ID, "prototype-backed", rel(VALID_FIXTURE), COMMAND],
        errors,
    )
    require_text(
        LEAN_FILE,
        [
            "TheseusArtifactRetentionReplayImportSummary",
            "theseusArtifactRetentionReplayImportFixture",
            *LEAN_THEOREMS,
        ],
        errors,
    )
    for path in (CHAPTER, READER_CHAPTER, OUTLINE):
        require_text(
            path,
            [
                "artifact-retention replay",
                CLAIM_ID,
                COMMAND,
                "does not prove clean live Project Theseus replay",
            ],
            errors,
        )
    require_text(
        CHANGELOG,
        [
            "Theseus artifact-retention replay import",
            COMMAND,
            CLAIM_ID,
        ],
        errors,
    )
    require_text(
        VALIDATION_REGISTRY,
        [
            "scripts/validate_theseus_artifact_retention_replay_import.py",
            "docs/theseus_artifact_retention_replay_import.md",
            "evidence_transitions/v1_x_measured/theseus_artifact_retention_replay_import_prototype_backed.json",
        ],
        errors,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not VALID_FIXTURE.exists():
        fail([f"missing fixture: {rel(VALID_FIXTURE)}"])
    fixture = load_json(VALID_FIXTURE)
    if not isinstance(fixture, dict):
        fail([f"{rel(VALID_FIXTURE)} must contain an object."])
    fixture_errors, metrics = validate_record(fixture, rel(VALID_FIXTURE))
    errors.extend(fixture_errors)
    invalid_paths = sorted(INVALID_DIR.glob("*.invalid.json"))
    if len(invalid_paths) != 7:
        errors.append(f"expected 7 invalid controls, found {len(invalid_paths)}.")
    for path in invalid_paths:
        validate_invalid_fixture(path, fixture, errors)

    built = build_result(fixture, metrics, len(invalid_paths))
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not RESULT.exists():
        errors.append(f"{rel(RESULT)} missing; run `{COMMAND} --write-result`.")
    else:
        recorded = load_json(RESULT)
        if recorded != built:
            errors.append(f"{rel(RESULT)} is stale; rerun `{COMMAND} --write-result`.")
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print(
        "Theseus artifact-retention replay import validation passed: "
        f"{len(invalid_paths)} expected-invalid controls, "
        f"{metrics['payload_bytes']} payload bytes replayed by exact hash in sanitized source report."
    )


if __name__ == "__main__":
    main()
