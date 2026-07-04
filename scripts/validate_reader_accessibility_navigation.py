#!/usr/bin/env python3
"""Validate source-level accessibility and navigation shape for the reader edition.

This is a tracked source review for the curated reader manuscript. It checks
chapter source files, headings, draft key-figure text alternatives, and
release-boundary preservation without claiming rendered accessibility,
screen-reader approval, keyboard-only approval, e-reader approval, or release
approval.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_navigation_manifest.json"
REVIEW = ROOT / "docs" / "reader_accessibility_navigation_review.md"
COMMAND = "python3 scripts/validate_reader_accessibility_navigation.py"
RESULT_ID = "reader-accessibility-navigation-source-review-2026-07-04"

EXPECTED_CHAPTERS = 44
EXPECTED_KEY_FIGURES = 10
REQUIRED_RELEASE_BLOCKERS = {
    "curated_reconciliation_not_approved",
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
}
LIVE_ONLY_MARKERS = [
    "Chapter status",
    "Drafting guardrail",
    "Codex test plan",
    "Source crosswalk",
    "Claim-source mapping status",
    "Formalization hooks",
]
RAW_CORE_CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[(?P<caption>[^\]]*)\]\((?P<path>[^)]+)\)\{(?P<attrs>[^}]*)\}")
FIG_ALT_RE = re.compile(r'fig-alt="([^"]+)"')


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader accessibility/navigation validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_heading_slug(text: str) -> str:
    text = re.sub(r"\{#.*?\}\s*$", "", text).strip().lower()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def chapter_records(manifest: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    records = manifest.get("chapter_records", [])
    if not isinstance(records, list):
        errors.append("reader manuscript chapter_records must be a list.")
        return []
    typed_records: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"chapter_records[{index}] must be an object.")
            continue
        typed_records.append(record)
    return typed_records


def inspect_chapter(record: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    chapter_id = str(record.get("chapter_id", ""))
    file_value = record.get("file")
    if not isinstance(file_value, str) or not file_value:
        errors.append(f"{chapter_id or '<missing>'}: chapter record missing file.")
        return {
            "chapter_id": chapter_id,
            "file": "",
            "exists": False,
            "passed": False,
        }
    path = ROOT / file_value
    if not path.exists():
        errors.append(f"{chapter_id}: missing curated reader chapter file {file_value}.")
        return {
            "chapter_id": chapter_id,
            "file": file_value,
            "exists": False,
            "passed": False,
        }

    text = path.read_text(encoding="utf-8")
    headings = [
        {"level": len(match.group(1)), "title": match.group(2).strip(), "slug": markdown_heading_slug(match.group(2))}
        for match in HEADING_RE.finditer(text)
    ]
    heading_counts = Counter(str(row["level"]) for row in headings)
    h1_count = heading_counts.get("1", 0)
    handoff_count = text.count("## Handoff")
    skipped_headings: list[str] = []
    duplicate_slugs: list[str] = []
    live_marker_leaks = [marker for marker in LIVE_ONLY_MARKERS if marker in text]

    previous_level = 0
    for heading in headings:
        level = int(heading["level"])
        if previous_level and level > previous_level + 1:
            skipped_headings.append(f"{previous_level}->{level}: {heading['title']}")
        previous_level = level

    seen: Counter[str] = Counter()
    for heading in headings:
        slug = str(heading["slug"])
        if not slug:
            continue
        seen[slug] += 1
        if seen[slug] == 2:
            duplicate_slugs.append(slug)

    images: list[dict[str, Any]] = []
    for match in IMAGE_RE.finditer(text):
        image_path = match.group("path")
        attrs = match.group("attrs")
        alt_match = FIG_ALT_RE.search(attrs)
        resolved = (path.parent / image_path).resolve()
        boundary_window = text[match.end() : match.end() + 500]
        images.append(
            {
                "caption": match.group("caption").strip(),
                "image_path": image_path,
                "resolved_exists": resolved.exists(),
                "fig_alt": alt_match.group(1) if alt_match else "",
                "fig_alt_word_count": word_count(alt_match.group(1)) if alt_match else 0,
                "figure_id": next((part for part in attrs.split() if part.startswith("#")), ""),
                "figure_boundary_present": "Figure boundary:" in boundary_window,
            }
        )

    raw_claim_marker = RAW_CORE_CLAIM_RE.search(text) is not None
    missing_blockers = sorted(REQUIRED_RELEASE_BLOCKERS - set(record.get("release_blockers", [])))
    passed = (
        h1_count == 1
        and handoff_count == 1
        and not skipped_headings
        and not duplicate_slugs
        and not live_marker_leaks
        and not raw_claim_marker
        and not missing_blockers
        and all(image.get("resolved_exists") for image in images)
        and all(image.get("fig_alt_word_count", 0) >= 12 for image in images)
        and all(image.get("figure_boundary_present") for image in images)
    )
    if h1_count != 1:
        errors.append(f"{chapter_id}: expected exactly one H1, found {h1_count}.")
    if handoff_count != 1:
        errors.append(f"{chapter_id}: expected exactly one ## Handoff section, found {handoff_count}.")
    if skipped_headings:
        errors.append(f"{chapter_id}: heading levels skip: {skipped_headings[:3]}.")
    if duplicate_slugs:
        errors.append(f"{chapter_id}: duplicate heading slug(s): {duplicate_slugs[:3]}.")
    if live_marker_leaks:
        errors.append(f"{chapter_id}: live-only marker leak(s): {live_marker_leaks}.")
    if raw_claim_marker:
        errors.append(f"{chapter_id}: raw core claim marker leaked into reader source.")
    if missing_blockers:
        errors.append(f"{chapter_id}: missing release blockers {missing_blockers}.")
    for image in images:
        if not image["resolved_exists"]:
            errors.append(f"{chapter_id}: image path does not resolve: {image['image_path']}.")
        if image["fig_alt_word_count"] < 12:
            errors.append(f"{chapter_id}: image {image['image_path']} fig-alt is shorter than 12 words.")
        if image["figure_boundary_present"] is not True:
            errors.append(f"{chapter_id}: image {image['image_path']} missing nearby Figure boundary paragraph.")

    return {
        "chapter_id": chapter_id,
        "title": record.get("title", ""),
        "file": file_value,
        "exists": True,
        "reconciliation_status": record.get("reconciliation_status", ""),
        "missing_release_blockers": missing_blockers,
        "character_count": len(text),
        "heading_count": len(headings),
        "heading_counts": dict(sorted(heading_counts.items())),
        "h1_count": h1_count,
        "h2_count": heading_counts.get("2", 0),
        "max_heading_level": max((int(row["level"]) for row in headings), default=0),
        "skipped_headings": skipped_headings,
        "duplicate_heading_slugs": duplicate_slugs,
        "handoff_count": handoff_count,
        "image_count": len(images),
        "fig_alt_count": sum(1 for image in images if image.get("fig_alt")),
        "figure_boundary_count": sum(1 for image in images if image.get("figure_boundary_present") is True),
        "live_marker_leaks": live_marker_leaks,
        "raw_core_claim_marker_leak": raw_claim_marker,
        "images": images,
        "passed": passed,
    }


def inspect_key_figures(manifest: dict[str, Any], chapter_rows: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    targets = manifest.get("reader_handoff_contract", {}).get("key_figure_targets", [])
    if not isinstance(targets, list):
        errors.append("reader_handoff_contract.key_figure_targets must be a list.")
        targets = []
    chapter_text: dict[str, str] = {}
    for row in chapter_rows:
        file_value = row.get("file")
        if isinstance(file_value, str) and file_value and (ROOT / file_value).exists():
            chapter_text[file_value] = (ROOT / file_value).read_text(encoding="utf-8")

    rows: list[dict[str, Any]] = []
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            errors.append(f"key_figure_targets[{index}] must be an object.")
            continue
        figure_id = str(target.get("id", ""))
        asset = str(target.get("draft_asset_path", ""))
        reader_ref = str(target.get("reader_manuscript_ref", ""))
        if "#" in reader_ref:
            ref_file, ref_anchor = reader_ref.split("#", 1)
            ref_anchor = "#" + ref_anchor
        else:
            ref_file, ref_anchor = reader_ref, ""
        text = chapter_text.get(ref_file, "")
        asset_exists = bool(asset and (ROOT / asset).exists())
        ref_present = bool(text and ref_anchor and ref_anchor in text)
        alt_present = bool(text and ref_anchor and re.search(rf"\{{[^}}]*{re.escape(ref_anchor)}[^}}]*fig-alt=\"[^\"]+\"", text))
        boundary_present = bool(text and ref_anchor and "Figure boundary:" in text[text.find(ref_anchor) : text.find(ref_anchor) + 700])
        if not asset_exists:
            errors.append(f"{figure_id}: key-figure asset missing: {asset}.")
        if not ref_present:
            errors.append(f"{figure_id}: reader manuscript reference missing: {reader_ref}.")
        if not alt_present:
            errors.append(f"{figure_id}: reader manuscript figure missing fig-alt near {reader_ref}.")
        if not boundary_present:
            errors.append(f"{figure_id}: reader manuscript figure missing boundary paragraph near {reader_ref}.")
        rows.append(
            {
                "id": figure_id,
                "draft_asset_path": asset,
                "asset_exists": asset_exists,
                "reader_manuscript_ref": reader_ref,
                "reader_ref_present": ref_present,
                "fig_alt_present": alt_present,
                "figure_boundary_present": boundary_present,
                "passed": asset_exists and ref_present and alt_present and boundary_present,
            }
        )
    return {
        "target_count": len(targets),
        "asset_count": sum(1 for row in rows if row["asset_exists"]),
        "reader_ref_present_count": sum(1 for row in rows if row["reader_ref_present"]),
        "fig_alt_present_count": sum(1 for row in rows if row["fig_alt_present"]),
        "figure_boundary_present_count": sum(1 for row in rows if row["figure_boundary_present"]),
        "rows": rows,
    }


def observe() -> dict[str, Any]:
    errors: list[str] = []
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain an object."])
    records = chapter_records(manifest, errors)
    chapter_rows = [inspect_chapter(record, errors) for record in records]
    key_figures = inspect_key_figures(manifest, chapter_rows, errors)

    existing_rows = [row for row in chapter_rows if row.get("exists") is True]
    summary = {
        "chapter_records": len(records),
        "existing_chapter_files": len(existing_rows),
        "reconciled_records": sum(1 for record in records if record.get("reconciliation_status") == "reconciled"),
        "release_blocker_preserved_records": sum(
            1
            for record in records
            if REQUIRED_RELEASE_BLOCKERS.issubset(set(record.get("release_blockers", [])))
        ),
        "chapters_with_one_h1": sum(1 for row in existing_rows if row.get("h1_count") == 1),
        "total_headings": sum(int(row.get("heading_count", 0)) for row in existing_rows),
        "max_heading_level": max((int(row.get("max_heading_level", 0)) for row in existing_rows), default=0),
        "skipped_heading_count": sum(len(row.get("skipped_headings", [])) for row in existing_rows),
        "duplicate_heading_slug_count": sum(len(row.get("duplicate_heading_slugs", [])) for row in existing_rows),
        "handoff_sections": sum(int(row.get("handoff_count", 0)) for row in existing_rows),
        "min_h2_sections": min((int(row.get("h2_count", 0)) for row in existing_rows), default=0),
        "max_h2_sections": max((int(row.get("h2_count", 0)) for row in existing_rows), default=0),
        "min_character_count": min((int(row.get("character_count", 0)) for row in existing_rows), default=0),
        "max_character_count": max((int(row.get("character_count", 0)) for row in existing_rows), default=0),
        "image_count": sum(int(row.get("image_count", 0)) for row in existing_rows),
        "fig_alt_count": sum(int(row.get("fig_alt_count", 0)) for row in existing_rows),
        "figure_boundary_count": sum(int(row.get("figure_boundary_count", 0)) for row in existing_rows),
        "live_marker_leak_count": sum(1 for row in existing_rows if row.get("live_marker_leaks")),
        "raw_core_claim_marker_leak_count": sum(1 for row in existing_rows if row.get("raw_core_claim_marker_leak") is True),
        "key_figure_targets": key_figures["target_count"],
        "key_figure_assets_present": key_figures["asset_count"],
        "key_figure_reader_refs_present": key_figures["reader_ref_present_count"],
        "key_figure_fig_alts_present": key_figures["fig_alt_present_count"],
        "key_figure_boundaries_present": key_figures["figure_boundary_present_count"],
    }
    status = "passed_source_accessibility_navigation_review" if not errors else "failed_source_accessibility_navigation_review"
    return {
        "schema_version": "asi_stack.reader_accessibility_navigation.v0",
        "result_id": RESULT_ID,
        "status": status,
        "command": COMMAND,
        "source_manifest": rel(MANIFEST),
        "summary": summary,
        "key_figures": key_figures,
        "chapters": chapter_rows,
        "release_effect": "none",
        "support_state_effect": "none",
        "review_boundary": (
            "This source-level accessibility/navigation review checks tracked curated reader source structure, "
            "heading order, one-H1 chapter shape, handoff sections, key-figure source text alternatives, "
            "draft figure boundaries, live-scaffold leakage, raw claim-marker leakage, and preserved release "
            "blockers. It is not rendered browser review, not keyboard-only review, not screen-reader review, "
            "not WCAG conformance, not e-reader review, not audiobook review, and not reader release approval."
        ),
        "non_claims": [
            "does not certify WCAG conformance",
            "does not perform screen-reader or keyboard-only review",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
            "does not approve final figure art",
            "does not promote any chapter core claim or support state",
        ],
        "errors": errors,
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors = list(observed.get("errors", []))
    summary = observed.get("summary", {})
    expected_pairs = {
        "chapter_records": EXPECTED_CHAPTERS,
        "existing_chapter_files": EXPECTED_CHAPTERS,
        "reconciled_records": EXPECTED_CHAPTERS,
        "release_blocker_preserved_records": EXPECTED_CHAPTERS,
        "chapters_with_one_h1": EXPECTED_CHAPTERS,
        "skipped_heading_count": 0,
        "duplicate_heading_slug_count": 0,
        "handoff_sections": EXPECTED_CHAPTERS,
        "image_count": EXPECTED_KEY_FIGURES,
        "fig_alt_count": EXPECTED_KEY_FIGURES,
        "figure_boundary_count": EXPECTED_KEY_FIGURES,
        "live_marker_leak_count": 0,
        "raw_core_claim_marker_leak_count": 0,
        "key_figure_targets": EXPECTED_KEY_FIGURES,
        "key_figure_assets_present": EXPECTED_KEY_FIGURES,
        "key_figure_reader_refs_present": EXPECTED_KEY_FIGURES,
        "key_figure_fig_alts_present": EXPECTED_KEY_FIGURES,
        "key_figure_boundaries_present": EXPECTED_KEY_FIGURES,
    }
    if observed.get("status") != "passed_source_accessibility_navigation_review":
        errors.append("status must be passed_source_accessibility_navigation_review.")
    for key, expected in expected_pairs.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    if summary.get("max_heading_level", 0) > 3:
        errors.append(f"summary.max_heading_level must be at most 3; found {summary.get('max_heading_level')!r}.")
    if summary.get("min_h2_sections", 0) < 8:
        errors.append(f"summary.min_h2_sections must be at least 8; found {summary.get('min_h2_sections')!r}.")
    if summary.get("min_character_count", 0) < 10000:
        errors.append(f"summary.min_character_count must be at least 10000; found {summary.get('min_character_count')!r}.")
    for row in observed.get("chapters", []):
        if isinstance(row, dict) and row.get("passed") is not True:
            errors.append(f"{row.get('chapter_id')}: chapter accessibility/navigation row must pass.")
    for row in observed.get("key_figures", {}).get("rows", []):
        if isinstance(row, dict) and row.get("passed") is not True:
            errors.append(f"{row.get('id')}: key-figure accessibility/navigation row must pass.")
    boundary = str(observed.get("review_boundary", ""))
    for fragment in (
        "not rendered browser review",
        "not keyboard-only review",
        "not screen-reader review",
        "not WCAG conformance",
        "not e-reader review",
        "not audiobook review",
        "not reader release approval",
    ):
        if fragment not in boundary:
            errors.append(f"review_boundary missing {fragment!r}.")
    return errors


def render_review(observed: dict[str, Any]) -> str:
    summary = observed["summary"]
    return "\n".join(
        [
            "# Reader Accessibility And Navigation Review",
            "",
            "Last checked: 2026-07-04",
            "",
            "Command:",
            "",
            "```bash",
            COMMAND,
            "```",
            "",
            f"Tracked result: `{rel(RESULT)}`",
            "",
            "This CI-friendly source-level review checks the tracked curated reader manuscript for chapter navigation shape, handoff consistency, release-blocker preservation, draft key-figure text alternatives, and source-leak boundaries. It is not rendered browser review, not keyboard-only review, not screen-reader review, not WCAG conformance, not e-reader review, not audiobook review, and not reader release approval.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{observed['status']}` |",
            f"| Chapter records | {summary['chapter_records']} |",
            f"| Existing chapter files | {summary['existing_chapter_files']} |",
            f"| Reconciled records | {summary['reconciled_records']} |",
            f"| Release blockers preserved | {summary['release_blocker_preserved_records']} |",
            f"| Chapters with one H1 | {summary['chapters_with_one_h1']} |",
            f"| Total headings | {summary['total_headings']} |",
            f"| Maximum heading level | {summary['max_heading_level']} |",
            f"| Skipped heading levels | {summary['skipped_heading_count']} |",
            f"| Duplicate heading slugs | {summary['duplicate_heading_slug_count']} |",
            f"| Handoff sections | {summary['handoff_sections']} |",
            f"| H2 sections per chapter | {summary['min_h2_sections']} min / {summary['max_h2_sections']} max |",
            f"| Character count per chapter | {summary['min_character_count']} min / {summary['max_character_count']} max |",
            f"| Draft reader images | {summary['image_count']} |",
            f"| Figure alt texts | {summary['fig_alt_count']} |",
            f"| Figure boundary paragraphs | {summary['figure_boundary_count']} |",
            f"| Live-marker leaks | {summary['live_marker_leak_count']} |",
            f"| Raw core-claim marker leaks | {summary['raw_core_claim_marker_leak_count']} |",
            f"| Key-figure targets | {summary['key_figure_targets']} |",
            f"| Key-figure assets present | {summary['key_figure_assets_present']} |",
            f"| Key-figure reader refs present | {summary['key_figure_reader_refs_present']} |",
            f"| Key-figure fig-alt refs present | {summary['key_figure_fig_alts_present']} |",
            f"| Key-figure boundary refs present | {summary['key_figure_boundaries_present']} |",
            "",
            "## Gate",
            "",
            "Every curated reader chapter must exist, remain reconciled, preserve release blockers, keep exactly one H1, keep one `## Handoff` section, avoid heading-level skips and duplicate heading slugs, avoid live-book scaffold markers, and avoid raw claim-marker leakage. The ten draft reader figures must resolve to tracked SVG assets and carry `fig-alt` text plus nearby `Figure boundary:` paragraphs in the reader manuscript.",
            "",
            "## Non-Claims",
            "",
            "- This review does not certify WCAG conformance.",
            "- This review does not perform screen-reader or keyboard-only review.",
            "- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.",
            "- This review does not approve final figure art.",
            "- This review does not promote any chapter core claim or support state.",
            "",
        ]
    )


def validate_review_doc(errors: list[str]) -> None:
    if not REVIEW.exists():
        errors.append(f"Missing {rel(REVIEW)}.")
        return
    text = REVIEW.read_text(encoding="utf-8")
    for fragment in (
        "Reader Accessibility And Navigation Review",
        COMMAND,
        rel(RESULT),
        "source-level review",
        "Chapter records | 44",
        "Release blockers preserved | 44",
        "Chapters with one H1 | 44",
        "Skipped heading levels | 0",
        "Duplicate heading slugs | 0",
        "Handoff sections | 44",
        "Draft reader images | 10",
        "Figure alt texts | 10",
        "Figure boundary paragraphs | 10",
        "not keyboard-only review",
        "not screen-reader review",
        "not WCAG conformance",
        "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
    ):
        if fragment not in text:
            errors.append(f"{rel(REVIEW)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true", help="write the tracked source review manifest and doc")
    args = parser.parse_args()

    observed = observe()
    errors = validate_observed(observed)
    if args.write_result:
        RESULT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
        REVIEW.write_text(render_review(observed), encoding="utf-8")
    else:
        if not RESULT.exists():
            errors.append(f"Missing {rel(RESULT)}; run `{COMMAND} --write-result`.")
        elif load_json(RESULT) != observed:
            errors.append(f"{rel(RESULT)} is stale; run `{COMMAND} --write-result`.")
        validate_review_doc(errors)
    if errors:
        fail(errors)
    print(
        "Reader accessibility/navigation validation passed: "
        f"{observed['summary']['chapter_records']} chapters, "
        f"{observed['summary']['handoff_sections']} handoffs, "
        f"{observed['summary']['key_figure_fig_alts_present']} key-figure alt refs."
    )


if __name__ == "__main__":
    main()
