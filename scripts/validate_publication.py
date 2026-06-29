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
    "docs/release_reproducibility.md",
    "docs/public_site_accessibility_review.md",
    "docs/v1_progress_ledger.md",
    "docs/v1_0_release_gate_audit.md",
    "docs/circle_external_receipt_slice.md",
    "docs/non_core_evidence_ledger.md",
    "docs/external_sota_positioning_audit.md",
    "docs/book_outline.md",
    "editions/release_profiles.json",
    "editions/reader_overlays/README.md",
    "editions/reader_overlays/v1_0/manifest.json",
    "assets/reader-overlays.html",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/H_external_sources.qmd",
    "appendices/J_release_editions.qmd",
    "proofs/proof_manifest.json",
    "scripts/build_reader_edition.py",
    "scripts/sync_reader_overlay_asset.py",
    "scripts/render_reader_formats.py",
    "scripts/inspect_reader_format_artifacts.py",
    "scripts/validate_reader_spine.py",
    "scripts/validate_reading_mode_toggle.py",
    "scripts/validate_human_reading_paths.py",
    "scripts/validate_reader_evidence_boundaries.py",
    "scripts/validate_reader_overlays.py",
    "scripts/sync_reader_chapter_review_matrix.py",
    "editions/reader_manuscript/v1_0/chapter_review_matrix.json",
    "editions/reader_manuscript/v1_0/companion_note_routing.json",
    "editions/reader_manuscript/v1_0/reconciliation_report.md",
    "docs/reader_companion_note_routing_review.md",
    "docs/reader_chapter_review_matrix.md",
    "docs/reader_part_i_review_pass.md",
    "docs/reader_part_ii_review_pass.md",
    "docs/reader_part_iii_review_pass.md",
    "docs/reader_part_iv_review_pass.md",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_source_appendices.py",
    "scripts/validate_v1_status_snapshot.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_release_profiles.py",
    "scripts/validate_release_reproducibility.py",
    "scripts/validate_public_site_accessibility.py",
    "scripts/validate_v1_release_gate_audit.py",
    "scripts/validate_circle_external_receipt_slice.py",
    "scripts/validate_non_core_evidence_ledger.py",
    "scripts/validate_external_sota_positioning.py",
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
    "scripts/sync_reader_overlay_asset.py",
    "editions/reader_overlays/README.md",
    "editions/reader_overlays/v1_0/manifest.json",
    "assets/reader-overlays.html",
    "scripts/render_reader_formats.py",
    "scripts/inspect_reader_format_artifacts.py",
    "scripts/validate_reader_spine.py",
    "scripts/validate_human_reading_paths.py",
    "scripts/validate_reader_evidence_boundaries.py",
    "scripts/validate_reader_overlays.py",
    "scripts/sync_reader_chapter_review_matrix.py",
    "editions/reader_manuscript/v1_0/chapter_review_matrix.json",
    "editions/reader_manuscript/v1_0/companion_note_routing.json",
    "editions/reader_manuscript/v1_0/reconciliation_report.md",
    "docs/reader_companion_note_routing_review.md",
    "docs/reader_chapter_review_matrix.md",
    "docs/reader_part_i_review_pass.md",
    "docs/reader_part_ii_review_pass.md",
    "docs/reader_part_iii_review_pass.md",
    "docs/reader_part_iv_review_pass.md",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_source_appendices.py",
    "scripts/validate_v1_status_snapshot.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_publication.py",
    "scripts/validate_release_reproducibility.py",
    "scripts/validate_public_site_accessibility.py",
    "scripts/validate_v1_release_gate_audit.py",
    "scripts/validate_circle_external_receipt_slice.py",
    "scripts/validate_non_core_evidence_ledger.py",
    "scripts/validate_external_sota_positioning.py",
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
