#!/usr/bin/env python3
"""Initialize a curated reader-manuscript chapter record.

This tool prepares the future parallel human-reader source path without making
the curated manuscript an evidence authority. By default it prints the record it
would add. Use --write only after review decides that reader overlays are too
small for the intended prose edit.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
CURATED_DIR = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters"
GENERATED_DIR = ROOT / "build" / "reader_edition"

DEFAULT_CURATION_SCOPE = ["pacing", "section flow", "sentence-level voice"]
DEFAULT_RELEASE_BLOCKERS = [
    "reader_release_record_not_created",
    "format_artifact_not_reviewed",
    "curated_reconciliation_not_approved",
]
DEFAULT_MEANING_CHECKS = [
    "support-state boundary preserved in reader prose",
    "source boundary preserved or reconciled back to the live chapter",
    "proof/test status preserved without adding unrun results",
    "implementation horizon preserved without implying current implementation",
    "release blocker status preserved until an edition release record clears it",
]
DEFAULT_VOICE_PASS_SLOT_ID = "opening-origin"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def flatten_chapters(structure: dict[str, Any]) -> dict[str, dict[str, Any]]:
    chapters: dict[str, dict[str, Any]] = {}
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("id"), str):
                chapters[chapter["id"]] = chapter
    return chapters


def git_head() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except Exception:
        return "git-head-unavailable"
    return result.stdout.strip() or "git-head-unavailable"


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def generated_chapter_path(chapter: dict[str, Any]) -> Path:
    live_file = Path(str(chapter.get("file", "")))
    return GENERATED_DIR / live_file


def curated_chapter_path(chapter: dict[str, Any]) -> Path:
    live_file = Path(str(chapter.get("file", "")))
    return CURATED_DIR / live_file.name


def starter_text(chapter: dict[str, Any], generated_path: Path, head: str) -> str:
    baseline = generated_path.read_text(encoding="utf-8")
    marker = (
        "<!--\n"
        "Curated reader manuscript draft.\n"
        f"chapter_id: {chapter['id']}\n"
        f"generated_baseline_ref: {relative(generated_path)}\n"
        f"live_source_ref: {chapter['file']}@{head}\n"
        "This file is a reader-prose derivative only. Preserve claim meaning,\n"
        "support-state boundaries, source boundaries, proof/test status,\n"
        "implementation horizons, and release blockers.\n"
        "-->\n\n"
    )
    return marker + baseline


def default_voice_pass_slot_id(manifest: dict[str, Any]) -> str:
    handoff = manifest.get("reader_handoff_contract")
    if not isinstance(handoff, dict):
        return DEFAULT_VOICE_PASS_SLOT_ID
    slots = handoff.get("corben_voice_pass_slots")
    if not isinstance(slots, list):
        return DEFAULT_VOICE_PASS_SLOT_ID
    for slot in slots:
        if isinstance(slot, dict) and isinstance(slot.get("slot_id"), str) and slot["slot_id"].strip():
            return slot["slot_id"]
    return DEFAULT_VOICE_PASS_SLOT_ID


def build_record(
    chapter: dict[str, Any],
    generated_path: Path,
    curated_path: Path,
    head: str,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    chapter_id = str(chapter["id"])
    title = str(chapter["title"])
    return {
        "chapter_id": chapter_id,
        "title": title,
        "file": relative(curated_path),
        "reconciliation_status": "drafting",
        "generated_baseline_ref": relative(generated_path),
        "live_source_ref": f"{chapter['file']}@{head}",
        "claim_boundary_ref": f"appendices/C_claim_evidence_matrix.qmd#{chapter_id}.core",
        "implementation_horizon_ref": f"appendices/K_implementation_horizons.qmd#{chapter_id}",
        "curation_scope": DEFAULT_CURATION_SCOPE,
        "reader_stakes": (
            f"Readers need to understand why {title} matters to the ASI Stack before the "
            "curated prose can become release-candidate human reading."
        ),
        "reader_payoff": (
            f"The reader should leave {title} with a clear boundary, an implementation horizon, "
            "and the evidence limits that keep the idea honest."
        ),
        "voice_pass_slot_ids": [default_voice_pass_slot_id(manifest)],
        "divergence_summary": (
            "Curated reader source initialized from the generated reader baseline "
            "for future prose editing; no meaning divergence has been approved yet."
        ),
        "meaning_preservation_checks": DEFAULT_MEANING_CHECKS,
        "release_blockers": DEFAULT_RELEASE_BLOCKERS,
        "canonical_change_required": False,
        "canonical_change_ref": "",
        "review_notes": "Initialized for future curated-reader drafting; not release-reviewed.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a starter curated reader chapter file and manifest record. "
            "Defaults to dry-run output."
        )
    )
    parser.add_argument("--chapter-id", required=True, help="Manifest chapter ID to initialize.")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the starter file and update the curated reader manifest.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing starter file or replace an existing manifest record.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    structure = load_json(STRUCTURE)
    manifest = load_json(MANIFEST)
    if not isinstance(structure, dict) or not isinstance(manifest, dict):
        print("book_structure.json and curated reader manifest must both contain objects.", file=sys.stderr)
        sys.exit(1)

    chapters = flatten_chapters(structure)
    chapter = chapters.get(args.chapter_id)
    if chapter is None:
        print(f"Unknown chapter_id: {args.chapter_id}", file=sys.stderr)
        sys.exit(1)

    generated_path = generated_chapter_path(chapter)
    if not generated_path.exists():
        print(
            f"Generated reader baseline not found: {relative(generated_path)}\n"
            "Run `python3 scripts/build_reader_edition.py` before initializing curated source.",
            file=sys.stderr,
        )
        sys.exit(1)

    curated_path = curated_chapter_path(chapter)
    head = git_head()
    record = build_record(chapter, generated_path, curated_path, head, manifest)
    records = manifest.get("chapter_records")
    if not isinstance(records, list):
        print("manifest chapter_records must be a list.", file=sys.stderr)
        sys.exit(1)

    existing_index = next(
        (index for index, item in enumerate(records) if isinstance(item, dict) and item.get("chapter_id") == args.chapter_id),
        None,
    )
    if existing_index is not None and not args.force:
        print(
            f"Curated chapter record already exists for {args.chapter_id}; use --force to replace it.",
            file=sys.stderr,
        )
        sys.exit(1)
    if curated_path.exists() and not args.force:
        print(f"Curated chapter file already exists: {relative(curated_path)}; use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    if not args.write:
        print(json.dumps(record, indent=2, ensure_ascii=False))
        print("\nDry run only. Re-run with --write after review approves curated-reader drafting.")
        return

    CURATED_DIR.mkdir(parents=True, exist_ok=True)
    curated_path.write_text(starter_text(chapter, generated_path, head), encoding="utf-8")
    if existing_index is None:
        records.append(record)
    else:
        records[existing_index] = record
    if manifest.get("status") == "not_graduated":
        manifest["status"] = "drafting"
    write_json(MANIFEST, manifest)

    print(f"Initialized curated reader chapter: {relative(curated_path)}")
    print(f"Updated manifest record for {args.chapter_id}.")
    print("Run `python3 scripts/validate_reader_manuscript_manifest.py` before committing.")


if __name__ == "__main__":
    main()
