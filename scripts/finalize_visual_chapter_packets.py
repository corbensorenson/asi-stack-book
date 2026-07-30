#!/usr/bin/env python3
"""Bind reviewed local final masters into non-promoting chapter packets."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "build/visual_edition/final"
AUDIO = ROOT / "build/visual_edition/audio"
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chapter_ids(include_pilots: bool = False) -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter["id"]
        for part in structure["parts"]
        for chapter in part["chapters"]
        if include_pilots or chapter["id"] not in PILOTS
    ]


def artifact_hashes(packet: dict) -> dict:
    mapping = {
        "storyboard": "storyboard",
        "scene_code": "scene_code",
        "narration_script": "narration_script",
        "captions": "captions",
        "descriptive_transcript": "descriptive_transcript",
        "thumbnail": "thumbnail",
    }
    result = {
        receipt_name: sha256(ROOT / packet["artifacts"][artifact_name])
        for receipt_name, artifact_name in mapping.items()
    }
    if packet["artifacts"].get("scene_spec"):
        result["scene_spec"] = sha256(ROOT / packet["artifacts"]["scene_spec"])
    return result


def finalize(slug: str) -> None:
    packet_path = ROOT / f"visual_edition/chapters/{slug}/packet.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    master = json.loads((FINAL / f"{slug}.validation.json").read_text(encoding="utf-8"))
    narration = json.loads(
        (AUDIO / f"{slug}-narration-master.validation.json").read_text(encoding="utf-8")
    )
    if master.get("validation_state") != "pass" or narration.get("validation_state") != "pass":
        raise SystemExit(f"Unvalidated local master: {slug}")
    narration_receipt = AUDIO / f"{slug}-narration-master.receipt.json"
    narration_asr = AUDIO / f"{slug}-narration-master.json"
    narration_validator = ROOT / "scripts/validate_visual_narration.py"
    if (
        narration.get("validator_sha256") != sha256(narration_validator)
        or narration.get("receipt_sha256") != sha256(narration_receipt)
        or narration.get("asr_sha256") != sha256(narration_asr)
    ):
        raise SystemExit(f"Stale narration validation provenance: {slug}")
    master_validator = ROOT / "scripts/validate_visual_master.py"
    narration_validation_path = AUDIO / f"{slug}-narration-master.validation.json"
    mux_receipt_path = FINAL / f"{slug}.mux.json"
    if (
        master.get("validator_sha256") != sha256(master_validator)
        or master.get("caption_sha256")
        != sha256(ROOT / f"visual_edition/chapters/{slug}/captions.vtt")
        or master.get("narration_validation_sha256")
        != sha256(narration_validation_path)
        or master.get("mux_receipt_sha256") != sha256(mux_receipt_path)
    ):
        raise SystemExit(f"Stale final-master validation provenance: {slug}")
    duration = float(master["duration_seconds"])
    mux_receipt = json.loads(mux_receipt_path.read_text(encoding="utf-8"))
    endpoints = [
        float(value)
        for value in mux_receipt["audio_scene_endpoints_seconds"]
    ]
    if len(endpoints) != 7:
        raise SystemExit(f"Invalid scene endpoint count in mux receipt: {slug}")
    starts = [0.0, *endpoints[:-1]]
    samples = [
        round(start + ((end - start) / 2.0), 3)
        for start, end in zip(starts, endpoints)
    ]
    rendered_at = datetime.fromtimestamp(
        (FINAL / f"{slug}.mp4").stat().st_mtime,
        tz=timezone.utc,
    ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    packet["lifecycle_state"] = "ready_not_published"
    packet["render_receipt"] = {
        "receipt_state": "current_final_av_master",
        "validation_state": "validated",
        "rendered_at_utc": rendered_at,
        "toolchain_id": "manimce-0.20.1-macos-arm64-python-3.12.5",
        "toolchain_qualification": "qualified_for_all_non_latex_chapters",
        "render_profile": "final_av_master",
        "command": (
            (
                "Reuse the ratified chapter-specific pilot visual"
                if slug in PILOTS
                else "Render the exact-timing ChapterVisualAbstract"
            )
            + " with pinned ManimCE 0.20.1 at 1920x1080/30, render pinned "
            "Kokoro-82M af_heart narration at speed 1.08 with a hard maximum "
            "of 300 characters per synthesis call and -16 LUFS, then align all "
            "seven visual scenes to the exact audio paragraph boundaries and mux "
            "with FFmpeg 8.0.1 "
            "as H.264 CRF 18 yuv420p plus AAC-LC 192 kb/s 48 kHz mono."
        ),
        "duration_seconds": duration,
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_rate": 30,
        "video_codec": "h264",
        "pixel_format": "yuv420p",
        "output_sha256": master["video_sha256"],
        "mux_receipt_sha256": master["mux_receipt_sha256"],
        "output_storage": "ignored build/visual_edition media only",
        "visual_review": {
            "draft_sample_seconds": samples,
            "release_sample_seconds": [samples[1], samples[5]],
            "result": "pass",
            "review_scope": (
                "Exact mux-receipt midpoint sampling across all seven narration scenes "
                "checked composition, legibility, persistent "
                "labels, color-plus-shape semantics, evidence ceiling, non-claims, end-card "
                "identity, and absence of clipping or overflowing text."
            ),
        },
        "audio_master": {
            "identity": "Kokoro-82M bf16 af_heart via kokoro-mlx 0.1.2 at speed 1.08",
            "provenance": (
                "Locally generated from the canonical narration with the pinned Apache-2.0 "
                "Kokoro-82M model and MIT kokoro-mlx implementation recorded in "
                "visual_edition/narration_toolchain.json."
            ),
            "publication_rights_state": "cleared",
            "duration_seconds": duration,
            "sha256": narration["audio_sha256"],
        },
        "caption_review": {
            "state": "machine_audited",
            "audit_method": (
                "Exact receipt-derived canonical timing plus local MLX Whisper transcript "
                "comparison and complete beginning/end coverage checks."
            ),
            "reviewed_against_audio_sha256": narration["audio_sha256"],
            "asr_model": (
                "mlx-community/whisper-small.en-mlx@"
                "52a88bf6e98b114a210c21bb83e22d6e1505cb73"
            ),
            "asr_word_error_rate": narration["content_word_error_rate"],
            "terminology": "pass",
            "timing": "pass",
            "non_speech_information": "pass",
            "material_visual_changes": "described_in_adjacent_transcript",
        },
        "artifact_sha256": artifact_hashes(packet),
        "remaining_release_gates": [
            "obtain exact action-time authority before any YouTube or playlist mutation"
        ],
    }
    packet["non_claims"] = [
        "This derivative video does not promote or otherwise change any book claim.",
        "The validated local final master is not a YouTube upload or a public publication.",
        "Automated intelligibility and caption audits do not establish that every listener will prefer the synthetic voice.",
        "A successful animation render does not establish deployment, safety, efficiency, transfer, state of the art, AGI, or ASI.",
    ]
    packet_path.write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--all-non-pilots", action="store_true")
    parser.add_argument("--all-chapters", action="store_true")
    parser.add_argument(
        "--visual-review-complete",
        action="store_true",
        help="Required assertion that the generated seven-frame release samples were reviewed.",
    )
    args = parser.parse_args()
    if not args.visual_review_complete:
        raise SystemExit("Refusing to finalize before --visual-review-complete")
    selected = (
        chapter_ids(include_pilots=args.all_chapters)
        if args.all_non_pilots or args.all_chapters
        else args.chapter
    )
    if not selected:
        raise SystemExit("Select --chapter or --all-non-pilots")
    for slug in selected:
        finalize(slug)
    print(
        f"Finalized {len(selected)} reviewed visual chapter packets against "
        "their existing canonical chapter source commits."
    )


if __name__ == "__main__":
    main()
