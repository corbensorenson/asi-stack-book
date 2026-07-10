#!/usr/bin/env python3
"""Validate deferred external-review history and no-prepublication-outreach policy.

This check is local-only. It does not call GitHub and does not claim an
independent review exists; it verifies that the public request and status
records preserve the review-is-not-evidence boundary without soliciting review.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/external_review_packet.md",
    "docs/external_review_status.md",
    "docs/chapter_consolidation_external_review_packet.md",
    "docs/chapter_consolidation_full_review_packet.md",
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
    "external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json",
    "external_reviews/blockers/no_named_external_reviewer_2026-07-01.json",
    "scripts/validate_external_review_intake.py",
]

ISSUE_URL = "https://github.com/corbensorenson/asi-stack-book/issues/1"
CONSOLIDATION_COMMENT_URL = (
    "https://github.com/corbensorenson/asi-stack-book/issues/1#issuecomment-4835627101"
)
FULL_CONSOLIDATION_COMMENT_URL = (
    "https://github.com/corbensorenson/asi-stack-book/issues/1#issuecomment-4837313658"
)

REQUIRED_STATUS_STRINGS = [
    ISSUE_URL,
    CONSOLIDATION_COMMENT_URL,
    FULL_CONSOLIDATION_COMMENT_URL,
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
    "external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json",
    "external_reviews/blockers/no_named_external_reviewer_2026-07-01.json",
    "governance/external_review_program.json",
    "governance/reviewer_capacity_registry.json",
    "no external-human review, outreach, or reader approval is a prepublication gate",
    "deferred_postpublication",
    "no independent external review has been accepted yet",
    "no named independent reviewer response or approved direct outreach target",
    "Review input remains separate from evidence.",
    "cannot by itself promote a claim",
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

REQUIRED_FULL_PACKET_STRINGS = [
    ISSUE_URL,
    "request surface",
    "Decision Queue Under Review",
    "Execute, revise, defer, reject, or no opinion",
    "Reviewer comments are review input, not source evidence",
    "Accepted Review Record Requirements",
    "This packet does not authorize any merge or fold.",
    "This packet does not change `book_structure.json`.",
]

PUBLIC_SURFACE_REFS = [
    ("README.md", "docs/external_review_status.md"),
    ("README.md", "docs/chapter_consolidation_full_review_packet.md"),
    ("README.md", "external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json"),
    ("index.qmd", "docs/external_review_status.md"),
    ("docs/publication_readiness.md", "docs/external_review_status.md"),
    ("docs/publication_readiness.md", "docs/chapter_consolidation_full_review_packet.md"),
    ("docs/repository_map.md", "docs/external_review_packet.md"),
    ("docs/repository_map.md", "docs/chapter_consolidation_full_review_packet.md"),
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
    full_packet = read("docs/chapter_consolidation_full_review_packet.md")

    for needle in REQUIRED_STATUS_STRINGS:
        if needle not in status:
            errors.append(f"external review status missing: {needle}")
    for needle in REQUIRED_PACKET_STRINGS:
        if needle not in packet:
            errors.append(f"external review packet missing: {needle}")
    for needle in REQUIRED_FULL_PACKET_STRINGS:
        if needle not in full_packet:
            errors.append(f"full consolidation review packet missing: {needle}")
    combined = "\n".join([status, packet, full_packet])
    for forbidden in FORBIDDEN_STRINGS:
        if forbidden in combined:
            errors.append(f"external-review surfaces contain overclaim: {forbidden}")

    for path, needle in PUBLIC_SURFACE_REFS:
        text = read(path)
        if needle not in text:
            errors.append(f"{path} does not reference {needle}")

    if errors:
        fail(errors)

    print("External review status validation passed: historical request preserved, no prepublication outreach, and no accepted independent review claimed.")


if __name__ == "__main__":
    main()
