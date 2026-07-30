#!/usr/bin/env python3
"""Reconcile 84 exact public YouTube receipts into packets and Quarto.

The operation is intentionally all-or-nothing: every receipt is validated
before any tracked file changes. This script records completed platform state;
it never calls or mutates YouTube itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "visual_edition/youtube_upload_plan.json"
CHANNEL = ROOT / "visual_edition/youtube_channel.json"
MANIFEST = ROOT / "visual_edition/manifest.json"
LEDGER = ROOT / "visual_edition/youtube_ledger.json"
RECEIPT_SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
RECEIPT_ROOT = ROOT / "visual_edition/platform_receipts/generation-1"


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


def validate_receipts(authority_digest: str) -> tuple[list[tuple[dict, dict, Path]], str]:
    plan = load(PLAN)
    schema = load(RECEIPT_SCHEMA)
    expected_paths = {
        RECEIPT_ROOT / f"{entry['chapter_id']}.json"
        for entry in plan["entries"]
    }
    actual_paths = set(RECEIPT_ROOT.glob("*.json")) if RECEIPT_ROOT.exists() else set()
    failures = []
    missing = expected_paths - actual_paths
    extra = actual_paths - expected_paths
    if missing:
        failures.append(f"missing {len(missing)} platform receipt(s)")
    if extra:
        failures.append(f"unexpected platform receipt(s): {sorted(map(str, extra))}")
    rows: list[tuple[dict, dict, Path]] = []
    video_ids = set()
    playlist_item_ids = set()
    playlist_ids = set()
    for entry in plan["entries"]:
        path = RECEIPT_ROOT / f"{entry['chapter_id']}.json"
        if not path.is_file():
            continue
        receipt = load(path)
        for error in Draft202012Validator(schema).iter_errors(receipt):
            failures.append(
                f"{entry['chapter_id']}:schema:"
                f"{'.'.join(map(str, error.path))}: {error.message}"
            )
        packet = load(
            ROOT / f"visual_edition/chapters/{entry['chapter_id']}/packet.json"
        )
        exact = {
            "authorization_scope_sha256": authority_digest,
            "chapter_id": entry["chapter_id"],
            "stable_internal_video_id": entry["stable_internal_video_id"],
            "generation": entry["generation"],
            "channel_id": plan["channel_id"],
            "playlist_position": entry["desired_playlist_position"],
        }
        for key, expected in exact.items():
            if receipt.get(key) != expected:
                failures.append(f"{entry['chapter_id']}: receipt {key} drift")
        if receipt.get("watch_url") != (
            f"https://www.youtube.com/watch?v={receipt.get('video_id')}"
        ):
            failures.append(f"{entry['chapter_id']}: watch URL drift")
        source = receipt.get("source_upload", {})
        master = ROOT / entry["local_master_path"]
        source_exact = {
            "local_master_path": entry["local_master_path"],
            "local_master_sha256": entry["local_master_sha256"],
            "local_master_bytes": master.stat().st_size if master.is_file() else -1,
            "bound_chapter_sha256": packet["chapter_sha256"],
            "bound_source_commit": packet["source_commit"],
        }
        for key, expected in source_exact.items():
            if source.get(key) != expected:
                failures.append(f"{entry['chapter_id']}: source upload {key} drift")
        metadata = receipt.get("metadata", {})
        metadata_exact = {
            "title_sha256": text_sha256(entry["title"]),
            "description_sha256": text_sha256(entry["description"]),
            "tags_sha256": tags_sha256(entry["tags"]),
            "category_id": entry["category_id"],
            "made_for_kids": entry["made_for_kids"],
            "synthetic_narration_disclosed": (
                entry["contains_synthetic_narration_disclosure"]
            ),
            "state": "exact",
        }
        for key, expected in metadata_exact.items():
            if metadata.get(key) != expected:
                failures.append(f"{entry['chapter_id']}: metadata {key} drift")
        accessibility = receipt.get("accessibility", {})
        caption = ROOT / entry["caption_path"]
        thumbnail = ROOT / entry["thumbnail_path"]
        accessibility_exact = {
            "caption_path": entry["caption_path"],
            "caption_sha256": sha256(caption) if caption.is_file() else None,
            "caption_language": "en",
            "caption_state": "published",
            "thumbnail_path": entry["thumbnail_path"],
            "thumbnail_sha256": sha256(thumbnail) if thumbnail.is_file() else None,
            "thumbnail_state": "applied",
        }
        for key, expected in accessibility_exact.items():
            if accessibility.get(key) != expected:
                failures.append(f"{entry['chapter_id']}: accessibility {key} drift")
        video_id = receipt.get("video_id")
        playlist_item_id = receipt.get("playlist_item_id")
        if video_id in video_ids:
            failures.append(f"{entry['chapter_id']}: duplicate YouTube video ID")
        if playlist_item_id in playlist_item_ids:
            failures.append(f"{entry['chapter_id']}: duplicate playlist item ID")
        video_ids.add(video_id)
        playlist_item_ids.add(playlist_item_id)
        playlist_ids.add(receipt.get("playlist_id"))
        rows.append((entry, receipt, path))
    if len(playlist_ids) != 1:
        failures.append(f"expected one canonical playlist ID, found {playlist_ids}")
    if len(rows) != 84:
        failures.append(f"expected 84 validatable receipt rows, found {len(rows)}")
    if failures:
        raise SystemExit(
            "YouTube publication receipt reconciliation failed:\n - "
            + "\n - ".join(failures)
        )
    return rows, next(iter(playlist_ids))


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def transaction_paths(rows: list[tuple[dict, dict, Path]]) -> list[Path]:
    structure = load(ROOT / "book_structure.json")
    chapter_paths = [
        ROOT / chapter["file"]
        for part in structure["parts"]
        for chapter in part["chapters"]
    ]
    packet_paths = [
        ROOT / f"visual_edition/chapters/{entry['chapter_id']}/packet.json"
        for entry, _, _ in rows
    ]
    return [CHANNEL, MANIFEST, LEDGER, *packet_paths, *chapter_paths]


def restore(snapshot: dict[Path, bytes | None]) -> None:
    for path, prior in snapshot.items():
        if prior is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(prior)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization-scope-sha256", required=True)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write packet/channel/embed reconciliation after all checks pass",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{64}", args.authorization_scope_sha256):
        raise SystemExit("authorization scope must be a lowercase SHA-256 digest")
    rows, playlist_id = validate_receipts(args.authorization_scope_sha256)
    if not args.write:
        print(
            "YouTube publication receipts are ready to reconcile: "
            "84/84 exact public rows, one ordered playlist, no files changed."
        )
        return
    paths = transaction_paths(rows)
    snapshot = {
        path: path.read_bytes() if path.is_file() else None
        for path in paths
    }
    try:
        channel = load(CHANNEL)
        channel["canonical_playlist"].update({
            "playlist_id": playlist_id,
            "playlist_url": f"https://www.youtube.com/playlist?list={playlist_id}",
            "state": "public",
        })
        CHANNEL.write_text(json.dumps(channel, indent=2) + "\n", encoding="utf-8")
        for entry, receipt, path in rows:
            packet_path = (
                ROOT / f"visual_edition/chapters/{entry['chapter_id']}/packet.json"
            )
            packet = load(packet_path)
            packet["lifecycle_state"] = "published_current"
            packet["render_receipt"]["remaining_release_gates"] = []
            packet["youtube"] = {
                "channel_id": receipt["channel_id"],
                "video_id": receipt["video_id"],
                "watch_url": receipt["watch_url"],
                "playlist_id": receipt["playlist_id"],
                "generation": receipt["generation"],
                "publication_state": "published_current",
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
                "platform_receipt_path": str(path.relative_to(ROOT)),
                "supersedes_video_id": receipt["supersedes_video_id"],
            }
            packet["quarto_embed"]["state"] = "published_current"
            packet_path.write_text(
                json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        run("python3", "scripts/build_visual_edition_manifest.py")
        run("python3", "scripts/build_youtube_ledger.py")
        run("python3", "scripts/sync_visual_edition_embeds.py", "--write")
        run("python3", "scripts/validate_visual_edition.py")
    except Exception:
        restore(snapshot)
        raise
    print(
        "Reconciled 84 public YouTube receipts into packets, playlist identity, "
        "ledger, manifest, and Quarto embeds."
    )


if __name__ == "__main__":
    main()
