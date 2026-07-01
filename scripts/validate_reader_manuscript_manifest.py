#!/usr/bin/env python3
"""Validate the curated reader manuscript manifest.

The curated reader manuscript is allowed to become a parallel derivative source
for human prose, but it is not allowed to become an independent evidence source.
This validator keeps that path explicit as chapters move from dormant
not-graduated state into drafting, reconciliation, candidate, or released
states.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
ALLOWED_STATUS = {"not_graduated", "drafting", "reconciliation", "release_candidate", "released"}
ALLOWED_RECONCILIATION_STATUS = {"not_started", "drafting", "blocked", "reconciled"}
ALLOWED_CURATION_CONTRACT_STATUS = {"active_contract"}
ALLOWED_READER_HANDOFF_STATUS = {"drafting_handoff_ready"}
ALLOWED_FIGURE_TARGET_STATUS = {"target_defined_not_final_art"}
ALLOWED_ROUTING_STATUS = {
    "retain_in_reader_spine_with_companion_note",
    "future_curated_review_with_companion_note",
}
FIRST_PERSON_RE = re.compile(r"\b(i|me|my|mine|we|our|ours|us)\b", re.IGNORECASE)
REQUIRED_READER_HANDOFF_FIELDS = {
    "schema_version",
    "major_version",
    "status",
    "relationship",
    "single_thesis",
    "part_arcs",
    "signature_ideas",
    "key_figure_targets",
    "corben_voice_pass_slots",
    "non_claims",
}
REQUIRED_PART_ARC_FIELDS = {
    "part_id",
    "title",
    "reader_arc",
    "reader_stakes",
    "handoff_payoff",
}
REQUIRED_SIGNATURE_IDEA_FIELDS = {
    "id",
    "label",
    "reader_promise",
    "anchor_chapter_ids",
}
REQUIRED_FIGURE_TARGET_FIELDS = {
    "id",
    "working_title",
    "purpose",
    "candidate_chapter_ids",
    "status",
    "release_boundary",
}
REQUIRED_VOICE_SLOT_FIELDS = {
    "slot_id",
    "location",
    "prompt",
    "source_chapter_ids",
    "requires_author_input",
    "must_not_fabricate",
}
REQUIRED_CURATION_CONTRACT_FIELDS = {
    "schema_version",
    "major_version",
    "status",
    "canonical_relationship",
    "manifest",
    "contract_doc",
    "curated_chapter_dir",
    "chapter_record_required_fields",
    "allowed_edit_scopes",
    "blocked_edit_scopes",
    "meaning_preservation_checks",
    "required_release_blockers_before_release",
    "required_commands",
    "graduation_modes",
    "non_claims",
}
REQUIRED_CURATED_CHAPTER_RECORD_FIELDS = {
    "chapter_id",
    "title",
    "file",
    "reconciliation_status",
    "generated_baseline_ref",
    "live_source_ref",
    "claim_boundary_ref",
    "implementation_horizon_ref",
    "curation_scope",
    "reader_stakes",
    "reader_payoff",
    "voice_pass_slot_ids",
    "divergence_summary",
    "meaning_preservation_checks",
    "release_blockers",
    "canonical_change_required",
    "canonical_change_ref",
    "review_notes",
}
REQUIRED_CURATION_RELEASE_BLOCKERS = {
    "reader_release_record_not_created",
    "format_artifact_not_reviewed",
    "curated_reconciliation_not_approved",
}
REQUIRED_ROUTING_RELEASE_BLOCKERS = {
    "reader_release_record_not_created",
    "format_artifact_not_reviewed",
    "companion_note_not_release_reviewed",
    "audio_script_not_reviewed",
}
REQUIRED_FIELDS = {
    "schema_version",
    "major_version",
    "status",
    "canonical_relationship",
    "live_sources_of_truth",
    "generated_baseline",
    "overlay_source",
    "allowed_divergence",
    "blocked_divergence",
    "graduation_criteria",
    "companion_note_routing",
    "chapter_review_matrix",
    "format_review_matrix",
    "curation_contract",
    "chapter_records",
    "reader_handoff_contract",
    "reconciliation_report",
    "non_claims",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def flatten_chapters(structure: dict[str, Any]) -> dict[str, dict[str, Any]]:
    chapters: dict[str, dict[str, Any]] = {}
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("id"), str):
                chapters[chapter["id"]] = chapter
    return chapters


def require_string_list(owner: str, key: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner}: {key} entries must be non-empty strings.")
        else:
            result.append(item)
    return result


def require_substantive_string(
    owner: str,
    key: str,
    value: Any,
    errors: list[str],
    *,
    min_words: int = 8,
    no_first_person: bool = False,
) -> str:
    if not isinstance(value, str) or len(value.split()) < min_words:
        errors.append(f"{owner}: {key} must be a substantive sentence.")
        return ""
    if no_first_person and FIRST_PERSON_RE.search(value):
        errors.append(f"{owner}: {key} must not fabricate first-person authorial voice.")
    return value


def require_existing_path(owner: str, path_value: str, errors: list[str]) -> None:
    path = ROOT / path_value
    if not path.exists():
        errors.append(f"{owner}: referenced path does not exist: {path_value}")


def flatten_parts(structure: dict[str, Any]) -> list[dict[str, Any]]:
    parts: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        if isinstance(part, dict) and isinstance(part.get("id"), str):
            parts.append(part)
    return parts


def validate_manifest(data: dict[str, Any], errors: list[str]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        errors.append(f"{rel(MANIFEST)} missing required fields: {missing}")
        return

    if data.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if data.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if data.get("status") not in ALLOWED_STATUS:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUS)}.")
    if data.get("canonical_relationship") != "parallel_derivative_not_equal_authority":
        errors.append("canonical_relationship must be parallel_derivative_not_equal_authority.")

    for path_value in require_string_list("reader manuscript manifest", "live_sources_of_truth", data.get("live_sources_of_truth"), errors):
        require_existing_path("live_sources_of_truth", path_value, errors)

    baseline = data.get("generated_baseline")
    if not isinstance(baseline, dict):
        errors.append("generated_baseline must be an object.")
    else:
        if baseline.get("command") != "python3 scripts/build_reader_edition.py":
            errors.append("generated_baseline.command must be python3 scripts/build_reader_edition.py.")
        if baseline.get("check_command") != "python3 scripts/build_reader_edition.py --check":
            errors.append("generated_baseline.check_command must be python3 scripts/build_reader_edition.py --check.")
        if baseline.get("baseline_dir") != "build/reader_edition":
            errors.append("generated_baseline.baseline_dir must be build/reader_edition.")

    overlay = data.get("overlay_source")
    if not isinstance(overlay, dict):
        errors.append("overlay_source must be an object.")
    else:
        for key in ("manifest", "asset"):
            value = overlay.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"overlay_source.{key} must be a non-empty string.")
            else:
                require_existing_path(f"overlay_source.{key}", value, errors)

    allowed = require_string_list("reader manuscript manifest", "allowed_divergence", data.get("allowed_divergence"), errors)
    blocked = require_string_list("reader manuscript manifest", "blocked_divergence", data.get("blocked_divergence"), errors)
    require_string_list("reader manuscript manifest", "graduation_criteria", data.get("graduation_criteria"), errors)
    non_claims = require_string_list("reader manuscript manifest", "non_claims", data.get("non_claims"), errors)

    blocked_text = " ".join(blocked).lower()
    for required_phrase in ("support-state", "source boundary", "proof/test", "release artifact"):
        if required_phrase not in blocked_text:
            errors.append(f"blocked_divergence must mention {required_phrase}.")

    non_claim_text = " ".join(non_claims).lower()
    for required_phrase in ("does not create", "does not promote", "source of truth"):
        if required_phrase not in non_claim_text:
            errors.append(f"non_claims must include boundary phrase: {required_phrase}")

    if "pacing" not in allowed or "section flow" not in allowed:
        errors.append("allowed_divergence must include pacing and section flow.")

    routing = data.get("companion_note_routing")
    if not isinstance(routing, dict):
        errors.append("companion_note_routing must be an object.")
    else:
        if routing.get("path") != "editions/reader_manuscript/v1_0/companion_note_routing.json":
            errors.append(
                "companion_note_routing.path must be "
                "editions/reader_manuscript/v1_0/companion_note_routing.json."
            )
        if routing.get("review") != "docs/reader_companion_note_routing_review.md":
            errors.append("companion_note_routing.review must be docs/reader_companion_note_routing_review.md.")
        policy = routing.get("policy")
        if not isinstance(policy, str) or "reader spine" not in policy or "audio" not in policy:
            errors.append("companion_note_routing.policy must mention reader spine and audio.")
        for key in ("path", "review"):
            value = routing.get(key)
            if isinstance(value, str):
                require_existing_path(f"companion_note_routing.{key}", value, errors)

    matrix = data.get("chapter_review_matrix")
    if not isinstance(matrix, dict):
        errors.append("chapter_review_matrix must be an object.")
    else:
        expected = {
            "path": "editions/reader_manuscript/v1_0/chapter_review_matrix.json",
            "summary": "docs/reader_chapter_review_matrix.md",
            "sync_command": "python3 scripts/sync_reader_chapter_review_matrix.py --write",
            "check_command": "python3 scripts/sync_reader_chapter_review_matrix.py --check",
        }
        for key, expected_value in expected.items():
            if matrix.get(key) != expected_value:
                errors.append(f"chapter_review_matrix.{key} must be {expected_value}.")
        for key in ("path", "summary"):
            value = matrix.get(key)
            if isinstance(value, str):
                require_existing_path(f"chapter_review_matrix.{key}", value, errors)
        policy = matrix.get("policy")
        if not isinstance(policy, str) or "book_structure.json" not in policy or "release blockers" not in policy:
            errors.append("chapter_review_matrix.policy must mention book_structure.json and release blockers.")

    format_matrix = data.get("format_review_matrix")
    if not isinstance(format_matrix, dict):
        errors.append("format_review_matrix must be an object.")
    else:
        expected = {
            "path": "editions/reader_manuscript/v1_0/format_review_matrix.json",
            "summary": "docs/reader_format_review_matrix.md",
            "sync_command": "python3 scripts/sync_reader_format_review_matrix.py --write",
            "check_command": "python3 scripts/sync_reader_format_review_matrix.py --check",
        }
        for key, expected_value in expected.items():
            if format_matrix.get(key) != expected_value:
                errors.append(f"format_review_matrix.{key} must be {expected_value}.")
        for key in ("path", "summary"):
            value = format_matrix.get(key)
            if isinstance(value, str):
                require_existing_path(f"format_review_matrix.{key}", value, errors)
        policy = format_matrix.get("policy")
        if (
            not isinstance(policy, str)
            or "format artifact" not in policy
            or "edition release record" not in policy
        ):
            errors.append("format_review_matrix.policy must mention format artifact and edition release record.")

    contract_ref = data.get("curation_contract")
    if not isinstance(contract_ref, dict):
        errors.append("curation_contract must be an object.")
    else:
        expected = {
            "path": "editions/reader_manuscript/v1_0/curation_contract.json",
            "doc": "docs/curated_reader_source_contract.md",
            "check_command": "python3 scripts/validate_reader_manuscript_manifest.py",
        }
        for key, expected_value in expected.items():
            if contract_ref.get(key) != expected_value:
                errors.append(f"curation_contract.{key} must be {expected_value}.")
        for key in ("path", "doc"):
            value = contract_ref.get(key)
            if isinstance(value, str):
                require_existing_path(f"curation_contract.{key}", value, errors)
        policy = contract_ref.get("policy")
        if (
            not isinstance(policy, str)
            or "parallel derivative" not in policy
            or "subordinate" not in policy
            or "support states" not in policy
        ):
            errors.append(
                "curation_contract.policy must mention parallel derivative, subordinate status, and support states."
            )


def validate_reader_handoff_contract(
    data: dict[str, Any],
    parts: list[dict[str, Any]],
    chapters: dict[str, dict[str, Any]],
    errors: list[str],
) -> set[str]:
    handoff = data.get("reader_handoff_contract")
    if not isinstance(handoff, dict):
        errors.append("reader_handoff_contract must be an object.")
        return set()

    missing = sorted(REQUIRED_READER_HANDOFF_FIELDS - set(handoff))
    if missing:
        errors.append(f"reader_handoff_contract missing required fields: {missing}")
        return set()

    if handoff.get("schema_version") != "0.1":
        errors.append("reader_handoff_contract.schema_version must be 0.1.")
    if handoff.get("major_version") != "v1.0":
        errors.append("reader_handoff_contract.major_version must be v1.0.")
    if handoff.get("status") not in ALLOWED_READER_HANDOFF_STATUS:
        errors.append(
            f"reader_handoff_contract.status must be one of {sorted(ALLOWED_READER_HANDOFF_STATUS)}."
        )
    if handoff.get("relationship") != "reader_handoff_not_release_record":
        errors.append("reader_handoff_contract.relationship must be reader_handoff_not_release_record.")

    thesis = require_substantive_string(
        "reader_handoff_contract",
        "single_thesis",
        handoff.get("single_thesis"),
        errors,
        min_words=22,
        no_first_person=True,
    ).lower()
    for phrase in ("governed", "stack", "evidence"):
        if thesis and phrase not in thesis:
            errors.append(f"reader_handoff_contract.single_thesis must mention {phrase}.")

    expected_part_ids = [str(part.get("id")) for part in parts]
    expected_part_titles = {str(part.get("id")): str(part.get("title")) for part in parts}
    part_arcs = handoff.get("part_arcs")
    if not isinstance(part_arcs, list) or len(part_arcs) != len(expected_part_ids):
        errors.append("reader_handoff_contract.part_arcs must contain exactly one record per book part.")
    else:
        seen_parts: list[str] = []
        for index, arc in enumerate(part_arcs):
            owner = f"reader_handoff_contract.part_arcs[{index}]"
            if not isinstance(arc, dict):
                errors.append(f"{owner} must be an object.")
                continue
            missing_arc = sorted(REQUIRED_PART_ARC_FIELDS - set(arc))
            if missing_arc:
                errors.append(f"{owner} missing required fields: {missing_arc}")
                continue
            part_id = arc.get("part_id")
            if not isinstance(part_id, str) or part_id not in expected_part_ids:
                errors.append(f"{owner}: part_id must reference a manifest part.")
            else:
                seen_parts.append(part_id)
                if arc.get("title") != expected_part_titles.get(part_id):
                    errors.append(f"{owner}: title must match book_structure.json title.")
            for key in ("reader_arc", "reader_stakes", "handoff_payoff"):
                require_substantive_string(owner, key, arc.get(key), errors, min_words=10, no_first_person=True)
        if seen_parts != expected_part_ids:
            errors.append("reader_handoff_contract.part_arcs must follow book_structure.json part order.")

    signatures = handoff.get("signature_ideas")
    if not isinstance(signatures, list) or not 8 <= len(signatures) <= 12:
        errors.append("reader_handoff_contract.signature_ideas must contain 8 to 12 records.")
    else:
        seen_signatures: set[str] = set()
        for index, idea in enumerate(signatures):
            owner = f"reader_handoff_contract.signature_ideas[{index}]"
            if not isinstance(idea, dict):
                errors.append(f"{owner} must be an object.")
                continue
            missing_idea = sorted(REQUIRED_SIGNATURE_IDEA_FIELDS - set(idea))
            if missing_idea:
                errors.append(f"{owner} missing required fields: {missing_idea}")
                continue
            idea_id = idea.get("id")
            if not isinstance(idea_id, str) or not idea_id.strip():
                errors.append(f"{owner}: id must be a non-empty string.")
            elif idea_id in seen_signatures:
                errors.append(f"{owner}: duplicate id {idea_id}.")
            else:
                seen_signatures.add(idea_id)
            require_substantive_string(owner, "label", idea.get("label"), errors, min_words=2)
            require_substantive_string(
                owner, "reader_promise", idea.get("reader_promise"), errors, min_words=8, no_first_person=True
            )
            anchors = require_string_list(owner, "anchor_chapter_ids", idea.get("anchor_chapter_ids"), errors)
            invalid = sorted(anchor for anchor in anchors if anchor not in chapters)
            if invalid:
                errors.append(f"{owner}: anchor_chapter_ids reference unknown chapters: {invalid}")

    figures = handoff.get("key_figure_targets")
    if not isinstance(figures, list) or not 8 <= len(figures) <= 12:
        errors.append("reader_handoff_contract.key_figure_targets must contain 8 to 12 records.")
    else:
        seen_figures: set[str] = set()
        for index, figure in enumerate(figures):
            owner = f"reader_handoff_contract.key_figure_targets[{index}]"
            if not isinstance(figure, dict):
                errors.append(f"{owner} must be an object.")
                continue
            missing_figure = sorted(REQUIRED_FIGURE_TARGET_FIELDS - set(figure))
            if missing_figure:
                errors.append(f"{owner} missing required fields: {missing_figure}")
                continue
            figure_id = figure.get("id")
            if not isinstance(figure_id, str) or not figure_id.strip():
                errors.append(f"{owner}: id must be a non-empty string.")
            elif figure_id in seen_figures:
                errors.append(f"{owner}: duplicate id {figure_id}.")
            else:
                seen_figures.add(figure_id)
            if figure.get("status") not in ALLOWED_FIGURE_TARGET_STATUS:
                errors.append(
                    f"{owner}: status must be one of {sorted(ALLOWED_FIGURE_TARGET_STATUS)}."
                )
            require_substantive_string(owner, "working_title", figure.get("working_title"), errors, min_words=3)
            require_substantive_string(owner, "purpose", figure.get("purpose"), errors, min_words=10, no_first_person=True)
            candidates = require_string_list(
                owner, "candidate_chapter_ids", figure.get("candidate_chapter_ids"), errors
            )
            invalid = sorted(candidate for candidate in candidates if candidate not in chapters)
            if invalid:
                errors.append(f"{owner}: candidate_chapter_ids reference unknown chapters: {invalid}")
            boundary = require_substantive_string(
                owner, "release_boundary", figure.get("release_boundary"), errors, min_words=8, no_first_person=True
            ).lower()
            if boundary and ("not a completed" not in boundary or "not reviewed" not in boundary):
                errors.append(f"{owner}: release_boundary must state the target is not a completed and not reviewed artifact.")

    voice_slots = handoff.get("corben_voice_pass_slots")
    slot_ids: set[str] = set()
    if not isinstance(voice_slots, list) or not 8 <= len(voice_slots) <= 12:
        errors.append("reader_handoff_contract.corben_voice_pass_slots must contain 8 to 12 records.")
    else:
        for index, slot in enumerate(voice_slots):
            owner = f"reader_handoff_contract.corben_voice_pass_slots[{index}]"
            if not isinstance(slot, dict):
                errors.append(f"{owner} must be an object.")
                continue
            missing_slot = sorted(REQUIRED_VOICE_SLOT_FIELDS - set(slot))
            if missing_slot:
                errors.append(f"{owner} missing required fields: {missing_slot}")
                continue
            slot_id = slot.get("slot_id")
            if not isinstance(slot_id, str) or not slot_id.strip():
                errors.append(f"{owner}: slot_id must be a non-empty string.")
            elif slot_id in slot_ids:
                errors.append(f"{owner}: duplicate slot_id {slot_id}.")
            else:
                slot_ids.add(slot_id)
            require_substantive_string(owner, "location", slot.get("location"), errors, min_words=3)
            require_substantive_string(owner, "prompt", slot.get("prompt"), errors, min_words=10)
            if slot.get("requires_author_input") is not True:
                errors.append(f"{owner}: requires_author_input must be true.")
            if slot.get("must_not_fabricate") is not True:
                errors.append(f"{owner}: must_not_fabricate must be true.")
            source_chapter_ids = require_string_list(
                owner, "source_chapter_ids", slot.get("source_chapter_ids"), errors
            )
            invalid = sorted(chapter_id for chapter_id in source_chapter_ids if chapter_id not in chapters)
            if invalid:
                errors.append(f"{owner}: source_chapter_ids reference unknown chapters: {invalid}")

    non_claims = require_string_list("reader_handoff_contract", "non_claims", handoff.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("not a reader release", "does not promote", "does not fabricate"):
        if phrase not in non_claim_text:
            errors.append(f"reader_handoff_contract.non_claims must include boundary phrase: {phrase}")

    return slot_ids


def validate_curation_contract(data: dict[str, Any], errors: list[str]) -> dict[str, Any] | None:
    contract_ref = data.get("curation_contract")
    if not isinstance(contract_ref, dict) or not isinstance(contract_ref.get("path"), str):
        return None
    contract_path = ROOT / contract_ref["path"]
    if not contract_path.exists():
        return None

    contract = load_json(contract_path)
    if not isinstance(contract, dict):
        errors.append(f"{rel(contract_path)} must contain an object.")
        return None

    missing = sorted(REQUIRED_CURATION_CONTRACT_FIELDS - set(contract))
    if missing:
        errors.append(f"{rel(contract_path)} missing required fields: {missing}")
        return contract

    if contract.get("schema_version") != "0.1":
        errors.append(f"{rel(contract_path)} schema_version must be 0.1.")
    if contract.get("major_version") != "v1.0":
        errors.append(f"{rel(contract_path)} major_version must be v1.0.")
    if contract.get("status") not in ALLOWED_CURATION_CONTRACT_STATUS:
        errors.append(f"{rel(contract_path)} status must be active_contract.")
    if contract.get("canonical_relationship") != "parallel_derivative_not_equal_authority":
        errors.append(f"{rel(contract_path)} canonical_relationship must be parallel_derivative_not_equal_authority.")

    expected_paths = {
        "manifest": "editions/reader_manuscript/v1_0/manifest.json",
        "contract_doc": "docs/curated_reader_source_contract.md",
        "curated_chapter_dir": "editions/reader_manuscript/v1_0/chapters",
    }
    for key, expected_value in expected_paths.items():
        if contract.get(key) != expected_value:
            errors.append(f"{rel(contract_path)} {key} must be {expected_value}.")
        if isinstance(contract.get(key), str):
            require_existing_path(f"{rel(contract_path)} {key}", contract[key], errors)

    record_fields = set(
        require_string_list(
            "curation contract",
            "chapter_record_required_fields",
            contract.get("chapter_record_required_fields"),
            errors,
        )
    )
    missing_fields = sorted(REQUIRED_CURATED_CHAPTER_RECORD_FIELDS - record_fields)
    if missing_fields:
        errors.append(f"curation contract chapter_record_required_fields missing {missing_fields}.")

    allowed = require_string_list(
        "curation contract", "allowed_edit_scopes", contract.get("allowed_edit_scopes"), errors
    )
    if "pacing" not in allowed or "section flow" not in allowed:
        errors.append("curation contract allowed_edit_scopes must include pacing and section flow.")

    blocked = require_string_list(
        "curation contract", "blocked_edit_scopes", contract.get("blocked_edit_scopes"), errors
    )
    blocked_text = " ".join(blocked).lower()
    for phrase in ("support-state", "source boundary", "proof/test", "release artifact"):
        if phrase not in blocked_text:
            errors.append(f"curation contract blocked_edit_scopes must mention {phrase}.")

    checks = require_string_list(
        "curation contract",
        "meaning_preservation_checks",
        contract.get("meaning_preservation_checks"),
        errors,
    )
    checks_text = " ".join(checks).lower()
    for phrase in ("support-state", "source boundary", "proof/test", "implementation horizon", "release blocker"):
        if phrase not in checks_text:
            errors.append(f"curation contract meaning_preservation_checks must mention {phrase}.")

    blockers = set(
        require_string_list(
            "curation contract",
            "required_release_blockers_before_release",
            contract.get("required_release_blockers_before_release"),
            errors,
        )
    )
    missing_blockers = REQUIRED_CURATION_RELEASE_BLOCKERS - blockers
    if missing_blockers:
        errors.append(f"curation contract required_release_blockers_before_release missing {sorted(missing_blockers)}.")

    commands = require_string_list(
        "curation contract", "required_commands", contract.get("required_commands"), errors
    )
    for command in (
        "python3 scripts/validate_reader_manuscript_manifest.py",
        "python3 scripts/validate_reader_spine.py --check",
        "python3 scripts/validate_reader_evidence_boundaries.py --check",
    ):
        if command not in commands:
            errors.append(f"curation contract required_commands must include {command}.")

    modes = contract.get("graduation_modes")
    if not isinstance(modes, list) or not modes:
        errors.append("curation contract graduation_modes must be a non-empty list.")
    else:
        seen_modes: set[str] = set()
        for index, mode in enumerate(modes):
            if not isinstance(mode, dict):
                errors.append(f"curation contract graduation_modes[{index}] must be an object.")
                continue
            status = mode.get("status")
            if status not in {"drafting", "reconciliation", "release_candidate"}:
                errors.append(f"curation contract graduation_modes[{index}].status is invalid.")
            else:
                seen_modes.add(status)
            meaning = mode.get("meaning")
            if not isinstance(meaning, str) or len(meaning.split()) < 8:
                errors.append(f"curation contract graduation_modes[{index}].meaning must be substantive.")
        for required_mode in ("drafting", "reconciliation", "release_candidate"):
            if required_mode not in seen_modes:
                errors.append(f"curation contract graduation_modes must include {required_mode}.")

    non_claims = require_string_list("curation contract", "non_claims", contract.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("does not create", "does not promote", "not equal"):
        if phrase not in non_claim_text:
            errors.append(f"curation contract non_claims must include boundary phrase: {phrase}")

    doc_value = contract.get("contract_doc")
    if isinstance(doc_value, str) and (ROOT / doc_value).exists():
        text = (ROOT / doc_value).read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in (
            "not equal authority",
            "claim text meaning",
            "support-state meaning",
            "source-boundary meaning",
            "proof/test status",
            "implementation horizons",
            "release blockers",
        ):
            if phrase not in text:
                errors.append(f"{doc_value} must include curation boundary phrase: {phrase}")

    return contract


def validate_companion_note_routing(
    data: dict[str, Any],
    chapters: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    routing_ref = data.get("companion_note_routing")
    if not isinstance(routing_ref, dict) or not isinstance(routing_ref.get("path"), str):
        return

    routing_path = ROOT / routing_ref["path"]
    if not routing_path.exists():
        return
    routing = load_json(routing_path)
    if not isinstance(routing, dict):
        errors.append(f"{rel(routing_path)} must contain an object.")
        return

    if routing.get("schema_version") != "0.1":
        errors.append(f"{rel(routing_path)} schema_version must be 0.1.")
    if routing.get("major_version") != "v1.0":
        errors.append(f"{rel(routing_path)} major_version must be v1.0.")
    if routing.get("status") != "active_review_routing":
        errors.append(f"{rel(routing_path)} status must be active_review_routing.")
    purpose = routing.get("purpose")
    if not isinstance(purpose, str) or "reader spine" not in purpose or "companion" not in purpose:
        errors.append(f"{rel(routing_path)} purpose must mention reader spine and companion routing.")

    source_refs = require_string_list("companion-note routing", "source_review_refs", routing.get("source_review_refs"), errors)
    for ref in source_refs:
        path = ref.split("#", 1)[0]
        if path and not (ROOT / path).exists():
            errors.append(f"companion-note routing source_review_refs path does not exist: {path}")

    non_claims = require_string_list("companion-note routing", "non_claims", routing.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("not a reader release", "does not move meaning-critical uncertainty", "does not promote"):
        if phrase not in non_claim_text:
            errors.append(f"companion-note routing non_claims must include boundary phrase: {phrase}")

    matrix_path = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_review_matrix.json"
    matrix = load_json(matrix_path) if matrix_path.exists() else {}
    matrix_rows = matrix.get("chapters", []) if isinstance(matrix, dict) else []
    companion_candidates = {
        str(row.get("chapter_id"))
        for row in matrix_rows
        if isinstance(row, dict)
        and "companion_note_candidate" in [str(item) for item in row.get("dispositions", [])]
    }

    records = routing.get("records")
    if not isinstance(records, list) or not records:
        errors.append("companion-note routing records must be a non-empty list.")
        return

    seen: set[str] = set()
    for index, record in enumerate(records):
        owner = f"companion_note_routing.records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{owner} must be an object.")
            continue
        chapter_id = record.get("chapter_id")
        if not isinstance(chapter_id, str) or chapter_id not in chapters:
            errors.append(f"{owner}: chapter_id must reference a manifest chapter.")
            continue
        if chapter_id in seen:
            errors.append(f"{owner}: duplicate chapter_id {chapter_id}.")
        seen.add(chapter_id)
        if chapter_id not in companion_candidates:
            errors.append(f"{owner}: {chapter_id} is not marked companion_note_candidate in the review matrix.")

        expected_title = chapters[chapter_id].get("title")
        if record.get("title") != expected_title:
            errors.append(f"{owner}: title must match book_structure.json title {expected_title!r}.")
        if record.get("routing_decision") not in ALLOWED_ROUTING_STATUS:
            errors.append(f"{owner}: routing_decision must be one of {sorted(ALLOWED_ROUTING_STATUS)}.")

        for key in ("reader_treatment", "companion_treatment", "audio_treatment"):
            value = record.get(key)
            if not isinstance(value, str) or len(value.split()) < 8:
                errors.append(f"{owner}: {key} must be a substantive sentence.")

        companion_note_file = record.get("companion_note_file")
        companion_note_status = record.get("companion_note_status")
        if companion_note_file is not None or companion_note_status is not None:
            if companion_note_status != "drafting_not_release_reviewed":
                errors.append(
                    f"{owner}: companion_note_status must be drafting_not_release_reviewed."
                )
            if (
                not isinstance(companion_note_file, str)
                or not companion_note_file.startswith("editions/reader_manuscript/v1_0/companion_notes/")
            ):
                errors.append(
                    f"{owner}: companion_note_file must be under "
                    "editions/reader_manuscript/v1_0/companion_notes/."
                )
            else:
                companion_note_path = ROOT / companion_note_file
                if not companion_note_path.exists():
                    errors.append(f"{owner}: companion_note_file does not exist: {companion_note_file}")
                else:
                    note_text = companion_note_path.read_text(encoding="utf-8", errors="ignore").lower()
                    for phrase in (
                        chapter_id.lower(),
                        "not a reader release",
                        "does not promote",
                        "does not prove model quality",
                        "reader spine",
                        "audio",
                    ):
                        if phrase not in note_text:
                            errors.append(
                                f"{owner}: companion note {companion_note_file} "
                                f"must include boundary phrase: {phrase}"
                            )

        for key in ("dense_material", "must_remain_in_reader", "companion_note_material", "release_blockers", "non_claims"):
            require_string_list(owner, key, record.get(key), errors)

        blockers = {str(item) for item in record.get("release_blockers", []) if isinstance(item, str)}
        missing_blockers = REQUIRED_ROUTING_RELEASE_BLOCKERS - blockers
        if missing_blockers:
            errors.append(f"{owner}: release_blockers missing {sorted(missing_blockers)}.")

        reader_boundary = " ".join(str(item) for item in record.get("must_remain_in_reader", [])).lower()
        if not any(term in reader_boundary for term in ("claim", "authority", "support", "boundary", "approval")):
            errors.append(f"{owner}: must_remain_in_reader must preserve a claim, authority, support, or approval boundary.")

    missing_routes = companion_candidates - seen
    extra_routes = seen - companion_candidates
    if missing_routes:
        errors.append(f"companion-note routing missing matrix candidates: {sorted(missing_routes)}")
    if extra_routes:
        errors.append(f"companion-note routing has non-candidate records: {sorted(extra_routes)}")


def validate_chapter_records(
    data: dict[str, Any],
    chapters: dict[str, dict[str, Any]],
    contract: dict[str, Any] | None,
    voice_slot_ids: set[str],
    errors: list[str],
) -> None:
    records = data.get("chapter_records")
    if not isinstance(records, list):
        errors.append("chapter_records must be a list.")
        return

    allowed_scopes = set(contract.get("allowed_edit_scopes", [])) if isinstance(contract, dict) else set()
    required_pre_release_blockers = (
        set(contract.get("required_release_blockers_before_release", [])) if isinstance(contract, dict) else set()
    )
    seen: set[str] = set()
    for index, record in enumerate(records):
        owner = f"chapter_records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{owner} must be an object.")
            continue
        chapter_id = record.get("chapter_id")
        if not isinstance(chapter_id, str) or chapter_id not in chapters:
            errors.append(f"{owner}: chapter_id must reference a manifest chapter.")
            continue
        if chapter_id in seen:
            errors.append(f"{owner}: duplicate chapter_id {chapter_id}.")
        seen.add(chapter_id)

        expected_title = chapters[chapter_id].get("title")
        if record.get("title") != expected_title:
            errors.append(f"{owner}: title must match book_structure.json title {expected_title!r}.")

        file_path = record.get("file")
        if not isinstance(file_path, str) or not file_path.startswith("editions/reader_manuscript/v1_0/chapters/"):
            errors.append(f"{owner}: file must be under editions/reader_manuscript/v1_0/chapters/.")
        elif not (ROOT / file_path).exists():
            errors.append(f"{owner}: curated chapter file does not exist: {file_path}")

        status = record.get("reconciliation_status")
        if status not in ALLOWED_RECONCILIATION_STATUS:
            errors.append(f"{owner}: reconciliation_status must be one of {sorted(ALLOWED_RECONCILIATION_STATUS)}.")

        for key in ("generated_baseline_ref", "live_source_ref", "claim_boundary_ref", "implementation_horizon_ref"):
            if not isinstance(record.get(key), str) or not record[key].strip():
                errors.append(f"{owner}: {key} must be a non-empty string.")

        scopes = require_string_list(owner, "curation_scope", record.get("curation_scope"), errors)
        if allowed_scopes:
            invalid_scopes = sorted(scope for scope in scopes if scope not in allowed_scopes)
            if invalid_scopes:
                errors.append(f"{owner}: curation_scope includes scopes not allowed by contract: {invalid_scopes}")

        require_substantive_string(
            owner,
            "reader_stakes",
            record.get("reader_stakes"),
            errors,
            min_words=10,
            no_first_person=True,
        )
        require_substantive_string(
            owner,
            "reader_payoff",
            record.get("reader_payoff"),
            errors,
            min_words=10,
            no_first_person=True,
        )
        voice_slots = require_string_list(owner, "voice_pass_slot_ids", record.get("voice_pass_slot_ids"), errors)
        invalid_voice_slots = sorted(slot_id for slot_id in voice_slots if slot_id not in voice_slot_ids)
        if invalid_voice_slots:
            errors.append(f"{owner}: voice_pass_slot_ids reference unknown slots: {invalid_voice_slots}")

        divergence_summary = record.get("divergence_summary")
        if not isinstance(divergence_summary, str) or len(divergence_summary.split()) < 8:
            errors.append(f"{owner}: divergence_summary must be a substantive sentence.")

        preservation_checks = require_string_list(
            owner,
            "meaning_preservation_checks",
            record.get("meaning_preservation_checks"),
            errors,
        )
        preservation_text = " ".join(preservation_checks).lower()
        for phrase in ("support-state", "source boundary", "proof/test", "implementation horizon", "release blocker"):
            if phrase not in preservation_text:
                errors.append(f"{owner}: meaning_preservation_checks must mention {phrase}.")

        release_blockers = set(require_string_list(owner, "release_blockers", record.get("release_blockers"), errors))
        if data.get("status") not in {"release_candidate", "released"} and required_pre_release_blockers:
            missing_blockers = sorted(required_pre_release_blockers - release_blockers)
            if missing_blockers:
                errors.append(f"{owner}: release_blockers missing pre-release blockers {missing_blockers}.")

        if not isinstance(record.get("canonical_change_required"), bool):
            errors.append(f"{owner}: canonical_change_required must be a boolean.")
        canonical_ref = record.get("canonical_change_ref")
        if record.get("canonical_change_required") is True:
            if not isinstance(canonical_ref, str) or len(canonical_ref.split()) < 3:
                errors.append(f"{owner}: canonical_change_ref must explain the live-source change requirement.")
        elif not isinstance(canonical_ref, str):
            errors.append(f"{owner}: canonical_change_ref must be a string.")

        review_notes = record.get("review_notes")
        if not isinstance(review_notes, str) or len(review_notes.split()) < 5:
            errors.append(f"{owner}: review_notes must be a substantive note.")

    if data.get("status") in {"release_candidate", "released"}:
        missing = sorted(set(chapters) - seen)
        if missing:
            errors.append(f"{data['status']} curated reader manuscript missing chapter records: {missing}")
        unreconciled = [
            record.get("chapter_id")
            for record in records
            if isinstance(record, dict) and record.get("reconciliation_status") != "reconciled"
        ]
        if unreconciled:
            errors.append(f"{data['status']} curated reader manuscript has unreconciled chapters: {unreconciled}")


def validate_reconciliation_report(data: dict[str, Any], errors: list[str]) -> None:
    report = data.get("reconciliation_report")
    if not isinstance(report, dict):
        errors.append("reconciliation_report must be an object.")
        return
    if report.get("required_before_release") is not True:
        errors.append("reconciliation_report.required_before_release must be true.")
    path = report.get("path")
    if not isinstance(path, str) or not path.startswith("editions/reader_manuscript/v1_0/"):
        errors.append("reconciliation_report.path must stay under editions/reader_manuscript/v1_0/.")
    status = report.get("status")
    if status not in ALLOWED_RECONCILIATION_STATUS:
        errors.append(f"reconciliation_report.status must be one of {sorted(ALLOWED_RECONCILIATION_STATUS)}.")
    if isinstance(path, str):
        report_path = ROOT / path
        if report_path.exists():
            text = report_path.read_text(encoding="utf-8", errors="ignore").lower()
            for phrase in (
                "not a reader release record",
                "not a support-state promotion",
                "live ai/research book",
                "chapter_review_matrix.json",
                "generated reader source",
                "proof/test status",
                "implementation horizons",
                "release blockers",
            ):
                if phrase not in text:
                    errors.append(f"{path} must include reconciliation boundary phrase: {phrase}")
        elif data.get("status") in {"release_candidate", "released"}:
            errors.append(f"release-ready curated reader manuscript requires reconciliation report: {path}")


def validate_docs_reference_manifest(errors: list[str]) -> None:
    required_mentions = {
        ROOT / "editions" / "README.md": "editions/reader_manuscript/",
        ROOT / "docs" / "release_editions_plan.md": "editions/reader_manuscript/v1_0/manifest.json",
        ROOT / "docs" / "major_version_release_runbook.md": "python3 scripts/validate_reader_manuscript_manifest.py",
        ROOT / "README.md": "scripts/validate_reader_manuscript_manifest.py",
        ROOT / "docs" / "repository_map.md": "scripts/sync_reader_chapter_review_matrix.py --check",
    }
    for path, needle in required_mentions.items():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if needle not in text:
            errors.append(f"{rel(path)} must mention {needle}.")


def main() -> None:
    errors: list[str] = []
    data = load_json(MANIFEST)
    if not isinstance(data, dict):
        errors.append(f"{rel(MANIFEST)} must contain an object.")
        data = {}
    structure = load_json(ROOT / "book_structure.json")
    parts = flatten_parts(structure if isinstance(structure, dict) else {})
    chapters = flatten_chapters(structure if isinstance(structure, dict) else {})

    validate_manifest(data, errors)
    curation_contract = validate_curation_contract(data, errors)
    voice_slot_ids = validate_reader_handoff_contract(data, parts, chapters, errors)
    validate_chapter_records(data, chapters, curation_contract, voice_slot_ids, errors)
    validate_companion_note_routing(data, chapters, errors)
    validate_reconciliation_report(data, errors)
    validate_docs_reference_manifest(errors)

    if errors:
        print("Reader manuscript manifest validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Reader manuscript manifest validation passed: "
        f"{data.get('status')} with {len(data.get('chapter_records', []))} curated chapter record(s)."
    )


if __name__ == "__main__":
    main()
