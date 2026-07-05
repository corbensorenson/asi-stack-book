#!/usr/bin/env python3
"""Render the curated-reader DOCX through LibreOffice and record review evidence.

This is a local application-engine review of the ignored curated-reader DOCX.
It is stronger than inspecting the DOCX package XML alone, but it is not Word,
LibreOffice GUI, Google Docs, manual document review, or release approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
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
DOCX = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "docx" / "_reader_site" / "The-ASI-Stack.docx"
REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_docx_libreoffice_review_report.json"
COMMAND = "python3 scripts/validate_curated_reader_docx_libreoffice_review.py --write-manifest"
DEFAULT_DPI = 72
NONWHITE_THRESHOLD = 245
EDGE_MARGIN_PX = 2
LOW_INK_THRESHOLD = 1000
PAGE_RE = re.compile(r"-(\d+)\.png$")
RAW_CORE_CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]")
REQUIRED_MARKERS = (
    "The ASI Stack",
    "Reader Edition Draft",
    "evidence boundary",
    "Reader Source List",
    "External Citation Policy",
)
LIVE_ONLY_MARKERS = (
    "Chapter status",
    "Drafting guardrail",
    "Codex test plan",
    "Source crosswalk",
    "Claim-source mapping status",
    "Formalization hooks",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader DOCX LibreOffice review failed:")
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


def candidate_soffice_paths() -> list[str]:
    paths: list[str] = []
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            paths.append(found)
    bundled = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "bin"
        / "soffice"
    )
    if bundled.exists():
        paths.append(str(bundled))
    return list(dict.fromkeys(paths))


def run(command: list[str], *, cwd: Path = ROOT, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)


def soffice_version(soffice: str) -> str:
    completed = run([soffice, "--version"], timeout=60)
    if completed.returncode:
        return "unknown"
    return completed.stdout.strip() or completed.stderr.strip() or "unknown"


def convert_docx_to_pdf(soffice: str, temp_root: Path) -> Path:
    output_dir = temp_root / "pdf"
    profile_dir = temp_root / "lo-profile"
    output_dir.mkdir()
    profile_dir.mkdir()
    command = [
        soffice,
        f"-env:UserInstallation=file://{profile_dir}",
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--nodefault",
        "--nolockcheck",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(DOCX),
    ]
    completed = run(command, timeout=300)
    if completed.returncode:
        fail(
            [
                "LibreOffice DOCX conversion failed "
                f"({completed.returncode}): {completed.stderr[-2000:] or completed.stdout[-2000:]}"
            ]
        )
    pdf_path = output_dir / "The-ASI-Stack.pdf"
    if not pdf_path.exists():
        candidates = sorted(output_dir.glob("*.pdf"))
        if candidates:
            pdf_path = candidates[0]
        else:
            fail(["LibreOffice conversion produced no PDF."])
    return pdf_path


def parse_pdfinfo(pdf_path: Path) -> dict[str, str]:
    if shutil.which("pdfinfo") is None:
        fail(["pdfinfo is required for DOCX LibreOffice review."])
    completed = run(["pdfinfo", str(pdf_path)], timeout=60)
    if completed.returncode:
        fail([f"pdfinfo failed: {completed.stderr[-2000:]}"])
    result: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def pdftotext(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        fail(["pdftotext is required for DOCX LibreOffice review."])
    completed = run(["pdftotext", str(pdf_path), "-"], timeout=120)
    if completed.returncode:
        fail([f"pdftotext failed: {completed.stderr[-2000:]}"])
    return completed.stdout


def page_number(path: Path) -> int:
    match = PAGE_RE.search(path.name)
    if not match:
        fail([f"could not parse rendered page number from {path.name}"])
    return int(match.group(1))


def raster_pages(pdf_path: Path, output_dir: Path, dpi: int) -> list[Path]:
    if shutil.which("pdftoppm") is None:
        fail(["pdftoppm is required for DOCX LibreOffice review."])
    output_dir.mkdir()
    prefix = output_dir / "page"
    completed = run(["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), str(prefix)], timeout=240)
    if completed.returncode:
        fail([f"pdftoppm failed: {completed.stderr[-2000:]}"])
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


def observe() -> dict[str, Any]:
    if not DOCX.exists():
        fail([f"Missing DOCX artifact: {rel(DOCX)}. Run `python3 scripts/render_curated_reader_formats.py --formats docx` first."])
    soffice_paths = candidate_soffice_paths()
    if not soffice_paths:
        fail(["LibreOffice/soffice is required for DOCX LibreOffice review."])
    soffice = soffice_paths[0]
    version = soffice_version(soffice)

    with tempfile.TemporaryDirectory(prefix="asi-curated-docx-lo-") as temp_dir:
        temp_root = Path(temp_dir)
        pdf_path = convert_docx_to_pdf(soffice, temp_root)
        info = parse_pdfinfo(pdf_path)
        text = pdftotext(pdf_path)
        pages = [inspect_page(path) for path in raster_pages(pdf_path, temp_root / "pages", DEFAULT_DPI)]

    if not pages:
        fail(["LibreOffice-converted PDF raster pass produced no pages."])

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
    marker_hits = {marker: marker in text for marker in REQUIRED_MARKERS}
    live_marker_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in text]
    raw_claim_hits = bool(RAW_CORE_CLAIM_RE.search(text))

    return {
        "status": "passed_docx_libreoffice_headless_pdf_review",
        "source_artifact": rel(DOCX),
        "source_sha256": sha256_file(DOCX),
        "report_ref": rel(REPORT),
        "review_command": COMMAND,
        "converter": "LibreOffice headless Writer PDF export",
        "converter_executable": os.path.basename(soffice),
        "converter_version": version,
        "converted_pdf_pages": int(info.get("Pages", "0")),
        "converted_pdf_file_size_bytes": int(info.get("File size", "0").split()[0]),
        "converted_pdf_title": info.get("Title", ""),
        "converted_pdf_author": info.get("Author", ""),
        "converted_pdf_creator": info.get("Creator", ""),
        "converted_pdf_producer": info.get("Producer", ""),
        "converted_pdf_tagged": info.get("Tagged", ""),
        "converted_pdf_encrypted": info.get("Encrypted", ""),
        "converted_pdf_page_size": info.get("Page size", ""),
        "converted_pdf_version": info.get("PDF version", ""),
        "text_characters_checked": len(text),
        "required_text_markers_present": [
            marker for marker, present in marker_hits.items() if present
        ],
        "live_marker_hits": len(live_marker_hits),
        "raw_core_claim_marker_hits": int(raw_claim_hits),
        "raster_dpi": DEFAULT_DPI,
        "nonwhite_threshold": NONWHITE_THRESHOLD,
        "edge_margin_px": EDGE_MARGIN_PX,
        "low_ink_threshold": LOW_INK_THRESHOLD,
        "pages_raster_rendered": len(pages),
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
        "sample_blank_pages": blank_pages[:10],
        "sample_low_ink_pages": low_ink_pages[:10],
        "sample_near_edge_pages": near_edge_pages[:10],
        "review_boundary": (
            "LibreOffice headless Writer PDF export is stronger local DOCX application-engine "
            "evidence than package inspection alone, but it is not Word review, not LibreOffice GUI "
            "review, not Google Docs review, not manual document review, and does not approve the DOCX artifact."
        ),
        "non_claims": [
            "does not approve the DOCX artifact for release",
            "does not replace Word, LibreOffice GUI, or Google Docs application review",
            "does not publish or archive a reader artifact",
            "does not approve EPUB, PDF, e-reader, audio, or final figure artifacts",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_exact = {
        "status": "passed_docx_libreoffice_headless_pdf_review",
        "source_artifact": "build/curated_reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx",
        "converted_pdf_pages": 505,
        "converted_pdf_title": "The ASI Stack",
        "converted_pdf_author": "Corben Sorenson",
        "converted_pdf_creator": "Writer",
        "converted_pdf_tagged": "yes",
        "converted_pdf_encrypted": "no",
        "converted_pdf_page_size": "612 x 792 pts (letter)",
        "raster_dpi": DEFAULT_DPI,
        "nonwhite_threshold": NONWHITE_THRESHOLD,
        "edge_margin_px": EDGE_MARGIN_PX,
        "low_ink_threshold": LOW_INK_THRESHOLD,
        "pages_raster_rendered": 505,
        "page_width_pixels": [612],
        "page_height_pixels": [792],
        "blank_pages": 0,
        "low_ink_pages": 0,
        "near_edge_content_pages": 0,
        "min_nonwhite_pixels": 10476,
        "max_nonwhite_pixels": 140565,
        "min_left_margin_px": 66,
        "min_top_margin_px": 72,
        "min_right_margin_px": 72,
        "min_bottom_margin_px": 72,
        "sample_blank_pages": [],
        "sample_low_ink_pages": [],
        "sample_near_edge_pages": [],
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
    }
    for key, expected in expected_exact.items():
        if observed.get(key) != expected:
            errors.append(f"DOCX LibreOffice review expected {key}={expected!r}, found {observed.get(key)!r}.")
    if not re.fullmatch(r"[0-9a-f]{64}", str(observed.get("source_sha256", ""))):
        errors.append("source_sha256 must be a SHA-256 digest.")
    if observed.get("converted_pdf_file_size_bytes", 0) < 8_000_000:
        errors.append("converted_pdf_file_size_bytes is unexpectedly small.")
    if observed.get("text_characters_checked", 0) < 1_000_000:
        errors.append("text_characters_checked is unexpectedly small.")
    producer = str(observed.get("converted_pdf_producer", ""))
    if "LibreOffice" not in producer:
        errors.append("converted_pdf_producer must identify LibreOffice.")
    missing = sorted(set(REQUIRED_MARKERS) - set(observed.get("required_text_markers_present", [])))
    if missing:
        errors.append(f"missing required text marker(s): {missing}.")
    boundary = str(observed.get("review_boundary", ""))
    if "not Word review" not in boundary or "does not approve the DOCX artifact" not in boundary:
        errors.append("review_boundary must preserve Word/GUI/Docs and release-approval boundaries.")
    non_claim_text = " ".join(str(item) for item in observed.get("non_claims", [])).lower()
    for phrase in (
        "does not approve the docx artifact",
        "does not replace word, libreoffice gui, or google docs",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed review into the curated format probe manifest")
    args = parser.parse_args()

    manifest = load_manifest()
    observed = observe()
    report = {
        "schema_version": "0.1",
        "review_type": "curated_reader_docx_libreoffice_headless_pdf_review",
        "manifest": observed,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    errors = validate_observed(observed)
    if errors:
        fail(errors)

    if args.write_manifest:
        commands = manifest.setdefault("source_commands", [])
        if COMMAND not in commands:
            commands.append(COMMAND)
        refs = manifest.setdefault("local_report_refs", [])
        if rel(REPORT) not in refs:
            refs.append(rel(REPORT))
        manifest["docx_libreoffice_review"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        recorded = manifest.get("docx_libreoffice_review")
        if recorded != observed:
            fail(
                [
                    "curated_format_probe_manifest.json docx_libreoffice_review is stale; "
                    "run `python3 scripts/validate_curated_reader_docx_libreoffice_review.py --write-manifest`."
                ]
            )

    print(
        "Curated reader DOCX LibreOffice review passed: "
        f"{observed['converted_pdf_pages']} converted pages, "
        f"{observed['blank_pages']} blank raster pages, "
        f"{observed['near_edge_content_pages']} near-edge pages."
    )


if __name__ == "__main__":
    main()
