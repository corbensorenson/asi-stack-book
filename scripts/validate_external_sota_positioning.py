#!/usr/bin/env python3
"""Validate the external-SOTA chapter-positioning audit report.

The release gate is stricter than this default check: every chapter eventually
needs in-prose external positioning or an explicit exception. This validator
keeps the current audit honest while that prose work is still in progress.
Use --release to require the gate to be fully closed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
NOTES_DIR = ROOT / "sources" / "source_notes"
REPORT = ROOT / "docs" / "external_sota_positioning_audit.md"
SOURCE_CROSSWALK_RE = re.compile(r"^## Source crosswalk\b", re.MULTILINE)
EXT_ID_RE = re.compile(r"\bext_[A-Za-z0-9_]+\b")
EXCEPTION_RE = re.compile(r"External baseline exception:\s+\S", re.IGNORECASE)


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def before_source_crosswalk(text: str) -> str:
    match = SOURCE_CROSSWALK_RE.search(text)
    return text[: match.start()] if match else text


def source_targets(records: list[dict]) -> dict[str, list[str]]:
    targets: dict[str, list[str]] = {}
    for record in records:
        source_id = str(record.get("id", ""))
        if not source_id.startswith("ext_"):
            continue
        for chapter_id in record.get("chapter_targets", []) or []:
            targets.setdefault(str(chapter_id), []).append(source_id)
    return {chapter_id: sorted(set(source_ids)) for chapter_id, source_ids in targets.items()}


def chapter_rows() -> list[dict[str, object]]:
    structure = read_json(STRUCTURE)
    records = read_json(INVENTORY)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    if not isinstance(records, list):
        raise SystemExit("sources/source_inventory.json must contain a list.")
    targets = source_targets([record for record in records if isinstance(record, dict)])
    note_ids = {
        path.stem
        for path in NOTES_DIR.glob("ext_*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    rows: list[dict[str, object]] = []
    for chapter in flatten_chapters(structure):
        chapter_id = str(chapter.get("id", ""))
        file_path = ROOT / str(chapter.get("file", ""))
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        pre_crosswalk = before_source_crosswalk(text)
        positioned_ids = sorted(set(EXT_ID_RE.findall(pre_crosswalk)))
        has_exception = bool(EXCEPTION_RE.search(pre_crosswalk))
        targeted_ids = targets.get(chapter_id, [])
        missing_notes = [source_id for source_id in targeted_ids if source_id not in note_ids]
        if positioned_ids:
            status = "positioned"
            next_action = "Keep source-note boundary and support-state language honest."
        elif has_exception:
            status = "exception_recorded"
            next_action = "Keep exception rationale current until a source-noted external baseline is assigned."
        elif targeted_ids:
            status = "needs_positioning"
            next_action = "Add in-prose external baseline positioning before Source crosswalk."
        else:
            status = "needs_exception_or_source"
            next_action = "Record a deliberate exception or add a source-noted external baseline before Source crosswalk."
        rows.append(
            {
                "chapter_id": chapter_id,
                "title": str(chapter.get("title", "")),
                "file": str(chapter.get("file", "")),
                "status": status,
                "positioned_ids": positioned_ids,
                "has_exception": has_exception,
                "targeted_ids": targeted_ids,
                "missing_notes": missing_notes,
                "next_action": next_action,
            }
        )
    return rows


def md_join(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"


def render_report(rows: list[dict[str, object]]) -> str:
    total = len(rows)
    positioned = sum(1 for row in rows if row["status"] == "positioned")
    exceptions = sum(1 for row in rows if row["status"] == "exception_recorded")
    needs_positioning = sum(1 for row in rows if row["status"] == "needs_positioning")
    needs_exception = sum(1 for row in rows if row["status"] == "needs_exception_or_source")
    missing_notes = sum(len(row["missing_notes"]) for row in rows)
    lines = [
        "# External SOTA Positioning Audit",
        "",
        "Last updated: 2026-06-29",
        "",
        "This generated audit tracks the Phase 6 release blocker: each chapter should name the relevant external baseline in prose before the Source crosswalk, or record a deliberate exception. It is a placement audit only; it does not claim complete literature coverage, reproduced external results, source-derived support, or support-state promotion.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Manifest chapters | {total} |",
        f"| Chapters with `ext_*` positioning before Source crosswalk | {positioned} |",
        f"| Chapters with explicit external-baseline exceptions | {exceptions} |",
        f"| Chapters with source-noted external targets but no in-prose positioning yet | {needs_positioning} |",
        f"| Chapters needing an exception or additional external source assignment | {needs_exception} |",
        f"| Targeted external source notes missing | {missing_notes} |",
        "",
        "## Chapter Queue",
        "",
        "| Chapter | Status | External IDs already in prose | Source-inventory targets | Next action |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['chapter_id']}` | "
            f"`{row['status']}` | "
            f"{md_join(row['positioned_ids'])} | "
            f"{md_join(row['targeted_ids'])} | "
            f"{row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
            "- This audit does not promote any chapter core claim above `argument`.",
            "- This audit does not treat a source-inventory target as a sufficient citation in chapter prose.",
            "- This audit does not reproduce or verify any external result.",
            "- This audit does not claim comprehensive literature coverage.",
            "- This audit does not approve a v1.0 evidence release.",
            "",
            "Run `python3 scripts/validate_external_sota_positioning.py --write-report` after external-positioning prose changes, then run the default validator in check mode.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true", help="Regenerate docs/external_sota_positioning_audit.md.")
    parser.add_argument("--release", action="store_true", help="Require every chapter to have positioning or an exception marker.")
    args = parser.parse_args()

    rows = chapter_rows()
    report = render_report(rows)
    if args.write_report:
        REPORT.write_text(report, encoding="utf-8")

    errors: list[str] = []
    if not REPORT.exists():
        errors.append(f"{REPORT.relative_to(ROOT)} is missing; run with --write-report.")
    elif REPORT.read_text(encoding="utf-8") != report:
        errors.append(f"{REPORT.relative_to(ROOT)} is stale; run with --write-report.")

    if any(row["missing_notes"] for row in rows):
        for row in rows:
            if row["missing_notes"]:
                errors.append(
                    f"{row['chapter_id']}: targeted external sources missing notes: {row['missing_notes']}"
                )

    if args.release:
        open_rows = [
            row
            for row in rows
            if row["status"] not in {"positioned", "exception_recorded"}
        ]
        for row in open_rows:
            errors.append(f"{row['chapter_id']}: external-SOTA release gate still open ({row['status']}).")

    if errors:
        print("External SOTA positioning validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    positioned = sum(1 for row in rows if row["status"] == "positioned")
    print(
        "External SOTA positioning audit passed: "
        f"{positioned} of {len(rows)} chapters positioned before Source crosswalk; "
        f"{sum(1 for row in rows if row['status'] == 'exception_recorded')} exception(s) recorded."
    )


if __name__ == "__main__":
    main()
