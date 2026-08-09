#!/usr/bin/env python3
"""Build the Manim v2 production ledger from canonical book structure.

Chapters without a generation-one packet enter as planned generation-two
targets with no predecessor. The ledger never fabricates a legacy packet for
count symmetry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "visual_edition/manim_v2_production_ledger.json"
PREVIEW_BINDINGS = ROOT / "visual_edition/youtube_preview_bindings.json"
PREVIEW_HISTORY = ROOT / "visual_edition/youtube_preview_history_2026-07-30.json"
SKILL_COMPONENT_GATES = {
    "skills/asi-stack-manim-videos/references/writing-and-story.md": "treatment",
    "skills/asi-stack-manim-videos/references/learning-and-engagement.md": "treatment",
    "skills/asi-stack-manim-videos/references/art-direction-and-motion.md": "treatment",
    "skills/asi-stack-manim-videos/references/audio-and-accessibility.md": "treatment",
    "skills/asi-stack-manim-videos/references/research-basis.md": "treatment",
    "skills/asi-stack-manim-videos/references/asi-stack-pipeline.md": "treatment",
    "skills/asi-stack-manim-videos/references/manim-patterns.md": "animatic",
    "skills/asi-stack-manim-videos/references/experience-review.md": "animatic",
    "skills/asi-stack-manim-videos/scripts/audit_video_plan.py": "treatment",
    "skills/asi-stack-manim-videos/scripts/audit_scene_source.py": "animatic",
    "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py": "animatic",
    "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py": "picture_and_sound_lock",
    "skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py": "animatic",
    "skills/asi-stack-manim-videos/scripts/sample_video_beats.py": "animatic",
    "skills/asi-stack-manim-videos/scripts/audit_av_experience.py": "picture_and_sound_lock",
    "skills/asi-stack-manim-videos/scripts/build_caption_review_sheet.py": "picture_and_sound_lock",
}


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def load_path(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def optional_digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def skill_bundle_digest() -> str:
    base = ROOT / "skills/asi-stack-manim-videos"
    paths = [base / "SKILL.md", base / "agents/openai.yaml"]
    paths.extend(sorted((base / "references").glob("*.md")))
    paths.extend(sorted((base / "scripts").glob("*.py")))
    hasher = hashlib.sha256()
    for path in sorted(paths):
        relative = path.relative_to(ROOT).as_posix().encode("utf-8")
        hasher.update(len(relative).to_bytes(4, "big"))
        hasher.update(relative)
        body = path.read_bytes()
        hasher.update(len(body).to_bytes(8, "big"))
        hasher.update(body)
    return hasher.hexdigest()


def skill_component_digests() -> dict[str, str]:
    return {path: digest(path) for path in sorted(SKILL_COMPONENT_GATES)}


def primitive_regression_bundle_digest() -> str:
    paths = (
        "schemas/manim_primitive_regression.schema.json",
        "visual_edition/primitive_regression_manifest.json",
        "visual_edition/tests/primitive_regression_scenes.py",
        "visual_edition/tests/control_data/asi_visuals_v1.npz",
    )
    hasher = hashlib.sha256()
    for relative_value in paths:
        relative = relative_value.encode("utf-8")
        hasher.update(len(relative).to_bytes(4, "big"))
        hasher.update(relative)
        body = (ROOT / relative_value).read_bytes()
        hasher.update(len(body).to_bytes(8, "big"))
        hasher.update(body)
    return hasher.hexdigest()


def chapter_source_context_digest(chapter: dict) -> str:
    inventory = {
        row["id"]: row for row in load("sources/source_inventory.json")
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    bindings = []
    for source_id in chapter.get("source_ids", []):
        relative = f"sources/source_notes/{source_id}.md"
        path = ROOT / relative
        if not path.is_file():
            raise ValueError(f"{chapter.get('id')}: assigned source note is missing: {relative}")
        bindings.append({
            "source_id": source_id,
            "inventory_record": inventory.get(source_id),
            "note_path": relative,
            "note_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    body = json.dumps(bindings, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def canonical_chapters() -> list[dict]:
    structure = load("book_structure.json")
    return [chapter for part in structure["parts"] for chapter in part["chapters"]]


def preserved_state() -> tuple[dict[str, dict], dict[str, object]]:
    if not OUTPUT.is_file():
        return {}, {}
    current = json.loads(OUTPUT.read_text(encoding="utf-8"))
    entries = {
        entry["chapter_id"]: {
            "chapter_sha256": entry.get("chapter_sha256"),
            "source_context_sha256": entry.get("source_context_sha256"),
            "target": entry["target"],
        }
        for entry in current.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("target"), dict)
    }
    metadata = {
        key: current.get(key)
        for key in (
            "authoring_standard_sha256",
            "authoring_bundle_sha256",
            "authoring_component_sha256",
            "treatment_schema_sha256",
            "beat_plan_schema_sha256",
            "experience_review_schema_sha256",
            "review_context_schema_sha256",
            "av_diagnostics_schema_sha256",
            "frame_sample_manifest_schema_sha256",
            "render_receipt_schema_sha256",
            "sandbox_policy_receipt_schema_sha256",
            "narration_toolchain_sha256",
            "visual_grammar_sha256",
            "visual_toolchain_sha256",
            "primitive_library_sha256",
            "primitive_regression_bundle_sha256",
            "scene_source_auditor_sha256",
            "isolated_render_runner_sha256",
            "primitive_regression_manifest_sha256",
        )
    }
    return entries, metadata


def target_for(
    chapter_id: str,
    has_current_preview: bool,
    prior: dict | None,
    reopen_from: str | None,
) -> dict:
    base = f"visual_edition/chapters/{chapter_id}"
    narration_path = ROOT / f"{base}/generation-2/narration.txt"
    narration_sha256 = optional_digest(narration_path)
    treatment_path = ROOT / f"{base}/generation-2/treatment.json"
    treatment_sha256 = optional_digest(treatment_path)
    beat_plan_path = ROOT / f"{base}/generation-2/beat_plan.json"
    beat_plan_sha256 = optional_digest(beat_plan_path)
    scene_path = ROOT / f"{base}/generation-2/scene.py"
    scene_sha256 = optional_digest(scene_path)
    caption_path = ROOT / f"{base}/generation-2/captions.vtt"
    caption_sha256 = optional_digest(caption_path)
    transcript_path = ROOT / f"{base}/generation-2/transcript.md"
    transcript_sha256 = optional_digest(transcript_path)
    thumbnail_path = ROOT / f"{base}/generation-2/thumbnail.svg"
    thumbnail_sha256 = optional_digest(thumbnail_path)
    master_path = ROOT / f"build/visual_edition/generation-2/final/{chapter_id}.mp4"
    master_sha256 = optional_digest(master_path) or (prior or {}).get("master_sha256")
    receipt_path = ROOT / f"{base}/generation-2/render_receipt.json"
    render_receipt_sha256 = optional_digest(receipt_path)
    if beat_plan_sha256 and treatment_sha256 and narration_sha256:
        stage = "beat_planned"
    elif treatment_sha256:
        stage = "treated"
    elif narration_sha256:
        stage = "narration_draft"
    else:
        stage = "planned"
    default = {
        "generation": 2,
        "stage": stage,
        "treatment_path": f"{base}/generation-2/treatment.json",
        "treatment_sha256": treatment_sha256,
        "beat_plan_path": f"{base}/generation-2/beat_plan.json",
        "beat_plan_sha256": beat_plan_sha256,
        "scene_path": f"{base}/generation-2/scene.py",
        "scene_sha256": scene_sha256,
        "narration_path": f"{base}/generation-2/narration.txt",
        "narration_sha256": narration_sha256,
        "caption_path": f"{base}/generation-2/captions.vtt",
        "caption_sha256": caption_sha256,
        "transcript_path": f"{base}/generation-2/transcript.md",
        "transcript_sha256": transcript_sha256,
        "thumbnail_path": f"{base}/generation-2/thumbnail.svg",
        "thumbnail_sha256": thumbnail_sha256,
        "master_path": f"build/visual_edition/generation-2/final/{chapter_id}.mp4",
        "master_sha256": master_sha256,
        "render_receipt_path": f"{base}/generation-2/render_receipt.json",
        "render_receipt_sha256": render_receipt_sha256,
        "experience_review_paths": {
            "animatic": f"{base}/generation-2/reviews/animatic.json",
            "picture_and_sound_lock": f"{base}/generation-2/reviews/picture_and_sound_lock.json",
            "release_candidate": f"{base}/generation-2/reviews/release_candidate.json",
            "independent_release_candidate": f"{base}/generation-2/reviews/independent_release_candidate.json"
        },
        "gates": {
            "treatment": "revise" if treatment_sha256 else "not_started",
            "script": "revise" if treatment_sha256 and narration_sha256 else "not_started",
            "beat_plan": "revise" if treatment_sha256 and narration_sha256 and beat_plan_sha256 else "not_started",
            "animatic": "not_started",
            "picture_and_sound_lock": "not_started",
            "release_candidate": "not_started",
            "independent_release_candidate": "not_started",
            "technical": "not_started",
            "claim_fidelity": "not_started",
            "accepted": "not_started"
        },
        "youtube_state": "not_ready",
        "youtube_video_id": None,
        "quarto_embed_state": "predecessor_preview" if has_current_preview else "absent"
    }
    if not prior:
        return default
    merged = dict(default)
    merged.update(prior)
    merged["experience_review_paths"] = {
        **default["experience_review_paths"],
        **prior.get("experience_review_paths", {})
    }
    merged["gates"] = {**default["gates"], **prior.get("gates", {})}

    gate_rank = {
        "treatment": 0,
        "script": 1,
        "beat_plan": 2,
        "animatic": 3,
        "picture_and_sound_lock": 4,
        "release_candidate": 5,
    }
    changed_inputs = (
        ("treatment_sha256", treatment_sha256, "treatment"),
        ("narration_sha256", narration_sha256, "script"),
        ("beat_plan_sha256", beat_plan_sha256, "beat_plan"),
        ("scene_sha256", scene_sha256, "animatic"),
        ("caption_sha256", caption_sha256, "picture_and_sound_lock"),
        ("transcript_sha256", transcript_sha256, "picture_and_sound_lock"),
        ("thumbnail_sha256", thumbnail_sha256, "release_candidate"),
        ("master_sha256", master_sha256, "picture_and_sound_lock"),
        ("render_receipt_sha256", render_receipt_sha256, "picture_and_sound_lock"),
    )
    reopen_candidates = [reopen_from] if reopen_from else []
    reopen_candidates.extend(
        gate for field, current, gate in changed_inputs
        if prior.get(field) != current
    )
    earliest = min(reopen_candidates, key=gate_rank.get) if reopen_candidates else None

    current_identities = {
        field: current for field, current, _ in changed_inputs
    }
    current_identities.update({
        "treatment_path": default["treatment_path"],
        "beat_plan_path": default["beat_plan_path"],
        "scene_path": default["scene_path"],
        "narration_path": default["narration_path"],
        "caption_path": default["caption_path"],
        "transcript_path": default["transcript_path"],
        "thumbnail_path": default["thumbnail_path"],
        "master_path": default["master_path"],
        "render_receipt_path": default["render_receipt_path"],
    })
    merged.update(current_identities)

    if earliest:
        reset_rank = gate_rank[earliest]
        for gate, rank in gate_rank.items():
            if rank >= reset_rank:
                merged["gates"][gate] = default["gates"][gate]
        for gate in ("independent_release_candidate", "technical", "claim_fidelity", "accepted"):
            merged["gates"][gate] = "not_started"
        merged["youtube_state"] = "not_ready"
        merged["youtube_video_id"] = None

    # The current preview binding is authoritative for the live Quarto
    # projection; a withdrawn predecessor must not leave a stale embed state.
    merged["quarto_embed_state"] = (
        "predecessor_preview" if has_current_preview else "absent"
    )
    gates = merged["gates"]
    if gates.get("accepted") == "pass":
        stage = "accepted"
    elif gates.get("release_candidate") == "pass" or gates.get("independent_release_candidate") == "pass":
        stage = "release_candidate"
    elif gates.get("picture_and_sound_lock") == "pass":
        stage = "picture_and_sound_lock"
    elif gates.get("animatic") == "pass":
        stage = "animatic"
    elif gates.get("beat_plan") == "pass" or (beat_plan_sha256 and treatment_sha256 and narration_sha256):
        stage = "beat_planned"
    elif gates.get("script") == "pass":
        stage = "script_passed"
    elif treatment_sha256:
        stage = "treated"
    elif narration_sha256:
        stage = "narration_draft"
    else:
        stage = "planned"
    if merged.get("youtube_state") == "public_current":
        stage = "youtube_current"
    if merged.get("quarto_embed_state") == "generation_2_current":
        stage = "quarto_current"
    merged["stage"] = stage
    return merged


def build() -> dict:
    chapters = canonical_chapters()
    manifest = load("visual_edition/manifest.json")
    packets = {row["chapter_id"]: row for row in manifest["chapters"]}
    binding = load_path(PREVIEW_BINDINGS)
    previews = {row["chapter_id"]: row for row in binding["entries"]}
    history_rows = {}
    if PREVIEW_HISTORY.is_file():
        history = load_path(PREVIEW_HISTORY)
        history_rows = {
            row["chapter_id"]: row for row in history.get("entries", [])
        }
    withdrawn_at = binding.get("withdrawal", {}).get("withdrawn_at_utc")
    history_path = str(PREVIEW_HISTORY.relative_to(ROOT))
    prior_entries, prior_metadata = preserved_state()
    authoring_standard_sha256 = digest("skills/asi-stack-manim-videos/SKILL.md")
    authoring_bundle_sha256 = skill_bundle_digest()
    authoring_component_sha256 = skill_component_digests()
    treatment_schema_sha256 = digest("schemas/manim_treatment.schema.json")
    beat_plan_schema_sha256 = digest("schemas/manim_beat_plan.schema.json")
    experience_review_schema_sha256 = digest("schemas/manim_experience_review.schema.json")
    review_context_schema_sha256 = digest("schemas/manim_review_context_manifest.schema.json")
    av_diagnostics_schema_sha256 = digest("schemas/manim_av_diagnostics.schema.json")
    frame_sample_manifest_schema_sha256 = digest(
        "schemas/manim_frame_sample_manifest.schema.json"
    )
    render_receipt_schema_sha256 = digest("schemas/manim_render_receipt.schema.json")
    sandbox_policy_receipt_schema_sha256 = digest(
        "schemas/manim_sandbox_policy_receipt.schema.json"
    )
    narration_toolchain_sha256 = digest("visual_edition/narration_toolchain.json")
    visual_grammar_sha256 = digest("visual_edition/visual_grammar.json")
    visual_toolchain_sha256 = digest("visual_edition/toolchain.json")
    primitive_library_sha256 = digest("visual_edition/lib/asi_visuals.py")
    scene_source_auditor_sha256 = digest(
        "skills/asi-stack-manim-videos/scripts/audit_scene_source.py"
    )
    isolated_render_runner_sha256 = digest(
        "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py"
    )
    primitive_regression_manifest_sha256 = digest(
        "visual_edition/primitive_regression_manifest.json"
    )
    primitive_regression_bundle_sha256 = primitive_regression_bundle_digest()
    global_reopen_candidates = []
    global_dependencies = (
        ("authoring_standard_sha256", authoring_standard_sha256, "treatment"),
        ("treatment_schema_sha256", treatment_schema_sha256, "treatment"),
        ("beat_plan_schema_sha256", beat_plan_schema_sha256, "beat_plan"),
        ("experience_review_schema_sha256", experience_review_schema_sha256, "animatic"),
        ("review_context_schema_sha256", review_context_schema_sha256, "animatic"),
        ("av_diagnostics_schema_sha256", av_diagnostics_schema_sha256, "picture_and_sound_lock"),
        ("frame_sample_manifest_schema_sha256", frame_sample_manifest_schema_sha256, "animatic"),
        ("render_receipt_schema_sha256", render_receipt_schema_sha256, "picture_and_sound_lock"),
        ("sandbox_policy_receipt_schema_sha256", sandbox_policy_receipt_schema_sha256, "animatic"),
        ("narration_toolchain_sha256", narration_toolchain_sha256, "beat_plan"),
        ("visual_grammar_sha256", visual_grammar_sha256, "animatic"),
        ("visual_toolchain_sha256", visual_toolchain_sha256, "animatic"),
        ("primitive_library_sha256", primitive_library_sha256, "animatic"),
        ("scene_source_auditor_sha256", scene_source_auditor_sha256, "animatic"),
        ("isolated_render_runner_sha256", isolated_render_runner_sha256, "animatic"),
        ("primitive_regression_manifest_sha256", primitive_regression_manifest_sha256, "animatic"),
        ("primitive_regression_bundle_sha256", primitive_regression_bundle_sha256, "animatic"),
    )
    if prior_metadata:
        global_reopen_candidates = [
            gate for key, current, gate in global_dependencies
            if prior_metadata.get(key) != current
        ]
        prior_components = prior_metadata.get("authoring_component_sha256") or {}
        global_reopen_candidates.extend(
            gate for path, gate in SKILL_COMPONENT_GATES.items()
            if prior_components.get(path) != authoring_component_sha256[path]
        )
    global_gate_rank = {
        "treatment": 0, "script": 1, "beat_plan": 2, "animatic": 3,
        "picture_and_sound_lock": 4, "release_candidate": 5,
    }
    global_reopen_from = (
        min(global_reopen_candidates, key=global_gate_rank.get)
        if global_reopen_candidates else None
    )
    entries = []
    cohorts = {
        "owner_reviewed_remediation": [],
        "withdrawn_predecessor_previews": [],
        "current_unlisted_previews": [],
        "not_yet_uploaded": []
    }
    for canonical_position, chapter in enumerate(chapters, start=1):
        chapter_id = chapter["id"]
        chapter_sha256 = digest(chapter["file"])
        source_context_sha256 = chapter_source_context_digest(chapter)
        packet_row = packets.get(chapter_id)
        if not packet_row:
            raise ValueError(f"visual manifest is missing canonical chapter {chapter_id}")
        if canonical_position <= 5:
            cohort = "owner_reviewed_remediation"
        elif canonical_position <= 12:
            cohort = "withdrawn_predecessor_previews"
        elif chapter_id in previews:
            cohort = "current_unlisted_previews"
        else:
            cohort = "not_yet_uploaded"
        cohorts[cohort].append(chapter_id)
        packet_path = packet_row.get("packet_path")
        preview = previews.get(chapter_id)
        historical = history_rows.get(chapter_id)
        if not packet_path and (preview or historical):
            raise ValueError(f"{chapter_id}: YouTube custody exists without a visual packet")
        if not packet_path:
            predecessor = None
        else:
            packet = load(packet_path)
            receipt = packet["render_receipt"]
        if packet_path and preview:
            predecessor = {
                "local_generation": 1,
                "packet_path": packet_path,
                "master_path": f"build/visual_edition/final/{chapter_id}.mp4",
                "master_sha256": receipt["output_sha256"],
                "custody_state": "unlisted_preview_bound",
                "youtube_video_id": preview["video_id"],
                "youtube_visibility": "unlisted",
                "preserve_history": True
            }
        elif packet_path and historical:
            predecessor = {
                "local_generation": 1,
                "packet_path": packet_path,
                "master_path": f"build/visual_edition/final/{chapter_id}.mp4",
                "master_sha256": historical["local_master_sha256"],
                "custody_state": "private_historical_withdrawn",
                "youtube_video_id": historical["video_id"],
                "youtube_visibility": "private",
                "preserve_history": True,
                "withdrawn_at_utc": withdrawn_at or historical["observed_at_utc"],
                "history_record_path": history_path
            }
        elif packet_path:
            predecessor = {
                "local_generation": 1,
                "packet_path": packet_path,
                "master_path": f"build/visual_edition/final/{chapter_id}.mp4",
                "master_sha256": receipt["output_sha256"],
                "custody_state": "local_only",
                "youtube_video_id": None,
                "youtube_visibility": "not_uploaded",
                "preserve_history": True
            }
        entries.append({
            "position": canonical_position,
            "chapter_id": chapter_id,
            "title": chapter["title"],
            "chapter_path": chapter["file"],
            "chapter_sha256": chapter_sha256,
            "source_context_sha256": source_context_sha256,
            "cohort": cohort,
            "predecessor": predecessor,
            "target": target_for(
                chapter_id,
                has_current_preview=preview is not None,
                prior=prior_entries.get(chapter_id, {}).get("target"),
                reopen_from=(
                    "treatment"
                    if (
                        prior_entries.get(chapter_id, {}).get("chapter_sha256") != chapter_sha256
                        or prior_entries.get(chapter_id, {}).get("source_context_sha256")
                        != source_context_sha256
                    )
                    else global_reopen_from
                ),
            )
        })
    counts = {
        "planned": sum(e["target"]["stage"] == "planned" for e in entries),
        "narration_draft": sum(e["target"]["stage"] == "narration_draft" for e in entries),
        "treated": sum(e["target"]["stage"] == "treated" for e in entries),
        "script_passed": sum(e["target"]["gates"]["script"] == "pass" for e in entries),
        "beat_planned": sum(e["target"]["stage"] == "beat_planned" for e in entries),
        "animatic_passed": sum(e["target"]["gates"]["animatic"] == "pass" for e in entries),
        "picture_and_sound_lock_passed": sum(e["target"]["gates"]["picture_and_sound_lock"] == "pass" for e in entries),
        "release_candidate_passed": sum(e["target"]["gates"]["release_candidate"] == "pass" for e in entries),
        "independent_release_candidate_passed": sum(e["target"]["gates"]["independent_release_candidate"] == "pass" for e in entries),
        "accepted_generation_2": sum(e["target"]["gates"]["accepted"] == "pass" for e in entries),
        "youtube_predecessors": len(history_rows),
        "youtube_generation_2_unlisted_preview": len(previews),
        "youtube_generation_2_current": sum(e["target"]["youtube_state"] == "public_current" for e in entries),
        "quarto_generation_2_current": sum(e["target"]["quarto_embed_state"] == "generation_2_current" for e in entries)
    }
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if OUTPUT.is_file():
        generated = json.loads(OUTPUT.read_text(encoding="utf-8")).get("generated_at_utc", generated)
    return {
        "schema_version": "asi_stack.manim_v2_production_ledger.v3",
        "edition_id": "asi-stack-p7.3-visual-edition",
        "generated_at_utc": generated,
        "book_structure_path": "book_structure.json",
        "book_structure_sha256": digest("book_structure.json"),
        "visual_manifest_path": "visual_edition/manifest.json",
        "visual_manifest_sha256": digest("visual_edition/manifest.json"),
        "authoring_standard_path": "skills/asi-stack-manim-videos/SKILL.md",
        "authoring_standard_sha256": authoring_standard_sha256,
        "authoring_bundle_sha256": authoring_bundle_sha256,
        "authoring_component_sha256": authoring_component_sha256,
        "treatment_schema_path": "schemas/manim_treatment.schema.json",
        "treatment_schema_sha256": treatment_schema_sha256,
        "beat_plan_schema_path": "schemas/manim_beat_plan.schema.json",
        "beat_plan_schema_sha256": beat_plan_schema_sha256,
        "experience_review_schema_path": "schemas/manim_experience_review.schema.json",
        "experience_review_schema_sha256": experience_review_schema_sha256,
        "review_context_schema_path": "schemas/manim_review_context_manifest.schema.json",
        "review_context_schema_sha256": review_context_schema_sha256,
        "av_diagnostics_schema_path": "schemas/manim_av_diagnostics.schema.json",
        "av_diagnostics_schema_sha256": av_diagnostics_schema_sha256,
        "frame_sample_manifest_schema_path": "schemas/manim_frame_sample_manifest.schema.json",
        "frame_sample_manifest_schema_sha256": frame_sample_manifest_schema_sha256,
        "render_receipt_schema_path": "schemas/manim_render_receipt.schema.json",
        "render_receipt_schema_sha256": render_receipt_schema_sha256,
        "sandbox_policy_receipt_schema_path": "schemas/manim_sandbox_policy_receipt.schema.json",
        "sandbox_policy_receipt_schema_sha256": sandbox_policy_receipt_schema_sha256,
        "narration_toolchain_path": "visual_edition/narration_toolchain.json",
        "narration_toolchain_sha256": narration_toolchain_sha256,
        "visual_grammar_path": "visual_edition/visual_grammar.json",
        "visual_grammar_sha256": visual_grammar_sha256,
        "visual_toolchain_path": "visual_edition/toolchain.json",
        "visual_toolchain_sha256": visual_toolchain_sha256,
        "primitive_library_path": "visual_edition/lib/asi_visuals.py",
        "primitive_library_sha256": primitive_library_sha256,
        "scene_source_auditor_path": "skills/asi-stack-manim-videos/scripts/audit_scene_source.py",
        "scene_source_auditor_sha256": scene_source_auditor_sha256,
        "isolated_render_runner_path": "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py",
        "isolated_render_runner_sha256": isolated_render_runner_sha256,
        "primitive_regression_manifest_path": "visual_edition/primitive_regression_manifest.json",
        "primitive_regression_manifest_sha256": primitive_regression_manifest_sha256,
        "primitive_regression_bundle_sha256": primitive_regression_bundle_sha256,
        "canonical_chapter_count": len(chapters),
        "target_generation": 2,
        "cohorts": cohorts,
        "acceptance_contract": {
            "required_passes": ["animatic", "picture_and_sound_lock", "release_candidate", "independent_release_candidate"],
            "experience_dimensions": ["teaching_clarity", "composition", "motion_quality", "synchronization", "continuity", "pacing", "voice", "sound_mix", "engagement", "accessibility", "claim_fidelity"],
            "minimum_score_each_scored_dimension": 4,
            "minimum_frame_samples_per_beat": 5,
            "average_may_hide_failure": False,
            "forced_alignment_required": True,
            "source_aware_release_review_required": True,
            "cold_independent_proxy_required": True,
            "cold_proxy_is_human_learning_evidence": False,
            "external_human_prepublication_gate_required": False,
            "scene_source_preflight_required": True,
            "isolated_render_execution_required": True,
            "primitive_graphical_regression_required": True,
        },
        "counts": counts,
        "entries": entries,
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": "Planning, rendering, review, or acceptance of a derivative video does not strengthen a book claim or itself authorize any YouTube mutation or public publication."
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build()
    body = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != body:
            raise SystemExit("Manim v2 production ledger is stale; run without --check")
        print(f"Manim v2 production ledger is current for {len(value['entries'])} canonical chapters.")
        return
    OUTPUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(value['entries'])} entries.")


if __name__ == "__main__":
    main()
