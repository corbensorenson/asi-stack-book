#!/usr/bin/env python3
"""Validate external-review request/status surfaces.

This check is local-only. It does not call GitHub and does not claim an
independent review exists; it verifies that the public request and status
records preserve the review-is-not-evidence boundary.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/external_review_packet.md",
    "docs/external_review_status.md",
    "docs/chapter_consolidation_external_review_packet.md",
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
    "scripts/validate_external_review_intake.py",
    ".github/ISSUE_TEMPLATE/external-review.yml",
]

ISSUE_URL = "https://github.com/corbensorenson/asi-stack-book/issues/1"
CONSOLIDATION_COMMENT_URL = (
    "https://github.com/corbensorenson/asi-stack-book/issues/1#issuecomment-4835627101"
)

REQUIRED_STATUS_STRINGS = [
    ISSUE_URL,
    CONSOLIDATION_COMMENT_URL,
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
    "scripts/validate_external_review_intake.py",
    "Requested publicly; no independent external review has been accepted yet.",
    "Support-state effect | None.",
    "Artifact-release effect | None.",
    "review input, not source evidence",
    "does not promote any chapter core claim above `argument`",
]

REQUIRED_PACKET_STRINGS = [
    ISSUE_URL,
    "docs/chapter_consolidation_external_review_packet.md",
    "External review is review input.",
    "support-state transition",
    "AI safety",
    "formal methods",
    "v1.x roadmap",
]

REQUIRED_TEMPLATE_STRINGS = [
    "name: External review",
    "Reviewer background",
    "Review scope",
    "Strongest issue",
    "Recommended actions",
    "I understand this review is not itself source evidence",
]

PUBLIC_SURFACE_REFS = [
    ("README.md", "docs/external_review_status.md"),
    ("index.qmd", ISSUE_URL),
    ("docs/publication_readiness.md", "docs/external_review_status.md"),
    ("docs/repository_map.md", "docs/external_review_packet.md"),
]

FORBIDDEN_STRINGS = [
    "external review accepted",
    "review proves",
    "review validates the architecture",
    "review promotes",
    "artifact approved by reviewer",
]


def fail(errors: list[str]) -> None:
    print("External review status validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def main() -> None:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            errors.append(f"missing required external-review file: {path}")

    if errors:
        fail(errors)

    status = read("docs/external_review_status.md")
    packet = read("docs/external_review_packet.md")
    template = read(".github/ISSUE_TEMPLATE/external-review.yml")

    for needle in REQUIRED_STATUS_STRINGS:
        if needle not in status:
            errors.append(f"external review status missing: {needle}")
    for needle in REQUIRED_PACKET_STRINGS:
        if needle not in packet:
            errors.append(f"external review packet missing: {needle}")
    for needle in REQUIRED_TEMPLATE_STRINGS:
        if needle not in template:
            errors.append(f"external review issue template missing: {needle}")

    combined = "\n".join([status, packet, template])
    for forbidden in FORBIDDEN_STRINGS:
        if forbidden in combined:
            errors.append(f"external-review surfaces contain overclaim: {forbidden}")

    for path, needle in PUBLIC_SURFACE_REFS:
        text = read(path)
        if needle not in text:
            errors.append(f"{path} does not reference {needle}")

    if errors:
        fail(errors)

    print("External review status validation passed: public request recorded, no accepted external review claimed.")


if __name__ == "__main__":
    main()
