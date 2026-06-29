#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "architecture_red_team_review.md"

REQUIRED_SECTIONS = [
    "## Authority Ladder Attack",
    "## SCIF/Context Leakage Attack",
    "## Evaluator Capture Attack",
    "## Support-State Inflation Attack",
    "## Benchmark Gaming Attack",
    "## Reader-Release Laundering Attack",
]

REQUIRED_FIELDS = [
    "**Attack setup:**",
    "**Expected failure:**",
    "**Observed current defense:**",
    "**Residual risk:**",
    "**Routed follow-up:**",
]

REQUIRED_NON_CLAIMS = [
    "not an exploit run",
    "does not prove the ASI Stack is safe",
    "does not promote any chapter core claim above `argument`",
    "does not approve any reader, ebook, document, PDF, audio, DOI, release, or benchmark artifact",
]


def main() -> None:
    text = REPORT.read_text(encoding="utf-8", errors="ignore")
    errors: list[str] = []

    if "Status: planned" in text:
        errors.append("architecture red-team report still says planned.")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"Missing required red-team section: {section}")
            continue
        start = text.index(section)
        next_section = text.find("\n## ", start + 1)
        section_text = text[start: next_section if next_section != -1 else len(text)]
        for field in REQUIRED_FIELDS:
            if field not in section_text:
                errors.append(f"{section} missing field {field}")

    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in text:
            errors.append(f"Missing non-claim phrase: {phrase}")

    if errors:
        print("Architecture red-team validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Architecture red-team validation passed: {len(REQUIRED_SECTIONS)} scenario(s).")


if __name__ == "__main__":
    main()
