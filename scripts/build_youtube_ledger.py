#!/usr/bin/env python3
"""Build the exact 84-chapter YouTube publication and revision ledger."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
VISUAL_MANIFEST = ROOT / "visual_edition/manifest.json"
CHANNEL = ROOT / "visual_edition/youtube_channel.json"
OUT = ROOT / "visual_edition/youtube_ledger.json"
RECEIPT_ROOT = ROOT / "visual_edition/platform_receipts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blank_youtube(channel_id: str) -> dict:
    return {
        "channel_id": channel_id,
        "video_id": None,
        "watch_url": None,
        "playlist_id": None,
        "generation": 0,
        "publication_state": "not_authorized",
        "uploaded_output_sha256": None,
        "bound_chapter_sha256": None,
        "bound_source_commit": None,
        "published_at_utc": None,
        "platform_receipt_path": None,
        "supersedes_video_id": None,
    }


def required_action(packet: dict | None) -> str:
    if packet is None:
        return "create_derivative_packet"
    state = packet["lifecycle_state"]
    youtube = packet["youtube"]
    if youtube.get("publication_state") == "stale" and youtube.get("video_id"):
        if (
            state == "ready_not_published"
            and packet.get("render_receipt", {}).get("validation_state")
            == "validated"
        ):
            return "prepare_supersession_plan"
        return "regenerate_stale_derivative"
    if state in {"planned", "storyboarded", "scripted"}:
        return "finish_derivative_packet"
    if state == "rendered":
        return "finish_rights_cleared_final_av"
    if state == "validated":
        return "prepare_youtube_metadata_and_receipt"
    if state == "ready_not_published":
        return "obtain_action_time_upload_authority"
    if state == "published_current":
        return "monitor_chapter_freshness"
    if state == "stale":
        return "regenerate_stale_derivative"
    return "retain_historical_receipt"


def generation_history(
    chapter_id: str,
    current: dict,
    receipt_root: Path = RECEIPT_ROOT,
) -> list[dict]:
    rows = []
    for path in sorted(receipt_root.glob(f"generation-*/{chapter_id}.json")):
        receipt = load(path)
        try:
            receipt_relative = path.relative_to(ROOT)
        except ValueError:
            receipt_relative = (
                Path("visual_edition/platform_receipts")
                / path.relative_to(receipt_root)
            )
        if (
            receipt.get("video_id") == current.get("video_id")
            and current.get("publication_state") in {"published_current", "stale"}
        ):
            state = current["publication_state"]
        else:
            state = "superseded"
        rows.append({
            "generation": receipt["generation"],
            "video_id": receipt["video_id"],
            "watch_url": receipt["watch_url"],
            "playlist_id": receipt["playlist_id"],
            "playlist_item_id": receipt["playlist_item_id"],
            "publication_state": state,
            "platform_receipt_path": str(receipt_relative),
            "platform_receipt_sha256": digest(path),
            "uploaded_output_sha256": receipt["source_upload"][
                "local_master_sha256"
            ],
            "bound_chapter_sha256": receipt["source_upload"][
                "bound_chapter_sha256"
            ],
            "bound_source_commit": receipt["source_upload"][
                "bound_source_commit"
            ],
            "published_at_utc": receipt["platform_observation"][
                "observed_at_utc"
            ],
            "supersedes_video_id": receipt["supersedes_video_id"],
        })
    rows = sorted(rows, key=lambda row: row["generation"])
    generations = [row["generation"] for row in rows]
    if generations and generations != list(range(1, generations[-1] + 1)):
        raise SystemExit(
            f"{chapter_id}: non-contiguous YouTube generation history {generations}"
        )
    if len({row["video_id"] for row in rows}) != len(rows):
        raise SystemExit(f"{chapter_id}: duplicate video ID in generation history")
    for index, row in enumerate(rows):
        expected_predecessor = None if index == 0 else rows[index - 1]["video_id"]
        if row["supersedes_video_id"] != expected_predecessor:
            raise SystemExit(
                f"{chapter_id}: broken predecessor chain at generation "
                f"{row['generation']}"
            )
    if (
        rows
        and current.get("publication_state") in {"published_current", "stale"}
        and rows[-1]["video_id"] != current.get("video_id")
    ):
        raise SystemExit(
            f"{chapter_id}: current packet does not match latest generation receipt"
        )
    return rows


def build() -> dict:
    structure = load(STRUCTURE)
    visual = load(VISUAL_MANIFEST)
    channel = load(CHANNEL)
    channel_id = channel["channel"]["channel_id"]
    visual_rows = {row["chapter_id"]: row for row in visual["chapters"]}
    entries = []
    counts = {
        "total_chapters": 0,
        "packets_present": 0,
        "youtube_objects": 0,
        "published_current": 0,
        "stale_or_superseded": 0,
        "replacement_required": 0,
        "platform_generations": 0,
        "historical_generations": 0,
    }
    position = 0
    for part in structure["parts"]:
        for chapter in part["chapters"]:
            position += 1
            chapter_id = chapter["id"]
            row = visual_rows[chapter_id]
            packet_path = row.get("packet_path")
            packet = load(ROOT / packet_path) if packet_path else None
            youtube = packet["youtube"] if packet else blank_youtube(channel_id)
            generations = generation_history(chapter_id, youtube)
            if packet:
                counts["packets_present"] += 1
            counts["youtube_objects"] += len(generations)
            counts["platform_generations"] += len(generations)
            counts["historical_generations"] += sum(
                item["publication_state"] == "superseded"
                for item in generations
            )
            if youtube["publication_state"] == "published_current":
                counts["published_current"] += 1
            if youtube["publication_state"] in {"stale", "superseded"}:
                counts["stale_or_superseded"] += 1
            action = required_action(packet)
            if action == "prepare_supersession_plan":
                counts["replacement_required"] += 1
            entries.append({
                "position": position,
                "chapter_id": chapter_id,
                "chapter_path": chapter["file"],
                "chapter_sha256": row["chapter_sha256"],
                "stable_internal_video_id": (
                    packet["video_id"] if packet else f"asi-video-{chapter_id}"
                ),
                "packet_path": packet_path,
                "lifecycle_state": row["lifecycle_state"],
                "staleness_state": (
                    packet["staleness"]["state"] if packet else "not_yet_derived"
                ),
                "youtube": youtube,
                "generations": generations,
                "required_action": action,
            })
            counts["total_chapters"] += 1
    return {
        "schema_version": "asi_stack.youtube_ledger.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "book_structure_path": "book_structure.json",
        "book_structure_sha256": digest(STRUCTURE),
        "visual_manifest_path": "visual_edition/manifest.json",
        "visual_manifest_sha256": digest(VISUAL_MANIFEST),
        "channel_config_path": "visual_edition/youtube_channel.json",
        "channel_config_sha256": digest(CHANNEL),
        "channel_id": channel_id,
        "playlist_id": channel["canonical_playlist"]["playlist_id"],
        "counts": counts,
        "entries": entries,
        "support_state_effect": "none",
        "release_effect": "none",
    }


def main() -> None:
    value = build()
    OUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    counts = value["counts"]
    print(
        "Built YouTube ledger: "
        f"{counts['total_chapters']} chapters, "
        f"{counts['packets_present']} packets, "
        f"{counts['youtube_objects']} platform objects, "
        f"{counts['published_current']} current publications."
    )


if __name__ == "__main__":
    main()
