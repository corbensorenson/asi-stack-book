#!/usr/bin/env python3
"""Build the exact non-authorizing preflight for ready visual packets."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "visual_edition/youtube_upload_plan.json"
MUTATION_SCOPE = ROOT / "visual_edition/youtube_mutation_scope.json"
OUT = ROOT / "visual_edition/youtube_publication_preflight.json"
MAX_API_THUMBNAIL_BYTES = 2 * 1024 * 1024
MAX_CAPTION_BYTES = 100 * 1024 * 1024


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def batches(count: int, width: int = 15) -> list[int]:
    return [min(width, count - start) for start in range(0, count, width)]


def build() -> dict:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    mutation_scope = json.loads(MUTATION_SCOPE.read_text(encoding="utf-8"))
    if mutation_scope.get("upload_plan_sha256") != sha256(PLAN):
        raise SystemExit("YouTube mutation scope is stale against upload plan")
    if mutation_scope.get("channel_id") != plan.get("channel_id"):
        raise SystemExit("YouTube mutation scope channel differs from upload plan")
    if mutation_scope.get("playlist_title") != plan.get("playlist_title"):
        raise SystemExit("YouTube mutation scope playlist title differs from upload plan")
    if mutation_scope.get("chapter_count") != len(plan.get("entries", [])):
        raise SystemExit("YouTube mutation scope chapter denominator differs from upload plan")
    if mutation_scope.get("external_mutation_authorized_now") is not False:
        raise SystemExit("YouTube mutation scope improperly claims current authority")
    rows = []
    total_bytes = 0
    for entry in plan["entries"]:
        master = ROOT / entry["local_master_path"]
        caption = ROOT / entry["caption_path"]
        thumbnail = ROOT / entry["thumbnail_path"]
        missing = [
            str(path.relative_to(ROOT))
            for path in (master, caption, thumbnail)
            if not path.is_file()
        ]
        if missing:
            raise SystemExit(f"{entry['chapter_id']}: missing publication input(s): {missing}")
        master_digest = sha256(master)
        caption_digest = sha256(caption)
        thumbnail_digest = sha256(thumbnail)
        if master_digest != entry["local_master_sha256"]:
            raise SystemExit(f"{entry['chapter_id']}: local master digest drift")
        if thumbnail_digest != entry["thumbnail_sha256"]:
            raise SystemExit(f"{entry['chapter_id']}: thumbnail digest drift")
        if thumbnail.stat().st_size > MAX_API_THUMBNAIL_BYTES:
            raise SystemExit(f"{entry['chapter_id']}: thumbnail exceeds API 2 MiB limit")
        if caption.stat().st_size > MAX_CAPTION_BYTES:
            raise SystemExit(f"{entry['chapter_id']}: caption exceeds API 100 MiB limit")
        total_bytes += master.stat().st_size
        rows.append({
            "position": entry["position"],
            "chapter_id": entry["chapter_id"],
            "master_path": entry["local_master_path"],
            "master_sha256": master_digest,
            "master_bytes": master.stat().st_size,
            "caption_path": entry["caption_path"],
            "caption_sha256": caption_digest,
            "caption_bytes": caption.stat().st_size,
            "thumbnail_path": entry["thumbnail_path"],
            "thumbnail_sha256": thumbnail_digest,
            "thumbnail_bytes": thumbnail.stat().st_size,
            "ready": True,
        })
    if len(rows) != len(plan.get("entries", [])):
        raise SystemExit(
            "Publication rows do not match upload-plan entries: "
            f"{len(rows)} != {len(plan.get('entries', []))}"
        )
    count = len(rows)
    batch_sizes = batches(count)
    first_day_captions = min(3, count)
    remaining_captions = max(0, count - first_day_captions)
    caption_days = [
        min(25, remaining_captions - start)
        for start in range(0, remaining_captions, 25)
    ]
    quota_schedule = [
        {
            "day": 1,
            "video_insert_calls": count,
            "other_units": 50 + count * 50 + count * 50 + first_day_captions * 400,
            "operations": [
                "create one private playlist",
                f"upload {count} private or unlisted masters",
                f"insert {count} ordered playlist items",
                f"set {count} thumbnails",
                f"insert {first_day_captions} caption tracks",
            ],
        }
    ]
    for day, caption_count in enumerate(caption_days, start=2):
        quota_schedule.append(
            {
                "day": day,
                "video_insert_calls": 0,
                "other_units": caption_count * 400,
                "operations": [f"insert {caption_count} caption tracks"],
            }
        )
    final_day = len(quota_schedule) + 1
    quota_schedule.append(
        {
            "day": final_day,
            "video_insert_calls": 0,
            "other_units": count * 50 + 50,
            "operations": [
                f"set {count} videos public",
                "set canonical playlist public",
            ],
        }
    )
    return {
        "schema_version": "asi_stack.youtube_publication_preflight.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(
            microsecond=0
        ).isoformat().replace("+00:00", "Z"),
        "state": "ready_not_authorized",
        "upload_plan_path": "visual_edition/youtube_upload_plan.json",
        "upload_plan_sha256": sha256(PLAN),
        "mutation_scope_path": "visual_edition/youtube_mutation_scope.json",
        "mutation_scope_sha256": sha256(MUTATION_SCOPE),
        "scope_id": mutation_scope["scope_id"],
        "channel_id": plan["channel_id"],
        "playlist_title": plan["playlist_title"],
        "entry_count": len(rows),
        "ready_entry_count": sum(row["ready"] for row in rows),
        "local_master_total_bytes": total_bytes,
        "studio_browser_route": {
            "adapter": "youtube_studio_signed_in_browser",
            "signed_in_channel_recheck_required_at_execution": True,
            "maximum_files_per_upload_dialog": 15,
            "batch_count": len(batch_sizes),
            "batch_sizes": batch_sizes,
            "daily_video_upload_limit_is_channel_specific": True,
            "daily_thumbnail_limit_is_channel_specific": True,
            "resume_policy": (
                "stop on a platform limit or unresolved check; preserve completed "
                "unlisted identities and resume without duplicate upload"
            ),
        },
        "data_api_route": {
            "adapter": "youtube_data_api_v3_resumable",
            "oauth_and_verified_api_project_required": True,
            "unverified_api_projects_force_private_uploads": True,
            "default_daily_video_insert_calls": 100,
            "default_daily_other_units": 10000,
            "operation_costs": {
                "videos_insert": 1,
                "playlists_insert": 50,
                "playlist_items_insert": 50,
                "thumbnails_set": 50,
                "captions_insert": 400,
                "videos_update": 50,
                "playlists_update": 50,
            },
            "minimum_quota_days_for_complete_batch": len(quota_schedule),
            "quota_schedule": quota_schedule,
        },
        "entries": rows,
        "official_platform_sources": [
            "https://support.google.com/youtube/answer/57407?hl=en",
            "https://support.google.com/youtube/answer/2734796?hl=en-EN",
            "https://support.google.com/youtube/answer/72431?hl=en",
            "https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol",
            "https://developers.google.com/youtube/v3/determine_quota_cost",
            "https://developers.google.com/youtube/v3/docs/videos/insert",
            "https://developers.google.com/youtube/v3/docs/captions/insert",
            "https://developers.google.com/youtube/v3/docs/thumbnails/set",
        ],
        "external_mutation_authorized_now": False,
        "support_state_effect": "none",
        "book_claim_release_effect": "none",
    }


def main() -> None:
    value = build()
    OUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(
        "Built YouTube publication preflight: "
        f"{value['ready_entry_count']}/{value['entry_count']} exact inputs ready, "
        f"{value['local_master_total_bytes']} master bytes, no mutation authorized."
    )


if __name__ == "__main__":
    main()
