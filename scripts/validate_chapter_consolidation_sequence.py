#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SEQUENCE = ROOT / "docs" / "chapter_consolidation_sequence.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
REPOSITORY_MAP = ROOT / "docs" / "repository_map.md"
STRUCTURE = ROOT / "book_structure.json"

REQUIRED_IDS = {
    "constitutional-alignment-substrate",
    "agency-dignity-and-corrigibility",
    "moral-uncertainty-and-value-conflict",
    "governance-rights-fork-exit-and-audit",
    "compact-generative-systems-and-residual-honesty",
    "generate-verify-repair-compression",
    "rankfold-neuralfold-and-artifact-compression",
    "intent-to-execution-contracts",
    "command-contracts-and-semantic-interfaces",
    "human-intent-as-a-formal-input",
    "virtual-context-abi",
    "semantic-pages-context-cells-and-certificates",
    "context-transactions-snapshots-mounts-and-taint",
    "verification-bandwidth-and-context-adequacy",
    "spinoza-verification-and-proof-carrying-claims",
    "unified-adaptive-tribunal-and-adversarial-review",
    "claim-ledgers-and-belief-revision",
    "planning-as-a-control-layer",
    "planforge-dags-and-intelligence-arbitrage",
    "cognitive-compilation-and-semantic-ir",
    "moecot-runtime-and-multi-core-orchestration",
    "routing-heads-and-specialist-cores",
    "simulation-fidelity-and-physical-constraints",
    "resource-economics-and-token-budgets",
    "semantic-representation-and-tree-structured-models",
    "labor-os-and-typed-jobs",
    "runtime-adapters-tool-permissions-and-human-approval",
    "artifact-graphs-audit-logs-and-replay",
    "procedural-memory-and-cognitive-loop-closure",
    "recursive-self-improvement-boundaries",
    "circle-calculus-and-proof-carrying-ai-contracts",
    "coil-attention-cyclic-memory-and-recurrence-contracts",
    "coilra-multicoil-rope-and-cyclic-mixers",
    "mathematical-and-search-substrates",
    "project-theseus-as-report-first-implementation-reference",
    "executable-specifications-and-lean-proof-envelope",
    "living-book-methodology",
}

REQUIRED_FRAGMENTS = (
    "planning and release-control artifact, not source evidence",
    "not a manifest edit",
    "not a support-state transition",
    "54 manifest chapters",
    "Do not run a broad 54-to-44 manifest edit",
    "Do not target a fixed chapter count.",
    "Do not delete ideas merely to reduce repetition.",
    "Do not promote any chapter core claim above `argument`",
    "Current Pilot Status",
    "The current decision is still deferral",
    "Chapter-Ownership Rubric",
    "A chapter is chapter-owning when it owns a distinct artifact",
    "A chapter is a consolidation candidate when most of its reader-visible load",
    "A merge is justified only if the destination draft reduces repeated skeleton",
    "A merge is rejected or deferred when the proposed destination loses a useful",
    "Candidate Sequence",
    "Protected Standalone Chapters",
    "Required Package Before Any Non-Pilot Merge",
    "Chapter-ownership rubric result",
    "Reader Work Sequencing",
    "This sequence does not merge chapters.",
    "This sequence does not change `book_structure.json`.",
    "This sequence does not change Appendix C support states.",
)

REQUIRED_DESTINATIONS = (
    "Constitutional Alignment: Agency, Dignity, and Corrigibility",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty",
    "Command Contracts: From Intent to Executable Work",
    "The Virtual Context ABI: Typed Pages, Cells, and Certificates",
    "Proof-Carrying Claims and Adversarial Review",
    "Planning as a Control Layer: DAGs and Intelligence Arbitrage",
)

PUBLIC_REFERENCES = (
    "docs/chapter_consolidation_sequence.md",
    "scripts/validate_chapter_consolidation_sequence.py",
)


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def manifest_chapter_ids() -> set[str]:
    data = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("book_structure.json must contain an object.")
    ids: set[str] = set()
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            chapter_id = chapter.get("id")
            if isinstance(chapter_id, str):
                ids.add(chapter_id)
    return ids


def main() -> None:
    errors: list[str] = []

    try:
        sequence = read_text(SEQUENCE)
    except FileNotFoundError:
        print("Missing docs/chapter_consolidation_sequence.md")
        sys.exit(1)

    ids = manifest_chapter_ids()
    if len(ids) != 54:
        errors.append("Consolidation sequence expects the current manifest to remain at 54 chapters.")

    for chapter_id in sorted(REQUIRED_IDS):
        if chapter_id not in ids:
            errors.append(f"Required consolidation chapter ID is missing from manifest: {chapter_id}")
        if f"`{chapter_id}`" not in sequence:
            errors.append(f"Consolidation sequence does not mention `{chapter_id}`.")

    for fragment in REQUIRED_FRAGMENTS:
        if fragment not in sequence:
            errors.append(f"Consolidation sequence missing required boundary: {fragment}")

    for destination in REQUIRED_DESTINATIONS:
        if destination not in sequence:
            errors.append(f"Consolidation sequence missing destination title: {destination}")

    for path in (ROADMAP, README, PUBLICATION, REPOSITORY_MAP):
        text = read_text(path)
        for reference in PUBLIC_REFERENCES:
            if reference not in text:
                errors.append(f"{path.relative_to(ROOT)} missing public reference to {reference}")

    if errors:
        print("Chapter consolidation sequence validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Chapter consolidation sequence validation passed: "
        "54-chapter manifest preserved and full candidate sequence recorded."
    )


if __name__ == "__main__":
    main()
