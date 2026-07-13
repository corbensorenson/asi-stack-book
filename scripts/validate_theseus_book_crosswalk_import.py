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
BASE = ROOT / "experiments" / "theseus_book_crosswalk_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "book_to_theseus_crosswalk_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-05-local.json"
DOC = ROOT / "docs" / "theseus_book_crosswalk_import.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_book_crosswalk_import_no_change.json"
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
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

COMMAND = "python3 scripts/validate_theseus_book_crosswalk_import.py"
IMPORT_ID = "theseus-book-crosswalk-import-2026-07-05"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.book_to_theseus_crosswalk_pointer"
PROOF_TAG = "lean:theseus.reference.book_crosswalk.pointer_boundary"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_SOURCE_REPORT = "reports/book_to_theseus_crosswalk.json"
EXPECTED_SOURCE_HASH = "76f28eab4f1ffba860bedcb41327191060bee9eab3dcf18739f3b2355128dd4b"
EXPECTED_STABLE_HASH = "d1ffd02d10682214bb28a6023196c46a899f1b132305ee7b9c0943f0b56c86c9"
EXPECTED_SUMMARY = {
    "ai_book_root_redacted": True,
    "ai_book_source_file_count": 1474,
    "ai_book_source_manifest_hash": "74e960bd50da56136881997996e130b4ece150c99f1eb93ddd223ade701b3cd5",
    "previous_source_inventory_available": True,
    "changed_source_file_count": 9,
    "removed_source_file_count": 0,
    "stale_phase_count": 0,
    "roadmap_backlog_item_count": 20,
    "source_sync_review_decision_count": 134,
    "cleared_roadmap_backlog_item_count": 0,
    "theseus_to_book_evidence_count": 53,
    "public_safe_evidence_smoke_passed": True,
    "source_sync_smoke_passed": True,
    "crosswalk_item_count": 20,
    "missing_source_basis_count": 0,
    "done_phase_missing_evidence_count": 0,
}
EXPECTED_POINTER_STATES = {
    "PUBLIC_SAFE_REPORT_POINTER": 46,
    "PUBLIC_SAFE_SOURCE_OR_CONFIG_POINTER": 7,
}
EXPECTED_SUPPORT_STATES = {"PUBLIC_SAFE_POINTER_ONLY": 53}
EXPECTED_RULES = (
    "source_basis",
    "evidence_sync",
    "no_bloat",
    "source_sync",
    "theseus_to_book_evidence",
)
EXPECTED_THEOREMS = (
    "theseus_book_crosswalk_import_fixture_valid",
    "theseus_book_crosswalk_import_pointer_only_preserves_argument",
    "theseus_book_crosswalk_import_source_sync_failure_rejected",
    "theseus_book_crosswalk_import_public_safety_failure_rejected",
    "theseus_book_crosswalk_import_core_promotion_rejected",
    "theseus_book_crosswalk_import_clean_replay_overclaim_rejected",
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
    "pointer-only implementation-reference evidence",
    "does not copy the raw Project Theseus crosswalk report",
    "does not prove clean live Project Theseus replay",
    "does not create an upward support-state transition",
    "does not promote any chapter core claim above argument",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus book-crosswalk import validation failed:")
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
    if record.get("schema_version") != "asi_stack.theseus_book_crosswalk_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("source_report") != EXPECTED_SOURCE_REPORT:
        errors.append(f"{owner}: source_report mismatch.")
    for field, expected in (
        ("source_report_sha256", EXPECTED_SOURCE_HASH),
        ("source_report_stable_sha256", EXPECTED_STABLE_HASH),
    ):
        value = record.get(field)
        if value != expected:
            errors.append(f"{owner}: {field} mismatch.")
        if not isinstance(value, str) or not SHA_RE.match(value):
            errors.append(f"{owner}: {field} must be a SHA-256 hex digest.")
    if record.get("policy") != "project_theseus_book_to_theseus_crosswalk_v1":
        errors.append(f"{owner}: policy mismatch.")
    if record.get("created_utc") != "2026-07-04T11:18:22.401681+00:00":
        errors.append(f"{owner}: created_utc mismatch.")
    if record.get("trigger_state") != "GREEN":
        errors.append(f"{owner}: trigger_state must be GREEN.")

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
    if record.get("pointer_state_counts") != EXPECTED_POINTER_STATES:
        errors.append(f"{owner}: pointer_state_counts mismatch.")
    if record.get("support_state_counts") != EXPECTED_SUPPORT_STATES:
        errors.append(f"{owner}: support_state_counts must preserve pointer-only support.")
    if record.get("rules_present") != list(EXPECTED_RULES):
        errors.append(f"{owner}: rules_present mismatch.")

    safety = record.get("public_safety_boundary")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety_boundary must be an object.")
        safety = {}
    for field in ("raw_report_copied", "private_payload_copied"):
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
        "chapter_core_claim_promotion": False,
        "clean_live_replay_claim": False,
        "deployment_claim": False,
        "model_quality_claim": False,
        "capability_claim": False,
        "pointer_only_evidence_claim": True,
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
        "theseus_to_book_evidence_count": summary.get("theseus_to_book_evidence_count"),
        "roadmap_backlog_item_count": summary.get("roadmap_backlog_item_count"),
        "source_sync_review_decision_count": summary.get("source_sync_review_decision_count"),
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
        "pointer-only",
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
        "structure TheseusBookCrosswalkImportSummary",
        "def theseusBookCrosswalkImportFixture",
        "TheseusBookCrosswalkImportPointerOnly",
        "TheseusBookCrosswalkImportPublicSafe",
        "TheseusBookCrosswalkImportPreservesBoundaries",
    ):
        if fragment not in text:
            errors.append(f"{rel(LEAN_FILE)} missing Lean fragment {fragment!r}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Theseus Book Crosswalk Import",
            IMPORT_ID,
            "53 public-safe pointer rows",
            "20 backlog cards",
            rel(TRANSITION),
            PROOF_TAG,
        ],
        CHAPTER: [
            "book-to-Theseus crosswalk import",
            "53 public-safe pointer rows",
            "does not prove clean live Project Theseus replay",
        ],
        READER_CHAPTER: [
            "book-to-Theseus crosswalk import",
            "53 public-safe pointer rows",
            "does not prove clean live Project Theseus replay",
        ],
        ACTIVE_CYCLE: [
            "book-to-Theseus crosswalk import",
            "53 public-safe pointer rows",
            "evidence_transitions/v1_x_measured/theseus_book_crosswalk_import_no_change.json",
        ],
        ROADMAP: [
            "book-to-Theseus crosswalk import",
            "53 public-safe pointer rows",
            "20 backlog cards",
        ],
        LEDGER: [
            CLAIM_ID,
            rel(TRANSITION),
            "book-to-Theseus crosswalk import",
        ],
        PROJECT_LEDGER: [
            "Book-to-Theseus crosswalk pointer imports | 1",
            "docs/theseus_book_crosswalk_import.md",
            "53 public-safe pointer rows",
        ],
        APPENDIX_E: [
            "Theseus book-to-Theseus crosswalk import validation",
            "scripts/validate_theseus_book_crosswalk_import.py",
            "53 public-safe pointer rows",
        ],
        CHANGELOG: [
            "Import Theseus book-to-Theseus crosswalk pointer",
            rel(RESULT),
            rel(TRANSITION),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_theseus_book_crosswalk_import.py",
            "docs/theseus_book_crosswalk_import.md",
            "experiments/theseus_book_crosswalk_import/results/2026-07-05-local.json",
            '"script": "validate_theseus_book_crosswalk_import.py"',
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
        "schema_version": "asi_stack.theseus_book_crosswalk_import_result.v0",
        "result_id": IMPORT_ID,
        "command": COMMAND,
        "source_commit": valid["source_commit"],
        "source_checkout_state": valid["source_checkout_state"],
        "source_report": valid["source_report"],
        "source_report_sha256": valid["source_report_sha256"],
        "source_report_stable_sha256": valid["source_report_stable_sha256"],
        "policy": valid["policy"],
        "created_utc": valid["created_utc"],
        "trigger_state": valid["trigger_state"],
        "summary": valid["summary"],
        "pointer_state_counts": valid["pointer_state_counts"],
        "support_state_counts": valid["support_state_counts"],
        "rules_present": valid["rules_present"],
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
                "trigger_green": True,
                "source_sync_smoke_passed": True,
                "public_safe_evidence_smoke_passed": True,
                "theseus_to_book_evidence_count": 53,
                "roadmap_backlog_item_count": 20,
                "pointer_only_rows": 53,
                "missing_source_basis_count": 0,
                "public_training_rows_written": 0,
                "external_inference_calls": 0,
                "fallback_return_count": 0,
                "chapter_core_promotion": False,
                "clean_live_replay_claimed": False,
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
        "# Theseus Book Crosswalk Import",
        "",
        f"Import ID: `{IMPORT_ID}`",
        "",
        "This document records a sanitized public-safe Project Theseus book-to-Theseus crosswalk import. It is a pointer-only implementation-reference evidence slice, not a clean live Theseus replay and not a chapter-core support-state promotion.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---:|",
        f"| Trigger state | `{valid['trigger_state']}` |",
        f"| AI-book source files in source manifest | {summary['ai_book_source_file_count']:,} |",
        f"| Public-safe pointer rows | {summary['theseus_to_book_evidence_count']} |",
        f"| Book-to-Theseus backlog cards | {summary['roadmap_backlog_item_count']} |",
        f"| Source-sync review decisions | {summary['source_sync_review_decision_count']} |",
        f"| Changed AI-book source files | {summary['changed_source_file_count']} |",
        f"| Removed AI-book source files | {summary['removed_source_file_count']} |",
        f"| Stale phases | {summary['stale_phase_count']} |",
        f"| Missing source-basis rows | {summary['missing_source_basis_count']} |",
        f"| Done phases missing evidence | {summary['done_phase_missing_evidence_count']} |",
        "",
        f"The import preserves {summary['theseus_to_book_evidence_count']} public-safe pointer rows and {summary['roadmap_backlog_item_count']} backlog cards while keeping every imported support row at pointer-only support.",
        "",
        "## Validation",
        "",
        f"- Command: `{COMMAND}`",
        f"- Result: `{rel(RESULT)}`",
        f"- Decision: `{rel(TRANSITION)}`",
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
    print(
        "Theseus book-crosswalk import validation passed: "
        f"{stats['theseus_to_book_evidence_count']} public-safe pointer rows, "
        f"{len(controls)} expected-invalid controls."
    )


if __name__ == "__main__":
    main()
