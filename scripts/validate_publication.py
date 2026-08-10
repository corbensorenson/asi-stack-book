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
    "docs/living_update_workflow.md",
    "docs/book_outline.md",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json",
    "docs/publication_readiness.md",
    "docs/external_review_status.md",
    "docs/core_claim_disposition_ledger.md",
    "docs/non_core_evidence_ledger.md",
    "docs/contribution_novelty_ledger.md",
    "editions/release_profiles.json",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/H_external_sources.qmd",
    "appendices/J_release_editions.qmd",
    "proofs/proof_manifest.json",
    "scripts/sync_scaffold.py",
    "scripts/sync_proof_manifest.py",
    "scripts/validate_live_human_view.py",
    "scripts/validate_live_human_view_browser.js",
    "scripts/validate_source_appendices.py",
    "scripts/validate_paper_library.py",
    "scripts/validate_trust_surface.py",
    "scripts/validate_outline_consistency.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_release_profiles.py",
    "assets/reading-mode.html",
    "papers/paper_library.json",
    "papers/index.qmd",
    "schemas/paper_library.schema.json",
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
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "docs/repository_map.md",
    "docs/living_update_workflow.md",
    "Do not report a theorem as proven unless",
]

FORBIDDEN_TRACKED_PREFIXES = [
    "_site/",
    ".quarto/",
    "site_libs/",
    "build/",
    "sources/raw/google_docs/",
    "lean/.lake/",
]

FORBIDDEN_TRACKED_EXACT = {
    ".DS_Store",
    "index.html",
}

ROOT_TRACKED_ALLOWLIST = {
    ".gitattributes",
    ".gitignore",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "NOTICE.md",
    "README.md",
    "_quarto.yml",
    "book_structure.json",
    "index.qmd",
    "preface.qmd",
}

PRIVATE_BOUNDARY_ALLOWLISTS = {
    "sources/raw/": {"sources/raw/README.md"},
    "sources/inbox/": {"sources/inbox/README.md"},
    "_archive/": {"_archive/README.md"},
}

LARGE_TRACKED_FILE_THRESHOLD_BYTES = 40 * 1024 * 1024
MAX_TRACKED_FILE_BYTES = 60 * 1024 * 1024
LARGE_TRACKED_FILE_ALLOWLIST = {
    "evidence_quality/claim_atom_registry.json",
    "experiments/p4_situated_world_model/raw/campaign_run.json",
}

REPOSITORY_MAP_REQUIRED_STRINGS = [
    "## Authority order",
    "## Storage and lifecycle classes",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "Earlier roadmaps are immutable execution history",
    "Tracked files above 40 MiB",
    "60 MiB is the project hard ceiling",
    "Exactly one current record may correspond to the active-roadmap marker",
]

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
    "147 proof targets",
    "168 proof targets",
    "177 proof targets",
    "203 proof targets",
    "Thirty-five synthetic",
    "Forty-one synthetic",
    "Forty-seven synthetic",
    "Forty-eight synthetic",
    "Sixty-four synthetic",
    "Four narrow non-core evidence transitions accepted",
    "Four narrow non-core transitions",
    "four accepted non-core upward transitions",
    "Five narrow non-core evidence transitions accepted",
    "Five narrow non-core transitions",
    "Six narrow non-core evidence transitions accepted",
    "Six narrow non-core transitions",
    "six accepted non-core upward transitions",
    "Seven narrow non-core evidence transitions accepted",
    "Seven narrow non-core transitions",
    "seven accepted non-core upward transitions",
    "Eight narrow non-core evidence transitions accepted",
    "Eight narrow non-core transitions",
    "eight accepted non-core upward transitions",
    "Nine narrow non-core evidence transitions accepted",
    "Nine narrow non-core transitions",
    "nine accepted non-core upward transitions",
    "Ten narrow non-core evidence transitions accepted",
    "Ten narrow non-core transitions",
    "ten accepted non-core upward transitions",
    "Eleven narrow non-core evidence transitions accepted",
    "Eleven narrow non-core transitions",
    "eleven accepted non-core upward transitions",
    "Thirteen narrow non-core evidence transitions accepted",
    "Thirteen narrow non-core transitions",
    "thirteen accepted non-core upward transitions",
    "207 proof targets",
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
    repository_map = (ROOT / "docs/repository_map.md").read_text(
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

    for needle in REPOSITORY_MAP_REQUIRED_STRINGS:
        if needle not in repository_map:
            errors.append(f"docs/repository_map.md is missing repository authority text: {needle}")

    public_requirements = {
        "index.qmd": [
            f"{source_count} public-safe records",
            f"{chapter_count}/{chapter_count} chapters externally positioned",
            "0 explicit external-baseline exceptions",
            "The 25 accepted non-core upward evidence transitions are recorded in",
        ],
        "README.md": [
            f"{chapter_count}/{chapter_count} chapters are externally positioned",
            "0 explicit external-baseline exceptions",
            "The 25 accepted non-core upward evidence transitions are recorded in",
        ],
        "docs/publication_readiness.md": [
            f"{chapter_count} of {chapter_count} chapters currently have in-prose `ext_*` positioning",
            "0 have explicit external-baseline exceptions",
            f"{chapter_count} source-noted chapters",
            "0 explicit exceptions",
            "twenty-five accepted non-core upward transitions",
            "298 proof targets",
            "Seventy-one synthetic",
        ],
    }
    for path, needles in public_requirements.items():
        text = public_texts[path]
        for needle in needles:
            if needle not in text:
                errors.append(f"{path} is missing current public trust-surface text: {needle}")

    tracked_paths = git_ls_files()
    for path in tracked_paths:
        if not (ROOT / path).exists():
            # `git ls-files` includes an unstaged deletion. Canonical missing
            # files are already handled by REQUIRED_FILES.
            continue
        if path in FORBIDDEN_TRACKED_EXACT or path.endswith("/.DS_Store"):
            errors.append(f"Forbidden tracked local artifact: {path}")
        if any(path.startswith(prefix) for prefix in FORBIDDEN_TRACKED_PREFIXES):
            errors.append(f"Forbidden tracked generated/private path: {path}")
        if "/" not in path and path not in ROOT_TRACKED_ALLOWLIST:
            errors.append(f"Unexpected tracked repository-root artifact: {path}")
        for prefix, allowlist in PRIVATE_BOUNDARY_ALLOWLISTS.items():
            if path.startswith(prefix) and path not in allowlist:
                errors.append(f"Forbidden tracked private/local-history path: {path}")
        size = (ROOT / path).stat().st_size
        if size > MAX_TRACKED_FILE_BYTES:
            errors.append(
                f"Tracked file exceeds the 60 MiB repository ceiling: {path} ({size} bytes)"
            )
        elif size > LARGE_TRACKED_FILE_THRESHOLD_BYTES and path not in LARGE_TRACKED_FILE_ALLOWLIST:
            errors.append(
                f"Tracked file above 40 MiB lacks an explicit evidence allowlist entry: {path} ({size} bytes)"
            )

    missing_large_allowlist = sorted(LARGE_TRACKED_FILE_ALLOWLIST - set(tracked_paths))
    if missing_large_allowlist:
        errors.append(f"Large-file allowlist contains missing paths: {missing_large_allowlist}")

    if errors:
        fail(errors)

    run_validator("validate_paper_library.py")
    run_validator("validate_trust_surface.py")
    print("Publication surface validation passed.")


if __name__ == "__main__":
    main()
