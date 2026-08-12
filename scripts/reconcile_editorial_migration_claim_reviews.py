#!/usr/bin/env python3
"""Adjudicate the bounded claim-scanner deltas from the EM2 pilot."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
REVIEWS = ROOT / "evidence_quality/claim_reviews"
EXPECTED = {
    "compact-generative-systems-and-residual-honesty.prose.f453a2a79d93",
    "governed-deliberation-and-test-time-scaling.prose.9ae4362e7bf9",
    "rankfold-neuralfold-and-artifact-compression.prose.74d774f633ee",
    "resource-economics-and-token-budgets.prose.14e49047fde9",
    "resource-economics-and-token-budgets.prose.2913c68cb1f8",
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
    for candidate_id, row in pending.items():
        chapter_id = row["chapter_id"]
        path = REVIEWS / f"{chapter_id}.json"
        review = load(path)
        review["prose_candidate_dispositions"][candidate_id] = {
            "state": "nonmaterial_explanation",
            "rationale": (
                "EM2 publication-composition semantic review identifies this scanner hit as a "
                "line-wrapped clause from an explicit ownership or uncertainty boundary, not a "
                "complete independent proposition. The surrounding chapter preserves local claim, "
                "source, proof, test, evidence, authority, and support ownership without creating a "
                "new support-bearing atom."
            ),
        }
        review["semantic_sweep"]["prose_candidates_adjudicated"] = counts[chapter_id]
        prior = review["semantic_sweep"].get("review_note", "")
        suffix = (
            " EM2 publication-composition additions were re-reviewed; new scanner deltas are "
            "line-wrapped ownership or uncertainty clauses, not new material claims."
        )
        if suffix.strip() not in prior:
            review["semantic_sweep"]["review_note"] = prior.rstrip() + suffix
        dump(path, review)
    print(f"Adjudicated {len(EXPECTED)} EM2 prose candidates across {len(set(row['chapter_id'] for row in pending.values()))} chapters.")


if __name__ == "__main__":
    main()
