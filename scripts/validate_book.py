#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "_quarto.yml",
    "book_structure.json",
    "index.qmd",
    "preface.qmd",
    "sources/source_inventory.json",
    "sources/source_inventory.md",
    "scripts/sync_scaffold.py",
    "scripts/sync_proof_manifest.py",
    "scripts/validate_publication.py",
    "scripts/validate_release_profiles.py",
    "scripts/validate_reader_spine.py",
    "scripts/validate_reading_mode_toggle.py",
    "scripts/validate_human_reading_paths.py",
    "scripts/validate_reader_evidence_boundaries.py",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_chapter_handoffs.py",
    "scripts/validate_source_appendices.py",
    "scripts/validate_v1_status_snapshot.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_proof_artifact_audit.py",
    "scripts/validate_source_evidence_audit.py",
    "scripts/build_reader_edition.py",
    "scripts/build_source_matrix.py",
    "docs/book_outline.md",
    "docs/proof_artifact_audit.md",
    "docs/source_evidence_audit.md",
    "editions/release_profiles.json",
    "proofs/proof_manifest.json",
    "appendices/A_source_matrix.qmd",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/E_codex_test_specs.qmd",
    "appendices/F_changelog.qmd",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/H_external_sources.qmd",
    "appendices/J_release_editions.qmd",
    "appendices/K_implementation_horizons.qmd",
]

BAD_PHRASES = [
    "solves ASI",
    "guarantees safety",
    "proves alignment",
    "obviously safe",
    "replaces all existing methods",
]

STALE_GENERATED_PHRASES = [
    "Probe whether the chapter claim holds under the relevant",
    "Chapter is a v0.2 manuscript draft; v1.0 still needs source-note substantiation",
    "No Codex tests have been implemented or run for this chapter unless separately recorded",
    "| Test state | Planned only; no tests have been run",
    "Support or falsify this chapter's layer claim",
]

ALLOWED_SUPPORT_STATES = {
    "unsupported",
    "argument",
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
    "deprecated",
    "refuted",
}

ALLOWED_CLAIM_LABELS = {
    "Demonstrated",
    "Measured",
    "Mechanized",
    "Hypothesized",
    "Design rationale",
    "Speculative",
}


def fail(message: str) -> None:
    print(message)
    sys.exit(1)


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict) -> list[dict]:
    chapters = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            chapters.append(chapter)
    return chapters


def validate_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f" - {path}")
        sys.exit(1)


def validate_inventory() -> set[str]:
    records = read_json(ROOT / "sources" / "source_inventory.json")
    if not isinstance(records, list):
        fail("sources/source_inventory.json must contain a list.")
    required_keys = {"id", "title", "priority", "layer", "chapter_targets", "url", "notes"}
    bad_records = []
    seen = set()
    duplicates = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or not required_keys.issubset(record):
            bad_records.append(index)
            continue
        source_id = record["id"]
        if source_id in seen:
            duplicates.add(source_id)
        seen.add(source_id)
    if bad_records:
        fail(f"Source inventory records missing required keys: {bad_records}")
    if duplicates:
        fail(f"Duplicate source IDs: {sorted(duplicates)}")
    return seen


def validate_structure(source_ids: set[str]) -> list[dict]:
    structure = read_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        fail("book_structure.json must contain an object.")
    chapters = flatten_chapters(structure)
    if not chapters:
        fail("book_structure.json has no chapters.")

    ids = set()
    files = set()
    duplicate_ids = set()
    duplicate_files = set()
    unknown_sources = []
    missing_files = []

    for chapter in chapters:
        chapter_id = chapter.get("id")
        file_path = chapter.get("file")
        if not chapter_id or not file_path:
            fail(f"Chapter entry missing id or file: {chapter}")
        if chapter_id in ids:
            duplicate_ids.add(chapter_id)
        ids.add(chapter_id)
        if file_path in files:
            duplicate_files.add(file_path)
        files.add(file_path)
        if not (ROOT / file_path).exists():
            missing_files.append(file_path)
        for source_id in chapter.get("source_ids", []):
            if source_id not in source_ids:
                unknown_sources.append((chapter_id, source_id))
        chapter_source_ids = set(chapter.get("source_ids", []))
        for index, mapping in enumerate(chapter.get("claim_source_mappings", [])):
            if not isinstance(mapping, dict):
                fail(f"{chapter_id}: claim_source_mappings[{index}] must be an object.")
            mapping_source = mapping.get("source_id")
            if mapping_source not in chapter_source_ids:
                fail(f"{chapter_id}: claim_source_mappings[{index}] uses unassigned source {mapping_source!r}.")
            for field in ("mapped_support", "limits"):
                if not isinstance(mapping.get(field), str) or not mapping[field].strip():
                    fail(f"{chapter_id}: claim_source_mappings[{index}] missing non-empty {field}.")

    if duplicate_ids:
        fail(f"Duplicate chapter IDs in book_structure.json: {sorted(duplicate_ids)}")
    if duplicate_files:
        fail(f"Duplicate chapter files in book_structure.json: {sorted(duplicate_files)}")
    if missing_files:
        print("Chapter files listed in book_structure.json are missing:")
        for path in missing_files:
            print(f" - {path}")
        sys.exit(1)
    if unknown_sources:
        print("Unknown source IDs in book_structure.json:")
        for chapter_id, source_id in unknown_sources:
            print(f" - {chapter_id}: {source_id}")
        sys.exit(1)

    return chapters


def validate_chapter_frontmatter(chapters: list[dict]) -> None:
    stale = []
    for chapter in chapters:
        path = ROOT / chapter["file"]
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'last_updated: "YYYY-MM-DD"' in text:
            stale.append(path.relative_to(ROOT))
        if f'chapter_id: "{chapter["id"]}"' not in text:
            stale.append(path.relative_to(ROOT))
        if "Source loading state" not in text:
            stale.append(path.relative_to(ROOT))
    if stale:
        print("Chapter files need dynamic scaffold status updates:")
        for path in sorted(set(stale)):
            print(f" - {path}")
        sys.exit(1)


def validate_quarto_generated() -> None:
    text = (ROOT / "_quarto.yml").read_text(encoding="utf-8", errors="ignore")
    if "generated by scripts/sync_scaffold.py" not in text:
        fail("_quarto.yml should be generated by scripts/sync_scaffold.py.")


def validate_overclaims() -> None:
    violations = []
    targets = list((ROOT / "chapters").glob("*.qmd")) + list((ROOT / "appendices").glob("*.qmd"))
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in BAD_PHRASES:
            if phrase.lower() in text:
                violations.append((path.relative_to(ROOT), phrase))
    if violations:
        print("Potential overclaim phrases found:")
        for path, phrase in violations:
            print(f" - {path}: {phrase}")
        sys.exit(2)


def validate_stale_generated_language() -> None:
    violations = []
    targets = (
        list((ROOT / "chapters").glob("*.qmd"))
        + [
            ROOT / "scripts" / "draft_v02_from_manifest.py",
            ROOT / "scripts" / "sync_scaffold.py",
        ]
    )
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in STALE_GENERATED_PHRASES:
            if phrase in text:
                violations.append((path.relative_to(ROOT), phrase))
    if violations:
        print("Stale generated manuscript language found:")
        for path, phrase in violations:
            print(f" - {path}: {phrase}")
        sys.exit(2)


def validate_claim_states() -> None:
    text = (ROOT / "appendices" / "C_claim_evidence_matrix.qmd").read_text(encoding="utf-8", errors="ignore")
    missing = [state for state in ALLOWED_SUPPORT_STATES if state not in text]
    if missing:
        fail(f"Claim/evidence matrix is missing support-state definitions: {sorted(missing)}")
    missing_labels = [label for label in ALLOWED_CLAIM_LABELS if label not in text]
    if missing_labels:
        fail(f"Claim/evidence matrix is missing claim-label definitions: {sorted(missing_labels)}")


def validate_structure_proof_statuses(chapters: list[dict]) -> None:
    manifest = read_json(ROOT / "proofs" / "proof_manifest.json")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("records"), list):
        fail("proofs/proof_manifest.json must contain a records list.")

    manifest_records = {
        record.get("tag"): record
        for record in manifest["records"]
        if isinstance(record, dict) and isinstance(record.get("tag"), str)
    }
    errors: list[str] = []
    for chapter in chapters:
        chapter_id = chapter.get("id", "<missing>")
        for target in chapter.get("proof_targets", []):
            if not isinstance(target, dict):
                errors.append(f"{chapter_id}: proof_targets entry must be an object.")
                continue
            tag = target.get("tag")
            if not isinstance(tag, str) or not tag:
                errors.append(f"{chapter_id}: proof target missing tag.")
                continue
            manifest_record = manifest_records.get(tag)
            if manifest_record is None:
                errors.append(f"{chapter_id}: proof target {tag!r} missing from proofs/proof_manifest.json.")
                continue
            if manifest_record.get("chapter_id") != chapter_id:
                errors.append(
                    f"{chapter_id}: proof target {tag!r} manifest chapter is "
                    f"{manifest_record.get('chapter_id')!r}."
                )
            if manifest_record.get("status") != target.get("status"):
                errors.append(
                    f"{chapter_id}: proof target {tag!r} status "
                    f"{target.get('status')!r} does not match manifest "
                    f"{manifest_record.get('status')!r}."
                )

    if errors:
        print("book_structure.json proof targets disagree with proofs/proof_manifest.json:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)


def validate_proof_manifest() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_proof_manifest.py"), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def validate_publication_surface() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_publication.py")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def run_validator(script_name: str, *args: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def main() -> None:
    validate_required_files()
    source_ids = validate_inventory()
    chapters = validate_structure(source_ids)
    validate_quarto_generated()
    validate_chapter_frontmatter(chapters)
    validate_overclaims()
    validate_stale_generated_language()
    validate_claim_states()
    validate_proof_manifest()
    validate_structure_proof_statuses(chapters)
    run_validator("validate_release_profiles.py")
    validate_publication_surface()
    run_validator("validate_reading_mode_toggle.py")
    run_validator("validate_human_reading_paths.py")
    run_validator("validate_reader_evidence_boundaries.py", "--check")
    run_validator("validate_source_appendices.py")
    run_validator("validate_v1_status_snapshot.py")
    run_validator("validate_outline_consistency.py")
    run_validator("validate_implementation_horizons.py")
    run_validator("validate_reader_spine.py", "--check")
    run_validator("validate_chapter_dod.py")
    run_validator("validate_chapter_handoffs.py")
    run_validator("validate_visual_coverage.py")
    run_validator("validate_repeated_prose.py")
    run_validator("validate_source_notes.py")
    run_validator("validate_proof_readiness.py")
    run_validator("validate_proof_artifact_audit.py")
    run_validator("validate_source_evidence_audit.py")
    print("Book validation passed.")


if __name__ == "__main__":
    main()
