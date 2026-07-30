#!/usr/bin/env python3
"""Atomically reconcile one observed replacement generation into the book."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

from prepare_youtube_supersession import semantic_failures as plan_semantic_failures

ROOT = Path(__file__).resolve().parents[1]
PLAN_SCHEMA = ROOT / "schemas/youtube_supersession_plan.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
MANIFEST = ROOT / "visual_edition/manifest.json"
LEDGER = ROOT / "visual_edition/youtube_ledger.json"


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


def schema_errors(value: dict, schema_path: Path, label: str) -> list[str]:
    return [
        f"{label}:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(load(schema_path)).iter_errors(value)
    ]


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def restore(snapshot: dict[Path, bytes | None]) -> None:
    for path, prior in snapshot.items():
        if prior is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(prior)


def receipt_semantic_failures(plan: dict, receipt: dict) -> list[str]:
    failures = []
    predecessor = plan.get("predecessor", {})
    disposition = receipt.get("predecessor_disposition") or {}
    exact = {
        "chapter_id": plan.get("chapter_id"),
        "stable_internal_video_id": plan.get("stable_internal_video_id"),
        "generation": plan.get("generation"),
        "channel_id": plan.get("channel_id"),
        "playlist_id": plan.get("playlist_id"),
        "playlist_position": plan.get("playlist_position"),
        "supersedes_video_id": predecessor.get("video_id"),
    }
    for key, expected in exact.items():
        if receipt.get(key) != expected:
            failures.append(f"replacement receipt {key} drift")
    if receipt.get("video_id") == predecessor.get("video_id"):
        failures.append("replacement reuses predecessor video ID")
    disposition_exact = {
        "video_id": predecessor.get("video_id"),
        "old_playlist_item_id": predecessor.get("playlist_item_id"),
        "privacy_status": "unlisted",
        "playlist_state": "removed_from_canonical_playlist",
        "current_pointer_state": "points_to_successor",
    }
    for key, expected in disposition_exact.items():
        if disposition.get(key) != expected:
            failures.append(f"predecessor disposition {key} drift")
    return failures


def validate(
    plan_path: Path,
    receipt_path: Path,
    authority_digest: str,
) -> tuple[dict, dict, Path, dict]:
    plan = load(plan_path)
    receipt = load(receipt_path)
    failures = schema_errors(plan, PLAN_SCHEMA, "plan")
    failures.extend(
        f"plan:{failure}" for failure in plan_semantic_failures(plan)
    )
    failures.extend(schema_errors(receipt, RECEIPT_SCHEMA, "receipt"))
    failures.extend(receipt_semantic_failures(plan, receipt))
    if authority_digest != sha256(plan_path):
        failures.append("authorization digest does not match exact plan")
    packet_path = (
        ROOT / f"visual_edition/chapters/{plan.get('chapter_id')}/packet.json"
    )
    if not packet_path.is_file():
        failures.append("current chapter packet is missing")
        packet = {}
    else:
        packet = load(packet_path)
    predecessor_receipt_path = ROOT / plan.get("predecessor", {}).get(
        "platform_receipt_path", ""
    )
    predecessor_receipt = (
        load(predecessor_receipt_path)
        if predecessor_receipt_path.is_file()
        else {}
    )
    if (
        not predecessor_receipt_path.is_file()
        or sha256(predecessor_receipt_path)
        != plan.get("predecessor", {}).get("platform_receipt_sha256")
    ):
        failures.append("predecessor receipt is missing or drifted")
    current_youtube = packet.get("youtube", {})
    packet_exact = {
        "chapter_id": plan.get("chapter_id"),
        "chapter_path": plan.get("chapter_path"),
        "video_id": plan.get("stable_internal_video_id"),
        "lifecycle_state": "ready_not_published",
        "chapter_sha256": plan.get("replacement", {}).get(
            "bound_chapter_sha256"
        ),
        "source_commit": plan.get("replacement", {}).get(
            "bound_source_commit"
        ),
    }
    for key, expected in packet_exact.items():
        if packet.get(key) != expected:
            failures.append(f"packet {key} drift")
    youtube_exact = {
        "publication_state": "stale",
        "video_id": plan.get("predecessor", {}).get("video_id"),
        "generation": plan.get("predecessor", {}).get("generation"),
        "playlist_id": plan.get("playlist_id"),
        "platform_receipt_path": plan.get("predecessor", {}).get(
            "platform_receipt_path"
        ),
    }
    for key, expected in youtube_exact.items():
        if current_youtube.get(key) != expected:
            failures.append(f"packet predecessor {key} drift")
    replacement = plan.get("replacement", {})
    receipt_exact = {"authorization_scope_sha256": authority_digest}
    for key, expected in receipt_exact.items():
        if receipt.get(key) != expected:
            failures.append(f"replacement receipt {key} drift")
    source = receipt.get("source_upload", {})
    source_exact = {
        "local_master_path": replacement.get("local_master_path"),
        "local_master_sha256": replacement.get("local_master_sha256"),
        "local_master_bytes": replacement.get("local_master_bytes"),
        "bound_chapter_sha256": replacement.get("bound_chapter_sha256"),
        "bound_source_commit": replacement.get("bound_source_commit"),
    }
    for key, expected in source_exact.items():
        if source.get(key) != expected:
            failures.append(f"replacement source {key} drift")
    metadata = receipt.get("metadata", {})
    metadata_exact = {
        "title_sha256": text_sha256(replacement.get("title", "")),
        "description_sha256": text_sha256(replacement.get("description", "")),
        "tags_sha256": tags_sha256(replacement.get("tags", [])),
        "category_id": replacement.get("category_id"),
        "made_for_kids": replacement.get("made_for_kids"),
        "synthetic_narration_disclosed": replacement.get(
            "contains_synthetic_narration_disclosure"
        ),
        "state": "exact",
    }
    for key, expected in metadata_exact.items():
        if metadata.get(key) != expected:
            failures.append(f"replacement metadata {key} drift")
    accessibility = receipt.get("accessibility", {})
    accessibility_exact = {
        "caption_path": replacement.get("caption_path"),
        "caption_sha256": replacement.get("caption_sha256"),
        "caption_language": "en",
        "caption_state": "published",
        "thumbnail_path": replacement.get("thumbnail_path"),
        "thumbnail_sha256": replacement.get("thumbnail_sha256"),
        "thumbnail_state": "applied",
    }
    for key, expected in accessibility_exact.items():
        if accessibility.get(key) != expected:
            failures.append(f"replacement accessibility {key} drift")
    if predecessor_receipt and (
        predecessor_receipt.get("video_id")
        != plan.get("predecessor", {}).get("video_id")
        or predecessor_receipt.get("generation")
        != plan.get("predecessor", {}).get("generation")
    ):
        failures.append("predecessor receipt identity drift")
    for path_key, digest_key in (
        ("local_master_path", "local_master_sha256"),
        ("caption_path", "caption_sha256"),
        ("thumbnail_path", "thumbnail_sha256"),
    ):
        path = ROOT / replacement.get(path_key, "")
        if not path.is_file() or sha256(path) != replacement.get(digest_key):
            failures.append(f"replacement file {path_key} missing or drifted")
    if failures:
        raise SystemExit(
            "YouTube supersession reconciliation failed:\n - "
            + "\n - ".join(failures)
        )
    return plan, receipt, packet_path, packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--authorization-scope-sha256", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{64}", args.authorization_scope_sha256):
        raise SystemExit("authorization scope must be a lowercase SHA-256 digest")
    plan_path = ROOT / args.plan
    receipt_path = ROOT / args.receipt
    plan, receipt, packet_path, packet = validate(
        plan_path,
        receipt_path,
        args.authorization_scope_sha256,
    )
    if not args.write:
        print(
            f"YouTube supersession ready to reconcile: {plan['chapter_id']} "
            f"generation {plan['generation']}, no files changed."
        )
        return
    chapter_path = ROOT / plan["chapter_path"]
    paths = [packet_path, chapter_path, MANIFEST, LEDGER]
    snapshot = {
        path: path.read_bytes() if path.is_file() else None
        for path in paths
    }
    try:
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
            "platform_receipt_path": str(receipt_path.relative_to(ROOT)),
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
        f"Reconciled {plan['chapter_id']} generation {plan['generation']}; "
        "predecessor receipt preserved and current embed replaced."
    )


if __name__ == "__main__":
    main()
