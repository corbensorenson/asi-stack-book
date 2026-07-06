#!/usr/bin/env python3
"""Validate the curated-reader audio script narration-treatment review."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_narration_treatment_review_manifest.json"
DOC = ROOT / "docs" / "reader_audio_narration_treatment_review.md"
AUDIO_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
KEY_FIGURE_COMPANION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "companion_notes" / "key-figures.md"

EXPECTED_STATUS = "accepted_audio_script_narration_treatment_for_release_preparation"
EXPECTED_CLEARED = ["narration_quality_review_not_completed"]
EXPECTED_PRESERVED = [
    "reviewed_reader_release_record_not_created_for_audio",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_metadata_not_reviewed",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
]
EXPECTED_TARGET_STATUS = {
    "mp3": "target_not_generated",
    "m4b": "target_not_generated",
    "audio-embedded-epub": "target_not_generated",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader audio narration-treatment validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_dict(owner: str, value: Any, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{owner} must be an object.")
        return {}
    return value


def require_text(owner: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner} must contain at least {min_words} words.")
    return value


def validate() -> list[str]:
    errors: list[str] = []
    for path in (MANIFEST, DOC, AUDIO_PROBE, KEY_FIGURE_COMPANION):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return errors

    manifest = require_dict(rel(MANIFEST), load_json(MANIFEST), errors)
    audio_probe = require_dict(rel(AUDIO_PROBE), load_json(AUDIO_PROBE), errors)
    reading_flow = require_dict(
        "audio_probe.audio_script_reading_flow_review",
        audio_probe.get("audio_script_reading_flow_review"),
        errors,
    )
    key_figure_note = require_dict("audio_probe.key_figure_companion_note", audio_probe.get("key_figure_companion_note"), errors)
    doc_text = DOC.read_text(encoding="utf-8")
    companion_text = KEY_FIGURE_COMPANION.read_text(encoding="utf-8")

    if manifest.get("schema_version") != "asi_stack.reader_audio_narration_treatment_review.v0":
        errors.append("schema_version must be asi_stack.reader_audio_narration_treatment_review.v0.")
    if manifest.get("status") != EXPECTED_STATUS:
        errors.append(f"status must be {EXPECTED_STATUS}.")
    if manifest.get("decision_date") != "2026-07-05":
        errors.append("decision_date must remain 2026-07-05 for this recorded review.")
    if manifest.get("source_audio_probe_manifest") != rel(AUDIO_PROBE):
        errors.append("source_audio_probe_manifest must point to the tracked audio probe manifest.")
    if manifest.get("key_figure_companion_note") != rel(KEY_FIGURE_COMPANION):
        errors.append("key_figure_companion_note must point to the tracked key-figure companion note.")

    expected_top_level = {
        "reading_flow_status": reading_flow.get("status"),
        "combined_script_sha256": reading_flow.get("combined_script_sha256"),
        "script_files_checked": reading_flow.get("script_files_checked"),
        "chapter_scripts_checked": reading_flow.get("chapter_scripts_checked"),
        "appendix_scripts_checked": reading_flow.get("appendix_scripts_checked"),
        "chapter_marker_rows": reading_flow.get("chapter_marker_rows"),
        "chapter_marker_tbd_rows": reading_flow.get("chapter_marker_tbd_rows"),
        "narration_note_count": reading_flow.get("narration_note_count"),
        "text_characters_checked": reading_flow.get("text_characters_checked"),
        "word_tokens_checked": reading_flow.get("word_tokens_checked"),
        "live_marker_hits": reading_flow.get("live_marker_hits"),
        "raw_core_claim_marker_hits": reading_flow.get("raw_core_claim_marker_hits"),
        "replacement_character_count": reading_flow.get("replacement_character_count"),
        "target_artifact_status": EXPECTED_TARGET_STATUS,
        "key_figure_spoken_summaries": key_figure_note.get("figure_count"),
    }
    for key, expected in expected_top_level.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must be {expected!r}; found {manifest.get(key)!r}.")

    expected_exact = {
        "reading_flow_status": "passed_audio_script_reading_flow_review",
        "script_files_checked": 49,
        "chapter_scripts_checked": 44,
        "appendix_scripts_checked": 3,
        "chapter_marker_rows": 49,
        "chapter_marker_tbd_rows": 49,
        "narration_note_count": 66,
        "text_characters_checked": 1095099,
        "word_tokens_checked": 146737,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
        "replacement_character_count": 0,
        "key_figure_spoken_summaries": 10,
    }
    for key, expected in expected_exact.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must remain {expected!r}; found {manifest.get(key)!r}.")

    treatment_totals = require_dict("companion_treatment_totals", manifest.get("companion_treatment_totals"), errors)
    if treatment_totals != reading_flow.get("companion_treatment_totals"):
        errors.append("companion_treatment_totals must match the audio reading-flow review.")
    if treatment_totals != {"tables": 5, "mermaid_diagrams": 50, "code_or_schema_blocks": 0, "images": 11}:
        errors.append("companion_treatment_totals drifted from the tracked narration-note counts.")

    if "## Audio Treatment" not in companion_text:
        errors.append("key-figure companion note must contain an Audio Treatment section.")
    if companion_text.count("| `assets/diagrams/") < 10:
        errors.append("key-figure companion note must keep ten draft spoken-summary rows.")
    if "This does not approve any reader release" not in companion_text:
        errors.append("key-figure companion note must preserve release non-claim boundary.")

    if manifest.get("cleared_blockers") != EXPECTED_CLEARED:
        errors.append(f"cleared_blockers must be {EXPECTED_CLEARED}.")
    if manifest.get("preserved_blockers") != EXPECTED_PRESERVED:
        errors.append(f"preserved_blockers must be {EXPECTED_PRESERVED}.")

    decision = require_text("decision", manifest.get("decision"), errors, min_words=30)
    for fragment in (
        "script-level narration treatment",
        "clears only `narration_quality_review_not_completed`",
        "does not approve pronunciation",
        "does not approve recorded audio",
        "does not timecode chapter markers",
    ):
        if fragment not in decision:
            errors.append(f"decision missing required fragment: {fragment!r}.")

    boundary = require_text("release_boundary", manifest.get("release_boundary"), errors, min_words=30)
    for fragment in (
        "clears only `narration_quality_review_not_completed`",
        "does not create MP3, M4B, or audio-embedded EPUB artifacts",
        "does not approve an audiobook",
        "does not create an audio edition release record",
        "does not promote any claim support state",
    ):
        if fragment not in boundary:
            errors.append(f"release_boundary missing required fragment: {fragment!r}.")

    non_claim_text = " ".join(str(item) for item in manifest.get("non_claims", [])).lower()
    for phrase in (
        "does not approve pronunciation quality",
        "does not approve recorded audio",
        "does not create mp3",
        "does not timecode chapter markers",
        "does not approve an audiobook",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")

    for fragment in (
        "Reader Audio Narration Treatment Review",
        EXPECTED_STATUS,
        "script-level narration treatment",
        "clears only `narration_quality_review_not_completed`",
        "66 narration notes",
        "1,093,838 text characters",
        "10 draft key-figure spoken summaries",
        "does not approve pronunciation",
        "does not create MP3, M4B, or audio-embedded EPUB artifacts",
        "does not approve an audiobook",
    ):
        if fragment not in doc_text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")

    return errors


def main() -> None:
    errors = validate()
    if errors:
        fail(errors)
    print("Reader audio narration-treatment validation passed.")


if __name__ == "__main__":
    main()
