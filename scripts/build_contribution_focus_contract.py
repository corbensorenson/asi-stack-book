#!/usr/bin/env python3
"""Build the three-contribution focus contract and live-chapter assignment map."""

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
        "exit_ladder": {
            "bounded_claim_slice": "For the tracked Human Reader source-link repair, full governed admission blocks the declared out-of-scope mutation before effect and reaches the expected residual-free terminal state after a partial-effect crash or compensable external Git effect.",
            "closest_implemented_comparator": "The P5-U1 record-only route captures intent, partial effects, external effects, and outcomes without adding admission, recovery, or compensation policy.",
            "simplest_credible_baseline": "The P5-U1 direct route applies the repair and runs its ordinary two-file source-link check without governance records.",
            "positive_and_instrument_controls": "All three routes must complete the happy path; twelve state checks and seven validator-level mutations must detect route loss, false state, authority, compensation, classification, and support-record corruption.",
            "distinctive_mechanism_ablation": "Remove admission and governed recovery while preserving record capture, yielding the record-only route on the same four paths.",
            "strongest_alternative_explanation": "The replay is retrospective, local, and authored after the successful repair was known; the route code and checks may encode the expected differences without predicting usefulness on natural work.",
            "outcome_dispositions": {
                "success": "Preserve the bounded local route result with no chapter-core movement; use it to qualify the natural campaign's authority, recovery, compensation, and cost instruments.",
                "negative": "If the governed route fails a required state check or does not differ from record-only on the declared fault, treat the claimed mechanism as unimplemented or ineffective at this scope and repair or narrow it.",
                "inconclusive": "If the positive control, mutation sensitivity, historical pre-fix identity, or effect-state observation fails, classify the instrument or replay as N0 and draw no route conclusion.",
                "support_ceiling": "No chapter core may move above argument from this retrospective local replay; prospective natural-task, production, safety, transfer, and general-utility claims remain open."
            },
            "next_behavior_changing_consumer": "The frozen P5 natural stateful-service campaign must use the demonstrated authority, effect, recovery, compensation, and full-cost fields before any protected opening; RuntimeAdapters and AuthorityEffectRefinement remain the formal consumers without a duplicate theorem family."
        },
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
        "exit_ladder": {
            "bounded_claim_slice": "For one content-addressed claim identity, the maintained transition gate rejects a record that changes support without the required prior state, evidence identity, bounded inference, and accepted disposition while preserving explicit no-change and negative outcomes.",
            "closest_implemented_comparator": "The repository's append-only transition records preserve before/after state and prose rationale but, without the identity graph and competence checks, do not independently prevent parent, sibling, or chapter-core support inheritance.",
            "simplest_credible_baseline": "JSON Schema validation of a transition record checks shape and enumerated states without checking whether the evidence belongs to the exact claim or earns the stated inference.",
            "positive_and_instrument_controls": "A known accepted bounded non-core transition and a known accepted no-change record must validate; identity erasure, support laundering, broad-negative inference, and maximum-inference weakening must reject.",
            "distinctive_mechanism_ablation": "Validate schema and file identity while removing claim-identity resolution, competence classification, and prohibited-inference checks.",
            "strongest_alternative_explanation": "The gate may only prove consistency among repository-authored records; it does not show that evidence is true, evaluators are competent, or the support ontology is epistemically optimal.",
            "outcome_dispositions": {
                "success": "Retain a bounded mechanism result for silent-promotion resistance and route it to claim-ledger maintenance; do not infer truth or optimal epistemology.",
                "negative": "If the ablation and full gate accept the same laundering controls, remove or redesign the distinctive mechanism and narrow the defended contribution.",
                "inconclusive": "If positive records cannot pass or the mutations do not isolate identity and inference checks, classify the gate as instrument failure and preserve existing support states.",
                "support_ceiling": "A successful gate can support only the exact non-core transition-discipline mechanism tested; it cannot make any chapter thesis true or promote a chapter core by construction."
            },
            "next_behavior_changing_consumer": "The claim/evidence transition workflow and public status compiler must refuse any future support change whose claim identity, evidence competence, and maximum inference do not pass this ladder."
        },
    },
    "record-reality-residual-honesty": {
        "label": "Record/reality reconciliation and residual honesty",
        "defended_claim": "Receipts and ledgers become useful governance only when independent observation can challenge them and unresolved effects, costs, failures, and rollback gaps remain conserved as owned residuals.",
        "not_claim": "This does not prove complete observation, tamper-proof logging, safe governance, efficient oversight, or production reliability.",
        "empirical_lane": "matched governed/baseline workload, receipt mismatch, hidden-residual, rollback, and governance-overhead measurements",
        "primary_product": "evidence_registry",
        "legacy_subtracks": ["costed-routing-residual-accounting-resource-discipline"],
        "exit_ladder": {
            "bounded_claim_slice": "For the tracked P5-U1 external-effect and crash paths, terminal disposition must agree with independently read Git state, unresolved local or remote effects must remain counted as residuals, and compensation may close branch content only while preserving effect history.",
            "closest_implemented_comparator": "The P5-U1 record-only route records the executor's partial and remote effects but leaves one residual open in each affected path.",
            "simplest_credible_baseline": "The direct route relies on the ordinary source-link test and process result without a separate effect receipt or residual owner.",
            "positive_and_instrument_controls": "The happy path must reconcile as useful on every route; remote-content, retained-history, compensation-closure, residual-count, and false-record mutations must be observable and rejecting.",
            "distinctive_mechanism_ablation": "Remove independent terminal-state reads and residual conservation while retaining the executor's outcome record.",
            "strongest_alternative_explanation": "Local Git exposes state and history unusually well, and repository-authored observers share an institutional and implementation boundary; success may not transfer to opaque services or adversarial observers.",
            "outcome_dispositions": {
                "success": "Preserve the bounded local record/reality and residual result and use it to qualify external-effect observers and compensation accounting in the natural campaign.",
                "negative": "Any receipt/state disagreement, erased history, or uncounted residual refutes the exact implementation claim and must remain visible until repaired or narrowed.",
                "inconclusive": "If the observer cannot distinguish effect, compensation, history, and residual states, classify the instrument as N0 rather than treating missing observations as clean closure.",
                "support_ceiling": "No complete-observation, tamper-proof logging, production reliability, efficient oversight, safety, or chapter-core promotion follows from the local replay."
            },
            "next_behavior_changing_consumer": "The P5 natural campaign's independently separated effect monitor and residual ledger must reproduce these distinctions over multiple external dependencies before protected outcomes can support a broader claim."
        },
    },
}

GROUPS = {
    "governed-cognition-interface-contracts": [
        "asi-is-a-stack-not-a-model", "system-boundaries-and-authority",
        "scalable-oversight-and-adversarial-ai-control", "human-intent-as-a-formal-input",
        "human-factors-and-meaningful-control-in-oversight",
        "human-ai-communication-persuasion-and-epistemic-security",
        "constitutional-alignment-substrate",
        "inner-alignment-mesa-optimization-and-learned-objective-integrity",
        "moral-uncertainty-and-value-conflict",
        "governed-objective-formation-value-learning-and-goal-integrity",
        "institutions-international-coordination-and-public-legitimacy",
        "societal-resilience-and-misuse-defense",
        "military-ai-autonomous-weapons-and-strategic-stability",
        "stable-capability-fields", "capability-replacement-and-rollback",
        "security-kernel-and-digital-scifs",
        "adversarial-machine-learning-and-model-attack-surface",
        "privacy-data-rights-and-information-flow-governance",
        "confidential-and-verifiable-ai-computation",
        "model-weight-custody-and-hardware-roots-of-trust",
        "open-weight-release-and-post-release-control",
        "ai-supply-chain-integrity-and-lifecycle-provenance", "recursive-self-improvement-boundaries",
        "open-ended-improvement-engines",
        "autonomous-replication-proliferation-and-containment",
        "intent-to-execution-contracts",
        "planning-as-a-control-layer", "cognitive-compilation-and-semantic-ir",
        "virtual-context-abi", "durable-semantic-memory-and-knowledge-lattices",
        "labor-os-and-typed-jobs",
        "ai-work-surfaces-agent-harnesses-and-organizational-absorption",
        "human-ai-organizations-delegation-and-accountability",
        "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty",
        "ai-deployment-transition-distribution-and-human-agency",
        "runtime-adapters-tool-permissions-and-human-approval",
        "inter-stack-protocols-identity-and-economic-exchange",
        "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
        "routing-heads-and-specialist-cores", "replaceable-cognitive-substrates-beyond-transformer-monoculture",
        "relational-dimension-compilation-and-polyadic-cognition",
        "governed-model-training-distributed-optimization-and-scaling",
        "learning-compute-topology-and-adaptive-process-architecture",
        "adjudicated-persistence-and-the-adaptive-commit-boundary",
        "readiness-gates-residual-escrow-and-quarantine",
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
        "safety-cases-and-structured-assurance",
        "white-box-evidence-interpretability-and-activation-governance",
        "dangerous-capability-domains-and-misuse-uplift",
        "learning-theory-generalization-and-scaling-science",
        "scientific-discovery-and-experimental-governance",
        "living-book-methodology",
        "open-research-agenda-and-bibliography-plan"
    ],
    "record-reality-residual-honesty": [
        "the-efficient-asi-hypothesis", "failure-modes-of-ungoverned-intelligence",
        "perception-sensor-fusion-and-observation-trust",
        "governed-world-models-and-reality-grounding",
        "context-transactions-snapshots-mounts-and-taint",
        "artifact-graphs-audit-logs-and-replay",
        "embodied-agency-real-time-control-and-physical-safety",
        "procedural-memory-and-cognitive-loop-closure",
        "compact-generative-systems-and-residual-honesty", "fast-generation-architectures",
        "rankfold-neuralfold-and-artifact-compression", "resource-economics-and-token-budgets",
        "physical-compute-infrastructure-energy-and-environmental-constraints",
        "mathematical-and-search-substrates", "circle-calculus-and-proof-carrying-ai-contracts",
        "coil-attention-cyclic-memory-and-recurrence-contracts",
        "coilra-multicoil-rope-and-cyclic-mixers",
        "policy-optimization-and-learning-from-feedback",
        "data-engines-continual-learning-and-unlearning",
        "content-authenticity-watermarking-and-synthetic-media-integrity",
        "governed-operations-incident-command-and-graceful-degradation",
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
