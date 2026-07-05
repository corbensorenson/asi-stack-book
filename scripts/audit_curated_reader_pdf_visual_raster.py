#!/usr/bin/env python3
"""Audit curated-reader PDF raster rendering without approving release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
DEFAULT_DPI = 72
NONWHITE_THRESHOLD = 245
EDGE_MARGIN_PX = 2
LOW_INK_THRESHOLD = 1000
PAGE_RE = re.compile(r"-(\d+)\.png$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader PDF visual raster audit failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        fail([f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stderr[-2000:]}"])


def page_number(path: Path) -> int:
    match = PAGE_RE.search(path.name)
    if not match:
        fail([f"could not parse rendered PDF page number from {path.name}"])
    return int(match.group(1))


def render_pdf(pdf_path: Path, output_dir: Path, dpi: int) -> list[Path]:
    if shutil.which("pdftoppm") is None:
        fail(["pdftoppm is required for PDF visual raster audit."])
    prefix = output_dir / "page"
    run(["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), str(prefix)])
    return sorted(output_dir.glob("page-*.png"), key=page_number)


def inspect_page(path: Path) -> dict[str, Any]:
    page = page_number(path)
    image = Image.open(path).convert("L")
    mask = image.point(lambda value: 255 if value < NONWHITE_THRESHOLD else 0, mode="L")
    bbox = mask.getbbox()
    nonwhite_pixels = sum(1 for value in mask.getdata() if value)
    if bbox is None:
        return {
            "page": page,
            "width": image.width,
            "height": image.height,
            "nonwhite_pixels": 0,
            "blank": True,
            "margins": None,
            "near_edge": False,
        }
    left, top, right, bottom = bbox
    margins = {
        "left": left,
        "top": top,
        "right": image.width - right,
        "bottom": image.height - bottom,
    }
    return {
        "page": page,
        "width": image.width,
        "height": image.height,
        "nonwhite_pixels": nonwhite_pixels,
        "blank": False,
        "margins": margins,
        "near_edge": min(margins.values()) <= EDGE_MARGIN_PX,
    }


def observe(dpi: int) -> dict[str, Any]:
    manifest = load_manifest()
    pdf_audit = manifest.get("pdf_layout_audit", {})
    if not isinstance(pdf_audit, dict):
        fail(["curated format manifest must contain pdf_layout_audit before visual raster audit."])
    source_artifact = pdf_audit.get("source_artifact")
    if not isinstance(source_artifact, str) or not source_artifact:
        fail(["pdf_layout_audit.source_artifact must be present before visual raster audit."])
    pdf_path = ROOT / source_artifact
    if not pdf_path.exists():
        fail([f"Missing PDF artifact: {source_artifact}"])

    with tempfile.TemporaryDirectory(prefix="asi-curated-pdf-raster-") as temp_dir:
        page_paths = render_pdf(pdf_path, Path(temp_dir), dpi)
        pages = [inspect_page(path) for path in page_paths]

    if not pages:
        fail(["pdftoppm produced no page PNGs."])

    widths = sorted({page["width"] for page in pages})
    heights = sorted({page["height"] for page in pages})
    blank_pages = [page["page"] for page in pages if page["blank"]]
    low_ink_pages = [
        page["page"]
        for page in pages
        if not page["blank"] and page["nonwhite_pixels"] < LOW_INK_THRESHOLD
    ]
    near_edge_pages = [page["page"] for page in pages if page["near_edge"]]
    nonwhite_counts = [page["nonwhite_pixels"] for page in pages]
    margins = [page["margins"] for page in pages if page["margins"] is not None]

    return {
        "status": "passed_all_page_pdf_raster_probe",
        "source_artifact": source_artifact,
        "source_sha256": sha256_file(pdf_path),
        "raster_dpi": dpi,
        "nonwhite_threshold": NONWHITE_THRESHOLD,
        "edge_margin_px": EDGE_MARGIN_PX,
        "low_ink_threshold": LOW_INK_THRESHOLD,
        "pages_rendered": len(pages),
        "page_width_pixels": widths,
        "page_height_pixels": heights,
        "blank_pages": len(blank_pages),
        "low_ink_pages": len(low_ink_pages),
        "near_edge_content_pages": len(near_edge_pages),
        "min_nonwhite_pixels": min(nonwhite_counts),
        "max_nonwhite_pixels": max(nonwhite_counts),
        "min_left_margin_px": min(item["left"] for item in margins),
        "min_top_margin_px": min(item["top"] for item in margins),
        "min_right_margin_px": min(item["right"] for item in margins),
        "min_bottom_margin_px": min(item["bottom"] for item in margins),
        "sample_low_ink_pages": low_ink_pages[:10],
        "sample_near_edge_pages": near_edge_pages[:10],
        "review_boundary": (
            "All-page low-resolution raster rendering is stronger local PDF visual evidence than sample-page "
            "rendering alone, but it is not manual PDF page-by-page review and does not approve the PDF artifact for release."
        ),
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_exact = {
        "raster_dpi": DEFAULT_DPI,
        "nonwhite_threshold": NONWHITE_THRESHOLD,
        "edge_margin_px": EDGE_MARGIN_PX,
        "low_ink_threshold": LOW_INK_THRESHOLD,
        "pages_rendered": 507,
        "page_width_pixels": [612],
        "page_height_pixels": [792],
        "blank_pages": 0,
        "low_ink_pages": 1,
        "near_edge_content_pages": 0,
        "min_nonwhite_pixels": 681,
        "max_nonwhite_pixels": 143139,
        "min_left_margin_px": 82,
        "min_top_margin_px": 71,
        "min_right_margin_px": 47,
        "min_bottom_margin_px": 92,
        "sample_low_ink_pages": [24],
        "sample_near_edge_pages": [],
    }
    for key, expected in expected_exact.items():
        if observed.get(key) != expected:
            errors.append(f"PDF raster audit expected {key}={expected!r}, found {observed.get(key)!r}.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed PDF raster audit into the curated format probe manifest")
    args = parser.parse_args()

    manifest = load_manifest()
    observed = observe(DEFAULT_DPI)
    if args.write_manifest:
        manifest["pdf_visual_raster_audit"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        errors = validate_observed(observed)
        if errors:
            fail(errors)
        recorded = manifest.get("pdf_visual_raster_audit")
        if recorded != observed:
            fail(["curated_format_probe_manifest.json pdf_visual_raster_audit is stale; run `python3 scripts/audit_curated_reader_pdf_visual_raster.py --write-manifest`."])

    print(
        "Curated reader PDF visual raster audit passed: "
        f"{observed['pages_rendered']} pages, "
        f"{observed['blank_pages']} blank pages, "
        f"{observed['near_edge_content_pages']} near-edge pages."
    )


if __name__ == "__main__":
    main()
