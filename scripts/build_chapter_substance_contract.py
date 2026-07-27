#!/usr/bin/env python3
"""Build the current-book chapter-depth, concept-fidelity, and atom-coverage contract."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
OUTPUT = ROOT / "evidence_quality/chapter_substance_contract.json"
WORD_TRIGGER = 5000
MANIFEST_FREEZE = 84

ATOM_SOURCES = [
    ROOT / "evidence_quality/claim_atom_registry.json",
    ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json",
    ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
    ROOT / "evidence_quality/taxonomy_completion_claim_atoms_2026_07_24.json",
    ROOT / "evidence_quality/round_18_breadth_completion_claim_atoms.json",
    ROOT / "evidence_quality/round20_four_chapter_claim_atom_addendum.json",
]

CONCEPT_SPECS: dict[str, list[dict[str, Any]]] = {
    "dangerous-capability-domains-and-misuse-uplift": [
        {"concept_id": "knowledge-versus-completion", "heading": "Knowledge is not completion", "source_ids": ["ext_model_evaluation_extreme_risks_2023", "ext_aisi_frontier_ai_trends_2025"]},
        {"concept_id": "refusal-versus-capability", "heading": "Refusal is not incapability", "source_ids": ["ext_openai_worst_case_open_weight_risks_2025"]},
        {"concept_id": "capability-versus-propensity", "heading": "Capability is not propensity", "source_ids": ["ext_singapore_consensus_2026"]},
        {"concept_id": "measurement-ladder", "heading": "The six-level measurement ladder", "source_ids": ["ext_aisi_misuse_safeguards_safety_case_2026"]},
        {"concept_id": "threat-model-freeze", "heading": "1. Freeze the threat model", "source_ids": ["ext_openai_preparedness_framework_2025", "ext_anthropic_responsible_scaling_policy_3_4_2026"]},
        {"concept_id": "actor-cohorts-and-counterfactuals", "heading": "2. Define actor cohorts and counterfactuals", "source_ids": ["ext_singapore_consensus_2026"]},
        {"concept_id": "elicitation-competence", "heading": "3. Audit elicitation competence", "source_ids": ["ext_model_evaluation_extreme_risks_2023", "ext_openai_worst_case_open_weight_risks_2025"]},
        {"concept_id": "cbrn-domain-program", "heading": "CBRN and biological/chemical misuse", "source_ids": ["ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026", "ext_anthropic_responsible_scaling_policy_3_4_2026"]},
    ],
    "content-authenticity-watermarking-and-synthetic-media-integrity": [
        {"concept_id": "signed-provenance", "heading": "Signed provenance", "source_ids": ["ext_c2pa_specification_2_3_2025"]},
        {"concept_id": "watermarking", "heading": "Watermarking", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "fingerprinting", "heading": "Fingerprinting", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "statistical-detection", "heading": "Statistical detection", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "visible-disclosure", "heading": "Visible disclosure", "source_ids": ["ext_eu_article_50_transparency_guidelines_2026"]},
        {"concept_id": "contextual-verification", "heading": "Contextual verification", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "transformation-lineage", "heading": "Transformation is the central engineering problem", "source_ids": ["ext_c2pa_specification_2_3_2025"]},
        {"concept_id": "article-50-interface", "heading": "Regulation is an interface, not a design substitute", "source_ids": ["ext_eu_article_50_transparency_guidelines_2026"]},
    ],
    "societal-resilience-and-misuse-defense": [
        {"concept_id": "classifier-coverage", "heading": "One classifier sees one surface", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "recovery-beyond-takedown", "heading": "Takedown is not recovery", "source_ids": ["ext_nist_incident_response_2025"]},
        {"concept_id": "rights-preserving-reporting", "heading": "Reporting is not automatically safe", "source_ids": ["ext_singapore_consensus_2026", "ext_nist_incident_response_2025"]},
        {"concept_id": "four-stage-resilience", "heading": "The four-stage resilience contract", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "federated-incident-envelope", "heading": "The federated incident envelope", "source_ids": ["ext_nist_incident_response_2025"]},
        {"concept_id": "fraud-and-impersonation", "heading": "Fraud, scams, extortion, defamation, and impersonation", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "child-safety-and-ncii", "heading": "Child safety and non-consensual intimate imagery", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "mental-health-and-parasocial-harm", "heading": "Manipulation, mental health, and parasocial harms", "source_ids": ["ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026"]},
    ],
}

REQUIRED_ELEMENTS = ["**Mechanism.**", "**Failure mode.**", "**Non-claim.**", "**Source grounding.**"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_chapters() -> list[dict[str, Any]]:
    return [
        chapter
        for part in load(STRUCTURE)["parts"]
        for chapter in part["chapters"]
    ]


def atom_coverage() -> dict[str, list[dict[str, str]]]:
    coverage: dict[str, list[dict[str, str]]] = {}
    for path in ATOM_SOURCES:
        packet = load(path)
        source = path.relative_to(ROOT).as_posix()
        if path.name == "claim_atom_registry.json":
            rows = [(row["chapter_id"], row["atom_id"]) for row in packet["atoms"]]
        elif path.name == "replaceable_cognitive_substrates_claim_atom_addendum.json":
            rows = [(packet["chapter_id"], row["id"]) for row in packet["atoms"]]
        elif path.name in {
            "taxonomy_completion_claim_atoms_2026_07_24.json",
            "round_18_breadth_completion_claim_atoms.json",
        }:
            rows = [
                (row["chapter_owner"], row["stable_claim_identity"])
                for row in packet["atoms"]
            ]
        else:
            rows = [(row["chapter_id"], row["id"]) for row in packet["atoms"]]
        for chapter_id, atom_id in rows:
            coverage.setdefault(chapter_id, []).append(
                {"atom_id": atom_id, "source_path": source}
            )
    return coverage


def heading_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?m)^(?P<marks>#+)\s+{re.escape(heading)}\s*$")
    match = pattern.search(text)
    if match is None:
        return ""
    level = len(match.group("marks"))
    tail = text[match.end():]
    next_heading = re.search(rf"(?m)^#{{1,{level}}}\s+", tail)
    return tail[: next_heading.start()] if next_heading else tail


def build() -> dict[str, Any]:
    chapters = manifest_chapters()
    if len(chapters) != MANIFEST_FREEZE:
        raise ValueError(
            f"chapter-count freeze violated: expected {MANIFEST_FREEZE}, found {len(chapters)}"
        )
    coverage = atom_coverage()
    records = []
    for chapter in chapters:
        path = ROOT / chapter["file"]
        text = path.read_text(encoding="utf-8")
        word_count = len(text.split())
        specs = CONCEPT_SPECS.get(chapter["id"], [])
        concepts = []
        for spec in specs:
            section = heading_section(text, spec["heading"])
            concepts.append(
                {
                    **spec,
                    "minimum_section_words": 150,
                    "required_elements": REQUIRED_ELEMENTS,
                    "observed_section_words": len(section.split()),
                    "observed_elements": [
                        element for element in REQUIRED_ELEMENTS if element in section
                    ],
                    "source_ids_declared_by_chapter": all(
                        source_id in chapter.get("source_ids", [])
                        for source_id in spec["source_ids"]
                    ),
                }
            )
        if specs:
            state = "active_priority_concept_contract"
        elif word_count < WORD_TRIGGER:
            state = "queued_thin_chapter_for_manual_concept_contract"
        else:
            state = "word_trigger_clear_semantic_certification_not_implied"
        records.append(
            {
                "chapter_id": chapter["id"],
                "chapter_title": chapter["title"],
                "path": chapter["file"],
                "sha256": sha256(path),
                "word_count": word_count,
                "word_trigger": WORD_TRIGGER,
                "depth_state": state,
                "short_reference_exception": False,
                "short_reference_justification": None,
                "atom_refs": coverage.get(chapter["id"], []),
                "concept_contracts": concepts,
            }
        )
    thin = [row for row in records if row["word_count"] < WORD_TRIGGER]
    active = [row for row in records if row["depth_state"] == "active_priority_concept_contract"]
    all_concepts = [concept for row in active for concept in row["concept_contracts"]]
    return {
        "schema_version": "asi_stack.chapter_substance_contract.v1",
        "contract_id": "P6.9-R20-chapter-substance-and-concept-fidelity",
        "recorded_date": "2026-07-27",
        "manifest_path": "book_structure.json",
        "manifest_chapter_count_freeze": MANIFEST_FREEZE,
        "word_count_method": "Unicode text split on whitespace over the complete tracked QMD; diagnostic trigger only",
        "word_trigger": WORD_TRIGGER,
        "concept_contract_rule": (
            "An active concept section must be named, contain at least 150 words, "
            "and separately state mechanism, failure mode, non-claim, and source grounding. "
            "Passing remains editorial preparation, not semantic certification or evidence."
        ),
        "atom_source_paths": [path.relative_to(ROOT).as_posix() for path in ATOM_SOURCES],
        "chapter_records": records,
        "summary": {
            "chapter_count": len(records),
            "thin_chapter_count": len(thin),
            "active_priority_chapter_count": len(active),
            "queued_thin_chapter_count": sum(
                row["depth_state"] == "queued_thin_chapter_for_manual_concept_contract"
                for row in records
            ),
            "word_trigger_clear_chapter_count": sum(
                row["word_count"] >= WORD_TRIGGER for row in records
            ),
            "atom_covered_chapter_count": sum(bool(row["atom_refs"]) for row in records),
            "atom_uncovered_chapter_count": sum(not row["atom_refs"] for row in records),
            "active_concept_count": len(all_concepts),
            "active_concepts_passing_count": sum(
                concept["observed_section_words"] >= concept["minimum_section_words"]
                and set(concept["observed_elements"]) == set(concept["required_elements"])
                and concept["source_ids_declared_by_chapter"]
                for concept in all_concepts
            ),
            "support_state_effect": "none",
        },
        "manual_semantic_review_required": True,
        "chapter_growth_authority": "frozen_at_84_until_thin_and_atom_debt_are_zero_or_terminally_justified",
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "Word count is a triage signal, not a quality score or proof of depth.",
            "Required labels and section length cannot establish semantic adequacy; manual review remains required.",
            "Atom coverage records responsibility and falsifiability, not truth or evidence maturity.",
            "No chapter-core, safety, performance, deployment, SOTA, AGI, ASI, publication, or release claim follows.",
        ],
    }


def main() -> None:
    value = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = value["summary"]
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)}: {summary['chapter_count']} chapters, "
        f"{summary['thin_chapter_count']} below trigger, "
        f"{summary['atom_covered_chapter_count']} atom-covered, "
        f"{summary['active_concepts_passing_count']}/{summary['active_concept_count']} "
        "priority concepts passing."
    )


if __name__ == "__main__":
    main()
