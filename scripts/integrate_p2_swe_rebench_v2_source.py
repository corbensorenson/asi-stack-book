#!/usr/bin/env python3
"""Idempotently install the passage-reviewed SWE-rebench V2 source mapping."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "sources/source_inventory.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCE_ID = "ext_swe_rebench_v2_2026"

RECORD = {
    "id": SOURCE_ID,
    "title": "SWE-rebench V2: Language-Agnostic SWE Task Collection at Scale",
    "priority": "external_literature",
    "layer": "natural_software_task_construction_and_evaluation",
    "chapter_targets": [
        "benchmark-ratchets-and-anti-goodhart-evidence",
        "artifact-graphs-audit-logs-and-replay",
        "integrated-reference-architecture",
        "prototype-roadmap",
        "readiness-gates-residual-escrow-and-quarantine",
    ],
    "url": "https://arxiv.org/abs/2602.23866",
    "notes": "Primary 2026 natural-task substrate for multilingual repository changes, interactive setup, containerized full-suite execution, separated solution/test patches, task diagnostics, and explicit environment pathologies. It does not establish local task validity, gold execution, model competence, governance benefit, safety, transfer, or SOTA.",
    "source_type": "preprint",
    "arxiv_id": "2602.23866",
    "published": "2026-02-27",
    "updated": "2026-06-01",
    "citation_label": "Badertdinov et al. (2026), SWE-rebench V2",
    "doi": "10.48550/arXiv.2602.23866",
}

MAPPINGS = {
    "benchmark-ratchets-and-anti-goodhart-evidence": (
        "Adds a current multilingual natural repository-task construction funnel, full-suite executable oracle, per-instance pathology metadata, and setup/clarity ablations that expose why benchmark membership is not construct validity.",
        "The released tasks and automated labels are not locally validated en masse; post-snapshot filtering reduces but does not eliminate contamination, and no local benchmark score is established.",
    ),
    "artifact-graphs-audit-logs-and-replay": (
        "Supplies concrete source, repository, base-commit, solution-patch, test-patch, image, parser, and test-transition identities that a replayable repository task must bind.",
        "Dataset records and image manifests do not prove local replay, independent evaluation, authority-to-effect linkage, or rollback completeness.",
    ),
    "integrated-reference-architecture": (
        "Provides a natural repository-change substrate for testing the same candidate through matched test-only, record-only, and full-governance admission routes with visible utility, unsafe admission, false blocking, latency, rollback, residual, and cost outcomes.",
        "No local gold run, candidate campaign, final heldout result, governance advantage, deployment, safety, or transfer result exists yet.",
    ),
    "prototype-roadmap": (
        "Replaces authored repository fixtures in the empirical lane with post-snapshot public merged changes while requiring setup repair, gold execution, test-path collision guards, independent task review, and final-heldout custody.",
        "The 12 selected development tasks are debugging inputs, not the final denominator or evidence for a chapter claim.",
    ),
    "readiness-gates-residual-escrow-and-quarantine": (
        "Adds concrete instrument-failure gates for missing images, broken setup, parser drift, implicit naming, external context, test coupling, emulation cost, and failed positive controls.",
        "A failed instrument closes the denominator and cannot be laundered into negative evidence about a model, mechanism, or governance architecture.",
    ),
}

PASSAGES = [
    "arXiv:2602.23866v2, Sections 3.1-3.3 (collection, setup synthesis, paired full-suite execution)",
    "arXiv:2602.23866v2, Sections 4.1-4.3 (setup ablation, clarity filtering, task pathologies)",
    "Official GitHub evaluator README and pinned Hugging Face dataset revision 475dd5e8703bb5fb22dd3c60b5d038b019eba1e0",
]


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    found = False
    for index, row in enumerate(inventory):
        if row.get("id") == SOURCE_ID:
            inventory[index] = RECORD
            found = True
            break
    if not found:
        insert_at = next((i + 1 for i, row in enumerate(inventory) if row.get("id") == "ext_swe_bench_2023"), len(inventory))
        inventory.insert(insert_at, RECORD)

    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapters = {chapter["id"]: chapter for part in structure["parts"] for chapter in part["chapters"]}
    for chapter_id, (support, limits) in MAPPINGS.items():
        chapter = chapters[chapter_id]
        if SOURCE_ID not in chapter["source_ids"]:
            chapter["source_ids"].append(SOURCE_ID)
        mapping = {
            "source_id": SOURCE_ID,
            "mapped_support": support,
            "limits": limits,
            "passage_refs": PASSAGES,
            "passage_review_state": "reviewed",
            "passage_review_note": "Primary paper, official code/data descriptions, pinned metadata, and local preflight receipt reviewed; no paper result is promoted into local evidence.",
        }
        rows = chapter.setdefault("claim_source_mappings", [])
        for index, row in enumerate(rows):
            if row.get("source_id") == SOURCE_ID:
                rows[index] = mapping
                break
        else:
            rows.append(mapping)

    INVENTORY.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    STRUCTURE.write_text(json.dumps(structure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Integrated SWE-rebench V2 into five existing chapter owners; no new chapter or support promotion.")


if __name__ == "__main__":
    main()
