#!/usr/bin/env python3
"""Validate the owner-authorized partial YouTube preview projection."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

from visual_chapter_source import canonical_chapter_sha256


ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "visual_edition/youtube_preview_bindings.json"
SCHEMA = ROOT / "schemas/youtube_preview_bindings.schema.json"
UPLOAD_PLAN = ROOT / "visual_edition/youtube_upload_plan.json"
GENERATION2_CANDIDATES = ROOT / "visual_edition/youtube_generation2_upload_candidates.json"
MANIFEST = ROOT / "visual_edition/manifest.json"
BEGIN = "<!-- BEGIN MANAGED VISUAL ABSTRACT:{chapter_id} -->"
END = "<!-- END MANAGED VISUAL ABSTRACT:{chapter_id} -->"
ROSTER_BEGIN = "<!-- BEGIN MANAGED VISUAL PREVIEW ROSTER -->"
ROSTER_END = "<!-- END MANAGED VISUAL PREVIEW ROSTER -->"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_errors(value: dict) -> list[str]:
    schema = load(SCHEMA)
    return [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(value)
    ]


def semantic_errors(
    preview: dict,
    *,
    check_manifest_binding: bool = True,
    check_projection: bool = True,
) -> list[str]:
    failures = schema_errors(preview)
    upload_plan = load(UPLOAD_PLAN)
    generation2 = load(GENERATION2_CANDIDATES)
    candidate_by_chapter = {
        row.get("chapter_id"): row for row in generation2.get("entries", [])
    }
    structure = load(ROOT / "book_structure.json")
    chapter_ids = []
    for part in structure.get("parts", []):
        chapter_ids.extend(
            chapter.get("id") for chapter in part.get("chapters", [])
        )
    chapter_positions = {
        chapter_id: position
        for position, chapter_id in enumerate(chapter_ids, start=1)
    }
    entries = preview.get("entries", [])
    count = len(entries)
    state = preview.get("state")
    withdrawn = state == "owner_withdrew_partial_unlisted_preview"
    if preview.get("preview_entry_count") != count:
        failures.append("preview entry count drift")
    withdrawn_entries = preview.get("withdrawn_entries", [])
    if withdrawn and len(withdrawn_entries) != 4:
        failures.append("withdrawn preview custody count drift")
    if withdrawn:
        withdrawn_ids = [entry.get("video_id") for entry in withdrawn_entries]
        if len(withdrawn_ids) != len(set(withdrawn_ids)) or any(
            not re.fullmatch(r"[A-Za-z0-9_-]{11}", value or "")
            for value in withdrawn_ids
        ):
            failures.append("withdrawn preview custody identity drift")
    bound_positions = {entry.get("position") for entry in entries}
    expected_next_position = next(
        (
            position
            for position in range(1, 85)
            if position not in bound_positions
        ),
        85,
    )
    if preview.get("next_upload_position") != expected_next_position:
        failures.append("next upload position is not the first unbound chapter")
    positions = [entry.get("position") for entry in entries]
    if count and all(isinstance(position, int) for position in positions):
        if positions != sorted(positions):
            failures.append("preview entries are not in canonical order")
    if len(positions) != len(set(positions)):
        failures.append("preview positions are not unique")
    if any(not isinstance(position, int) or not 1 <= position <= 84 for position in positions):
        failures.append("preview position is outside the canonical denominator")
    if withdrawn and count:
        failures.append("withdrawn preview projection retains current entries")
    if not withdrawn and not count:
        failures.append("active preview projection has no entries")
    video_ids = [entry.get("video_id") for entry in entries]
    if len(video_ids) != len(set(video_ids)):
        failures.append("preview video IDs are not unique")
    if (
        preview.get("authority_statement_sha256")
        != hashlib.sha256(
            preview.get("authority_statement", "").encode("utf-8")
        ).hexdigest()
    ):
        failures.append("preview authority statement digest drift")
    if preview.get("channel_id") != upload_plan.get("channel_id"):
        failures.append("preview/upload-plan channel identity drift")
    if generation2.get("channel_id") != upload_plan.get("channel_id"):
        failures.append("preview/generation-2 candidate channel identity drift")

    for entry in entries:
        chapter_id = entry.get("chapter_id")
        upload = candidate_by_chapter.get(chapter_id)
        if upload is None:
            failures.append(f"{chapter_id}: no exact generation-2 upload candidate")
            continue
        expected_position = chapter_positions.get(chapter_id)
        if expected_position is None:
            failures.append(f"{chapter_id}: preview chapter is not canonical")
            continue
        if entry.get("position") != expected_position:
            failures.append(f"{chapter_id}: preview position is not canonical")
        chapter_id = upload.get("chapter_id")
        packet_path = ROOT / f"visual_edition/chapters/{chapter_id}/packet.json"
        packet = load(packet_path)
        caption_path = ROOT / upload.get("caption_path", "")
        chapter_path = ROOT / packet.get("chapter_path", "")
        exact = {
            "position": expected_position,
            "chapter_id": chapter_id,
            "chapter_path": packet.get("chapter_path"),
            "title": upload.get("title"),
            "watch_url": f"https://www.youtube.com/watch?v={entry.get('video_id')}",
            "embed_url": (
                "https://www.youtube-nocookie.com/embed/"
                f"{entry.get('video_id')}"
            ),
            "playlist_position": expected_position,
            "video_visibility": "unlisted",
            "projection_state": "preview_current",
            "local_master_sha256": upload.get("local_master_sha256"),
            "bound_chapter_sha256": packet.get("chapter_sha256"),
            "bound_source_commit": packet.get("source_commit"),
            "descriptive_transcript_path": packet.get("artifacts", {}).get(
                "descriptive_transcript"
            ),
            "local_caption_path": upload.get("caption_path"),
            "local_caption_sha256": (
                digest(caption_path) if caption_path.is_file() else None
            ),
            "platform_caption_state": (
                "published"
                if upload.get("youtube_captions_state") == "published"
                else "machine_audited_local_vtt_not_yet_attached"
            ),
            "platform_thumbnail_state": (
                "applied"
                if upload.get("youtube_thumbnail_state") == "uploaded"
                else "not_yet_applied"
            ),
        }
        for key, expected in exact.items():
            if entry.get(key) != expected:
                failures.append(f"{chapter_id}: preview {key} drift")
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", entry.get("video_id", "")):
            failures.append(f"{chapter_id}: invalid YouTube video identity")
        if canonical_chapter_sha256(chapter_path) != entry.get(
            "bound_chapter_sha256"
        ):
            failures.append(f"{chapter_id}: preview chapter binding is stale")
        if packet.get("lifecycle_state") != "ready_not_published":
            failures.append(
                f"{chapter_id}: preview packet must remain ready_not_published"
            )
        if packet.get("youtube", {}).get("publication_state") == "published_current":
            failures.append(
                f"{chapter_id}: preview duplicates a published-current packet"
            )
        if packet.get("quarto_embed", {}).get("state") == "published_current":
            failures.append(
                f"{chapter_id}: preview is mislabeled as a current publication"
            )
        if check_projection:
            source = chapter_path.read_text(encoding="utf-8")
            begin = BEGIN.format(chapter_id=chapter_id)
            end = END.format(chapter_id=chapter_id)
            if source.count(begin) != 1 or source.count(end) != 1:
                failures.append(
                    f"{chapter_id}: exact managed preview block is absent"
                )
            elif (
                entry.get("embed_url") not in source
                or "unlisted staging preview" not in source
            ):
                failures.append(
                    f"{chapter_id}: managed preview block content is stale"
                )

    if check_projection:
        preview_ids = {entry.get("chapter_id") for entry in entries}
        for part in structure.get("parts", []):
            for chapter in part.get("chapters", []):
                if chapter.get("id") in preview_ids:
                    continue
                source = (ROOT / chapter["file"]).read_text(encoding="utf-8")
                if (
                    "youtube.com/embed/" in source
                    or "youtube-nocookie.com/embed/" in source
                ):
                    failures.append(
                        f"{chapter['id']}: unmanaged or out-of-preview YouTube embed"
                    )
        index_source = (ROOT / "index.qmd").read_text(encoding="utf-8")
        if (
            index_source.count(ROSTER_BEGIN) != 1
            or index_source.count(ROSTER_END) != 1
        ):
            failures.append("landing-page preview roster is absent")
        if withdrawn and "No visual abstracts are currently linked" not in index_source:
            failures.append("withdrawn preview roster does not state that current embeds are absent")
        for entry in entries:
            target = (
                f"{entry['chapter_path']}#visual-abstract"
            )
            if target not in index_source:
                failures.append(
                    f"{entry['chapter_id']}: landing-page preview link missing"
                )

    if check_manifest_binding:
        manifest = load(MANIFEST)
        manifest_preview = manifest.get("preview", {})
        expected_manifest = {
            "state": state,
            "binding_path": "visual_edition/youtube_preview_bindings.json",
            "binding_sha256": digest(PREVIEW),
            "unlisted_video_count": count,
            "current_quarto_preview_embeds": count,
            "edition_complete": False,
            "next_upload_position": expected_next_position,
        }
        for key, expected in expected_manifest.items():
            if manifest_preview.get(key) != expected:
                failures.append(f"manifest preview {key} drift")
        counts = manifest.get("counts", {})
        if (
            counts.get("youtube_videos_published") != 0
            or counts.get("current_quarto_embeds") != 0
            or counts.get("youtube_videos_unlisted_preview") != count
            or counts.get("current_quarto_preview_embeds") != count
        ):
            failures.append("manifest confuses preview and published-current counts")
    if withdrawn:
        withdrawal = preview.get("withdrawal", {})
        history_path = ROOT / withdrawal.get("historical_record_path", "")
        if not history_path.is_file():
            failures.append("withdrawn preview historical record is missing")
        else:
            try:
                history = load(history_path)
                if len(history.get("entries", [])) < 12:
                    failures.append("withdrawn preview historical denominator drift")
                if history.get("source_binding_sha256_before_withdrawal") != "58aacb7d7e3057deda783bb260c466e8a8f10f31c7169190890c08f810aa1dca":
                    failures.append("withdrawn preview historical source digest drift")
                if history.get("post_withdrawal_visibility") != "private":
                    failures.append("withdrawn preview post-withdrawal privacy is not private")
                history_ids = [row.get("video_id") for row in history.get("entries", [])]
                if sorted(history.get("private_video_ids_observed", [])) != sorted(history_ids):
                    failures.append("withdrawn preview private-video receipt identity drift")
            except (OSError, json.JSONDecodeError):
                failures.append("withdrawn preview historical record is not readable JSON")
    if preview.get("support_state_effect") != "none":
        failures.append("preview projection moves support state")
    expected_release_effect = (
        "preview_withdrawal_only_no_published_current_transition"
        if withdrawn
        else "preview_projection_only_no_published_current_transition"
    )
    if preview.get("release_effect") != expected_release_effect:
        failures.append("preview release effect does not match projection state")
    return failures


def main() -> None:
    preview = load(PREVIEW)
    failures = semantic_errors(preview)
    mutations = [
        ("authority digest drift", lambda value: value.__setitem__("authority_statement_sha256", "0" * 64)),
        ("preview count drift", lambda value: value.__setitem__("preview_entry_count", 1)),
        ("next position drift", lambda value: value.__setitem__("next_upload_position", 13)),
        ("state widening", lambda value: value.__setitem__("state", "owner_authorized_full_public_release")),
        (
            "release effect drift",
            lambda value: value.__setitem__(
                "release_effect",
                (
                    "preview_projection_only_no_published_current_transition"
                    if value.get("state") == "owner_withdrew_partial_unlisted_preview"
                    else "preview_withdrawal_only_no_published_current_transition"
                ),
            ),
        ),
        ("unexpected current entry", lambda value: value["entries"].append({})),
        ("support promotion", lambda value: value.__setitem__("support_state_effect", "promotion")),
    ]
    if preview.get("state") == "owner_withdrew_partial_unlisted_preview":
        mutations.append(("withdrawal deletion", lambda value: value.pop("withdrawal", None)))
    else:
        mutations.append(("unexpected withdrawal", lambda value: value.__setitem__("withdrawal", {})))
    for label, mutate in mutations:
        candidate = copy.deepcopy(preview)
        mutate(candidate)
        if not semantic_errors(
            candidate,
            check_manifest_binding=False,
            check_projection=False,
        ):
            failures.append(f"negative preview mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "YouTube preview validation failed:\n - " + "\n - ".join(failures)
        )
    print(
        "YouTube preview validation passed: "
        f"{preview['preview_entry_count']} exact unlisted chapter bindings, "
        f"{preview['preview_entry_count']} managed preview embeds, 8/8 mutations rejected, "
        "published-current count zero, support effect none."
    )


if __name__ == "__main__":
    main()
