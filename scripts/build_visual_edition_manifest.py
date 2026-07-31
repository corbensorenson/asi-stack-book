#!/usr/bin/env python3
"""Build the canonical 84-entry P7.3 visual-edition manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from visual_chapter_source import canonical_chapter_sha256


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
OUT = ROOT / "visual_edition/manifest.json"
CHANNEL = ROOT / "visual_edition/youtube_channel.json"
PREVIEW_BINDINGS = ROOT / "visual_edition/youtube_preview_bindings.json"
PILOTS = [
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
]
STATES = [
    "planned",
    "storyboarded",
    "scripted",
    "rendered",
    "validated",
    "ready_not_published",
    "published_current",
    "stale",
    "superseded",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def main() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    channel = json.loads(CHANNEL.read_text(encoding="utf-8"))
    preview = json.loads(PREVIEW_BINDINGS.read_text(encoding="utf-8"))
    preview_count = len(preview["entries"])
    rows = []
    state_counts = {state: 0 for state in STATES}
    packet_count = 0
    rendered_count = 0
    youtube_count = 0
    embed_count = 0
    for part_index, part in enumerate(structure["parts"], start=1):
        for chapter_index, chapter in enumerate(part["chapters"], start=1):
            chapter_id = chapter["id"]
            packet_rel = f"visual_edition/chapters/{chapter_id}/packet.json"
            packet_path = ROOT / packet_rel
            state = "planned"
            packet_pointer = None
            if packet_path.exists():
                packet = json.loads(packet_path.read_text(encoding="utf-8"))
                state = packet["lifecycle_state"]
                packet_pointer = packet_rel
                packet_count += 1
                receipt = packet.get("render_receipt")
                if receipt and receipt.get("validation_state") == "validated":
                    rendered_count += 1
                if packet["youtube"]["publication_state"] == "published_current":
                    youtube_count += 1
                if packet["quarto_embed"]["state"] == "published_current":
                    embed_count += 1
            state_counts[state] += 1
            chapter_path = ROOT / chapter["file"]
            rows.append({
                "chapter_id": chapter_id,
                "title": chapter["title"],
                "chapter_path": chapter["file"],
                "chapter_sha256": canonical_chapter_sha256(chapter_path),
                "part_id": part["id"],
                "part_index": part_index,
                "chapter_index": chapter_index,
                "pilot": chapter_id in PILOTS,
                "lifecycle_state": state,
                "packet_path": packet_pointer,
            })
    value = {
        "schema_version": "asi_stack.visual_edition_manifest.v1",
        "edition_id": "asi-stack-p7.3-visual-edition",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "book_structure_path": "book_structure.json",
        "source_commit_at_generation": git_head(),
        "canonical_chapter_count": len(rows),
        "pilot_chapter_ids": PILOTS,
        "toolchain_path": "visual_edition/toolchain.json",
        "visual_grammar_path": "visual_edition/visual_grammar.json",
        "hosting": {
            "canonical_binary_host": "YouTube",
            "channel_config_path": "visual_edition/youtube_channel.json",
            "youtube_ledger_path": "visual_edition/youtube_ledger.json",
            "channel_id": channel["channel"]["channel_id"],
            "canonical_playlist_required": True,
            "playlist_id": channel["canonical_playlist"]["playlist_id"],
            "external_publication_authorized_now": False,
        },
        "repository_boundary": {
            "rendered_video_binary_tracked_in_git": False,
            "rendered_video_binary_in_pages_artifact": False,
            "local_render_location_class": "ignored_build_space",
        },
        "preview": {
            "state": preview["state"],
            "binding_path": "visual_edition/youtube_preview_bindings.json",
            "binding_sha256": digest(PREVIEW_BINDINGS),
            "unlisted_video_count": preview_count,
            "current_quarto_preview_embeds": preview_count,
            "edition_complete": False,
            "next_upload_position": preview["next_upload_position"],
        },
        "counts": {
            **state_counts,
            "packets_present": packet_count,
            "current_rendered_videos": rendered_count,
            "youtube_videos_published": youtube_count,
            "current_quarto_embeds": embed_count,
            "youtube_videos_unlisted_preview": preview_count,
            "current_quarto_preview_embeds": preview_count,
        },
        "chapters": rows,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    if len(rows) != 84:
        raise SystemExit(f"Expected 84 canonical chapters, found {len(rows)}")
    OUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(
        f"Built visual-edition manifest: {len(rows)} chapters, {packet_count} packets, "
        f"{rendered_count} validated render receipts, {youtube_count} YouTube publications."
    )


if __name__ == "__main__":
    main()
