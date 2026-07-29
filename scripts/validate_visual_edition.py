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


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "visual_edition/manifest.json"
MANIFEST_SCHEMA = ROOT / "schemas/visual_edition_manifest.schema.json"
PACKET_SCHEMA = ROOT / "schemas/visual_chapter_packet.schema.json"
GRAMMAR = ROOT / "visual_edition/visual_grammar.json"
GRAMMAR_SCHEMA = ROOT / "schemas/visual_grammar.schema.json"
TOOLCHAIN = ROOT / "visual_edition/toolchain.json"
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


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    toolchain = load(TOOLCHAIN)
    structure = load(ROOT / "book_structure.json")
    canonical = [
        (part_index, part, chapter_index, chapter)
        for part_index, part in enumerate(structure["parts"], start=1)
        for chapter_index, chapter in enumerate(part["chapters"], start=1)
    ]
    rows = manifest.get("chapters", [])
    if len(canonical) != 84 or len(rows) != 84:
        failures.append(f"canonical/manifest count mismatch: {len(canonical)}/{len(rows)}")
        return failures
    if manifest.get("pilot_chapter_ids") != PILOTS:
        failures.append("five-pilot identity or order drift")

    lifecycle_counts = {state: 0 for state in (
        "planned", "storyboarded", "scripted", "rendered", "validated",
        "ready_not_published", "published_current", "stale", "superseded",
    )}
    packet_count = rendered_count = youtube_count = embed_count = 0
    packets = []
    for expected, row in zip(canonical, rows):
        part_index, part, chapter_index, chapter = expected
        path = ROOT / chapter["file"]
        exact = {
            "chapter_id": chapter["id"],
            "title": chapter["title"],
            "chapter_path": chapter["file"],
            "chapter_sha256": digest(path),
            "part_id": part["id"],
            "part_index": part_index,
            "chapter_index": chapter_index,
            "pilot": chapter["id"] in PILOTS,
        }
        for key, value in exact.items():
            if row.get(key) != value:
                failures.append(f"{chapter['id']}: manifest {key} drift")
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
        if packet.get("chapter_id") != chapter["id"]:
            failures.append(f"{chapter['id']}: packet identity mismatch")
        if packet.get("chapter_path") != chapter["file"]:
            failures.append(f"{chapter['id']}: packet path mismatch")
        if packet.get("chapter_sha256") != digest(path):
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
        publication = packet.get("youtube", {}).get("publication_state")
        embed = packet.get("quarto_embed", {}).get("state")
        if publication == "published_current":
            youtube_count += 1
            youtube = packet["youtube"]
            if not youtube.get("video_id") or not youtube.get("playlist_id") or not youtube.get("platform_receipt_path"):
                failures.append(f"{chapter['id']}: published YouTube identity incomplete")
            if embed != "published_current":
                failures.append(f"{chapter['id']}: published video lacks current Quarto embed")
        if embed == "published_current":
            embed_count += 1
            if publication != "published_current":
                failures.append(f"{chapter['id']}: current embed without current YouTube publication")
        if state == "published_current" and publication != "published_current":
            failures.append(f"{chapter['id']}: lifecycle publication mismatch")

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
    if grammar.get("state") == "ratified" and validated_pilots != set(PILOTS):
        failures.append("visual grammar ratified before all five pilots validated")

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
    for label, target, edit in (
        ("chapter deletion", "manifest", lambda d: d["chapters"].pop()),
        ("pilot substitution", "manifest", lambda d: d["pilot_chapter_ids"].__setitem__(0, "wrong")),
        ("binary host widening", "manifest", lambda d: d["hosting"].__setitem__("canonical_binary_host", "GitHub Pages")),
        ("premature authority", "manifest", lambda d: d["hosting"].__setitem__("external_publication_authorized_now", True)),
        ("support promotion", "manifest", lambda d: d.__setitem__("support_state_effect", "promotion")),
        ("premature grammar ratification", "grammar", lambda d: d.__setitem__("state", "ratified")),
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
