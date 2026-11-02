#!/usr/bin/env python3
"""Consume a complete, current browser report before publication.

This checks report custody, coverage and reported outcomes. It does not rerun
the DOM probes or turn a producer-authored observation into independent human
accessibility review, editorial approval or claim support.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

from build_tested_site_bundle import file_rows
from schema_validation import validate_value

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ("book_structure.json", "editions/reader_manuscript/current/conclusion_claim_crosswalk.json",
          "scripts/validate_live_human_view_browser.js")
VIEWPORTS = {"desktop": {"width": 1280, "height": 900}, "mobile": {"width": 390, "height": 844}}
MAX_REPORT_BYTES = 32 * 1024 * 1024


def obj(properties: dict, *, extra: bool = False) -> dict:
    return {"type": "object", "required": list(properties), "properties": properties,
            "additionalProperties": extra}


TEXT = {"type": "string", "minLength": 1}
COUNT = {"type": "integer", "minimum": 0}
POSITIVE = {"type": "integer", "minimum": 1}
ZERO = {"type": "integer", "const": 0}
TRUE = {"type": "boolean", "const": True}
FALSE = {"type": "boolean", "const": False}
OVERFLOW = {"type": "number", "minimum": 0, "maximum": 2}
HASH = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
HASHES = {"type": "object", "minProperties": 1, "additionalProperties": HASH}
RECT = obj({name: {"type": "number"} for name in ("left", "right", "top", "bottom", "width", "height")})
BUTTON = obj({"choice": {"enum": ["ai", "human"]}, "text": TEXT, "visible": TRUE,
              "rect": RECT, "clipped_horizontally": FALSE, "text_overflow_px": OVERFLOW})
LAYOUT = obj({"viewport_width": POSITIVE, "viewport_height": POSITIVE, "client_width": POSITIVE,
              "scroll_width": POSITIVE, "horizontal_overflow_px": OVERFLOW, "toggle_visible": TRUE,
              "toggle_rect": RECT, "toggle_clipped_horizontally": FALSE,
              "buttons": {"type": "array", "minItems": 2, "maxItems": 2, "items": BUTTON},
              "label": obj({"height": {"type": "number", "minimum": 0},
                            "line_height": {"type": "number", "exclusiveMinimum": 0}, "text_overflow_px": OVERFLOW}),
              "reader_link": obj({"text": TEXT, "href": TEXT, "visible": TRUE,
                                  "clipped_horizontally": FALSE, "text_overflow_px": OVERFLOW})})
OVERLAY = obj({"processed": TRUE, "total": COUNT, "matching": COUNT, "applied": COUNT,
               "skipped": COUNT, "skipped_ids": {"type": "string"}, "applied_nodes": COUNT, "original_wrappers": COUNT})
DIAGRAMS = obj({"diagram_count": POSITIVE, "visible_diagram_count": POSITIVE,
                "diagrams": {"type": "array", "minItems": 1, "items": obj({"id": TEXT,
                    "width": {"type": "number", "minimum": 0}, "height": {"type": "number", "minimum": 0},
                    "visible": {"type": "boolean"}, "content_count": COUNT, "text_count": COUNT})}})
HUMAN = obj({"reader_overlay_operations": COUNT, "reader_overlay_runtime": OVERLAY,
             "status_text": TEXT, "layout": LAYOUT}, extra=True)
AI = obj({"visible_live_sections": POSITIVE, "visible_human_blocks": ZERO,
          "visible_core_claim_markers": POSITIVE, "visible_support_boilerplate_phrases": COUNT,
          "visible_human_support_boundaries": ZERO, "layout": LAYOUT, "diagrams": DIAGRAMS}, extra=True)
READER = obj({"horizontal_overflow_px": OVERFLOW, "control_visible": TRUE, "control_clipped": FALSE,
              "research_href": TEXT, "research_text": TEXT, "current_text": {"const": "Human Reader"},
              "title": TEXT, "main_present": TRUE, "skip_link_present": TRUE,
              "research_link_label": TEXT, "callout_count": POSITIVE})
TECHNICAL_ROW = obj({"page_id": TEXT, "url": TEXT, "viewport": {"enum": list(VIEWPORTS)},
                     "viewport_size": obj({"width": POSITIVE, "height": POSITIVE}),
                     "checks": obj({"human_url_mode": HUMAN}, extra=True)})
SCHEMA = {"$schema": "https://json-schema.org/draft/2020-12/schema", **obj({
    "schema_version": {"const": "0.2"}, "status": {"const": "pass"},
    "page_selection": {"const": "all-chapters"}, "viewport_selection": {"const": "all-viewports"},
    "viewports": {"type": "array", "minItems": 2, "maxItems": 2,
                  "items": obj({"name": {"enum": list(VIEWPORTS)}, "width": POSITIVE, "height": POSITIVE})},
    "browser_version": TEXT, "site_dir": TEXT, "site_sha256": HASHES,
    "input_sha256": obj({name: HASH for name in INPUTS}),
    "validated_pages": {"type": "array", "minItems": 1, "items": TECHNICAL_ROW},
    "validated_reader_pages": {"type": "array", "minItems": 1,
                               "items": obj({"unit_id": TEXT, "viewport": {"enum": list(VIEWPORTS)},
                                             "url": TEXT, "checks": READER})},
    "sampled_pages": {"type": "array", "items": TECHNICAL_ROW},
    "edition_control_accessibility": {"type": "array", "minItems": 6, "maxItems": 6,
                                      "items": obj({"width": {"type": "integer", "enum": [320, 390, 430]},
                                                    "text_scale": {"type": "integer", "enum": [1, 2]},
                                                    "metrics": LAYOUT, "keyboard_controls": {"type": "integer", "minimum": 3},
                                                    "screenshot": TEXT})},
    "non_claims": {"type": "array", "minItems": 2, "items": TEXT},
})}


def ordinary(path: Path) -> None:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f"browser report custody must not traverse a symlink: {path}")


def snapshot(site: Path, root: Path) -> tuple[dict, dict]:
    ordinary(site)
    inputs = {}
    for relative in INPUTS:
        path = root / relative
        ordinary(path)
        if not path.is_file():
            raise ValueError(f"browser report input is not a regular file: {path}")
        inputs[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    rows = file_rows(site)
    files = {row["path"]: row["sha256"] for row in rows}
    if "index.html" not in files:
        raise ValueError("browser report site lacks index.html")
    return files, inputs


def public_file(site: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if (path.is_absolute() or path.as_posix() != relative or ".." in path.parts or "\\" in relative
            or path.suffix != ".html"):
        raise ValueError(f"invalid browser coverage path: {relative!r}")
    return site / path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def layout(metrics: dict, size: dict, *, touch: bool = False) -> None:
    require((metrics["viewport_width"], metrics["viewport_height"]) == (size["width"], size["height"]),
            "reported layout viewport differs from required viewport")
    require({button["choice"] for button in metrics["buttons"]} == {"ai", "human"}, "duplicate/missing reading choice")
    require(metrics["label"]["height"] <= metrics["label"]["line_height"] * 1.2, "reported Edition label wraps")
    require(abs(metrics["horizontal_overflow_px"] - max(0, metrics["scroll_width"] - metrics["client_width"])) < 0.01,
            "reported overflow contradicts measured widths")
    if touch:
        require(all(button["rect"]["width"] >= 44 and button["rect"]["height"] >= 44
                    for button in metrics["buttons"]), "reported touch target is smaller than 44px")


def coverage(rows: list, expected: dict, *, key: str, site: Path) -> None:
    pairs = [(row[key], row["viewport"]) for row in rows]
    require(len(pairs) == len(set(pairs)), "duplicate browser page/viewport pair")
    require(set(pairs) == {(identifier, viewport) for identifier in expected for viewport in VIEWPORTS},
            "browser page/viewport coverage is incomplete or unexpected")
    for row in rows:
        require(row["url"] == public_file(site, expected[row[key]]).as_uri(), "browser page URL differs from canonical route")


def validate_report(report: dict, site: Path, *, root: Path = ROOT) -> dict:
    json.dumps(report, allow_nan=False)  # JSON numbers cannot be NaN/Infinity.
    errors = validate_value(report, SCHEMA, "browser_report")
    require(not errors, "; ".join(errors[:8]))
    before = snapshot(site, root)
    site = site.resolve()
    require(report["site_dir"] == str(site), "browser report identifies a different site")
    require((report["site_sha256"], report["input_sha256"]) == before, "browser report inputs/site are stale")
    structure = json.loads((root / INPUTS[0]).read_bytes())
    crosswalk = json.loads((root / INPUTS[1]).read_bytes())
    chapters = [chapter for part in structure["parts"] for chapter in part["chapters"]]
    appendices = [row for row in structure["appendices"] if row["id"] in {"corben-source-corpus", "external-sources-and-literature"}]
    require(len(appendices) == 2, "canonical browser appendix coverage is ambiguous")
    technical = {row["id"]: str(PurePosixPath(row["file"]).with_suffix(".html")) for row in chapters + appendices}
    reader = {row["unit_id"]: row["public_path"] for row in crosswalk["units"]}
    require(len(technical) == len(chapters) + 2 and len(reader) == len(crosswalk["units"]), "canonical browser identifiers duplicate")
    coverage(report["validated_pages"], technical, key="page_id", site=site)
    coverage(report["validated_reader_pages"], reader, key="unit_id", site=site)
    require(report["sampled_pages"] == report["validated_pages"], "compatibility page alias differs from full coverage")
    require(report["viewports"] == [{"name": name, **size} for name, size in VIEWPORTS.items()], "browser viewport declarations differ")
    chapter_ids = {row["id"] for row in chapters}
    for row in report["validated_pages"]:
        checks = row["checks"]
        human = checks["human_url_mode"]
        require("Human view active." in human["status_text"], "reported Human view status is missing")
        runtime = human["reader_overlay_runtime"]
        require(runtime["total"] == human["reader_overlay_operations"]
                and runtime["matching"] == runtime["applied"] + runtime["skipped"]
                and runtime["applied"] == runtime["applied_nodes"], "reported overlay counts contradict")
        size = VIEWPORTS[row["viewport"]]
        require(row["viewport_size"] == size, "technical row viewport size differs")
        layout(human["layout"], size)
        if row["page_id"] in chapter_ids:
            for name in ("ai_click_mode", "ai_url_mode"):
                errors = validate_value(checks.get(name), AI, f"{row['page_id']}.{name}")
                require(not errors, "; ".join(errors[:4]))
                layout(checks[name]["layout"], size)
            for mode in (human, checks["ai_click_mode"], checks["ai_url_mode"]):
                diagrams = mode.get("diagrams")
                require(not validate_value(diagrams, DIAGRAMS, "diagrams"), "diagram checks are absent or invalid")
                visible = [diagram for diagram in diagrams["diagrams"] if diagram["visible"]]
                require(diagrams["diagram_count"] == len(diagrams["diagrams"])
                        and diagrams["visible_diagram_count"] == len(visible)
                        and all(diagram["width"] > 80 and diagram["height"] > 20 and diagram["content_count"] > 5 for diagram in visible),
                        "reported diagram visibility/counts contradict")
            require(checks.get("local_storage_persistence") == "human", "persistence check is absent")
            require(checks.get("human_click_url") == row["url"] + "?view=human"
                    and checks["ai_click_mode"].get("url") == row["url"] + "?view=ai", "mode-click checks are absent or wrong")
            for name in ("visible_live_sections", "visible_core_claim_markers", "visible_live_toc_links", "visible_support_boilerplate_phrases"):
                require(not validate_value(human.get(name), ZERO, name), f"reported Human view exposes {name}")
            for name in ("live_sections", "human_blocks", "core_claim_markers", "visible_human_blocks", "visible_core_claim_text", "visible_human_support_boundaries"):
                require(not validate_value(human.get(name), POSITIVE, name), f"reported Human view lacks {name}")
        else:
            require(checks.get("ai_click_url") == row["url"] + "?view=ai", "appendix click check is absent or wrong")
            require(not validate_value(checks.get("ai_click_layout"), LAYOUT, "appendix layout"), "appendix layout check is absent or invalid")
            layout(checks["ai_click_layout"], size)
    units = {row["unit_id"]: row for row in crosswalk["units"]}
    for row in report["validated_reader_pages"]:
        require(units[row["unit_id"]]["title"] in row["checks"]["title"], "reader title differs from current crosswalk")
    controls = report["edition_control_accessibility"]
    pairs = [(row["width"], row["text_scale"]) for row in controls]
    require(len(set(pairs)) == 6 and set(pairs) == {(width, scale) for width in (320, 390, 430) for scale in (1, 2)},
            "responsive control coverage is incomplete or duplicated")
    for row in controls:
        layout(row["metrics"], {"width": row["width"], "height": 844}, touch=True)
    require(snapshot(site, root) == before, "browser report inputs/site changed while being checked")
    return {"technical_pairs": len(report["validated_pages"]), "reader_pairs": len(report["validated_reader_pages"]), "control_pairs": len(controls)}


def report_bytes(path: Path) -> bytes:
    ordinary(path)
    require(path.is_file(), "browser report is missing or not a regular file")
    with path.open("rb") as stream:
        data = stream.read(MAX_REPORT_BYTES + 1)
    require(len(data) <= MAX_REPORT_BYTES, "browser report exceeds the 32 MiB consumer bound")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "_site")
    parser.add_argument("--report", type=Path, default=ROOT / "build/live_human_view_browser_report.json")
    args = parser.parse_args()
    try:
        before = report_bytes(args.report)
        report = json.loads(before)
        result = validate_report(report, args.site)
        require(report_bytes(args.report) == before, "browser report changed during checking")
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f"Browser report rejected: {error}") from error
    print(f"Browser report accepted: {result['technical_pairs']} technical, {result['reader_pairs']} reader and {result['control_pairs']} control pairs; report custody/coverage only, no support or release effect.")


if __name__ == "__main__":
    from admission_guard import canonical_access
    try:
        with canonical_access(ROOT):
            main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Browser report rejected: {error}")
