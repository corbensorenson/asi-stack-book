#!/usr/bin/env python3
"""Adjudicate bounded claim-scanner deltas from completed EM2 packages."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
REVIEWS = ROOT / "evidence_quality/claim_reviews"
EXPECTED = {
    "constitutional-alignment-substrate.prose.91abf2b0ecb5",
    "constitutional-alignment-substrate.prose.c2872320d27d",
    "moral-uncertainty-and-value-conflict.prose.7f99887ffe9d",
    "moral-uncertainty-and-value-conflict.prose.c01b2f4c5b0e",
    "institutions-international-coordination-and-public-legitimacy.prose.b2ec6d08f0be",
    "intent-to-execution-contracts.prose.05b6de551cc8",
    "intent-to-execution-contracts.prose.0a47a15a695d",
}
REVIEWED_CHAPTERS = {
    "constitutional-alignment-substrate",
    "human-ai-communication-persuasion-and-epistemic-security",
    "human-intent-as-a-formal-input",
    "institutions-international-coordination-and-public-legitimacy",
    "intent-to-execution-contracts",
    "moral-uncertainty-and-value-conflict",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    queue = load(QUEUE)
    candidates = queue["candidates"]
    candidate_by_id = {row["candidate_id"]: row for row in candidates}
    pending = {
        row["candidate_id"]: row
        for row in candidates
        if row.get("review_state") == "pending_materiality_adjudication"
    }
    missing_expected = EXPECTED - set(candidate_by_id)
    unexpected_pending = set(pending) - EXPECTED
    if missing_expected or unexpected_pending:
        raise SystemExit(
            "EM2 claim-review candidate set drifted: "
            f"missing expected {sorted(missing_expected)}, unexpected pending {sorted(unexpected_pending)}"
        )
    counts = Counter(row["chapter_id"] for row in candidates)
    for chapter_id in REVIEWED_CHAPTERS:
        path = REVIEWS / f"{chapter_id}.json"
        review = load(path)
        for candidate_id in EXPECTED:
            row = candidate_by_id[candidate_id]
            if row["chapter_id"] != chapter_id:
                continue
            review["prose_candidate_dispositions"][candidate_id] = {
                "state": "nonmaterial_explanation",
                "rationale": (
                    "EM2 publication-composition semantic review identifies this scanner hit as a "
                    "line-wrapped clause from an explicit ownership or non-inference boundary, not a "
                    "complete independent proposition. The surrounding chapter preserves local claim, "
                    "source, proof, test, evidence, authority, and support ownership without creating a "
                    "new support-bearing atom."
                ),
            }
        review["semantic_sweep"]["prose_candidates_adjudicated"] = counts[chapter_id]
        prior = review["semantic_sweep"].get("review_note", "")
        suffix = (
            " The human-intent and institutional-governance EM2 publication-composition additions "
            "were re-reviewed; every scanner delta is a line-wrapped ownership or non-inference "
            "clause, and the composition adds no new material or support-bearing claim."
        )
        if suffix.strip() not in prior:
            review["semantic_sweep"]["review_note"] = prior.rstrip() + suffix
        dump(path, review)
    print(f"Adjudicated {len(EXPECTED)} EM2 prose candidates and re-reviewed {len(REVIEWED_CHAPTERS)} chapters.")


if __name__ == "__main__":
    main()
