#!/usr/bin/env python3
"""Validate current-book chapter depth, concept fidelity, and atom ownership."""

from __future__ import annotations

import copy
import json

from build_canonical_public_status import validate_against_schema
from build_chapter_substance_contract import (
    CONCEPT_SPECS,
    MANIFEST_FREEZE,
    OUTPUT,
    REQUIRED_ELEMENTS,
    ROOT,
    WORD_TRIGGER,
    build,
)


SCHEMA = ROOT / "schemas/chapter_substance_contract.schema.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def errors(contract: dict) -> list[str]:
    out = validate_against_schema(contract, load(SCHEMA), str(OUTPUT.relative_to(ROOT)))
    if contract != build():
        out.append("tracked substance contract is stale against current chapters and atom sources")
    records = contract.get("chapter_records", [])
    ids = [row.get("chapter_id") for row in records]
    if len(ids) != MANIFEST_FREEZE or len(set(ids)) != MANIFEST_FREEZE:
        out.append("chapter denominator is not the exact frozen 84-owner manifest")
    if any(not row.get("atom_refs") for row in records):
        out.append("at least one manifest chapter has no exact atom source")
    for row in records:
        chapter_id = row.get("chapter_id")
        specs = CONCEPT_SPECS.get(chapter_id)
        if specs is None:
            continue
        if row.get("word_count", 0) < WORD_TRIGGER:
            out.append(f"{chapter_id}: priority chapter remains below the 5,000-word triage floor")
        concepts = row.get("concept_contracts", [])
        if len(concepts) != len(specs):
            out.append(f"{chapter_id}: concept denominator drifted")
            continue
        for concept in concepts:
            if concept.get("observed_section_words", 0) < concept.get("minimum_section_words", 0):
                out.append(
                    f"{chapter_id}/{concept.get('concept_id')}: section is below its substance floor"
                )
            if set(concept.get("observed_elements", [])) != set(REQUIRED_ELEMENTS):
                out.append(
                    f"{chapter_id}/{concept.get('concept_id')}: mechanism/failure/non-claim/source roles incomplete"
                )
            if not concept.get("source_ids_declared_by_chapter"):
                out.append(
                    f"{chapter_id}/{concept.get('concept_id')}: source grounding is outside the chapter queue"
                )
    summary = contract.get("summary", {})
    if summary.get("atom_covered_chapter_count") != 84 or summary.get("atom_uncovered_chapter_count") != 0:
        out.append("unified atom-at-birth coverage is not 84/84")
    if summary.get("active_concepts_passing_count") != summary.get("active_concept_count"):
        out.append("not every priority concept contract passes")
    return out


def main() -> None:
    contract = load(OUTPUT)
    out = errors(contract)
    mutation_count = 0

    def reject(label, mutate):
        nonlocal mutation_count
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        mutation_count += 1
        if not errors(candidate):
            out.append(f"negative control accepted: {label}")

    reject("chapter deletion", lambda c: c["chapter_records"].pop())
    reject("manifest freeze widening", lambda c: c.__setitem__("manifest_chapter_count_freeze", 85))
    reject("word trigger weakening", lambda c: c.__setitem__("word_trigger", 1000))
    reject("atom source deletion", lambda c: c["chapter_records"][0].__setitem__("atom_refs", []))
    reject("concept deletion", lambda c: c["chapter_records"][4]["concept_contracts"].pop())
    reject("concept word laundering", lambda c: c["chapter_records"][4]["concept_contracts"][0].__setitem__("observed_section_words", 1))
    reject("source grounding deletion", lambda c: c["chapter_records"][4]["concept_contracts"][0].__setitem__("source_ids_declared_by_chapter", False))
    reject("manual review bypass", lambda c: c.__setitem__("manual_semantic_review_required", False))
    reject("chapter growth authorization", lambda c: c.__setitem__("chapter_growth_authority", "open"))
    reject("support promotion", lambda c: c.__setitem__("support_state_effect", "promoted"))

    if out:
        print("Chapter substance contract validation failed:")
        for item in out:
            print(f" - {item}")
        raise SystemExit(1)
    summary = contract["summary"]
    print(
        "Chapter substance contract passed: "
        f"{summary['chapter_count']} frozen chapters, "
        f"{summary['atom_covered_chapter_count']}/84 atom-covered, "
        f"{summary['active_concepts_passing_count']}/{summary['active_concept_count']} "
        f"priority concepts, {summary['thin_chapter_count']} chapters below the diagnostic trigger, "
        f"and {mutation_count}/{mutation_count} rejecting mutations."
    )


if __name__ == "__main__":
    main()
