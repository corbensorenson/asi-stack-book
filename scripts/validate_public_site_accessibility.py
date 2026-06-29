#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCESSIBILITY_REVIEW = ROOT / "docs" / "public_site_accessibility_review.md"
PROGRESS_LEDGER = ROOT / "docs" / "v1_progress_ledger.md"
SITE_VISUAL_REVIEW = ROOT / "docs" / "site_visual_phase7_review.md"
SITE_QUALITY_STANDARD = ROOT / "docs" / "site_quality_standard.md"
READING_MODE = ROOT / "assets" / "reading-mode.html"
STYLES = ROOT / "assets" / "styles.scss"
INDEX = ROOT / "index.qmd"
STRUCTURE = ROOT / "book_structure.json"

WALKTHROUGH_RE = re.compile(
    r"\*\*((?:How to read (?:the|this) [^:\n*]{3,80}|"
    r"Reading (?:the|this) [^:\n*]{3,80}|"
    r"What (?:the|this) [^:\n*]{3,80} shows)):\*\*",
    re.IGNORECASE,
)
MERMAID_RE = re.compile(r"```(?:\{mermaid\}|mermaid)\s*\n(.*?)\n```", re.DOTALL)

ACCESSIBILITY_SECTIONS = (
    "# Public Site Accessibility Readiness Review",
    "## Scope",
    "## Evidence Reviewed",
    "## Accessibility Readiness Matrix",
    "## Residuals",
    "## Validation Command",
    "## Non-Claims",
)

ACCESSIBILITY_FRAGMENTS = (
    "not an accessibility certification",
    "does not claim WCAG conformance",
    "does not certify the site as fully accessible",
    "AI view",
    "Human view",
    "role=\"status\"",
    "aria-live=\"polite\"",
    "aria-pressed",
    "fig-alt",
    "contained Mermaid scrolling",
    "diagram walkthrough note",
    "manual keyboard-only pass",
    "screen-reader pass",
    "EPUB e-reader application review",
    "DOCX application review",
    "PDF page-by-page layout review",
    "does not promote any chapter core claim above `argument`",
)

ACCESSIBILITY_SURFACES = (
    "| Reading-mode switch |",
    "| AI/Human view projection |",
    "| Mermaid diagrams |",
    "| Diagram text equivalents |",
    "| Landing image |",
    "| Tables and appendices |",
    "| Color and contrast |",
    "| Keyboard and focus |",
    "| Screen reader |",
    "| E-reader and reader artifacts |",
    "| Release/status language |",
)

PROGRESS_SECTIONS = (
    "# v1.0 Progress Ledger",
    "## Phase Ledger",
    "## Current Release Classification",
    "## Next Work Queue",
    "## Non-Claims",
)

PROGRESS_FRAGMENTS = (
    "not a final v1.0 evidence release",
    "| Phase 0 |",
    "| Phase 1 |",
    "| Phase 2 |",
    "| Phase 3 |",
    "| Phase 3B |",
    "| Phase 4 |",
    "| Phase 5 |",
    "| Phase 5A |",
    "| Phase 6 |",
    "| Phase 7 |",
    "| Phase 7A |",
    "| Phase 8 |",
    "| Phase 9 |",
    "all chapter core claims remain at `argument`",
    "final v1.0 tag, DOI/Zenodo archive, and final release citation metadata are still pending",
    "does not promote any chapter core claim above `argument`",
)

ASSET_FRAGMENTS = {
    "assets/reading-mode.html": (
        'control.setAttribute("aria-describedby", "asi-reading-mode-description")',
        'role="status"',
        'aria-live="polite"',
        "aria-pressed",
        "Switch to",
        "AI/research view active.",
        "Human view active.",
    ),
    "assets/styles.scss": (
        ".asi-sr-only",
        ":focus-visible",
        "overflow-x: auto",
        '@media (max-width: 640px)',
        'svg[id^="mermaid"]',
        "min-width: 46rem",
        "word-break: break-word",
    ),
    "index.qmd": (
        "assets/images/asi-stack-hero.png",
        "fig-alt=",
        "Layered conceptual architecture for the ASI Stack",
    ),
}

BAD_CLAIMS = (
    "WCAG compliant",
    "WCAG-certified",
    "accessibility-certified",
    "site is fully accessible",
    "screen-reader approved",
    "keyboard-accessible for all users",
)


def fail(errors: list[str]) -> None:
    print("Public-site accessibility validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{owner} missing required fragment: {fragment}")


def validate_accessibility_review(errors: list[str]) -> None:
    if not ACCESSIBILITY_REVIEW.exists():
        errors.append("Missing docs/public_site_accessibility_review.md")
        return
    text = read(ACCESSIBILITY_REVIEW)
    require_fragments("docs/public_site_accessibility_review.md", text, ACCESSIBILITY_SECTIONS, errors)
    require_fragments("docs/public_site_accessibility_review.md", text, ACCESSIBILITY_FRAGMENTS, errors)
    require_fragments("docs/public_site_accessibility_review.md", text, ACCESSIBILITY_SURFACES, errors)
    for bad_claim in BAD_CLAIMS:
        if bad_claim in text:
            errors.append(
                "docs/public_site_accessibility_review.md contains unsupported accessibility claim: "
                f"{bad_claim}"
            )


def validate_progress_ledger(errors: list[str]) -> None:
    if not PROGRESS_LEDGER.exists():
        errors.append("Missing docs/v1_progress_ledger.md")
        return
    text = read(PROGRESS_LEDGER)
    require_fragments("docs/v1_progress_ledger.md", text, PROGRESS_SECTIONS, errors)
    require_fragments("docs/v1_progress_ledger.md", text, PROGRESS_FRAGMENTS, errors)


def validate_assets(errors: list[str]) -> None:
    for relative, fragments in ASSET_FRAGMENTS.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"Missing {relative}")
            continue
        require_fragments(relative, read(path), fragments, errors)


def validate_diagram_walkthroughs(errors: list[str]) -> None:
    structure = json.loads(read(STRUCTURE))
    chapters = [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]
    missing_diagrams: list[str] = []
    missing_walkthroughs: list[str] = []
    for chapter in chapters:
        path = ROOT / str(chapter.get("file", ""))
        text = read(path)
        if not MERMAID_RE.search(text):
            missing_diagrams.append(str(chapter.get("file", "")))
        if not WALKTHROUGH_RE.search(text):
            missing_walkthroughs.append(str(chapter.get("file", "")))
    if missing_diagrams:
        errors.append(f"Chapters missing Mermaid diagrams: {missing_diagrams}")
    if missing_walkthroughs:
        errors.append(f"Chapters missing diagram walkthrough notes: {missing_walkthroughs}")


def validate_cross_references(errors: list[str]) -> None:
    for path in (SITE_VISUAL_REVIEW, SITE_QUALITY_STANDARD):
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
    site_visual_text = read(SITE_VISUAL_REVIEW) if SITE_VISUAL_REVIEW.exists() else ""
    if "not an accessibility certification" not in site_visual_text:
        errors.append("docs/site_visual_phase7_review.md must preserve accessibility non-certification boundary.")
    site_quality_text = read(SITE_QUALITY_STANDARD) if SITE_QUALITY_STANDARD.exists() else ""
    if "python3 scripts/validate_public_site_accessibility.py" not in site_quality_text:
        errors.append("docs/site_quality_standard.md must list validate_public_site_accessibility.py.")


def main() -> None:
    errors: list[str] = []
    validate_accessibility_review(errors)
    validate_progress_ledger(errors)
    validate_assets(errors)
    validate_diagram_walkthroughs(errors)
    validate_cross_references(errors)
    if errors:
        fail(errors)
    print("Public-site accessibility validation passed: readiness review, progress ledger, assets, and diagram text equivalents checked.")


if __name__ == "__main__":
    main()
