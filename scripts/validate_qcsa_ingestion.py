#!/usr/bin/env python3
"""Validate conservative QCSA source ingestion across existing chapter owners."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "qcsa_whitepaper"
RAW = ROOT / "sources" / "raw" / "question_compiled_semantic_addressing_whitepaper.md"
DIGEST = "d9e594d40dfd62c899ab25e9d395d34c702dac12e8afd75eed133392f78c0c8c"
TARGETS = {
    "cognitive-compilation-and-semantic-ir",
    "virtual-context-abi",
    "routing-heads-and-specialist-cores",
    "compact-generative-systems-and-residual-honesty",
    "runtime-adapters-tool-permissions-and-human-approval",
    "claim-ledgers-and-belief-revision",
    "data-engines-continual-learning-and-unlearning",
    "inter-stack-protocols-identity-and-economic-exchange",
    "integrated-reference-architecture",
}
REQUIRED_NOTE_TERMS = [
    "Question-Compiled Semantic Addressing",
    "Semantic Object ID",
    "Semantic virtual address",
    "Multi-facet semantic address atlas",
    "Semantic Address Certificate",
    "Question compiler",
    "Typed temporal evidence-bearing hypergraph",
    "Semantic-to-physical",
    "atlas epoch",
    "open-world",
    "The source itself remains conceptual architecture and design rationale",
    "Local Implementation And Evaluation Update (2026-07-13)",
]


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def snapshot() -> dict:
    structure = load_json("book_structure.json")
    inventory = load_json("sources/source_inventory.json")
    note = (ROOT / "sources/source_notes/qcsa_whitepaper.md").read_text(encoding="utf-8")
    chapters = {
        chapter["id"]: {
            "record": chapter,
            "text": (ROOT / chapter["file"]).read_text(encoding="utf-8", errors="ignore"),
        }
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    }
    return {"structure": structure, "inventory": inventory, "note": note, "chapters": chapters}


def validate(data: dict) -> list[str]:
    errors = []
    structure = data.get("structure", {})
    inventory = data.get("inventory", [])
    chapters = data.get("chapters", {})
    records = [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]
    if len(records) != 54:
        errors.append("QCSA ingestion must preserve the 54-chapter architecture")
    if any(chapter.get("id") in {"qcsa", "question-compiled-semantic-addressing"} for chapter in records):
        errors.append("QCSA ingestion unexpectedly created a standalone chapter")
    if any(chapter.get("evidence_level") != "argument" for chapter in records):
        errors.append("QCSA ingestion moved a core claim above argument")

    source_rows = [row for row in inventory if row.get("id") == SOURCE_ID]
    if len(source_rows) != 1:
        errors.append("source inventory must contain exactly one QCSA record")
    else:
        source = source_rows[0]
        if set(source.get("chapter_targets", [])) != TARGETS:
            errors.append("QCSA inventory chapter targets drifted")
        if source.get("priority") != "must_use" or source.get("source_type") != "author_whitepaper":
            errors.append("QCSA inventory classification drifted")
        if DIGEST not in str(source.get("url", "")):
            errors.append("QCSA inventory locator lost the canonical source digest")

    note = str(data.get("note", ""))
    for term in REQUIRED_NOTE_TERMS:
        if term.lower() not in note.lower():
            errors.append(f"QCSA source note missing required boundary or term: {term}")
    if DIGEST not in note:
        errors.append("QCSA source note lost the canonical source digest")
    if "Keep the active 54-chapter architecture" not in note:
        errors.append("QCSA source note lost the chapter decision")

    for chapter_id in TARGETS:
        owner = chapters.get(chapter_id)
        if not owner:
            errors.append(f"missing QCSA chapter owner: {chapter_id}")
            continue
        chapter = owner["record"]
        if SOURCE_ID not in chapter.get("source_ids", []):
            errors.append(f"{chapter_id}: QCSA source assignment missing")
        mappings = [row for row in chapter.get("claim_source_mappings", []) if row.get("source_id") == SOURCE_ID]
        if len(mappings) != 1:
            errors.append(f"{chapter_id}: expected one QCSA claim-source mapping")
        else:
            mapping = mappings[0]
            if mapping.get("passage_review_state") != "reviewed" or not mapping.get("passage_refs"):
                errors.append(f"{chapter_id}: QCSA mapping is not passage reviewed")
            limits = str(mapping.get("limits", "")).lower()
            if not any(term in limits for term in ["does not", "not establish", "no natural", "no learned", "no useful", "no peer", "no learning"]):
                errors.append(f"{chapter_id}: QCSA mapping lost its non-claim boundary")
        if SOURCE_ID not in owner["text"]:
            errors.append(f"{chapter_id}: prose/source crosswalk does not name QCSA source")
    return errors


def mutation_controls(base: dict) -> list[str]:
    failures = []
    mutations = []
    missing_source = copy.deepcopy(base)
    missing_source["inventory"] = [row for row in missing_source["inventory"] if row.get("id") != SOURCE_ID]
    mutations.append(("source erasure", missing_source))
    target_erasure = copy.deepcopy(base)
    target_erasure["chapters"][next(iter(TARGETS))]["record"]["source_ids"].remove(SOURCE_ID)
    mutations.append(("target erasure", target_erasure))
    unreviewed = copy.deepcopy(base)
    row = next(row for row in unreviewed["chapters"]["virtual-context-abi"]["record"]["claim_source_mappings"] if row.get("source_id") == SOURCE_ID)
    row["passage_review_state"] = "metadata_only"
    mutations.append(("passage-review laundering", unreviewed))
    promoted = copy.deepcopy(base)
    promoted["chapters"]["integrated-reference-architecture"]["record"]["evidence_level"] = "source-derived"
    mutations.append(("support promotion", promoted))
    new_chapter = copy.deepcopy(base)
    new_chapter["structure"]["parts"][0]["chapters"].append({"id": "qcsa", "evidence_level": "argument"})
    mutations.append(("chapter invention", new_chapter))
    boundary_erasure = copy.deepcopy(base)
    boundary_erasure["note"] = boundary_erasure["note"].replace("The source itself remains conceptual architecture and design rationale", "The source proves the completed architecture")
    mutations.append(("non-claim erasure", boundary_erasure))
    for name, mutated in mutations:
        if not validate(mutated):
            failures.append(name)
    return failures


def main() -> None:
    data = snapshot()
    errors = validate(data)
    controls = mutation_controls(data)
    if controls:
        errors.append(f"mutation controls failed to reject: {controls}")
    if RAW.exists():
        actual = hashlib.sha256(RAW.read_bytes()).hexdigest()
        if actual != DIGEST:
            errors.append("local raw QCSA source digest differs from its canonical inventory binding")
    if errors:
        print("QCSA ingestion validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("QCSA ingestion passed: 1 digest-bound author source, 9 passage-reviewed existing-chapter routes, 54 argument-state chapters, no new chapter, and 6 rejecting mutations.")


if __name__ == "__main__":
    main()
