#!/usr/bin/env python3
"""Build the cumulative repository-change trace for the 22-unit narrative route."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPINE = ROOT / "products" / "narrative_product_spine.json"
OUTPUT = ROOT / "products" / "narrative_running_example_trace.json"

ARTIFACT_BY_CHAPTER = {
    "asi-is-a-stack-not-a-model": "artifact://responsibility-boundary-map",
    "the-efficient-asi-hypothesis": "artifact://routed-cost-quality-ledger",
    "system-boundaries-and-authority": "artifact://scoped-authority-and-failure-map",
    "evidence-states-and-claim-discipline": "artifact://bounded-claim-state-record",
    "constitutional-alignment-substrate": "artifact://constitutional-conflict-disposition",
    "stable-capability-fields": "artifact://capability-replacement-contract",
    "intent-to-execution-contracts": "artifact://validated-command-contract",
    "planning-as-a-control-layer": "artifact://governed-plan-dag",
    "governed-world-models-and-reality-grounding": "artifact://world-model-reconciliation-record",
    "cognitive-compilation-and-semantic-ir": "artifact://semantic-ir-and-loss-map",
    "virtual-context-abi": "artifact://context-mount-and-adequacy-record",
    "durable-semantic-memory-and-knowledge-lattices": "artifact://belief-and-procedure-consolidation-record",
    "verification-bandwidth-and-context-adequacy": "artifact://verification-bandwidth-decision",
    "claim-ledgers-and-belief-revision": "artifact://claim-and-proof-review-record",
    "labor-os-and-typed-jobs": "artifact://typed-job-artifact-graph",
    "runtime-adapters-tool-permissions-and-human-approval": "artifact://observed-effect-operations-recovery-record",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture": "artifact://substrate-route-and-qualification-record",
    "governed-model-training-distributed-optimization-and-scaling": "artifact://developmental-learning-candidate-record",
    "readiness-gates-residual-escrow-and-quarantine": "artifact://readiness-and-bounded-liveness-decision",
    "resource-economics-and-token-budgets": "artifact://governance-lifecycle-cost-ledger",
    "integrated-reference-architecture": "artifact://end-to-end-reference-trace",
    "living-book-methodology": "artifact://book-change-and-release-record",
}


def main() -> None:
    spine = json.loads(SPINE.read_text(encoding="utf-8"))
    chapters = spine["chapters"]
    chapter_ids = [row["chapter_id"] for row in chapters]
    missing = sorted(set(chapter_ids) - set(ARTIFACT_BY_CHAPTER))
    extra = sorted(set(ARTIFACT_BY_CHAPTER) - set(chapter_ids))
    if missing or extra:
        raise SystemExit(f"narrative trace artifact map drift: missing={missing}, extra={extra}")

    initial = ["artifact://human-repository-change-request"]
    cumulative = list(initial)
    previous = initial[0]
    steps = []
    for index, chapter in enumerate(chapters):
        chapter_id = chapter["chapter_id"]
        produced = ARTIFACT_BY_CHAPTER[chapter_id]
        cumulative.append(produced)
        steps.append({
            "order": index + 1,
            "chapter_id": chapter_id,
            "consumes": [previous],
            "produces": [produced],
            "cumulative_artifact_refs": list(cumulative),
            "failure_pressure": chapter["failure_story"],
            "handoff_to": chapter_ids[index + 1] if index + 1 < len(chapter_ids) else None,
        })
        previous = produced

    trace = {
        "schema_version": "asi_stack.narrative_running_example_trace.v0",
        "trace_id": "narrative://governed-repository-change-v0",
        "narrative_spine_ref": "products/narrative_product_spine.json",
        "scenario": "One bounded repository change moves through the twenty-two-unit narrative from human intent to governed development, observed effects, evidence, recovery, publication, or refusal.",
        "initial_artifact_refs": initial,
        "steps": steps,
        "decision": {
            "status": "editorially_complete_candidate_not_release",
            "support_state_effect": "none",
            "release_approved": False,
        },
        "non_claims": [
            "the trace is an editorial continuity contract, not evidence that the architecture works",
            "the generated twenty-two-unit candidate is not a final reader release",
            "the trace does not promote any chapter claim or approve reference chapters for deletion",
            "a compound narrative unit does not inherit evidence or authority from its specialist owners",
        ],
    }
    OUTPUT.write_text(json.dumps(trace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(ROOT)} with {len(steps)} steps and {len(cumulative)} cumulative artifacts.")


if __name__ == "__main__":
    main()
