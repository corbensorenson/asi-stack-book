#!/usr/bin/env python3
"""Validate EPUB key-figure XHTML layout evidence without e-reader approval."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_epub_layout_manifest.json"
DOC = ROOT / "docs" / "reader_key_figure_epub_layout_review.md"
EPUB = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "epub" / "_reader_site" / "The-ASI-Stack.epub"
BROWSER_REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_epub_browser_review_report.json"
COMMAND = "python3 scripts/validate_reader_key_figure_epub_layout.py"
EXPECTED_VIEWPORTS = {"desktop", "ereader"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader key-figure EPUB layout validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_zip_path(path: str) -> str:
    return path.removeprefix("EPUB/")


def key_figure_rows() -> list[dict[str, Any]]:
    probe = load_json(FORMAT_PROBE)
    rows = probe.get("epub", {}).get("per_figure", [])
    if not isinstance(rows, list) or len(rows) != 10:
        fail(["key_figure_format_probe_manifest epub.per_figure must contain 10 rows."])
    result = []
    for row in rows:
        if not isinstance(row, dict):
            fail(["key_figure_format_probe_manifest epub.per_figure rows must be objects."])
        entry = str(row.get("packaged_svg_entry", ""))
        if not entry.startswith("EPUB/media/"):
            fail([f"unexpected packaged SVG entry for {row.get('id')}: {entry}"])
        result.append(
            {
                "id": str(row.get("id", "")),
                "source_svg_title": str(row.get("source_svg_title", "")),
                "packaged_svg_entry": entry,
                "packaged_svg_href": "../" + normalize_zip_path(entry),
            }
        )
    return result


def map_figure_pages(figures: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if not EPUB.exists():
        fail([f"missing curated reader EPUB artifact: {rel(EPUB)}"])
    with ZipFile(EPUB) as archive:
        xhtml_names = [name for name in archive.namelist() if name.endswith(".xhtml")]
        mapping: dict[str, dict[str, Any]] = {}
        for figure in figures:
            matches = []
            for name in xhtml_names:
                text = archive.read(name).decode("utf-8", errors="replace")
                if figure["packaged_svg_href"] in text:
                    matches.append((name, text))
            if len(matches) != 1:
                fail([f"{figure['id']}: expected exactly one EPUB XHTML page for {figure['packaged_svg_entry']}, found {[name for name, _ in matches]}."])
            name, text = matches[0]
            alt_match = re.search(rf'<img\b[^>]*src=["\']{re.escape(figure["packaged_svg_href"])}["\'][^>]*alt=["\']([^"\']+)["\']', text)
            figcaption = re.search(r"<figcaption>(.*?)</figcaption>", text, re.DOTALL)
            mapping[figure["id"]] = {
                "xhtml_entry": name,
                "has_figure_boundary": "Figure boundary:" in text,
                "has_draft_reader_aid_boundary": "draft reader aid" in text.lower(),
                "has_release_boundary": "not release-reviewed art" in text,
                "alt_text_words": len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", alt_match.group(1) if alt_match else "")),
                "figcaption": re.sub(r"\s+", " ", figcaption.group(1)).strip() if figcaption else "",
            }
    return mapping


def browser_results_by_page() -> dict[tuple[str, str], dict[str, Any]]:
    if not BROWSER_REPORT.exists():
        fail([f"missing EPUB browser review report: {rel(BROWSER_REPORT)}"])
    report = load_json(BROWSER_REPORT)
    if report.get("review_type") != "curated_reader_epub_browser_xhtml_application_review":
        fail(["EPUB browser report review_type drifted."])
    results = report.get("results", [])
    if not isinstance(results, list):
        fail(["EPUB browser report results must be a list."])
    by_key = {}
    for row in results:
        if not isinstance(row, dict):
            continue
        by_key[(str(row.get("zip_path", "")), str(row.get("viewport", "")))] = row
    return by_key


def observe() -> dict[str, Any]:
    figures = key_figure_rows()
    page_map = map_figure_pages(figures)
    browser_results = browser_results_by_page()
    rows = []
    for figure in figures:
        page = page_map[figure["id"]]
        viewport_rows = []
        for viewport in sorted(EXPECTED_VIEWPORTS):
            result = browser_results.get((page["xhtml_entry"], viewport))
            if not result:
                fail([f"{figure['id']}: browser report missing {page['xhtml_entry']} {viewport}."])
            viewport_rows.append(
                {
                    "viewport": viewport,
                    "status": result.get("status"),
                    "body_text_chars": result.get("body_text_chars"),
                    "image_count": result.get("image_count"),
                    "horizontal_overflow_px": result.get("horizontal_overflow_px"),
                    "main_visible": result.get("main_visible"),
                    "image_failures": len(result.get("image_failures", [])),
                }
            )
        rows.append(
            {
                "id": figure["id"],
                "source_svg_title": figure["source_svg_title"],
                "packaged_svg_entry": figure["packaged_svg_entry"],
                **page,
                "viewports": viewport_rows,
                "passed": (
                    page["has_figure_boundary"]
                    and page["has_draft_reader_aid_boundary"]
                    and page["has_release_boundary"]
                    and page["alt_text_words"] >= 12
                    and all(row["status"] == "passed" for row in viewport_rows)
                    and all(row["image_count"] >= 1 for row in viewport_rows)
                    and all(row["image_failures"] == 0 for row in viewport_rows)
                    and all(row["main_visible"] is True for row in viewport_rows)
                    and all(row["horizontal_overflow_px"] <= 10 for row in viewport_rows)
                    and all(row["body_text_chars"] >= 1_200 for row in viewport_rows)
                ),
            }
        )
    all_viewports = [viewport for row in rows for viewport in row["viewports"]]
    summary = {
        "figure_count": len(rows),
        "unique_xhtml_entries": len({row["xhtml_entry"] for row in rows}),
        "viewport_count": len(EXPECTED_VIEWPORTS),
        "page_view_pairs": len(all_viewports),
        "failed_page_view_pairs": sum(1 for row in all_viewports if row["status"] != "passed"),
        "minimum_body_text_chars": min(int(row["body_text_chars"]) for row in all_viewports),
        "minimum_alt_text_words": min(int(row["alt_text_words"]) for row in rows),
        "maximum_horizontal_overflow_px": max(int(row["horizontal_overflow_px"]) for row in all_viewports),
        "minimum_image_count": min(int(row["image_count"]) for row in all_viewports),
        "image_failure_count": sum(int(row["image_failures"]) for row in all_viewports),
        "figure_boundary_count": sum(1 for row in rows if row["has_figure_boundary"]),
        "release_boundary_count": sum(1 for row in rows if row["has_release_boundary"]),
    }
    return {
        "schema_version": "asi_stack.reader_key_figure_epub_layout.v0",
        "status": "passed_local_epub_key_figure_xhtml_layout_probe",
        "command": COMMAND,
        "source_format_probe": rel(FORMAT_PROBE),
        "source_browser_report": rel(BROWSER_REPORT),
        "source_epub_artifact": rel(EPUB),
        "summary": summary,
        "figures": rows,
        "release_blockers_preserved": [
            "epub_e_reader_review_not_completed",
            "final_figure_artifact_review_not_completed",
            "reader_edition_release_record_not_created",
        ],
        "non_claims": [
            "This is a local EPUB XHTML key-figure browser-report probe only.",
            "This probe is not dedicated e-reader device review and not e-reader application approval.",
            "This probe is not final figure-artifact approval and not reader release approval.",
            "This probe does not prove visual quality, accessibility adequacy, source interpretation, support-state movement, or publication readiness.",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema_version") != "asi_stack.reader_key_figure_epub_layout.v0":
        errors.append("schema_version must be asi_stack.reader_key_figure_epub_layout.v0.")
    if result.get("status") != "passed_local_epub_key_figure_xhtml_layout_probe":
        errors.append("status must be passed_local_epub_key_figure_xhtml_layout_probe.")
    summary = result.get("summary", {})
    if not isinstance(summary, dict):
        errors.append("summary must be an object.")
        summary = {}
    expected_summary = {
        "figure_count": 10,
        "unique_xhtml_entries": 10,
        "viewport_count": 2,
        "page_view_pairs": 20,
        "failed_page_view_pairs": 0,
        "maximum_horizontal_overflow_px": 10,
        "minimum_image_count": 1,
        "image_failure_count": 0,
        "figure_boundary_count": 10,
        "release_boundary_count": 10,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    thresholds = {
        "minimum_body_text_chars": 1_200,
        "minimum_alt_text_words": 12,
    }
    for key, threshold in thresholds.items():
        observed = summary.get(key)
        if not isinstance(observed, (int, float)) or observed < threshold:
            errors.append(f"summary.{key} must be at least {threshold}; found {observed!r}.")
    figures = result.get("figures", [])
    if not isinstance(figures, list) or len(figures) != 10:
        errors.append("figures must contain 10 rows.")
        figures = []
    for row in figures:
        if not isinstance(row, dict):
            errors.append("figure rows must be objects.")
            continue
        if row.get("passed") is not True:
            errors.append(f"{row.get('id')}: EPUB layout row must pass.")
        viewports = row.get("viewports", [])
        if not isinstance(viewports, list) or {item.get("viewport") for item in viewports if isinstance(item, dict)} != EXPECTED_VIEWPORTS:
            errors.append(f"{row.get('id')}: expected desktop and ereader viewport rows.")
    blockers = set(result.get("release_blockers_preserved", []))
    for blocker in (
        "epub_e_reader_review_not_completed",
        "final_figure_artifact_review_not_completed",
        "reader_edition_release_record_not_created",
    ):
        if blocker not in blockers:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in (
        "local epub xhtml key-figure browser-report probe",
        "not dedicated e-reader device review",
        "not e-reader application approval",
        "not final figure-artifact approval",
        "not reader release approval",
        "does not prove visual quality",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")
    return errors


def write_doc(result: dict[str, Any]) -> None:
    summary = result["summary"]
    lines = [
        "# Reader Key-Figure EPUB Layout Review",
        "",
        "Last checked: 2026-07-04",
        "",
        "Command:",
        "",
        "```bash",
        f"{COMMAND} --write-manifest --write-doc",
        "```",
        "",
        "This local probe combines the current ignored curated-reader EPUB package with the local Chromium EPUB XHTML browser review report. It checks the ten draft key-figure XHTML entries, their packaged SVG references, figure-boundary paragraphs, release-boundary text, alt text, and desktop/e-reader-like viewport browser results. It is not dedicated e-reader device review, not e-reader application approval, not final figure-artifact approval, and not reader release approval.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | `{result['status']}` |",
        f"| Key-figure XHTML entries | {summary['unique_xhtml_entries']} |",
        f"| Browser page-view pairs | {summary['page_view_pairs']} |",
        f"| Failed page-view pairs | {summary['failed_page_view_pairs']} |",
        f"| Minimum body text characters | {summary['minimum_body_text_chars']} |",
        f"| Minimum alt-text words | {summary['minimum_alt_text_words']} |",
        f"| Maximum horizontal overflow | {summary['maximum_horizontal_overflow_px']} px |",
        f"| Minimum image count | {summary['minimum_image_count']} |",
        f"| Image failures | {summary['image_failure_count']} |",
        f"| Figure boundaries | {summary['figure_boundary_count']} |",
        f"| Release boundaries | {summary['release_boundary_count']} |",
        "",
        "## Per-Figure XHTML Entries",
        "",
        "| Figure | XHTML entry | Alt words | Desktop overflow | E-reader overflow |",
        "|---|---|---:|---:|---:|",
    ]
    for row in result["figures"]:
        by_viewport = {item["viewport"]: item for item in row["viewports"]}
        lines.append(
            f"| `{row['id']}` | `{row['xhtml_entry']}` | {row['alt_text_words']} | {by_viewport['desktop']['horizontal_overflow_px']} px | {by_viewport['ereader']['horizontal_overflow_px']} px |"
        )
    lines.extend(
        [
            "",
            "## Residuals",
            "",
            "- This probe checks the ten key-figure XHTML entries, not a real e-reader device or app.",
            "- It does not replace dedicated e-reader review, manual visual review, or final figure-artifact approval.",
            "- Figure-artifact approval and reader release approval still require an edition release record naming exact reviewed artifacts.",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"{rel(DOC)} is missing.")
        return
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Reader Key-Figure EPUB Layout Review",
        f"{COMMAND} --write-manifest --write-doc",
        "| Key-figure XHTML entries | 10 |",
        "| Browser page-view pairs | 20 |",
        "| Failed page-view pairs | 0 |",
        "| Maximum horizontal overflow | 10 px |",
        "| Image failures | 0 |",
        "not dedicated e-reader device review",
        "not e-reader application approval",
        "not final figure-artifact approval",
        "not reader release approval",
    ]
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="inspect local EPUB/report and write the tracked manifest")
    parser.add_argument("--write-doc", action="store_true", help="rewrite the tracked markdown review doc")
    args = parser.parse_args()

    if args.write_manifest:
        result = observe()
        errors = validate_result(result)
        if errors:
            fail(errors)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run with --write-manifest."])
        result = load_json(RESULT)

    errors = validate_result(result)
    if args.write_doc:
        write_doc(result)
    validate_doc(errors)
    if errors:
        fail(errors)
    print(
        "Reader key-figure EPUB layout validation passed: "
        f"{result['summary']['unique_xhtml_entries']} XHTML entries, "
        f"{result['summary']['page_view_pairs']} page-view pairs."
    )


if __name__ == "__main__":
    main()
