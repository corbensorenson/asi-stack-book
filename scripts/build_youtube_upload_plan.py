#!/usr/bin/env python3
"""Build deterministic, non-authorizing YouTube metadata for all 84 videos."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "visual_edition/youtube_upload_plan.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def youtube_title(position: int, title: str) -> str:
    suffix = " — The ASI Stack"
    prefix = f"{position:02d}. "
    available = 100 - len(prefix) - len(suffix)
    chapter = title if len(title) <= available else title[: available - 1].rstrip() + "…"
    return prefix + chapter + suffix


def main() -> None:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    channel = json.loads(
        (ROOT / "visual_edition/youtube_channel.json").read_text(encoding="utf-8")
    )
    entries = []
    position = 0
    for part in structure["parts"]:
        for chapter in part["chapters"]:
            position += 1
            packet_path = ROOT / f"visual_edition/chapters/{chapter['id']}/packet.json"
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            thumbnail_path = (
                ROOT / f"build/visual_edition/thumbnails/{chapter['id']}.png"
            )
            chapter_url = (
                "https://corbensorenson.github.io/asi-stack-book/"
                + chapter["file"].replace(".qmd", ".html")
            )
            description = "\n".join([
                "Read the live book: https://corbensorenson.github.io/asi-stack-book/",
                f"Read this chapter: {chapter_url}",
                "",
                compact(chapter["core_claim"]),
                "",
                f"Current evidence state: {chapter['evidence_level']} — {chapter['claim_label']}.",
                compact(packet["maximum_inference"]),
                "",
                (
                    "Narration is synthetic and generated locally with the Apache-2.0 "
                    "Kokoro-82M model using the af_heart voice."
                ),
                (
                    "This visual abstract is a derivative explanation. It does not promote "
                    "or otherwise change any claim in the book."
                ),
                "",
                f"Stable video identity: {packet['video_id']}",
                f"Chapter digest: {packet['chapter_sha256']}",
                f"Source commit: {packet['source_commit']}",
            ])
            entries.append({
                "position": position,
                "chapter_id": chapter["id"],
                "stable_internal_video_id": packet["video_id"],
                "generation": 1,
                "title": youtube_title(position, chapter["title"]),
                "description": description,
                "category_id": "27",
                "made_for_kids": False,
                "contains_synthetic_narration_disclosure": True,
                "tags": [
                    "The ASI Stack",
                    "artificial intelligence",
                    "AI architecture",
                    "AI governance",
                    "AI safety",
                ],
                "thumbnail_source_path": packet["artifacts"]["thumbnail"],
                "thumbnail_source_sha256": sha256(
                    ROOT / packet["artifacts"]["thumbnail"]
                ),
                "thumbnail_path": str(thumbnail_path.relative_to(ROOT)),
                "thumbnail_sha256": (
                    sha256(thumbnail_path) if thumbnail_path.is_file() else None
                ),
                "caption_path": packet["artifacts"]["captions"],
                "local_master_path": f"build/visual_edition/final/{chapter['id']}.mp4",
                "local_master_sha256": (
                    packet["render_receipt"]["output_sha256"]
                    if packet.get("render_receipt")
                    and packet["render_receipt"].get("validation_state") == "validated"
                    else None
                ),
                "desired_playlist_position": position,
                "initial_upload_privacy": "unlisted",
                "desired_final_privacy": "public",
                "mutation_state": "prepared_not_authorized",
            })
    value = {
        "schema_version": "asi_stack.youtube_upload_plan.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "book_structure_sha256": sha256(ROOT / "book_structure.json"),
        "channel_config_sha256": sha256(ROOT / "visual_edition/youtube_channel.json"),
        "channel_id": channel["channel"]["channel_id"],
        "playlist_title": channel["canonical_playlist"]["title"],
        "entry_count": len(entries),
        "external_mutation_authorized_now": False,
        "publication_mode": "stage_all_unlisted_then_publish_reconciled_set",
        "entries": entries,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    if len(entries) != 84 or any(len(item["title"]) > 100 for item in entries):
        raise SystemExit("YouTube upload-plan count or title-length contract failed")
    OUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Built non-authorizing YouTube upload plan for 84 chapter videos.")


if __name__ == "__main__":
    main()
