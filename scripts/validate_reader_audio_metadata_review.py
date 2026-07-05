#!/usr/bin/env python3
"""Validate the curated-reader audio metadata release-preparation review."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_metadata_review_manifest.json"
DOC = ROOT / "docs" / "reader_audio_metadata_review.md"
AUDIO_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
RELEASE_PROFILES = ROOT / "editions" / "release_profiles.json"
BLOCKED_RECORD = ROOT / "release_records" / "2026-07-05-v1-curated-reader-blocked-3e59bde3.json"

EXPECTED_STATUS = "accepted_audio_metadata_for_release_preparation"
EXPECTED_RELEASE_ID = "2026-07-05-v1-curated-reader-blocked-3e59bde3"
EXPECTED_SOURCE_COMMIT = "3e59bde35f4aa5147017ddab3159cfeffddc9ee7"
EXPECTED_SOURCE_TAG = "not_tagged_curated_reader_blocked_candidate_2026-07-05"
EXPECTED_SCRIPT_DIGEST = "66d78ff80b2b2577782fdfd41a59ba43c07179095b43a2dc3ca82de5d9938f2e"
EXPECTED_CLEARED = ["audio_metadata_not_reviewed"]
EXPECTED_PRESERVED = [
    "reviewed_reader_release_record_not_created_for_audio",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
]
EXPECTED_PROFILE_REQUIREMENTS = [
    "title",
    "major version",
    "source tag or commit",
    "narrator/tooling note",
    "license or rights statement",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader audio metadata review validation failed:")
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


def audio_profile(release_profiles: dict[str, Any]) -> dict[str, Any]:
    profiles = release_profiles.get("profiles", [])
    if not isinstance(profiles, list):
        return {}
    for profile in profiles:
        if isinstance(profile, dict) and profile.get("id") == "audio_release":
            return profile
    return {}


def validate() -> list[str]:
    errors: list[str] = []
    for path in (MANIFEST, DOC, AUDIO_PROBE, RELEASE_PROFILES, BLOCKED_RECORD):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return errors

    manifest = require_dict(rel(MANIFEST), load_json(MANIFEST), errors)
    audio_probe = require_dict(rel(AUDIO_PROBE), load_json(AUDIO_PROBE), errors)
    release_profiles = require_dict(rel(RELEASE_PROFILES), load_json(RELEASE_PROFILES), errors)
    blocked_record = require_dict(rel(BLOCKED_RECORD), load_json(BLOCKED_RECORD), errors)
    reading_flow = require_dict(
        "audio_probe.audio_script_reading_flow_review",
        audio_probe.get("audio_script_reading_flow_review"),
        errors,
    )
    profile = audio_profile(release_profiles)
    if not profile:
        errors.append("editions/release_profiles.json must contain the audio_release profile.")
        profile = {}
    metadata = require_dict("metadata_fields", manifest.get("metadata_fields"), errors)
    doc_text = DOC.read_text(encoding="utf-8")

    if manifest.get("schema_version") != "asi_stack.reader_audio_metadata_review.v0":
        errors.append("schema_version must be asi_stack.reader_audio_metadata_review.v0.")
    if manifest.get("status") != EXPECTED_STATUS:
        errors.append(f"status must be {EXPECTED_STATUS}.")
    if manifest.get("decision_date") != "2026-07-05":
        errors.append("decision_date must remain 2026-07-05 for this recorded review.")
    if manifest.get("source_audio_probe_manifest") != rel(AUDIO_PROBE):
        errors.append("source_audio_probe_manifest must point to the tracked audio probe manifest.")
    if manifest.get("source_release_profiles") != rel(RELEASE_PROFILES):
        errors.append("source_release_profiles must point to editions/release_profiles.json.")
    if manifest.get("source_blocked_release_record") != rel(BLOCKED_RECORD):
        errors.append("source_blocked_release_record must point to the active blocked record.")
    if manifest.get("source_candidate_release_id") != EXPECTED_RELEASE_ID:
        errors.append("source_candidate_release_id drifted.")
    if blocked_record.get("release_id") != EXPECTED_RELEASE_ID:
        errors.append("blocked release record release_id drifted.")
    if manifest.get("source_candidate_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append("source_candidate_commit drifted.")
    if metadata.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append("metadata_fields.source_commit drifted.")
    if manifest.get("source_candidate_tag") != EXPECTED_SOURCE_TAG:
        errors.append("source_candidate_tag drifted.")
    if metadata.get("source_tag") != EXPECTED_SOURCE_TAG:
        errors.append("metadata_fields.source_tag drifted.")

    expected_top_level = {
        "source_audio_script_sha256": reading_flow.get("combined_script_sha256"),
        "script_files_checked": reading_flow.get("script_files_checked"),
        "chapter_scripts_checked": reading_flow.get("chapter_scripts_checked"),
        "chapter_marker_rows": reading_flow.get("chapter_marker_rows"),
        "audio_profile": "audio_release",
    }
    for key, expected in expected_top_level.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must be {expected!r}; found {manifest.get(key)!r}.")
    if manifest.get("source_audio_script_sha256") != EXPECTED_SCRIPT_DIGEST:
        errors.append("source_audio_script_sha256 drifted from the reviewed script digest.")
    if metadata.get("script_digest") != EXPECTED_SCRIPT_DIGEST:
        errors.append("metadata_fields.script_digest drifted from the reviewed script digest.")

    expected_metadata = {
        "title": "The ASI Stack",
        "subtitle": "A Systems Architecture for Governed, Efficient, Self-Improving AI",
        "author": "Corben Sorenson",
        "major_version": "v1.0",
        "language": "en-US",
    }
    for key, expected in expected_metadata.items():
        if metadata.get(key) != expected:
            errors.append(f"metadata_fields.{key} must be {expected!r}; found {metadata.get(key)!r}.")

    narrator_note = require_text("metadata_fields.narrator_or_tooling_note", metadata.get("narrator_or_tooling_note"), errors, min_words=12)
    rights = require_text("metadata_fields.rights_statement", metadata.get("rights_statement"), errors, min_words=12)
    if "No narrator or synthesis tooling is approved yet" not in narrator_note:
        errors.append("narrator_or_tooling_note must preserve the no-approved-narrator boundary.")
    if "no audio publication or distribution approval exists" not in rights:
        errors.append("rights_statement must preserve the no-publication-approval boundary.")

    if manifest.get("profile_requirements_checked") != EXPECTED_PROFILE_REQUIREMENTS:
        errors.append("profile_requirements_checked drifted from the release-profile metadata rule.")
    audio_checks = " ".join(str(item) for item in profile.get("release_gate", []) + release_profiles.get("audio_manuscript_policy", {}).get("audio_packaging_checks", []))
    for phrase in ("chapter markers and metadata are verified", "Audio metadata includes title", "source tag or commit", "license or rights statement"):
        if phrase not in audio_checks:
            errors.append(f"release profile audio metadata requirement missing phrase: {phrase}")

    if manifest.get("cleared_blockers") != EXPECTED_CLEARED:
        errors.append(f"cleared_blockers must be {EXPECTED_CLEARED}.")
    if manifest.get("preserved_blockers") != EXPECTED_PRESERVED:
        errors.append(f"preserved_blockers must be {EXPECTED_PRESERVED}.")

    decision = require_text("decision", manifest.get("decision"), errors, min_words=35)
    for fragment in (
        "clears only `audio_metadata_not_reviewed`",
        "no narrator",
        "audio artifact",
        "distribution right",
        "audio release approval",
    ):
        if fragment not in decision:
            errors.append(f"decision missing required fragment: {fragment!r}.")
    boundary = require_text("release_boundary", manifest.get("release_boundary"), errors, min_words=35)
    for fragment in (
        "clears only `audio_metadata_not_reviewed`",
        "does not create MP3, M4B, or audio-embedded EPUB artifacts",
        "does not approve a narrator or synthesis tool",
        "does not timecode chapter markers",
        "does not perform a pronunciation or listening spot check",
        "does not approve audio publication rights",
        "does not create an audio edition release record",
        "does not promote any claim support state",
    ):
        if fragment not in boundary:
            errors.append(f"release_boundary missing required fragment: {fragment!r}.")
    non_claim_text = " ".join(str(item) for item in manifest.get("non_claims", [])).lower()
    for phrase in (
        "does not create mp3",
        "does not approve a narrator",
        "does not timecode chapter markers",
        "does not approve audio publication",
        "does not approve an audiobook",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")

    for fragment in (
        "Reader Audio Metadata Review",
        EXPECTED_STATUS,
        "clears only `audio_metadata_not_reviewed`",
        "Source candidate | `2026-07-05-v1-curated-reader-blocked-3e59bde3`",
        "Audio script digest | `66d78ff80b2b2577782fdfd41a59ba43c07179095b43a2dc3ca82de5d9938f2e`",
        "Script files checked | 49",
        "Chapter-marker rows | 49",
        "does not create MP3",
        "does not approve a narrator or synthesis",
        "does not approve an audiobook",
    ):
        if fragment not in doc_text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")

    return errors


def main() -> None:
    errors = validate()
    if errors:
        fail(errors)
    print("Reader audio metadata review validation passed.")


if __name__ == "__main__":
    main()
