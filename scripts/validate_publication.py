#!/usr/bin/env python3
"""Validate the public-facing repository surface."""

from __future__ import annotations

import json
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
    "claim_revisions/v1_x/manifest_core_claim_count_narrowing.json",
    "docs/external_review_packet.md",
    "docs/external_review_status.md",
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
    "external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json",
    "external_reviews/blockers/no_named_external_reviewer_2026-07-01.json",
    "docs/defended_contribution_tracks.md",
    "docs/defended_contribution_prior_art_positioning.md",
    "docs/evidence_laundering_prevention_case_studies.md",
    "docs/chapter_consolidation_sequence.md",
    "docs/chapter_consolidation_full_review_packet.md",
    "docs/chapter_external_grounding_status.md",
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
    "editions/reader_manuscript/v1_0/companion_notes/README.md",
    "editions/reader_manuscript/v1_0/audio_script_probe_manifest.json",
    "editions/reader_manuscript/v1_0/reconciliation_report.md",
    "docs/reader_companion_note_routing_review.md",
    "docs/reader_audio_script_probe_manifest.md",
    "docs/reader_chapter_review_matrix.md",
    "docs/reader_part_i_review_pass.md",
    "docs/reader_part_ii_review_pass.md",
    "docs/reader_part_iii_review_pass.md",
    "docs/reader_part_iv_review_pass.md",
    "docs/external_review_packet.md",
    "docs/external_review_status.md",
    "docs/chapter_external_grounding_status.md",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_source_appendices.py",
    "scripts/validate_trust_surface.py",
    "scripts/validate_v1_status_snapshot.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_release_profiles.py",
    "scripts/validate_release_reproducibility.py",
    "scripts/validate_public_site_accessibility.py",
    "scripts/validate_v1_release_gate_audit.py",
    "scripts/validate_circle_external_receipt_slice.py",
    "scripts/validate_non_core_evidence_ledger.py",
    "scripts/validate_claim_revision_records.py",
    "scripts/validate_external_review_status.py",
    "scripts/validate_external_review_intake.py",
    "scripts/validate_defended_contribution_tracks.py",
    "scripts/validate_defended_contribution_prior_art.py",
    "scripts/validate_evidence_laundering_case_studies.py",
    "scripts/validate_chapter_consolidation_sequence.py",
    "scripts/validate_core_claim_promotion_paths.py",
    "scripts/validate_chapter_external_grounding_status.py",
    "scripts/validate_external_sota_positioning.py",
    "assets/reading-mode.html",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/external-review.yml",
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
    "editions/reader_manuscript/v1_0/companion_notes/README.md",
    "editions/reader_manuscript/v1_0/audio_script_probe_manifest.json",
    "editions/reader_manuscript/v1_0/reconciliation_report.md",
    "docs/reader_companion_note_routing_review.md",
    "docs/reader_audio_script_probe_manifest.md",
    "docs/reader_chapter_review_matrix.md",
    "docs/reader_part_i_review_pass.md",
    "docs/reader_part_ii_review_pass.md",
    "docs/reader_part_iii_review_pass.md",
    "docs/reader_part_iv_review_pass.md",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_source_appendices.py",
    "scripts/validate_trust_surface.py",
    "scripts/validate_v1_status_snapshot.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_publication.py",
    "scripts/validate_release_reproducibility.py",
    "scripts/validate_public_site_accessibility.py",
    "scripts/validate_v1_release_gate_audit.py",
    "scripts/validate_circle_external_receipt_slice.py",
    "scripts/validate_non_core_evidence_ledger.py",
    "scripts/validate_claim_revision_records.py",
    "scripts/validate_external_review_status.py",
    "scripts/validate_external_review_intake.py",
    "external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json",
    "docs/chapter_consolidation_full_review_packet.md",
    "scripts/validate_defended_contribution_tracks.py",
    "scripts/validate_defended_contribution_prior_art.py",
    "scripts/validate_evidence_laundering_case_studies.py",
    "scripts/validate_chapter_consolidation_sequence.py",
    "scripts/validate_core_claim_promotion_paths.py",
    "scripts/validate_chapter_external_grounding_status.py",
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

PUBLIC_SURFACE_FILES = [
    "README.md",
    "index.qmd",
    "docs/publication_readiness.md",
]

FORBIDDEN_PUBLIC_STALE_STRINGS = [
    "160 inventoried records",
    "44 of 54 chapters currently have",
    "44 chapters have source-noted external comparators",
    "10 have explicit external-baseline exceptions",
    "10 carry explicit exceptions",
    "Most chapter-core claims, external-grounding upgrades",
    "Three narrow non-core evidence transitions accepted",
    "Three narrow non-core transitions",
    "three accepted non-core upward transitions",
    "147 proof targets",
    "168 proof targets",
    "177 proof targets",
    "Thirty-five synthetic",
    "Forty-one synthetic",
    "Forty-seven synthetic",
    "Forty-eight synthetic",
    "Four narrow non-core evidence transitions accepted",
    "Four narrow non-core transitions",
    "four accepted non-core upward transitions",
]


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


def read_json(path: str) -> object:
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)


def run_validator(script_name: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print(result.stdout.strip())
        sys.exit(result.returncode)


def manifest_chapter_count() -> int:
    structure = read_json("book_structure.json")
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    return sum(len(part.get("chapters", [])) for part in structure.get("parts", []))


def source_record_count() -> int:
    inventory = read_json("sources/source_inventory.json")
    if not isinstance(inventory, list):
        raise SystemExit("sources/source_inventory.json must contain a list.")
    return len(inventory)


def main() -> None:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            errors.append(f"Missing public-readiness file: {path}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    index = (ROOT / "index.qmd").read_text(encoding="utf-8", errors="ignore")
    publication = (ROOT / "docs/publication_readiness.md").read_text(
        encoding="utf-8", errors="ignore"
    )
    chapter_count = manifest_chapter_count()
    source_count = source_record_count()
    for needle in REQUIRED_README_STRINGS:
        if needle not in readme:
            errors.append(f"README.md is missing required public-readiness text: {needle}")

    public_texts = {
        "README.md": readme,
        "index.qmd": index,
        "docs/publication_readiness.md": publication,
    }
    for path, text in public_texts.items():
        for stale in FORBIDDEN_PUBLIC_STALE_STRINGS:
            if stale in text:
                errors.append(f"{path} contains stale public trust-surface text: {stale}")

    public_requirements = {
        "index.qmd": [
            f"{source_count} public-safe records",
            f"{chapter_count}/{chapter_count} chapters externally positioned",
            "0 explicit external-baseline exceptions",
            "Five narrow non-core evidence transitions accepted",
            "Five narrow non-core transitions are accepted",
        ],
        "README.md": [
            f"all {chapter_count} chapters have source-noted external positioning records",
            "0 explicit external-baseline exceptions",
            "Five narrow non-core transitions are accepted",
            f"{chapter_count} of {chapter_count} chapters currently have in-prose `ext_*` positioning",
            "0 carry explicit exceptions",
        ],
        "docs/publication_readiness.md": [
            f"{chapter_count} of {chapter_count} chapters currently have in-prose `ext_*` positioning",
            "0 have explicit external-baseline exceptions",
            f"{chapter_count} source-noted chapters",
            "0 explicit exceptions",
            "five accepted non-core upward transitions",
            "181 proof targets",
            "Fifty-three synthetic",
        ],
    }
    for path, needles in public_requirements.items():
        text = public_texts[path]
        for needle in needles:
            if needle not in text:
                errors.append(f"{path} is missing current public trust-surface text: {needle}")

    for path in git_ls_files():
        if path in FORBIDDEN_TRACKED_EXACT or path.endswith("/.DS_Store"):
            errors.append(f"Forbidden tracked local artifact: {path}")
        if any(path.startswith(prefix) for prefix in FORBIDDEN_TRACKED_PREFIXES):
            errors.append(f"Forbidden tracked generated/private path: {path}")

    if errors:
        fail(errors)

    run_validator("validate_trust_surface.py")
    print("Publication surface validation passed.")


if __name__ == "__main__":
    main()
