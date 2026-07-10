#!/usr/bin/env python3
"""Build the three-contribution focus contract and 54-chapter assignment map."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "book_structure.json"
OUTPUT = ROOT / "products" / "contribution_focus_contract.json"

CONTRIBUTIONS: dict[str, dict[str, Any]] = {
    "governed-cognition-interface-contracts": {
        "label": "Governed-cognition interface contracts",
        "defended_claim": "Responsibility, authority, context, planning, verification, execution, replacement, and review can be joined through typed contracts that preserve refusal, narrowing, rollback, and accountable handoff state.",
        "not_claim": "This does not establish a complete ASI architecture, deployed enforcement, alignment, safety, or optimal modularity.",
        "empirical_lane": "governed repository-change vertical slice plus authority/revocation trace invariants",
        "primary_product": "architecture_reference",
        "legacy_subtracks": ["governed-self-improvement-boundary"],
    },
    "claim-state-transition-discipline": {
        "label": "Public claim-state transition discipline",
        "defended_claim": "A living technical work can make claim identity, support movement, negative evidence, review, scope, and prohibited inference explicit enough to block silent promotion and evidence laundering.",
        "not_claim": "This does not prove that the support ladder is epistemically optimal, that reviewers are correct, or that any chapter thesis is true.",
        "empirical_lane": "claim/evidence ledgers, transition gates, contradiction controls, and adversarial counterexample pressure tests",
        "primary_product": "evidence_registry",
        "legacy_subtracks": [
            "living-evidence-book-methodology",
            "claim-support-states-and-evidence-laundering-prevention",
            "proof-carrying-claims-and-ai-contracts"
        ],
    },
    "record-reality-residual-honesty": {
        "label": "Record/reality reconciliation and residual honesty",
        "defended_claim": "Receipts and ledgers become useful governance only when independent observation can challenge them and unresolved effects, costs, failures, and rollback gaps remain conserved as owned residuals.",
        "not_claim": "This does not prove complete observation, tamper-proof logging, safe governance, efficient oversight, or production reliability.",
        "empirical_lane": "matched governed/baseline workload, receipt mismatch, hidden-residual, rollback, and governance-overhead measurements",
        "primary_product": "evidence_registry",
        "legacy_subtracks": ["costed-routing-residual-accounting-resource-discipline"],
    },
}

GROUPS = {
    "governed-cognition-interface-contracts": [
        "asi-is-a-stack-not-a-model", "system-boundaries-and-authority",
        "scalable-oversight-and-adversarial-ai-control", "human-intent-as-a-formal-input",
        "constitutional-alignment-substrate", "moral-uncertainty-and-value-conflict",
        "stable-capability-fields", "capability-replacement-and-rollback",
        "security-kernel-and-digital-scifs", "model-weight-custody-and-hardware-roots-of-trust",
        "ai-supply-chain-integrity-and-lifecycle-provenance", "recursive-self-improvement-boundaries",
        "open-ended-improvement-engines", "intent-to-execution-contracts",
        "planning-as-a-control-layer", "cognitive-compilation-and-semantic-ir",
        "virtual-context-abi", "labor-os-and-typed-jobs",
        "runtime-adapters-tool-permissions-and-human-approval",
        "inter-stack-protocols-identity-and-economic-exchange",
        "routing-heads-and-specialist-cores", "readiness-gates-residual-escrow-and-quarantine",
        "personal-compute-hives-and-federated-edge-intelligence",
        "artifact-steward-agents-and-living-project-governance",
        "integrated-reference-architecture"
    ],
    "claim-state-transition-discipline": [
        "evidence-states-and-claim-discipline", "verification-bandwidth-and-context-adequacy",
        "claim-ledgers-and-belief-revision", "spinoza-verification-and-proof-carrying-claims",
        "governed-deliberation-and-test-time-scaling",
        "executable-specifications-and-lean-proof-envelope",
        "benchmark-ratchets-and-anti-goodhart-evidence",
        "capability-thresholds-and-deployment-commitments",
        "adversarial-evaluation-sandbagging-and-training-time-deception",
        "safety-cases-and-structured-assurance", "living-book-methodology",
        "open-research-agenda-and-bibliography-plan"
    ],
    "record-reality-residual-honesty": [
        "the-efficient-asi-hypothesis", "failure-modes-of-ungoverned-intelligence",
        "context-transactions-snapshots-mounts-and-taint",
        "artifact-graphs-audit-logs-and-replay",
        "procedural-memory-and-cognitive-loop-closure",
        "compact-generative-systems-and-residual-honesty", "fast-generation-architectures",
        "rankfold-neuralfold-and-artifact-compression", "resource-economics-and-token-budgets",
        "mathematical-and-search-substrates", "circle-calculus-and-proof-carrying-ai-contracts",
        "coil-attention-cyclic-memory-and-recurrence-contracts",
        "coilra-multicoil-rope-and-cyclic-mixers",
        "policy-optimization-and-learning-from-feedback",
        "data-engines-continual-learning-and-unlearning",
        "project-theseus-as-report-first-implementation-reference", "prototype-roadmap"
    ],
}

PRIMARY_OWNERS = {
    "system-boundaries-and-authority", "intent-to-execution-contracts",
    "recursive-self-improvement-boundaries", "integrated-reference-architecture",
    "evidence-states-and-claim-discipline", "claim-ledgers-and-belief-revision",
    "executable-specifications-and-lean-proof-envelope", "living-book-methodology",
    "artifact-graphs-audit-logs-and-replay",
    "compact-generative-systems-and-residual-honesty",
    "resource-economics-and-token-budgets",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_contract() -> dict[str, Any]:
    structure = load_json(MANIFEST)
    chapters = [chapter for part in structure["parts"] for chapter in part["chapters"]]
    assignment: dict[str, str] = {}
    for contribution_id, chapter_ids in GROUPS.items():
        for chapter_id in chapter_ids:
            if chapter_id in assignment:
                raise ValueError(f"duplicate contribution assignment: {chapter_id}")
            assignment[chapter_id] = contribution_id
    manifest_ids = {chapter["id"] for chapter in chapters}
    if set(assignment) != manifest_ids:
        raise ValueError(f"assignment mismatch: {sorted(set(assignment) ^ manifest_ids)}")
    rows = []
    for position, chapter in enumerate(chapters, start=1):
        contribution_id = assignment[chapter["id"]]
        rows.append(
            {
                "position": position,
                "chapter_id": chapter["id"],
                "chapter_title": chapter["title"],
                "contribution_id": contribution_id,
                "contribution_role": "primary_owner" if chapter["id"] in PRIMARY_OWNERS else "supporting_or_integration",
                "primary_product": CONTRIBUTIONS[contribution_id]["primary_product"],
                "independent_flagship_claim": False,
            }
        )
    return {
        "schema_version": "asi_stack.contribution_focus_contract.v0",
        "program_rule": "Exactly three program-level defended contributions; every chapter has one primary contribution role and is not an independent flagship claim.",
        "contributions": [dict({"id": key}, **value) for key, value in CONTRIBUTIONS.items()],
        "chapter_assignments": rows,
        "summary": {
            "contribution_count": 3,
            "chapter_count": len(rows),
            "primary_owner_count": sum(row["contribution_role"] == "primary_owner" for row in rows),
            "supporting_or_integration_count": sum(row["contribution_role"] == "supporting_or_integration" for row in rows),
            "independent_flagship_chapter_count": 0,
        },
        "non_claims": [
            "Selection and assignment are research-program controls, not novelty proof.",
            "A primary owner does not imply adequate evidence, external review, or support-state promotion.",
            "Supporting chapters remain part of the book without becoming separate flagship contribution claims.",
            "No chapter-core support state changes."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = json.dumps(build_contract(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit(f"{OUTPUT.relative_to(ROOT)} is stale; run without --check")
        print("Contribution focus contract is current.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
