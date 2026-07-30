#!/usr/bin/env python3
"""Validate P7.3 identity, packet completeness, freshness, and binary boundaries."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

from build_youtube_publication_preflight import build as build_expected_youtube_preflight
from build_youtube_ledger import build as build_expected_youtube_ledger
from visual_chapter_source import canonical_chapter_sha256, canonicalize_chapter_source


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "visual_edition/manifest.json"
MANIFEST_SCHEMA = ROOT / "schemas/visual_edition_manifest.schema.json"
PACKET_SCHEMA = ROOT / "schemas/visual_chapter_packet.schema.json"
YOUTUBE_CHANNEL = ROOT / "visual_edition/youtube_channel.json"
YOUTUBE_CHANNEL_SCHEMA = ROOT / "schemas/youtube_channel.schema.json"
YOUTUBE_LEDGER = ROOT / "visual_edition/youtube_ledger.json"
YOUTUBE_LEDGER_SCHEMA = ROOT / "schemas/youtube_ledger.schema.json"
YOUTUBE_UPLOAD_PLAN = ROOT / "visual_edition/youtube_upload_plan.json"
YOUTUBE_UPLOAD_PLAN_SCHEMA = ROOT / "schemas/youtube_upload_plan.schema.json"
YOUTUBE_PREFLIGHT = ROOT / "visual_edition/youtube_publication_preflight.json"
YOUTUBE_PREFLIGHT_SCHEMA = ROOT / "schemas/youtube_publication_preflight.schema.json"
YOUTUBE_PLATFORM_RECEIPT_SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
GRAMMAR = ROOT / "visual_edition/visual_grammar.json"
GRAMMAR_SCHEMA = ROOT / "schemas/visual_grammar.schema.json"
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
NARRATION_TOOLCHAIN = ROOT / "visual_edition/narration_toolchain.json"
NARRATION_TOOLCHAIN_SCHEMA = ROOT / "schemas/narration_toolchain.schema.json"
VIDEO_SUFFIXES = {".mp4", ".webm", ".mov", ".mkv"}
AUDIO_SUFFIXES = {".wav", ".aiff", ".mp3", ".m4a", ".aac", ".flac"}
PILOTS = [
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
]
STALENESS_TRIGGERS = {
    "core_claim",
    "mechanism",
    "worked_trace",
    "evidence_state",
    "non_claim",
    "material_source",
    "chapter_identity",
    "handoff",
    "public_url",
}
GENERATED_ARCHETYPES = {
    "state_machine", "stack", "graph", "ledger", "route", "timeline", "before_after"
}
_LOCAL_PREFLIGHT_CACHE: dict | None = None


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def tags_digest(values: list[str]) -> str:
    return text_digest(
        json.dumps(values, ensure_ascii=False, separators=(",", ":"))
    )


def expected_local_preflight() -> dict:
    global _LOCAL_PREFLIGHT_CACHE
    if _LOCAL_PREFLIGHT_CACHE is None:
        _LOCAL_PREFLIGHT_CACHE = build_expected_youtube_preflight()
    return copy.deepcopy(_LOCAL_PREFLIGHT_CACHE)


def vtt_seconds(timestamp: str) -> float:
    hours, minutes, seconds = timestamp.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def schema_errors(value: dict, schema_path: Path, label: str) -> list[str]:
    schema = load(schema_path)
    return [
        f"{label}:schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(value)
    ]


def errors(manifest: dict, grammar: dict | None = None) -> list[str]:
    failures = schema_errors(manifest, MANIFEST_SCHEMA, "manifest")
    grammar = grammar or load(GRAMMAR)
    failures.extend(schema_errors(grammar, GRAMMAR_SCHEMA, "grammar"))
    channel = load(YOUTUBE_CHANNEL)
    ledger = load(YOUTUBE_LEDGER)
    upload_plan = load(YOUTUBE_UPLOAD_PLAN)
    youtube_preflight = load(YOUTUBE_PREFLIGHT)
    failures.extend(schema_errors(channel, YOUTUBE_CHANNEL_SCHEMA, "youtube-channel"))
    failures.extend(schema_errors(ledger, YOUTUBE_LEDGER_SCHEMA, "youtube-ledger"))
    failures.extend(
        schema_errors(upload_plan, YOUTUBE_UPLOAD_PLAN_SCHEMA, "youtube-upload-plan")
    )
    failures.extend(
        schema_errors(
            youtube_preflight,
            YOUTUBE_PREFLIGHT_SCHEMA,
            "youtube-publication-preflight",
        )
    )
    narration_toolchain = load(NARRATION_TOOLCHAIN)
    failures.extend(
        schema_errors(
            narration_toolchain,
            NARRATION_TOOLCHAIN_SCHEMA,
            "narration-toolchain",
        )
    )
    tracked_narration_inputs = narration_toolchain.get("tracked_inputs", {})
    for path_key, digest_key in (
        ("requirements_lock", "requirements_lock_sha256"),
        ("pronunciation_lexicon", "pronunciation_lexicon_sha256"),
        ("renderer", "renderer_sha256"),
        ("caption_builder", "caption_builder_sha256"),
        ("narration_validator", "narration_validator_sha256"),
        ("visual_master_validator", "visual_master_validator_sha256"),
    ):
        relative = tracked_narration_inputs.get(path_key)
        expected_digest = tracked_narration_inputs.get(digest_key)
        if not relative or not (ROOT / relative).is_file():
            failures.append(f"narration toolchain missing tracked input: {path_key}")
        elif digest(ROOT / relative) != expected_digest:
            failures.append(f"narration toolchain tracked input drift: {path_key}")
    hosting = manifest.get("hosting", {})
    if (
        hosting.get("channel_config_path") != "visual_edition/youtube_channel.json"
        or hosting.get("youtube_ledger_path") != "visual_edition/youtube_ledger.json"
        or hosting.get("channel_id") != channel.get("channel", {}).get("channel_id")
        or hosting.get("playlist_id") != channel.get("canonical_playlist", {}).get("playlist_id")
    ):
        failures.append("manifest/channel/playlist identity drift")
    if ledger.get("book_structure_sha256") != digest(ROOT / "book_structure.json"):
        failures.append("YouTube ledger is stale against book_structure.json")
    if ledger.get("visual_manifest_sha256") != digest(MANIFEST):
        failures.append("YouTube ledger is stale against visual manifest")
    if ledger.get("channel_config_sha256") != digest(YOUTUBE_CHANNEL):
        failures.append("YouTube ledger is stale against channel contract")
    if upload_plan.get("book_structure_sha256") != digest(ROOT / "book_structure.json"):
        failures.append("YouTube upload plan is stale against book_structure.json")
    if upload_plan.get("channel_config_sha256") != digest(YOUTUBE_CHANNEL):
        failures.append("YouTube upload plan is stale against channel contract")
    if upload_plan.get("external_mutation_authorized_now") is not False:
        failures.append("YouTube upload plan claims external mutation authority")
    local_preflight_inputs_present = all(
        (ROOT / entry.get("local_master_path", "")).is_file()
        and (ROOT / entry.get("thumbnail_path", "")).is_file()
        for entry in upload_plan.get("entries", [])
    )
    if local_preflight_inputs_present:
        expected_preflight = expected_local_preflight()
        expected_preflight["generated_at_utc"] = youtube_preflight.get(
            "generated_at_utc"
        )
        if youtube_preflight != expected_preflight:
            failures.append("YouTube publication preflight drift")
    elif (
        youtube_preflight.get("upload_plan_sha256") != digest(YOUTUBE_UPLOAD_PLAN)
        or youtube_preflight.get("entry_count") != 84
        or youtube_preflight.get("ready_entry_count") != 84
        or youtube_preflight.get("external_mutation_authorized_now") is not False
    ):
        failures.append("tracked YouTube publication preflight binding drift")
    preflight_entries = youtube_preflight.get("entries", [])
    if len(preflight_entries) != len(upload_plan.get("entries", [])):
        failures.append("YouTube publication preflight entry count drift")
    for position, (upload_entry, preflight_entry) in enumerate(
        zip(upload_plan.get("entries", []), preflight_entries),
        start=1,
    ):
        caption_path = ROOT / upload_entry.get("caption_path", "")
        exact_preflight = {
            "position": position,
            "chapter_id": upload_entry.get("chapter_id"),
            "master_path": upload_entry.get("local_master_path"),
            "master_sha256": upload_entry.get("local_master_sha256"),
            "caption_path": upload_entry.get("caption_path"),
            "caption_sha256": (
                digest(caption_path) if caption_path.is_file() else None
            ),
            "thumbnail_path": upload_entry.get("thumbnail_path"),
            "thumbnail_sha256": upload_entry.get("thumbnail_sha256"),
            "ready": True,
        }
        for key, expected in exact_preflight.items():
            if preflight_entry.get(key) != expected:
                failures.append(
                    f"{upload_entry.get('chapter_id', position)}: "
                    f"YouTube publication preflight {key} drift"
                )
    expected_ledger = build_expected_youtube_ledger()
    expected_ledger["generated_at_utc"] = ledger.get("generated_at_utc")
    if ledger != expected_ledger:
        failures.append("YouTube ledger entries or derived counts drift")
    toolchain = load(TOOLCHAIN)
    structure = load(ROOT / "book_structure.json")
    canonical = [
        (part_index, part, chapter_index, chapter)
        for part_index, part in enumerate(structure["parts"], start=1)
        for chapter_index, chapter in enumerate(part["chapters"], start=1)
    ]
    binding_probe_path = ROOT / canonical[0][3]["file"]
    binding_probe_source = binding_probe_path.read_text(encoding="utf-8")
    front_matter_close = binding_probe_source.find("\n---\n", 4)
    if front_matter_close < 0:
        failures.append("visual chapter-binding probe lacks closed front matter")
    else:
        insertion_point = front_matter_close + len("\n---\n")
        binding_probe_projected = (
            binding_probe_source[:insertion_point]
            + "\n<!-- BEGIN MANAGED VISUAL ABSTRACT:asi-is-a-stack-not-a-model -->\n"
            + "projection-only probe\n"
            + "<!-- END MANAGED VISUAL ABSTRACT:asi-is-a-stack-not-a-model -->\n"
            + binding_probe_source[insertion_point:].lstrip("\n")
        )
        if canonicalize_chapter_source(binding_probe_projected) != binding_probe_source:
            failures.append("managed visual projection changes canonical chapter binding")
        changed_probe = binding_probe_source.replace(
            "## Chapter status",
            "## Changed chapter status",
            1,
        )
        if hashlib.sha256(
            canonicalize_chapter_source(changed_probe).encode("utf-8")
        ).hexdigest() == canonical_chapter_sha256(binding_probe_path):
            failures.append("manuscript change does not change canonical chapter binding")
    rows = manifest.get("chapters", [])
    upload_entries = upload_plan.get("entries", [])
    if len(canonical) != 84 or len(rows) != 84:
        failures.append(f"canonical/manifest count mismatch: {len(canonical)}/{len(rows)}")
        return failures
    if manifest.get("pilot_chapter_ids") != PILOTS:
        failures.append("five-pilot identity or order drift")
    if len(upload_entries) != len(canonical):
        failures.append("YouTube upload-plan chapter count drift")

    lifecycle_counts = {state: 0 for state in (
        "planned", "storyboarded", "scripted", "rendered", "validated",
        "ready_not_published", "published_current", "stale", "superseded",
    )}
    packet_count = rendered_count = youtube_count = embed_count = 0
    packets = []
    published_authority_digests = set()
    published_video_ids = set()
    published_playlist_ids = set()
    published_playlist_item_ids = set()
    published_playlist_positions = set()
    for manifest_position, (expected, row, upload_entry) in enumerate(
        zip(canonical, rows, upload_entries),
        start=1,
    ):
        preflight_entry = (
            preflight_entries[manifest_position - 1]
            if manifest_position <= len(preflight_entries)
            else {}
        )
        part_index, part, chapter_index, chapter = expected
        path = ROOT / chapter["file"]
        exact = {
            "chapter_id": chapter["id"],
            "title": chapter["title"],
            "chapter_path": chapter["file"],
            "chapter_sha256": canonical_chapter_sha256(path),
            "part_id": part["id"],
            "part_index": part_index,
            "chapter_index": chapter_index,
            "pilot": chapter["id"] in PILOTS,
        }
        for key, value in exact.items():
            if row.get(key) != value:
                failures.append(f"{chapter['id']}: manifest {key} drift")
        if upload_entry.get("position") != manifest_position:
            failures.append(f"{chapter['id']}: YouTube upload-plan order drift")
        if upload_entry.get("chapter_id") != chapter["id"]:
            failures.append(f"{chapter['id']}: YouTube upload-plan identity drift")
        if upload_entry.get("desired_playlist_position") != upload_entry.get("position"):
            failures.append(f"{chapter['id']}: YouTube upload-plan playlist order drift")
        state = row.get("lifecycle_state")
        if state in lifecycle_counts:
            lifecycle_counts[state] += 1
        packet_rel = row.get("packet_path")
        if packet_rel is None:
            if state != "planned":
                failures.append(f"{chapter['id']}: absent packet must remain planned")
            continue
        packet_path = ROOT / packet_rel
        if not packet_path.exists():
            failures.append(f"{chapter['id']}: packet path missing")
            continue
        packet_count += 1
        packet = load(packet_path)
        packets.append(packet)
        failures.extend(schema_errors(packet, PACKET_SCHEMA, chapter["id"]))
        if upload_entry.get("stable_internal_video_id") != packet.get("video_id"):
            failures.append(f"{chapter['id']}: upload-plan stable video identity drift")
        if (
            upload_entry.get("thumbnail_source_path")
            != packet.get("artifacts", {}).get("thumbnail")
        ):
            failures.append(f"{chapter['id']}: upload-plan thumbnail-source drift")
        thumbnail_source = ROOT / packet.get("artifacts", {}).get("thumbnail", "")
        if (
            not thumbnail_source.is_file()
            or upload_entry.get("thumbnail_source_sha256")
            != digest(thumbnail_source)
        ):
            failures.append(f"{chapter['id']}: upload-plan thumbnail-source digest drift")
        expected_thumbnail = f"build/visual_edition/thumbnails/{chapter['id']}.png"
        if upload_entry.get("thumbnail_path") != expected_thumbnail:
            failures.append(f"{chapter['id']}: upload-plan thumbnail path drift")
        local_thumbnail = ROOT / expected_thumbnail
        if (
            local_thumbnail.is_file()
            and upload_entry.get("thumbnail_sha256") != digest(local_thumbnail)
        ):
            failures.append(f"{chapter['id']}: upload-plan thumbnail digest drift")
        if upload_entry.get("caption_path") != packet.get("artifacts", {}).get("captions"):
            failures.append(f"{chapter['id']}: upload-plan caption path drift")
        description = upload_entry.get("description", "")
        if (
            packet.get("chapter_sha256") not in description
            or packet.get("source_commit") not in description
            or "Narration is synthetic" not in description
        ):
            failures.append(f"{chapter['id']}: upload-plan description binding drift")
        if packet.get("chapter_id") != chapter["id"]:
            failures.append(f"{chapter['id']}: packet identity mismatch")
        if packet.get("chapter_path") != chapter["file"]:
            failures.append(f"{chapter['id']}: packet path mismatch")
        if packet.get("chapter_sha256") != canonical_chapter_sha256(path):
            failures.append(f"{chapter['id']}: packet is stale against chapter bytes")
        if packet.get("lifecycle_state") != state:
            failures.append(f"{chapter['id']}: packet/manifest lifecycle mismatch")
        if set(packet.get("assigned_source_ids", [])) != set(chapter.get("source_ids", [])):
            failures.append(f"{chapter['id']}: assigned source IDs drift")
        core_bindings = [
            binding for binding in packet.get("claim_bindings", [])
            if binding.get("claim_id") == f"{chapter['id']}.core"
        ]
        if core_bindings != [{
            "claim_id": f"{chapter['id']}.core",
            "claim_label": chapter.get("claim_label"),
            "support_state": chapter.get("evidence_level"),
        }]:
            failures.append(f"{chapter['id']}: exact core claim binding drift")
        if set(packet.get("staleness", {}).get("triggers", [])) != STALENESS_TRIGGERS:
            failures.append(f"{chapter['id']}: staleness trigger contract drift")
        if not packet.get("pilot"):
            directory = packet_path.parent
            scene_spec_path = directory / "scene_spec.json"
            if not scene_spec_path.is_file():
                failures.append(f"{chapter['id']}: generated scene specification missing")
            else:
                scene_spec = load(scene_spec_path)
                if scene_spec.get("chapter_id") != chapter["id"]:
                    failures.append(f"{chapter['id']}: scene specification identity drift")
                if scene_spec.get("archetype") not in GENERATED_ARCHETYPES:
                    failures.append(f"{chapter['id']}: unknown generated visual archetype")
                display = scene_spec.get("display", {})
                for key, count in (
                    ("mechanism", 4),
                    ("trace", 4),
                    ("failures", 4),
                    ("proof_targets", 3),
                    ("nonclaims", 4),
                ):
                    if len(display.get(key, [])) != count:
                        failures.append(
                            f"{chapter['id']}: scene specification {key} count drift"
                        )
                timing = scene_spec.get("timing")
                if timing:
                    endpoints = timing.get("scene_endpoints_seconds", [])
                    target = timing.get("target_duration_seconds")
                    if timing.get("basis") != "exact_narration_paragraph_boundaries":
                        failures.append(f"{chapter['id']}: scene timing basis drift")
                    if (
                        len(endpoints) != 7
                        or any(
                            not isinstance(value, (int, float)) or value <= 0
                            for value in endpoints
                        )
                        or any(a >= b for a, b in zip(endpoints, endpoints[1:]))
                    ):
                        failures.append(f"{chapter['id']}: invalid scene timing endpoints")
                    elif (
                        not isinstance(target, (int, float))
                        or not 180 <= target <= 360
                        or abs(endpoints[-1] - target) > 0.25
                    ):
                        failures.append(f"{chapter['id']}: scene/audio duration binding drift")
                    if not re.fullmatch(
                        r"[0-9a-f]{64}",
                        timing.get("narration_receipt_sha256", ""),
                    ):
                        failures.append(f"{chapter['id']}: narration timing receipt digest missing")
                elif state in {"validated", "ready_not_published", "published_current"}:
                    failures.append(f"{chapter['id']}: validated render lacks exact scene timing")
            narration_path = directory / "narration.txt"
            if narration_path.is_file():
                narration_text = narration_path.read_text(encoding="utf-8").strip()
                paragraphs = [
                    item for item in re.split(r"\n\s*\n", narration_text) if item.strip()
                ]
                narration_words = re.findall(r"\b[\w’'-]+\b", narration_text)
                if len(paragraphs) != 7:
                    failures.append(f"{chapter['id']}: narration must contain seven semantic paragraphs")
                if not 400 <= len(narration_words) <= 700:
                    failures.append(
                        f"{chapter['id']}: narration word count outside governed source range"
                    )
                stop_words = {
                    "a", "an", "and", "as", "at", "before", "by", "for", "from",
                    "in", "into", "of", "on", "or", "the", "that", "to", "under",
                    "which", "while", "with", "without",
                }
                for paragraph in paragraphs:
                    final_word = paragraph.rstrip(".!?").split()[-1].lower().strip(",:;")
                    if final_word in stop_words:
                        failures.append(
                            f"{chapter['id']}: narration ends a paragraph mid-clause"
                        )
        for artifact_name, relative in packet.get("artifacts", {}).items():
            if artifact_name == "thumbnail_alt_text":
                continue
            artifact_path = ROOT / relative
            if not artifact_path.exists():
                failures.append(f"{chapter['id']}: missing {artifact_name}: {relative}")
        receipt = packet.get("render_receipt")
        if receipt:
            if receipt.get("toolchain_id") != toolchain.get("toolchain_id"):
                failures.append(f"{chapter['id']}: render/toolchain identity drift")
            artifact_keys = {
                "storyboard": "storyboard",
                "scene_code": "scene_code",
                "narration_script": "narration_script",
                "captions": "captions",
                "descriptive_transcript": "descriptive_transcript",
                "thumbnail": "thumbnail",
                "scene_spec": "scene_spec",
            }
            recorded_hashes = receipt.get("artifact_sha256", {})
            for hash_key, artifact_key in artifact_keys.items():
                relative = packet.get("artifacts", {}).get(artifact_key)
                if relative and (ROOT / relative).exists():
                    if recorded_hashes.get(hash_key) != digest(ROOT / relative):
                        failures.append(f"{chapter['id']}: {artifact_key} receipt digest drift")
            captions = ROOT / packet.get("artifacts", {}).get("captions", "")
            if captions.is_file():
                timestamps = re.findall(
                    r"-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})",
                    captions.read_text(encoding="utf-8"),
                )
                if not timestamps:
                    failures.append(f"{chapter['id']}: caption timing is absent")
                elif abs(vtt_seconds(timestamps[-1]) - receipt.get("duration_seconds", 0)) > 2:
                    failures.append(f"{chapter['id']}: caption track does not span the render")
            if receipt.get("validation_state") == "validated":
                rendered_count += 1
                if not (180 <= receipt.get("duration_seconds", 0) <= 360):
                    failures.append(f"{chapter['id']}: validated duration outside 180-360 seconds")
                if receipt.get("output_sha256") in (None, "", "0" * 64):
                    failures.append(f"{chapter['id']}: validated render lacks digest")
                if upload_entry.get("local_master_sha256") != receipt.get("output_sha256"):
                    failures.append(f"{chapter['id']}: upload-plan local master digest drift")
            elif upload_entry.get("local_master_sha256") is not None:
                failures.append(f"{chapter['id']}: upload-plan digest without validated master")
        elif upload_entry.get("local_master_sha256") is not None:
            failures.append(f"{chapter['id']}: upload-plan digest without render receipt")
        publication = packet.get("youtube", {}).get("publication_state")
        embed = packet.get("quarto_embed", {}).get("state")
        youtube = packet.get("youtube", {})
        if youtube.get("channel_id") != channel["channel"]["channel_id"]:
            failures.append(f"{chapter['id']}: YouTube channel identity drift")
        if publication == "published_current":
            youtube_count += 1
            if receipt and receipt.get("remaining_release_gates"):
                failures.append(
                    f"{chapter['id']}: published video retains release gates"
                )
            if not youtube.get("video_id") or not youtube.get("playlist_id") or not youtube.get("platform_receipt_path"):
                failures.append(f"{chapter['id']}: published YouTube identity incomplete")
            if youtube.get("watch_url") != f"https://www.youtube.com/watch?v={youtube.get('video_id')}":
                failures.append(f"{chapter['id']}: published YouTube watch URL drift")
            if not receipt:
                failures.append(f"{chapter['id']}: published video lacks render receipt")
            elif youtube.get("uploaded_output_sha256") != receipt.get("output_sha256"):
                failures.append(f"{chapter['id']}: uploaded binary digest/render receipt drift")
            if youtube.get("bound_chapter_sha256") != packet.get("chapter_sha256"):
                failures.append(f"{chapter['id']}: published chapter digest binding drift")
            if youtube.get("bound_source_commit") != packet.get("source_commit"):
                failures.append(f"{chapter['id']}: published source commit binding drift")
            receipt_path = ROOT / youtube.get("platform_receipt_path", "")
            if not receipt_path.is_file():
                failures.append(f"{chapter['id']}: YouTube platform receipt missing")
            else:
                platform_receipt = load(receipt_path)
                failures.extend(
                    schema_errors(
                        platform_receipt,
                        YOUTUBE_PLATFORM_RECEIPT_SCHEMA,
                        f"{chapter['id']}:youtube-platform-receipt",
                    )
                )
                receipt_exact = {
                    "chapter_id": chapter["id"],
                    "stable_internal_video_id": packet.get("video_id"),
                    "channel_id": youtube.get("channel_id"),
                    "video_id": youtube.get("video_id"),
                    "watch_url": youtube.get("watch_url"),
                    "playlist_id": youtube.get("playlist_id"),
                    "playlist_position": manifest_position,
                    "generation": youtube.get("generation"),
                }
                for key, expected in receipt_exact.items():
                    if platform_receipt.get(key) != expected:
                        failures.append(
                            f"{chapter['id']}: platform receipt {key} drift"
                        )
                published_authority_digests.add(
                    platform_receipt.get("authorization_scope_sha256")
                )
                video_id = platform_receipt.get("video_id")
                playlist_id = platform_receipt.get("playlist_id")
                playlist_item_id = platform_receipt.get("playlist_item_id")
                playlist_position = platform_receipt.get("playlist_position")
                if video_id in published_video_ids:
                    failures.append(
                        f"{chapter['id']}: duplicate published YouTube video ID"
                    )
                if playlist_item_id in published_playlist_item_ids:
                    failures.append(
                        f"{chapter['id']}: duplicate published playlist item ID"
                    )
                if playlist_position in published_playlist_positions:
                    failures.append(
                        f"{chapter['id']}: duplicate published playlist position"
                    )
                published_video_ids.add(video_id)
                published_playlist_ids.add(playlist_id)
                published_playlist_item_ids.add(playlist_item_id)
                published_playlist_positions.add(playlist_position)
                source_upload = platform_receipt.get("source_upload", {})
                if (
                    source_upload.get("local_master_path")
                    != upload_entry.get("local_master_path")
                    or source_upload.get("local_master_sha256")
                    != upload_entry.get("local_master_sha256")
                    or source_upload.get("local_master_bytes")
                    != preflight_entry.get("master_bytes")
                    or source_upload.get("local_master_sha256")
                    != receipt.get("output_sha256")
                    or source_upload.get("bound_chapter_sha256")
                    != packet.get("chapter_sha256")
                    or source_upload.get("bound_source_commit")
                    != packet.get("source_commit")
                ):
                    failures.append(
                        f"{chapter['id']}: platform receipt source binding drift"
                    )
                expected_metadata = {
                    "title_sha256": text_digest(upload_entry.get("title", "")),
                    "description_sha256": text_digest(
                        upload_entry.get("description", "")
                    ),
                    "tags_sha256": tags_digest(upload_entry.get("tags", [])),
                    "category_id": upload_entry.get("category_id"),
                    "made_for_kids": upload_entry.get("made_for_kids"),
                    "synthetic_narration_disclosed": upload_entry.get(
                        "contains_synthetic_narration_disclosure"
                    ),
                    "state": "exact",
                }
                metadata = platform_receipt.get("metadata", {})
                for key, expected in expected_metadata.items():
                    if metadata.get(key) != expected:
                        failures.append(
                            f"{chapter['id']}: platform receipt metadata {key} drift"
                        )
                caption_path = ROOT / upload_entry.get("caption_path", "")
                thumbnail_path = ROOT / upload_entry.get("thumbnail_path", "")
                expected_accessibility = {
                    "caption_path": upload_entry.get("caption_path"),
                    "caption_sha256": (
                        digest(caption_path) if caption_path.is_file() else None
                    ),
                    "caption_language": "en",
                    "caption_state": "published",
                    "thumbnail_path": upload_entry.get("thumbnail_path"),
                    "thumbnail_sha256": upload_entry.get("thumbnail_sha256"),
                    "thumbnail_state": "applied",
                }
                accessibility = platform_receipt.get("accessibility", {})
                for key, expected in expected_accessibility.items():
                    if accessibility.get(key) != expected:
                        failures.append(
                            f"{chapter['id']}: platform receipt accessibility "
                            f"{key} drift"
                        )
                if (
                    thumbnail_path.is_file()
                    and accessibility.get("thumbnail_sha256")
                    != digest(thumbnail_path)
                ):
                    failures.append(
                        f"{chapter['id']}: published thumbnail bytes drift"
                    )
            if embed != "published_current":
                failures.append(f"{chapter['id']}: published video lacks current Quarto embed")
        if embed == "published_current":
            embed_count += 1
            if publication != "published_current":
                failures.append(f"{chapter['id']}: current embed without current YouTube publication")
        if state == "published_current" and publication != "published_current":
            failures.append(f"{chapter['id']}: lifecycle publication mismatch")

    if youtube_count:
        if youtube_count != 84:
            failures.append(
                "published visual edition must reconcile as zero or all 84 videos"
            )
        if len(published_authority_digests) != 1:
            failures.append(
                "published videos do not share one exact authorization scope"
            )
        if len(published_playlist_ids) != 1:
            failures.append(
                "published videos do not share one canonical playlist"
            )
        if published_playlist_positions != set(range(1, youtube_count + 1)):
            failures.append(
                "published playlist positions are not a complete ordered prefix"
            )

    counts = manifest.get("counts", {})
    for state, count in lifecycle_counts.items():
        if counts.get(state) != count:
            failures.append(f"manifest count drift: {state}")
    exact_counts = {
        "packets_present": packet_count,
        "current_rendered_videos": rendered_count,
        "youtube_videos_published": youtube_count,
        "current_quarto_embeds": embed_count,
    }
    for key, count in exact_counts.items():
        if counts.get(key) != count:
            failures.append(f"manifest count drift: {key}")

    validated_pilots = {
        packet["chapter_id"]
        for packet in packets
        if packet.get("pilot") and packet.get("lifecycle_state") in {
            "validated", "ready_not_published", "published_current"
        }
    }
    all_pilots_validated = validated_pilots == set(PILOTS)
    grammar_ratified = (
        grammar.get("state") == "ratified"
        and grammar.get("ratification_gate", {}).get("current_state") == "ratified"
    )
    if grammar_ratified and not all_pilots_validated:
        failures.append("visual grammar ratified before all five pilots validated")
    if all_pilots_validated and not grammar_ratified:
        failures.append("visual grammar remained candidate after all five pilots validated")

    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    forbidden_tracked = [
        path for path in tracked
        if Path(path).suffix.lower() in VIDEO_SUFFIXES | AUDIO_SUFFIXES
        and not path.startswith("archive/")
    ]
    if forbidden_tracked:
        failures.append(f"tracked visual-edition media binary: {forbidden_tracked[:5]}")
    site = ROOT / "_site"
    if site.exists():
        forbidden_site = [
            str(path.relative_to(ROOT))
            for path in site.rglob("*")
            if path.is_file() and path.suffix.lower() in VIDEO_SUFFIXES | AUDIO_SUFFIXES
        ]
        if forbidden_site:
            failures.append(f"Pages artifact contains media binary: {forbidden_site[:5]}")
    if manifest.get("support_state_effect") != "none" or load(TOOLCHAIN).get("support_state_effect") != "none":
        failures.append("visual derivative moved support state")
    return failures


def main() -> None:
    manifest = load(MANIFEST)
    grammar = load(GRAMMAR)
    failures = errors(manifest, grammar)
    mutations = []
    grammar_mutation_label = (
        "post-gate grammar deratification"
        if grammar.get("state") == "ratified"
        else "premature grammar ratification"
    )
    grammar_mutation = (
        (lambda d: d.__setitem__("state", "candidate_until_five_pilots_pass"))
        if grammar.get("state") == "ratified"
        else (lambda d: d.__setitem__("state", "ratified"))
    )
    for label, target, edit in (
        ("chapter deletion", "manifest", lambda d: d["chapters"].pop()),
        ("pilot substitution", "manifest", lambda d: d["pilot_chapter_ids"].__setitem__(0, "wrong")),
        ("binary host widening", "manifest", lambda d: d["hosting"].__setitem__("canonical_binary_host", "GitHub Pages")),
        ("premature authority", "manifest", lambda d: d["hosting"].__setitem__("external_publication_authorized_now", True)),
        ("support promotion", "manifest", lambda d: d.__setitem__("support_state_effect", "promotion")),
        (grammar_mutation_label, "grammar", grammar_mutation),
        ("motion-only meaning", "grammar", lambda d: d["motion"].__setitem__("meaning_must_survive_motion_disabled", False)),
        ("caption deletion", "grammar", lambda d: d["accessibility"].__setitem__("reviewed_captions_required", False)),
    ):
        manifest_candidate = copy.deepcopy(manifest)
        grammar_candidate = copy.deepcopy(grammar)
        edit(manifest_candidate if target == "manifest" else grammar_candidate)
        mutations.append((label, manifest_candidate, grammar_candidate))
    for label, manifest_candidate, grammar_candidate in mutations:
        if not errors(manifest_candidate, grammar_candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Visual-edition validation failed:\n - " + "\n - ".join(failures))
    counts = manifest["counts"]
    print(
        "Visual-edition validation passed: "
        f"84 chapters, {counts['packets_present']} packet(s), "
        f"{counts['current_rendered_videos']} validated render(s), "
        f"{counts['youtube_videos_published']} YouTube publication(s), "
        "zero tracked/Pages media binaries, 8/8 mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
