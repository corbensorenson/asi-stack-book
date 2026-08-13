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
    "adversarial-evaluation-sandbagging-and-training-time-deception.prose.24cc47fd5e4d",
}
REVIEWED_CHAPTERS = {
    "adversarial-evaluation-sandbagging-and-training-time-deception",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    queue = load(QUEUE)
    candidates = queue["candidates"]
    pending = {
        row["candidate_id"]: row
        for row in candidates
        if row.get("review_state") == "pending_materiality_adjudication"
    }
    if set(pending) != EXPECTED:
        raise SystemExit(
            "EM2 claim-review pending set drifted: "
            f"expected {sorted(EXPECTED)}, found {sorted(pending)}"
        )
    counts = Counter(row["chapter_id"] for row in candidates)
    for chapter_id in REVIEWED_CHAPTERS:
        path = REVIEWS / f"{chapter_id}.json"
        review = load(path)
        for candidate_id, row in pending.items():
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
            " The white-box/evaluation EM2 publication-composition additions were re-reviewed; "
            "the scanner delta is a line-wrapped non-inference clause, and the composition "
            "adds no new material or support-bearing claim."
        )
        if suffix.strip() not in prior:
            review["semantic_sweep"]["review_note"] = prior.rstrip() + suffix
        dump(path, review)
    print(f"Adjudicated {len(EXPECTED)} EM2 prose candidates and re-reviewed {len(REVIEWED_CHAPTERS)} chapters.")


if __name__ == "__main__":
    main()
