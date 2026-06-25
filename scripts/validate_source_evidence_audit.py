#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"
SOURCE_NOTES = ROOT / "sources" / "source_notes"
APPENDIX_C = ROOT / "appendices" / "C_claim_evidence_matrix.qmd"
REPORT = ROOT / "docs" / "source_evidence_audit.md"

SUPPORT_STATES_REQUIRING_EVIDENCE = {
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
}

ACCEPTED_PASSAGE_STATES = {"reviewed", "accepted", "complete"}


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def note_texts() -> dict[str, str]:
    return {
        path.stem: path.read_text(encoding="utf-8", errors="ignore")
        for path in SOURCE_NOTES.glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }


def passage_reviewed(mapping: dict[str, Any]) -> bool:
    refs = mapping.get("passage_refs") or mapping.get("passage_references") or []
    state = str(mapping.get("passage_review_state", "")).strip().lower()
    if isinstance(refs, str):
        refs = [refs] if refs.strip() else []
    return bool(refs) and state in ACCEPTED_PASSAGE_STATES


def appendix_c_has_current_counts(chapter_count: int, mapping_count: int) -> bool:
    if not APPENDIX_C.exists():
        return False
    text = APPENDIX_C.read_text(encoding="utf-8", errors="ignore")
    return (
        "No claim is marked `source-derived`" in text
        and str(chapter_count) in text
        and str(mapping_count) in text
    )


def build_report() -> tuple[str, list[str]]:
    structure = read_json(STRUCTURE)
    inventory = read_json(SOURCE_INVENTORY)
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    if not isinstance(inventory, list):
        raise TypeError("sources/source_inventory.json must contain a list")

    inventory_ids = {str(record.get("id", "")) for record in inventory if isinstance(record, dict)}
    notes = note_texts()
    chapters = flatten_chapters(structure)

    errors: list[str] = []
    warnings: list[str] = []
    chapter_rows: list[str] = []
    trace_rows: list[str] = []
    source_counts: Counter[str] = Counter()
    support_counts: Counter[str] = Counter()
    chapter_review_counts: dict[str, Counter[str]] = defaultdict(Counter)

    assigned_pairs = 0
    mapping_count = 0
    passage_reviewed_count = 0
    note_present_count = 0
    chapter_listed_count = 0
    unmapped_pairs = 0

    for chapter in chapters:
        chapter_id = str(chapter.get("id", ""))
        title = str(chapter.get("title", ""))
        claim_id = f"{chapter_id}.core"
        source_ids = [str(source_id) for source_id in chapter.get("source_ids", [])]
        assigned_pairs += len(source_ids)
        support_state = str(chapter.get("evidence_level", "argument"))
        support_counts[support_state] += 1

        mapping_by_source: dict[str, dict[str, Any]] = {}
        for index, mapping in enumerate(chapter.get("claim_source_mappings", [])):
            if not isinstance(mapping, dict):
                errors.append(f"{chapter_id}: claim_source_mappings[{index}] is not an object.")
                continue
            source_id = str(mapping.get("source_id", ""))
            if source_id in mapping_by_source:
                errors.append(f"{chapter_id}: duplicate claim-source mapping for {source_id}.")
            mapping_by_source[source_id] = mapping

        missing_mappings = [source_id for source_id in source_ids if source_id not in mapping_by_source]
        extra_mappings = [source_id for source_id in mapping_by_source if source_id not in source_ids]
        unmapped_pairs += len(missing_mappings)
        for source_id in extra_mappings:
            errors.append(f"{chapter_id}: claim-source mapping uses unassigned source {source_id}.")

        chapter_passage_reviewed = 0
        chapter_note_present = 0
        chapter_listed = 0

        for source_id in source_ids:
            source_counts[source_id] += 1
            if source_id not in inventory_ids:
                errors.append(f"{chapter_id}: assigned source {source_id} is missing from source_inventory.json.")

            mapping = mapping_by_source.get(source_id)
            note_text = notes.get(source_id, "")
            note_state = "note present" if note_text else "note missing"
            chapter_listing = bool(note_text and (chapter_id in note_text or title in note_text))
            mapping_state = "mapped" if mapping else "unmapped"
            review_state = "not passage-reviewed"

            if note_text:
                note_present_count += 1
                chapter_note_present += 1
            else:
                errors.append(f"{chapter_id}: source note missing for {source_id}.")
            if chapter_listing:
                chapter_listed_count += 1
                chapter_listed += 1
            elif note_text:
                errors.append(f"{chapter_id}: source note {source_id}.md does not list this chapter.")

            if mapping:
                mapping_count += 1
                support = str(mapping.get("mapped_support", "")).strip()
                limits = str(mapping.get("limits", "")).strip()
                if not support:
                    errors.append(f"{chapter_id}: mapping for {source_id} missing mapped_support.")
                if not limits:
                    errors.append(f"{chapter_id}: mapping for {source_id} missing limits.")
                if passage_reviewed(mapping):
                    passage_reviewed_count += 1
                    chapter_passage_reviewed += 1
                    review_state = "passage-reviewed"
                if support_state in SUPPORT_STATES_REQUIRING_EVIDENCE and not passage_reviewed(mapping):
                    errors.append(
                        f"{chapter_id}: support state {support_state} requires passage-reviewed mapping for {source_id}."
                    )

            trace_rows.append(
                f"| `{qmd_escape(claim_id)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(source_id)}` | {qmd_escape(mapping_state)} | {qmd_escape(note_state)} | {qmd_escape('chapter listed' if chapter_listing else 'chapter listing missing')} | {qmd_escape(review_state)} |"
            )

        chapter_review_counts[chapter_id]["assigned"] = len(source_ids)
        chapter_review_counts[chapter_id]["mapped"] = len(mapping_by_source) - len(extra_mappings)
        chapter_review_counts[chapter_id]["notes"] = chapter_note_present
        chapter_review_counts[chapter_id]["listed"] = chapter_listed
        chapter_review_counts[chapter_id]["passage_reviewed"] = chapter_passage_reviewed

        next_action = (
            "eligible for support review"
            if source_ids and chapter_passage_reviewed == len(source_ids)
            else "passage review required before source-derived promotion"
        )
        chapter_rows.append(
            f"| `{qmd_escape(chapter_id)}` | {len(source_ids)} | {len(mapping_by_source) - len(extra_mappings)} | {chapter_note_present} | {chapter_listed} | {chapter_passage_reviewed} | {qmd_escape(support_state)} | {qmd_escape(next_action)} |"
        )

    if not appendix_c_has_current_counts(len(chapters), mapping_count):
        errors.append("Appendix C does not expose the current chapter/mapping count and no-promotion boundary.")

    source_rows = []
    for source_id, count in source_counts.most_common():
        source_rows.append(f"| `{qmd_escape(source_id)}` | {count} | {'yes' if source_id in notes else 'no'} |")

    summary_rows = [
        f"| Chapters audited | {len(chapters)} |",
        f"| Assigned source/chapter pairs | {assigned_pairs} |",
        f"| Exact claim-source mappings | {mapping_count} |",
        f"| Unmapped assigned pairs | {unmapped_pairs} |",
        f"| Source notes present for assigned pairs | {note_present_count} |",
        f"| Source notes listing assigned chapter | {chapter_listed_count} |",
        f"| Passage-reviewed mappings recorded | {passage_reviewed_count} |",
        f"| Support-state counts | {qmd_escape(json.dumps(dict(sorted(support_counts.items()))))} |",
        f"| Validation errors | {len(errors)} |",
        f"| Warnings | {len(warnings)} |",
    ]

    error_text = "\n".join(f"- {qmd_escape(error)}" for error in errors) if errors else "- None."
    warning_text = "\n".join(f"- {qmd_escape(warning)}" for warning in warnings) if warnings else "- None."

    report = f"""# Source Evidence Audit

Generated by `python3 scripts/validate_source_evidence_audit.py --write`.

This report audits the public-safe evidence boundary between chapter claims, assigned source records, source notes, and Appendix C claim-source mappings.

It does **not** quote or publish raw private source passages. It also does **not** promote any support state. A passing audit means the source-note and claim-mapping layer is internally traceable and explicitly bounded; it does not prove the substantive adequacy of any passage review.

## Summary

| Metric | Value |
|---|---:|
{chr(10).join(summary_rows)}

## Review Policy

- A source note is drafting context, not evidence promotion.
- A claim-source mapping is a public-safe summary of why a source matters to a chapter claim, not a passage-level citation.
- A passage-reviewed mapping requires explicit passage references and a reviewed/accepted/complete passage review state in the mapping record.
- No claim should move above `argument` support until source passages, accepted evidence transitions, proof/test artifacts, or reproduced external evidence justify the narrower move.
- Raw Google Docs exports and connector-only sources remain private/local unless explicitly approved for publication.

## Chapter Review Queue

| Chapter ID | Assigned pairs | Claim-source mappings | Source notes present | Source notes listing chapter | Passage-reviewed mappings | Support state | Next action |
|---|---:|---:|---:|---:|---:|---|---|
{chr(10).join(chapter_rows)}

## Source Load Priority

Sources are sorted by how many chapter claims currently depend on their source-note mappings.

| Source ID | Assigned chapter count | Source note exists |
|---|---:|---|
{chr(10).join(source_rows)}

## Claim-Source Trace

| Claim ID | Chapter ID | Source ID | Mapping state | Source note state | Source-note chapter listing | Passage review state |
|---|---|---|---|---|---|---|
{chr(10).join(trace_rows)}

## Validation Errors

{error_text}

## Warnings

{warning_text}
"""
    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write docs/source_evidence_audit.md.")
    args = parser.parse_args()

    try:
        report, errors = build_report()
    except Exception as exc:
        print(f"Source evidence audit failed: {exc}")
        sys.exit(1)

    if args.write:
        REPORT.write_text(report, encoding="utf-8")
    elif not REPORT.exists():
        print(f"{REPORT.relative_to(ROOT)} is missing; run scripts/validate_source_evidence_audit.py --write")
        sys.exit(1)
    else:
        current = REPORT.read_text(encoding="utf-8")
        if current != report:
            print(f"{REPORT.relative_to(ROOT)} is out of date; run scripts/validate_source_evidence_audit.py --write")
            sys.exit(1)

    if errors:
        print("Source evidence audit failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    records = re.search(r"\| Assigned source/chapter pairs \| (\d+) \|", report)
    count = records.group(1) if records else "unknown"
    action = "wrote" if args.write else "validated"
    print(f"Source evidence audit {action}: {count} assigned source/chapter pairs.")


if __name__ == "__main__":
    main()
