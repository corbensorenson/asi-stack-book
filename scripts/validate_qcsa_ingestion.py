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
HISTORICAL_55TH_CHAPTER = "replaceable-cognitive-substrates-beyond-transformer-monoculture"
ACTIVE_MAINTENANCE_ROADMAP = "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
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
    return {
        "structure": structure,
        "inventory": inventory,
        "note": note,
        "chapters": chapters,
        "historical_status": load_json("roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"),
        "maintenance_status": load_json("roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"),
        "vectors": load_json("evidence_quality/core_claim_vectors.json"),
    }


def validate(data: dict) -> list[str]:
    errors = []
    structure = data.get("structure", {})
    inventory = data.get("inventory", [])
    chapters = data.get("chapters", {})
    records = [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]
    live_chapter_count = len(records)
    record_ids = {chapter.get("id") for chapter in records}
    if len(record_ids) != live_chapter_count:
        errors.append("live architecture contains duplicate chapter identifiers")
    historical_status = data.get("historical_status", {})
    activation = historical_status.get("activation_baseline", {})
    if activation.get("active_chapter_count") != 54:
        errors.append("historical QCSA-era 54-chapter activation baseline drifted")
    historical_expansion = historical_status.get("structural_expansion_contract", {})
    if (
        historical_expansion.get("live_chapter_count") != 55
        or historical_expansion.get("chapter_id") != HISTORICAL_55TH_CHAPTER
        or historical_expansion.get("support_state_effect") != "none"
    ):
        errors.append("historical QCSA/55th-chapter ingestion contract drifted")
    maintenance_status = data.get("maintenance_status", {})
    activation_truth = maintenance_status.get("activation_truth", {})
    structural_tranche = maintenance_status.get("quality_uplift_program", {}).get("structural_completeness_tranche", {})
    first_tranche = structural_tranche.get("first_tranche", {})
    admitted_chapter_ids = set(first_tranche.get("candidate_ids", []))
    if (
        maintenance_status.get("status") != "active"
        or maintenance_status.get("roadmap_path") != ACTIVE_MAINTENANCE_ROADMAP
        or activation_truth.get("live_working_chapter_count") != live_chapter_count
        or activation_truth.get("chapter_core_argument_count") != live_chapter_count
        or activation_truth.get("chapter_core_promotion_count") != 0
        or structural_tranche.get("current_manifest_chapter_count") != live_chapter_count
        or first_tranche.get("manifest_admitted_count") != len(admitted_chapter_ids)
        or not admitted_chapter_ids.issubset(record_ids)
    ):
        errors.append("current live architecture disagrees with active maintenance authority")
    if any(chapter.get("id") in {"qcsa", "question-compiled-semantic-addressing"} for chapter in records):
        errors.append("QCSA ingestion unexpectedly created a standalone chapter")
    if any(chapter.get("evidence_level") != "argument" for chapter in records):
        errors.append("QCSA ingestion moved a core claim above argument")
    vectors = data.get("vectors", {})
    vector_rows = vectors.get("vectors", [])
    vector_summary = vectors.get("summary", {})
    if (
        len(vector_rows) != live_chapter_count
        or vector_summary.get("vector_count") != live_chapter_count
        or vector_summary.get("summary_support_states") != {"argument": live_chapter_count}
        or any(row.get("summary_support_state") != "argument" for row in vector_rows)
    ):
        errors.append("live evidence vectors moved or miscounted a chapter-core claim")

    qcsa_manifest_routes = {
        chapter.get("id")
        for chapter in records
        if SOURCE_ID in chapter.get("source_ids", [])
    }
    later_qcsa_routes = qcsa_manifest_routes - TARGETS

    source_rows = [row for row in inventory if row.get("id") == SOURCE_ID]
    if len(source_rows) != 1:
        errors.append("source inventory must contain exactly one QCSA record")
    else:
        source = source_rows[0]
        if set(source.get("chapter_targets", [])) != qcsa_manifest_routes:
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

    if not later_qcsa_routes.issubset(admitted_chapter_ids):
        errors.append("later QCSA source reuse escaped manifest-admitted chapters")

    for chapter_id in TARGETS | later_qcsa_routes:
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
    unauthorized_route = copy.deepcopy(base)
    unauthorized_chapter = next(chapter for part in unauthorized_route["structure"]["parts"] for chapter in part["chapters"] if chapter.get("id") == "prototype-roadmap")
    unauthorized_chapter.setdefault("source_ids", []).append(SOURCE_ID)
    mutations.append(("unauthorized later source reuse", unauthorized_route))
    authority_promotion = copy.deepcopy(base)
    authority_promotion["maintenance_status"]["activation_truth"]["chapter_core_promotion_count"] = 1
    mutations.append(("current authority promotion", authority_promotion))
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
    live_chapter_count = sum(
        len(part.get("chapters", []))
        for part in data["structure"].get("parts", [])
    )
    later_route_count = len({
        chapter.get("id")
        for part in data["structure"].get("parts", [])
        for chapter in part.get("chapters", [])
        if SOURCE_ID in chapter.get("source_ids", []) and chapter.get("id") not in TARGETS
    })
    print(f"QCSA ingestion passed: 1 digest-bound author source, 9 passage-reviewed historical chapter routes plus {later_route_count} bounded reuses in later manifest-admitted chapters, preserved 54-chapter activation and historical authorized 55th-chapter ingestion, {live_chapter_count} live argument-state chapters, no QCSA standalone chapter, and 8 rejecting mutations.")


if __name__ == "__main__":
    main()
