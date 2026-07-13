#!/usr/bin/env python3
"""Reject undeclared HTML build artifacts in the chapter source directory."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
QUARTO = ROOT / "_quarto.yml"
HISTORY = ROOT / "docs/chapter_history_ledger.md"


def hygiene_errors() -> list[str]:
    errors: list[str] = []
    quarto = QUARTO.read_text(encoding="utf-8")
    history = HISTORY.read_text(encoding="utf-8")
    html_files = sorted(CHAPTERS.glob("*.html"))

    if len(html_files) != 10:
        errors.append(f"expected 10 declared historical redirects, found {len(html_files)}")

    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        refresh = re.search(r'<meta\s+http-equiv="refresh"\s+content="0;\s*url=([^"]+)"', text, re.I)
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', text, re.I)
        if not refresh or not canonical:
            errors.append(f"{rel}: not a redirect with refresh and canonical targets")
            continue
        if refresh.group(1) != canonical.group(1):
            errors.append(f"{rel}: refresh and canonical targets disagree")
        target = canonical.group(1)
        if "/" in target or not target.endswith(".html"):
            errors.append(f"{rel}: canonical target is not a local chapter HTML basename")
        else:
            target_source = CHAPTERS / (Path(target).stem + ".qmd")
            if not target_source.is_file():
                errors.append(f"{rel}: canonical target has no active QMD source")
        if f"    - {rel}" not in quarto:
            errors.append(f"{rel}: absent from explicit Quarto resources")
        if f"`{rel}`" not in history:
            errors.append(f"{rel}: absent from chapter history ledger")
        lowered = text.lower()
        if not any(boundary in lowered for boundary in ["support-state promotion", "no-support-state-promotion", "no support state"]):
            errors.append(f"{rel}: missing no-support-effect boundary")

    declared = set(re.findall(r"^\s+- (chapters/[^\s]+\.html)\s*$", quarto, re.M))
    actual = {path.relative_to(ROOT).as_posix() for path in html_files}
    if declared != actual:
        errors.append(f"Quarto redirect resources disagree with chapter HTML files: declared={sorted(declared)}, actual={sorted(actual)}")
    return errors


def main() -> None:
    errors = hygiene_errors()
    if errors:
        raise SystemExit("Chapter source hygiene validation failed:\n - " + "\n - ".join(errors))
    print("Chapter source hygiene passed: 10 declared historical redirects, 10 canonical active targets, no undeclared chapter HTML.")


if __name__ == "__main__":
    main()
