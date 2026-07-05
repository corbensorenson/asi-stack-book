#!/usr/bin/env python3
"""Validate source-geometry safety for the reader key figures.

This check is deliberately CI-friendly: it parses the tracked SVG source and
checks geometry/layout invariants without requiring a rasterizer. It does not
replace rendered browser review, e-reader review, manual aesthetic review, or
final figure-artifact approval.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_geometry_manifest.json"
REVIEW = ROOT / "docs" / "reader_key_figure_geometry_review.md"
COMMAND = "python3 scripts/validate_reader_key_figure_geometry.py"
RESULT_ID = "reader-key-figure-source-geometry-2026-07-04"

EXPECTED_COUNT = 10
EXPECTED_VIEWBOX = (0.0, 0.0, 1200.0, 760.0)
MIN_VISIBLE_TEXT_NODES = 25
MIN_VISIBLE_RECTS = 7
MIN_VISIBLE_CONNECTOR_PATHS = 8
MIN_CONTENT_WIDTH_PX = 1000.0
MIN_CONTENT_HEIGHT_PX = 520.0
MIN_LEFT_MARGIN_PX = 50.0
MIN_TOP_MARGIN_PX = 50.0
MAX_RIGHT_BOUND_PX = 1175.0
MAX_BOTTOM_BOUND_PX = 740.0
MAX_TEXT_ANCHOR_X = 1070.0
MAX_TEXT_ANCHOR_Y = 740.0

EXPECTED_SUMMARY = {
    "figure_count": 10,
    "standard_viewbox_count": 10,
    "content_bounds_passed_count": 10,
    "text_anchor_bounds_passed_count": 10,
    "minimum_visible_text_nodes": 25,
    "minimum_visible_rects": 8,
    "minimum_visible_connector_paths": 8,
    "minimum_content_width_px": 1016.0,
    "minimum_content_height_px": 532.0,
    "minimum_content_edge_margin_px": 22.0,
    "maximum_text_anchor_x": 1064.0,
    "maximum_text_anchor_y": 738.0,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader key-figure geometry validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tag_name(node: ET.Element) -> str:
    return node.tag.rsplit("}", 1)[-1]


def numeric(value: str | None, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def parse_viewbox(value: str | None) -> tuple[float, float, float, float] | None:
    if not value:
        return None
    parts = value.split()
    if len(parts) != 4:
        return None
    try:
        return tuple(float(part) for part in parts)  # type: ignore[return-value]
    except ValueError:
        return None


def walk_visible(root: ET.Element) -> Iterable[ET.Element]:
    def visit(node: ET.Element, in_defs: bool = False) -> Iterable[ET.Element]:
        name = tag_name(node)
        now_in_defs = in_defs or name == "defs"
        if not now_in_defs:
            yield node
        for child in list(node):
            yield from visit(child, now_in_defs)

    yield from visit(root)


def path_numbers(value: str) -> list[float]:
    return [float(part) for part in re.findall(r"-?\d+(?:\.\d+)?", value)]


def visible_metrics(path: Path, figure_id: str, errors: list[str]) -> dict[str, Any]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{figure_id}: {rel(path)} is not parseable SVG: {exc}.")
        return {"figure_id": figure_id, "asset_path": rel(path), "passed": False}

    viewbox = parse_viewbox(root.attrib.get("viewBox"))
    visible_text_nodes = 0
    visible_rects = 0
    visible_connector_paths = 0
    xs: list[float] = []
    ys: list[float] = []
    text_xs: list[float] = []
    text_ys: list[float] = []
    visible_text = []

    for node in walk_visible(root):
        name = tag_name(node)
        if name == "rect":
            x = numeric(node.attrib.get("x"))
            y = numeric(node.attrib.get("y"))
            width = numeric(node.attrib.get("width"))
            height = numeric(node.attrib.get("height"))
            if (x, y, width, height) == EXPECTED_VIEWBOX:
                continue
            visible_rects += 1
            xs.extend([x, x + width])
            ys.extend([y, y + height])
        elif name == "path":
            visible_connector_paths += 1
            values = path_numbers(node.attrib.get("d", ""))
            for index, value in enumerate(values):
                if index % 2 == 0:
                    xs.append(value)
                else:
                    ys.append(value)
        elif name == "text":
            visible_text_nodes += 1
            x = numeric(node.attrib.get("x"))
            y = numeric(node.attrib.get("y"))
            text_xs.append(x)
            text_ys.append(y)
            xs.append(x)
            ys.append(y)
            visible_text.append(node.text or "")

    if not xs or not ys:
        errors.append(f"{figure_id}: no visible SVG geometry found.")
        return {"figure_id": figure_id, "asset_path": rel(path), "passed": False}

    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)
    text_max_x = max(text_xs) if text_xs else 0.0
    text_max_y = max(text_ys) if text_ys else 0.0
    content_width = max_x - min_x
    content_height = max_y - min_y
    edge_margin = min(min_x, min_y, EXPECTED_VIEWBOX[2] - max_x, EXPECTED_VIEWBOX[3] - max_y)

    standard_viewbox = viewbox == EXPECTED_VIEWBOX
    content_bounds_passed = (
        min_x >= MIN_LEFT_MARGIN_PX
        and min_y >= MIN_TOP_MARGIN_PX
        and max_x <= MAX_RIGHT_BOUND_PX
        and max_y <= MAX_BOTTOM_BOUND_PX
        and content_width >= MIN_CONTENT_WIDTH_PX
        and content_height >= MIN_CONTENT_HEIGHT_PX
    )
    text_anchor_bounds_passed = (
        visible_text_nodes >= MIN_VISIBLE_TEXT_NODES
        and visible_rects >= MIN_VISIBLE_RECTS
        and visible_connector_paths >= MIN_VISIBLE_CONNECTOR_PATHS
        and text_max_x <= MAX_TEXT_ANCHOR_X
        and text_max_y <= MAX_TEXT_ANCHOR_Y
    )
    visible_text_joined = " ".join(visible_text).lower()
    has_non_release_status = "draft visual asset" in visible_text_joined and "not release-reviewed" in visible_text_joined
    no_release_approval_claim = "release-approved" not in visible_text_joined

    if not standard_viewbox:
        errors.append(f"{figure_id}: viewBox must be 0 0 1200 760.")
    if not content_bounds_passed:
        errors.append(
            f"{figure_id}: content bounds failed: min=({min_x}, {min_y}) max=({max_x}, {max_y}) "
            f"size=({content_width}, {content_height})."
        )
    if not text_anchor_bounds_passed:
        errors.append(
            f"{figure_id}: text/entity bounds failed: text={visible_text_nodes}, rects={visible_rects}, "
            f"paths={visible_connector_paths}, text_max=({text_max_x}, {text_max_y})."
        )
    if not has_non_release_status:
        errors.append(f"{figure_id}: visible text must include draft visual asset and not release-reviewed status.")
    if not no_release_approval_claim:
        errors.append(f"{figure_id}: visible text must not claim release-approved status.")

    return {
        "figure_id": figure_id,
        "asset_path": rel(path),
        "viewbox": list(viewbox) if viewbox else None,
        "standard_viewbox": standard_viewbox,
        "visible_text_nodes": visible_text_nodes,
        "visible_rects": visible_rects,
        "visible_connector_paths": visible_connector_paths,
        "content_bounds": {
            "min_x": min_x,
            "min_y": min_y,
            "max_x": max_x,
            "max_y": max_y,
            "width": content_width,
            "height": content_height,
            "minimum_edge_margin": edge_margin,
        },
        "text_anchor_bounds": {
            "max_x": text_max_x,
            "max_y": text_max_y,
        },
        "content_bounds_passed": content_bounds_passed,
        "text_anchor_bounds_passed": text_anchor_bounds_passed,
        "has_non_release_status": has_non_release_status,
        "no_release_approval_claim": no_release_approval_claim,
        "passed": (
            standard_viewbox
            and content_bounds_passed
            and text_anchor_bounds_passed
            and has_non_release_status
            and no_release_approval_claim
        ),
    }


def key_figures() -> list[dict[str, Any]]:
    manifest = load_json(MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets", [])
    if not isinstance(figures, list):
        fail(["reader_handoff_contract.key_figure_targets must be a list."])
    return figures


def observe() -> dict[str, Any]:
    errors: list[str] = []
    rows: list[dict[str, Any]] = []
    for figure in key_figures():
        figure_id = str(figure.get("id", ""))
        asset = figure.get("draft_asset_path")
        if not isinstance(asset, str):
            errors.append(f"{figure_id or 'unknown'}: draft_asset_path must be a string.")
            continue
        rows.append(visible_metrics(ROOT / asset, figure_id, errors))

    summary = {
        "figure_count": len(rows),
        "standard_viewbox_count": sum(1 for row in rows if row.get("standard_viewbox") is True),
        "content_bounds_passed_count": sum(1 for row in rows if row.get("content_bounds_passed") is True),
        "text_anchor_bounds_passed_count": sum(1 for row in rows if row.get("text_anchor_bounds_passed") is True),
        "minimum_visible_text_nodes": min((row.get("visible_text_nodes", 0) for row in rows), default=0),
        "minimum_visible_rects": min((row.get("visible_rects", 0) for row in rows), default=0),
        "minimum_visible_connector_paths": min((row.get("visible_connector_paths", 0) for row in rows), default=0),
        "minimum_content_width_px": min((row.get("content_bounds", {}).get("width", 0.0) for row in rows), default=0.0),
        "minimum_content_height_px": min((row.get("content_bounds", {}).get("height", 0.0) for row in rows), default=0.0),
        "minimum_content_edge_margin_px": min(
            (row.get("content_bounds", {}).get("minimum_edge_margin", 0.0) for row in rows),
            default=0.0,
        ),
        "maximum_text_anchor_x": max((row.get("text_anchor_bounds", {}).get("max_x", 0.0) for row in rows), default=0.0),
        "maximum_text_anchor_y": max((row.get("text_anchor_bounds", {}).get("max_y", 0.0) for row in rows), default=0.0),
    }

    return {
        "schema_version": "asi_stack.reader_key_figure_geometry.v0",
        "result_id": RESULT_ID,
        "status": "passed_source_geometry_review" if not errors else "failed_source_geometry_review",
        "command": COMMAND,
        "source_manifest": rel(MANIFEST),
        "figure_count": len(rows),
        "summary": summary,
        "figures": rows,
        "release_effect": "none",
        "support_state_effect": "none",
        "review_boundary": (
            "This source-geometry review checks SVG viewBox, visible content bounds, text anchors, "
            "entity counts, and visible draft/non-release status. It is not raster review, not manual "
            "aesthetic review, not e-reader visual review, not DOCX/PDF application review, not final "
            "figure-artifact approval, and not reader release approval."
        ),
        "non_claims": [
            "does not render or raster-inspect the figures",
            "does not approve final figure art",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
            "does not prove visual quality in every target application",
            "does not promote any chapter core claim or support state",
        ],
        "errors": errors,
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors = list(observed.get("errors", []))
    if observed.get("status") != "passed_source_geometry_review":
        errors.append("status must be passed_source_geometry_review.")
    summary = observed.get("summary", {})
    for key, expected in EXPECTED_SUMMARY.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    for row in observed.get("figures", []):
        if row.get("passed") is not True:
            errors.append(f"{row.get('figure_id')}: source-geometry row must pass.")
        if row.get("has_non_release_status") is not True:
            errors.append(f"{row.get('figure_id')}: must preserve visible non-release status.")
        if row.get("no_release_approval_claim") is not True:
            errors.append(f"{row.get('figure_id')}: must not claim release approval.")
    boundary = str(observed.get("review_boundary", ""))
    for fragment in (
        "not raster review",
        "not manual aesthetic review",
        "not e-reader visual review",
        "not DOCX/PDF application review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if fragment not in boundary:
            errors.append(f"review_boundary missing {fragment!r}.")
    return errors


def render_review(observed: dict[str, Any]) -> str:
    summary = observed["summary"]
    return "\n".join(
        [
            "# Reader Key-Figure Geometry Review",
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
            "This CI-friendly source-geometry review checks the ten draft key figures for stable SVG layout bounds before final visual-art review exists. It parses the SVG source and checks the standard viewBox, visible content bounds, text-anchor bounds, entity counts, and visible draft/non-release status. It is not raster review, not manual aesthetic review, not e-reader visual review, not DOCX/PDF application review, not final figure-artifact approval, and not reader release approval.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{observed['status']}` |",
            f"| Key figures checked | {summary['figure_count']} |",
            f"| Standard viewBox count | {summary['standard_viewbox_count']} |",
            f"| Content bounds passed | {summary['content_bounds_passed_count']} |",
            f"| Text-anchor bounds passed | {summary['text_anchor_bounds_passed_count']} |",
            f"| Minimum visible text nodes | {summary['minimum_visible_text_nodes']} |",
            f"| Minimum visible rectangles | {summary['minimum_visible_rects']} |",
            f"| Minimum visible connector paths | {summary['minimum_visible_connector_paths']} |",
            f"| Minimum content width | {summary['minimum_content_width_px']} px |",
            f"| Minimum content height | {summary['minimum_content_height_px']} px |",
            f"| Minimum content edge margin | {summary['minimum_content_edge_margin_px']} px |",
            f"| Maximum text anchor x | {summary['maximum_text_anchor_x']} px |",
            f"| Maximum text anchor y | {summary['maximum_text_anchor_y']} px |",
            "",
            "## Gate",
            "",
            "Each draft key figure must keep the `0 0 1200 760` viewBox, keep visible content within the source-layout safety bounds, include at least 25 visible text nodes, 7 visible rectangles, and 8 visible connector paths, and preserve visible `draft visual asset` / `not release-reviewed` status text.",
            "",
            "## Non-Claims",
            "",
            "- This review does not render or raster-inspect the figures.",
            "- This review does not approve final figure art.",
            "- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.",
            "- This review does not prove visual quality in every target application.",
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
        "Reader Key-Figure Geometry Review",
        COMMAND,
        rel(RESULT),
        "source-geometry review",
        "Standard viewBox count | 10",
        "Content bounds passed | 10",
        "Text-anchor bounds passed | 10",
        "Minimum visible text nodes | 25",
        "Minimum content edge margin | 22.0 px",
        "not raster review",
        "not final figure-artifact approval",
        "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
    ):
        if fragment not in text:
            errors.append(f"{rel(REVIEW)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true", help="write the tracked geometry manifest and review doc")
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
        "Reader key-figure geometry validation passed: "
        f"{observed['summary']['figure_count']} figures, "
        f"{observed['summary']['content_bounds_passed_count']} content-bound checks, "
        f"{observed['summary']['minimum_content_edge_margin_px']}px minimum edge margin."
    )


if __name__ == "__main__":
    main()
