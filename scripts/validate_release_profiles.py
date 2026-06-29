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
    "companion_material",
}
CONTENT_LAYER_POLICY_KEYS = ("retain", "strip_or_summarize", "derive", "exclude")
REQUIRED_TOP_LEVEL_POLICIES = {
    "major_version_policy",
    "companion_material_policy",
    "human_consumption_bundle_policy",
    "reader_manuscript_policy",
    "reader_overlay_policy",
    "reader_spine_validation",
    "live_human_view_policy",
    "audio_manuscript_policy",
}
REQUIRED_RELEASE_LADDER_STAGES = {
    "live_tag",
    "research_release",
    "reader_source",
    "reader_formats",
    "audio_script",
    "audio_artifacts",
}
REQUIRED_BUNDLE_CLASSES = {
    "reader_formats",
    "optional_ereader_conversions",
    "audio_artifacts",
    "audio_embedded_epub",
}
REQUIRED_READER_BUNDLE_FORMATS = {"html", "epub", "pdf", "docx"}
REQUIRED_OPTIONAL_EREADER_FORMATS = {"azw3", "mobi", "markdown", "plain text"}
REQUIRED_AUDIO_BUNDLE_FORMATS = {"mp3", "m4b", "audio-embedded-epub"}
READER_REQUIRED_STRIPS = {
    (2, "chapter status"),
    (2, "drafting guardrail"),
    (2, "codex test plan"),
    (2, "source crosswalk"),
    (2, "formalization hooks"),
    (3, "claim-source mapping status"),
    (3, "formalization hooks"),
}
READER_REQUIRED_HEADINGS = {
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Interfaces",
    "Invariants",
    "Failure modes",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Summary",
    "Handoff",
}
READER_REQUIRED_HARD_BLOCKED_TERMS = {
    "drafting guardrail",
    "codex test plan",
    "codex workflow",
    "claim-source mapping status",
    "formalization hooks",
    "source crosswalk",
    "source-note",
}
READER_REQUIRED_SECTION_WORD_FLOORS = {
    "Problem": 120,
    "Why existing approaches are insufficient": 110,
    "Core Claim": 40,
    "Mechanism": 300,
    "Interfaces": 120,
    "Invariants": 100,
    "Failure modes": 100,
    "Minimum Viable Implementation": 110,
    "Beyond the State of the Art": 180,
    "Summary": 110,
    "Handoff": 45,
}
READER_REQUIRED_SECTION_PROSE_PARAGRAPH_FLOORS = {
    "Problem": 2,
    "Why existing approaches are insufficient": 2,
    "Core Claim": 1,
    "Mechanism": 4,
    "Interfaces": 1,
    "Invariants": 1,
    "Failure modes": 1,
    "Minimum Viable Implementation": 2,
    "Beyond the State of the Art": 3,
    "Summary": 2,
    "Handoff": 1,
}
READER_OVERLAY_ALLOWED_ACTIONS = {
    "replace_section",
    "prepend_to_section",
    "append_to_section",
    "insert_before_section",
    "insert_after_section",
}
AUDIO_FORBIDDEN_STRIPS = {
    (2, "minimum viable implementation"),
    (2, "beyond the state of the art"),
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


def validate_release_gate_sequence(
    profile_id: str,
    release_gate: object,
    required_sequence: list[str],
    errors: list[str],
) -> None:
    if not isinstance(release_gate, list):
        errors.append(f"{profile_id}: release_gate must be a list before sequence checks.")
        return

    positions: list[tuple[str, int]] = []
    for command in required_sequence:
        try:
            positions.append((command, release_gate.index(command)))
        except ValueError:
            errors.append(f"{profile_id}: release_gate must include `{command}`.")

    if len(positions) != len(required_sequence):
        return

    for (earlier_command, earlier_index), (later_command, later_index) in zip(
        positions,
        positions[1:],
    ):
        if earlier_index >= later_index:
            errors.append(
                f"{profile_id}: release_gate must run `{earlier_command}` before `{later_command}`."
            )


def validate_int_floor_map(
    owner: str,
    key: str,
    value: object,
    required_floors: dict[str, int],
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{owner}: {key} must be an object.")
        return
    for heading, floor in required_floors.items():
        actual = value.get(heading)
        if not isinstance(actual, int) or actual < floor:
            errors.append(f"{owner}: {key}.{heading} must be an integer >= {floor}.")
    for heading, actual in value.items():
        if not isinstance(heading, str) or not heading.strip():
            errors.append(f"{owner}: {key} headings must be non-empty strings.")
        if not isinstance(actual, int) or actual < 0:
            errors.append(f"{owner}: {key}.{heading} must be a non-negative integer.")


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
        derived = set(policy.get("derive", [])) if isinstance(policy.get("derive"), list) else set()
        if "reader_spine" not in retained:
            errors.append("reader_release must retain the reader_spine content layer.")
        for required_layer in ("live_research_scaffold", "machine_contracts"):
            if required_layer not in stripped:
                errors.append(f"reader_release must strip_or_summarize {required_layer}.")
        if "companion_material" not in derived:
            errors.append("reader_release must derive companion_material for e-reader/audio treatment notes.")

    if profile_id == "audio_release":
        derived = set(policy.get("derive", [])) if isinstance(policy.get("derive"), list) else set()
        stripped = (
            set(policy.get("strip_or_summarize", []))
            if isinstance(policy.get("strip_or_summarize"), list)
            else set()
        )
        if "audio_adaptation" not in derived:
            errors.append("audio_release must derive the audio_adaptation content layer.")
        if "companion_material" not in derived:
            errors.append("audio_release must derive companion_material for spoken-treatment notes.")
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
        release_ladder = major_policy.get("release_ladder")
        if not isinstance(release_ladder, list) or not release_ladder:
            errors.append("major_version_policy.release_ladder must be a non-empty list.")
        else:
            stages: set[str] = set()
            for index, record in enumerate(release_ladder):
                if not isinstance(record, dict):
                    errors.append(f"major_version_policy.release_ladder[{index}] must be an object.")
                    continue
                stage = record.get("stage")
                if not isinstance(stage, str) or not stage.strip():
                    errors.append(f"major_version_policy.release_ladder[{index}] missing non-empty stage.")
                else:
                    stages.add(stage)
                profile_id = record.get("profile")
                if not isinstance(profile_id, str) or profile_id not in REQUIRED_PROFILES:
                    errors.append(
                        f"major_version_policy.release_ladder[{index}] profile must be one of "
                        f"{sorted(REQUIRED_PROFILES)}."
                    )
                audiences = record.get("audiences")
                if not isinstance(audiences, list) or not audiences:
                    errors.append(f"major_version_policy.release_ladder[{index}] audiences must be a non-empty list.")
                else:
                    unknown = sorted(set(audiences) - REQUIRED_AUDIENCES)
                    if unknown:
                        errors.append(
                            f"major_version_policy.release_ladder[{index}] unknown audiences: {unknown}"
                        )
                for key in ("gate", "artifact_rule"):
                    if not isinstance(record.get(key), str) or not record[key].strip():
                        errors.append(
                            f"major_version_policy.release_ladder[{index}] missing non-empty {key}."
                        )
            missing_ladder = REQUIRED_RELEASE_LADDER_STAGES - stages
            if missing_ladder:
                errors.append(f"major_version_policy.release_ladder missing stages: {sorted(missing_ladder)}")

    companion_policy = data.get("companion_material_policy")
    if isinstance(companion_policy, dict):
        for key in ("reader_companion_path", "audio_companion_path", "purpose"):
            value = companion_policy.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"companion_material_policy.{key} must be a non-empty string.")
        routing_manifest = companion_policy.get("routing_manifest")
        if routing_manifest != "editions/reader_manuscript/v1_0/companion_note_routing.json":
            errors.append(
                "companion_material_policy.routing_manifest must be "
                "editions/reader_manuscript/v1_0/companion_note_routing.json."
            )
        elif not (ROOT / routing_manifest).exists():
            errors.append(f"companion_material_policy.routing_manifest does not exist: {routing_manifest}")
        for path_key in ("reader_companion_path", "audio_companion_path"):
            value = companion_policy.get(path_key)
            if isinstance(value, str) and value and not value.endswith(".md"):
                errors.append(f"companion_material_policy.{path_key} must be a Markdown file name.")
        validate_string_list(
            "companion_material_policy",
            "required_topics",
            companion_policy.get("required_topics"),
            errors,
        )
        validate_string_list(
            "companion_material_policy",
            "review_requirements",
            companion_policy.get("review_requirements"),
            errors,
        )
        validate_string_list(
            "companion_material_policy",
            "non_claims",
            companion_policy.get("non_claims"),
            errors,
        )

    bundle_policy = data.get("human_consumption_bundle_policy")
    if isinstance(bundle_policy, dict):
        if bundle_policy.get("canonical_reader_profile") != "reader_release":
            errors.append("human_consumption_bundle_policy.canonical_reader_profile must be reader_release.")
        validate_string_list(
            "human_consumption_bundle_policy",
            "source_sequence",
            bundle_policy.get("source_sequence"),
            errors,
        )
        validate_string_list(
            "human_consumption_bundle_policy",
            "human_quality_gates",
            bundle_policy.get("human_quality_gates"),
            errors,
        )
        validate_string_list(
            "human_consumption_bundle_policy",
            "audio_quality_gates",
            bundle_policy.get("audio_quality_gates"),
            errors,
        )
        classes = bundle_policy.get("bundle_artifact_classes")
        if not isinstance(classes, list) or not classes:
            errors.append("human_consumption_bundle_policy.bundle_artifact_classes must be a non-empty list.")
        else:
            class_ids: set[str] = set()
            formats_by_class: dict[str, set[str]] = {}
            for index, record in enumerate(classes):
                if not isinstance(record, dict):
                    errors.append(
                        f"human_consumption_bundle_policy.bundle_artifact_classes[{index}] must be an object."
                    )
                    continue
                class_id = record.get("id")
                if not isinstance(class_id, str) or not class_id.strip():
                    errors.append(
                        f"human_consumption_bundle_policy.bundle_artifact_classes[{index}] missing non-empty id."
                    )
                    continue
                class_ids.add(class_id)
                profile_id = record.get("profile")
                if not isinstance(profile_id, str) or profile_id not in REQUIRED_PROFILES:
                    errors.append(
                        f"human_consumption_bundle_policy.bundle_artifact_classes[{index}] "
                        f"profile must be one of {sorted(REQUIRED_PROFILES)}."
                    )
                formats = record.get("formats")
                if not isinstance(formats, list) or not formats:
                    errors.append(
                        f"human_consumption_bundle_policy.bundle_artifact_classes[{index}] "
                        "formats must be a non-empty list."
                    )
                else:
                    normalized_formats = {str(value) for value in formats if isinstance(value, str)}
                    formats_by_class[class_id] = normalized_formats
                    if len(normalized_formats) != len(formats):
                        errors.append(
                            f"human_consumption_bundle_policy.bundle_artifact_classes[{index}] "
                            "formats must be strings."
                        )
                for key in ("artifact_rule", "review_gate"):
                    if not isinstance(record.get(key), str) or not record[key].strip():
                        errors.append(
                            f"human_consumption_bundle_policy.bundle_artifact_classes[{index}] "
                            f"missing non-empty {key}."
                        )
            missing_classes = REQUIRED_BUNDLE_CLASSES - class_ids
            if missing_classes:
                errors.append(
                    "human_consumption_bundle_policy.bundle_artifact_classes missing "
                    f"{sorted(missing_classes)}."
                )
            reader_formats = formats_by_class.get("reader_formats", set())
            missing_reader_formats = REQUIRED_READER_BUNDLE_FORMATS - reader_formats
            if missing_reader_formats:
                errors.append(
                    "human_consumption_bundle_policy.reader_formats missing "
                    f"{sorted(missing_reader_formats)}."
                )
            optional_formats = formats_by_class.get("optional_ereader_conversions", set())
            missing_optional_formats = REQUIRED_OPTIONAL_EREADER_FORMATS - optional_formats
            if missing_optional_formats:
                errors.append(
                    "human_consumption_bundle_policy.optional_ereader_conversions missing "
                    f"{sorted(missing_optional_formats)}."
                )
            audio_formats = (
                formats_by_class.get("audio_artifacts", set())
                | formats_by_class.get("audio_embedded_epub", set())
            )
            missing_audio_formats = REQUIRED_AUDIO_BUNDLE_FORMATS - audio_formats
            if missing_audio_formats:
                errors.append(
                    "human_consumption_bundle_policy audio bundle classes missing "
                    f"{sorted(missing_audio_formats)}."
                )

    reader_policy = data.get("reader_manuscript_policy")
    if isinstance(reader_policy, dict):
        checklist = reader_policy.get("generated_checklist_path")
        if not isinstance(checklist, str) or checklist != "READER_RELEASE_CHECKLIST.md":
            errors.append("reader_manuscript_policy.generated_checklist_path must be READER_RELEASE_CHECKLIST.md.")
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
        validate_string_list(
            "reader_manuscript_policy",
            "human_reader_quality_floor",
            reader_policy.get("human_reader_quality_floor"),
            errors,
        )
        validate_string_list(
            "reader_manuscript_policy",
            "ebook_quality_checks",
            reader_policy.get("ebook_quality_checks"),
            errors,
        )
        validate_string_list(
            "reader_manuscript_policy",
            "optional_downstream_formats",
            reader_policy.get("optional_downstream_formats"),
            errors,
        )

    overlay_policy = data.get("reader_overlay_policy")
    if isinstance(overlay_policy, dict):
        if overlay_policy.get("script") != "scripts/validate_reader_overlays.py":
            errors.append("reader_overlay_policy.script must be scripts/validate_reader_overlays.py.")
        if overlay_policy.get("default_manifest") != "editions/reader_overlays/v1_0/manifest.json":
            errors.append(
                "reader_overlay_policy.default_manifest must be "
                "editions/reader_overlays/v1_0/manifest.json."
            )
        if overlay_policy.get("live_human_view_asset") != "assets/reader-overlays.html":
            errors.append("reader_overlay_policy.live_human_view_asset must be assets/reader-overlays.html.")
        if overlay_policy.get("live_human_view_asset_sync") != "scripts/sync_reader_overlay_asset.py":
            errors.append(
                "reader_overlay_policy.live_human_view_asset_sync must be "
                "scripts/sync_reader_overlay_asset.py."
            )
        if overlay_policy.get("generated_delta_report") != "reader_delta_report.md":
            errors.append("reader_overlay_policy.generated_delta_report must be reader_delta_report.md.")
        if overlay_policy.get("editable_delta_source") != "editions/reader_overlays/":
            errors.append("reader_overlay_policy.editable_delta_source must be editions/reader_overlays/.")
        report_policy = overlay_policy.get("generated_delta_report_policy")
        if not isinstance(report_policy, str) or "review artifact" not in report_policy or "regenerate" not in report_policy:
            errors.append(
                "reader_overlay_policy.generated_delta_report_policy must describe the generated report as "
                "a review artifact that is regenerated from source."
            )
        for path_key in ("script", "default_manifest", "live_human_view_asset", "live_human_view_asset_sync"):
            value = overlay_policy.get(path_key)
            if isinstance(value, str) and value and not (ROOT / value).exists():
                errors.append(f"reader_overlay_policy.{path_key} does not exist: {value}")
        actions = overlay_policy.get("allowed_actions")
        if not isinstance(actions, list):
            errors.append("reader_overlay_policy.allowed_actions must be a list.")
        else:
            normalized_actions = {str(action) for action in actions if isinstance(action, str)}
            missing_actions = READER_OVERLAY_ALLOWED_ACTIONS - normalized_actions
            unknown_actions = normalized_actions - READER_OVERLAY_ALLOWED_ACTIONS
            if missing_actions:
                errors.append(f"reader_overlay_policy.allowed_actions missing {sorted(missing_actions)}.")
            if unknown_actions:
                errors.append(f"reader_overlay_policy.allowed_actions has unknown actions {sorted(unknown_actions)}.")
        for key in ("manual_edit_policy", "non_claims"):
            validate_string_list("reader_overlay_policy", key, overlay_policy.get(key), errors)
        manual_policy = overlay_policy.get("manual_edit_policy", [])
        if isinstance(manual_policy, list):
            joined_policy = " ".join(str(item) for item in manual_policy)
            for fragment in (
                "editable source for reader-only deltas",
                "reader_delta_report.md is reviewed",
                "stable repository-relative files and headings",
            ):
                if fragment not in joined_policy:
                    errors.append(f"reader_overlay_policy.manual_edit_policy must mention {fragment!r}.")
        purpose = overlay_policy.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            errors.append("reader_overlay_policy.purpose must be a non-empty string.")
    else:
        errors.append("editions/release_profiles.json must define reader_overlay_policy.")

    spine_policy = data.get("reader_spine_validation")
    if isinstance(spine_policy, dict):
        if spine_policy.get("script") != "scripts/validate_reader_spine.py":
            errors.append("reader_spine_validation.script must be scripts/validate_reader_spine.py.")
        report_path = spine_policy.get("report_path")
        if not isinstance(report_path, str) or report_path != "build/reader_spine_report.json":
            errors.append("reader_spine_validation.report_path must be build/reader_spine_report.json.")
        minimum = spine_policy.get("minimum_chapter_word_count")
        if not isinstance(minimum, int) or minimum < 1000:
            errors.append("reader_spine_validation.minimum_chapter_word_count must be an integer >= 1000.")
        minimum_handoff = spine_policy.get("minimum_handoff_word_count")
        if not isinstance(minimum_handoff, int) or minimum_handoff < 45:
            errors.append("reader_spine_validation.minimum_handoff_word_count must be an integer >= 45.")
        validate_string_list(
            "reader_spine_validation",
            "hard_blocked_terms",
            spine_policy.get("hard_blocked_terms"),
            errors,
        )
        hard_blocked_terms = {
            str(term).lower()
            for term in spine_policy.get("hard_blocked_terms", [])
            if isinstance(term, str)
        }
        missing_hard_terms = READER_REQUIRED_HARD_BLOCKED_TERMS - hard_blocked_terms
        if missing_hard_terms:
            errors.append(
                "reader_spine_validation.hard_blocked_terms missing "
                f"{sorted(missing_hard_terms)}."
            )
        validate_string_list(
            "reader_spine_validation",
            "blocked_paragraph_starts",
            spine_policy.get("blocked_paragraph_starts"),
            errors,
        )
        blocked_paragraph_starts = {
            str(term)
            for term in spine_policy.get("blocked_paragraph_starts", [])
            if isinstance(term, str)
        }
        if "Evidence boundary: architectural argument." not in blocked_paragraph_starts:
            errors.append(
                "reader_spine_validation.blocked_paragraph_starts must reject "
                "'Evidence boundary: architectural argument.'."
            )
        validate_string_list(
            "reader_spine_validation",
            "required_reader_headings",
            spine_policy.get("required_reader_headings"),
            errors,
        )
        required_headings = set(spine_policy.get("required_reader_headings", []))
        missing_reader_headings = READER_REQUIRED_HEADINGS - required_headings
        if missing_reader_headings:
            errors.append(
                "reader_spine_validation.required_reader_headings missing "
                f"{sorted(missing_reader_headings)}."
            )
        validate_int_floor_map(
            "reader_spine_validation",
            "minimum_section_word_counts",
            spine_policy.get("minimum_section_word_counts"),
            READER_REQUIRED_SECTION_WORD_FLOORS,
            errors,
        )
        validate_int_floor_map(
            "reader_spine_validation",
            "minimum_section_prose_paragraph_counts",
            spine_policy.get("minimum_section_prose_paragraph_counts"),
            READER_REQUIRED_SECTION_PROSE_PARAGRAPH_FLOORS,
            errors,
        )
        purpose = spine_policy.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            errors.append("reader_spine_validation.purpose must be a non-empty string.")
    else:
        errors.append("editions/release_profiles.json must define reader_spine_validation.")

    evidence_boundary_policy = data.get("reader_evidence_boundary_validation")
    if isinstance(evidence_boundary_policy, dict):
        if evidence_boundary_policy.get("script") != "scripts/validate_reader_evidence_boundaries.py":
            errors.append(
                "reader_evidence_boundary_validation.script must be "
                "scripts/validate_reader_evidence_boundaries.py."
            )
        report_path = evidence_boundary_policy.get("report_path")
        if not isinstance(report_path, str) or report_path != "build/reader_evidence_boundaries_report.json":
            errors.append(
                "reader_evidence_boundary_validation.report_path must be "
                "build/reader_evidence_boundaries_report.json."
            )
        if evidence_boundary_policy.get("required_live_source_core_claim_marker") is not True:
            errors.append("reader_evidence_boundary_validation.required_live_source_core_claim_marker must be true.")
        if evidence_boundary_policy.get("strip_raw_reader_core_claim_marker") is not True:
            errors.append("reader_evidence_boundary_validation.strip_raw_reader_core_claim_marker must be true.")
        if evidence_boundary_policy.get("required_reader_claim_text") is not True:
            errors.append("reader_evidence_boundary_validation.required_reader_claim_text must be true.")
        if evidence_boundary_policy.get("required_plain_support_boundary") is not True:
            errors.append("reader_evidence_boundary_validation.required_plain_support_boundary must be true.")
        if evidence_boundary_policy.get("strip_repeated_support_boilerplate") is not True:
            errors.append("reader_evidence_boundary_validation.strip_repeated_support_boilerplate must be true.")
        if evidence_boundary_policy.get("human_argument_boundary_phrase") != "Evidence boundary: architectural argument.":
            errors.append(
                "reader_evidence_boundary_validation.human_argument_boundary_phrase must be "
                "'Evidence boundary: architectural argument.'."
            )
        purpose = evidence_boundary_policy.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            errors.append("reader_evidence_boundary_validation.purpose must be a non-empty string.")
        script = evidence_boundary_policy.get("script")
        if isinstance(script, str) and script and not (ROOT / script).exists():
            errors.append(f"reader_evidence_boundary_validation.script does not exist: {script}")
    else:
        errors.append("editions/release_profiles.json must define reader_evidence_boundary_validation.")

    live_human_policy = data.get("live_human_view_policy")
    if isinstance(live_human_policy, dict):
        expected_values = {
            "toggle_asset": "assets/reading-mode.html",
            "reader_overlay_asset": "assets/reader-overlays.html",
            "reader_overlay_asset_sync": "scripts/sync_reader_overlay_asset.py",
            "static_validator": "scripts/validate_live_human_view.py",
            "browser_validator": "scripts/validate_live_human_view_browser.js",
            "browser_report_path": "build/live_human_view_browser_report.json",
            "default_mode": "ai",
            "human_mode": "human",
            "storage_key": "asi-stack-reading-mode",
            "url_query_parameter": "view",
            "mode_status_selector": "[data-asi-reading-mode-status]",
            "toc_link_marker": "data-asi-live-toc-link",
            "human_toc_link_marker": "data-asi-human-toc-link",
            "ai_toc_link_marker": "data-asi-ai-toc-link",
            "core_claim_marker_class": "asi-core-claim-marker",
            "human_view_core_claim_marker_policy": "hide raw bracketed core-claim markers in Human view while preserving claim text and support-state prose",
            "support_boundary_ai_class": "asi-support-boilerplate-ai",
            "support_boundary_human_class": "asi-support-boundary-human",
            "human_view_support_boundary_policy": "hide repeated AI/research support-state boilerplate in Human view and attach a compact evidence-boundary phrase to the core claim while preserving the original sentence in AI view",
            "assistive_description_class": "asi-sr-only",
            "human_view_section_number_policy": "hide rendered section numbers in Human view to avoid numbering gaps left by stripped live-only sections and unheaded bridge prose",
            "ai_only_class": "asi-ai-only",
            "human_only_class": "asi-human-only",
            "live_only_class": "asi-live-only",
        }
        for key, expected in expected_values.items():
            if live_human_policy.get(key) != expected:
                errors.append(f"live_human_view_policy.{key} must be {expected!r}.")
        for path_key in (
            "toggle_asset",
            "reader_overlay_asset",
            "reader_overlay_asset_sync",
            "static_validator",
            "browser_validator",
        ):
            value = live_human_policy.get(path_key)
            if isinstance(value, str) and value and not (ROOT / value).exists():
                errors.append(f"live_human_view_policy.{path_key} does not exist: {value}")
        for key in ("reader_release_processing", "chapter_contract"):
            if not isinstance(live_human_policy.get(key), str) or not live_human_policy[key].strip():
                errors.append(f"live_human_view_policy.{key} must be a non-empty string.")

    audio_policy = data.get("audio_manuscript_policy")
    if isinstance(audio_policy, dict):
        if audio_policy.get("derived_from_profile") != "reader_release":
            errors.append("audio_manuscript_policy.derived_from_profile must be reader_release.")
        checklist = audio_policy.get("generated_checklist_path")
        if not isinstance(checklist, str) or checklist != "AUDIO_RELEASE_CHECKLIST.md":
            errors.append("audio_manuscript_policy.generated_checklist_path must be AUDIO_RELEASE_CHECKLIST.md.")
        if audio_policy.get("pronunciation_glossary_path") != "pronunciation_glossary.md":
            errors.append(
                "audio_manuscript_policy.pronunciation_glossary_path must be pronunciation_glossary.md."
            )
        if audio_policy.get("proof_equation_reading_rules_path") != "proof_equation_reading_rules.md":
            errors.append(
                "audio_manuscript_policy.proof_equation_reading_rules_path must be proof_equation_reading_rules.md."
            )
        audio_formats = audio_policy.get("audio_artifact_formats")
        if not isinstance(audio_formats, list):
            errors.append("audio_manuscript_policy.audio_artifact_formats must be a list.")
        else:
            missing_audio_formats = {"mp3", "m4b", "audio-embedded-epub"} - set(audio_formats)
            if missing_audio_formats:
                errors.append(
                    "audio_manuscript_policy.audio_artifact_formats is missing "
                    f"{sorted(missing_audio_formats)}."
                )
        validate_string_list(
            "audio_manuscript_policy",
            "review_requirements",
            audio_policy.get("review_requirements"),
            errors,
        )
        review_text = " ".join(str(item) for item in audio_policy.get("review_requirements", [])).lower()
        if "pronunciation" not in review_text or "proof" not in review_text or "equation" not in review_text:
            errors.append(
                "audio_manuscript_policy.review_requirements must mention pronunciation, proof, and equation review."
            )
        validate_string_list(
            "audio_manuscript_policy",
            "audio_packaging_checks",
            audio_policy.get("audio_packaging_checks"),
            errors,
        )
        validate_string_list(
            "audio_manuscript_policy",
            "spoken_treatment_rules",
            audio_policy.get("spoken_treatment_rules"),
            errors,
        )
        spoken_text = " ".join(str(item) for item in audio_policy.get("spoken_treatment_rules", [])).lower()
        if "proof" not in spoken_text or "equation" not in spoken_text or "support state" not in spoken_text:
            errors.append(
                "audio_manuscript_policy.spoken_treatment_rules must mention proof, equation, and support-state treatment."
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
        if reader.get("reader_overlay_manifest") != "editions/reader_overlays/v1_0/manifest.json":
            errors.append(
                "reader_release.reader_overlay_manifest must be "
                "editions/reader_overlays/v1_0/manifest.json."
            )
        overlay_manifest = reader.get("reader_overlay_manifest")
        if isinstance(overlay_manifest, str) and overlay_manifest and not (ROOT / overlay_manifest).exists():
            errors.append(f"reader_release.reader_overlay_manifest does not exist: {overlay_manifest}")
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
        validate_release_gate_sequence(
            "reader_release",
            release_gate,
            [
                "python3 scripts/build_reader_edition.py --check",
                "python3 scripts/sync_reader_overlay_asset.py --check",
                "python3 scripts/validate_reader_overlays.py --check",
                "python3 scripts/validate_human_reading_paths.py",
                "python3 scripts/validate_reader_evidence_boundaries.py --check",
                "python3 scripts/validate_reader_spine.py --check",
                "python3 scripts/render_reader_formats.py --check",
            ],
            errors,
        )

    live_book = profiles_by_id.get("live_book")
    if live_book:
        release_gate = live_book.get("release_gate", [])
        validate_release_gate_sequence(
            "live_book",
            release_gate,
            [
                "python3 scripts/sync_scaffold.py",
                "python3 scripts/sync_proof_manifest.py --check",
                "python3 scripts/validate_release_profiles.py",
                "python3 scripts/validate_reading_mode_toggle.py",
                "python3 scripts/validate_human_reading_paths.py",
                "python3 scripts/validate_reader_evidence_boundaries.py --check",
                "python3 scripts/sync_reader_overlay_asset.py --check",
                "python3 scripts/validate_reader_overlays.py --check",
                "python3 scripts/validate_publication.py",
                "python3 scripts/validate_book.py",
                "LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html",
                "python3 scripts/validate_live_human_view.py",
                "node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports",
            ],
            errors,
        )

    audio = profiles_by_id.get("audio_release")
    if audio and not isinstance(audio.get("narration_rules"), list):
        errors.append("audio_release must define narration_rules.")
    if audio:
        if audio.get("reader_profile_dependency") != "reader_release":
            errors.append("audio_release.reader_profile_dependency must be reader_release.")
        if audio.get("generated_script_dir") != "build/audio_script":
            errors.append("audio_release.generated_script_dir must be build/audio_script.")
        forbidden_audio_strips = normalized_strip_set(audio) & AUDIO_FORBIDDEN_STRIPS
        if forbidden_audio_strips:
            errors.append(
                "audio_release must preserve implementation-horizon headings: "
                f"{sorted(forbidden_audio_strips)}."
            )

    if errors:
        fail(errors)

    print("Release profile validation passed.")


if __name__ == "__main__":
    main()
