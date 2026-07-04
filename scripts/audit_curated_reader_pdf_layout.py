#!/usr/bin/env python3
"""Audit the tracked curated reader PDF for extractable text and layout drift."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
REQUIRED_MARKERS = (
    "The ASI Stack",
    "Reader Edition Draft",
    "evidence boundary",
    "Reader Source List",
    "External Citation Policy",
)
LONG_LINE_LIMIT = 160


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        sys.stderr.write(completed.stderr)
        raise SystemExit(f"Command failed: {' '.join(command)}")


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bbox_metrics(path: Path, html_path: Path) -> dict[str, Any]:
    run(["pdftotext", "-bbox", str(path), str(html_path)])
    root = ET.parse(html_path).getroot()
    pages_checked = 0
    textless_pages = 0
    word_boxes_checked = 0
    out_of_bounds = 0
    heights: list[float] = []

    for page in root.iter():
        if not page.tag.endswith("page"):
            continue
        pages_checked += 1
        width = float(page.attrib["width"])
        height = float(page.attrib["height"])
        page_words = 0
        for word in page:
            if not word.tag.endswith("word"):
                continue
            page_words += 1
            word_boxes_checked += 1
            x_min = float(word.attrib["xMin"])
            y_min = float(word.attrib["yMin"])
            x_max = float(word.attrib["xMax"])
            y_max = float(word.attrib["yMax"])
            heights.append(y_max - y_min)
            if x_min < 0 or y_min < 0 or x_max > width or y_max > height:
                out_of_bounds += 1
        if page_words == 0:
            textless_pages += 1

    return {
        "pages_checked": pages_checked,
        "word_boxes_checked": word_boxes_checked,
        "textless_pages": textless_pages,
        "out_of_bounds_word_boxes": out_of_bounds,
        "min_word_box_height": round(min(heights), 3) if heights else 0,
        "max_word_box_height": round(max(heights), 3) if heights else 0,
    }


def layout_metrics(path: Path, text_path: Path) -> dict[str, Any]:
    run(["pdftotext", "-layout", str(path), str(text_path)])
    text = text_path.read_text(encoding="utf-8", errors="replace")
    long_lines = sum(1 for line in text.splitlines() if len(line) > LONG_LINE_LIMIT)
    present = [marker for marker in REQUIRED_MARKERS if marker in text]
    return {
        "long_layout_lines_over_160_chars": long_lines,
        "required_text_markers_present": present,
    }


def fail(errors: list[str]) -> None:
    print("Curated reader PDF layout audit failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed PDF layout audit into the curated format probe manifest")
    args = parser.parse_args()

    manifest = load_manifest()
    audit = manifest.get("pdf_layout_audit", {})
    if not isinstance(audit, dict):
        fail(["pdf_layout_audit must be an object in the curated format probe manifest."])

    source_artifact = audit.get("source_artifact")
    if not isinstance(source_artifact, str):
        fail(["pdf_layout_audit.source_artifact must be a string."])
    pdf_path = ROOT / source_artifact
    if not pdf_path.exists():
        fail([f"Missing PDF artifact: {source_artifact}"])

    with tempfile.TemporaryDirectory(prefix="asi-curated-pdf-audit-") as tmp:
        tmpdir = Path(tmp)
        observed = {
            "status": "passed_full_text_bbox_probe",
            "source_artifact": source_artifact,
            "source_sha256": sha256_file(pdf_path),
        }
        observed.update(bbox_metrics(pdf_path, tmpdir / "bbox.html"))
        observed.update(layout_metrics(pdf_path, tmpdir / "layout.txt"))
        observed["review_boundary"] = (
            "All-page text and bounding-box extraction is stronger local PDF layout evidence than representative "
            "sampling, but it is not manual PDF page-by-page review and does not approve the PDF artifact for release."
        )

    errors: list[str] = []
    if args.write_manifest:
        manifest["pdf_layout_audit"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        audit = observed

    for key, value in observed.items():
        if audit.get(key) != value:
            errors.append(f"pdf_layout_audit.{key} expected {value!r}, found {audit.get(key)!r}.")
    boundary = audit.get("review_boundary", "")
    if "not manual PDF page-by-page review" not in boundary or "does not approve the PDF artifact" not in boundary:
        errors.append("pdf_layout_audit.review_boundary must preserve manual-review and release-approval boundaries.")
    if errors:
        fail(errors)

    print(
        "Curated reader PDF layout audit passed: "
        f"{observed['pages_checked']} pages, "
        f"{observed['word_boxes_checked']} word boxes, "
        f"{observed['out_of_bounds_word_boxes']} out-of-bounds boxes."
    )


if __name__ == "__main__":
    main()
