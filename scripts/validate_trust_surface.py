#!/usr/bin/env python3
"""Validate the first-minute public trust surface.

The trust surface is the compact public contract that tells cold readers what
is actually evidenced, what is still only argued, and what must not be inferred
from the book's internal proof/test/source machinery.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
READER_AUDIT = ROOT / "docs" / "reader_continuity_audit.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"

EXPECTED_NON_CORE = {
    "living-book-methodology.phase5_harness_registry_runner": "synthetic-test-backed",
    "resource-economics.costed_route_budget_slice": "synthetic-test-backed",
    "resource-economics.finite_burst_load_smoothing_selector": "synthetic-test-backed",
    "resource-economics.scoped_workflow_trace_route_selector": "empirical-test-backed",
    "circle-calculus.external_rope_receipt_replay": "prototype-backed",
    "compact-generative-systems.compact_gvr_receipt_slice": "synthetic-test-backed",
}

REQUIRED_LINKS = [
    "docs/v1_0_candidate_status.md",
    "docs/non_core_evidence_ledger.md",
    "docs/contribution_novelty_ledger.md",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/H_external_sources.qmd",
    "docs/external_review_status.md",
    "docs/reader_continuity_audit.md",
    "docs/v1_x_beyond_sota_roadmap.md",
]

REQUIRED_NON_CLAIMS = [
    "not a validated ASI implementation",
    "not a deployed safety system",
    "not a benchmark-proven architecture",
    "not a reviewed reader-release manuscript",
    "not proof of novelty",
    "no chapter-core promotion",
    "not exhaustive literature synthesis",
]

FORBIDDEN_OVERCLAIMS = [
    "chapter core claims are synthetic-test-backed",
    "chapter core claims are prototype-backed",
    "chapter core claims are external-literature-backed",
    "validated ASI implementation",
    "deployed safety system",
    "benchmark-proven architecture",
    "approved audiobook",
]


def fail(errors: list[str]) -> None:
    print("Trust-surface validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def chapter_count() -> int:
    structure = read_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    return sum(len(part.get("chapters", [])) for part in structure.get("parts", []))


def source_count() -> int:
    inventory = read_json(ROOT / "sources" / "source_inventory.json")
    if not isinstance(inventory, list):
        raise SystemExit("sources/source_inventory.json must contain a list.")
    return len(inventory)


def metric(report: str, label: str) -> str:
    pattern = re.compile(rf"^\|\s*{re.escape(label)}\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
    match = pattern.search(report)
    if not match:
        raise SystemExit(f"docs/reader_continuity_audit.md missing metric: {label}")
    return match.group(1).strip()


def assert_surface(
    errors: list[str],
    *,
    name: str,
    text: str,
    chapters: int,
    sources: int,
    high: str,
    medium: str,
    long_paragraphs: str,
    active_overlays: str,
) -> None:
    required = [
        "60-Second Trust Surface",
        f"{chapters} chapter core claims remain at `argument`",
        f"{sources} public-safe records",
        f"{chapters}/{chapters} chapters externally positioned",
        "0 explicit external-baseline exceptions",
        "Six narrow non-core transitions are accepted",
        f"{high} high-priority",
        f"{medium} medium-priority",
        f"{long_paragraphs} paragraphs at or above 160 words",
        f"{active_overlays} active/applied reader-overlay operations",
    ]
    for needle in required:
        if needle not in text:
            errors.append(f"{name} missing trust-surface text: {needle}")

    for link in REQUIRED_LINKS:
        if link not in text:
            errors.append(f"{name} missing trust-surface link: {link}")

    for claim_id, state in EXPECTED_NON_CORE.items():
        if claim_id not in text:
            errors.append(f"{name} missing non-core transition id: {claim_id}")
        if state not in text:
            errors.append(f"{name} missing non-core transition state: {state}")

    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in text:
            errors.append(f"{name} missing non-claim boundary: {phrase}")

    if "six narrow non-core transitions are accepted" not in text.lower():
        errors.append(f"{name} missing current six-transition count")

    lowered = text.lower()
    for phrase in FORBIDDEN_OVERCLAIMS:
        if phrase.lower() in lowered and f"not a {phrase.lower()}" not in lowered:
            errors.append(f"{name} contains unbounded overclaim phrase: {phrase}")


def main() -> None:
    errors: list[str] = []
    chapters = chapter_count()
    sources = source_count()
    reader_audit = read_text(READER_AUDIT)
    high = metric(reader_audit, "High-priority heuristic review chapters")
    medium = metric(reader_audit, "Medium-priority heuristic review chapters")
    long_paragraphs = metric(reader_audit, "Paragraphs at or above 160 words")
    active_overlays = metric(reader_audit, "Active reader overlay operations")

    readme = read_text(README)
    index = read_text(INDEX)
    status = read_text(STATUS)
    publication = read_text(PUBLICATION)

    for name, text in {
        "README.md": readme,
        "index.qmd": index,
    }.items():
        assert_surface(
            errors,
            name=name,
            text=text,
            chapters=chapters,
            sources=sources,
            high=high,
            medium=medium,
            long_paragraphs=long_paragraphs,
            active_overlays=active_overlays,
        )

    public_status_needles = [
        "The live Human view is a convenience projection, not a reviewed reader-release manuscript",
        "no chapter core claim support-state promotion",
        "All core chapter support states remain `argument`.",
    ]
    normalized_status = re.sub(r"\s+", " ", status)
    for needle in public_status_needles:
        if needle not in normalized_status:
            errors.append(f"docs/v1_0_candidate_status.md missing boundary text: {needle}")

    if "scripts/validate_trust_surface.py" not in publication:
        errors.append("docs/publication_readiness.md does not name scripts/validate_trust_surface.py")
    if "scripts/validate_trust_surface.py" not in readme:
        errors.append("README.md does not name scripts/validate_trust_surface.py")

    if errors:
        fail(errors)

    print(
        "Trust-surface validation passed: "
        f"{chapters} core claims at argument, "
        f"{len(EXPECTED_NON_CORE)} non-core transitions, "
        f"{high} high-priority reader rows, {medium} medium-priority reader rows."
    )


if __name__ == "__main__":
    main()
