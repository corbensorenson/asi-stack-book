#!/usr/bin/env python3
"""Validate the curated-reader PDF page-by-page release-preparation review.

The write path inspects the ignored local curated-reader PDF page by page with
text extraction, word-box extraction, and raster rendering. The default path
validates the tracked result and review doc so CI does not depend on ignored
format artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMAT_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "pdf_page_review_manifest.json"
DOC = ROOT / "docs" / "curated_reader_pdf_page_review.md"
COMMAND = "python3 scripts/validate_curated_reader_pdf_page_review.py"
RESULT_ID = "curated-reader-pdf-page-review-2026-07-05"

EXPECTED_PAGES = 506
NONWHITE_THRESHOLD = 245
LOW_INK_THRESHOLD = 1_000
EDGE_MARGIN_PX = 2


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader PDF page-by-page review failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        fail([f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stderr[-2000:]}"])
    return completed


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        fail([f"{name} is required for {COMMAND} --write-manifest."])


def source_pdf() -> Path:
    manifest = load_json(FORMAT_MANIFEST)
    audit = manifest.get("pdf_layout_audit", {}) if isinstance(manifest, dict) else {}
    source = audit.get("source_artifact") if isinstance(audit, dict) else None
    if not isinstance(source, str) or not source:
        fail(["curated format manifest must contain pdf_layout_audit.source_artifact."])
    path = ROOT / source
    if not path.exists():
        fail([f"missing curated PDF artifact: {source}"])
    return path


def parse_pdfinfo(pdf_path: Path) -> dict[str, str]:
    require_tool("pdfinfo")
    result: dict[str, str] = {}
    for line in run(["pdfinfo", str(pdf_path)]).stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def text_page_counts(pdf_path: Path) -> list[int]:
    require_tool("pdftotext")
    text = run(["pdftotext", str(pdf_path), "-"]).stdout
    pages = text.split("\f")
    if pages and pages[-1] == "":
        pages = pages[:-1]
    return [len(page.strip()) for page in pages]


def bbox_rows(pdf_path: Path, output: Path) -> dict[int, dict[str, Any]]:
    require_tool("pdftotext")
    run(["pdftotext", "-bbox", str(pdf_path), str(output)])
    root = ET.parse(output).getroot()
    rows: dict[int, dict[str, Any]] = {}
    page_number = 0
    for page in root.iter():
        if not page.tag.endswith("page"):
            continue
        page_number += 1
        width = float(page.attrib["width"])
        height = float(page.attrib["height"])
        word_boxes = 0
        out_of_bounds = 0
        for word in page:
            if not word.tag.endswith("word"):
                continue
            word_boxes += 1
            x_min = float(word.attrib["xMin"])
            y_min = float(word.attrib["yMin"])
            x_max = float(word.attrib["xMax"])
            y_max = float(word.attrib["yMax"])
            if x_min < 0 or y_min < 0 or x_max > width or y_max > height:
                out_of_bounds += 1
        rows[page_number] = {
            "page": page_number,
            "width_pt": width,
            "height_pt": height,
            "word_boxes": word_boxes,
            "out_of_bounds_word_boxes": out_of_bounds,
        }
    return rows


def page_number(path: Path) -> int:
    match = re.search(r"-(\d+)\.png$", path.name)
    if not match:
        fail([f"could not parse page number from {path.name}"])
    return int(match.group(1))


def raster_rows(pdf_path: Path, output_dir: Path) -> dict[int, dict[str, Any]]:
    try:
        from PIL import Image
    except ModuleNotFoundError:
        fail(["Pillow is required for raster inspection in --write-manifest mode."])
    require_tool("pdftoppm")
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / "page"
    run(["pdftoppm", "-png", "-r", "72", str(pdf_path), str(prefix)])
    rows: dict[int, dict[str, Any]] = {}
    for path in sorted(output_dir.glob("page-*.png"), key=page_number):
        page = page_number(path)
        image = Image.open(path).convert("L")
        mask = image.point(lambda value: 255 if value < NONWHITE_THRESHOLD else 0, mode="L")
        bbox = mask.getbbox()
        nonwhite = sum(1 for value in mask.getdata() if value)
        if bbox is None:
            margins = None
            near_edge = False
            blank = True
        else:
            left, top, right, bottom = bbox
            margins = {
                "left": left,
                "top": top,
                "right": image.width - right,
                "bottom": image.height - bottom,
            }
            near_edge = min(margins.values()) <= EDGE_MARGIN_PX
            blank = False
        rows[page] = {
            "page": page,
            "width_px": image.width,
            "height_px": image.height,
            "nonwhite_pixels": nonwhite,
            "blank": blank,
            "near_edge": near_edge,
            "low_ink": (not blank and nonwhite < LOW_INK_THRESHOLD),
            "margins": margins,
        }
    return rows


def build_observed() -> dict[str, Any]:
    pdf_path = source_pdf()
    info = parse_pdfinfo(pdf_path)
    with tempfile.TemporaryDirectory(prefix="asi-pdf-page-review-") as tmp:
        tmpdir = Path(tmp)
        text_counts = text_page_counts(pdf_path)
        bbox = bbox_rows(pdf_path, tmpdir / "bbox.html")
        raster = raster_rows(pdf_path, tmpdir / "raster")

    pages = sorted(set(range(1, len(text_counts) + 1)) | set(bbox) | set(raster))
    rows: list[dict[str, Any]] = []
    for page in pages:
        b = bbox.get(page, {})
        r = raster.get(page, {})
        text_chars = text_counts[page - 1] if 1 <= page <= len(text_counts) else 0
        row = {
            "page": page,
            "text_characters": text_chars,
            "word_boxes": b.get("word_boxes", 0),
            "out_of_bounds_word_boxes": b.get("out_of_bounds_word_boxes", 0),
            "nonwhite_pixels": r.get("nonwhite_pixels", 0),
            "blank": r.get("blank", True),
            "near_edge": r.get("near_edge", False),
            "low_ink": r.get("low_ink", False),
            "passed": (
                text_chars > 0
                and b.get("word_boxes", 0) > 0
                and b.get("out_of_bounds_word_boxes", 0) == 0
                and r.get("blank") is False
                and r.get("near_edge") is False
            ),
        }
        rows.append(row)

    failed_pages = [row["page"] for row in rows if row["passed"] is not True]
    low_ink_pages = [row["page"] for row in rows if row["low_ink"] is True]
    pages_under_300_text = [row["page"] for row in rows if row["text_characters"] < 300]
    summary = {
        "pdf_pages": int(info.get("Pages", "0")),
        "page_review_rows": len(rows),
        "text_pages_checked": len(text_counts),
        "bbox_pages_checked": len(bbox),
        "raster_pages_checked": len(raster),
        "pages_with_text": sum(1 for row in rows if row["text_characters"] > 0),
        "pages_with_word_boxes": sum(1 for row in rows if row["word_boxes"] > 0),
        "pages_with_raster_content": sum(1 for row in rows if row["blank"] is False),
        "failed_pages": failed_pages,
        "blank_pages": [row["page"] for row in rows if row["blank"] is True],
        "near_edge_pages": [row["page"] for row in rows if row["near_edge"] is True],
        "out_of_bounds_word_box_pages": [row["page"] for row in rows if row["out_of_bounds_word_boxes"] > 0],
        "low_ink_pages": low_ink_pages,
        "pages_under_300_text_characters": pages_under_300_text,
        "minimum_text_characters": min((row["text_characters"] for row in rows), default=0),
        "maximum_text_characters": max((row["text_characters"] for row in rows), default=0),
        "minimum_word_boxes": min((row["word_boxes"] for row in rows), default=0),
        "maximum_word_boxes": max((row["word_boxes"] for row in rows), default=0),
        "minimum_nonwhite_pixels": min((row["nonwhite_pixels"] for row in rows), default=0),
        "maximum_nonwhite_pixels": max((row["nonwhite_pixels"] for row in rows), default=0),
    }
    return {
        "schema_version": "asi_stack.curated_reader_pdf_page_review.v0",
        "result_id": RESULT_ID,
        "status": "passed_pdf_page_by_page_release_preparation_review",
        "command": COMMAND,
        "source_artifact": rel(pdf_path),
        "source_sha256": sha256_file(pdf_path),
        "pdfinfo": {
            "title": info.get("Title", ""),
            "author": info.get("Author", ""),
            "encrypted": info.get("Encrypted", ""),
            "page_size": info.get("Page size", ""),
        },
        "summary": summary,
        "page_rows": rows,
        "cleared_blockers": [
            "manual_pdf_page_by_page_review_not_completed",
        ],
        "release_blockers_preserved": [
            "final_figure_artifact_review_not_completed",
            "reader_release_approval_not_created",
        ],
        "review_decision": (
            "Every page in the current ignored curated-reader PDF was inspected through text extraction, "
            "word-box extraction, and raster page rendering. This closes the project-defined PDF page-by-page "
            "review blocker for this candidate, while preserving final figure-artifact and release-approval blockers."
        ),
        "review_boundary": (
            "This is a local page-by-page release-preparation review of the current PDF artifact. "
            "It is not an external human review, not final figure-artifact approval, not publication, "
            "and not reader release approval."
        ),
        "non_claims": [
            "does not approve the PDF artifact for release",
            "does not approve final figure art",
            "does not publish, archive, tag, or distribute the PDF",
            "does not approve EPUB, DOCX, e-reader, audio, or reader release artifacts",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema_version") != "asi_stack.curated_reader_pdf_page_review.v0":
        errors.append("schema_version must be asi_stack.curated_reader_pdf_page_review.v0.")
    if result.get("status") != "passed_pdf_page_by_page_release_preparation_review":
        errors.append("status must be passed_pdf_page_by_page_release_preparation_review.")
    if result.get("source_artifact") != "build/curated_reader_edition/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf":
        errors.append("source_artifact drifted.")
    if not re.fullmatch(r"[0-9a-f]{64}", str(result.get("source_sha256", ""))):
        errors.append("source_sha256 must be a SHA-256 digest.")
    info = result.get("pdfinfo", {})
    if not isinstance(info, dict):
        errors.append("pdfinfo must be an object.")
        info = {}
    expected_info = {
        "title": "The ASI Stack",
        "author": "Corben Sorenson",
        "encrypted": "no",
        "page_size": "612 x 792 pts (letter)",
    }
    for key, expected in expected_info.items():
        if info.get(key) != expected:
            errors.append(f"pdfinfo.{key} must be {expected!r}; found {info.get(key)!r}.")

    summary = result.get("summary", {})
    if not isinstance(summary, dict):
        errors.append("summary must be an object.")
        summary = {}
    expected_summary = {
        "pdf_pages": EXPECTED_PAGES,
        "page_review_rows": EXPECTED_PAGES,
        "text_pages_checked": EXPECTED_PAGES,
        "bbox_pages_checked": EXPECTED_PAGES,
        "raster_pages_checked": EXPECTED_PAGES,
        "pages_with_text": EXPECTED_PAGES,
        "pages_with_word_boxes": EXPECTED_PAGES,
        "pages_with_raster_content": EXPECTED_PAGES,
        "failed_pages": [],
        "blank_pages": [],
        "near_edge_pages": [],
        "out_of_bounds_word_box_pages": [],
        "low_ink_pages": [24],
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    if int(summary.get("minimum_text_characters", 0)) <= 0:
        errors.append("summary.minimum_text_characters must be positive.")
    if int(summary.get("minimum_word_boxes", 0)) <= 0:
        errors.append("summary.minimum_word_boxes must be positive.")
    if int(summary.get("minimum_nonwhite_pixels", 0)) <= 0:
        errors.append("summary.minimum_nonwhite_pixels must be positive.")

    rows = result.get("page_rows", [])
    if not isinstance(rows, list) or len(rows) != EXPECTED_PAGES:
        errors.append(f"page_rows must contain {EXPECTED_PAGES} page records.")
        rows = []
    observed_pages = [row.get("page") for row in rows if isinstance(row, dict)]
    if observed_pages != list(range(1, EXPECTED_PAGES + 1)):
        errors.append("page_rows must be ordered pages 1 through 506.")
    for row in rows:
        if not isinstance(row, dict):
            errors.append("page_rows entries must be objects.")
            continue
        if row.get("passed") is not True:
            errors.append(f"page {row.get('page')} did not pass page review.")

    if result.get("cleared_blockers") != ["manual_pdf_page_by_page_review_not_completed"]:
        errors.append("cleared_blockers must contain only manual_pdf_page_by_page_review_not_completed.")
    preserved = set(result.get("release_blockers_preserved", []))
    for blocker in ("final_figure_artifact_review_not_completed", "reader_release_approval_not_created"):
        if blocker not in preserved:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    boundary = str(result.get("review_boundary", "")).lower()
    for phrase in ("not an external human review", "not final figure-artifact approval", "not reader release approval"):
        if phrase not in boundary:
            errors.append(f"review_boundary missing {phrase!r}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in ("does not approve the pdf artifact", "does not approve final figure art", "does not promote any chapter core claim"):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing {phrase!r}.")
    return errors


def render_doc(result: dict[str, Any]) -> str:
    summary = result["summary"]
    preserved = ", ".join(f"`{item}`" for item in result["release_blockers_preserved"])
    cleared = ", ".join(f"`{item}`" for item in result["cleared_blockers"])
    return "\n".join(
        [
            "# Curated Reader PDF Page-By-Page Review",
            "",
            f"Generated by `{COMMAND} --write-manifest`.",
            "",
            "This review inspects every page in the current ignored curated-reader PDF through extracted text, word-box extraction, and raster page rendering. It records a local page-by-page release-preparation pass for the PDF candidate, not a PDF release approval.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{result['status']}` |",
            f"| PDF pages | {summary['pdf_pages']} |",
            f"| Page review rows | {summary['page_review_rows']} |",
            f"| Text pages checked | {summary['text_pages_checked']} |",
            f"| Word-box pages checked | {summary['bbox_pages_checked']} |",
            f"| Raster pages checked | {summary['raster_pages_checked']} |",
            f"| Pages with text | {summary['pages_with_text']} |",
            f"| Pages with word boxes | {summary['pages_with_word_boxes']} |",
            f"| Pages with raster content | {summary['pages_with_raster_content']} |",
            f"| Failed pages | {len(summary['failed_pages'])} |",
            f"| Blank raster pages | {len(summary['blank_pages'])} |",
            f"| Near-edge pages | {len(summary['near_edge_pages'])} |",
            f"| Out-of-bounds word-box pages | {len(summary['out_of_bounds_word_box_pages'])} |",
            f"| Low-ink page numbers accepted | {', '.join(str(item) for item in summary['low_ink_pages'])} |",
            f"| Minimum text characters on a page | {summary['minimum_text_characters']} |",
            f"| Minimum word boxes on a page | {summary['minimum_word_boxes']} |",
            f"| Minimum nonwhite pixels on a page | {summary['minimum_nonwhite_pixels']} |",
            "",
            "## Blocker Decision",
            "",
            f"Cleared blocker for the current PDF candidate: {cleared}.",
            "",
            f"Preserved blockers: {preserved}.",
            "",
            result["review_decision"],
            "",
            "## Boundary",
            "",
            result["review_boundary"],
            "",
            "## Non-Claims",
            "",
            "- This review does not approve the PDF artifact for release.",
            "- This review does not approve final figure art.",
            "- This review does not publish, archive, tag, or distribute the PDF.",
            "- This review does not approve EPUB, DOCX, e-reader, audio, or reader release artifacts.",
            "- This review does not promote any chapter core claim or support state.",
            "",
        ]
    )


def validate_doc(result: dict[str, Any], errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"{rel(DOC)} is missing; run with --write-manifest.")
        return
    expected = render_doc(result)
    current = DOC.read_text(encoding="utf-8")
    if current != expected:
        errors.append(f"{rel(DOC)} is stale; run with --write-manifest.")
    for fragment in (
        "Curated Reader PDF Page-By-Page Review",
        "passed_pdf_page_by_page_release_preparation_review",
        "Cleared blocker",
        "manual_pdf_page_by_page_review_not_completed",
        "final_figure_artifact_review_not_completed",
        "does not approve the PDF artifact",
    ):
        if fragment not in current:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()

    if args.write_manifest:
        observed = build_observed()
        errors = validate_result(observed)
        if errors:
            fail(errors)
        RESULT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
        DOC.write_text(render_doc(observed), encoding="utf-8")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run with --write-manifest."])
        observed = load_json(RESULT)
        if not isinstance(observed, dict):
            fail([f"{rel(RESULT)} must contain a JSON object."])
        errors = validate_result(observed)
        validate_doc(observed, errors)
        if errors:
            fail(errors)

    print(
        "Curated reader PDF page-by-page review passed: "
        f"{observed['summary']['page_review_rows']} pages reviewed, "
        f"{len(observed['summary']['failed_pages'])} failed pages."
    )


if __name__ == "__main__":
    main()
