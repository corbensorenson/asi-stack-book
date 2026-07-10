#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_contrast_manifest.json"
REVIEW = ROOT / "docs" / "reader_key_figure_contrast_review.md"
ARTIFACT_REVIEW = ROOT / "docs" / "reader_key_figure_artifact_review.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

COMMAND = "python3 scripts/validate_reader_key_figure_contrast.py"
RESULT_ID = "reader-key-figure-contrast-2026-07-04"
EXPECTED_COUNT = 10
TEXT_CONTRAST_MIN = 4.5
GRAPHIC_CONTRAST_MIN = 3.0
MIN_TEXT_SIZE_PX = 15.0
TEXT_COLOR_CLASSES = {"ink", "muted"}
SURFACE_CLASSES = {
    "bg",
    "panel",
    "core",
    "gate",
    "evidence",
    "risk",
    "ok",
    "deny",
    "effect",
    "abi",
    "tx",
    "bad",
    "contract",
    "work",
    "artifact",
    "residual",
    "labelBox",
    "stateBox",
    "ledger",
    "selected",
    "rejected",
    "baseline",
    "route",
    "input",
    "escrow",
    "blocked",
    "path",
    "accept",
    "reject",
    "stage",
    "hold",
    "source",
    "reader",
}
FLOW_CLASSES = {"line", "loop", "copper", "rose", "redline", "amber", "gray", "dash"}
FONT_CLASSES = {"label", "small", "tiny", "caption", "number"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader key-figure contrast validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_hex(value: str) -> str | None:
    value = value.strip().lower()
    if value.startswith("#") and re.fullmatch(r"#[0-9a-f]{3}", value):
        return "#" + "".join(ch * 2 for ch in value[1:])
    if value.startswith("#") and re.fullmatch(r"#[0-9a-f]{6}", value):
        return value
    return None


def srgb_channel(value: float) -> float:
    return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    color = hex_color.lstrip("#")
    r = srgb_channel(int(color[0:2], 16) / 255)
    g = srgb_channel(int(color[2:4], 16) / 255)
    b = srgb_channel(int(color[4:6], 16) / 255)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground: str, background: str) -> float:
    fg = luminance(foreground)
    bg = luminance(background)
    high = max(fg, bg)
    low = min(fg, bg)
    return (high + 0.05) / (low + 0.05)


def parse_style(root: ET.Element) -> dict[str, dict[str, str]]:
    style_text = "\n".join(node.text or "" for node in root.iter() if node.tag.endswith("style"))
    rules: dict[str, dict[str, str]] = {}
    for match in re.finditer(r"\.([A-Za-z0-9_-]+)\s*\{([^}]*)\}", style_text):
        class_name = match.group(1)
        body = match.group(2)
        properties: dict[str, str] = {}
        for declaration in body.split(";"):
            if ":" not in declaration:
                continue
            key, value = declaration.split(":", 1)
            properties[key.strip()] = value.strip()
        rules[class_name] = properties
    return rules


def class_tokens(value: str | None) -> list[str]:
    if not value:
        return []
    return [token for token in re.split(r"\s+", value.strip()) if token]


def style_color(rules: dict[str, dict[str, str]], class_name: str, field: str) -> str | None:
    value = rules.get(class_name, {}).get(field)
    return normalize_hex(value) if value else None


def font_size_px(rules: dict[str, dict[str, str]], class_name: str) -> float | None:
    value = rules.get(class_name, {}).get("font-size")
    if not value:
        return None
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)px", value)
    if not match:
        return None
    return float(match.group(1))


def marker_fill_colors(root: ET.Element) -> list[str]:
    colors: list[str] = []
    for node in root.iter():
        if not node.tag.endswith("path"):
            continue
        color = normalize_hex(node.attrib.get("fill", ""))
        if color:
            colors.append(color)
    return sorted(set(colors))


def min_ratio(pairs: list[tuple[str, str]]) -> float:
    if not pairs:
        return 0.0
    return min(contrast_ratio(fg, bg) for fg, bg in pairs)


def rounded(value: float) -> float:
    return round(value, 2)


def analyze_figure(figure: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    asset = str(figure.get("draft_asset_path", ""))
    figure_id = str(figure.get("id", ""))
    path = ROOT / asset
    owner = figure_id or asset
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{owner}: {rel(path)} is not parseable SVG: {exc}.")
        return {"figure_id": figure_id, "asset_path": asset, "passed": False}

    rules = parse_style(root)
    surface_colors: dict[str, str] = {}
    for class_name in SURFACE_CLASSES:
        color = style_color(rules, class_name, "fill")
        if color:
            surface_colors[class_name] = color
    if "bg" not in surface_colors or "panel" not in surface_colors:
        errors.append(f"{owner}: SVG must define bg and panel fills for contrast checks.")

    text_colors: dict[str, str] = {}
    for class_name in TEXT_COLOR_CLASSES:
        color = style_color(rules, class_name, "fill")
        if color:
            text_colors[class_name] = color
        else:
            errors.append(f"{owner}: missing text color class .{class_name}.")

    text_elements = [node for node in root.iter() if node.tag.endswith("text")]
    text_color_classes_used: set[str] = set()
    font_classes_used: set[str] = set()
    for node in text_elements:
        tokens = set(class_tokens(node.attrib.get("class")))
        color_hits = tokens & TEXT_COLOR_CLASSES
        font_hits = tokens & FONT_CLASSES
        if len(color_hits) != 1:
            errors.append(f"{owner}: text node {node.text!r} must use exactly one text color class.")
        else:
            text_color_classes_used.update(color_hits)
        if not font_hits:
            errors.append(f"{owner}: text node {node.text!r} must use a font-size class.")
        font_classes_used.update(font_hits)

    font_sizes: dict[str, float] = {}
    for class_name in font_classes_used:
        size = font_size_px(rules, class_name)
        if size is None:
            errors.append(f"{owner}: font class .{class_name} must define px font-size.")
        else:
            font_sizes[class_name] = size
            if size < MIN_TEXT_SIZE_PX:
                errors.append(f"{owner}: font class .{class_name} is {size}px below {MIN_TEXT_SIZE_PX}px.")

    text_pairs = [
        (text_colors[text_class], surface_color)
        for text_class in sorted(text_color_classes_used)
        for surface_class, surface_color in sorted(surface_colors.items())
        if text_class in text_colors and surface_class in SURFACE_CLASSES
    ]
    text_min = min_ratio(text_pairs)
    if text_min and text_min < TEXT_CONTRAST_MIN:
        errors.append(f"{owner}: minimum text contrast {text_min:.2f} is below {TEXT_CONTRAST_MIN:.1f}.")

    flow_colors: dict[str, str] = {}
    for class_name in FLOW_CLASSES:
        color = style_color(rules, class_name, "stroke")
        if color:
            flow_colors[class_name] = color
    flow_pairs = [
        (flow_color, surface_colors[surface_class])
        for flow_color in flow_colors.values()
        for surface_class in ("bg", "panel")
        if surface_class in surface_colors
    ]
    flow_min = min_ratio(flow_pairs)
    if flow_colors and flow_min < GRAPHIC_CONTRAST_MIN:
        errors.append(f"{owner}: minimum flow-line contrast {flow_min:.2f} is below {GRAPHIC_CONTRAST_MIN:.1f}.")

    marker_colors = marker_fill_colors(root)
    marker_pairs = [
        (marker_color, surface_colors[surface_class])
        for marker_color in marker_colors
        for surface_class in ("bg", "panel")
        if surface_class in surface_colors
    ]
    marker_min = min_ratio(marker_pairs)
    if marker_colors and marker_min < GRAPHIC_CONTRAST_MIN:
        errors.append(f"{owner}: minimum marker contrast {marker_min:.2f} is below {GRAPHIC_CONTRAST_MIN:.1f}.")

    return {
        "figure_id": figure_id,
        "asset_path": asset,
        "text_color_classes_checked": sorted(text_color_classes_used),
        "surface_classes_checked": sorted(surface_colors),
        "flow_classes_checked": sorted(flow_colors),
        "marker_color_count": len(marker_colors),
        "minimum_text_contrast_ratio": rounded(text_min),
        "minimum_flow_line_contrast_ratio": rounded(flow_min),
        "minimum_marker_contrast_ratio": rounded(marker_min),
        "minimum_font_size_px": min(font_sizes.values()) if font_sizes else 0,
        "text_contrast_threshold": TEXT_CONTRAST_MIN,
        "graphic_contrast_threshold": GRAPHIC_CONTRAST_MIN,
        "minimum_font_size_threshold_px": MIN_TEXT_SIZE_PX,
        "passed": True,
    }


def build_expected(errors: list[str]) -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets")
    if not isinstance(figures, list) or len(figures) != EXPECTED_COUNT:
        errors.append(f"Expected {EXPECTED_COUNT} key figure target records.")
        figures = []

    figure_results: list[dict[str, Any]] = []
    for figure in figures:
        if not isinstance(figure, dict):
            errors.append("Key figure target record must be an object.")
            continue
        asset = figure.get("draft_asset_path")
        if not isinstance(asset, str):
            errors.append("Key figure target missing draft_asset_path.")
            continue
        path = ROOT / asset
        if not path.exists():
            errors.append(f"Missing key figure asset {asset}.")
            continue
        figure_results.append(analyze_figure(figure, errors))

    text_min = min((record["minimum_text_contrast_ratio"] for record in figure_results), default=0)
    flow_min = min((record["minimum_flow_line_contrast_ratio"] for record in figure_results), default=0)
    marker_min = min((record["minimum_marker_contrast_ratio"] for record in figure_results), default=0)
    font_min = min((record["minimum_font_size_px"] for record in figure_results), default=0)
    return {
        "schema_version": "asi_stack.reader_key_figure_contrast.v0",
        "result_id": RESULT_ID,
        "recorded_date": "2026-07-04",
        "command": COMMAND,
        "figure_count": len(figure_results),
        "all_figures_passed": len(figure_results) == EXPECTED_COUNT and not errors,
        "thresholds": {
            "text_contrast_minimum": TEXT_CONTRAST_MIN,
            "graphic_contrast_minimum": GRAPHIC_CONTRAST_MIN,
            "minimum_text_size_px": MIN_TEXT_SIZE_PX,
        },
        "summary": {
            "minimum_text_contrast_ratio": rounded(text_min),
            "minimum_flow_line_contrast_ratio": rounded(flow_min),
            "minimum_marker_contrast_ratio": rounded(marker_min),
            "minimum_font_size_px": font_min,
        },
        "figure_results": figure_results,
        "release_effect": "none",
        "support_state_effect": "none",
        "residuals": [
            "This is a deterministic source-level SVG contrast and readability gate, not a human visual-art review.",
            "EPUB, DOCX, PDF, e-reader, and audio artifacts still need application-level review before release approval.",
            "The figures remain draft reader aids until an edition release record names exact reviewed artifacts.",
        ],
        "non_claims": [
            "does not approve final figure art",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or HTML release artifacts",
            "does not prove any ASI Stack claim",
            "does not promote any chapter core claim",
        ],
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_surfaces(expected: dict[str, Any], errors: list[str]) -> None:
    result_path = rel(RESULT)
    surfaces = {
        rel(REVIEW): (
            REVIEW,
            [
                COMMAND,
                result_path,
                "minimum text contrast ratio",
                "does not approve final figure art",
                "not a release approval",
            ],
        ),
        rel(ARTIFACT_REVIEW): (
            ARTIFACT_REVIEW,
            [
                "measured contrast review",
                COMMAND,
                result_path,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "measured contrast/readability gate",
                result_path,
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add reader key-figure contrast gate",
                COMMAND,
                result_path,
            ],
        ),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "validate_reader_key_figure_contrast.py",
                result_path,
            ],
        ),
    }
    for owner, (path, fragments) in surfaces.items():
        if not path.exists():
            errors.append(f"Missing {owner}.")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            require_fragment(owner, text, fragment, errors)

    review_text = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else ""
    for record in expected.get("figure_results", []):
        asset = record.get("asset_path")
        figure_id = record.get("figure_id")
        if asset:
            require_fragment(rel(REVIEW), review_text, str(asset), errors)
        if figure_id:
            require_fragment(rel(REVIEW), review_text, str(figure_id), errors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_expected(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(expected, errors)
    if errors:
        fail(errors)
    summary = expected["summary"]
    print(
        "Reader key-figure contrast validation passed: "
        f"{expected['figure_count']} figure(s), "
        f"minimum text contrast {summary['minimum_text_contrast_ratio']}, "
        f"minimum flow-line contrast {summary['minimum_flow_line_contrast_ratio']}, "
        f"minimum marker contrast {summary['minimum_marker_contrast_ratio']}, "
        f"minimum text size {summary['minimum_font_size_px']}px."
    )


if __name__ == "__main__":
    main()
