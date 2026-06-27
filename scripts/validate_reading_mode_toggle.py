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


def main() -> None:
    errors: list[str] = []
    expected = reader_strip_keys()

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
