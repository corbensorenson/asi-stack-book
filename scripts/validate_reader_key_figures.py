#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
ASSET_README = ROOT / "assets" / "diagrams" / "README.md"
REVIEW = ROOT / "docs" / "reader_key_figure_artifact_review.md"

EXPECTED_COUNT = 10
BOUNDARY_PHRASES = (
    "does not prove",
    "not proof",
    "not deployed",
    "not an accepted",
    "not epub",
    "not release",
    "not a release",
    "not evidence",
    "does not promote",
    "no deployed",
    "no support-state",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def text_near_asset(text: str, asset_name: str, chars: int = 1500) -> str:
    index = text.find(asset_name)
    if index < 0:
        return ""
    start = max(0, index - 400)
    end = min(len(text), index + chars)
    return text[start:end]


def heading_anchor(path: Path, anchor: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip()
        slug = re.sub(r"[^a-z0-9 -]", "", heading.lower())
        slug = re.sub(r"\s+", "-", slug).strip("-")
        if slug == anchor:
            return True
    return False


def validate_svg(path: Path, owner: str, errors: list[str]) -> None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{owner}: {rel(path)} is not parseable SVG: {exc}.")
        return
    if not root.tag.endswith("svg"):
        errors.append(f"{owner}: {rel(path)} root is not svg.")
    if root.attrib.get("role") != "img":
        errors.append(f"{owner}: {rel(path)} must declare role='img'.")
    aria = root.attrib.get("aria-labelledby", "")
    if "title" not in aria or "desc" not in aria:
        errors.append(f"{owner}: {rel(path)} must aria-label title and desc.")
    view_box = root.attrib.get("viewBox")
    if not view_box or len(view_box.split()) != 4:
        errors.append(f"{owner}: {rel(path)} must carry a four-value viewBox.")

    title = root.find("{http://www.w3.org/2000/svg}title")
    desc = root.find("{http://www.w3.org/2000/svg}desc")
    title_text = normalize(title.text or "") if title is not None else ""
    desc_text = normalize(desc.text or "") if desc is not None else ""
    if len(words(title_text)) < 4 or "draft figure" not in title_text.lower():
        errors.append(f"{owner}: {rel(path)} title must be a substantive draft-figure title.")
    if len(words(desc_text)) < 15:
        errors.append(f"{owner}: {rel(path)} desc must be a substantive text equivalent.")
    visible_text = " ".join((node.text or "") for node in root.iter())
    if "Draft key figure" not in visible_text:
        errors.append(f"{owner}: {rel(path)} must visibly label itself as a draft key figure.")
    if "release-approved" in visible_text.lower():
        errors.append(f"{owner}: {rel(path)} must not claim release approval.")


def validate_live_surface(
    figure: dict[str, Any],
    owner: str,
    asset_name: str,
    errors: list[str],
) -> None:
    ref = figure.get("text_equivalent_ref")
    if not isinstance(ref, str) or "#" not in ref:
        errors.append(f"{owner}: text_equivalent_ref must include a path and anchor.")
        return
    text_path, anchor = ref.split("#", 1)
    path = ROOT / text_path
    if not path.exists():
        errors.append(f"{owner}: text_equivalent_ref path missing: {text_path}.")
        return
    if not heading_anchor(path, anchor):
        errors.append(f"{owner}: text_equivalent_ref anchor missing: {ref}.")
    text = path.read_text(encoding="utf-8", errors="ignore")
    if asset_name not in text:
        errors.append(f"{owner}: live chapter does not embed {asset_name}.")
        return
    window = text_near_asset(text, asset_name).lower()
    for phrase in ("fig-alt=", "how to read", "draft reader aid"):
        if phrase not in window:
            errors.append(f"{owner}: live chapter figure block missing {phrase!r}.")
    if not any(phrase in window for phrase in BOUNDARY_PHRASES):
        errors.append(f"{owner}: live chapter figure block lacks a visible non-claim boundary.")


def validate_reader_surface(
    figure: dict[str, Any],
    owner: str,
    asset_name: str,
    errors: list[str],
) -> None:
    ref = figure.get("reader_manuscript_ref")
    if not isinstance(ref, str) or "#" not in ref:
        errors.append(f"{owner}: reader_manuscript_ref must include a path and anchor.")
        return
    reader_path, anchor = ref.split("#", 1)
    path = ROOT / reader_path
    if not path.exists():
        errors.append(f"{owner}: reader_manuscript_ref path missing: {reader_path}.")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    if f"#{anchor}" not in text:
        errors.append(f"{owner}: reader figure anchor missing: {ref}.")
    if asset_name not in text:
        errors.append(f"{owner}: reader manuscript does not embed {asset_name}.")
        return
    window = text_near_asset(text, asset_name).lower()
    for phrase in ("fig-alt=", "figure boundary:", "draft reader aid"):
        if phrase not in window:
            errors.append(f"{owner}: reader figure block missing {phrase!r}.")
    if not any(phrase in window for phrase in BOUNDARY_PHRASES):
        errors.append(f"{owner}: reader figure block lacks a visible non-claim boundary.")


def validate_review_doc(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not REVIEW.exists():
        errors.append(f"Missing {rel(REVIEW)}.")
        return
    text = REVIEW.read_text(encoding="utf-8", errors="ignore")
    required = [
        "python3 scripts/validate_reader_key_figures.py",
        "not a release approval",
        "not final figure-artifact review",
        "EPUB",
        "DOCX",
        "PDF",
        "audio",
    ]
    for phrase in required:
        if phrase not in text:
            errors.append(f"{rel(REVIEW)} missing required phrase {phrase!r}.")
    for figure in figures:
        asset = str(figure.get("draft_asset_path", ""))
        if asset and asset not in text:
            errors.append(f"{rel(REVIEW)} missing figure asset {asset}.")


def main() -> None:
    errors: list[str] = []
    manifest = load_json(MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets")
    if not isinstance(figures, list) or len(figures) != EXPECTED_COUNT:
        errors.append(
            f"reader_handoff_contract.key_figure_targets must contain exactly {EXPECTED_COUNT} records."
        )
        figures = []

    asset_readme = ASSET_README.read_text(encoding="utf-8", errors="ignore") if ASSET_README.exists() else ""
    seen: set[str] = set()
    for index, figure in enumerate(figures):
        owner = f"key_figure_targets[{index}]"
        if not isinstance(figure, dict):
            errors.append(f"{owner}: figure record must be an object.")
            continue
        figure_id = figure.get("id")
        if not isinstance(figure_id, str) or not figure_id:
            errors.append(f"{owner}: id must be non-empty.")
        elif figure_id in seen:
            errors.append(f"{owner}: duplicate figure id {figure_id}.")
        else:
            seen.add(figure_id)
        if figure.get("status") != "target_defined_not_final_art":
            errors.append(f"{owner}: status must remain target_defined_not_final_art.")
        if figure.get("draft_artifact_state") != "draft_not_release_reviewed":
            errors.append(f"{owner}: draft_artifact_state must remain draft_not_release_reviewed.")
        boundary = str(figure.get("release_boundary", "")).lower()
        if "not a completed figure" not in boundary or "not reviewed as a release artifact" not in boundary:
            errors.append(f"{owner}: release_boundary must preserve no-release-review boundary.")
        asset = figure.get("draft_asset_path")
        if not isinstance(asset, str) or not asset.startswith("assets/diagrams/") or not asset.endswith(".svg"):
            errors.append(f"{owner}: draft_asset_path must be an assets/diagrams/*.svg path.")
            continue
        path = ROOT / asset
        asset_name = Path(asset).name
        if not path.exists():
            errors.append(f"{owner}: draft SVG missing: {asset}.")
            continue
        if asset not in asset_readme:
            errors.append(f"{owner}: {asset} missing from {rel(ASSET_README)}.")
        validate_svg(path, owner, errors)
        validate_live_surface(figure, owner, asset_name, errors)
        validate_reader_surface(figure, owner, asset_name, errors)

    validate_review_doc(figures, errors)
    if errors:
        print("Reader key-figure validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Reader key-figure validation passed: "
        f"{len(figures)} draft SVG assets checked for metadata, live placement, "
        "reader placement, alt text, captions, and non-claim boundaries."
    )


if __name__ == "__main__":
    main()
