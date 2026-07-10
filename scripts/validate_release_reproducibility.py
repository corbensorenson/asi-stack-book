#!/usr/bin/env python3
"""Validate release reproducibility and v1.0.0 citation metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_WORKFLOW = ROOT / ".github" / "workflows" / "build-pages-artifact.yml"
DEPLOY_WORKFLOW = ROOT / ".github" / "workflows" / "publish.yml"
CURRENT_CITATION = ROOT / "CITATION.cff"
HISTORICAL_CITATION = ROOT / "citations" / "v1.0.0.cff"
DOC = ROOT / "docs" / "release_reproducibility.md"
LEAN_TOOLCHAIN = ROOT / "lean" / "lean-toolchain"


REQUIRED_WORKFLOW_FRAGMENTS = [
    "uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5",
    'python-version: "3.11"',
    "uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4",
    'node-version: "22"',
    "uses: quarto-dev/quarto-actions/setup@8a96df13519ee81fd526f2dfca5962811136661b # v2",
    'version: "1.9.38"',
    '$(cat lean/lean-toolchain)',
    "6737edca3d2ca3dbaa1b47b87769b48b420633ae/elan-init.sh",
    "a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53",
    "python3 scripts/run_validation_registry.py --tier deep",
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
    "citations/v1.0.0.cff",
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

    for path in [BUILD_WORKFLOW, DEPLOY_WORKFLOW, CURRENT_CITATION, HISTORICAL_CITATION, DOC, LEAN_TOOLCHAIN]:
        if not path.exists():
            errors.append(f"Missing required release reproducibility file: {path.relative_to(ROOT)}")

    if errors:
        fail(errors)

    workflow_text = BUILD_WORKFLOW.read_text(encoding="utf-8", errors="ignore") + "\n" + DEPLOY_WORKFLOW.read_text(encoding="utf-8", errors="ignore")
    citation_text = HISTORICAL_CITATION.read_text(encoding="utf-8", errors="ignore")
    current_citation_text = CURRENT_CITATION.read_text(encoding="utf-8", errors="ignore")
    doc_text = DOC.read_text(encoding="utf-8", errors="ignore")
    lean_toolchain = LEAN_TOOLCHAIN.read_text(encoding="utf-8").strip()

    errors.extend(missing_fragments(workflow_text, REQUIRED_WORKFLOW_FRAGMENTS, ".github/workflows/publish.yml"))
    errors.extend(missing_fragments(citation_text, REQUIRED_CITATION_FRAGMENTS, "citations/v1.0.0.cff"))
    if 'title: "The ASI Stack: A Governed Systems Architecture for Advanced AI, with ASI as the Stress Case"' not in current_citation_text:
        errors.append("CITATION.cff does not carry the active reframed title")
    errors.extend(missing_fragments(doc_text, REQUIRED_DOC_FRAGMENTS, "docs/release_reproducibility.md"))

    if lean_toolchain != "leanprover/lean4:v4.31.0":
        errors.append(f"lean/lean-toolchain is {lean_toolchain!r}, expected 'leanprover/lean4:v4.31.0'.")
    if f"| Lean | `{lean_toolchain}` |" not in doc_text:
        errors.append("docs/release_reproducibility.md does not mirror lean/lean-toolchain.")
    if re.search(r"\bDOI\s*:\s*10\.", doc_text, re.IGNORECASE):
        errors.append("docs/release_reproducibility.md appears to claim a DOI.")
    if "doi:" in citation_text.lower() or "doi:" in current_citation_text.lower():
        errors.append("Citation metadata must not include a DOI until one exists.")

    if errors:
        fail(errors)

    print("Release reproducibility validation passed.")


if __name__ == "__main__":
    main()
