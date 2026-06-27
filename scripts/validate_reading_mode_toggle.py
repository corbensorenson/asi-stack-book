#!/usr/bin/env python3
"""Validate the live-site reading-mode toggle wiring.

The toggle is a convenience projection of the reader-release strip policy. It
does not generate or publish a reader edition, but it should hide the same
live-only chapter sections in the rendered HTML view.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "editions" / "release_profiles.json"
READING_MODE_INCLUDE = ROOT / "assets" / "reading-mode.html"
STYLES = ROOT / "assets" / "styles.scss"
SYNC_SCAFFOLD = ROOT / "scripts" / "sync_scaffold.py"
QUARTO = ROOT / "_quarto.yml"


def normalize(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip()).lower()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def reader_strip_keys() -> set[str]:
    data = load_json(PROFILES)
    if not isinstance(data, dict) or not isinstance(data.get("profiles"), list):
        raise TypeError("editions/release_profiles.json must contain a profiles list")
    reader = next(
        (profile for profile in data["profiles"] if isinstance(profile, dict) and profile.get("id") == "reader_release"),
        None,
    )
    if not isinstance(reader, dict):
        raise KeyError("reader_release profile is missing")
    keys: set[str] = set()
    for record in reader.get("strip_headings", []):
        if not isinstance(record, dict):
            continue
        keys.add(f"{int(record['level'])}:{normalize(str(record['title']))}")
    return keys


def live_human_view_policy() -> dict:
    data = load_json(PROFILES)
    if not isinstance(data, dict) or not isinstance(data.get("live_human_view_policy"), dict):
        raise TypeError("editions/release_profiles.json must define live_human_view_policy")
    return data["live_human_view_policy"]


def main() -> None:
    errors: list[str] = []
    expected = reader_strip_keys()
    policy = live_human_view_policy()

    include_text = READING_MODE_INCLUDE.read_text(encoding="utf-8", errors="ignore") if READING_MODE_INCLUDE.exists() else ""
    style_text = STYLES.read_text(encoding="utf-8", errors="ignore") if STYLES.exists() else ""
    sync_text = SYNC_SCAFFOLD.read_text(encoding="utf-8", errors="ignore") if SYNC_SCAFFOLD.exists() else ""
    quarto_text = QUARTO.read_text(encoding="utf-8", errors="ignore") if QUARTO.exists() else ""

    if not include_text:
        errors.append("Missing assets/reading-mode.html")
    if "include-after-body: assets/reading-mode.html" not in sync_text:
        errors.append("scripts/sync_scaffold.py does not include the reading-mode after-body asset")
    if "include-after-body: assets/reading-mode.html" not in quarto_text:
        errors.append("_quarto.yml is missing the generated reading-mode after-body include")
    if 'html[data-asi-reading-mode="human"] section[data-asi-live-section="true"]' not in style_text:
        errors.append("assets/styles.scss is missing the human-mode live-section hide rule")
    if 'html[data-asi-reading-mode="human"] [data-asi-live-toc-link="true"]' not in style_text:
        errors.append("assets/styles.scss is missing the human-mode live TOC hide rule")
    if '[data-asi-human-toc-link="true"]' not in style_text:
        errors.append("assets/styles.scss is missing the Human Reading Path TOC hide rule")
    if 'html[data-asi-reading-mode="human"] [data-asi-ai-toc-link="true"]' not in style_text:
        errors.append("assets/styles.scss is missing the human-mode AI/live block TOC hide rule")
    if 'html[data-asi-reading-mode="human"] main.content .header-section-number' not in style_text:
        errors.append("assets/styles.scss is missing the human-mode body section-number hide rule")
    if 'html[data-asi-reading-mode="human"] #TOC .header-section-number' not in style_text:
        errors.append("assets/styles.scss is missing the human-mode TOC section-number hide rule")
    if ".asi-sr-only" not in style_text:
        errors.append("assets/styles.scss is missing the assistive-only helper class")
    if 'html[data-asi-reading-mode="human"] .asi-human-only' not in style_text:
        errors.append("assets/styles.scss is missing the Human view Human Reading Path emphasis rule")
    for css_class in ("asi-ai-only", "asi-human-only", "asi-live-only"):
        if css_class not in style_text:
            errors.append(f"assets/styles.scss is missing the {css_class} view-mode class")

    expected_policy = {
        "toggle_asset": "assets/reading-mode.html",
        "static_validator": "scripts/validate_live_human_view.py",
        "default_mode": "ai",
        "human_mode": "human",
        "storage_key": "asi-stack-reading-mode",
        "url_query_parameter": "view",
        "mode_status_selector": "[data-asi-reading-mode-status]",
        "toc_link_marker": "data-asi-live-toc-link",
        "human_toc_link_marker": "data-asi-human-toc-link",
        "ai_toc_link_marker": "data-asi-ai-toc-link",
        "assistive_description_class": "asi-sr-only",
        "human_view_section_number_policy": "hide rendered section numbers in Human view to avoid numbering gaps left by stripped live-only sections and unheaded bridge prose",
        "ai_only_class": "asi-ai-only",
        "human_only_class": "asi-human-only",
        "live_only_class": "asi-live-only",
    }
    for key, value in expected_policy.items():
        if policy.get(key) != value:
            errors.append(f"live_human_view_policy.{key} must be {value!r}")

    required_asset_strings = {
        "storage key": 'const storageKey = "asi-stack-reading-mode"',
        "URL query parameter": 'const queryParam = "view"',
        "URL mode reader": "function modeFromUrl",
        "URL mode initializer": "function initialMode",
        "URL mode updater": "function updateUrlMode",
        "URLSearchParams reader": "new URLSearchParams(window.location.search)",
        "history URL replacement": "window.history.replaceState",
        "toggle URL update": "{ updateUrl: true }",
        "assistive description": 'control.setAttribute("aria-describedby", "asi-reading-mode-description")',
        "assistive helper": 'class="asi-sr-only"',
        "status role": 'role="status"',
        "polite live region": 'aria-live="polite"',
        "mode status selector": "data-asi-reading-mode-status",
        "toc link marker": "data-asi-live-toc-link",
        "human TOC link marker": "data-asi-human-toc-link",
        "AI TOC link marker": "data-asi-ai-toc-link",
        "view-mode TOC marker function": "function markViewModeTocLinks",
        "view-mode TOC marker call": "markViewModeTocLinks()",
        "toc link marker function": "function markLiveTocLinks",
        "toc link marker call": "markLiveTocLinks(liveIds)",
        "ai status copy": "AI/research view active.",
        "human status copy": "Human view active.",
        "ai button title": "Show the full AI and researcher scaffold",
        "human button title": "Read the human-facing chapter prose",
        "active button aria label": "active",
        "switch button aria label": "Switch to",
    }
    for label, needle in required_asset_strings.items():
        if needle not in include_text:
            errors.append(f"assets/reading-mode.html is missing {label}: {needle!r}")

    actual = set(re.findall(r'"([23]:[a-z0-9][^"]+)"', include_text))
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append("reading-mode heading list missing: " + ", ".join(missing))
        if extra:
            errors.append("reading-mode heading list has extra entries: " + ", ".join(extra))

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print(f"Reading mode toggle validation passed: {len(expected)} live-only headings tracked.")


if __name__ == "__main__":
    main()
