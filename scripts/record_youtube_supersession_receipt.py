#!/usr/bin/env python3
"""Record an observed replacement upload and predecessor disposition."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PLAN_SCHEMA = ROOT / "schemas/youtube_supersession_plan.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
OUT_ROOT = ROOT / "visual_edition/platform_receipts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def tags_sha256(values: list[str]) -> str:
    return text_sha256(
        json.dumps(values, ensure_ascii=False, separators=(",", ":"))
    )


def now() -> str:
    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")


def schema_errors(value: dict, schema_path: Path) -> list[str]:
    return [
        f"{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(load(schema_path)).iter_errors(value)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
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
    parser.add_argument("--playlist-item-id", required=True)
    parser.add_argument("--caption-track-id", required=True)
    parser.add_argument("--observation-payload", required=True)
    parser.add_argument("--predecessor-observation-payload", required=True)
    parser.add_argument("--observed-at-utc", default=now())
    parser.add_argument("--recorded-at-utc", default=now())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    plan_path = ROOT / args.plan
    if not plan_path.is_file():
        raise SystemExit(f"Missing supersession plan: {plan_path}")
    plan = load(plan_path)
    failures = schema_errors(plan, PLAN_SCHEMA)
    if failures:
        raise SystemExit("Supersession plan invalid:\n - " + "\n - ".join(failures))
    if (
        not re.fullmatch(r"[0-9a-f]{64}", args.authorization_scope_sha256)
        or args.authorization_scope_sha256 != sha256(plan_path)
    ):
        raise SystemExit(
            "authorization scope digest does not match the exact supersession plan"
        )
    if args.video_id == plan["predecessor"]["video_id"]:
        raise SystemExit("replacement video ID equals predecessor video ID")
    replacement = plan["replacement"]
    master = ROOT / replacement["local_master_path"]
    caption = ROOT / replacement["caption_path"]
    thumbnail = ROOT / replacement["thumbnail_path"]
    observation = ROOT / args.observation_payload
    predecessor_observation = ROOT / args.predecessor_observation_payload
    for path in (
        master,
        caption,
        thumbnail,
        observation,
        predecessor_observation,
    ):
        if not path.is_file():
            raise SystemExit(f"Missing supersession receipt input: {path}")
    exact_files = (
        (master, replacement["local_master_sha256"]),
        (caption, replacement["caption_sha256"]),
        (thumbnail, replacement["thumbnail_sha256"]),
    )
    if any(sha256(path) != expected for path, expected in exact_files):
        raise SystemExit("supersession input drifted after plan preparation")
    receipt = {
        "schema_version": "asi_stack.youtube_platform_receipt.v1",
        "receipt_id": (
            f"youtube-{plan['chapter_id']}-g{plan['generation']}"
        ),
        "recorded_at_utc": args.recorded_at_utc,
        "authorization_scope_sha256": args.authorization_scope_sha256,
        "adapter": args.adapter,
        "chapter_id": plan["chapter_id"],
        "stable_internal_video_id": plan["stable_internal_video_id"],
        "generation": plan["generation"],
        "channel_id": plan["channel_id"],
        "video_id": args.video_id,
        "watch_url": f"https://www.youtube.com/watch?v={args.video_id}",
        "playlist_id": plan["playlist_id"],
        "playlist_item_id": args.playlist_item_id,
        "playlist_position": plan["playlist_position"],
        "source_upload": {
            "local_master_path": replacement["local_master_path"],
            "local_master_sha256": replacement["local_master_sha256"],
            "local_master_bytes": replacement["local_master_bytes"],
            "bound_chapter_sha256": replacement["bound_chapter_sha256"],
            "bound_source_commit": replacement["bound_source_commit"],
        },
        "metadata": {
            "title_sha256": text_sha256(replacement["title"]),
            "description_sha256": text_sha256(replacement["description"]),
            "tags_sha256": tags_sha256(replacement["tags"]),
            "category_id": replacement["category_id"],
            "made_for_kids": replacement["made_for_kids"],
            "synthetic_narration_disclosed": (
                replacement["contains_synthetic_narration_disclosure"]
            ),
            "state": "exact",
        },
        "accessibility": {
            "caption_path": replacement["caption_path"],
            "caption_sha256": replacement["caption_sha256"],
            "caption_language": "en",
            "caption_track_id": args.caption_track_id,
            "caption_state": "published",
            "thumbnail_path": replacement["thumbnail_path"],
            "thumbnail_sha256": replacement["thumbnail_sha256"],
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
        "supersedes_video_id": plan["predecessor"]["video_id"],
        "predecessor_disposition": {
            "video_id": plan["predecessor"]["video_id"],
            "old_playlist_item_id": plan["predecessor"]["playlist_item_id"],
            "privacy_status": "unlisted",
            "playlist_state": "removed_from_canonical_playlist",
            "current_pointer_state": "points_to_successor",
            "observed_at_utc": args.observed_at_utc,
            "observation_payload_sha256": sha256(predecessor_observation),
        },
        "support_state_effect": "none",
        "book_claim_release_effect": "none",
        "non_claims": [
            "The replacement publication does not promote or otherwise change a book claim.",
            "The predecessor disposition does not erase its historical receipt or watch identity.",
            "Platform processing does not independently verify the chapter argument.",
            "The receipt does not establish safety, deployment efficacy, transfer, AGI, or ASI.",
        ],
    }
    failures = schema_errors(receipt, RECEIPT_SCHEMA)
    if failures:
        raise SystemExit(
            "Supersession receipt invalid:\n - " + "\n - ".join(failures)
        )
    output = (
        OUT_ROOT
        / f"generation-{plan['generation']}"
        / f"{plan['chapter_id']}.json"
    )
    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {output.relative_to(ROOT)}")
    else:
        print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
