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
SCHEMA = ROOT / "schemas" / "theseus_report.schema.json"
VALID_DIR = ROOT / "experiments" / "theseus_import" / "fixtures" / "valid"
INVALID_DIR = ROOT / "experiments" / "theseus_import" / "fixtures" / "invalid"
RESULT = ROOT / "experiments" / "theseus_import" / "results" / "2026-06-29-local.json"
SUMMARY = ROOT / "docs" / "theseus_report_import_slice.md"

EXPECTED_SOURCE_SHA256 = "7994e2909029644d6073289d8c9c59f774473f366a1c8cbda5943326f28518b2"
EXPECTED_REPORT_ID = "theseus.architecture_gate.20260618T192303Z.public_static_import"
EXPECTED_GATES = {
    "rgs_complete",
    "rmi_complete",
    "ora_complete",
    "rule_router_eval_passed",
    "learned_router_head_promoted",
    "safety_ledger_passed",
    "regression_suite_present",
    "public_calibration_present",
    "residual_escrow_present",
    "bridge_benchmark_present",
    "procedural_tools_registered",
    "routing_memory_present",
    "arm_lifecycle_governed",
    "external_inference_zero",
}
REQUIRED_CHAPTERS = {
    "recursive-self-improvement-boundaries",
    "readiness-gates-residual-escrow-and-quarantine",
    "project-theseus-as-report-first-implementation-reference",
}
REQUIRED_NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not prove deployed Theseus runtime behavior",
    "does not authorize heavy training",
    "does not copy private training rows",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Project Theseus report validation failed:")
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
        if not isinstance(cursor, dict) or part not in cursor:
            raise KeyError(path)
        cursor = cursor[part]
    if not isinstance(cursor, dict):
        raise KeyError(path)
    cursor[parts[-1]] = new_value


def validate_non_claims(owner: str, non_claims: Any, errors: list[str]) -> None:
    if not isinstance(non_claims, list) or not non_claims:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    blob = text_blob(non_claims)
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing boundary phrase {phrase!r}.")


def validate_report(report: dict[str, Any], schema: dict[str, Any], owner: str) -> list[str]:
    errors = validate_value(report, schema, owner)
    if errors:
        return errors

    if report.get("report_id") != EXPECTED_REPORT_ID:
        errors.append(f"{owner}: report_id must be {EXPECTED_REPORT_ID}.")
    if report.get("trace_class") != "architecture_gate":
        errors.append(f"{owner}: trace_class must be architecture_gate.")

    source_project = report.get("source_project", {})
    if source_project.get("git_commit") != "1ad88a22":
        errors.append(f"{owner}: source_project.git_commit must be 1ad88a22.")
    if source_project.get("worktree_state") != "dirty_at_import_review":
        errors.append(f"{owner}: worktree_state must record dirty_at_import_review.")

    source_artifact = report.get("source_artifact", {})
    source_sha = source_artifact.get("source_artifact_sha256")
    expected_replay_sha = report.get("replay", {}).get("expected_source_artifact_sha256")
    if source_sha != EXPECTED_SOURCE_SHA256:
        errors.append(f"{owner}: source artifact digest mismatch.")
    if expected_replay_sha != EXPECTED_SOURCE_SHA256:
        errors.append(f"{owner}: replay source artifact digest mismatch.")
    if source_artifact.get("source_artifact_status") != "sanitized_static_import":
        errors.append(f"{owner}: source artifact must be a sanitized_static_import.")

    public_safety = report.get("public_safety", {})
    if public_safety.get("redaction_state") != "public_safe_static_summary":
        errors.append(f"{owner}: redaction state must be public_safe_static_summary.")
    if public_safety.get("private_payload_copied") is not False:
        errors.append(f"{owner}: private payload copied.")
    redactions = public_safety.get("redactions", [])
    if not isinstance(redactions, list) or len(redactions) < 4:
        errors.append(f"{owner}: redactions must name at least four excluded private surfaces.")

    gates = report.get("gate_decisions", [])
    if not isinstance(gates, list) or len(gates) != len(EXPECTED_GATES):
        errors.append(f"{owner}: gate_decisions must contain exactly {len(EXPECTED_GATES)} gates.")
        gates = []
    observed_gates = {row.get("gate") for row in gates if isinstance(row, dict)}
    if observed_gates != EXPECTED_GATES:
        errors.append(f"{owner}: gate set does not match expected architecture gate set.")
    failed_gates = [row.get("gate") for row in gates if isinstance(row, dict) and row.get("passed") is not True]
    if failed_gates:
        errors.append(f"{owner}: all imported gate decisions must pass; failed {failed_gates}.")

    decision = report.get("decision_summary", {})
    expected_decision = {
        "status": "ready_for_heavy_training",
        "ready_for_heavy_training": True,
        "gate_count": 14,
        "passed_count": 14,
        "external_inference_calls": 0,
    }
    for key, expected in expected_decision.items():
        if decision.get(key) != expected:
            errors.append(f"{owner}: decision_summary.{key} must be {expected!r}.")

    failed_attempt_text = text_blob(report.get("failed_attempts", []))
    if "live_theseus_rerun_blocked_dirty_checkout" not in failed_attempt_text:
        errors.append(f"{owner}: failed_attempts must record the blocked dirty-checkout rerun.")

    replay = report.get("replay", {})
    if replay.get("mode") != "digest_verification" or replay.get("ci_verifiable") is not True:
        errors.append(f"{owner}: replay must be CI-verifiable digest_verification.")
    if replay.get("command") != "python3 scripts/validate_theseus_report.py":
        errors.append(f"{owner}: replay.command must name this validator.")

    connected = set(report.get("connected_chapter_ids", []))
    if not REQUIRED_CHAPTERS.issubset(connected):
        errors.append(f"{owner}: connected_chapter_ids missing {sorted(REQUIRED_CHAPTERS - connected)}.")
    if report.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append(f"{owner}: support state effect must remain no_chapter_core_claim_promotion.")

    boundaries = text_blob(report.get("claim_boundaries", []))
    for phrase in (
        "checkpoint recorded a 14/14 architecture-gate pass",
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
        if not isinstance(spec.get(key), (str, dict)):
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
    except KeyError:
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
        "Project Theseus Report Import Slice",
        EXPECTED_REPORT_ID,
        EXPECTED_SOURCE_SHA256,
        expected_digest,
        "14/14",
        "dirty_at_import_review",
        "live_theseus_rerun_blocked_dirty_checkout",
        "Does not promote any chapter core claim above `argument`.",
        "Does not prove deployed Theseus runtime behavior",
        "python3 scripts/validate_theseus_report.py",
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
    if len(invalid_paths) != 3:
        errors.append(f"{rel(INVALID_DIR)} must contain exactly three expected-invalid mutation fixtures.")

    report: dict[str, Any] | None = None
    report_digest = ""
    for path in valid_paths:
        value = load_json(path)
        if not isinstance(value, dict):
            errors.append(f"{rel(path)} must contain an object.")
            continue
        report = value
        report_errors = validate_report(value, schema, rel(path))
        errors.extend(report_errors)
        if not report_errors:
            report_digest = stable_hash(value)

    for path in invalid_paths:
        validate_invalid_fixture(path, schema, errors)

    if report is not None and report_digest:
        expected_result = {
            "schema_version": "0.1",
            "result_id": "2026-06-29-theseus-architecture-gate-public-import",
            "slice_id": "theseus_report_import",
            "validation_result": "pass",
            "accepted_report_id": EXPECTED_REPORT_ID,
            "accepted_public_report_sha256": report_digest,
            "source_artifact_sha256": EXPECTED_SOURCE_SHA256,
            "valid_report_count": len(valid_paths),
            "expected_invalid_count": len(invalid_paths),
            "accepted_gate_count": 14,
            "accepted_passed_count": 14,
            "support_state_effect": "no_chapter_core_claim_promotion",
            "ci_verification_command": "python3 scripts/validate_theseus_report.py",
        }
        validate_result(expected_result, errors)
        validate_summary(report_digest, errors)

    if errors:
        fail(errors)

    print(
        "Project Theseus report validation passed: "
        f"{len(valid_paths)} valid report, {len(invalid_paths)} expected-invalid controls, "
        f"digest {report_digest}."
    )


if __name__ == "__main__":
    main()
