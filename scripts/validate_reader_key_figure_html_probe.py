#!/usr/bin/env python3
"""Render the curated reader workspace and inspect key figures in HTML.

This is a local HTML probe for the draft reader key figures. It checks rendered
HTML structure only; it is not visual design review, release approval, or a
format artifact approval.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html import unescape
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
RESULT = ROOT / "experiments" / "reader_key_figure_html_probe" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "reader_key_figure_html_probe.md"
EXPECTED_COUNT = 10
BOUNDARY_PHRASES = (
    "does not prove",
    "not evidence",
    "not release",
    "not release-reviewed",
    "not a deployment",
    "no support-state",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def active_spine_differs_from_historical_snapshot() -> bool:
    manifest = load_json(MANIFEST)
    structure = load_json(BOOK_STRUCTURE)
    if not isinstance(manifest, dict) or not isinstance(structure, dict):
        fail(["reader manifest and book structure must be objects."])
    snapshot = manifest.get("historical_spine_snapshot", {})
    snapshot_ids = snapshot.get("chapter_ids", []) if isinstance(snapshot, dict) else []
    active_ids = [
        str(chapter.get("id", ""))
        for part in structure.get("parts", [])
        if isinstance(part, dict)
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]
    if not isinstance(snapshot_ids, list) or not all(isinstance(item, str) for item in snapshot_ids):
        fail(["historical_spine_snapshot.chapter_ids must be a list of chapter IDs."])
    return active_ids != snapshot_ids


def fail(errors: list[str]) -> None:
    print("Reader key-figure HTML probe validation failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


def run_command(cmd: list[str], cwd: Path) -> None:
    env = os.environ.copy()
    env.setdefault("LANG", "en_US.UTF-8")
    env.setdefault("LC_ALL", "en_US.UTF-8")
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        raise RuntimeError(f"Command failed with exit {proc.returncode}: {' '.join(cmd)}")


def build_and_render(output_dir: Path) -> Path:
    run_command(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_curated_reader_edition.py"),
            "--output",
            str(output_dir),
        ],
        ROOT,
    )
    run_command(["quarto", "render", "--to", "html"], output_dir)
    site = output_dir / "_reader_site"
    if not site.exists():
        raise RuntimeError("curated reader render did not create _reader_site")
    return site


def rendered_chapter_path(site: Path, reader_ref: str) -> Path:
    path_part = reader_ref.split("#", 1)[0]
    source_path = Path(path_part)
    return site / "chapters" / f"{source_path.stem}.html"


def inspect_figure(site: Path, figure: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    figure_id = str(figure.get("id", ""))
    asset = str(figure.get("draft_asset_path", ""))
    asset_name = Path(asset).name
    reader_ref = str(figure.get("reader_manuscript_ref", ""))
    anchor = reader_ref.split("#", 1)[1] if "#" in reader_ref else ""
    html_path = rendered_chapter_path(site, reader_ref)
    copied_asset = site / "assets" / "diagrams" / asset_name

    row: dict[str, Any] = {
        "id": figure_id,
        "asset": asset,
        "reader_ref": reader_ref,
        "rendered_chapter_html": str(html_path.relative_to(site.parent)),
        "rendered_asset": str(copied_asset.relative_to(site.parent)),
        "status": "rendered_present",
    }

    if not html_path.exists():
        errors.append(f"{figure_id}: rendered chapter missing: {html_path}")
        row["status"] = "missing_rendered_chapter"
        return row, errors
    if not copied_asset.exists():
        errors.append(f"{figure_id}: rendered SVG asset missing: {copied_asset}")
        row["status"] = "missing_rendered_asset"

    text = html_path.read_text(encoding="utf-8", errors="ignore")
    if anchor not in text:
        errors.append(f"{figure_id}: rendered figure anchor missing: {anchor}")
        row["status"] = "missing_anchor"
        return row, errors
    index = text.find(anchor)
    window = text[index : index + 2600]
    lower_window = window.lower()

    if asset_name not in window:
        errors.append(f"{figure_id}: rendered figure block missing asset {asset_name}")
    img_match = re.search(r"<img\b[^>]*>", window, re.IGNORECASE)
    img_tag = img_match.group(0) if img_match else ""
    if not img_tag:
        errors.append(f"{figure_id}: rendered figure block missing img tag")
    src_match = re.search(r'\bsrc="([^"]+)"', img_tag)
    alt_match = re.search(r'\balt="([^"]+)"', img_tag)
    class_match = re.search(r'\bclass="([^"]+)"', img_tag)
    src = unescape(src_match.group(1)) if src_match else ""
    alt = unescape(alt_match.group(1)) if alt_match else ""
    classes = class_match.group(1) if class_match else ""
    caption_match = re.search(r"<figcaption>(.*?)</figcaption>", window, re.IGNORECASE | re.DOTALL)
    caption = unescape(re.sub(r"<[^>]+>", "", caption_match.group(1))).strip() if caption_match else ""
    boundary_match = re.search(r"</div>\s*<p>(.*?)</p>", window, re.IGNORECASE | re.DOTALL)
    boundary = (
        unescape(re.sub(r"<[^>]+>", "", boundary_match.group(1))).strip()
        if boundary_match
        else ""
    )

    row.update(
        {
            "img_src": src,
            "img_class": classes,
            "alt_word_count": len(words(alt)),
            "caption": caption,
            "boundary_excerpt": boundary,
        }
    )

    if f"../assets/diagrams/{asset_name}" != src:
        errors.append(f"{figure_id}: unexpected rendered img src {src!r}")
    if "img-fluid" not in classes or "figure-img" not in classes:
        errors.append(f"{figure_id}: rendered img classes should include img-fluid figure-img")
    if len(words(alt)) < 12 or "draft" not in alt.lower():
        errors.append(f"{figure_id}: rendered alt text is too thin or not draft-scoped")
    if len(words(caption)) < 3 or "draft" not in caption.lower():
        errors.append(f"{figure_id}: rendered caption is too thin or not draft-scoped")
    if "figure boundary:" not in lower_window:
        errors.append(f"{figure_id}: rendered figure block missing Figure boundary paragraph")
    if not any(phrase in boundary.lower() for phrase in BOUNDARY_PHRASES):
        errors.append(f"{figure_id}: rendered boundary lacks a non-claim phrase")
    if "release-approved" in lower_window:
        errors.append(f"{figure_id}: rendered figure block must not claim release approval")

    return row, errors


def current_probe_result() -> dict[str, Any]:
    # A historical reader artifact must not be rebuilt from a changed active spine.
    # The active generated reader has separate spine and Human-view validators.
    if active_spine_differs_from_historical_snapshot():
        if not RESULT.exists():
            fail([f"Missing frozen historical result: {rel(RESULT)}."])
        stored = load_json(RESULT)
        if not isinstance(stored, dict):
            fail([f"{rel(RESULT)} must contain an object."])
        return stored

    manifest = load_json(MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets", [])
    if not isinstance(figures, list) or len(figures) != EXPECTED_COUNT:
        fail(["reader_handoff_contract.key_figure_targets must contain exactly 10 records."])

    with tempfile.TemporaryDirectory(prefix="asi-reader-key-figures-html-") as temp_dir:
        site = build_and_render(Path(temp_dir))
        rows: list[dict[str, Any]] = []
        errors: list[str] = []
        for figure in figures:
            row, row_errors = inspect_figure(site, figure)
            rows.append(row)
            errors.extend(row_errors)
        if errors:
            fail(errors)

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "probe": "reader_key_figure_html_probe",
        "source_manifest": rel(MANIFEST),
        "builder": "python3 scripts/build_curated_reader_edition.py",
        "render_command": "LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html",
        "rendered_site": "_reader_site",
        "figure_count": len(rows),
        "status": "passed",
        "figures": rows,
        "non_claims": [
            "This probe inspects rendered curated-reader HTML structure only.",
            "This probe is not final figure-artifact review.",
            "This probe is not HTML, EPUB, DOCX, PDF, e-reader, audio, or release approval.",
            "This probe does not prove model quality, deployed runtime behavior, evidence transitions, or support-state promotion.",
        ],
    }


def comparable(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": result.get("schema_version"),
        "probe": result.get("probe"),
        "source_manifest": result.get("source_manifest"),
        "builder": result.get("builder"),
        "render_command": result.get("render_command"),
        "rendered_site": result.get("rendered_site"),
        "figure_count": result.get("figure_count"),
        "status": result.get("status"),
        "figures": result.get("figures"),
        "non_claims": result.get("non_claims"),
    }


def write_doc(result: dict[str, Any]) -> None:
    lines = [
        "# Reader Key-Figure HTML Probe",
        "",
        f"Last checked: {result['generated_at_utc'][:10]}",
        "",
        "Command:",
        "",
        "```bash",
        "python3 scripts/validate_reader_key_figure_html_probe.py --write-result",
        "```",
        "",
        "This probe records a rendered HTML structural review of the frozen v1.0 curated",
        "reader snapshot. When the active book spine differs from that snapshot, the",
        "validator preserves this historical result rather than rebuilding the curated",
        "manuscript from newer chapters. The active generated reader has separate spine",
        "and Human-view validation. The recorded probe checks image references, copied SVG",
        "assets, alt text, captions, responsive image classes, and visible non-claim",
        "boundary paragraphs. It is not a release approval and not final figure-artifact review.",
        "",
        "## Result",
        "",
        f"- Status: `{result['status']}`",
        f"- Figures checked: {result['figure_count']}",
        f"- Result artifact: `{rel(RESULT)}`",
        "",
        "## Rendered Figure Checks",
        "",
        "| Figure | Rendered chapter HTML | Alt words | Caption | Boundary excerpt |",
        "|---|---|---:|---|---|",
    ]
    for row in result["figures"]:
        boundary = str(row.get("boundary_excerpt", "")).replace("|", "\\|")
        caption = str(row.get("caption", "")).replace("|", "\\|")
        lines.append(
            f"| `{row['asset']}` | `{row['rendered_chapter_html']}` | "
            f"{row['alt_word_count']} | {caption} | {boundary} |"
        )
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
            "- This probe does not approve the figures as final art.",
            "- This probe does not approve HTML, EPUB, DOCX, PDF, e-reader, audio, or release artifacts.",
            "- This probe does not promote any chapter core claim or support state.",
            "- EPUB, DOCX, PDF, e-reader, visual-design, contrast, page-break, and audio companion review remain open.",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_written_surfaces(result: dict[str, Any], current: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if comparable(result) != comparable(current):
        errors.append(f"{rel(RESULT)} is stale; rerun with --write-result.")
    if not DOC.exists():
        errors.append(f"Missing {rel(DOC)}.")
        return errors
    text = DOC.read_text(encoding="utf-8", errors="ignore")
    required = [
        "python3 scripts/validate_reader_key_figure_html_probe.py --write-result",
        "not a release approval",
        "not final figure-artifact review",
        "EPUB",
        "DOCX",
        "PDF",
        "audio",
    ]
    for phrase in required:
        if phrase not in text:
            errors.append(f"{rel(DOC)} missing required phrase {phrase!r}.")
    for row in current["figures"]:
        if row["asset"] not in text:
            errors.append(f"{rel(DOC)} missing asset {row['asset']}.")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true", help="write the tracked JSON result and docs page")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    current = current_probe_result()
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        write_doc(current)
    elif not RESULT.exists():
        fail([f"Missing {rel(RESULT)}; run with --write-result first."])

    written = load_json(RESULT)
    errors = validate_written_surfaces(written, current)
    if errors:
        fail(errors)
    print(
        "Reader key-figure HTML probe passed: "
        f"{current['figure_count']} rendered curated-reader figure blocks checked."
    )


if __name__ == "__main__":
    main()
