#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "evidence_laundering_prevention_case_studies.md"
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
SCORECARD = ROOT / "docs" / "a_plus_quality_scorecard.md"
TRACKS = ROOT / "docs" / "defended_contribution_tracks.md"
PRIOR_ART = ROOT / "docs" / "defended_contribution_prior_art_positioning.md"
REPOSITORY_MAP = ROOT / "docs" / "repository_map.md"

REQUIRED_CASES = (
    "Project Theseus Static Import Did Not Become Self-Improvement Evidence",
    "Circle Consumer Gate Did Not Become Proof-Contract Deployment Evidence",
    "Reader HTML Release Did Not Approve EPUB, DOCX, PDF, Audio, Or Claims",
)

REQUIRED_REFS = (
    "docs/theseus_report_import_slice.md",
    "docs/circle_public_replay_consumer_gate.md",
    "docs/reader_html_artifact_browser_review.md",
    "release_records/2026-06-29-v1-reader-html-855dc277.json",
)

BOUNDARY_FRAGMENTS = (
    "No-promotion / anti-laundering examples",
    "all 45 chapter core claims remain `argument`",
    "True demotion/refutation example | Still missing",
    "not a new evidence-transition record",
    "not a demotion/refutation event",
    "not accepted external review",
    "does not promote any chapter core claim above `argument`",
    "does not demote or refute any chapter core claim",
    "does not create accepted external review",
)

PUBLIC_REFERENCE = "docs/evidence_laundering_prevention_case_studies.md"
VALIDATOR_REFERENCE = "scripts/validate_evidence_laundering_case_studies.py"


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def main() -> None:
    errors: list[str] = []

    try:
        text = read(DOC)
    except FileNotFoundError:
        print("Missing docs/evidence_laundering_prevention_case_studies.md")
        sys.exit(1)

    for title in REQUIRED_CASES:
        if title not in text:
            errors.append(f"Missing case study: {title}")

    for relative in REQUIRED_REFS:
        if not (ROOT / relative).exists():
            errors.append(f"Referenced evidence boundary file does not exist: {relative}")
        if relative not in text:
            errors.append(f"Case-study record does not reference {relative}")

    for fragment in BOUNDARY_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Case-study record missing boundary fragment: {fragment}")

    for path in (README, PUBLICATION, ROADMAP, SCORECARD, TRACKS, PRIOR_ART, REPOSITORY_MAP):
        public_text = read(path)
        if PUBLIC_REFERENCE not in public_text:
            errors.append(f"{path.relative_to(ROOT)} missing public reference to {PUBLIC_REFERENCE}")

    for path in (README, PUBLICATION, REPOSITORY_MAP):
        public_text = read(path)
        if VALIDATOR_REFERENCE not in public_text:
            errors.append(f"{path.relative_to(ROOT)} missing public reference to {VALIDATOR_REFERENCE}")

    if errors:
        print("Evidence-laundering case-study validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Evidence-laundering case-study validation passed: "
        f"{len(REQUIRED_CASES)} no-promotion examples recorded with demotion/refutation gap preserved."
    )


if __name__ == "__main__":
    main()
