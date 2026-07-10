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
BASE = ROOT / "experiments" / "theseus_module_definition_of_done_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "module_definition_of_done_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-05-local.json"
DOC = ROOT / "docs" / "theseus_module_definition_of_done_import.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_module_definition_of_done_import_prototype_backed.json"
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER_CHAPTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

COMMAND = "python3 scripts/validate_theseus_module_definition_of_done_import.py"
IMPORT_ID = "theseus-module-definition-of-done-import-2026-07-05"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.module_definition_of_done_gate_import"
PROOF_TAG = "lean:theseus.reference.module_definition_of_done_import.fixture_bridge"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_HASHES = {
    "source_config_sha256": "116833d9a771ee768d67fe794111eda25c6d76fcaddbc3ee013e1f9b7e8963fc",
    "source_gate_script_sha256": "43d54cbde5b2aaad48c6a5ba32fec983e7c54fe3430b3be3d502e74a6aa2d5ef",
    "source_report_sha256": "efd0897b0a4e0158166398177c76df2c9ca3f79eed0956c253f4572cd852a0f2",
    "module_records_sha256": "e0199864080c2e391ad24b1a46e35bc6941699c8a4f1d17eb46720ef1e07ce38",
    "source_backlog_work_cards_sha256": "d6b6d639bffd18bd1be491a7ad8bf3b978bde526e4fe816331e92653ccb58fdf",
}
EXPECTED_SUMMARY = {
    "book_standard_source_count": 7,
    "book_standard_source_present_count": 7,
    "cleanup_queue_count": 0,
    "hard_gap_count": 0,
    "major_surface_count": 22,
    "major_surface_coverage_ratio": 1.0,
    "module_record_count": 22,
    "module_records_ready": 22,
    "negative_evidence_linked": True,
    "source_backlog_item_count": 20,
    "source_backlog_route_smoke_passed": True,
    "source_backlog_steward_decision_candidate_count": 20,
    "source_backlog_work_card_count": 20,
    "stale_latest_view_count": 0,
    "steward_decision_count": 8,
    "surfaces_over_report_cap": 0,
    "warning_count": 0,
}
EXPECTED_RULES = ("module_card", "source_crosswalk", "non_claim", "retirement")
EXPECTED_THEOREMS = (
    "theseus_module_definition_of_done_import_fixture_valid",
    "theseus_module_definition_of_done_import_core_promotion_rejected",
    "theseus_module_definition_of_done_import_capability_overclaim_rejected",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "checkpoints/",
    ".npz",
    "private_train/",
    "data/training_data/high_transfer/private_train",
    "runtime/dogfood/",
    "candidate_body",
    "solution_body",
)
REQUIRED_NON_CLAIMS = (
    "Project Theseus module definition-of-done gate health is repository-quality evidence only.",
    "does not copy the raw Project Theseus report",
    "does not prove clean live Project Theseus replay",
    "does not promote any chapter core claim above argument",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus module definition-of-done import validation failed:")
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
    if record.get("schema_version") != "asi_stack.theseus_module_definition_of_done_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("policy") != "project_theseus_module_definition_of_done_gate_v1":
        errors.append(f"{owner}: policy mismatch.")
    if record.get("trigger_state") != "GREEN":
        errors.append(f"{owner}: trigger_state must be GREEN.")

    for field, expected in EXPECTED_HASHES.items():
        value = record.get(field)
        if value != expected:
            errors.append(f"{owner}: {field} mismatch.")
        if not isinstance(value, str) or not SHA_RE.match(value):
            errors.append(f"{owner}: {field} must be a SHA-256 hex digest.")

    for field in ("raw_report_copied", "private_payload_copied"):
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
    for field, expected in EXPECTED_SUMMARY.items():
        if summary.get(field) != expected:
            errors.append(f"{owner}: summary.{field} must be {expected!r}.")

    rules = record.get("required_rules")
    if rules != list(EXPECTED_RULES):
        errors.append(f"{owner}: required_rules must preserve {list(EXPECTED_RULES)!r}.")
    sample = record.get("module_surface_sample")
    if not isinstance(sample, list) or len(sample) < 8 or "theseus_plan_compiler" not in sample:
        errors.append(f"{owner}: module_surface_sample must contain at least 8 named surfaces including theseus_plan_compiler.")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    expected_boundary = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "chapter_id": "project-theseus-as-report-first-implementation-reference",
        "chapter_core_claim_promotion": False,
        "capability_claim": False,
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
        "module_records_ready": summary.get("module_records_ready"),
        "major_surface_count": summary.get("major_surface_count"),
        "source_backlog_work_card_count": summary.get("source_backlog_work_card_count"),
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
    if len(controls) != 7:
        errors.append(f"expected 7 invalid controls, found {len(controls)}.")
    return errors, controls


def validate_transition(errors: list[str]) -> dict[str, Any]:
    record = load_json(TRANSITION)
    expected = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_command": COMMAND,
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for field, value in expected.items():
        if record.get(field) != value:
            errors.append(f"{rel(TRANSITION)}: {field} must be {value!r}.")
    if record.get("acceptance_blockers") != []:
        errors.append(f"{rel(TRANSITION)}: acceptance_blockers must be empty.")
    transition_text = text_blob(record)
    for phrase in ("does not prove clean live Project Theseus replay", "does not promote any chapter core claim"):
        if phrase.lower() not in transition_text.lower():
            errors.append(f"{rel(TRANSITION)} missing non-claim phrase {phrase!r}.")
    return record


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "triggerGreen",
        "moduleRecordsReady",
        "majorSurfaceCount",
        "hardGapCount",
        "warningCount",
        "sourceBacklogRouteSmokePassed",
        "chapterCorePromotion",
        "capabilityClaim",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing module DoD field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Theseus Module Definition Of Done Import",
            IMPORT_ID,
            "22 / 22",
            "20 source-backlog work cards",
            "seven expected-invalid controls",
            PROOF_TAG,
            "does not prove clean live Project Theseus replay",
        ],
        CHAPTER: [
            "module definition-of-done gate",
            "22 of 22 major module records ready",
            CLAIM_ID,
            "does not prove clean live Project Theseus replay",
        ],
        READER_CHAPTER: [
            "module definition-of-done gate",
            "22 of 22 major module records ready",
            "not a clean live Theseus replay",
        ],
        OUTLINE: [
            "Theseus module definition-of-done import",
            COMMAND,
            CLAIM_ID,
            PROOF_TAG,
        ],
        CHANGELOG: [
            "Import Theseus module definition-of-done gate",
            rel(RESULT),
            rel(TRANSITION),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_theseus_module_definition_of_done_import.py",
            "docs/theseus_module_definition_of_done_import.md",
            "experiments/theseus_module_definition_of_done_import/results/2026-07-05-local.json",
            '"script": "validate_theseus_module_definition_of_done_import.py"',
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
        "schema_version": "asi_stack.theseus_module_definition_of_done_import_result.v0",
        "result_id": IMPORT_ID,
        "command": COMMAND,
        "source_commit": valid["source_commit"],
        "source_checkout_state": valid["source_checkout_state"],
        "policy": valid["policy"],
        "trigger_state": valid["trigger_state"],
        "summary": valid["summary"],
        "claim_boundary": valid["claim_boundary"],
        "public_safety": {
            "raw_report_copied": valid["raw_report_copied"],
            "private_payload_copied": valid["private_payload_copied"],
            "private_path_fields_redacted": valid["private_path_fields_redacted"],
            "sanitized_for_public_repo": valid["sanitized_for_public_repo"],
        },
        "expected_invalid_controls": controls,
        "expected_invalid_control_count": len(controls),
        "valid_fixture_hash": stats["valid_fixture_hash"],
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.TheseusReference",
            "proof_tag": PROOF_TAG,
            "theorem_refs": list(EXPECTED_THEOREMS),
            "expected": {
                "trigger_green": True,
                "module_records_ready": 22,
                "major_surface_count": 22,
                "hard_gap_count": 0,
                "warning_count": 0,
                "source_backlog_route_smoke_passed": True,
                "chapter_core_promotion": False,
                "capability_claim": False,
            },
        },
        "support_state_effect": "bounded_non_core_transition_only",
        "chapter_core_support_effect": "none",
        "verification_result": "pass",
        "non_claims": valid["non_claims"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_doc(valid: dict[str, Any], controls: list[dict[str, Any]]) -> None:
    summary = valid["summary"]
    lines = [
        "# Theseus Module Definition Of Done Import",
        "",
        f"Import ID: `{IMPORT_ID}`",
        "",
        "This document records a sanitized public-safe Project Theseus module definition-of-done gate import. It is a bounded implementation-reference evidence slice, not a clean live Theseus replay and not a chapter-core support-state promotion.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---:|",
        f"| Trigger state | `{valid['trigger_state']}` |",
        f"| Major module records ready | {summary['module_records_ready']} / {summary['module_record_count']} |",
        f"| Major surfaces | {summary['major_surface_count']} |",
        f"| Major-surface coverage ratio | {summary['major_surface_coverage_ratio']} |",
        f"| Hard gaps | {summary['hard_gap_count']} |",
        f"| Warnings | {summary['warning_count']} |",
        f"| Book standard sources present | {summary['book_standard_source_present_count']} / {summary['book_standard_source_count']} |",
        f"| Source-backlog work cards | {summary['source_backlog_work_card_count']} |",
        f"| Steward decisions | {summary['steward_decision_count']} |",
        "",
        f"The import records {summary['source_backlog_work_card_count']} source-backlog work cards and seven expected-invalid controls.",
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
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
        ]
    )
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
    stats["expected_invalid_controls"] = len(controls)
    validate_transition(errors)
    write_result(valid, stats, controls)
    write_doc(valid, controls)
    validate_lean(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Theseus module definition-of-done import validation passed.")


if __name__ == "__main__":
    main()
