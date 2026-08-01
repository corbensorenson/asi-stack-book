#!/usr/bin/env python3
"""Build the canonical 84-chapter Manim v2 production ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "visual_edition/manim_v2_production_ledger.json"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def canonical_chapters() -> list[dict]:
    structure = load("book_structure.json")
    return [chapter for part in structure["parts"] for chapter in part["chapters"]]


def preserved_targets() -> dict[str, dict]:
    if not OUTPUT.is_file():
        return {}
    current = json.loads(OUTPUT.read_text(encoding="utf-8"))
    return {
        entry["chapter_id"]: entry["target"]
        for entry in current.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("target"), dict)
    }


def target_for(chapter_id: str, cohort: str, prior: dict | None) -> dict:
    base = f"visual_edition/chapters/{chapter_id}"
    default = {
        "generation": 2,
        "stage": "planned",
        "beat_plan_path": f"{base}/generation-2/beat_plan.json",
        "scene_path": f"{base}/generation-2/scene.py",
        "narration_path": f"{base}/generation-2/narration.txt",
        "caption_path": f"{base}/generation-2/captions.vtt",
        "transcript_path": f"{base}/generation-2/transcript.md",
        "thumbnail_path": f"{base}/generation-2/thumbnail.svg",
        "master_path": f"build/visual_edition/generation-2/final/{chapter_id}.mp4",
        "master_sha256": None,
        "render_receipt_path": None,
        "experience_review_paths": {
            "animatic": f"{base}/generation-2/reviews/animatic.json",
            "picture_and_sound_lock": f"{base}/generation-2/reviews/picture_and_sound_lock.json",
            "release_candidate": f"{base}/generation-2/reviews/release_candidate.json",
            "independent_release_candidate": f"{base}/generation-2/reviews/independent_release_candidate.json"
        },
        "gates": {
            "beat_plan": "not_started",
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
        "quarto_embed_state": "predecessor_preview" if cohort != "not_yet_uploaded" else "absent"
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
    return merged


def build() -> dict:
    chapters = canonical_chapters()
    manifest = load("visual_edition/manifest.json")
    packets = {row["chapter_id"]: row for row in manifest["chapters"]}
    previews = {
        row["chapter_id"]: row
        for row in load("visual_edition/youtube_preview_bindings.json")["entries"]
    }
    prior_targets = preserved_targets()
    entries = []
    cohorts = {
        "owner_reviewed_remediation": [],
        "remaining_unlisted_previews": [],
        "not_yet_uploaded": []
    }
    for position, chapter in enumerate(chapters, start=1):
        chapter_id = chapter["id"]
        if position <= 5:
            cohort = "owner_reviewed_remediation"
        elif position <= 12:
            cohort = "remaining_unlisted_previews"
        else:
            cohort = "not_yet_uploaded"
        cohorts[cohort].append(chapter_id)
        packet_path = packets[chapter_id]["packet_path"]
        packet = load(packet_path)
        receipt = packet["render_receipt"]
        preview = previews.get(chapter_id)
        entries.append({
            "position": position,
            "chapter_id": chapter_id,
            "title": chapter["title"],
            "chapter_path": chapter["file"],
            "chapter_sha256": packets[chapter_id]["chapter_sha256"],
            "cohort": cohort,
            "predecessor": {
                "local_generation": 1,
                "packet_path": packet_path,
                "master_path": f"build/visual_edition/final/{chapter_id}.mp4",
                "master_sha256": receipt["output_sha256"],
                "custody_state": "unlisted_preview_bound" if preview else "local_only",
                "youtube_video_id": preview["video_id"] if preview else None,
                "youtube_visibility": "unlisted" if preview else "not_uploaded",
                "preserve_history": True
            },
            "target": target_for(chapter_id, cohort, prior_targets.get(chapter_id))
        })
    counts = {
        "planned": sum(e["target"]["stage"] == "planned" for e in entries),
        "briefed": sum(e["target"]["stage"] == "briefed" for e in entries),
        "scripted": sum(e["target"]["stage"] == "scripted" for e in entries),
        "animatic_passed": sum(e["target"]["gates"]["animatic"] == "pass" for e in entries),
        "picture_and_sound_lock_passed": sum(e["target"]["gates"]["picture_and_sound_lock"] == "pass" for e in entries),
        "release_candidate_passed": sum(e["target"]["gates"]["release_candidate"] == "pass" for e in entries),
        "accepted_generation_2": sum(e["target"]["gates"]["accepted"] == "pass" for e in entries),
        "youtube_predecessors": len(previews),
        "youtube_generation_2_current": sum(e["target"]["youtube_state"] == "public_current" for e in entries),
        "quarto_generation_2_current": sum(e["target"]["quarto_embed_state"] == "generation_2_current" for e in entries)
    }
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if OUTPUT.is_file():
        generated = json.loads(OUTPUT.read_text(encoding="utf-8")).get("generated_at_utc", generated)
    return {
        "schema_version": "asi_stack.manim_v2_production_ledger.v1",
        "edition_id": "asi-stack-p7.3-visual-edition",
        "generated_at_utc": generated,
        "book_structure_path": "book_structure.json",
        "book_structure_sha256": digest("book_structure.json"),
        "visual_manifest_path": "visual_edition/manifest.json",
        "visual_manifest_sha256": digest("visual_edition/manifest.json"),
        "authoring_standard_path": "skills/asi-stack-manim-videos/SKILL.md",
        "authoring_standard_sha256": digest("skills/asi-stack-manim-videos/SKILL.md"),
        "beat_plan_schema_path": "schemas/manim_beat_plan.schema.json",
        "beat_plan_schema_sha256": digest("schemas/manim_beat_plan.schema.json"),
        "experience_review_schema_path": "schemas/manim_experience_review.schema.json",
        "experience_review_schema_sha256": digest("schemas/manim_experience_review.schema.json"),
        "canonical_chapter_count": 84,
        "target_generation": 2,
        "cohorts": cohorts,
        "acceptance_contract": {
            "required_passes": ["animatic", "picture_and_sound_lock", "release_candidate"],
            "experience_dimensions": ["teaching_clarity", "composition", "motion_quality", "synchronization", "continuity", "pacing", "voice", "sound_mix", "engagement", "accessibility", "claim_fidelity"],
            "minimum_score_each_dimension": 4,
            "average_may_hide_failure": False,
            "independent_review_required": True,
            "external_human_prepublication_gate_required": False
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
        print("Manim v2 production ledger is current for all 84 chapters.")
        return
    OUTPUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(value['entries'])} entries.")


if __name__ == "__main__":
    main()
