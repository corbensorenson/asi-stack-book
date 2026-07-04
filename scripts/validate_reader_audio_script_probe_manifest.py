#!/usr/bin/env python3
"""Validate the tracked reader audio-script probe manifest and summary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
SUMMARY = ROOT / "docs" / "reader_audio_script_probe_manifest.md"
SCRIPT = ROOT / "scripts" / "build_audio_script.py"
REQUIRED_COMMAND_FRAGMENTS = (
    "python3 scripts/build_audio_script.py --check",
    "python3 scripts/build_audio_script.py",
    "inspect audio_manifest.json in a temporary workspace",
    "python3 scripts/validate_reader_audio_script_reading_flow.py --write-manifest",
)
REQUIRED_REVIEW_FILES = {
    "audio_manifest.json",
    "AUDIO_RELEASE_CHECKLIST.md",
    "companion_notes.md",
    "chapter_markers.md",
    "pronunciation_glossary.md",
    "proof_equation_reading_rules.md",
}
EXPECTED_TARGET_STATUS = {
    "mp3": "target_not_generated",
    "m4b": "target_not_generated",
    "audio-embedded-epub": "target_not_generated",
}
KEY_FIGURE_COMPANION_PATH = "editions/reader_manuscript/v1_0/companion_notes/key-figures.md"
EXPECTED_KEY_FIGURE_COUNT = 10
COMPANION_TOTAL_KEYS = (
    "tables",
    "mermaid_diagrams",
    "code_or_schema_blocks",
    "images",
)
REQUIRED_BLOCKERS = {
    "reviewed_reader_release_record_not_created_for_audio",
    "narration_script_not_reviewed",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_metadata_not_reviewed",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
}
EXPECTED_READING_FLOW_EXACT = {
    "status": "passed_audio_script_reading_flow_review",
    "source_workspace": "build/audio_script",
    "source_generator": "scripts/build_audio_script.py",
    "source_mode": "tracked_curated_reader_manuscript",
    "requested_source_mode": "curated_reader_manuscript",
    "report_ref": "build/audio_script/audio_script_reading_flow_report.json",
    "review_command": "python3 scripts/validate_reader_audio_script_reading_flow.py --write-manifest",
    "script_files_checked": 49,
    "front_matter_scripts_checked": 2,
    "chapter_scripts_checked": 44,
    "appendix_scripts_checked": 3,
    "script_file_order_status": "matches_book_structure",
    "script_file_order_errors": [],
    "combined_script_sha256": "6c8aca942c3e05a6dddcb48696a2512283e713403387bc2d6ea10b4e17a26732",
    "text_characters_checked": 1067718,
    "word_tokens_checked": 143488,
    "release_note_count": 49,
    "review_frontmatter_count": 49,
    "narration_note_count": 66,
    "table_narration_notes": 5,
    "diagram_narration_notes": 50,
    "image_narration_notes": 11,
    "code_schema_narration_notes": 0,
    "companion_treatment_totals": {
        "tables": 5,
        "mermaid_diagrams": 50,
        "code_or_schema_blocks": 0,
        "images": 11,
    },
    "chapter_marker_rows": 49,
    "chapter_marker_order_status": "matches_script_file_order",
    "chapter_marker_order_errors": [],
    "chapter_marker_tbd_rows": 49,
    "implementation_horizon_chapter_scripts": 44,
    "chapter_scripts_with_evidence_boundary_phrase": 26,
    "live_marker_hits": 0,
    "raw_core_claim_marker_hits": 0,
    "replacement_character_count": 0,
    "max_line_characters": 1800,
    "max_word_characters": 143,
    "target_artifact_status": EXPECTED_TARGET_STATUS,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader audio-script probe manifest validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_string(owner: str, key: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}: {key} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner}: {key} must contain at least {min_words} words.")
    return value


def require_string_list(owner: str, key: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner}: {key} entries must be non-empty strings.")
        else:
            result.append(item)
    return result


def require_int(owner: str, key: str, value: Any, errors: list[str], *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{owner}: {key} must be an integer.")
        return 0
    if value < minimum:
        errors.append(f"{owner}: {key} must be at least {minimum}.")
    return value


def validate_ref(owner: str, ref: str, errors: list[str]) -> None:
    path_part = ref.split("#", 1)[0]
    if not path_part:
        errors.append(f"{owner}: ref must include a path before any anchor: {ref!r}.")
        return
    if not (ROOT / path_part).exists():
        errors.append(f"{owner}: referenced tracked path does not exist: {path_part}.")


def expected_script_order() -> list[str]:
    structure = load_json(ROOT / "book_structure.json")
    expected: list[str] = []
    if not isinstance(structure, dict):
        return expected
    for item in structure.get("front_matter", []):
        if isinstance(item, str):
            expected.append(str(Path(item).with_suffix(".md")))
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("file"), str):
                expected.append(str(Path(chapter["file"]).with_suffix(".md")))
    expected.extend(
        [
            "appendices/B_glossary.md",
            "appendices/G_corben_source_corpus.md",
            "appendices/H_external_sources.md",
        ]
    )
    return expected


def load_audio_module() -> Any:
    sys.path.insert(0, str((ROOT / "scripts").resolve()))
    spec = importlib.util.spec_from_file_location("build_audio_script", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {rel(SCRIPT)}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generated_audio_manifest(errors: list[str]) -> tuple[dict[str, Any], Path | None, tempfile.TemporaryDirectory[str] | None]:
    check = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check.returncode != 0:
        errors.append(f"`python3 scripts/build_audio_script.py --check` failed:\n{check.stdout}{check.stderr}")
        return {}, None, None

    module = load_audio_module()
    temp_context = tempfile.TemporaryDirectory(prefix="asi-audio-probe-")
    temp_path = Path(temp_context.name)
    manifest = module.generate(temp_path)
    if not isinstance(manifest, dict):
        errors.append("Generated audio manifest must be an object.")
        return {}, temp_path, temp_context
    return manifest, temp_path, temp_context


def validate_generated_workspace(
    generated: dict[str, Any],
    workspace: Path | None,
    tracked: dict[str, Any],
    errors: list[str],
) -> None:
    if workspace is None:
        return
    script_files = generated.get("script_files")
    if not isinstance(script_files, list):
        errors.append("Generated audio manifest script_files must be a list.")
        script_files = []
    summary = tracked.get("script_workspace_summary")
    if not isinstance(summary, dict):
        errors.append("script_workspace_summary must be an object.")
        summary = {}

    if len(script_files) != summary.get("script_files"):
        errors.append(
            f"tracked script file count {summary.get('script_files')} does not match generated {len(script_files)}."
        )
    if script_files != expected_script_order():
        errors.append("Generated audio manifest script_files must follow book_structure order.")
    if generated.get("source_profile") != summary.get("source_profile"):
        errors.append("Generated source_profile does not match tracked source_profile.")
    if generated.get("source_mode") != summary.get("source_mode"):
        errors.append("Generated source_mode does not match tracked source_mode.")
    if generated.get("requested_source_mode") != summary.get("requested_source_mode"):
        errors.append("Generated requested_source_mode does not match tracked requested_source_mode.")
    if generated.get("source_generator") != summary.get("source_generator"):
        errors.append("Generated source_generator does not match tracked source_generator.")
    if generated.get("audio_profile") != summary.get("audio_profile"):
        errors.append("Generated audio_profile does not match tracked audio_profile.")
    if generated.get("implementation_horizon_script_status") != "pass":
        errors.append("Generated implementation_horizon_script_status must be pass.")
    if generated.get("review_status") != "review_required":
        errors.append("Generated review_status must be review_required.")
    if generated.get("target_artifact_status") != EXPECTED_TARGET_STATUS:
        errors.append("Generated target_artifact_status must keep all audio targets not generated.")

    generated_key_figures = generated.get("key_figure_companion_note")
    tracked_key_figures = tracked.get("key_figure_companion_note")
    if generated_key_figures != tracked_key_figures:
        errors.append("Generated key_figure_companion_note does not match tracked manifest.")

    treatment = generated.get("companion_treatment_summary")
    if not isinstance(treatment, dict):
        errors.append("Generated companion_treatment_summary must be an object.")
        treatment = {}
    totals = {
        key: sum(int(value.get(key, 0)) for value in treatment.values() if isinstance(value, dict))
        for key in COMPANION_TOTAL_KEYS
    }
    if totals != tracked.get("companion_treatment_totals"):
        errors.append(f"tracked companion treatment totals {tracked.get('companion_treatment_totals')} do not match generated {totals}.")

    for required in REQUIRED_REVIEW_FILES:
        if not (workspace / required).exists():
            errors.append(f"Generated audio workspace missing required review file: {required}")

    proof_rules = (workspace / "proof_equation_reading_rules.md").read_text(
        encoding="utf-8",
        errors="ignore",
    ).lower()
    for phrase in (
        "theorem ids",
        "lean predicates",
        "support states",
        "equations",
        "negative controls",
        "these rules do not claim mp3",
        "these rules do not promote any chapter core claim",
    ):
        if phrase not in proof_rules:
            errors.append(f"proof_equation_reading_rules.md missing phrase: {phrase}")

    glossary = (workspace / "pronunciation_glossary.md").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    for term in ("ASI", "MoECOT", "Lean", "EPUB", "DOCX", "MP3", "M4B"):
        if term not in glossary:
            errors.append(f"pronunciation_glossary.md missing term: {term}")

    companion_notes = (workspace / "companion_notes.md").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    for phrase in (
        "Key-Figure Spoken Summary Routing",
        KEY_FIGURE_COMPANION_PATH,
        "Draft figure summaries routed: 10",
        "not narration approval",
        "not reader release approval",
    ):
        if phrase not in companion_notes:
            errors.append(f"companion_notes.md missing key-figure routing phrase: {phrase}")
    if companion_notes.count("assets/diagrams/") < EXPECTED_KEY_FIGURE_COUNT:
        errors.append("companion_notes.md must include all ten key-figure asset rows.")


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if manifest.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if manifest.get("status") != "local_audio_script_probe_record":
        errors.append("status must be local_audio_script_probe_record.")
    require_string("manifest", "purpose", manifest.get("purpose"), errors, min_words=18)

    commands = "\n".join(require_string_list("manifest", "source_commands", manifest.get("source_commands"), errors))
    for fragment in REQUIRED_COMMAND_FRAGMENTS:
        if fragment not in commands:
            errors.append(f"source_commands missing required fragment: {fragment}")

    for ref in require_string_list("manifest", "local_artifact_refs", manifest.get("local_artifact_refs"), errors):
        if not ref.startswith("build/"):
            errors.append(f"local_artifact_refs should point to ignored build outputs: {ref}")
    for ref in require_string_list("manifest", "tracked_evidence_refs", manifest.get("tracked_evidence_refs"), errors):
        validate_ref("tracked_evidence_refs", ref, errors)

    summary = manifest.get("script_workspace_summary")
    if not isinstance(summary, dict):
        errors.append("script_workspace_summary must be an object.")
        summary = {}
    if summary.get("status") != "generated_in_temp_and_checked":
        errors.append("script_workspace_summary.status must be generated_in_temp_and_checked.")
    if summary.get("source_profile") != "reader_release":
        errors.append("script_workspace_summary.source_profile must be reader_release.")
    if summary.get("source_mode") != "tracked_curated_reader_manuscript":
        errors.append("script_workspace_summary.source_mode must be tracked_curated_reader_manuscript.")
    if summary.get("requested_source_mode") != "curated_reader_manuscript":
        errors.append("script_workspace_summary.requested_source_mode must be curated_reader_manuscript.")
    if summary.get("source_generator") != "scripts/build_curated_reader_edition.py":
        errors.append("script_workspace_summary.source_generator must be scripts/build_curated_reader_edition.py.")
    if summary.get("audio_profile") != "audio_release":
        errors.append("script_workspace_summary.audio_profile must be audio_release.")
    require_int("script_workspace_summary", "script_files", summary.get("script_files"), errors, minimum=1)
    if summary.get("implementation_horizon_script_status") != "pass":
        errors.append("script_workspace_summary.implementation_horizon_script_status must be pass.")
    if summary.get("review_status") != "review_required":
        errors.append("script_workspace_summary.review_status must be review_required.")
    review_files = set(
        require_string_list(
            "script_workspace_summary",
            "required_review_files",
            summary.get("required_review_files"),
            errors,
        )
    )
    missing_review_files = REQUIRED_REVIEW_FILES - review_files
    if missing_review_files:
        errors.append(f"script_workspace_summary.required_review_files missing {sorted(missing_review_files)}.")

    totals = manifest.get("companion_treatment_totals")
    if not isinstance(totals, dict):
        errors.append("companion_treatment_totals must be an object.")
        totals = {}
    for key in COMPANION_TOTAL_KEYS:
        require_int("companion_treatment_totals", key, totals.get(key), errors, minimum=0)

    if manifest.get("target_artifact_status") != EXPECTED_TARGET_STATUS:
        errors.append("target_artifact_status must keep MP3, M4B, and audio-embedded EPUB at target_not_generated.")

    key_figures = manifest.get("key_figure_companion_note")
    if not isinstance(key_figures, dict):
        errors.append("key_figure_companion_note must be an object.")
        key_figures = {}
    if key_figures.get("path") != KEY_FIGURE_COMPANION_PATH:
        errors.append("key_figure_companion_note.path drifted.")
    if "drafting" not in str(key_figures.get("status", "")).lower():
        errors.append("key_figure_companion_note.status must remain drafting.")
    if key_figures.get("figure_count") != EXPECTED_KEY_FIGURE_COUNT:
        errors.append("key_figure_companion_note.figure_count must be 10.")
    if key_figures.get("has_audio_treatment") is not True:
        errors.append("key_figure_companion_note.has_audio_treatment must be true.")
    if key_figures.get("has_e_reader_treatment") is not True:
        errors.append("key_figure_companion_note.has_e_reader_treatment must be true.")
    if int(key_figures.get("non_claim_boundary_count", 0)) < 5:
        errors.append("key_figure_companion_note.non_claim_boundary_count must be at least 5.")
    table = key_figures.get("spoken_summary_table")
    if not isinstance(table, list) or sum(1 for row in table if "assets/diagrams/" in str(row)) != EXPECTED_KEY_FIGURE_COUNT:
        errors.append("key_figure_companion_note.spoken_summary_table must carry all ten asset rows.")

    blockers = set(require_string_list("manifest", "release_blockers_preserved", manifest.get("release_blockers_preserved"), errors))
    missing_blockers = REQUIRED_BLOCKERS - blockers
    if missing_blockers:
        errors.append(f"release_blockers_preserved missing {sorted(missing_blockers)}.")

    non_claims = require_string_list("manifest", "non_claims", manifest.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in (
        "not an audiobook",
        "does not approve",
        "does not check narration quality",
        "does not promote any chapter core claim",
        "does not promote any claim support state",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims must include boundary phrase: {phrase}")

    reading_flow = manifest.get("audio_script_reading_flow_review")
    if not isinstance(reading_flow, dict):
        errors.append("audio_script_reading_flow_review must be an object.")
        reading_flow = {}
    for key, expected in EXPECTED_READING_FLOW_EXACT.items():
        if reading_flow.get(key) != expected:
            errors.append(f"audio_script_reading_flow_review.{key} must be {expected!r}.")
    samples = reading_flow.get("ordered_script_file_samples", {})
    if not isinstance(samples, dict):
        errors.append("audio_script_reading_flow_review.ordered_script_file_samples must be an object.")
    else:
        if samples.get("first_five") != [
            "index.md",
            "preface.md",
            "chapters/asi-is-a-stack-not-a-model.md",
            "chapters/the-efficient-asi-hypothesis.md",
            "chapters/system-boundaries-and-authority.md",
        ]:
            errors.append("audio_script_reading_flow_review first_five sample must show the reader opening order.")
        if samples.get("last_five") != [
            "chapters/living-book-methodology.md",
            "chapters/open-research-agenda-and-bibliography-plan.md",
            "appendices/B_glossary.md",
            "appendices/G_corben_source_corpus.md",
            "appendices/H_external_sources.md",
        ]:
            errors.append("audio_script_reading_flow_review last_five sample must show the appendix closing order.")
    boundary = require_string(
        "audio_script_reading_flow_review",
        "review_boundary",
        reading_flow.get("review_boundary"),
        errors,
        min_words=28,
    )
    for phrase in (
        "not narration quality review",
        "not pronunciation review",
        "not chapter timecoding",
        "not an audiobook",
        "not release approval",
    ):
        if phrase not in boundary:
            errors.append(f"audio_script_reading_flow_review.review_boundary missing phrase: {phrase}")
    reading_non_claims = " ".join(
        require_string_list(
            "audio_script_reading_flow_review",
            "non_claims",
            reading_flow.get("non_claims"),
            errors,
        )
    ).lower()
    for phrase in (
        "does not approve narration quality",
        "does not create mp3",
        "does not timecode chapter markers",
        "does not approve an audiobook",
        "does not promote any chapter core claim",
    ):
        if phrase not in reading_non_claims:
            errors.append(f"audio_script_reading_flow_review.non_claims missing phrase: {phrase}")

    generated, workspace, temp_context = generated_audio_manifest(errors)
    if generated:
        validate_generated_workspace(generated, workspace, manifest, errors)
    if temp_context is not None:
        temp_context.cleanup()

    return errors


def validate_summary(manifest: dict[str, Any], errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    summary = manifest.get("script_workspace_summary", {})
    totals = manifest.get("companion_treatment_totals", {})
    script_files = summary.get("script_files") if isinstance(summary, dict) else None
    mermaid_diagrams = totals.get("mermaid_diagrams") if isinstance(totals, dict) else None
    required_fragments = [
        "Reader Audio-Script Probe Manifest",
        "tracked curated reader manuscript",
        "python3 scripts/build_audio_script.py --check",
        "| Source mode | `tracked_curated_reader_manuscript` |",
        f"| Script files | {script_files} |",
        "| Implementation-horizon script status | pass |",
        f"| Mermaid diagrams | {mermaid_diagrams} |",
        "Audio Script Reading-Flow Review",
        "matches book-structure order",
        "49 ordered markers",
        "66 narration notes",
        "1,067,718 text characters",
        "not narration quality review",
        "| MP3 | `target_not_generated` |",
        "Key-figure companion note |",
        "ten draft key figures",
        KEY_FIGURE_COMPANION_PATH,
        "audio_edition_release_record_not_created",
        "This manifest is not an audiobook",
        "does not promote any chapter core claim",
        "does not promote any claim support state",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def main() -> None:
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain an object."])
    errors = validate_manifest(manifest)
    validate_summary(manifest, errors)
    if errors:
        fail(errors)
    summary = manifest.get("script_workspace_summary", {})
    totals = manifest.get("companion_treatment_totals", {})
    print(
        "Reader audio-script probe manifest validation passed: "
        f"{summary.get('script_files')} script files, "
        f"{totals.get('mermaid_diagrams')} diagram notes, ordered reading flow, and no audio artifacts generated."
    )


if __name__ == "__main__":
    main()
