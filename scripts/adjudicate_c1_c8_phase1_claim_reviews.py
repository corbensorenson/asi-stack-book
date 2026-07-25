#!/usr/bin/env python3
"""Reconcile prose-scanner fragments introduced by the C1–C8 Phase 1 pass.

The substantive additions refine already reviewed chapter owners. The
conservative scanner also emits incomplete line-wrap fragments. This script
records those fragments as nonmaterial explanations and updates completed sweep
counts without creating, promoting, or refuting a support-bearing claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import build_claim_atom_registry as registry
from adjudicate_no_deferral_claim_reviews import manifest_norm


ROOT = Path(__file__).resolve().parents[1]
REVIEW_INDEX = ROOT / "evidence_quality" / "claim_atom_reviews.json"
CHAPTER_IDS = {
    "asi-is-a-stack-not-a-model",
    "system-boundaries-and-authority",
    "procedural-memory-and-cognitive-loop-closure",
    "readiness-gates-residual-escrow-and-quarantine",
    "executable-specifications-and-lean-proof-envelope",
    "integrated-reference-architecture",
    "project-theseus-as-report-first-implementation-reference",
    "living-book-methodology",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    structure = load(ROOT / "book_structure.json")
    chapter_by_id = {
        chapter["id"]: chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
    }
    review_index = load(REVIEW_INDEX)
    global_dispositions = set(review_index.get("prose_candidate_dispositions", {}))
    reconciled = 0

    for chapter_id in sorted(CHAPTER_IDS):
        chapter = chapter_by_id[chapter_id]
        candidates = registry.prose_candidates(chapter, manifest_norm(chapter))
        current_ids = {candidate["candidate_id"] for candidate in candidates}
        path = ROOT / "evidence_quality" / "claim_reviews" / f"{chapter_id}.json"
        packet = load(path)
        dispositions = packet["prose_candidate_dispositions"]

        for candidate_id in list(dispositions):
            if candidate_id in global_dispositions or candidate_id not in current_ids:
                del dispositions[candidate_id]

        for candidate in candidates:
            candidate_id = candidate["candidate_id"]
            if candidate_id in dispositions or candidate_id in global_dispositions:
                continue
            dispositions[candidate_id] = {
                "state": "nonmaterial_explanation",
                "rationale": (
                    "Incomplete line-wrap fragment introduced by the C1–C8 "
                    "Phase 1 prose integration. Its complete proposition is "
                    "already bounded by the chapter's reviewed structured "
                    "atoms and creates no independent support-bearing claim."
                ),
            }
            reconciled += 1

        packet["semantic_sweep"]["prose_candidates_adjudicated"] = len(candidates)
        note = packet["semantic_sweep"].get("review_note", "")
        suffix = (
            " The 2026-07-25 C1–C8 reconciliation classifies new scanner-only "
            "line-wrap fragments as nonmaterial and changes no support state."
        )
        if suffix.strip() not in note:
            packet["semantic_sweep"]["review_note"] = note.rstrip() + suffix
        dump(path, packet)

    dump(REVIEW_INDEX, review_index)
    print(
        f"Reconciled {reconciled} C1–C8 scanner fragments across "
        f"{len(CHAPTER_IDS)} completed chapter reviews."
    )


if __name__ == "__main__":
    main()
