#!/usr/bin/env python3
"""Validate the public-facing repository surface."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "CITATION.cff",
    "docs/repository_map.md",
    "docs/publication_readiness.md",
    "docs/book_outline.md",
    "editions/release_profiles.json",
    "appendices/G_bibliography.qmd",
    "appendices/H_external_literature.qmd",
    "appendices/J_release_editions.qmd",
    "proofs/proof_manifest.json",
    "scripts/build_reader_edition.py",
    "scripts/render_reader_formats.py",
    "scripts/validate_reader_spine.py",
    "scripts/validate_reading_mode_toggle.py",
    "scripts/validate_human_reading_paths.py",
    "scripts/validate_live_human_view.py",
    "scripts/validate_source_appendices.py",
    "scripts/validate_release_profiles.py",
    "assets/reading-mode.html",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/publish.yml",
]

REQUIRED_README_STRINGS = [
    "https://corbensorenson.github.io/asi-stack-book/",
    "docs/book_outline.md",
    "book_structure.json",
    "proofs/proof_manifest.json",
    "editions/release_profiles.json",
    "scripts/build_reader_edition.py",
    "scripts/render_reader_formats.py",
    "scripts/validate_reader_spine.py",
    "scripts/validate_human_reading_paths.py",
    "scripts/validate_live_human_view.py",
    "scripts/validate_source_appendices.py",
    "scripts/validate_publication.py",
    "Do not report a theorem as proven unless",
]

FORBIDDEN_TRACKED_PREFIXES = [
    "_site/",
    ".quarto/",
    "site_libs/",
    "sources/raw/google_docs/",
    "lean/.lake/",
]

FORBIDDEN_TRACKED_EXACT = {
    ".DS_Store",
    "index.html",
}


def fail(errors: list[str]) -> None:
    for error in errors:
        print(error)
    sys.exit(1)


def git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout.splitlines()


def main() -> None:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            errors.append(f"Missing public-readiness file: {path}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    for needle in REQUIRED_README_STRINGS:
        if needle not in readme:
            errors.append(f"README.md is missing required public-readiness text: {needle}")

    for path in git_ls_files():
        if path in FORBIDDEN_TRACKED_EXACT or path.endswith("/.DS_Store"):
            errors.append(f"Forbidden tracked local artifact: {path}")
        if any(path.startswith(prefix) for prefix in FORBIDDEN_TRACKED_PREFIXES):
            errors.append(f"Forbidden tracked generated/private path: {path}")

    if errors:
        fail(errors)

    print("Publication surface validation passed.")


if __name__ == "__main__":
    main()
