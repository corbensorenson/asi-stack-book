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
    SEMANTIC_REVIEW_DISPOSITION,
    build,
)


SCHEMA = ROOT / "schemas/chapter_substance_contract.schema.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def concept_errors(row: dict, specs: list[dict]) -> list[str]:
    out: list[str] = []
    chapter_id = row.get("chapter_id")
    concepts = row.get("concept_contracts", [])
    if len(concepts) != len(specs):
        return [f"{chapter_id}: concept denominator drifted"]
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
    review = row.get("semantic_review")
    if not isinstance(review, dict):
        out.append(f"{chapter_id}: digest-bound semantic review is missing")
    else:
        if review.get("reviewed_sha256") != row.get("sha256"):
            out.append(f"{chapter_id}: semantic review does not bind the current chapter digest")
        if review.get("disposition") != SEMANTIC_REVIEW_DISPOSITION:
            out.append(f"{chapter_id}: semantic review disposition is not editorially accepted")
        if review.get("support_state_effect") != "none":
            out.append(f"{chapter_id}: semantic review attempts support movement")
    return out


def errors(contract: dict, *, check_freshness: bool = True) -> list[str]:
    out = validate_against_schema(contract, load(SCHEMA), str(OUTPUT.relative_to(ROOT)))
    if check_freshness and contract != build():
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
        out.extend(concept_errors(row, specs))
    summary = contract.get("summary", {})
    if summary.get("atom_covered_chapter_count") != 84 or summary.get("atom_uncovered_chapter_count") != 0:
        out.append("unified atom-at-birth coverage is not 84/84")
    if summary.get("active_concepts_passing_count") != summary.get("active_concept_count"):
        out.append("not every priority concept contract passes")
    if summary.get("concept_complete_semantic_reviewed_chapter_count") != len(CONCEPT_SPECS):
        out.append("not every contracted chapter is concept-complete and digest-bound reviewed")
    if summary.get("current_semantic_review_count") != len(CONCEPT_SPECS):
        out.append("semantic review denominator drifted")
    if summary.get("atom_count_is_acceptance_target") is not False:
        out.append("atom-count parity was promoted into an acceptance target")
    if summary.get("word_trigger_is_completion_gate") is not False:
        out.append("diagnostic word count was promoted into a completion gate")
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
    reject("semantic review deletion", lambda c: c["chapter_records"][4].__setitem__("semantic_review", None))
    reject("semantic review digest drift", lambda c: c["chapter_records"][4]["semantic_review"].__setitem__("reviewed_sha256", "0" * 64))
    reject("manual review bypass", lambda c: c.__setitem__("manual_semantic_review_required", False))
    reject("chapter growth authorization", lambda c: c.__setitem__("chapter_growth_authority", "open"))
    reject("support promotion", lambda c: c.__setitem__("support_state_effect", "promoted"))

    # Positive control: completion mechanics remain unchanged when only the
    # diagnostic word count crosses below 5,000. This checks the concept gate
    # directly rather than relying on the generic stale-artifact rejection.
    first_contracted = next(
        row for row in contract["chapter_records"] if row["chapter_id"] in CONCEPT_SPECS
    )
    low_word_candidate = copy.deepcopy(first_contracted)
    low_word_candidate["word_count"] = 4200
    word_independence_controls = 1
    if concept_errors(low_word_candidate, CONCEPT_SPECS[low_word_candidate["chapter_id"]]):
        out.append("diagnostic word-count positive control failed concept completion")

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
        f"{summary['current_semantic_review_count']} current semantic reviews, "
        f"{word_independence_controls}/1 word-independence controls, "
        f"and {mutation_count}/{mutation_count} rejecting mutations."
    )


if __name__ == "__main__":
    main()
