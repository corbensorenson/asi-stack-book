#!/usr/bin/env python3
"""Build the chapter-level external-grounding status ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
AUDIT = ROOT / "docs" / "external_sota_positioning_audit.md"
OUTPUT = ROOT / "docs" / "chapter_external_grounding_status.md"
AUDIT_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|")
TODAY = "2026-06-29"


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def md_join(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"


def clean_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        part_id = str(part.get("id", ""))
        part_title = str(part.get("title", ""))
        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            row = dict(chapter)
            row["_part_id"] = part_id
            row["_part_title"] = part_title
            rows.append(row)
    return rows


def parse_audit_statuses() -> dict[str, str]:
    statuses: dict[str, str] = {}
    if not AUDIT.exists():
        return statuses
    for line in AUDIT.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = AUDIT_ROW_RE.match(line)
        if match:
            statuses[match.group(1)] = match.group(2)
    return statuses


def source_maps(records: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    by_id = {
        str(record.get("id")): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }
    external_targets: dict[str, set[str]] = {}
    for source_id, record in by_id.items():
        if record.get("priority") != "external_literature":
            continue
        for chapter_id in record.get("chapter_targets", []) or []:
            if isinstance(chapter_id, str):
                external_targets.setdefault(chapter_id, set()).add(source_id)
    return by_id, {chapter_id: sorted(source_ids) for chapter_id, source_ids in external_targets.items()}


def chapter_external_ids(
    chapter: dict[str, Any],
    inventory_by_id: dict[str, dict[str, Any]],
    external_targets: dict[str, list[str]],
) -> list[str]:
    chapter_id = str(chapter.get("id", ""))
    source_ids = {
        str(source_id)
        for source_id in chapter.get("source_ids", []) or []
        if isinstance(source_id, str)
    }
    explicit_external = {
        source_id
        for source_id in source_ids
        if inventory_by_id.get(source_id, {}).get("priority") == "external_literature"
        or source_id.startswith("ext_")
    }
    return sorted(set(external_targets.get(chapter_id, [])) | explicit_external)


def chapter_corben_source_ids(
    chapter: dict[str, Any],
    inventory_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    source_ids: list[str] = []
    for source_id in chapter.get("source_ids", []) or []:
        if not isinstance(source_id, str):
            continue
        record = inventory_by_id.get(source_id)
        if record is None:
            continue
        if record.get("priority") == "external_literature" or source_id.startswith("ext_"):
            continue
        source_ids.append(source_id)
    return source_ids


def next_action(status: str, corben_ids: list[str], external_ids: list[str]) -> str:
    if status == "source-noted":
        return (
            "Mine the linked Corben/local source notes for bibliographies, footnotes, "
            "and adjacent terms before broad search; keep these external records "
            "as comparators, not claim promotions."
        )
    if status == "explicit_exception":
        if corben_ids:
            return (
                "Keep the exception rationale current, then mine the linked "
                "Corben/local sources for fair baselines before adding any new "
                "external source records."
            )
        return (
            "Keep the exception rationale current and assign a public-safe Corben/local "
            "or external comparator source before treating the chapter as grounded."
        )
    if external_ids:
        return (
            "Add in-prose positioning before the Source crosswalk or record a deliberate "
            "exception; do not treat source assignment alone as citation."
        )
    return (
        "Mine the linked Corben/local sources first, then add source-inventory records "
        "or a deliberate exception."
    )


def build_rows() -> list[dict[str, Any]]:
    structure = read_json(STRUCTURE)
    records = read_json(INVENTORY)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    if not isinstance(records, list):
        raise SystemExit("sources/source_inventory.json must contain a list.")

    chapters = flatten_chapters(structure)
    inventory_by_id, external_targets = source_maps([record for record in records if isinstance(record, dict)])
    audit_statuses = parse_audit_statuses()

    rows: list[dict[str, Any]] = []
    for chapter in chapters:
        chapter_id = str(chapter.get("id", ""))
        external_ids = chapter_external_ids(chapter, inventory_by_id, external_targets)
        corben_ids = chapter_corben_source_ids(chapter, inventory_by_id)
        audit_status = audit_statuses.get(chapter_id, "missing")
        if external_ids:
            status = "source-noted"
        elif audit_status == "exception_recorded":
            status = "explicit_exception"
        elif audit_status == "missing":
            status = "missing"
        else:
            status = "candidate_backlog"
        rows.append(
            {
                "part": str(chapter.get("_part_title", "")),
                "chapter_id": chapter_id,
                "title": str(chapter.get("title", "")),
                "grounding_status": status,
                "external_ids": external_ids,
                "corben_ids": corben_ids,
                "audit_status": audit_status,
                "next_action": next_action(status, corben_ids, external_ids),
            }
        )
    return rows


def render_report(rows: list[dict[str, Any]]) -> str:
    counts = Counter(str(row["grounding_status"]) for row in rows)
    total = len(rows)
    source_noted = counts.get("source-noted", 0)
    exceptions = counts.get("explicit_exception", 0)
    backlog = counts.get("candidate_backlog", 0)
    missing = counts.get("missing", 0)

    lines = [
        "# Chapter External Grounding Status",
        "",
        f"Last updated: {TODAY}",
        "",
        "Generated by `python3 scripts/build_chapter_external_grounding_status.py`.",
        "",
        "This ledger turns the external-positioning audit into a chapter-by-chapter work surface for v1.x writing. It ties manifest chapters to source-noted external records, explicit external-baseline exceptions, and the Corben/local sources that should be mined before broad literature search. It is a routing and grounding status report only; it does not add citations, reproduce external results, or promote support states.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Manifest chapters | {total} |",
        f"| Chapters with source-noted external grounding records | {source_noted} |",
        f"| Chapters with explicit external-baseline exceptions | {exceptions} |",
        f"| Chapters still in candidate-backlog state | {backlog} |",
        f"| Chapters missing from the external-positioning audit | {missing} |",
        "",
        "## How To Use This Ledger",
        "",
        "- For a `source-noted` chapter, use the listed `ext_*` records as known comparators and then mine the linked Corben/local sources for bibliographies, footnotes, adjacent terms, and named prior art before adding more records.",
        "- For an `explicit_exception` chapter, keep the exception rationale visible in the chapter until a fair baseline is source-noted and positioned.",
        "- For a `candidate_backlog` chapter, do not draft external-SOTA prose until the source inventory or exception status is updated.",
        "- Do not treat this ledger as source-derived support, external-literature-backed support, reproduced benchmark evidence, or an accepted evidence transition.",
        "",
        "## Chapter Ledger",
        "",
        "| Part | Chapter ID | Chapter | Grounding status | External grounding records | Corben/local sources to mine first | External-positioning audit state | Next action |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{clean_cell(str(row['part']))} | "
            f"`{row['chapter_id']}` | "
            f"{clean_cell(str(row['title']))} | "
            f"`{row['grounding_status']}` | "
            f"{md_join(row['external_ids'])} | "
            f"{md_join(row['corben_ids'])} | "
            f"`{row['audit_status']}` | "
            f"{clean_cell(str(row['next_action']))} |"
        )
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
            "- This ledger does not promote any chapter core claim above `argument`.",
            "- This ledger does not add new external source records or source notes.",
            "- This ledger does not claim exhaustive literature coverage.",
            "- This ledger does not reproduce, verify, or accept any external result.",
            "- This ledger does not approve a v1.x evidence release or reader artifact.",
            "",
            "Regenerate with `python3 scripts/build_chapter_external_grounding_status.py`, then validate with `python3 scripts/validate_chapter_external_grounding_status.py`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the tracked report is stale.")
    args = parser.parse_args()

    text = render_report(build_rows())
    if args.check:
        if not OUTPUT.exists():
            print(f"{OUTPUT.relative_to(ROOT)} is missing; run without --check.")
            sys.exit(1)
        current = OUTPUT.read_text(encoding="utf-8", errors="ignore")
        if current != text:
            print(f"{OUTPUT.relative_to(ROOT)} is stale; run without --check.")
            sys.exit(1)
        print("Chapter external grounding status report is fresh.")
        return

    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
