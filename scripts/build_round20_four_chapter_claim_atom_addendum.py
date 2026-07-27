#!/usr/bin/env python3
"""Build the additive Round 20 claim-atom packet for four uncovered chapters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
OUTPUT = ROOT / "evidence_quality/round20_four_chapter_claim_atom_addendum.json"

CHAPTER_IDS = [
    "military-ai-autonomous-weapons-and-strategic-stability",
    "confidential-and-verifiable-ai-computation",
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty",
    "relational-dimension-compilation-and-polyadic-cognition",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def chapters() -> dict[str, dict[str, Any]]:
    structure = load(STRUCTURE)
    return {
        chapter["id"]: chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
    }


def atom(
    chapter: dict[str, Any],
    role: str,
    proposition: str,
    falsifier: str,
    acceptance: str,
) -> dict[str, Any]:
    chapter_id = chapter["id"]
    return {
        "id": f"{chapter_id}.{role}",
        "chapter_id": chapter_id,
        "role": role,
        "proposition": proposition,
        "scope": (
            f"The exact argument-level responsibility owned by {chapter['title']} "
            "under its manifest sources, interfaces, evidence ceiling, and non-claims."
        ),
        "assumptions": [
            "The current manifest record accurately states the chapter responsibility.",
            "Source mappings retain their recorded limits and do not become local evidence.",
            "No prose, schema, validator, or atom packet changes support by itself.",
        ],
        "counterclaim": (
            "The responsibility is already absorbed by an adjacent owner, is too vague to "
            "falsify, or gains no decision value over a competent simpler boundary."
        ),
        "falsifier": falsifier,
        "required_evidence_lanes": [
            "source-specific comparator and limitation review",
            "reachable implementation or natural task",
            "strongest simpler baseline",
            "independent evaluation",
            "failure and negative controls",
            "cost, residual, and transfer accounting",
        ],
        "contrary_evidence": [],
        "acceptance_criterion": acceptance,
        "narrowing_criterion": (
            "Narrow the proposition to the exact mechanism, population, environment, "
            "artifact, or decision boundary that survives competent challenge."
        ),
        "refutation_criterion": (
            "Refute only after multiple competent implementations, valid positive controls, "
            "strong baselines, evaluator sensitivity, and the frozen rescue ladder pass."
        ),
        "deprecation_criterion": (
            "Deprecate if a better canonical owner absorbs the responsibility without losing "
            "identity, failure, evidence, authority, or residual boundaries."
        ),
        "promotion_ceiling": (
            "argument until claim-specific natural evidence and an accepted evidence "
            "transition justify a narrower movement"
        ),
        "owner": chapter_id,
        "support_state": "argument",
        "support_state_effect": "none",
        "non_claims": [
            "This atom records manuscript responsibility; it is not proof or empirical evidence.",
            "No chapter-core, safety, performance, deployment, SOTA, AGI, ASI, publication, or release claim moves.",
        ],
    }


def build() -> dict[str, Any]:
    by_id = chapters()
    if any(chapter_id not in by_id for chapter_id in CHAPTER_IDS):
        missing = sorted(set(CHAPTER_IDS) - set(by_id))
        raise ValueError(f"missing manifest chapter(s): {missing}")

    atoms: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    for chapter_id in CHAPTER_IDS:
        chapter = by_id[chapter_id]
        interfaces = " ".join(chapter.get("interfaces", []))
        mechanisms = " ".join(chapter.get("mechanism", []))
        failures = "; ".join(chapter.get("failure_modes", []))
        atoms.extend(
            [
                atom(
                    chapter,
                    "core",
                    chapter["core_claim"],
                    f"A competent natural comparison shows that the {chapter['title']} core boundary adds no decision-relevant value over a simpler owner at comparable burden.",
                    f"The bounded {chapter['title']} responsibility improves a named decision or outcome without hidden authority, evidence, cost, or residual transfer.",
                ),
                atom(
                    chapter,
                    "boundary",
                    interfaces,
                    "An adjacent chapter can safely absorb every interface while preserving the exact authority, evidence, consumer, and failure boundaries.",
                    "Independent consumers can join the interfaces without responsibility or support-state inheritance.",
                ),
                atom(
                    chapter,
                    "mechanism",
                    mechanisms,
                    "The mechanism is inactive, non-identifiable, dominated by a competent simpler design, or cannot preserve the chapter's obligations in a reachable implementation.",
                    "A reachable implementation activates the mechanism, survives positive and negative controls, and improves its exact bounded outcome.",
                ),
                atom(
                    chapter,
                    "failure_boundary",
                    f"The chapter must detect, retain, and route failures including: {failures}",
                    "Material failures remain unobserved, unowned, or are erased by a success aggregate under representative challenge.",
                    "The exact failure families are detected or retained as owned residuals under competent adversarial and ordinary cases.",
                ),
                atom(
                    chapter,
                    "argument_exit",
                    f"{chapter['minimal_implementation']} {chapter['beyond_state_of_art']}",
                    "The smallest honest implementation cannot be built safely, fails its positive controls, or produces no useful signal for the mature decision target.",
                    "The smallest implementation, strong alternatives, natural workload, independent evaluator, cost accounting, and transfer gate justify a bounded conclusion.",
                ),
            ]
        )
        reviews.append(
            {
                "chapter_id": chapter_id,
                "atom_ids": [row["id"] for row in atoms if row["chapter_id"] == chapter_id],
                "semantic_review_state": "reviewed_against_manifest_owned_contract",
                "support_state_effect": "none",
            }
        )

    return {
        "schema_version": "asi_stack.round20_four_chapter_claim_atom_addendum.v1",
        "packet_id": "P6.9-R20-four-chapter-atom-at-birth-repair",
        "recorded_date": "2026-07-27",
        "chapter_count": len(CHAPTER_IDS),
        "atoms_per_chapter": 5,
        "atom_count": len(atoms),
        "chapter_ids": CHAPTER_IDS,
        "atoms": atoms,
        "chapter_reviews": reviews,
        "historical_atom_sources_rewritten": False,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "The packet closes atom ownership for four chapters; it does not establish chapter depth or truth.",
            "The packet does not rewrite the frozen 64-chapter registry or earlier addenda.",
            "Atom coverage is an editorial custody property, not evidence maturity.",
        ],
    }


def main() -> None:
    value = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {value['chapter_count']} chapters, {value['atom_count']} atoms.")


if __name__ == "__main__":
    main()
