#!/usr/bin/env python3
"""Validate release reproducibility and v1.0.0 citation metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish.yml"
CITATION = ROOT / "CITATION.cff"
DOC = ROOT / "docs" / "release_reproducibility.md"
LEAN_TOOLCHAIN = ROOT / "lean" / "lean-toolchain"


REQUIRED_WORKFLOW_FRAGMENTS = [
    "uses: actions/setup-python@v5",
    'python-version: "3.11"',
    "uses: actions/setup-node@v4",
    'node-version: "22"',
    "uses: quarto-dev/quarto-actions/setup@v2",
    'version: "1.9.38"',
    '$(cat lean/lean-toolchain)',
    "python3 scripts/validate_release_reproducibility.py",
    "LANG: C.UTF-8",
    "LC_ALL: C.UTF-8",
]

REQUIRED_CITATION_FRAGMENTS = [
    "cff-version: 1.2.0",
    'version: "1.0.0"',
    'date-released: "2026-06-29"',
    "No DOI has been issued yet",
    'url: "https://corbensorenson.github.io/asi-stack-book/"',
    'repository-code: "https://github.com/corbensorenson/asi-stack-book"',
]

REQUIRED_DOC_FRAGMENTS = [
    "# Release Reproducibility",
    "| Quarto | `1.9.38` |",
    "| Python | `3.11` in CI; Python `3.9.23` is the current local validated interpreter |",
    "| Node | `22` in CI; `v22.15.0` is the current local validated runtime |",
    "| Lean | `leanprover/lean4:v4.31.0` |",
    "| `libreoffice` | not found on `PATH` in the current shell during this audit |",
    "The current shell reports `LANG=C.UTF-8` and `LC_ALL=C`.",
    "LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8",
    "version `1.0.0`",
    "tag `v1.0.0` at commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`",
    "release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json",
    "no DOI or Zenodo archive has been issued",
    "Include tag `v1.0.0` and source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`.",
    "This file does not claim that a DOI exists",
]


def fail(errors: list[str]) -> None:
    print("Release reproducibility validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def missing_fragments(text: str, fragments: list[str], label: str) -> list[str]:
    return [f"{label} is missing required text: {fragment}" for fragment in fragments if fragment not in text]


def main() -> None:
    errors: list[str] = []

    for path in [WORKFLOW, CITATION, DOC, LEAN_TOOLCHAIN]:
        if not path.exists():
            errors.append(f"Missing required release reproducibility file: {path.relative_to(ROOT)}")

    if errors:
        fail(errors)

    workflow_text = WORKFLOW.read_text(encoding="utf-8", errors="ignore")
    citation_text = CITATION.read_text(encoding="utf-8", errors="ignore")
    doc_text = DOC.read_text(encoding="utf-8", errors="ignore")
    lean_toolchain = LEAN_TOOLCHAIN.read_text(encoding="utf-8").strip()

    errors.extend(missing_fragments(workflow_text, REQUIRED_WORKFLOW_FRAGMENTS, ".github/workflows/publish.yml"))
    errors.extend(missing_fragments(citation_text, REQUIRED_CITATION_FRAGMENTS, "CITATION.cff"))
    errors.extend(missing_fragments(doc_text, REQUIRED_DOC_FRAGMENTS, "docs/release_reproducibility.md"))

    if lean_toolchain != "leanprover/lean4:v4.31.0":
        errors.append(f"lean/lean-toolchain is {lean_toolchain!r}, expected 'leanprover/lean4:v4.31.0'.")
    if f"| Lean | `{lean_toolchain}` |" not in doc_text:
        errors.append("docs/release_reproducibility.md does not mirror lean/lean-toolchain.")
    if re.search(r"\bDOI\s*:\s*10\.", doc_text, re.IGNORECASE):
        errors.append("docs/release_reproducibility.md appears to claim a DOI.")
    if "doi:" in citation_text.lower():
        errors.append("CITATION.cff must not include DOI metadata until a DOI exists.")

    if errors:
        fail(errors)

    print("Release reproducibility validation passed.")


if __name__ == "__main__":
    main()
