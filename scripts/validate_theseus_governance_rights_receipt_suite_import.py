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
    / "theseus_governance_rights_receipt_suite_import"
    / "fixtures"
    / "valid"
    / "governance_rights_receipt_suite_import.valid.json"
)
INVALID_DIR = (
    ROOT
    / "experiments"
    / "theseus_governance_rights_receipt_suite_import"
    / "fixtures"
    / "invalid"
)
RESULT = (
    ROOT
    / "experiments"
    / "theseus_governance_rights_receipt_suite_import"
    / "results"
    / "2026-07-05-local.json"
)
DOC = ROOT / "docs" / "theseus_governance_rights_receipt_suite_import.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_governance_rights_receipt_suite_import_prototype_backed.json"
)
CHAPTER = ROOT / "chapters" / "moral-uncertainty-and-value-conflict.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "moral-uncertainty-and-value-conflict.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "GovernanceRights.lean"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

COMMAND = "python3 scripts/validate_theseus_governance_rights_receipt_suite_import.py"
IMPORT_ID = "theseus-governance-rights-receipt-suite-import-2026-07-05"
CLAIM_ID = "moral-uncertainty-and-value-conflict.theseus_governance_rights_receipt_suite_import"
PROOF_TAG = "lean:governance.rights.theseus_receipt_suite.fixture_bridge"
EXPECTED_SOURCE_SHA = "a3bf2de7469cf5c2eee8459a0fdd53e707c0f1b9104e96fa859633eddb4a5fb4"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "runtime/candidate_replay_contract_v1",
    "checkpoints/",
    ".npz",
    "private_train/",
    "data/training_data/high_transfer/private_train",
)
REQUIRED_GOVERNANCE_SCENARIOS = (
    "complete_audit_response",
    "justified_redaction_with_appeal",
    "exit_export_with_portable_state",
    "fork_denied_safety_obligations",
)
REQUIRED_CONSTITUTIONAL_SCENARIOS = (
    "least_sufficient_power_prefers_low_power_route",
    "predicate_conflict_routes_to_review",
    "constitutional_migration_requires_record",
    "self_modification_weakening_rejected",
)
REQUIRED_GOVERNANCE_TYPES = ("audit", "audit_redaction", "exit", "fork")
REQUIRED_PREDICATES = (
    "predicate.least_sufficient_power.v1",
    "predicate.conflict_review.v1",
    "predicate.constitutional_migration.v1",
    "predicate.self_modification_freeze.v1",
)
REQUIRED_NON_CLAIMS = (
    "Governance-right receipt fixtures prove material-usability protocol shape only.",
    "Constitutional-predicate fixtures prove record-level control semantics only.",
    "This is not institutional governance, legal compliance, moral correctness, public benchmark transfer, or learned-generation evidence.",
    "does not copy the raw Project Theseus report or private payloads into this public repository",
    "does not prove legal rights, institutional governance, reviewer independence, export usability, safe fork execution, moral correctness, deployed runtime enforcement, clean live Project Theseus replay, safety, alignment, transfer, deployment readiness, or ASI",
    "does not promote any chapter core claim above argument",
)
LEAN_THEOREMS = (
    "theseus_governance_rights_receipt_suite_import_fixture_valid",
    "theseus_governance_rights_receipt_suite_import_core_promotion_rejected",
    "theseus_governance_rights_receipt_suite_import_legal_rights_overclaim_rejected",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus governance-rights receipt suite import validation failed:")
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


def require_exact_list(owner: str, record: dict[str, Any], field: str, expected: tuple[str, ...], errors: list[str]) -> None:
    value = record.get(field)
    if not isinstance(value, list):
        errors.append(f"{owner}: {field} must be a list.")
        return
    if value != list(expected):
        errors.append(f"{owner}: {field} must preserve {list(expected)!r}.")


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if record.get("schema_version") != "asi_stack.theseus_governance_rights_receipt_suite_import.v0":
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
    if record.get("policy") != "project_theseus_governance_rights_receipt_suite_v1":
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
            errors.append(f"{owner}: sanitized fixture leaks forbidden private fragment {forbidden!r}.")

    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{owner}: summary must be an object.")
        summary = {}
    for field, expected in {
        "artifact_graph_record_count": 8,
        "claim_record_count": 8,
        "constitutional_fixture_count": 4,
        "constitutional_predicate_record_count": 4,
        "constitutional_predicate_scenario_count": 4,
        "evidence_transition_record_count": 8,
        "external_inference_calls": 0,
        "failure_boundary_record_count": 8,
        "fallback_return_count": 0,
        "fixture_count": 4,
        "fork_safety_scenario_count": 1,
        "governance_right_record_count": 4,
        "hard_gap_count": 0,
        "material_audit_scenario_count": 2,
        "passed_constitutional_fixture_count": 4,
        "passed_fixture_count": 4,
        "portable_exit_scenario_count": 1,
        "public_training_rows_written": 0,
        "required_constitutional_scenario_count": 4,
        "required_scenario_count": 4,
        "warning_count": 0,
    }.items():
        require_count(owner, summary.get(field), expected, f"summary.{field}", errors)

    counts = record.get("record_counts")
    if not isinstance(counts, dict):
        errors.append(f"{owner}: record_counts must be an object.")
        counts = {}
    for field, expected in {
        "artifact_graph_records": 8,
        "claim_records": 8,
        "constitutional_predicate_records": 4,
        "evidence_transition_records": 8,
        "failure_boundary_records": 8,
        "governance_right_records": 4,
    }.items():
        require_count(owner, counts.get(field), expected, f"record_counts.{field}", errors)

    require_exact_list(owner, record, "governance_right_scenarios", REQUIRED_GOVERNANCE_SCENARIOS, errors)
    require_exact_list(owner, record, "constitutional_predicate_scenarios", REQUIRED_CONSTITUTIONAL_SCENARIOS, errors)
    require_exact_list(owner, record, "governance_right_types", REQUIRED_GOVERNANCE_TYPES, errors)
    require_exact_list(owner, record, "constitutional_predicate_ids", REQUIRED_PREDICATES, errors)
    if record.get("hard_gaps") != []:
        errors.append(f"{owner}: hard_gaps must remain empty.")
    if record.get("warnings") != []:
        errors.append(f"{owner}: warnings must remain empty.")

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
        "constitutional_chapter_core_promotion_claimed",
        "legal_rights_claimed",
        "institutional_governance_claimed",
        "moral_correctness_claimed",
        "reviewer_independence_claimed",
        "deployed_runtime_enforcement_claimed",
        "clean_live_theseus_replay_claimed",
    ):
        if boundary.get(field) is not False:
            errors.append(f"{owner}: {field} must remain false.")

    safety = record.get("public_safety_boundary")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety_boundary must be an object.")
        safety = {}
    for field in ("public_training_rows_written", "external_inference_calls", "fallback_return_count"):
        require_count(owner, safety.get(field), 0, field, errors)
    for field in (
        "raw_private_payloads_exported",
        "public_prompts_tests_solutions_traces_or_score_labels_exported",
        "model_artifacts_or_checkpoints_exported",
    ):
        if safety.get(field) is not False:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain false.")

    non_claim_blob = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_blob:
            errors.append(f"{owner}: non_claims missing {phrase!r}.")

    metrics = {
        "fixture_sha256": stable_hash(record),
        "summary": summary,
        "record_counts": counts,
        "governance_scenario_count": len(record.get("governance_right_scenarios", [])),
        "constitutional_scenario_count": len(record.get("constitutional_predicate_scenarios", [])),
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
        "schema_version": "asi_stack.theseus_governance_rights_receipt_suite_import.result.v0",
        "result_id": "2026-07-05-theseus-governance-rights-receipt-suite-import",
        "import_id": IMPORT_ID,
        "validation_result": "pass",
        "command": COMMAND,
        "valid_fixture_count": 1,
        "expected_invalid_count": invalid_count,
        "fixture_sha256": metrics["fixture_sha256"],
        "source_report_sha256": record["source_report_sha256"],
        "source_commit": record["source_commit"],
        "source_checkout_state": record["source_checkout_state"],
        "governance_scenario_count": metrics["governance_scenario_count"],
        "constitutional_scenario_count": metrics["constitutional_scenario_count"],
        "record_counts": metrics["record_counts"],
        "summary": metrics["summary"],
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
            "module": "AsiStackProofs.GovernanceRights",
            "proof_tag": PROOF_TAG,
            "fixture_def": "theseusGovernanceRightsReceiptSuiteImportFixture",
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
            "Project Theseus Governance-Rights Receipt Suite Import",
            IMPORT_ID,
            EXPECTED_SOURCE_SHA,
            "prototype-backed",
            "does not prove legal rights",
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
            "TheseusGovernanceRightsReceiptSuiteSummary",
            "theseusGovernanceRightsReceiptSuiteImportFixture",
            *LEAN_THEOREMS,
        ],
        errors,
    )
    for path in (CHAPTER, READER_CHAPTER, OUTLINE):
        require_text(
            path,
            [
                "Theseus governance-rights receipt suite import",
                CLAIM_ID,
                COMMAND,
                "does not prove legal rights",
            ],
            errors,
        )
    require_text(
        CHANGELOG,
        [
            "Theseus governance-rights receipt suite import",
            COMMAND,
            CLAIM_ID,
        ],
        errors,
    )
    require_text(
        VALIDATION_REGISTRY,
        [
            "scripts/validate_theseus_governance_rights_receipt_suite_import.py",
            "docs/theseus_governance_rights_receipt_suite_import.md",
            "evidence_transitions/v1_x_measured/theseus_governance_rights_receipt_suite_import_prototype_backed.json",
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
        "Theseus governance-rights receipt suite import validation passed: "
        f"{len(invalid_paths)} expected-invalid controls, "
        f"{metrics['governance_scenario_count']} governance scenarios and "
        f"{metrics['constitutional_scenario_count']} constitutional scenarios."
    )


if __name__ == "__main__":
    main()
