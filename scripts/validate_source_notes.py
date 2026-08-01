#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "sources" / "source_notes"
MANIFEST = NOTES_DIR / "backbone_manifest.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"
CORBEN_CORPUS_CLOSURE = ROOT / "sources" / "corben_paper_corpus_closure.json"
CORBEN_CONNECTOR_CLOSURE = ROOT / "sources" / "corben_connector_source_closure.json"
SOURCE_SYNTHESIS = ROOT / "docs" / "source_mining_synthesis.md"
ACTIVE_ROADMAP = ROOT / "docs" / "post_v2_3_maintenance_transfer_and_publication_roadmap.md"

CORBEN_CLOSURE_DISPOSITIONS = {
    "chapter_integration",
    "source_note_integration",
    "research_obligation",
    "explicit_boundary",
}
CORBEN_NOTE_CLOSURE_RE = re.compile(
    r"^##\s+(?:(?=[^\n]*section)(?=[^\n]*(?:closure|coverage))[^\n]+|"
    r"closure\s+(?:ledger|status))\s*$",
    re.IGNORECASE | re.MULTILINE,
)

REQUIRED_SECTIONS = [
    "## Thesis",
    "## Mechanisms",
    "## Evidence",
    "## Failure Modes",
    "## Book Chapters Supported",
    "## Claims To Add Or Update",
    "## Open Questions",
]

SUPPORT_REQUIRING_NOTES = {
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
}


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def frontmatter_field(text: str, label: str) -> str | None:
    pattern = rf"\|\s*{re.escape(label)}\s*\|\s*([^|]+?)\s*\|"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        chapters.extend(part.get("chapters", []))
    return chapters


def assigned_source_ids(structure: dict) -> set[str]:
    source_ids: set[str] = set()
    for chapter in flatten_chapters(structure):
        for source_id in chapter.get("source_ids", []):
            if isinstance(source_id, str):
                source_ids.add(source_id)
    return source_ids


def inventory_source_ids() -> set[str]:
    if not SOURCE_INVENTORY.exists():
        return set()
    inventory = read_json(SOURCE_INVENTORY)
    if not isinstance(inventory, list):
        return set()
    return {str(record.get("id", "")) for record in inventory if isinstance(record, dict) and record.get("id")}


def validate_corben_corpus_closure(inventory_ids: set[str], errors: list[str]) -> None:
    if not CORBEN_CORPUS_CLOSURE.exists():
        errors.append("missing sources/corben_paper_corpus_closure.json")
        return
    corpus = read_json(CORBEN_CORPUS_CLOSURE)
    if not isinstance(corpus, dict):
        errors.append("sources/corben_paper_corpus_closure.json must contain an object")
        return
    if corpus.get("schema_version") != "asi_stack.corben_paper_corpus_closure.v1":
        errors.append("Corben corpus closure ledger has the wrong schema_version")
    if corpus.get("as_of") != "2026-07-31":
        errors.append("Corben corpus closure ledger must retain its audited as_of date")
    if set(corpus.get("closure_rule", [])) != CORBEN_CLOSURE_DISPOSITIONS:
        errors.append("Corben corpus closure ledger must declare all four terminal dispositions")
    claim_boundary = corpus.get("claim_boundary", "")
    if not isinstance(claim_boundary, str) or "does not promote evidence" not in claim_boundary:
        errors.append("Corben corpus closure ledger must preserve its non-promotion boundary")

    records = corpus.get("records", [])
    expected_count = corpus.get("expected_record_count")
    if not isinstance(records, list) or expected_count != 46 or len(records) != expected_count:
        errors.append(
            f"Corben corpus closure ledger must contain exactly 46 records; found {len(records) if isinstance(records, list) else 'non-list'}"
        )
        return

    seen_ids: set[str] = set()
    seen_raw_paths: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"Corben corpus closure record {index} must be an object")
            continue
        source_id = record.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"Corben corpus closure record {index} has no source_id")
            continue
        if source_id in seen_ids:
            errors.append(f"Corben corpus closure ledger repeats source ID `{source_id}`")
        seen_ids.add(source_id)
        if source_id not in inventory_ids:
            errors.append(f"Corben corpus source `{source_id}` is missing from source_inventory.json")
        if record.get("closure_state") != "section_family_complete":
            errors.append(f"`{source_id}` is not marked section_family_complete")
        if record.get("evidence_effect") != "none":
            errors.append(f"`{source_id}` improperly changes evidence state through mining closure")

        expected_note = f"sources/source_notes/{source_id}.md"
        if record.get("source_note") != expected_note:
            errors.append(f"`{source_id}` source_note must be {expected_note}")
        raw_source = record.get("raw_source")
        audit_basis = record.get("audit_basis")
        for label, relative in (("raw_source", raw_source), ("source_note", record.get("source_note")), ("audit_basis", audit_basis)):
            if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or not (ROOT / relative).exists():
                errors.append(f"`{source_id}` has a missing or invalid {label}: {relative!r}")
        if isinstance(raw_source, str):
            if raw_source in seen_raw_paths:
                errors.append(f"Corben corpus closure ledger repeats raw source path `{raw_source}`")
            seen_raw_paths.add(raw_source)

        if isinstance(audit_basis, str) and (ROOT / audit_basis).exists():
            audit_text = (ROOT / audit_basis).read_text(encoding="utf-8", errors="ignore")
            if audit_basis == expected_note and not CORBEN_NOTE_CLOSURE_RE.search(audit_text):
                errors.append(f"`{source_id}` source note lacks a section-family closure or coverage heading")
            if audit_basis != expected_note and source_id not in audit_text:
                errors.append(f"`{source_id}` is not named in its shared audit basis {audit_basis}")

    synthesis = SOURCE_SYNTHESIS.read_text(encoding="utf-8", errors="ignore") if SOURCE_SYNTHESIS.exists() else ""
    roadmap = ACTIVE_ROADMAP.read_text(encoding="utf-8", errors="ignore") if ACTIVE_ROADMAP.exists() else ""
    if "Locally readable Corben paper corpus: 46" not in synthesis or "awaiting deep audit | none" not in synthesis:
        errors.append("source mining synthesis does not state closure of all 46 locally readable Corben papers")
    if "P6.10" not in roadmap or "all 46" not in roadmap:
        errors.append("active roadmap does not preserve P6.10 and the all-46 corpus closure")


def validate_corben_connector_closure(inventory_ids: set[str], errors: list[str]) -> None:
    if not CORBEN_CONNECTOR_CLOSURE.exists():
        errors.append("missing sources/corben_connector_source_closure.json")
        return
    corpus = read_json(CORBEN_CONNECTOR_CLOSURE)
    if not isinstance(corpus, dict):
        errors.append("sources/corben_connector_source_closure.json must contain an object")
        return
    if corpus.get("schema_version") != "asi_stack.corben_connector_source_closure.v1":
        errors.append("Corben connector closure ledger has the wrong schema_version")
    if corpus.get("as_of") != "2026-07-31":
        errors.append("Corben connector closure ledger must retain its audited as_of date")
    if set(corpus.get("closure_rule", [])) != CORBEN_CLOSURE_DISPOSITIONS:
        errors.append("Corben connector closure ledger must declare all four terminal dispositions")
    claim_boundary = corpus.get("claim_boundary", "")
    if not isinstance(claim_boundary, str) or "do not promote evidence" not in claim_boundary:
        errors.append("Corben connector closure ledger must preserve its non-promotion boundary")

    records = corpus.get("records", [])
    expected_count = corpus.get("expected_record_count")
    if not isinstance(records, list) or expected_count != 7 or len(records) != expected_count:
        errors.append(
            f"Corben connector closure ledger must contain exactly 7 records; found {len(records) if isinstance(records, list) else 'non-list'}"
        )
        return

    seen_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"Corben connector closure record {index} must be an object")
            continue
        source_id = record.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"Corben connector closure record {index} has no source_id")
            continue
        if source_id in seen_ids:
            errors.append(f"Corben connector closure ledger repeats source ID `{source_id}`")
        seen_ids.add(source_id)
        if source_id not in inventory_ids:
            errors.append(f"Corben connector source `{source_id}` is missing from source_inventory.json")
        if record.get("closure_state") != "section_family_complete":
            errors.append(f"connector source `{source_id}` is not marked section_family_complete")
        if record.get("evidence_effect") != "none":
            errors.append(f"connector source `{source_id}` improperly changes evidence state through mining closure")
        dispositions = record.get("dispositions", [])
        if not isinstance(dispositions, list) or not dispositions or not set(dispositions) <= CORBEN_CLOSURE_DISPOSITIONS:
            errors.append(f"connector source `{source_id}` has invalid terminal dispositions")
        connector_url = record.get("connector_url")
        if not isinstance(connector_url, str) or not connector_url.startswith("https://"):
            errors.append(f"connector source `{source_id}` has an invalid connector_url")
        expected_note = f"sources/source_notes/{source_id}.md"
        if record.get("source_note") != expected_note or record.get("audit_basis") != expected_note:
            errors.append(f"connector source `{source_id}` must use {expected_note} as source_note and audit_basis")
            continue
        note_path = ROOT / expected_note
        if not note_path.exists():
            errors.append(f"connector source `{source_id}` is missing {expected_note}")
            continue
        note_text = note_path.read_text(encoding="utf-8", errors="ignore")
        if not CORBEN_NOTE_CLOSURE_RE.search(note_text):
            errors.append(f"connector source `{source_id}` source note lacks a section-family closure heading")
        variant_of = record.get("variant_of")
        if variant_of is not None and (not isinstance(variant_of, str) or variant_of not in inventory_ids):
            errors.append(f"connector source `{source_id}` has invalid variant_of `{variant_of}`")


def validate_note(source_id: str, errors: list[str]) -> None:
    path = NOTES_DIR / f"{source_id}.md"
    if not path.exists():
        errors.append(f"`{source_id}`: missing {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"`{source_id}`: missing section {section}")
    actual_id = frontmatter_field(text, "Source ID")
    if actual_id != f"`{source_id}`":
        errors.append(f"`{source_id}`: Source ID field is {actual_id!r}")
    if "TBD" in text:
        errors.append(f"`{source_id}`: source note still contains TBD")
    if "Do not fill this until" in text:
        errors.append(f"`{source_id}`: source note still contains template guard text")


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing sources/source_notes/backbone_manifest.json.")
    manifest = read_json(MANIFEST)
    if not isinstance(manifest, dict):
        raise SystemExit("sources/source_notes/backbone_manifest.json must contain an object.")

    required = manifest.get("note_required_for", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise SystemExit("note_required_for must be a list of source IDs.")

    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")

    assigned = assigned_source_ids(structure)
    inventory_ids = inventory_source_ids()
    required_set = set(required)
    notes_to_validate = required_set | assigned

    errors: list[str] = []
    validate_corben_corpus_closure(inventory_ids, errors)
    validate_corben_connector_closure(inventory_ids, errors)
    missing_inventory = sorted(source_id for source_id in assigned if source_id not in inventory_ids)
    for source_id in missing_inventory:
        errors.append(f"`{source_id}`: assigned in book_structure.json but missing from sources/source_inventory.json")

    for source_id in sorted(notes_to_validate):
        validate_note(source_id, errors)

    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.name in {"README.md", "_template.md"}:
            continue
        validate_note(path.stem, errors)

    for chapter in flatten_chapters(structure):
        if chapter.get("evidence_level") in SUPPORT_REQUIRING_NOTES:
            missing = [source_id for source_id in chapter.get("source_ids", []) if not (NOTES_DIR / f"{source_id}.md").exists()]
            if missing:
                errors.append(
                    f"{chapter.get('id')}: evidence_level {chapter.get('evidence_level')!r} requires source notes for {', '.join(missing)}"
                )

    if errors:
        print("Source-note validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    checked = len(
        {
            path.stem
            for path in NOTES_DIR.glob("*.md")
            if path.name not in {"README.md", "_template.md"}
        }
        | notes_to_validate
    )
    print(f"Source-note validation passed: {len(required)} required backbone notes, {len(assigned)} assigned source notes, {checked} total notes checked.")


if __name__ == "__main__":
    main()
