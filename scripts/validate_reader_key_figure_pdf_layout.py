#!/usr/bin/env python3
"""Validate curated-reader PDF key-figure page layout without approving release."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_pdf_layout_manifest.json"
DOC = ROOT / "docs" / "reader_key_figure_pdf_layout_review.md"
PDF = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "pdf" / "_reader_site" / "The-ASI-Stack.pdf"
COMMAND = "python3 scripts/validate_reader_key_figure_pdf_layout.py"
EXPECTED_CAPTION_PAGES = {
    "asi_stack_control_plane": 29,
    "authority_to_effect_path": 45,
    "evidence_state_ladder": 63,
    "intent_to_artifact_trace": 129,
    "context_transaction_lifecycle": 164,
    "readiness_residual_quarantine_map": 242,
    "compression_and_generation_acceptance": 263,
    "route_selection_budget_tradeoff": 296,
    "cyclic_substrate_adoption_gate": 331,
    "living_book_release_pipeline": 403,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader key-figure PDF layout validation failed:")
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


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def pdf_pages(path: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(path)], text=True)
    match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    if not match:
        fail(["pdfinfo output did not contain a Pages line."])
    return int(match.group(1))


def caption_figures() -> list[dict[str, str]]:
    probe = load_json(FORMAT_PROBE)
    rows = probe.get("pdf", {}).get("per_figure", [])
    if not isinstance(rows, list) or len(rows) != 10:
        fail(["key_figure_format_probe_manifest pdf.per_figure must contain 10 rows."])
    result = []
    for row in rows:
        if not isinstance(row, dict):
            fail(["key_figure_format_probe_manifest pdf.per_figure rows must be objects."])
        result.append({"id": str(row.get("id", "")), "caption_title": str(row.get("caption_title", ""))})
    return result


def full_text_pages(path: Path) -> list[str]:
    text = subprocess.check_output(["pdftotext", str(path), "-"], text=True, errors="replace")
    return text.split("\f")


def locate_caption_pages(figures: list[dict[str, str]], pages: list[str]) -> dict[str, int]:
    found: dict[str, int] = {}
    for figure in figures:
        needle = normalize("Draft " + figure["caption_title"])
        matches = [index for index, page in enumerate(pages, start=1) if needle in normalize(page)]
        if len(matches) != 1:
            fail([f"{figure['id']}: expected exactly one PDF caption page for {needle!r}, found {matches}."])
        found[figure["id"]] = matches[0]
    return found


def caption_bbox(path: Path, page: int, caption_title: str) -> dict[str, float]:
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
    target = normalize("Draft " + caption_title)
    for start, word in enumerate(words):
        if word[4] != "Figure":
            continue
        collected: list[tuple[float, float, float, float, str]] = []
        normalized = ""
        for candidate in words[start:]:
            collected.append(candidate)
            normalized = normalize(" ".join(item[4] for item in collected))
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
    fail([f"page {page}: could not find caption bbox for {caption_title!r}."])


def raster_metrics(path: Path, pages: list[int]) -> dict[int, dict[str, Any]]:
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - depends on local environment.
        fail([f"Pillow is required for --write-manifest PDF layout raster inspection: {exc}"])
    import numpy as np

    metrics: dict[int, dict[str, Any]] = {}
    with tempfile.TemporaryDirectory(prefix="asi-key-figure-pdf-layout-") as temp_dir:
        out = Path(temp_dir) / "page"
        for page in sorted(pages):
            subprocess.run(
                ["pdftoppm", "-png", "-r", "72", "-f", str(page), "-l", str(page), str(path), str(out)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        for png in sorted(Path(temp_dir).glob("*.png")):
            match = re.search(r"-(\d+)\.png$", png.name)
            if not match:
                fail([f"could not parse rendered page number from {png.name}."])
            page = int(match.group(1))
            image = Image.open(png).convert("RGB")
            arr = np.asarray(image)
            luminance = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
            ink = luminance < 245
            edge = 20
            near_edge = np.concatenate(
                [ink[:edge, :].ravel(), ink[-edge:, :].ravel(), ink[:, :edge].ravel(), ink[:, -edge:].ravel()]
            )
            metrics[page] = {
                "width": image.size[0],
                "height": image.size[1],
                "ink_percent": round(float(ink.mean() * 100), 2),
                "near_edge_ink_percent": round(float(near_edge.mean() * 100), 2),
                "luminance_std": round(float(luminance.std()), 2),
            }
    return metrics


def observe() -> dict[str, Any]:
    if not PDF.exists():
        fail([f"missing curated reader PDF artifact: {rel(PDF)}"])
    figures = caption_figures()
    pages = full_text_pages(PDF)
    caption_pages = locate_caption_pages(figures, pages)
    raster_by_page = raster_metrics(PDF, list(caption_pages.values()))
    rows = []
    for figure in figures:
        page = caption_pages[figure["id"]]
        bbox = caption_bbox(PDF, page, figure["caption_title"])
        raster = raster_by_page[page]
        rows.append(
            {
                "id": figure["id"],
                "caption_title": figure["caption_title"],
                "caption_page": page,
                "expected_caption_page": EXPECTED_CAPTION_PAGES.get(figure["id"]),
                "caption_bbox": bbox,
                "raster": raster,
                "passed": (
                    EXPECTED_CAPTION_PAGES.get(figure["id"]) == page
                    and bbox["margin_min_pt"] >= 72.0
                    and raster["width"] == 612
                    and raster["height"] == 792
                    and raster["ink_percent"] >= 3.0
                    and raster["near_edge_ink_percent"] <= 0.1
                    and raster["luminance_std"] >= 14.0
                ),
            }
        )
    summary = {
        "figure_count": len(rows),
        "pdf_pages": pdf_pages(PDF),
        "unique_caption_pages": len(set(caption_pages.values())),
        "raster_pages_rendered": len(raster_by_page),
        "standard_page_size_count": sum(
            1 for row in rows if row["raster"]["width"] == 612 and row["raster"]["height"] == 792
        ),
        "minimum_caption_margin_pt": min(row["caption_bbox"]["margin_min_pt"] for row in rows),
        "minimum_page_ink_percent": min(row["raster"]["ink_percent"] for row in rows),
        "maximum_near_edge_ink_percent": max(row["raster"]["near_edge_ink_percent"] for row in rows),
        "minimum_luminance_std": min(row["raster"]["luminance_std"] for row in rows),
    }
    return {
        "schema_version": "asi_stack.reader_key_figure_pdf_layout.v0",
        "status": "passed_local_pdf_key_figure_layout_probe",
        "command": COMMAND,
        "source_format_probe": rel(FORMAT_PROBE),
        "pdf_artifact": rel(PDF),
        "pdf_sha256": sha256_file(PDF),
        "summary": summary,
        "figures": rows,
        "release_blockers_preserved": [
            "pdf_page_layout_review_not_completed",
            "final_figure_artifact_review_not_completed",
            "reader_edition_release_record_not_created",
        ],
        "non_claims": [
            "This is a local PDF key-figure layout probe only.",
            "This probe is not manual page-by-page PDF review.",
            "This probe is not final figure-artifact approval and not reader release approval.",
            "This probe does not prove visual quality, accessibility adequacy, source interpretation, support-state movement, or publication readiness.",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema_version") != "asi_stack.reader_key_figure_pdf_layout.v0":
        errors.append("schema_version must be asi_stack.reader_key_figure_pdf_layout.v0.")
    if result.get("status") != "passed_local_pdf_key_figure_layout_probe":
        errors.append("status must be passed_local_pdf_key_figure_layout_probe.")
    if result.get("source_format_probe") != rel(FORMAT_PROBE):
        errors.append("source_format_probe drifted.")
    summary = result.get("summary", {})
    if not isinstance(summary, dict):
        errors.append("summary must be an object.")
        summary = {}
    expected_summary = {
        "figure_count": 10,
        "pdf_pages": 504,
        "unique_caption_pages": 10,
        "raster_pages_rendered": 10,
        "standard_page_size_count": 10,
        "maximum_near_edge_ink_percent": 0.0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    thresholds = {
        "minimum_caption_margin_pt": 72.0,
        "minimum_page_ink_percent": 3.0,
        "minimum_luminance_std": 14.0,
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
        if row.get("expected_caption_page") != EXPECTED_CAPTION_PAGES.get(figure_id):
            errors.append(f"{figure_id}: expected_caption_page drifted.")
        if row.get("caption_page") != EXPECTED_CAPTION_PAGES.get(figure_id):
            errors.append(f"{figure_id}: caption_page drifted.")
        if row.get("passed") is not True:
            errors.append(f"{figure_id}: PDF layout row must pass.")
    blockers = set(result.get("release_blockers_preserved", []))
    for blocker in (
        "pdf_page_layout_review_not_completed",
        "final_figure_artifact_review_not_completed",
        "reader_edition_release_record_not_created",
    ):
        if blocker not in blockers:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in ("not manual page-by-page pdf review", "not final figure-artifact approval", "not reader release approval", "does not prove visual quality"):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")
    return errors


def write_doc(result: dict[str, Any]) -> None:
    summary = result["summary"]
    lines = [
        "# Reader Key-Figure PDF Layout Review",
        "",
        "Last checked: 2026-07-04",
        "",
        "Command:",
        "",
        "```bash",
        f"{COMMAND} --write-manifest --write-doc",
        "```",
        "",
        "This local probe inspects the current ignored curated-reader PDF for the ten draft key-figure caption pages. It verifies exact caption pages, caption bounding-box margins, page raster dimensions, nonblank page ink, near-edge ink absence, and luminance variation. It is not manual page-by-page PDF review, not final figure-artifact approval, and not reader release approval.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Status | `{result['status']}` |",
        f"| PDF pages | {summary['pdf_pages']} |",
        f"| Key-figure caption pages | {summary['unique_caption_pages']} |",
        f"| Raster pages rendered | {summary['raster_pages_rendered']} |",
        f"| Standard page size count | {summary['standard_page_size_count']} |",
        f"| Minimum caption margin | {summary['minimum_caption_margin_pt']} pt |",
        f"| Minimum page ink | {summary['minimum_page_ink_percent']}% |",
        f"| Maximum near-edge ink | {summary['maximum_near_edge_ink_percent']}% |",
        f"| Minimum luminance standard deviation | {summary['minimum_luminance_std']} |",
        "",
        "## Per-Figure Pages",
        "",
        "| Figure | Caption page | Caption margin | Page ink | Near-edge ink | Luminance std |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in result["figures"]:
        lines.append(
            f"| `{row['id']}` | {row['caption_page']} | {row['caption_bbox']['margin_min_pt']} pt | {row['raster']['ink_percent']}% | {row['raster']['near_edge_ink_percent']}% | {row['raster']['luminance_std']} |"
        )
    lines.extend(
        [
            "",
            "## Residuals",
            "",
            "- This probe checks the ten key-figure caption pages, not every PDF page.",
            "- It does not replace manual page-by-page PDF review, PDF viewer review, or final visual approval.",
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
        "Reader Key-Figure PDF Layout Review",
        f"{COMMAND} --write-manifest --write-doc",
        "| Key-figure caption pages | 10 |",
        "| Raster pages rendered | 10 |",
        "| Minimum caption margin | 165.878 pt |",
        "| Maximum near-edge ink | 0.0% |",
        "not manual page-by-page PDF review",
        "not final figure-artifact approval",
        "not reader release approval",
    ]
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="inspect local PDF artifact and write the tracked manifest")
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
        "Reader key-figure PDF layout validation passed: "
        f"{result['summary']['unique_caption_pages']} caption pages, "
        f"minimum caption margin {result['summary']['minimum_caption_margin_pt']}pt."
    )


if __name__ == "__main__":
    main()
