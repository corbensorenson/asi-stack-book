#!/usr/bin/env python3
"""Validate DOCX-derived key-figure page layout without approving release."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import validate_reader_key_figure_pdf_layout as pdf_layout  # noqa: E402

RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_docx_layout_manifest.json"
DOC = ROOT / "docs" / "reader_key_figure_docx_layout_review.md"
DOCX = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "docx" / "_reader_site" / "The-ASI-Stack.docx"
COMMAND = "python3 scripts/validate_reader_key_figure_docx_layout.py"
EXPECTED_TITLE_PAGES = {
    "asi_stack_control_plane": 4,
    "authority_to_effect_path": 21,
    "evidence_state_ladder": 39,
    "intent_to_artifact_trace": 106,
    "context_transaction_lifecycle": 142,
    "readiness_residual_quarantine_map": 223,
    "compression_and_generation_acceptance": 246,
    "route_selection_budget_tradeoff": 282,
    "cyclic_substrate_adoption_gate": 319,
    "living_book_release_pipeline": 393,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader key-figure DOCX layout validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_docx_review_module():
    # This module imports Pillow for page-raster inspection. Keep it out of the
    # normal tracked-manifest validation path so CI does not need Pillow here.
    from scripts import validate_curated_reader_docx_libreoffice_review as docx_review

    return docx_review


def figure_title_bbox(path: Path, page: int, caption_title: str) -> dict[str, float]:
    text = subprocess.check_output(
        ["pdftotext", "-bbox", "-f", str(page), "-l", str(page), str(path), "-"],
        text=True,
        errors="replace",
    )
    words: list[tuple[float, float, float, float, str]] = []
    for match in re.finditer(
        r'<word xMin="([^"]+)" yMin="([^"]+)" xMax="([^"]+)" yMax="([^"]+)">([^<]*)</word>',
        text,
    ):
        words.append((*map(float, match.groups()[:4]), html.unescape(match.group(5))))
    target = pdf_layout.normalize("Draft " + caption_title)
    for start, word in enumerate(words):
        if pdf_layout.normalize(word[4]) != "draft":
            continue
        collected: list[tuple[float, float, float, float, str]] = []
        for candidate in words[start : start + 12]:
            collected.append(candidate)
            normalized = pdf_layout.normalize(" ".join(item[4] for item in collected))
            if target in normalized:
                xs = [item[0] for item in collected] + [item[2] for item in collected]
                ys = [item[1] for item in collected] + [item[3] for item in collected]
                min_x, min_y, max_x, max_y = min(xs), min(ys), max(xs), max(ys)
                return {
                    "x_min": round(min_x, 3),
                    "y_min": round(min_y, 3),
                    "x_max": round(max_x, 3),
                    "y_max": round(max_y, 3),
                    "margin_min_pt": round(min(min_x, min_y, 612 - max_x, 792 - max_y), 3),
                }
    fail([f"page {page}: could not find DOCX-converted figure title for {caption_title!r}."])


def observe() -> dict[str, Any]:
    docx_review = load_docx_review_module()
    if not DOCX.exists():
        fail([f"missing curated reader DOCX artifact: {rel(DOCX)}"])
    soffice_paths = docx_review.candidate_soffice_paths()
    if not soffice_paths:
        fail(["LibreOffice/soffice is required for --write-manifest DOCX layout inspection."])
    soffice = soffice_paths[0]
    figures = pdf_layout.caption_figures()
    with tempfile.TemporaryDirectory(prefix="asi-key-figure-docx-layout-") as temp_dir:
        temp_root = Path(temp_dir)
        converted_pdf = docx_review.convert_docx_to_pdf(soffice, temp_root)
        text_pages = pdf_layout.full_text_pages(converted_pdf)
        title_pages = pdf_layout.locate_caption_pages(figures, text_pages)
        raster_by_page = pdf_layout.raster_metrics(converted_pdf, list(title_pages.values()))
        converted_pdf_pages = pdf_layout.pdf_pages(converted_pdf)
        converted_pdf_sha = docx_review.sha256_file(converted_pdf)

        rows = []
        for figure in figures:
            page = title_pages[figure["id"]]
            bbox = figure_title_bbox(converted_pdf, page, figure["caption_title"])
            raster = raster_by_page[page]
            rows.append(
                {
                    "id": figure["id"],
                    "caption_title": figure["caption_title"],
                    "title_page": page,
                    "expected_title_page": EXPECTED_TITLE_PAGES.get(figure["id"]),
                    "title_bbox": bbox,
                    "raster": raster,
                    "passed": (
                        EXPECTED_TITLE_PAGES.get(figure["id"]) == page
                        and bbox["margin_min_pt"] >= 72.0
                        and raster["width"] == 612
                        and raster["height"] == 792
                        and raster["ink_percent"] >= 9.0
                        and raster["near_edge_ink_percent"] <= 0.1
                        and raster["luminance_std"] >= 37.0
                    ),
                }
            )
    summary = {
        "figure_count": len(rows),
        "docx_converted_pdf_pages": converted_pdf_pages,
        "unique_title_pages": len(set(title_pages.values())),
        "raster_pages_rendered": len(raster_by_page),
        "standard_page_size_count": sum(
            1 for row in rows if row["raster"]["width"] == 612 and row["raster"]["height"] == 792
        ),
        "minimum_title_margin_pt": min(row["title_bbox"]["margin_min_pt"] for row in rows),
        "minimum_page_ink_percent": min(row["raster"]["ink_percent"] for row in rows),
        "maximum_near_edge_ink_percent": max(row["raster"]["near_edge_ink_percent"] for row in rows),
        "minimum_luminance_std": min(row["raster"]["luminance_std"] for row in rows),
    }
    return {
        "schema_version": "asi_stack.reader_key_figure_docx_layout.v0",
        "status": "passed_local_docx_key_figure_layout_probe",
        "command": COMMAND,
        "source_docx_artifact": rel(DOCX),
        "source_docx_sha256": docx_review.sha256_file(DOCX),
        "conversion_engine": "LibreOffice headless Writer PDF export",
        "converter_version": docx_review.soffice_version(soffice),
        "converted_pdf_sha256": converted_pdf_sha,
        "summary": summary,
        "figures": rows,
        "release_blockers_preserved": [
            "docx_application_review_not_completed",
            "final_figure_artifact_review_not_completed",
            "reader_edition_release_record_not_created",
        ],
        "non_claims": [
            "This is a local DOCX-to-PDF key-figure layout probe only.",
            "This probe is not Word review, not LibreOffice GUI review, not Google Docs review, and not manual document review.",
            "This probe is not final figure-artifact approval and not reader release approval.",
            "This probe does not prove visual quality, accessibility adequacy, source interpretation, support-state movement, or publication readiness.",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema_version") != "asi_stack.reader_key_figure_docx_layout.v0":
        errors.append("schema_version must be asi_stack.reader_key_figure_docx_layout.v0.")
    if result.get("status") != "passed_local_docx_key_figure_layout_probe":
        errors.append("status must be passed_local_docx_key_figure_layout_probe.")
    summary = result.get("summary", {})
    if not isinstance(summary, dict):
        errors.append("summary must be an object.")
        summary = {}
    expected_summary = {
        "figure_count": 10,
        "docx_converted_pdf_pages": 503,
        "unique_title_pages": 10,
        "raster_pages_rendered": 10,
        "standard_page_size_count": 10,
        "minimum_title_margin_pt": 72.1,
        "maximum_near_edge_ink_percent": 0.0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    thresholds = {
        "minimum_page_ink_percent": 9.0,
        "minimum_luminance_std": 37.0,
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
        figure_id = str(row.get("id", ""))
        if row.get("expected_title_page") != EXPECTED_TITLE_PAGES.get(figure_id):
            errors.append(f"{figure_id}: expected_title_page drifted.")
        if row.get("title_page") != EXPECTED_TITLE_PAGES.get(figure_id):
            errors.append(f"{figure_id}: title_page drifted.")
        if row.get("passed") is not True:
            errors.append(f"{figure_id}: DOCX layout row must pass.")
    blockers = set(result.get("release_blockers_preserved", []))
    for blocker in (
        "docx_application_review_not_completed",
        "final_figure_artifact_review_not_completed",
        "reader_edition_release_record_not_created",
    ):
        if blocker not in blockers:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in (
        "local docx-to-pdf key-figure layout probe",
        "not word review",
        "not libreoffice gui review",
        "not google docs review",
        "not manual document review",
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
        "# Reader Key-Figure DOCX Layout Review",
        "",
        "Last checked: 2026-07-04",
        "",
        "Command:",
        "",
        "```bash",
        f"{COMMAND} --write-manifest --write-doc",
        "```",
        "",
        "This local probe converts the current ignored curated-reader DOCX through LibreOffice headless Writer PDF export, then inspects the ten draft key-figure title pages in the converted PDF. It verifies exact title pages, title bounding-box margins, page raster dimensions, nonblank page ink, near-edge ink absence, and luminance variation. It is not Word review, not LibreOffice GUI review, not Google Docs review, not manual document review, not final figure-artifact approval, and not reader release approval.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | `{result['status']}` |",
        f"| Converted PDF pages | {summary['docx_converted_pdf_pages']} |",
        f"| Key-figure title pages | {summary['unique_title_pages']} |",
        f"| Raster pages rendered | {summary['raster_pages_rendered']} |",
        f"| Standard page size count | {summary['standard_page_size_count']} |",
        f"| Minimum title margin | {summary['minimum_title_margin_pt']} pt |",
        f"| Minimum page ink | {summary['minimum_page_ink_percent']}% |",
        f"| Maximum near-edge ink | {summary['maximum_near_edge_ink_percent']}% |",
        f"| Minimum luminance standard deviation | {summary['minimum_luminance_std']} |",
        "",
        "## Per-Figure Pages",
        "",
        "| Figure | Title page | Title margin | Page ink | Near-edge ink | Luminance std |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in result["figures"]:
        lines.append(
            f"| `{row['id']}` | {row['title_page']} | {row['title_bbox']['margin_min_pt']} pt | {row['raster']['ink_percent']}% | {row['raster']['near_edge_ink_percent']}% | {row['raster']['luminance_std']} |"
        )
    lines.extend(
        [
            "",
            "## Residuals",
            "",
            "- This probe checks the ten key-figure title pages in the LibreOffice-converted DOCX PDF, not every document page.",
            "- It does not replace Word review, LibreOffice GUI review, Google Docs review, manual document review, or final visual approval.",
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
        "Reader Key-Figure DOCX Layout Review",
        f"{COMMAND} --write-manifest --write-doc",
        "| Key-figure title pages | 10 |",
        "| Raster pages rendered | 10 |",
        "| Minimum title margin | 72.1 pt |",
        "| Maximum near-edge ink | 0.0% |",
        "not Word review",
        "not LibreOffice GUI review",
        "not Google Docs review",
        "not manual document review",
        "not final figure-artifact approval",
        "not reader release approval",
    ]
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="convert local DOCX artifact and write the tracked manifest")
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
        "Reader key-figure DOCX layout validation passed: "
        f"{result['summary']['unique_title_pages']} title pages, "
        f"minimum title margin {result['summary']['minimum_title_margin_pt']}pt."
    )


if __name__ == "__main__":
    main()
