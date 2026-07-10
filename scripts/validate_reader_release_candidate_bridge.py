#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "reader_release_candidate_bridge" / "results" / "2026-07-05-local.json"
DOC = ROOT / "docs" / "reader_release_candidate_bridge.md"
RECORD = ROOT / "release_records" / "2026-07-05-v1-curated-reader-blocked-3e59bde3.json"
FORMAT_MATRIX = ROOT / "editions" / "reader_manuscript" / "v1_0" / "format_review_matrix.json"
FINAL_FIGURE_REVIEW = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "final_figure_artifact_review_manifest.json"
)
CHAPTER_RECONCILIATION = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_reconciliation_approval_manifest.json"
)
KEYBOARD_ONLY_DECISION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "keyboard_only_decision_manifest.json"
ACCESSIBILITY_TREE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_tree_manifest.json"
WCAG_PREPARATION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "wcag_preparation_manifest.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "LivingBook.lean"

COMMAND = "python3 scripts/validate_reader_release_candidate_bridge.py"
CODEX_TEST_NAME = "Reader release-candidate bridge"
PROOF_TAG = "lean:living_book.methodology.reader_release_candidate_bridge"
LEAN_THEOREMS = [
    "curated_reader_blocked_candidate_fixture_routes_to_accessibility_review",
    "local_reader_artifacts_do_not_clear_missing_accessibility_review",
    "reader_release_candidate_missing_screen_reader_routes_to_accessibility_review",
    "reader_release_candidate_missing_wcag_routes_to_accessibility_review",
    "reader_release_candidate_missing_audio_routes_to_audio_review",
    "reader_release_candidate_missing_audio_files_routes_to_audio_review",
    "reader_release_candidate_missing_chapter_markers_routes_to_audio_review",
    "reader_release_candidate_missing_approval_routes_to_release_approval",
    "reader_release_candidate_missing_reader_release_approval_routes_to_release_approval",
    "reader_release_candidate_missing_approved_record_routes_to_release_approval",
    "reader_release_candidate_support_promotion_claim_rejected",
]
REQUIRED_NON_CLAIMS = [
    "does not approve curated reader HTML, EPUB, DOCX, PDF, e-reader, audio, MP3, M4B, or audio-embedded EPUB artifacts",
    "does not publish a reader artifact to GitHub Pages or an external archive",
    "does not create a source tag, DOI, Zenodo archive, audiobook, or final reader release",
    "does not promote any chapter core claim above argument",
]

LOCAL_FORMATS = {
    "curated_reader_html",
    "curated_reader_epub",
    "curated_reader_docx",
    "curated_reader_pdf",
    "ereader_application_review",
}
ACCESSIBILITY_BLOCKERS = {
    "screen_reader_review_not_completed",
}
AUDIO_BLOCKERS = {
    "reviewed_reader_release_record_not_created_for_audio",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
}
RELEASE_APPROVAL_BLOCKERS = {"reader_release_approval_not_created"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader release-candidate bridge validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def bool_field(value: Any, field: str) -> bool:
    return isinstance(value, dict) and value.get(field) is True


def matrix_records(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    candidate = matrix.get("current_curated_candidate")
    if not isinstance(candidate, dict):
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for row in candidate.get("records", []):
        if isinstance(row, dict) and isinstance(row.get("format"), str):
            rows[row["format"]] = row
    return rows


def row_has_passed_review(row: dict[str, Any]) -> bool:
    status = str(row.get("automated_review_status", ""))
    return status.startswith("passed") or status.startswith("accepted")


def row_is_rendered(row: dict[str, Any]) -> bool:
    return str(row.get("render_status")) == "rendered_local"


def candidate_blockers(matrix: dict[str, Any]) -> set[str]:
    rows = matrix_records(matrix)
    blockers: set[str] = set()
    for row in rows.values():
        for blocker in row.get("release_blockers", []):
            if isinstance(blocker, str):
                blockers.add(blocker)
    return blockers


def actual_candidate_from_tracked_records() -> dict[str, Any]:
    record = load_json(RECORD)
    matrix = load_json(FORMAT_MATRIX)
    final_figure = load_json(FINAL_FIGURE_REVIEW)
    reconciliation = load_json(CHAPTER_RECONCILIATION)
    keyboard = load_json(KEYBOARD_ONLY_DECISION)
    accessibility_tree = load_json(ACCESSIBILITY_TREE)
    wcag_preparation = load_json(WCAG_PREPARATION)
    rows = matrix_records(matrix)
    blockers = candidate_blockers(matrix)

    for required in LOCAL_FORMATS | {"audio"}:
        if required not in rows:
            raise ValueError(f"format matrix missing current candidate row {required!r}")

    return {
        "scenario_id": "actual_current_curated_candidate_blocked_by_accessibility",
        "expect_valid": True,
        "claimed_route": "request_accessibility_review",
        "source_record": rel(RECORD),
        "source_matrix": rel(FORMAT_MATRIX),
        "release_record_validation_status": record.get("validation_status"),
        "candidate_status": matrix.get("current_curated_candidate", {}).get("status"),
        "html_rendered": row_is_rendered(rows["curated_reader_html"]),
        "epub_rendered": row_is_rendered(rows["curated_reader_epub"]),
        "docx_rendered": row_is_rendered(rows["curated_reader_docx"]),
        "pdf_rendered": row_is_rendered(rows["curated_reader_pdf"]),
        "html_browser_reviewed": row_has_passed_review(rows["curated_reader_html"]),
        "epub_application_reviewed": row_has_passed_review(rows["ereader_application_review"]),
        "docx_application_reviewed": row_has_passed_review(rows["curated_reader_docx"]),
        "pdf_page_reviewed": row_has_passed_review(rows["curated_reader_pdf"]),
        "final_figure_reviewed": final_figure.get("status")
        == "passed_final_figure_artifact_release_preparation_review",
        "chapter_reconciliation_approved": reconciliation.get("status")
        == "passed_curated_chapter_reconciliation_approval",
        "keyboard_only_reviewed": keyboard.get("status")
        == "accepted_keyboard_only_evidence_for_release_preparation",
        "accessibility_tree_reviewed": accessibility_tree.get("status")
        == "passed_accessibility_tree_release_preparation_probe",
        "screen_reader_reviewed": "screen_reader_review_not_completed" not in blockers,
        "wcag_conformance_reviewed": wcag_preparation.get("status")
        == "accepted_wcag_automation_evidence_for_release_preparation"
        and wcag_preparation.get("cleared_blockers") == ["wcag_conformance_review_not_completed"]
        and "wcag_conformance_review_not_completed" not in blockers,
        "audio_files_generated": "audio_files_not_generated" not in blockers,
        "audio_listening_reviewed": "audio_spot_check_not_performed" not in blockers,
        "chapter_markers_timecoded": "chapter_markers_not_timecoded" not in blockers,
        "audio_embedded_epub_checked": "audio_embedded_epub_not_packaged_or_checked" not in blockers,
        "audio_release_record_created": "audio_edition_release_record_not_created" not in blockers,
        "reader_release_approval_recorded": "reader_release_approval_not_created" not in blockers,
        "approved_edition_release_record_created": record.get("validation_status") == "approved",
        "chapter_support_promotion_claimed": False,
        "non_claims_recorded": bool(record.get("non_claims")),
        "release_blockers_recorded": bool(blockers),
        "release_approved_rows": [
            row.get("format")
            for row in rows.values()
            if row.get("release_approved") is True or str(row.get("release_approved")).lower() == "yes"
        ],
        "release_blockers": sorted(blockers),
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claims": record.get("non_claims", []),
    }


def scenario(
    scenario_id: str,
    *,
    expect_valid: bool,
    claimed_route: str,
    local_complete: bool = True,
    accessibility_complete: bool = True,
    audio_complete: bool = True,
    approval_complete: bool = True,
    support_promotion: bool = False,
    non_claims: bool = True,
    blockers_recorded: bool = True,
) -> dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "expect_valid": expect_valid,
        "claimed_route": claimed_route,
        "source_record": "synthetic://reader-release-candidate-bridge",
        "source_matrix": "synthetic://reader-release-candidate-bridge",
        "release_record_validation_status": "synthetic",
        "candidate_status": "synthetic",
        "html_rendered": local_complete,
        "epub_rendered": local_complete,
        "docx_rendered": local_complete,
        "pdf_rendered": local_complete,
        "html_browser_reviewed": local_complete,
        "epub_application_reviewed": local_complete,
        "docx_application_reviewed": local_complete,
        "pdf_page_reviewed": local_complete,
        "final_figure_reviewed": local_complete,
        "chapter_reconciliation_approved": local_complete,
        "keyboard_only_reviewed": local_complete,
        "accessibility_tree_reviewed": local_complete,
        "screen_reader_reviewed": accessibility_complete,
        "wcag_conformance_reviewed": accessibility_complete,
        "audio_files_generated": audio_complete,
        "audio_listening_reviewed": audio_complete,
        "chapter_markers_timecoded": audio_complete,
        "audio_embedded_epub_checked": audio_complete,
        "audio_release_record_created": audio_complete,
        "reader_release_approval_recorded": approval_complete,
        "approved_edition_release_record_created": approval_complete,
        "chapter_support_promotion_claimed": support_promotion,
        "non_claims_recorded": non_claims,
        "release_blockers_recorded": blockers_recorded,
        "release_approved_rows": [],
        "release_blockers": [],
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS if non_claims else [],
    }


def local_review_complete(record: dict[str, Any]) -> bool:
    return all(
        bool_field(record, field)
        for field in (
            "html_rendered",
            "epub_rendered",
            "docx_rendered",
            "pdf_rendered",
            "html_browser_reviewed",
            "epub_application_reviewed",
            "docx_application_reviewed",
            "pdf_page_reviewed",
            "final_figure_reviewed",
            "chapter_reconciliation_approved",
            "keyboard_only_reviewed",
            "accessibility_tree_reviewed",
            "non_claims_recorded",
            "release_blockers_recorded",
        )
    )


def accessibility_complete(record: dict[str, Any]) -> bool:
    return bool_field(record, "screen_reader_reviewed") and bool_field(record, "wcag_conformance_reviewed")


def audio_complete(record: dict[str, Any]) -> bool:
    return all(
        bool_field(record, field)
        for field in (
            "audio_files_generated",
            "audio_listening_reviewed",
            "chapter_markers_timecoded",
            "audio_embedded_epub_checked",
            "audio_release_record_created",
        )
    )


def approval_complete(record: dict[str, Any]) -> bool:
    return bool_field(record, "reader_release_approval_recorded") and bool_field(
        record, "approved_edition_release_record_created"
    )


def route_for(record: dict[str, Any]) -> str:
    if bool_field(record, "chapter_support_promotion_claimed"):
        return "reject_support_promotion"
    if not local_review_complete(record):
        return "request_artifact_review"
    if not accessibility_complete(record):
        return "request_accessibility_review"
    if not audio_complete(record):
        return "request_audio_artifact_review"
    if not approval_complete(record):
        return "request_release_approval"
    return "approve_release"


def scenario_with_updates(record: dict[str, Any], **updates: Any) -> dict[str, Any]:
    cloned = json.loads(json.dumps(record))
    cloned.update(updates)
    return cloned


def scenario_rejection_reasons(record: dict[str, Any], actual_route: str) -> list[str]:
    reasons: list[str] = []
    claimed_route = str(record.get("claimed_route", ""))
    if claimed_route != actual_route:
        reasons.append(f"claimed_{claimed_route}_but_route_is_{actual_route}")
    if claimed_route == "approve_release" and record.get("release_blockers"):
        reasons.append("claimed_approval_has_release_blockers")
    if record.get("release_approved_rows"):
        reasons.append("release_approved_rows_present_in_blocked_candidate")
    if record.get("support_state_effect") != "none":
        reasons.append("support_state_effect_not_none")
    if record.get("chapter_core_support_effect") != "none":
        reasons.append("chapter_core_support_effect_not_none")
    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            reasons.append(f"missing_non_claim:{phrase}")
    if actual_route == "approve_release" and record.get("release_blockers"):
        reasons.append("approved_route_has_release_blockers")
    return sorted(set(reasons))


def build_result(errors: list[str]) -> dict[str, Any]:
    try:
        actual = actual_candidate_from_tracked_records()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        actual = scenario(
            "actual_current_curated_candidate_blocked_by_accessibility",
            expect_valid=False,
            claimed_route="request_artifact_review",
            local_complete=False,
        )

    scenarios = [
        actual,
        scenario(
            "synthetic_accessibility_done_audio_missing",
            expect_valid=True,
            claimed_route="request_audio_artifact_review",
            audio_complete=False,
            approval_complete=False,
        ),
        scenario(
            "synthetic_audio_done_release_approval_missing",
            expect_valid=True,
            claimed_route="request_release_approval",
            approval_complete=False,
        ),
        scenario("synthetic_all_release_gates_done", expect_valid=True, claimed_route="approve_release"),
        scenario_with_updates(
            actual,
            scenario_id="invalid_current_candidate_claimed_approved",
            expect_valid=False,
            claimed_route="approve_release",
        ),
        scenario_with_updates(
            scenario(
                "invalid_screen_reader_missing_claimed_approved",
                expect_valid=False,
                claimed_route="approve_release",
            ),
            screen_reader_reviewed=False,
            release_blockers=["screen_reader_review_not_completed"],
        ),
        scenario_with_updates(
            scenario(
                "invalid_wcag_conformance_missing_claimed_approved",
                expect_valid=False,
                claimed_route="approve_release",
            ),
            wcag_conformance_reviewed=False,
            release_blockers=["wcag_conformance_review_not_completed"],
        ),
        scenario(
            "invalid_audio_missing_claimed_approved",
            expect_valid=False,
            claimed_route="approve_release",
            audio_complete=False,
        ),
        scenario_with_updates(
            scenario(
                "invalid_audio_files_missing_claimed_approved",
                expect_valid=False,
                claimed_route="approve_release",
            ),
            audio_files_generated=False,
            release_blockers=["audio_files_not_generated"],
        ),
        scenario_with_updates(
            scenario(
                "invalid_chapter_markers_missing_claimed_approved",
                expect_valid=False,
                claimed_route="approve_release",
            ),
            chapter_markers_timecoded=False,
            release_blockers=["chapter_markers_not_timecoded"],
        ),
        scenario(
            "invalid_release_approval_missing_claimed_approved",
            expect_valid=False,
            claimed_route="approve_release",
            approval_complete=False,
        ),
        scenario_with_updates(
            scenario(
                "invalid_reader_release_approval_missing_claimed_approved",
                expect_valid=False,
                claimed_route="approve_release",
            ),
            reader_release_approval_recorded=False,
            release_blockers=["reader_release_approval_not_created"],
        ),
        scenario_with_updates(
            scenario(
                "invalid_approved_release_record_missing_claimed_approved",
                expect_valid=False,
                claimed_route="approve_release",
            ),
            approved_edition_release_record_created=False,
            release_blockers=["approved_edition_release_record_not_created"],
        ),
        scenario(
            "invalid_support_promotion_claimed",
            expect_valid=False,
            claimed_route="approve_release",
            support_promotion=True,
        ),
        scenario(
            "invalid_missing_non_claims_claimed_approved",
            expect_valid=False,
            claimed_route="approve_release",
            non_claims=False,
        ),
    ]

    rows: list[dict[str, Any]] = []
    valid_scenarios: list[str] = []
    rejected_controls: list[dict[str, Any]] = []
    for record in scenarios:
        actual_route = route_for(record)
        reasons = scenario_rejection_reasons(record, actual_route)
        actual_valid = not reasons
        expected_valid = record.get("expect_valid") is True
        scenario_id = str(record.get("scenario_id"))
        if expected_valid and not actual_valid:
            errors.append(f"{scenario_id}: expected valid but rejected: {', '.join(reasons)}")
        if not expected_valid and actual_valid:
            errors.append(f"{scenario_id}: expected invalid but no rejection reason was produced.")
        row = {
            "scenario_id": scenario_id,
            "expected_valid": expected_valid,
            "actual_valid": actual_valid,
            "claimed_route": record.get("claimed_route"),
            "actual_route": actual_route,
            "local_review_complete": local_review_complete(record),
            "accessibility_complete": accessibility_complete(record),
            "audio_complete": audio_complete(record),
            "approval_complete": approval_complete(record),
            "release_blockers": record.get("release_blockers", []),
            "rejection_reasons": reasons,
        }
        rows.append(row)
        if expected_valid:
            valid_scenarios.append(scenario_id)
        else:
            rejected_controls.append({"scenario_id": scenario_id, "rejection_reasons": reasons})

    actual_row = next(
        row for row in rows if row["scenario_id"] == "actual_current_curated_candidate_blocked_by_accessibility"
    )
    assertions = {
        "actual_candidate_local_review_complete": actual_row["local_review_complete"] is True,
        "actual_candidate_routes_to_accessibility_review": actual_row["actual_route"]
        == "request_accessibility_review",
        "actual_candidate_not_approved": actual_row["actual_route"] != "approve_release",
        "accessibility_blockers_visible": ACCESSIBILITY_BLOCKERS.issubset(set(actual_row["release_blockers"])),
        "audio_blockers_visible": AUDIO_BLOCKERS.issubset(set(actual_row["release_blockers"])),
        "release_approval_blockers_visible": RELEASE_APPROVAL_BLOCKERS.issubset(set(actual_row["release_blockers"])),
        "audio_gate_required_after_accessibility": any(
            row["scenario_id"] == "synthetic_accessibility_done_audio_missing"
            and row["actual_route"] == "request_audio_artifact_review"
            for row in rows
        ),
        "release_approval_required_after_audio": any(
            row["scenario_id"] == "synthetic_audio_done_release_approval_missing"
            and row["actual_route"] == "request_release_approval"
            for row in rows
        ),
        "support_promotion_rejected": any(
            row["scenario_id"] == "invalid_support_promotion_claimed"
            and row["actual_route"] == "reject_support_promotion"
            for row in rows
        ),
        "invalid_current_candidate_preserves_visible_blockers": any(
            row["scenario_id"] == "invalid_current_candidate_claimed_approved"
            and ACCESSIBILITY_BLOCKERS.issubset(set(row["release_blockers"]))
            and AUDIO_BLOCKERS.issubset(set(row["release_blockers"]))
            and RELEASE_APPROVAL_BLOCKERS.issubset(set(row["release_blockers"]))
            for row in rows
        ),
        "field_specific_accessibility_controls_rejected": all(
            any(
                row["scenario_id"] == scenario_id
                and row["actual_route"] == "request_accessibility_review"
                and row["actual_valid"] is False
                for row in rows
            )
            for scenario_id in (
                "invalid_screen_reader_missing_claimed_approved",
                "invalid_wcag_conformance_missing_claimed_approved",
            )
        ),
        "field_specific_audio_controls_rejected": all(
            any(
                row["scenario_id"] == scenario_id
                and row["actual_route"] == "request_audio_artifact_review"
                and row["actual_valid"] is False
                for row in rows
            )
            for scenario_id in (
                "invalid_audio_files_missing_claimed_approved",
                "invalid_chapter_markers_missing_claimed_approved",
            )
        ),
        "field_specific_approval_controls_rejected": all(
            any(
                row["scenario_id"] == scenario_id
                and row["actual_route"] == "request_release_approval"
                and row["actual_valid"] is False
                for row in rows
            )
            for scenario_id in (
                "invalid_reader_release_approval_missing_claimed_approved",
                "invalid_approved_release_record_missing_claimed_approved",
            )
        ),
        "no_chapter_core_support_effect": all(
            scenario.get("chapter_core_support_effect") == "none" for scenario in scenarios
        ),
    }
    for key, value in assertions.items():
        if value is not True:
            errors.append(f"bridge_assertions.{key} must be true.")

    return {
        "schema_version": "asi_stack.reader_release_candidate_bridge.v0",
        "result_id": "2026-07-05-reader-release-candidate-bridge",
        "recorded_date": "2026-07-05",
        "command": COMMAND,
        "result_kind": "deterministic_reader_release_candidate_route_bridge",
        "valid_scenario_count": len(valid_scenarios),
        "expected_invalid_control_count": len(rejected_controls),
        "valid_scenarios": sorted(valid_scenarios),
        "rejected_controls": rejected_controls,
        "scenario_results": rows,
        "actual_candidate_sources": {
            "release_record": rel(RECORD),
            "format_matrix": rel(FORMAT_MATRIX),
            "final_figure_review": rel(FINAL_FIGURE_REVIEW),
            "chapter_reconciliation": rel(CHAPTER_RECONCILIATION),
            "keyboard_only_decision": rel(KEYBOARD_ONLY_DECISION),
            "accessibility_tree": rel(ACCESSIBILITY_TREE),
            "wcag_preparation": rel(WCAG_PREPARATION),
        },
        "bridge_assertions": assertions,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.LivingBook",
            "proof_tag": PROOF_TAG,
            "theorem_refs": LEAN_THEOREMS,
            "expected": {
                "actual_candidate_route": "request_accessibility_review",
                "audio_missing_route": "request_audio_artifact_review",
                "approval_missing_route": "request_release_approval",
                "support_promotion_route": "reject_support_promotion",
            },
        },
        "weakening_condition": (
            "The reader-release boundary weakens if local format evidence, "
            "keyboard/accessibility-tree/WCAG-preparation probes, application smoke checks, or "
            "audio-script metadata can be converted into release approval while "
            "screen-reader, audio artifact, timecoding, and explicit "
            "reader-release approval blockers remain."
        ),
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_record(record: dict[str, Any], errors: list[str]) -> None:
    if record.get("schema_version") != "asi_stack.reader_release_candidate_bridge.v0":
        errors.append(f"{rel(RESULT)} schema_version mismatch.")
    if record.get("result_id") != "2026-07-05-reader-release-candidate-bridge":
        errors.append(f"{rel(RESULT)} result_id mismatch.")
    if record.get("recorded_date") != "2026-07-05":
        errors.append(f"{rel(RESULT)} recorded_date mismatch.")
    if record.get("command") != COMMAND:
        errors.append(f"{rel(RESULT)} command mismatch.")
    if record.get("valid_scenario_count") != 4:
        errors.append(f"{rel(RESULT)} valid_scenario_count must be 4.")
    if record.get("expected_invalid_control_count") != 11:
        errors.append(f"{rel(RESULT)} expected_invalid_control_count must be 11.")
    assertions = record.get("bridge_assertions")
    if not isinstance(assertions, dict) or not all(value is True for value in assertions.values()):
        errors.append(f"{rel(RESULT)} bridge_assertions must all be true.")
    alignment = record.get("lean_fixture_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)} lean_fixture_alignment must be an object.")
    else:
        if alignment.get("proof_tag") != PROOF_TAG:
            errors.append(f"{rel(RESULT)} lean proof tag mismatch.")
        if alignment.get("theorem_refs") != LEAN_THEOREMS:
            errors.append(f"{rel(RESULT)} theorem refs mismatch.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    non_claim_text = text_blob(record.get("non_claims"))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def require_text(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"{rel(path)} missing.")
        return
    text = path.read_text(encoding="utf-8")
    normalized = " ".join(text.lower().split())
    for phrase in phrases:
        if " ".join(phrase.lower().split()) not in normalized:
            errors.append(f"{rel(path)} missing required phrase: {phrase}")


def validate_surfaces(errors: list[str]) -> None:
    require_text(
        LEAN_FILE,
        [
            "ReaderReleaseCandidateReview",
            "curatedReaderBlockedCandidateFixture",
            *LEAN_THEOREMS,
        ],
        errors,
    )
    require_text(
        DOC,
        [
            "Reader Release-Candidate Bridge",
            COMMAND,
            "actual_current_curated_candidate_blocked_by_accessibility",
            "request_accessibility_review",
            "invalid_current_candidate_claimed_approved",
            "invalid_screen_reader_missing_claimed_approved",
            "invalid_wcag_conformance_missing_claimed_approved",
            "invalid_audio_files_missing_claimed_approved",
            "invalid_chapter_markers_missing_claimed_approved",
            "invalid_reader_release_approval_missing_claimed_approved",
            "invalid_approved_release_record_missing_claimed_approved",
            "does not approve curated reader HTML, EPUB, DOCX, PDF, e-reader, audio",
        ],
        errors,
    )
    require_text(
        OUTLINE,
        [
            CODEX_TEST_NAME,
            COMMAND,
            PROOF_TAG,
            "local reader artifacts cannot clear missing accessibility, audio, or release-approval blockers",
        ],
        errors,
    )
    require_text(
        ROADMAP,
        [
            "reader release-candidate bridge",
            "local format evidence",
            "screen-reader",
        ],
        errors,
    )
    require_text(
        CHANGELOG,
        [
            "Reader release-candidate bridge",
            COMMAND,
            PROOF_TAG,
        ],
        errors,
    )
    require_text(
        VALIDATION_REGISTRY,
        [
            "scripts/validate_reader_release_candidate_bridge.py",
            "docs/reader_release_candidate_bridge.md",
            "experiments/reader_release_candidate_bridge/results/2026-07-05-local.json",
            '"script": "validate_reader_release_candidate_bridge.py"',
        ],
        errors,
    )
    manifest = load_json(MANIFEST)
    manifest_text = text_blob(manifest)
    for phrase in [CODEX_TEST_NAME.lower(), PROOF_TAG.lower(), COMMAND.lower()]:
        if phrase not in manifest_text:
            errors.append(f"{rel(MANIFEST)} missing {phrase}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    built = build_result(errors)
    if errors:
        fail(errors)
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not RESULT.exists():
        errors.append(f"{rel(RESULT)} missing; run {COMMAND} --write-result.")
    else:
        recorded = load_json(RESULT)
        validate_record(recorded, errors)
        if recorded != built:
            errors.append(f"{rel(RESULT)} is stale; rerun {COMMAND} --write-result.")

    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Reader release-candidate bridge validation passed.")


if __name__ == "__main__":
    main()
