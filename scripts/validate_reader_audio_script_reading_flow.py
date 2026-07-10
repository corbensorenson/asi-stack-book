#!/usr/bin/env python3
"""Validate generated audio-script reading flow without approving audio release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import build_audio_script


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build" / "audio_script"
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
STRUCTURE = ROOT / "book_structure.json"
REPORT = BUILD_DIR / "audio_script_reading_flow_report.json"
COMMAND = "python3 scripts/validate_reader_audio_script_reading_flow.py --write-manifest"
EXPECTED_APPENDIX_SCRIPT_FILES = (
    "appendices/B_glossary.md",
    "appendices/G_corben_source_corpus.md",
    "appendices/H_external_sources.md",
)
EXPECTED_TARGET_STATUS = {
    "mp3": "target_not_generated",
    "m4b": "target_not_generated",
    "audio-embedded-epub": "target_not_generated",
}
LIVE_ONLY_MARKERS = (
    "Chapter status",
    "Drafting guardrail",
    "Codex test plan",
    "Source crosswalk",
    "Claim-source mapping status",
    "Formalization hooks",
)
RAW_CORE_CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader audio-script reading-flow review failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_script_files() -> list[str]:
    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    expected: list[str] = []
    for item in structure.get("front_matter", []):
        if isinstance(item, str):
            expected.append(str(Path(item).with_suffix(".md")))
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("file"), str):
                expected.append(str(Path(chapter["file"]).with_suffix(".md")))
    expected.extend(EXPECTED_APPENDIX_SCRIPT_FILES)
    return expected


def hash_joined_text(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.read_bytes())
        digest.update(b"\n--ASI-AUDIO-SCRIPT-FILE--\n")
    return digest.hexdigest()


def marker_rows(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    pattern = re.compile(r"^\| (?P<index>\d+) \| `(?P<file>[^`]+)` \| (?P<time>[^|]+) \|")
    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        rows.append((int(match.group("index")), match.group("file")))
    return rows


def generate_observation() -> dict[str, Any]:
    generated = build_audio_script.generate(BUILD_DIR, "generated_reader_edition")
    if not isinstance(generated, dict):
        fail(["build_audio_script.generate must return an object."])
    script_files = generated.get("script_files")
    if not isinstance(script_files, list) or not all(isinstance(item, str) for item in script_files):
        fail(["generated audio manifest must contain a string script_files list."])

    expected_files = expected_script_files()
    paths = [BUILD_DIR / script_file for script_file in script_files]
    missing_paths = [script_file for script_file, path in zip(script_files, paths) if not path.exists()]
    if missing_paths:
        fail([f"generated audio workspace missing script files: {missing_paths}"])

    script_texts = [path.read_text(encoding="utf-8", errors="ignore") for path in paths]
    combined_text = "\n".join(script_texts)
    chapter_files = [item for item in script_files if item.startswith("chapters/")]
    chapter_texts = [
        (BUILD_DIR / script_file).read_text(encoding="utf-8", errors="ignore")
        for script_file in chapter_files
    ]
    marker_text = (BUILD_DIR / "chapter_markers.md").read_text(encoding="utf-8", errors="ignore")
    markers = marker_rows(marker_text)
    marker_files = [script_file for _, script_file in markers]
    marker_indices = [index for index, _ in markers]
    words = re.findall(r"\S+", combined_text)
    companion_summary = generated.get("companion_treatment_summary", {})
    treatment_totals = {
        key: sum(
            int(value.get(key, 0))
            for value in companion_summary.values()
            if isinstance(value, dict)
        )
        for key in ("tables", "mermaid_diagrams", "code_or_schema_blocks", "images")
    }
    live_marker_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in combined_text]
    target_status = generated.get("target_artifact_status", {})

    return {
        "status": "passed_audio_script_reading_flow_review",
        "source_workspace": rel(BUILD_DIR),
        "source_generator": "scripts/build_audio_script.py",
        "source_mode": generated.get("source_mode"),
        "requested_source_mode": generated.get("requested_source_mode"),
        "report_ref": rel(REPORT),
        "review_command": COMMAND,
        "script_files_checked": len(script_files),
        "front_matter_scripts_checked": sum(1 for item in script_files if item in {"index.md", "preface.md"}),
        "chapter_scripts_checked": len(chapter_files),
        "appendix_scripts_checked": sum(1 for item in script_files if item.startswith("appendices/")),
        "script_file_order_status": "matches_book_structure",
        "script_file_order_errors": [] if script_files == expected_files else ["script_files do not match book_structure order"],
        "ordered_script_file_samples": {
            "first_five": script_files[:5],
            "last_five": script_files[-5:],
        },
        "combined_script_sha256": hash_joined_text(paths),
        "text_characters_checked": len(combined_text),
        "word_tokens_checked": len(words),
        "release_note_count": combined_text.count("Release note: This is a generated narration-script candidate."),
        "review_frontmatter_count": combined_text.count("audio_script_status: review_required"),
        "narration_note_count": combined_text.count("Narration note:"),
        "table_narration_notes": combined_text.count("Table retained in companion text"),
        "diagram_narration_notes": combined_text.count("Diagram retained in companion text"),
        "image_narration_notes": combined_text.count("Image retained in companion text"),
        "code_schema_narration_notes": combined_text.count("Code or schema block retained in companion text"),
        "companion_treatment_totals": treatment_totals,
        "chapter_marker_rows": len(markers),
        "chapter_marker_order_status": "matches_script_file_order",
        "chapter_marker_order_errors": [] if marker_files == script_files and marker_indices == list(range(1, len(script_files) + 1)) else ["chapter markers do not match script file order"],
        "chapter_marker_tbd_rows": marker_text.count("| TBD | Verify after audio render. |"),
        "implementation_horizon_chapter_scripts": sum(
            1
            for text in chapter_texts
            if "## Minimum Viable Implementation" in text
            and "## Beyond the State of the Art" in text
        ),
        "chapter_scripts_with_evidence_boundary_phrase": sum(
            1 for text in chapter_texts if "evidence boundary" in text.lower()
        ),
        "live_marker_hits": len(live_marker_hits),
        "raw_core_claim_marker_hits": int(bool(RAW_CORE_CLAIM_RE.search(combined_text))),
        "replacement_character_count": combined_text.count("\ufffd"),
        "max_line_characters": max(len(line) for line in combined_text.splitlines()),
        "max_word_characters": max(len(word) for word in words),
        "target_artifact_status": target_status,
        "review_boundary": (
            "This audio-script reading-flow review checks generated script order, chapter-marker order, "
            "implementation-horizon survival, narration-note coverage, stripped live markers, and audio target absence. "
            "It is not narration quality review, not pronunciation review, not chapter timecoding, not an audiobook, "
            "not audio generation, and not release approval."
        ),
        "non_claims": [
            "does not approve narration quality",
            "does not approve pronunciation quality",
            "does not create MP3, M4B, or audio-embedded EPUB artifacts",
            "does not timecode chapter markers",
            "does not approve an audiobook or audio release",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_files = expected_script_files()
    expected_chapter_scripts = sum(1 for item in expected_files if item.startswith("chapters/"))
    expected_front_matter_scripts = sum(1 for item in expected_files if item in {"index.md", "preface.md"})
    expected_exact = {
        "status": "passed_audio_script_reading_flow_review",
        "source_workspace": "build/audio_script",
        "source_generator": "scripts/build_audio_script.py",
        "source_mode": "generated_reader_edition",
        "requested_source_mode": "generated_reader_edition",
        "script_files_checked": len(expected_files),
        "front_matter_scripts_checked": expected_front_matter_scripts,
        "chapter_scripts_checked": expected_chapter_scripts,
        "appendix_scripts_checked": len(EXPECTED_APPENDIX_SCRIPT_FILES),
        "script_file_order_status": "matches_book_structure",
        "script_file_order_errors": [],
        "release_note_count": len(expected_files),
        "review_frontmatter_count": len(expected_files),
        "chapter_marker_rows": len(expected_files),
        "chapter_marker_order_status": "matches_script_file_order",
        "chapter_marker_order_errors": [],
        "chapter_marker_tbd_rows": len(expected_files),
        "implementation_horizon_chapter_scripts": expected_chapter_scripts,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
        "replacement_character_count": 0,
        "target_artifact_status": EXPECTED_TARGET_STATUS,
    }
    for key, expected in expected_exact.items():
        if observed.get(key) != expected:
            errors.append(f"audio script reading-flow expected {key}={expected!r}, found {observed.get(key)!r}.")
    treatment_counts = {
        "tables": "table_narration_notes",
        "mermaid_diagrams": "diagram_narration_notes",
        "code_or_schema_blocks": "code_schema_narration_notes",
        "images": "image_narration_notes",
    }
    for total_key, note_key in treatment_counts.items():
        total = observed.get("companion_treatment_totals", {}).get(total_key) if isinstance(observed.get("companion_treatment_totals"), dict) else None
        notes = observed.get(note_key)
        if not isinstance(total, int) or total < 0:
            errors.append(f"audio script reading-flow {total_key} treatment total must be a non-negative integer.")
        if not isinstance(notes, int) or notes < 0:
            errors.append(f"audio script reading-flow {note_key} must be a non-negative integer.")
        elif total != notes:
            errors.append(f"audio script reading-flow {total_key} total must match {note_key}.")
    narration_notes = observed.get("narration_note_count")
    if not isinstance(narration_notes, int) or narration_notes < 0:
        errors.append("audio script reading-flow narration_note_count must be a non-negative integer.")
    elif isinstance(observed.get("companion_treatment_totals"), dict) and narration_notes != sum(
        int(observed["companion_treatment_totals"].get(key, 0)) for key in treatment_counts
    ):
        errors.append("audio script reading-flow narration_note_count must equal the treatment total.")
    for key, maximum in (("max_line_characters", 1800), ("max_word_characters", 143)):
        value = observed.get(key)
        if not isinstance(value, int) or value < 1 or value > maximum:
            errors.append(f"audio script reading-flow {key} must be between 1 and {maximum}.")
    evidence_boundary_scripts = observed.get("chapter_scripts_with_evidence_boundary_phrase")
    if not isinstance(evidence_boundary_scripts, int) or not 0 <= evidence_boundary_scripts <= expected_chapter_scripts:
        errors.append("audio script reading-flow evidence-boundary script count must be within the active chapter count.")
    samples = observed.get("ordered_script_file_samples", {})
    if not isinstance(samples, dict):
        errors.append("ordered_script_file_samples must be an object.")
    else:
        if samples.get("first_five") != expected_files[:5]:
            errors.append("ordered_script_file_samples.first_five must show the reader opening order.")
        if samples.get("last_five") != expected_files[-5:]:
            errors.append("ordered_script_file_samples.last_five must show the appendix closing order.")
    boundary = str(observed.get("review_boundary", ""))
    for phrase in (
        "not narration quality review",
        "not pronunciation review",
        "not chapter timecoding",
        "not an audiobook",
        "not release approval",
    ):
        if phrase not in boundary:
            errors.append(f"review_boundary missing phrase: {phrase}")
    non_claim_text = " ".join(str(item) for item in observed.get("non_claims", [])).lower()
    for phrase in (
        "does not approve narration quality",
        "does not create mp3",
        "does not timecode chapter markers",
        "does not approve an audiobook",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing phrase: {phrase}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed review into the tracked audio-script probe manifest")
    args = parser.parse_args()

    observed = generate_observation()
    REPORT.write_text(
        json.dumps(
            {
                "schema_version": "0.1",
                "review_type": "reader_audio_script_reading_flow_review",
                "manifest": observed,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    errors = validate_observed(observed)
    if errors:
        fail(errors)

    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain an object."])
    if args.write_manifest:
        commands = manifest.setdefault("source_commands", [])
        if COMMAND not in commands:
            commands.append(COMMAND)
        refs = manifest.setdefault("local_artifact_refs", [])
        if rel(REPORT) not in refs:
            refs.append(rel(REPORT))
        manifest["audio_script_reading_flow_review"] = observed
        summary = manifest.setdefault("script_workspace_summary", {})
        if isinstance(summary, dict):
            summary["script_files"] = observed["script_files_checked"]
            summary["source_mode"] = observed["source_mode"]
            summary["requested_source_mode"] = observed["requested_source_mode"]
            summary["source_generator"] = "scripts/build_reader_edition.py"
        manifest["companion_treatment_totals"] = observed["companion_treatment_totals"]
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    elif manifest.get("audio_script_reading_flow_review") != observed:
        fail(
            [
                "audio_script_probe_manifest.json audio_script_reading_flow_review is stale; "
                "run `python3 scripts/validate_reader_audio_script_reading_flow.py --write-manifest`."
            ]
        )

    print(
        "Reader audio-script reading-flow review passed: "
        f"{observed['script_files_checked']} scripts, "
        f"{observed['chapter_marker_rows']} ordered markers, "
        f"{observed['narration_note_count']} narration notes."
    )


if __name__ == "__main__":
    main()
