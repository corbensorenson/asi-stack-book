#!/usr/bin/env python3
"""Validate the dormant generation-N YouTube replacement workflow."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

from prepare_youtube_supersession import (
    build as build_plan,
    semantic_failures as plan_semantic_failures,
)
from build_youtube_ledger import generation_history
from reconcile_youtube_supersession_receipt import receipt_semantic_failures
from visual_publication_lifecycle import preserve_predecessor_projection


ROOT = Path(__file__).resolve().parents[1]
PLAN_SCHEMA_PATH = ROOT / "schemas/youtube_supersession_plan.schema.json"
RECEIPT_SCHEMA_PATH = ROOT / "schemas/youtube_platform_receipt.schema.json"
PLAN_ROOT = ROOT / "visual_edition/supersession_plans"
RECEIPT_ROOT = ROOT / "visual_edition/platform_receipts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


PLAN_SCHEMA = load(PLAN_SCHEMA_PATH)
RECEIPT_SCHEMA = load(RECEIPT_SCHEMA_PATH)


def schema_errors(value: dict, schema: dict) -> list[str]:
    return [
        f"{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(value)
    ]


def fixture_plan() -> dict:
    arrays = PLAN_SCHEMA["properties"]
    return {
        "schema_version": "asi_stack.youtube_supersession_plan.v1",
        "plan_id": "youtube-supersession-example-chapter-g2",
        "generated_at_utc": "2026-07-30T12:00:00Z",
        "state": "ready_not_authorized",
        "channel_id": "UCX7Tu67cGmKfT6O38xxiQFA",
        "playlist_id": "PLexample123456",
        "playlist_position": 4,
        "chapter_id": "example-chapter",
        "chapter_path": "chapters/example-chapter.qmd",
        "stable_internal_video_id": "asi-video-example-chapter",
        "generation": 2,
        "change_reason": "Author feedback requires a corrected visual explanation.",
        "predecessor": {
            "generation": 1,
            "video_id": "OldVideo001",
            "watch_url": "https://www.youtube.com/watch?v=OldVideo001",
            "playlist_item_id": "OldPlaylistItem001",
            "platform_receipt_path": (
                "visual_edition/platform_receipts/generation-1/"
                "example-chapter.json"
            ),
            "platform_receipt_sha256": "1" * 64,
            "uploaded_output_sha256": "2" * 64,
            "bound_chapter_sha256": "3" * 64,
            "bound_source_commit": "4" * 40,
            "required_final_disposition": (
                "unlisted_outside_canonical_playlist_with_pointer_to_successor"
            ),
        },
        "replacement": {
            "title": "04. Example Chapter — The ASI Stack",
            "description": (
                "This is a sufficiently detailed replacement description that "
                "binds the live book, evidence boundary, chapter digest, source "
                "commit, synthetic narration disclosure, and predecessor identity."
            ),
            "tags": [
                "The ASI Stack",
                "artificial intelligence",
                "AI architecture",
            ],
            "category_id": "27",
            "made_for_kids": False,
            "contains_synthetic_narration_disclosure": True,
            "local_master_path": "build/visual_edition/final/example-chapter.mp4",
            "local_master_sha256": "5" * 64,
            "local_master_bytes": 123456,
            "caption_path": (
                "visual_edition/chapters/example-chapter/captions.vtt"
            ),
            "caption_sha256": "6" * 64,
            "thumbnail_path": (
                "build/visual_edition/thumbnails/example-chapter.png"
            ),
            "thumbnail_sha256": "7" * 64,
            "bound_chapter_sha256": "8" * 64,
            "bound_source_commit": "9" * 40,
            "initial_upload_privacy": "unlisted",
            "desired_final_privacy": "public",
        },
        "idempotency_key": (
            "asi-youtube-supersession:example-chapter:g2:" + "5" * 64
        ),
        "ordered_platform_steps": arrays["ordered_platform_steps"]["const"],
        "rollback_contract": arrays["rollback_contract"]["const"],
        "allowed_platform_mutations": arrays[
            "allowed_platform_mutations"
        ]["const"],
        "prohibited_mutations": arrays["prohibited_mutations"]["const"],
        "stop_conditions": arrays["stop_conditions"]["const"],
        "external_mutation_authorized_now": False,
        "support_state_effect": "none",
        "book_claim_release_effect": "none",
        "non_claims": [
            "Preparing the plan is not external mutation authority.",
            "The replacement does not promote the chapter claim.",
            "The predecessor remains historical and is not erased.",
            "The workflow does not establish safety, AGI, or ASI.",
        ],
    }


def fixture_receipt(plan: dict) -> dict:
    return {
        "schema_version": "asi_stack.youtube_platform_receipt.v1",
        "receipt_id": "youtube-example-chapter-g2",
        "recorded_at_utc": "2026-07-30T12:30:00Z",
        "authorization_scope_sha256": "a" * 64,
        "adapter": "youtube_studio_signed_in_browser",
        "chapter_id": plan["chapter_id"],
        "stable_internal_video_id": plan["stable_internal_video_id"],
        "generation": plan["generation"],
        "channel_id": plan["channel_id"],
        "video_id": "NewVideo002",
        "watch_url": "https://www.youtube.com/watch?v=NewVideo002",
        "playlist_id": plan["playlist_id"],
        "playlist_item_id": "NewPlaylistItem002",
        "playlist_position": plan["playlist_position"],
        "source_upload": {
            "local_master_path": plan["replacement"]["local_master_path"],
            "local_master_sha256": plan["replacement"]["local_master_sha256"],
            "local_master_bytes": plan["replacement"]["local_master_bytes"],
            "bound_chapter_sha256": plan["replacement"][
                "bound_chapter_sha256"
            ],
            "bound_source_commit": plan["replacement"]["bound_source_commit"],
        },
        "metadata": {
            "title_sha256": "b" * 64,
            "description_sha256": "c" * 64,
            "tags_sha256": "d" * 64,
            "category_id": "27",
            "made_for_kids": False,
            "synthetic_narration_disclosed": True,
            "state": "exact",
        },
        "accessibility": {
            "caption_path": plan["replacement"]["caption_path"],
            "caption_sha256": plan["replacement"]["caption_sha256"],
            "caption_language": "en",
            "caption_track_id": "caption-track-2",
            "caption_state": "published",
            "thumbnail_path": plan["replacement"]["thumbnail_path"],
            "thumbnail_sha256": plan["replacement"]["thumbnail_sha256"],
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
            "observed_at_utc": "2026-07-30T12:30:00Z",
            "observation_payload_sha256": "e" * 64,
        },
        "supersedes_video_id": plan["predecessor"]["video_id"],
        "predecessor_disposition": {
            "video_id": plan["predecessor"]["video_id"],
            "old_playlist_item_id": plan["predecessor"][
                "playlist_item_id"
            ],
            "privacy_status": "unlisted",
            "playlist_state": "removed_from_canonical_playlist",
            "current_pointer_state": "points_to_successor",
            "observed_at_utc": "2026-07-30T12:30:00Z",
            "observation_payload_sha256": "f" * 64,
        },
        "support_state_effect": "none",
        "book_claim_release_effect": "none",
        "non_claims": [
            "The replacement does not promote the book claim.",
            "The predecessor historical identity remains preserved.",
            "Platform processing does not verify the argument.",
            "The receipt does not establish safety, AGI, or ASI.",
        ],
    }


def validate_tracked_plans() -> list[str]:
    failures = []
    for path in sorted(PLAN_ROOT.glob("*.json")) if PLAN_ROOT.exists() else []:
        plan = load(path)
        failures.extend(
            f"{path.name}:{error}"
            for error in schema_errors(plan, PLAN_SCHEMA)
        )
        failures.extend(
            f"{path.name}:{error}" for error in plan_semantic_failures(plan)
        )
        if not failures:
            expected = build_plan(
                plan["chapter_id"],
                plan["change_reason"],
                plan["generated_at_utc"],
            )
            if expected != plan:
                failures.append(f"{path.name}: current input binding drift")
    return failures


def main() -> None:
    failures = validate_tracked_plans()
    plan = fixture_plan()
    receipt = fixture_receipt(plan)
    failures.extend(schema_errors(plan, PLAN_SCHEMA))
    failures.extend(plan_semantic_failures(plan))
    failures.extend(schema_errors(receipt, RECEIPT_SCHEMA))
    failures.extend(receipt_semantic_failures(plan, receipt))

    prior = {
        "youtube": {
            "publication_state": "published_current",
            "video_id": "OldVideo001",
            "generation": 1,
            "playlist_id": "PLexample123456",
        },
        "quarto_embed": {"state": "published_current"},
    }
    fresh = {
        "youtube": {
            "publication_state": "not_authorized",
            "video_id": None,
            "generation": 0,
        },
        "quarto_embed": {"state": "absent_until_published"},
    }
    preserved = preserve_predecessor_projection(prior, fresh)
    if (
        preserved["youtube"].get("video_id") != "OldVideo001"
        or preserved["youtube"].get("publication_state") != "stale"
        or preserved["quarto_embed"].get("state") != "historical_removed"
    ):
        failures.append("published predecessor was not preserved as stale")

    with tempfile.TemporaryDirectory() as temporary:
        receipt_root = Path(temporary)
        old_receipt = copy.deepcopy(receipt)
        old_receipt.update({
            "receipt_id": "youtube-example-chapter-g1",
            "generation": 1,
            "video_id": plan["predecessor"]["video_id"],
            "watch_url": plan["predecessor"]["watch_url"],
            "playlist_item_id": plan["predecessor"]["playlist_item_id"],
            "supersedes_video_id": None,
            "predecessor_disposition": None,
        })
        old_receipt["source_upload"].update({
            "local_master_sha256": plan["predecessor"][
                "uploaded_output_sha256"
            ],
            "bound_chapter_sha256": plan["predecessor"][
                "bound_chapter_sha256"
            ],
            "bound_source_commit": plan["predecessor"][
                "bound_source_commit"
            ],
        })
        for generation, value in ((1, old_receipt), (2, receipt)):
            path = (
                receipt_root
                / f"generation-{generation}"
                / "example-chapter.json"
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value), encoding="utf-8")
        history = generation_history(
            "example-chapter",
            {
                "video_id": receipt["video_id"],
                "publication_state": "published_current",
            },
            receipt_root,
        )
        if (
            [row["generation"] for row in history] != [1, 2]
            or [row["publication_state"] for row in history]
            != ["superseded", "published_current"]
        ):
            failures.append("two-generation ledger history was not preserved")
        broken = receipt_root / "generation-2" / "example-chapter.json"
        broken_value = load(broken)
        broken_value["supersedes_video_id"] = "WrongPred01"
        broken.write_text(json.dumps(broken_value), encoding="utf-8")
        try:
            generation_history(
                "example-chapter",
                {
                    "video_id": receipt["video_id"],
                    "publication_state": "published_current",
                },
                receipt_root,
            )
        except SystemExit:
            pass
        else:
            failures.append("broken generation predecessor chain was accepted")

    mutations: list[tuple[str, dict, dict]] = []

    def plan_mutation(label: str, edit) -> None:
        candidate = copy.deepcopy(plan)
        edit(candidate)
        mutations.append((label, candidate, receipt))

    def receipt_mutation(label: str, edit) -> None:
        candidate = copy.deepcopy(receipt)
        edit(candidate)
        mutations.append((label, plan, candidate))

    plan_mutation("generation gap", lambda d: d.__setitem__("generation", 3))
    plan_mutation(
        "identical predecessor",
        lambda d: d["replacement"].update({
            "local_master_sha256": d["predecessor"]["uploaded_output_sha256"],
            "bound_chapter_sha256": d["predecessor"]["bound_chapter_sha256"],
        }),
    )
    plan_mutation(
        "idempotency drift",
        lambda d: d.__setitem__(
            "idempotency_key",
            "asi-youtube-supersession:example-chapter:g2:" + "0" * 64,
        ),
    )
    plan_mutation(
        "premature authority",
        lambda d: d.__setitem__("external_mutation_authorized_now", True),
    )
    plan_mutation(
        "delete permission",
        lambda d: d["prohibited_mutations"].remove(
            "delete either video generation"
        ),
    )
    plan_mutation(
        "rollback deletion",
        lambda d: d["rollback_contract"].pop(),
    )
    plan_mutation(
        "support promotion",
        lambda d: d.__setitem__("support_state_effect", "promotion"),
    )
    receipt_mutation(
        "video ID reuse",
        lambda d: d.update({
            "video_id": plan["predecessor"]["video_id"],
            "watch_url": plan["predecessor"]["watch_url"],
        }),
    )
    receipt_mutation(
        "missing predecessor disposition",
        lambda d: d.__setitem__("predecessor_disposition", None),
    )
    receipt_mutation(
        "wrong old playlist item",
        lambda d: d["predecessor_disposition"].__setitem__(
            "old_playlist_item_id", "WrongPlaylistItem"
        ),
    )
    receipt_mutation(
        "predecessor deletion",
        lambda d: d["predecessor_disposition"].__setitem__(
            "privacy_status", "private"
        ),
    )
    receipt_mutation(
        "support promotion receipt",
        lambda d: d.__setitem__("support_state_effect", "promotion"),
    )
    for label, candidate_plan, candidate_receipt in mutations:
        candidate_failures = schema_errors(candidate_plan, PLAN_SCHEMA)
        candidate_failures.extend(plan_semantic_failures(candidate_plan))
        candidate_failures.extend(
            schema_errors(candidate_receipt, RECEIPT_SCHEMA)
        )
        candidate_failures.extend(
            receipt_semantic_failures(candidate_plan, candidate_receipt)
        )
        if not candidate_failures:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "YouTube supersession workflow validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "YouTube supersession workflow passed: predecessor preservation, "
        "generation-N plan/receipt schemas, 12/12 mutations rejected, "
        "no external mutation authorized."
    )


if __name__ == "__main__":
    main()
