#!/usr/bin/env python3
"""Validate source-level reader visual identity without approving final art."""

from __future__ import annotations

import argparse
from collections import Counter
import colorsys
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STYLES = ROOT / "assets" / "styles.scss"
DIAGRAMS = ROOT / "assets" / "diagrams"
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
CONTRAST_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_contrast_manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "visual_identity_manifest.json"
REVIEW = ROOT / "docs" / "reader_visual_identity_review.md"
COMMAND = "python3 scripts/validate_reader_visual_identity.py"
RESULT_ID = "reader-visual-identity-source-review-2026-07-04"

EXPECTED_STYLE_VARIABLES = {
    "--asi-border",
    "--asi-ink",
    "--asi-muted",
    "--asi-accent",
    "--asi-copper",
    "--asi-soft",
    "--asi-figure-bg",
    "--asi-figure-rule",
    "--asi-figure-shadow",
}
STYLE_FRAGMENT_GROUPS = {
    "key_figure_shell": [
        ".asi-key-figure,",
        '.quarto-figure[id^="reader-fig-"]',
        "border-top: 3px solid var(--asi-accent);",
        "box-shadow: var(--asi-figure-shadow);",
        "overflow-x: auto;",
    ],
    "key_figure_images": [
        ".asi-key-figure img,",
        'quarto-figure[id^="reader-fig-"] img',
        "border: 1px solid var(--asi-figure-rule);",
        "background: #ffffff;",
    ],
    "reading_mode": [
        ".asi-reading-mode",
        'button[aria-pressed="true"]',
        'html[data-asi-reading-mode="human"]',
        ".asi-support-boundary-human",
    ],
    "mobile_behavior": [
        "@media (max-width: 640px)",
        "min-width: 42rem;",
        "width: 100%;",
    ],
    "print_behavior": [
        "@media print",
        "break-inside: avoid;",
        "page-break-inside: avoid;",
        "max-height: 7.4in;",
    ],
    "overflow_and_accessibility": [
        ".asi-sr-only",
        "overflow-wrap: anywhere;",
        "table {",
        "overflow-x: auto;",
        "word-break: break-word;",
    ],
}
EXPECTED_FIGURE_COUNT = 10
EXPECTED_CSS_COLOR_COUNT = 18
EXPECTED_SVG_COLOR_COUNT = 56
EXPECTED_COMBINED_COLOR_COUNT = 67
EXPECTED_COLOR_FAMILIES = {
    "neutral": 33,
    "teal-blue": 20,
    "purple": 4,
    "green": 4,
    "rose-red": 2,
    "copper-amber": 4,
}
EXPECTED_CONTRAST_SUMMARY = {
    "minimum_text_contrast_ratio": 5.19,
    "minimum_flow_line_contrast_ratio": 3.96,
    "minimum_marker_contrast_ratio": 3.96,
    "minimum_font_size_px": 15.0,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader visual identity validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def colors_in(text: str) -> set[str]:
    values: set[str] = set()
    for value in re.findall(r"#[0-9a-fA-F]{3,6}", text):
        value = value.lower()
        if len(value) == 4:
            value = "#" + "".join(ch * 2 for ch in value[1:])
        values.add(value)
    return values


def color_family(hex_color: str) -> str:
    value = hex_color.lstrip("#")
    r = int(value[0:2], 16) / 255
    g = int(value[2:4], 16) / 255
    b = int(value[4:6], 16) / 255
    if max(r, g, b) - min(r, g, b) < 0.08:
        return "neutral"
    hue = colorsys.rgb_to_hsv(r, g, b)[0] * 360
    if 160 <= hue < 230:
        return "teal-blue"
    if 20 <= hue < 70:
        return "copper-amber"
    if 80 <= hue < 160:
        return "green"
    if hue >= 330 or hue < 20:
        return "rose-red"
    if 230 <= hue < 300:
        return "purple"
    return "other"


def key_figure_assets() -> list[Path]:
    manifest = load_json(READER_MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets", [])
    if not isinstance(figures, list):
        fail(["reader_handoff_contract.key_figure_targets must be a list."])
    assets: list[Path] = []
    for figure in figures:
        if not isinstance(figure, dict):
            fail(["key_figure_targets entries must be objects."])
        asset = figure.get("draft_asset_path")
        if not isinstance(asset, str):
            fail(["key_figure_targets entries must include draft_asset_path."])
        assets.append(ROOT / asset)
    return assets


def inspect_figures(paths: list[Path], errors: list[str]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    counts = Counter()
    svg_colors: set[str] = set()
    for path in paths:
        if not path.exists():
            errors.append(f"Missing key figure asset: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        svg_colors.update(colors_in(text))
        checks = {
            "role_img": 'role="img"' in text,
            "aria_labelledby_title_desc": 'aria-labelledby="title desc"' in text,
            "title_id": '<title id="title">' in text,
            "desc_id": '<desc id="desc">' in text,
            "standard_viewbox": 'viewBox="0 0 1200 760"' in text,
            "draft_visual_boundary": "draft visual asset" in text,
            "not_release_reviewed_boundary": "not release-reviewed" in text,
        }
        for key, passed in checks.items():
            counts[key] += int(passed)
            if not passed:
                errors.append(f"{rel(path)} missing visual identity check: {key}")
        rows.append(
            {
                "asset_path": rel(path),
                "hex_color_count": len(colors_in(text)),
                **checks,
            }
        )
    return {
        "figure_count": len(paths),
        "figure_rows": rows,
        "svg_color_count": len(svg_colors),
        "svg_accessibility_counts": dict(counts),
    }


def observe() -> dict[str, Any]:
    errors: list[str] = []
    style_text = STYLES.read_text(encoding="utf-8")
    css_colors = colors_in(style_text)
    figure_paths = key_figure_assets()
    figure_summary = inspect_figures(figure_paths, errors)
    svg_colors: set[str] = set()
    for path in figure_paths:
        if path.exists():
            svg_colors.update(colors_in(path.read_text(encoding="utf-8")))
    combined_colors = css_colors | svg_colors
    style_variables = sorted(set(re.findall(r"--asi-[A-Za-z0-9_-]+", style_text)))
    style_groups: dict[str, dict[str, Any]] = {}
    for group, fragments in STYLE_FRAGMENT_GROUPS.items():
        missing = [fragment for fragment in fragments if fragment not in style_text]
        if missing:
            errors.append(f"assets/styles.scss missing {group} fragment(s): {missing}")
        style_groups[group] = {
            "fragments_checked": len(fragments),
            "missing_fragments": missing,
        }
    contrast = load_json(CONTRAST_MANIFEST)
    contrast_summary = contrast.get("summary", {}) if isinstance(contrast, dict) else {}
    color_families = dict(sorted(Counter(color_family(color) for color in combined_colors).items()))

    missing_variables = sorted(EXPECTED_STYLE_VARIABLES - set(style_variables))
    if missing_variables:
        errors.append(f"assets/styles.scss missing visual identity variables: {missing_variables}")

    return {
        "schema_version": "asi_stack.reader_visual_identity.v0",
        "result_id": RESULT_ID,
        "status": "passed_source_level_visual_identity_review" if not errors else "failed_source_level_visual_identity_review",
        "command": COMMAND,
        "source_files": [
            rel(STYLES),
            rel(READER_MANIFEST),
            rel(CONTRAST_MANIFEST),
            "assets/diagrams/*.svg",
        ],
        "style_summary": {
            "style_variables_checked": sorted(EXPECTED_STYLE_VARIABLES),
            "style_variable_count": len(style_variables),
            "missing_style_variables": missing_variables,
            "fragment_groups": style_groups,
        },
        "palette_summary": {
            "css_hex_color_count": len(css_colors),
            "svg_hex_color_count": figure_summary["svg_color_count"],
            "combined_hex_color_count": len(combined_colors),
            "combined_color_family_counts": color_families,
            "dominant_family": max(color_families, key=color_families.get) if color_families else "",
            "non_neutral_family_count": len([key for key, count in color_families.items() if key != "neutral" and count > 0]),
        },
        "figure_source_summary": {
            "figure_count": figure_summary["figure_count"],
            "standard_viewbox_count": figure_summary["svg_accessibility_counts"].get("standard_viewbox", 0),
            "role_img_count": figure_summary["svg_accessibility_counts"].get("role_img", 0),
            "title_id_count": figure_summary["svg_accessibility_counts"].get("title_id", 0),
            "desc_id_count": figure_summary["svg_accessibility_counts"].get("desc_id", 0),
            "not_release_reviewed_boundary_count": figure_summary["svg_accessibility_counts"].get("not_release_reviewed_boundary", 0),
            "figure_rows": figure_summary["figure_rows"],
        },
        "contrast_summary": {
            "figure_count": contrast.get("figure_count"),
            "all_figures_passed": contrast.get("all_figures_passed"),
            "minimum_text_contrast_ratio": contrast_summary.get("minimum_text_contrast_ratio"),
            "minimum_flow_line_contrast_ratio": contrast_summary.get("minimum_flow_line_contrast_ratio"),
            "minimum_marker_contrast_ratio": contrast_summary.get("minimum_marker_contrast_ratio"),
            "minimum_font_size_px": contrast_summary.get("minimum_font_size_px"),
        },
        "release_effect": "none",
        "support_state_effect": "none",
        "review_boundary": (
            "This source-level visual identity review checks stylesheet tokens, key-figure presentation rules, "
            "mobile and print behavior, palette diversity, SVG accessibility metadata, and existing contrast metrics. "
            "It is not manual aesthetic review, not e-reader visual review, not DOCX/PDF application review, "
            "not final figure-artifact approval, and not reader release approval."
        ),
        "non_claims": [
            "does not approve final figure art",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
            "does not prove visual quality in every target application",
            "does not promote any chapter core claim or support state",
        ],
        "errors": errors,
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = list(observed.get("errors", []))
    expected_exact = {
        "status": "passed_source_level_visual_identity_review",
        "palette_summary.css_hex_color_count": EXPECTED_CSS_COLOR_COUNT,
        "palette_summary.svg_hex_color_count": EXPECTED_SVG_COLOR_COUNT,
        "palette_summary.combined_hex_color_count": EXPECTED_COMBINED_COLOR_COUNT,
        "palette_summary.combined_color_family_counts": EXPECTED_COLOR_FAMILIES,
        "palette_summary.non_neutral_family_count": 5,
        "figure_source_summary.figure_count": EXPECTED_FIGURE_COUNT,
        "figure_source_summary.standard_viewbox_count": EXPECTED_FIGURE_COUNT,
        "figure_source_summary.role_img_count": EXPECTED_FIGURE_COUNT,
        "figure_source_summary.title_id_count": EXPECTED_FIGURE_COUNT,
        "figure_source_summary.desc_id_count": EXPECTED_FIGURE_COUNT,
        "figure_source_summary.not_release_reviewed_boundary_count": EXPECTED_FIGURE_COUNT,
        "contrast_summary.figure_count": EXPECTED_FIGURE_COUNT,
        "contrast_summary.all_figures_passed": True,
        "contrast_summary.minimum_text_contrast_ratio": EXPECTED_CONTRAST_SUMMARY["minimum_text_contrast_ratio"],
        "contrast_summary.minimum_flow_line_contrast_ratio": EXPECTED_CONTRAST_SUMMARY["minimum_flow_line_contrast_ratio"],
        "contrast_summary.minimum_marker_contrast_ratio": EXPECTED_CONTRAST_SUMMARY["minimum_marker_contrast_ratio"],
        "contrast_summary.minimum_font_size_px": EXPECTED_CONTRAST_SUMMARY["minimum_font_size_px"],
    }

    def get(path: str) -> Any:
        value: Any = observed
        for part in path.split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(part)
        return value

    for path, expected in expected_exact.items():
        if get(path) != expected:
            errors.append(f"{path} must be {expected!r}; found {get(path)!r}.")

    for group, result in observed.get("style_summary", {}).get("fragment_groups", {}).items():
        if result.get("missing_fragments"):
            errors.append(f"style fragment group {group} has missing fragments: {result['missing_fragments']}")

    boundary = str(observed.get("review_boundary", ""))
    for phrase in (
        "not manual aesthetic review",
        "not e-reader visual review",
        "not DOCX/PDF application review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if phrase not in boundary:
            errors.append(f"review_boundary missing phrase: {phrase}")
    non_claim_text = " ".join(str(item) for item in observed.get("non_claims", [])).lower()
    for phrase in (
        "does not approve final figure art",
        "does not approve epub",
        "does not prove visual quality",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing phrase: {phrase}")
    return errors


def render_review(observed: dict[str, Any]) -> str:
    palette = observed["palette_summary"]
    figure = observed["figure_source_summary"]
    contrast = observed["contrast_summary"]
    families = ", ".join(f"{key}: {value}" for key, value in palette["combined_color_family_counts"].items())
    return "\n".join(
        [
            "# Reader Visual Identity Review",
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
            "This source-level review checks the shared reader visual system before a final visual-art review exists. It covers the stylesheet tokens, key-figure presentation shell, mobile/print behavior, SVG accessibility metadata, palette diversity, and the existing contrast/readability manifest. It is not manual aesthetic review, not e-reader visual review, not DOCX/PDF application review, not final figure-artifact approval, and not reader release approval.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{observed['status']}` |",
            f"| Stylesheet variables checked | {len(EXPECTED_STYLE_VARIABLES)} |",
            f"| CSS color count | {palette['css_hex_color_count']} |",
            f"| SVG color count | {palette['svg_hex_color_count']} |",
            f"| Combined color count | {palette['combined_hex_color_count']} |",
            f"| Non-neutral color families | {palette['non_neutral_family_count']} |",
            f"| Color-family mix | {families} |",
            f"| Key figures checked | {figure['figure_count']} |",
            f"| SVG role/title/desc/viewBox coverage | {figure['role_img_count']} / {figure['title_id_count']} / {figure['desc_id_count']} / {figure['standard_viewbox_count']} |",
            f"| Draft non-release boundaries | {figure['not_release_reviewed_boundary_count']} |",
            f"| Minimum text contrast ratio | {contrast['minimum_text_contrast_ratio']} |",
            f"| Minimum flow-line contrast ratio | {contrast['minimum_flow_line_contrast_ratio']} |",
            f"| Minimum marker contrast ratio | {contrast['minimum_marker_contrast_ratio']} |",
            f"| Minimum SVG text size | {contrast['minimum_font_size_px']} px |",
            "",
            "## Style Gates",
            "",
            "- Shared theme tokens exist for ink, muted text, accent, copper, borders, figure background, figure rule, and figure shadow.",
            "- Live `.asi-key-figure` blocks and curated-reader `reader-fig-*` figures share one presentation shell.",
            "- Wide diagrams are horizontally contained on mobile, and print CSS avoids page breaks inside figures.",
            "- The reading-mode switch, screen-reader-only helper class, table overflow, and inline-code wrapping are present in the public stylesheet.",
            "- The palette is not a one-note hue family: the source-level mix includes neutral, teal-blue, copper-amber, green, rose-red, and purple families.",
            "",
            "## Figure Gates",
            "",
            "All ten draft key figures use `role=\"img\"`, `aria-labelledby=\"title desc\"`, `<title id=\"title\">`, `<desc id=\"desc\">`, and the standard `0 0 1200 760` viewBox. Each carries a draft/non-release boundary in the SVG source and remains a draft reader aid.",
            "",
            "## Non-Claims",
            "",
            "- This review does not approve final figure art.",
            "- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.",
            "- This review does not prove visual quality in every target application.",
            "- This review does not promote any chapter core claim or support state.",
            "",
        ]
    )


def validate_review_doc(observed: dict[str, Any], errors: list[str]) -> None:
    if not REVIEW.exists():
        errors.append(f"Missing {rel(REVIEW)}.")
        return
    text = REVIEW.read_text(encoding="utf-8")
    for fragment in (
        "Reader Visual Identity Review",
        COMMAND,
        rel(RESULT),
        "source-level review",
        "CSS color count | 18",
        "SVG color count | 56",
        "Combined color count | 67",
        "Non-neutral color families | 5",
        "Minimum text contrast ratio | 5.19",
        "not final figure-artifact approval",
        "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
    ):
        if fragment not in text:
            errors.append(f"{rel(REVIEW)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true", help="write the tracked visual identity manifest and review doc")
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
        validate_review_doc(observed, errors)
    if errors:
        fail(errors)
    print(
        "Reader visual identity validation passed: "
        f"{observed['figure_source_summary']['figure_count']} figures, "
        f"{observed['palette_summary']['combined_hex_color_count']} colors, "
        f"{observed['palette_summary']['non_neutral_family_count']} non-neutral color families."
    )


if __name__ == "__main__":
    main()
