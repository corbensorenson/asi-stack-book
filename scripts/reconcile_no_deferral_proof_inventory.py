#!/usr/bin/env python3
"""Reconcile no-deferral chapter targets with proof triage and adequacy review."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
ADEQUACY = ROOT / "docs" / "proof_adequacy_review.md"
MARKER_START = "<!-- NO-DEFERRAL-PROOF-ADEQUACY:START -->"
MARKER_END = "<!-- NO-DEFERRAL-PROOF-ADEQUACY:END -->"
CHAPTER_IDS = {
    "dangerous-capability-domains-and-misuse-uplift",
    "human-ai-communication-persuasion-and-epistemic-security",
    "governed-objective-formation-value-learning-and-goal-integrity",
    "institutions-international-coordination-and-public-legitimacy",
    "adversarial-machine-learning-and-model-attack-surface",
    "autonomous-replication-proliferation-and-containment",
    "durable-semantic-memory-and-knowledge-lattices",
    "ai-deployment-transition-distribution-and-human-agency",
    "learning-theory-generalization-and-scaling-science",
    "physical-compute-infrastructure-energy-and-environmental-constraints",
    "scientific-discovery-and-experimental-governance",
    "societal-resilience-and-misuse-defense",
    "open-weight-release-and-post-release-control",
    "content-authenticity-watermarking-and-synthetic-media-integrity",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    structure = load(STRUCTURE)
    chapters = {
        chapter["id"]: chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] in CHAPTER_IDS
    }
    triage = load(TRIAGE)
    records = [
        row for row in triage["records"] if row.get("chapter_id") not in CHAPTER_IDS
    ]
    for chapter_id in sorted(CHAPTER_IDS):
        chapter = chapters[chapter_id]
        target = chapter["proof_targets"][0]
        records.append(
            {
                "tag": target["tag"],
                "chapter_id": chapter_id,
                "module": target["module"],
                "formal_target": target["target"],
                "target_status": target["status"],
                "triage": "process-contract",
                "recommended_route": "policy-model-first",
                "rationale": (
                    f"The planned admission boundary gives {chapter['title']} a finite "
                    "identity/authority/version/check/residual guard, but static authored "
                    "fields cannot establish the chapter mechanism, empirical effect, "
                    "independent enforcement, transfer, release readiness, AGI, or ASI. "
                    "Model the full lifecycle and rejecting routes before formal work."
                ),
            }
        )
    manifest = load(ROOT / "proofs" / "proof_manifest.json")
    order = {row["tag"]: index for index, row in enumerate(manifest["records"])}
    triage["records"] = sorted(records, key=lambda row: order[row["tag"]])
    triage["record_count"] = len(triage["records"])
    triage["updated"] = "2026-07-24"
    TRIAGE.write_text(json.dumps(triage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    rows = []
    for chapter_id in sorted(CHAPTER_IDS):
        title = chapters[chapter_id]["title"]
        rows.append(
            f"| `{chapter_id}` | 1 | needs richer state-machine or review semantics | "
            f"The planned finite admission boundary preserves identity, authority, "
            f"version, required checks, residual ownership, and a no-effect ceiling for "
            f"{title}. Build the chapter-specific lifecycle, rejecting routes, executable "
            f"consumers, and competent natural/adversarial campaign before interpreting "
            f"the guard as mechanism efficacy, transfer, readiness, or release evidence. |"
        )
    block = "\n".join([MARKER_START, *rows, MARKER_END])
    text = ADEQUACY.read_text(encoding="utf-8")
    if MARKER_START in text:
        prefix, rest = text.split(MARKER_START, 1)
        _, suffix = rest.split(MARKER_END, 1)
        text = prefix + block + suffix
    else:
        text = text.replace("\n## Follow-Through Increments", f"\n{block}\n\n## Follow-Through Increments")
    ADEQUACY.write_text(text, encoding="utf-8")
    print(f"Reconciled {len(CHAPTER_IDS)} targets; proof triage now has {len(records)} records.")


if __name__ == "__main__":
    main()
