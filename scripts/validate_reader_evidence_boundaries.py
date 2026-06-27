#!/usr/bin/env python3
"""Validate reader-edition evidence boundaries.

The live book can strip repeated research scaffolding for the reader edition and
live Human view, but the generated reader prose must still preserve each
chapter's core-claim text and support-state boundary. The live source keeps the
raw core-claim marker for AI/research auditability; the generated reader source
must strip that machine marker while preserving the claim prose and plain
support boundary. This guard checks the generated reader source, not the live
chapter source alone, so it catches regressions where evidence caveats are
hidden inside stripped sections.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import sys
import tempfile
from pathlib import Path

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "build" / "reader_evidence_boundaries_report.json"
HUMAN_ARGUMENT_BOUNDARY = "Evidence boundary: architectural argument."
REPEATED_SUPPORT_BOILERPLATE = (
    "The claim remains at `argument` support.",
    "The current support state is `argument`.",
    "The current support state is `argument`, so the claim should be read as a design rationale unless a later evidence bundle promotes it.",
)

CORE_MARKER_RE = re.compile(
    r"\[(?P<chapter_id>[A-Za-z0-9_-]+)\.core,\s*"
    r"label:\s*(?P<label>[^,\]]+),\s*"
    r"support:\s*(?P<support>[^\]]+)\]"
)
CORE_MARKER_LINE_RE = re.compile(
    r"^\[(?P<chapter_id>[A-Za-z0-9_-]+)\.core,\s*"
    r"label:\s*(?P<label>[^,\]]+),\s*"
    r"support:\s*(?P<support>[^\]]+)\]\s*(?P<claim_text>.*?)\s*$",
    re.MULTILINE,
)


def load_structure() -> dict:
    value = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapters(structure: dict) -> list[dict[str, object]]:
    chapters: list[dict[str, object]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def markers_for_chapter(text: str, chapter_id: str) -> list[dict[str, str]]:
    markers: list[dict[str, str]] = []
    for match in CORE_MARKER_LINE_RE.finditer(text):
        if match.group("chapter_id") != chapter_id:
            continue
        markers.append(
            {
                "label": match.group("label").strip(),
                "support": match.group("support").strip(),
                "marker": match.group(0),
                "claim_text": match.group("claim_text").strip(),
            }
        )
    return markers


def core_claim_section(text: str) -> str:
    match = re.search(r"^## Core Claim\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def has_plain_support_boundary(section: str, support: str) -> bool:
    normalized = re.sub(r"\s+", " ", section.lower())
    support = re.escape(support.lower())
    patterns = [
        rf"claim remains at `?{support}`? support",
        rf"current support state is `?{support}`?",
        rf"support remains `?{support}`?",
        rf"support state remains `?{support}`?",
        rf"evidence boundary:\s*architectural {support}",
    ]
    return any(re.search(pattern, normalized) for pattern in patterns)


def normalized_prose(text: str) -> str:
    text = re.sub(CORE_MARKER_RE, "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def contains_claim_text(section: str, claim_text: str) -> bool:
    if not claim_text.strip():
        return False
    return normalized_prose(claim_text) in normalized_prose(section)


def validate_generated_reader(output_dir: Path) -> dict[str, object]:
    structure = load_structure()
    chapters = flatten_chapters(structure)
    errors: list[str] = []
    records: list[dict[str, object]] = []

    for chapter in chapters:
        chapter_id = str(chapter.get("id", ""))
        relative = str(chapter.get("file", ""))
        expected_support = str(chapter.get("evidence_level", "")).strip()
        source_path = ROOT / relative
        reader_path = output_dir / relative

        if not chapter_id or not relative:
            errors.append(f"Malformed manifest chapter entry: {chapter!r}")
            continue
        if not expected_support:
            errors.append(f"{chapter_id}: manifest evidence_level is missing.")
            continue
        if not source_path.exists():
            errors.append(f"{chapter_id}: source chapter missing at {relative}.")
            continue
        if not reader_path.exists():
            errors.append(f"{chapter_id}: generated reader chapter missing at {relative}.")
            continue

        source_text = source_path.read_text(encoding="utf-8", errors="ignore")
        reader_text = reader_path.read_text(encoding="utf-8", errors="ignore")
        source_markers = markers_for_chapter(source_text, chapter_id)
        reader_markers = markers_for_chapter(reader_text, chapter_id)
        reader_raw_marker_count = len(CORE_MARKER_RE.findall(reader_text))
        reader_core = core_claim_section(reader_text)

        record: dict[str, object] = {
            "chapter_id": chapter_id,
            "file": relative,
            "manifest_support": expected_support,
            "source_marker_count": len(source_markers),
            "reader_raw_marker_count": reader_raw_marker_count,
            "reader_claim_text_retained": False,
            "reader_repeated_support_boilerplate_count": sum(
                reader_text.count(phrase) for phrase in REPEATED_SUPPORT_BOILERPLATE
            ),
            "plain_support_boundary": False,
        }

        if len(source_markers) != 1:
            errors.append(f"{relative}: expected one live-source core claim marker, found {len(source_markers)}.")
            records.append(record)
            continue
        if reader_markers or reader_raw_marker_count:
            errors.append(
                f"{relative}: generated reader chapter retained {reader_raw_marker_count} raw core claim marker(s)."
            )
            records.append(record)
            continue
        if record["reader_repeated_support_boilerplate_count"]:
            errors.append(
                f"{relative}: generated reader chapter retained repeated AI/research support boilerplate."
            )

        source_marker = source_markers[0]
        record["source_label"] = source_marker["label"]
        record["source_support"] = source_marker["support"]
        record["source_claim_text"] = source_marker["claim_text"]

        if source_marker["support"] != expected_support:
            errors.append(
                f"{relative}: live source marker support {source_marker['support']!r} "
                f"does not match manifest evidence_level {expected_support!r}."
            )
        if not reader_core:
            errors.append(f"{relative}: generated reader chapter is missing a Core Claim section.")
        else:
            claim_text_retained = contains_claim_text(reader_core, source_marker["claim_text"])
            record["reader_claim_text_retained"] = claim_text_retained
            if not claim_text_retained:
                errors.append(
                    f"{relative}: generated reader Core Claim section lacks the live source claim text after marker stripping."
                )
            plain_boundary = has_plain_support_boundary(reader_core, expected_support)
            record["plain_support_boundary"] = plain_boundary
            if not plain_boundary:
                errors.append(
                    f"{relative}: generated reader Core Claim section lacks a plain-language "
                    f"support boundary for {expected_support!r}."
                )

        records.append(record)

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile": "reader_release",
        "chapter_count": len(records),
        "status": "pass" if not errors else "fail",
        "chapter_records": records,
        "errors": errors,
        "non_claims": [
            "This report validates reader-edition evidence-boundary retention only.",
            "It does not claim a reviewed reader manuscript, ebook, PDF, DOCX, or audiobook exists.",
            "It does not promote any claim support state.",
        ],
    }


def write_report(report: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate in a temporary workspace without writing a report")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="report path for non-check runs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with tempfile.TemporaryDirectory(prefix="asi-reader-evidence-") as temp_dir:
        output_dir = Path(temp_dir)
        summary = build_reader_edition.generate(output_dir, "reader_release")
        report = validate_generated_reader(output_dir)
        report["reader_generation"] = summary

    if not args.check:
        write_report(report, Path(args.report))

    if report["status"] != "pass":
        print("Reader evidence-boundary validation failed:")
        for error in report["errors"]:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Reader evidence-boundary validation passed: "
        f"{report['chapter_count']} chapters strip raw core claim markers while preserving claim text and support boundaries."
    )


if __name__ == "__main__":
    main()
