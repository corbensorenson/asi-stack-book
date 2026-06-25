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
REQUIRED_CONTENT_LAYERS = {
    "reader_spine",
    "live_research_scaffold",
    "evidence_matrices",
    "machine_contracts",
    "release_derivatives",
    "audio_adaptation",
}
CONTENT_LAYER_POLICY_KEYS = ("retain", "strip_or_summarize", "derive", "exclude")
REQUIRED_TOP_LEVEL_POLICIES = {
    "major_version_policy",
    "reader_manuscript_policy",
    "audio_manuscript_policy",
}
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


def validate_string_list(owner: str, key: str, values: object, errors: list[str]) -> None:
    if not isinstance(values, list) or not values:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return
    for value in values:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{owner}: {key} entries must be non-empty strings.")


def validate_content_layer_policy(
    profile_id: str,
    policy: object,
    known_content_layers: set[str],
    errors: list[str],
) -> None:
    if not isinstance(policy, dict):
        errors.append(f"{profile_id}: content_layer_policy must be an object.")
        return

    for key in CONTENT_LAYER_POLICY_KEYS:
        values = policy.get(key)
        if not isinstance(values, list):
            errors.append(f"{profile_id}: content_layer_policy.{key} must be a list.")
            continue
        for value in values:
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{profile_id}: content_layer_policy.{key} entries must be non-empty strings.")
                continue
            if value not in known_content_layers:
                errors.append(f"{profile_id}: unknown content layer in {key}: {value}")

    if profile_id == "reader_release":
        retained = set(policy.get("retain", [])) if isinstance(policy.get("retain"), list) else set()
        stripped = (
            set(policy.get("strip_or_summarize", []))
            if isinstance(policy.get("strip_or_summarize"), list)
            else set()
        )
        if "reader_spine" not in retained:
            errors.append("reader_release must retain the reader_spine content layer.")
        for required_layer in ("live_research_scaffold", "machine_contracts"):
            if required_layer not in stripped:
                errors.append(f"reader_release must strip_or_summarize {required_layer}.")

    if profile_id == "audio_release":
        derived = set(policy.get("derive", [])) if isinstance(policy.get("derive"), list) else set()
        stripped = (
            set(policy.get("strip_or_summarize", []))
            if isinstance(policy.get("strip_or_summarize"), list)
            else set()
        )
        if "audio_adaptation" not in derived:
            errors.append("audio_release must derive the audio_adaptation content layer.")
        if "reader_spine" not in stripped:
            errors.append("audio_release must adapt the reader_spine through strip_or_summarize.")


def main() -> None:
    errors: list[str] = []
    data = load_json(PROFILES_PATH)
    if not isinstance(data, dict):
        fail(["editions/release_profiles.json must contain an object."])

    if data.get("schema_version") != "0.1":
        errors.append("release profile schema_version must be 0.1.")

    for key in REQUIRED_TOP_LEVEL_POLICIES:
        if not isinstance(data.get(key), dict):
            errors.append(f"Missing required top-level policy object: {key}")

    content_layers = data.get("content_layers")
    if not isinstance(content_layers, list):
        errors.append("content_layers must be a list.")
        known_content_layers: set[str] = set()
    else:
        known_content_layers = {
            str(record.get("id", ""))
            for record in content_layers
            if isinstance(record, dict)
        }
        missing_content_layers = REQUIRED_CONTENT_LAYERS - known_content_layers
        if missing_content_layers:
            errors.append(f"Missing required content layers: {sorted(missing_content_layers)}")
        for index, record in enumerate(content_layers):
            if not isinstance(record, dict):
                errors.append(f"content_layers[{index}] must be an object.")
                continue
            layer_id = str(record.get("id", ""))
            if not layer_id:
                errors.append(f"content_layers[{index}] missing id.")
            for key in ("label", "canonical_location", "description", "edition_policy"):
                if not isinstance(record.get(key), str) or not record[key].strip():
                    errors.append(f"content_layers[{index}] {layer_id}: missing non-empty {key}.")
            validate_path_list(
                f"content_layers[{index}] {layer_id}",
                "primary_audiences",
                record.get("primary_audiences"),
                errors,
            )

    validate_string_list(
        "reader_spine_contract",
        "reader_spine_contract",
        data.get("reader_spine_contract"),
        errors,
    )

    major_policy = data.get("major_version_policy")
    if isinstance(major_policy, dict):
        if major_policy.get("canonical_source_profile") != "live_book":
            errors.append("major_version_policy.canonical_source_profile must be live_book.")
        for path_key in ("living_release_record_schema", "edition_release_record_schema"):
            value = major_policy.get(path_key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"major_version_policy.{path_key} must be a non-empty string.")
            elif not (ROOT / value).exists():
                errors.append(f"major_version_policy.{path_key} does not exist: {value}")
        validate_string_list("major_version_policy", "artifact_policy", major_policy.get("artifact_policy"), errors)

    reader_policy = data.get("reader_manuscript_policy")
    if isinstance(reader_policy, dict):
        validate_string_list(
            "reader_manuscript_policy",
            "retain_section_intent",
            reader_policy.get("retain_section_intent"),
            errors,
        )
        validate_string_list(
            "reader_manuscript_policy",
            "continuity_requirements",
            reader_policy.get("continuity_requirements"),
            errors,
        )

    audio_policy = data.get("audio_manuscript_policy")
    if isinstance(audio_policy, dict):
        if audio_policy.get("derived_from_profile") != "reader_release":
            errors.append("audio_manuscript_policy.derived_from_profile must be reader_release.")
        validate_string_list(
            "audio_manuscript_policy",
            "review_requirements",
            audio_policy.get("review_requirements"),
            errors,
        )

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

        validate_content_layer_policy(
            profile_id,
            profile.get("content_layer_policy"),
            known_content_layers,
            errors,
        )
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
        if reader.get("generated_source_dir") != "build/reader_edition":
            errors.append("reader_release.generated_source_dir must be build/reader_edition.")
        if reader.get("reader_review_required") is not True:
            errors.append("reader_release.reader_review_required must be true.")
        reader_strips = normalized_strip_set(reader)
        missing_strips = READER_REQUIRED_STRIPS - reader_strips
        if missing_strips:
            errors.append(f"reader_release is missing required strip headings: {sorted(missing_strips)}")
        formats = set(reader.get("publication_formats", []))
        for required_format in ("epub", "pdf", "docx"):
            if required_format not in formats:
                errors.append(f"reader_release must list {required_format} as a publication format.")
        release_gate = reader.get("release_gate", [])
        if (
            not isinstance(release_gate, list)
            or "python3 scripts/render_reader_formats.py --check" not in release_gate
        ):
            errors.append("reader_release release_gate must include render_reader_formats.py --check.")

    audio = profiles_by_id.get("audio_release")
    if audio and not isinstance(audio.get("narration_rules"), list):
        errors.append("audio_release must define narration_rules.")
    if audio:
        if audio.get("reader_profile_dependency") != "reader_release":
            errors.append("audio_release.reader_profile_dependency must be reader_release.")
        if audio.get("generated_script_dir") != "build/audio_script":
            errors.append("audio_release.generated_script_dir must be build/audio_script.")

    if errors:
        fail(errors)

    print("Release profile validation passed.")


if __name__ == "__main__":
    main()
