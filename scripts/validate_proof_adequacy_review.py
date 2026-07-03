#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs" / "proof_adequacy_review.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
DEPTH = ROOT / "docs" / "proof_depth_classification.md"


def fail(errors: list[str]) -> None:
    print("Proof adequacy review validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def section(text: str, start: str, end: str) -> str:
    if start not in text:
        return ""
    body = text.split(start, 1)[1]
    if end in body:
        body = body.split(end, 1)[0]
    return body


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_summary_counts(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    body = section(text, "## Summary", "The reviewed targets")
    for line in body.splitlines():
        if not line.startswith("| ") or line.startswith("|---") or "Adequacy class" in line:
            continue
        cells = table_cells(line)
        if len(cells) < 2:
            continue
        try:
            counts[cells[0]] = int(cells[1].replace(",", ""))
        except ValueError:
            continue
    return counts


def parse_chapter_rows(text: str) -> list[tuple[str, int, str]]:
    rows: list[tuple[str, int, str]] = []
    body = section(text, "## Chapter-Level Target Classification", "## Follow-Through Increments")
    for line in body.splitlines():
        if not line.startswith("| `"):
            continue
        cells = table_cells(line)
        if len(cells) < 3:
            continue
        chapter_id = cells[0].strip("`")
        try:
            target_count = int(cells[1].replace(",", ""))
        except ValueError:
            continue
        rows.append((chapter_id, target_count, cells[2]))
    return rows


def metric(text: str, name: str) -> str | None:
    match = re.search(rf"^\|\s*{re.escape(name)}\s*\|\s*(.*?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def main() -> None:
    errors: list[str] = []
    review_text = REVIEW.read_text(encoding="utf-8")
    depth_text = DEPTH.read_text(encoding="utf-8")
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail(["proofs/proof_manifest.json must contain an object."])

    manifest_count = int(manifest.get("proof_target_count", 0))
    chapter_counts_raw = manifest.get("chapter_counts", {})
    if not isinstance(chapter_counts_raw, dict):
        fail(["proofs/proof_manifest.json must contain chapter_counts."])
    manifest_chapter_counts = {
        str(chapter_id): int(count)
        for chapter_id, count in chapter_counts_raw.items()
    }

    summary_counts = parse_summary_counts(review_text)
    chapter_rows = parse_chapter_rows(review_text)
    if not summary_counts:
        errors.append("Summary adequacy table is missing or unparseable.")
    if not chapter_rows:
        errors.append("Chapter-level target classification table is missing or unparseable.")

    row_chapter_counts: Counter[str] = Counter()
    row_class_counts: Counter[str] = Counter()
    for chapter_id, target_count, adequacy_class in chapter_rows:
        row_chapter_counts[chapter_id] += target_count
        row_class_counts[adequacy_class] += target_count

    if sum(row_chapter_counts.values()) != manifest_count:
        errors.append(
            f"Chapter-level adequacy rows cover {sum(row_chapter_counts.values())} targets; expected {manifest_count}."
        )
    if set(row_chapter_counts) != set(manifest_chapter_counts):
        missing = sorted(set(manifest_chapter_counts) - set(row_chapter_counts))
        extra = sorted(set(row_chapter_counts) - set(manifest_chapter_counts))
        if missing:
            errors.append(f"Chapter-level adequacy table is missing manifest chapters: {missing}.")
        if extra:
            errors.append(f"Chapter-level adequacy table contains non-manifest chapters: {extra}.")
    for chapter_id, expected_count in sorted(manifest_chapter_counts.items()):
        observed = row_chapter_counts.get(chapter_id, 0)
        if observed != expected_count:
            errors.append(f"{chapter_id}: adequacy table has {observed} targets; expected {expected_count}.")

    if row_class_counts != summary_counts:
        errors.append(
            f"Summary adequacy counts {dict(summary_counts)} do not match chapter table totals {dict(row_class_counts)}."
        )

    depth_metrics = {
        "Proof targets in manifest": metric(depth_text, "Proof targets in manifest"),
        "Lean modules scanned": metric(depth_text, "Lean modules scanned"),
        "Theorem declarations classified": metric(depth_text, "Theorem declarations classified"),
        "Direct/projection-style theorem declarations": metric(depth_text, "Direct/projection-style theorem declarations"),
        "Derived/decomposed theorem declarations": metric(depth_text, "Derived/decomposed theorem declarations"),
        "Unknown or mixed theorem declarations": metric(depth_text, "Unknown or mixed theorem declarations"),
        "Safety-critical chapter classifications present": metric(depth_text, "Safety-critical chapter classifications present"),
    }
    if any(value is None for value in depth_metrics.values()):
        errors.append("Proof-depth classification summary is missing required metrics.")
    else:
        snapshot = (
            f"Current proof-depth snapshot: {depth_metrics['Proof targets in manifest']} proof targets, "
            f"{depth_metrics['Lean modules scanned']} Lean modules, "
            f"{depth_metrics['Theorem declarations classified']} theorem declarations, "
            f"{depth_metrics['Derived/decomposed theorem declarations']} derived/decomposed, "
            f"{depth_metrics['Direct/projection-style theorem declarations']} direct/projection, "
            f"{depth_metrics['Unknown or mixed theorem declarations']} unknown/mixed, and "
            f"{depth_metrics['Safety-critical chapter classifications present']} safety-critical chapter classifications present."
        )
        normalized_review = re.sub(r"\s+", " ", review_text)
        if snapshot not in normalized_review:
            errors.append(f"Proof adequacy review is missing current proof-depth snapshot: {snapshot}")

    for required_phrase in (
        "It does not change any support state",
        "No support state changes were made.",
        "A finite predicate is not automatically an adequate formalization",
    ):
        if required_phrase not in review_text:
            errors.append(f"Proof adequacy review missing required boundary phrase: {required_phrase!r}.")

    if errors:
        fail(errors)

    print(
        "Proof adequacy review validation passed: "
        f"{manifest_count} targets, {len(manifest_chapter_counts)} manifest chapters, "
        f"{len(summary_counts)} adequacy classes."
    )


if __name__ == "__main__":
    main()
