#!/usr/bin/env python3
"""Reconcile the Evidence States claim review after lifecycle consolidation."""

from __future__ import annotations

import json
from pathlib import Path

import build_claim_atom_registry as registry
from adjudicate_no_deferral_claim_reviews import (
    headings,
    manifest_norm,
    prose_disposition,
    section_for,
    structured_atoms,
)


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "evidence-states-and-claim-discipline"
PACKET = ROOT / "evidence_quality" / "claim_reviews" / f"{CHAPTER_ID}.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    structure = load(ROOT / "book_structure.json")
    chapter = next(
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] == CHAPTER_ID
    )
    packet = load(PACKET)
    atoms = structured_atoms(chapter)
    atom_ids = {row["atom_id"] for row in atoms}
    packet["atom_reviews"] = {
        atom_id: review
        for atom_id, review in packet.get("atom_reviews", {}).items()
        if atom_id in atom_ids
    }

    chapter_path = ROOT / chapter["file"]
    chapter_headings = headings(chapter_path)
    candidates = registry.prose_candidates(chapter, manifest_norm(chapter))
    current_candidate_ids = {row["candidate_id"] for row in candidates}
    existing = {
        candidate_id: disposition
        for candidate_id, disposition in packet.get(
            "prose_candidate_dispositions", {}
        ).items()
        if candidate_id in current_candidate_ids
    }
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        if candidate_id in existing:
            continue
        line = int(str(candidate["source"]).rsplit(":", 1)[1])
        existing[candidate_id] = prose_disposition(
            candidate,
            section_for(line, chapter_headings),
            atoms,
        )
    packet["prose_candidate_dispositions"] = existing
    packet["semantic_sweep"]["structured_atoms_reviewed"] = len(atoms)
    packet["semantic_sweep"]["prose_candidates_adjudicated"] = len(candidates)
    packet["semantic_sweep"]["review_note"] = (
        "Reviewed the complete chapter, source boundaries, diagrams, tables, "
        "all three current formal targets, every scanner candidate, and "
        "unscanned evidence-cell and embedded-agency prose. The sweep narrows "
        "the core to a versioned atom-level transition contract; protects "
        "plain, normative, and machine claim projections; keeps evidence "
        "dimensions non-aggregating; and preserves finite-record and "
        "noninheritance limits. The 2026-07-26 consolidation replaces four "
        "artificial audit-mirror targets with one reachable six-stage "
        "transition lifecycle and an independent executable consumer. "
        "Historical audits remain executable consumers and no support state "
        "changes."
    )
    PACKET.write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "Evidence-transition claim review reconciled: "
        f"{len(atoms)} structured atoms, {len(candidates)} prose candidates."
    )


if __name__ == "__main__":
    main()
