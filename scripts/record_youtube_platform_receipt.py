#!/usr/bin/env python3
"""Record one observed, already-completed YouTube publication transaction.

This script does not call YouTube. It converts an exact browser/API observation
into the tracked receipt consumed by the all-or-nothing repository reconciler.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "visual_edition/youtube_upload_plan.json"
MUTATION_SCOPE = ROOT / "visual_edition/youtube_mutation_scope.json"
SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
OUT_ROOT = ROOT / "visual_edition/platform_receipts/generation-1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def tags_sha256(values: list[str]) -> str:
    canonical = json.dumps(
        values,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return text_sha256(canonical)


def now() -> str:
    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter-id", required=True)
    parser.add_argument("--authorization-scope-sha256", required=True)
    parser.add_argument(
        "--adapter",
        required=True,
        choices=[
            "youtube_studio_signed_in_browser",
            "youtube_data_api_v3_resumable",
        ],
    )
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--playlist-id", required=True)
    parser.add_argument("--playlist-item-id", required=True)
    parser.add_argument("--caption-track-id", required=True)
    parser.add_argument("--observation-payload", required=True)
    parser.add_argument("--observed-at-utc", default=now())
    parser.add_argument("--recorded-at-utc", default=now())
    parser.add_argument("--supersedes-video-id")
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the tracked receipt; default is validation-only preview",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{64}", args.authorization_scope_sha256):
        raise SystemExit("authorization scope must be a lowercase SHA-256 digest")
    expected_scope_digest = sha256(MUTATION_SCOPE)
    if args.authorization_scope_sha256 != expected_scope_digest:
        raise SystemExit(
            "authorization scope digest does not match the tracked exact mutation scope"
        )
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    entry = next(
        (
            item
            for item in plan["entries"]
            if item["chapter_id"] == args.chapter_id
        ),
        None,
    )
    if entry is None:
        raise SystemExit(f"Unknown chapter: {args.chapter_id}")
    packet_path = (
        ROOT / f"visual_edition/chapters/{args.chapter_id}/packet.json"
    )
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    master = ROOT / entry["local_master_path"]
    caption = ROOT / entry["caption_path"]
    thumbnail = ROOT / entry["thumbnail_path"]
    observation = ROOT / args.observation_payload
    for path in (master, caption, thumbnail, observation):
        if not path.is_file():
            raise SystemExit(f"Missing receipt input: {path}")
    if sha256(master) != entry["local_master_sha256"]:
        raise SystemExit("local master drifted after upload planning")
    receipt = {
        "schema_version": "asi_stack.youtube_platform_receipt.v1",
        "receipt_id": f"youtube-{args.chapter_id}-g{entry['generation']}",
        "recorded_at_utc": args.recorded_at_utc,
        "authorization_scope_sha256": args.authorization_scope_sha256,
        "adapter": args.adapter,
        "chapter_id": args.chapter_id,
        "stable_internal_video_id": entry["stable_internal_video_id"],
        "generation": entry["generation"],
        "channel_id": plan["channel_id"],
        "video_id": args.video_id,
        "watch_url": f"https://www.youtube.com/watch?v={args.video_id}",
        "playlist_id": args.playlist_id,
        "playlist_item_id": args.playlist_item_id,
        "playlist_position": entry["desired_playlist_position"],
        "source_upload": {
            "local_master_path": entry["local_master_path"],
            "local_master_sha256": sha256(master),
            "local_master_bytes": master.stat().st_size,
            "bound_chapter_sha256": packet["chapter_sha256"],
            "bound_source_commit": packet["source_commit"],
        },
        "metadata": {
            "title_sha256": text_sha256(entry["title"]),
            "description_sha256": text_sha256(entry["description"]),
            "tags_sha256": tags_sha256(entry["tags"]),
            "category_id": entry["category_id"],
            "made_for_kids": entry["made_for_kids"],
            "synthetic_narration_disclosed": (
                entry["contains_synthetic_narration_disclosure"]
            ),
            "state": "exact",
        },
        "accessibility": {
            "caption_path": entry["caption_path"],
            "caption_sha256": sha256(caption),
            "caption_language": "en",
            "caption_track_id": args.caption_track_id,
            "caption_state": "published",
            "thumbnail_path": entry["thumbnail_path"],
            "thumbnail_sha256": sha256(thumbnail),
            "thumbnail_state": "applied",
        },
        "platform_observation": {
            "upload_status": "processed",
            "privacy_status": "public",
            "definition": "hd",
            "embeddable": True,
            "playlist_state": "ordered_current",
            "metadata_state": "exact",
            "watch_page_state": "publicly_reachable",
            "observed_at_utc": args.observed_at_utc,
            "observation_payload_sha256": sha256(observation),
        },
        "supersedes_video_id": args.supersedes_video_id,
        "support_state_effect": "none",
        "book_claim_release_effect": "none",
        "non_claims": [
            "The video publication does not promote or otherwise change a book claim.",
            "A reachable watch page does not prove every regional or future playback route.",
            "Platform processing does not independently verify the chapter argument.",
            "The receipt does not establish safety, deployment efficacy, transfer, AGI, or ASI.",
        ],
    }
    failures = [
        f"{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(
            json.loads(SCHEMA.read_text(encoding="utf-8"))
        ).iter_errors(receipt)
    ]
    if failures:
        raise SystemExit("Platform receipt invalid:\n - " + "\n - ".join(failures))
    output = OUT_ROOT / f"{args.chapter_id}.json"
    if args.write:
        OUT_ROOT.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {output.relative_to(ROOT)}")
    else:
        print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
