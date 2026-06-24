#!/usr/bin/env python3
"""Validate audience-specific edition profile metadata."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "editions" / "release_profiles.json"

REQUIRED_AUDIENCES = {"ai_agents", "human_researchers", "interested_humans"}
REQUIRED_PROFILES = {"live_book", "research_release", "reader_release", "audio_release"}
READER_REQUIRED_STRIPS = {
    (2, "chapter status"),
    (2, "drafting guardrail"),
    (2, "codex test plan"),
    (2, "source crosswalk"),
    (2, "formalization hooks"),
    (3, "claim-source mapping status"),
    (3, "formalization hooks"),
}


def fail(errors: list[str]) -> None:
    for error in errors:
        print(error)
    sys.exit(1)


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def normalized_strip_set(profile: dict) -> set[tuple[int, str]]:
    records = profile.get("strip_headings", [])
    result: set[tuple[int, str]] = set()
    if not isinstance(records, list):
        return result
    for record in records:
        if not isinstance(record, dict):
            continue
        result.add((int(record.get("level", 0)), str(record.get("title", "")).strip().lower()))
    return result


def validate_path_list(profile_id: str, key: str, values: object, errors: list[str]) -> None:
    if not isinstance(values, list):
        errors.append(f"{profile_id}: {key} must be a list.")
        return
    for value in values:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{profile_id}: {key} entries must be non-empty strings.")
            continue
        if value.endswith(".qmd") and not (ROOT / value).exists():
            errors.append(f"{profile_id}: referenced appendix does not exist: {value}")


def main() -> None:
    errors: list[str] = []
    data = load_json(PROFILES_PATH)
    if not isinstance(data, dict):
        fail(["editions/release_profiles.json must contain an object."])

    if data.get("schema_version") != "0.1":
        errors.append("release profile schema_version must be 0.1.")

    audiences = data.get("audiences")
    if not isinstance(audiences, list):
        errors.append("audiences must be a list.")
        audience_ids: set[str] = set()
    else:
        audience_ids = {
            str(record.get("id", ""))
            for record in audiences
            if isinstance(record, dict)
        }
        missing_audiences = REQUIRED_AUDIENCES - audience_ids
        if missing_audiences:
            errors.append(f"Missing required audiences: {sorted(missing_audiences)}")

    profiles = data.get("profiles")
    if not isinstance(profiles, list):
        fail(errors + ["profiles must be a list."])

    profile_ids: set[str] = set()
    for profile in profiles:
        if not isinstance(profile, dict):
            errors.append("Every profile must be an object.")
            continue
        profile_id = str(profile.get("id", ""))
        if not profile_id:
            errors.append("Every profile needs an id.")
            continue
        if profile_id in profile_ids:
            errors.append(f"Duplicate profile id: {profile_id}")
        profile_ids.add(profile_id)

        for key in ("label", "purpose", "source_policy"):
            if not isinstance(profile.get(key), str) or not profile[key].strip():
                errors.append(f"{profile_id}: missing non-empty {key}.")

        validate_path_list(profile_id, "publication_formats", profile.get("publication_formats"), errors)
        validate_path_list(profile_id, "include_appendices", profile.get("include_appendices"), errors)
        validate_path_list(profile_id, "release_gate", profile.get("release_gate"), errors)
        validate_path_list(profile_id, "non_claims", profile.get("non_claims"), errors)

        primary_audiences = profile.get("primary_audiences")
        if not isinstance(primary_audiences, list) or not primary_audiences:
            errors.append(f"{profile_id}: primary_audiences must be a non-empty list.")
        else:
            unknown = sorted(set(primary_audiences) - audience_ids)
            if unknown:
                errors.append(f"{profile_id}: unknown primary audiences: {unknown}")

        strip_headings = profile.get("strip_headings")
        if not isinstance(strip_headings, list):
            errors.append(f"{profile_id}: strip_headings must be a list.")
        else:
            for index, record in enumerate(strip_headings):
                if not isinstance(record, dict):
                    errors.append(f"{profile_id}: strip_headings[{index}] must be an object.")
                    continue
                level = record.get("level")
                title = record.get("title")
                if not isinstance(level, int) or level < 1 or level > 6:
                    errors.append(f"{profile_id}: strip_headings[{index}] level must be 1..6.")
                if not isinstance(title, str) or not title.strip():
                    errors.append(f"{profile_id}: strip_headings[{index}] title must be non-empty.")

    missing_profiles = REQUIRED_PROFILES - profile_ids
    if missing_profiles:
        errors.append(f"Missing required profiles: {sorted(missing_profiles)}")

    profiles_by_id = {
        str(profile.get("id")): profile
        for profile in profiles
        if isinstance(profile, dict) and profile.get("id")
    }
    reader = profiles_by_id.get("reader_release")
    if reader:
        reader_strips = normalized_strip_set(reader)
        missing_strips = READER_REQUIRED_STRIPS - reader_strips
        if missing_strips:
            errors.append(f"reader_release is missing required strip headings: {sorted(missing_strips)}")
        formats = set(reader.get("publication_formats", []))
        for required_format in ("epub", "pdf", "docx"):
            if required_format not in formats:
                errors.append(f"reader_release must list {required_format} as a publication format.")

    audio = profiles_by_id.get("audio_release")
    if audio and not isinstance(audio.get("narration_rules"), list):
        errors.append("audio_release must define narration_rules.")

    if errors:
        fail(errors)

    print("Release profile validation passed.")


if __name__ == "__main__":
    main()
