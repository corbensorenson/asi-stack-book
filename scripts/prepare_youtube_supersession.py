#!/usr/bin/env python3
"""Prepare one exact, non-authorizing YouTube replacement generation."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

from build_youtube_upload_plan import compact, youtube_title


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
CHANNEL = ROOT / "visual_edition/youtube_channel.json"
PLAN_SCHEMA = ROOT / "schemas/youtube_supersession_plan.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
OUT_ROOT = ROOT / "visual_edition/supersession_plans"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")


def chapter_record(chapter_id: str) -> tuple[int, dict]:
    position = 0
    for part in load(STRUCTURE)["parts"]:
        for chapter in part["chapters"]:
            position += 1
            if chapter["id"] == chapter_id:
                return position, chapter
    raise SystemExit(f"Unknown chapter: {chapter_id}")


def schema_failures(value: dict, schema_path: Path) -> list[str]:
    return [
        f"{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(load(schema_path)).iter_errors(value)
    ]


def semantic_failures(plan: dict) -> list[str]:
    failures = []
    predecessor = plan.get("predecessor", {})
    replacement = plan.get("replacement", {})
    expected_generation = int(predecessor.get("generation", 0)) + 1
    if plan.get("generation") != expected_generation:
        failures.append("replacement generation is not predecessor plus one")
    if (
        replacement.get("local_master_sha256")
        == predecessor.get("uploaded_output_sha256")
        and replacement.get("bound_chapter_sha256")
        == predecessor.get("bound_chapter_sha256")
    ):
        failures.append("replacement is byte-and-chapter identical to predecessor")
    expected_key = (
        f"asi-youtube-supersession:{plan.get('chapter_id')}:"
        f"g{plan.get('generation')}:{replacement.get('local_master_sha256')}"
    )
    if plan.get("idempotency_key") != expected_key:
        failures.append("supersession idempotency key drift")
    if plan.get("playlist_position") not in range(1, 85):
        failures.append("supersession playlist position is out of range")
    if plan.get("external_mutation_authorized_now") is not False:
        failures.append("supersession plan improperly claims mutation authority")
    return failures


def build(
    chapter_id: str,
    change_reason: str,
    generated_at_utc: str | None = None,
) -> dict:
    position, chapter = chapter_record(chapter_id)
    packet_path = ROOT / f"visual_edition/chapters/{chapter_id}/packet.json"
    packet = load(packet_path)
    youtube = packet["youtube"]
    if packet.get("lifecycle_state") != "ready_not_published":
        raise SystemExit(
            f"{chapter_id}: replacement derivative is not ready_not_published"
        )
    if (
        youtube.get("publication_state") != "stale"
        or not youtube.get("video_id")
        or int(youtube.get("generation", 0)) < 1
        or not youtube.get("platform_receipt_path")
    ):
        raise SystemExit(
            f"{chapter_id}: no stale published predecessor is available"
        )
    receipt_path = ROOT / youtube["platform_receipt_path"]
    if not receipt_path.is_file():
        raise SystemExit(f"{chapter_id}: predecessor receipt is missing")
    predecessor = load(receipt_path)
    receipt_failures = schema_failures(predecessor, RECEIPT_SCHEMA)
    if receipt_failures:
        raise SystemExit(
            f"{chapter_id}: predecessor receipt invalid:\n - "
            + "\n - ".join(receipt_failures)
        )
    channel = load(CHANNEL)
    playlist_id = channel["canonical_playlist"]["playlist_id"]
    if (
        channel["canonical_playlist"]["state"] != "public"
        or not playlist_id
        or predecessor["playlist_id"] != playlist_id
        or predecessor["video_id"] != youtube["video_id"]
        or predecessor["generation"] != youtube["generation"]
    ):
        raise SystemExit(f"{chapter_id}: predecessor or playlist identity drift")
    master = ROOT / f"build/visual_edition/final/{chapter_id}.mp4"
    caption = ROOT / packet["artifacts"]["captions"]
    thumbnail = ROOT / f"build/visual_edition/thumbnails/{chapter_id}.png"
    for path in (master, caption, thumbnail):
        if not path.is_file():
            raise SystemExit(f"{chapter_id}: replacement input missing: {path}")
    master_digest = sha256(master)
    if (
        packet.get("render_receipt", {}).get("validation_state") != "validated"
        or packet["render_receipt"].get("output_sha256") != master_digest
    ):
        raise SystemExit(f"{chapter_id}: replacement master is not exactly validated")
    prior_source = predecessor["source_upload"]
    if (
        master_digest == prior_source["local_master_sha256"]
        and packet["chapter_sha256"] == prior_source["bound_chapter_sha256"]
    ):
        raise SystemExit(
            f"{chapter_id}: replacement does not differ from its predecessor"
        )
    generation = predecessor["generation"] + 1
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
        f"Generation: {generation}",
        f"Supersedes: {predecessor['watch_url']}",
        f"Stable video identity: {packet['video_id']}",
        f"Chapter digest: {packet['chapter_sha256']}",
        f"Source commit: {packet['source_commit']}",
    ])
    plan = {
        "schema_version": "asi_stack.youtube_supersession_plan.v1",
        "plan_id": f"youtube-supersession-{chapter_id}-g{generation}",
        "generated_at_utc": generated_at_utc or now(),
        "state": "ready_not_authorized",
        "channel_id": channel["channel"]["channel_id"],
        "playlist_id": playlist_id,
        "playlist_position": position,
        "chapter_id": chapter_id,
        "chapter_path": chapter["file"],
        "stable_internal_video_id": packet["video_id"],
        "generation": generation,
        "change_reason": change_reason,
        "predecessor": {
            "generation": predecessor["generation"],
            "video_id": predecessor["video_id"],
            "watch_url": predecessor["watch_url"],
            "playlist_item_id": predecessor["playlist_item_id"],
            "platform_receipt_path": str(receipt_path.relative_to(ROOT)),
            "platform_receipt_sha256": sha256(receipt_path),
            "uploaded_output_sha256": prior_source["local_master_sha256"],
            "bound_chapter_sha256": prior_source["bound_chapter_sha256"],
            "bound_source_commit": prior_source["bound_source_commit"],
            "required_final_disposition": (
                "unlisted_outside_canonical_playlist_with_pointer_to_successor"
            ),
        },
        "replacement": {
            "title": youtube_title(position, chapter["title"]),
            "description": description,
            "tags": [
                "The ASI Stack",
                "artificial intelligence",
                "AI architecture",
                "AI governance",
                "AI safety",
            ],
            "category_id": "27",
            "made_for_kids": False,
            "contains_synthetic_narration_disclosure": True,
            "local_master_path": str(master.relative_to(ROOT)),
            "local_master_sha256": master_digest,
            "local_master_bytes": master.stat().st_size,
            "caption_path": str(caption.relative_to(ROOT)),
            "caption_sha256": sha256(caption),
            "thumbnail_path": str(thumbnail.relative_to(ROOT)),
            "thumbnail_sha256": sha256(thumbnail),
            "bound_chapter_sha256": packet["chapter_sha256"],
            "bound_source_commit": packet["source_commit"],
            "initial_upload_privacy": "unlisted",
            "desired_final_privacy": "public",
        },
        "idempotency_key": (
            f"asi-youtube-supersession:{chapter_id}:g{generation}:{master_digest}"
        ),
        "ordered_platform_steps": [
            "recheck exact signed-in channel and scope digest",
            "upload the replacement master once as unlisted",
            "wait for HD processing and apply exact metadata captions and thumbnail",
            "insert the replacement at the predecessor canonical playlist position",
            "verify replacement watch accessibility metadata captions thumbnail and playlist position",
            "set the replacement public",
            "mark the predecessor description with a current-generation pointer",
            "set the predecessor unlisted and remove its old canonical playlist item",
            "record replacement and predecessor-disposition observations",
            "reconcile packet generation ledger and Quarto embed atomically",
        ],
        "rollback_contract": [
            "before replacement publication retain the predecessor as current and keep the candidate unlisted",
            "if playlist switching fails restore the predecessor playlist item and keep the candidate unlisted",
            "if repository reconciliation fails restore packet ledger manifest and Quarto bytes while retaining platform receipts",
            "never delete either generation as an automatic rollback",
        ],
        "allowed_platform_mutations": [
            "upload one exact replacement master",
            "apply exact replacement metadata captions and thumbnail",
            "insert one replacement playlist item at the predecessor position",
            "set the replacement public after all checks pass",
            "annotate and set the predecessor unlisted",
            "remove only the predecessor canonical playlist item",
            "read exact platform state for receipts",
        ],
        "prohibited_mutations": [
            "delete either video generation",
            "modify any unrelated video playlist comment subscription or channel setting",
            "reuse this plan for another chapter generation or master digest",
            "duplicate a completed replacement upload",
            "leave both generations in the canonical playlist",
            "mark the replacement current before receipt and embed reconciliation",
        ],
        "stop_conditions": [
            "signed-in channel playlist predecessor or digest identity differs",
            "the replacement no longer matches its validated packet inputs",
            "YouTube reports a limit policy warning unresolved processing error or ambiguous mutation result",
            "accessibility metadata playlist order or predecessor disposition cannot be verified",
            "receipt or repository reconciliation validation fails",
        ],
        "external_mutation_authorized_now": False,
        "support_state_effect": "none",
        "book_claim_release_effect": "none",
        "non_claims": [
            "Preparing this plan does not authorize a YouTube or playlist mutation.",
            "Replacing an explanatory video does not promote a chapter claim or support state.",
            "A successful platform switch does not validate the chapter argument.",
            "The workflow does not establish safety, deployment efficacy, transfer, AGI, or ASI.",
        ],
    }
    failures = schema_failures(plan, PLAN_SCHEMA)
    failures.extend(semantic_failures(plan))
    if failures:
        raise SystemExit(
            "Supersession plan invalid:\n - " + "\n - ".join(failures)
        )
    return plan


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter-id", required=True)
    parser.add_argument("--change-reason", required=True)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the tracked exact plan; default is validation-only preview",
    )
    args = parser.parse_args()
    plan = build(args.chapter_id, args.change_reason)
    output = OUT_ROOT / f"{args.chapter_id}-g{plan['generation']}.json"
    if args.write:
        OUT_ROOT.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"Wrote {output.relative_to(ROOT)}; exact scope SHA-256 {sha256(output)}"
        )
    else:
        print(json.dumps(plan, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
