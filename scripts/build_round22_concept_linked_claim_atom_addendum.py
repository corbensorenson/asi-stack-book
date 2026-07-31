#!/usr/bin/env python3
"""Build concept-linked claim atoms for Round 22's coarse-atom chapters."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any

from visual_chapter_source import canonical_chapter_text


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_BUILDER = ROOT / "scripts/build_chapter_substance_contract.py"
OUTPUT = ROOT / "evidence_quality/round22_concept_linked_claim_atom_addendum.json"

CHAPTER_IDS = [
    "dangerous-capability-domains-and-misuse-uplift",
    "military-ai-autonomous-weapons-and-strategic-stability",
    "inner-alignment-mesa-optimization-and-learned-objective-integrity",
    "societal-resilience-and-misuse-defense",
    "confidential-and-verifiable-ai-computation",
    "open-weight-release-and-post-release-control",
    "perception-sensor-fusion-and-observation-trust",
    "human-ai-organizations-delegation-and-accountability",
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty",
    "embodied-agency-real-time-control-and-physical-safety",
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
    "relational-dimension-compilation-and-polyadic-cognition",
    "content-authenticity-watermarking-and-synthetic-media-integrity",
]


def load_contract_module():
    spec = importlib.util.spec_from_file_location("chapter_substance_contract", CONTRACT_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load chapter-substance builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact(value: str, limit: int = 1100) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= limit:
        return value
    boundary = value.rfind(". ", 0, limit)
    return value[: boundary + 1 if boundary >= 200 else limit].strip()


def labeled_segments(section: str, labels: tuple[str, ...]) -> list[str]:
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(
        rf"\*\*(?:{label_pattern})(?::|\.)\*\*\s*(.*?)"
        rf"(?=\s*\*\*[A-Z][^*]{{1,80}}(?::|\.)\*\*|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    return [compact(match.group(1)) for match in pattern.finditer(section) if match.group(1).strip()]


def last_segment(section: str, labels: tuple[str, ...], concept_id: str) -> str:
    values = labeled_segments(section, labels)
    if not values:
        raise ValueError(f"{concept_id}: missing {'/'.join(labels)} segment")
    return values[-1]


def build() -> dict[str, Any]:
    module = load_contract_module()
    chapters = {chapter["id"]: chapter for chapter in module.manifest_chapters()}
    atoms: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []

    for chapter_id in CHAPTER_IDS:
        chapter = chapters[chapter_id]
        path = ROOT / chapter["file"]
        text = canonical_chapter_text(path)
        specs = module.CONCEPT_SPECS.get(chapter_id, [])
        semantic_review = module.SEMANTIC_REVIEWS.get(chapter_id)
        if len(specs) != 8:
            raise ValueError(f"{chapter_id}: expected eight reviewed concepts, found {len(specs)}")
        if not semantic_review or semantic_review["reviewed_sha256"] != module.sha256(path):
            raise ValueError(f"{chapter_id}: concept decomposition requires a current digest-bound review")

        chapter_atom_ids: list[str] = []
        for concept in specs:
            concept_id = concept["concept_id"]
            section = module.heading_section(text, concept["heading"])
            mechanism = last_segment(section, ("Mechanism",), concept_id)
            failure = last_segment(section, ("Failure mode",), concept_id)
            nonclaim = last_segment(section, ("Non-claim",), concept_id)
            grounding = last_segment(
                section,
                ("Source grounding", "Source engagement"),
                concept_id,
            )
            atom_id = f"{chapter_id}.concept.{concept_id}"
            chapter_atom_ids.append(atom_id)
            atoms.append(
                {
                    "id": atom_id,
                    "chapter_id": chapter_id,
                    "concept_id": concept_id,
                    "role": "concept",
                    "heading": concept["heading"],
                    "proposition": compact(
                        f"For the bounded `{concept['heading']}` responsibility, the "
                        f"chapter proposes this separately testable mechanism: {mechanism}"
                    ),
                    "scope": compact(
                        f"Only the concept section `{concept['heading']}` in "
                        f"{chapter['title']}, its declared sources "
                        f"{', '.join(concept['source_ids'])}, the current chapter digest, "
                        "and the argument-level authority of the living book."
                    ),
                    "assumptions": [
                        "The named concept section and source identities are the exact current editorial owners.",
                        "The current digest-bound semantic review establishes concept distinctness only, not truth.",
                        "A future experiment must preserve the concept's population, environment, intervention, outcome, authority, time, and artifact boundaries.",
                    ],
                    "counterclaim": compact(
                        f"The `{concept['heading']}` mechanism is unnecessary, non-identifiable, "
                        "or dominated by a competent simpler alternative under the same boundary."
                    ),
                    "falsifier": compact(
                        "The proposition must narrow or fail if a competent reachable comparison "
                        f"produces this owned failure without detection or remedy: {failure}"
                    ),
                    "required_evidence_lanes": [
                        "source-specific comparator and limitation review",
                        "reachable implementation or natural task",
                        "strongest competent simpler baseline",
                        "independently implemented evaluation",
                        "positive, negative, and failure controls",
                        "cost, residual, and transfer accounting",
                    ],
                    "source_ids": concept["source_ids"],
                    "source_grounding": grounding,
                    "contrary_evidence": [],
                    "acceptance_criterion": compact(
                        f"The `{concept['heading']}` mechanism changes its named bounded outcome "
                        "against a competent baseline while all required controls pass and all "
                        "residuals, costs, and authority effects remain visible."
                    ),
                    "narrowing_criterion": (
                        "Narrow to the exact mechanism, population, environment, artifact, or "
                        "decision boundary that survives competent challenge."
                    ),
                    "refutation_criterion": (
                        "Refute only after competent implementations, valid positive controls, "
                        "strong baselines, evaluator sensitivity, and the frozen rescue ladder pass."
                    ),
                    "deprecation_criterion": (
                        "Deprecate if another canonical owner absorbs this concept without losing "
                        "its distinct falsifier, evidence route, source limits, or non-claim."
                    ),
                    "promotion_ceiling": (
                        "argument until claim-specific natural evidence and an accepted evidence "
                        "transition justify a narrower movement"
                    ),
                    "owner": chapter_id,
                    "support_state": "argument",
                    "support_state_effect": "none",
                    "non_claims": [
                        nonclaim,
                        "Concept decomposition records falsifiable custody; it is not proof, evidence, support promotion, or a claim of atom-count parity.",
                    ],
                }
            )
        reviews.append(
            {
                "chapter_id": chapter_id,
                "chapter_sha256": module.sha256(path),
                "concept_ids": [spec["concept_id"] for spec in specs],
                "atom_ids": chapter_atom_ids,
                "semantic_review_state": "concept_linked_decomposition_bound_to_current_reviewed_chapter",
                "support_state_effect": "none",
            }
        )

    return {
        "schema_version": "asi_stack.round22_concept_linked_claim_atom_addendum.v1",
        "packet_id": "P6.10-R22-concept-linked-falsifiability",
        "recorded_date": "2026-07-30",
        "chapter_count": len(CHAPTER_IDS),
        "concepts_per_chapter": 8,
        "atom_count": len(atoms),
        "chapter_ids": CHAPTER_IDS,
        "atoms": atoms,
        "chapter_reviews": reviews,
        "historical_atom_sources_rewritten": False,
        "atom_count_is_acceptance_target": False,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "The packet decomposes already-reviewed concepts; it does not establish their truth.",
            "The packet does not rewrite or promote any historical claim atom or evidence transition.",
            "One atom per retained material concept is a falsifiability rule, not a numerical parity target.",
        ],
    }


def main() -> None:
    packet = build()
    OUTPUT.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)}: {packet['chapter_count']} chapters, "
        f"{packet['atom_count']} concept-linked atoms."
    )


if __name__ == "__main__":
    main()
