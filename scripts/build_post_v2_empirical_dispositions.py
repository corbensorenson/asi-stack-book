#!/usr/bin/env python3
"""Build accepted non-core transition records and core no-change decisions."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSITIONS = ROOT / "evidence_transitions/post_v2"
LEDGER = ROOT / "claim_decisions/post_v2_empirical_dispositions.json"

PROGRAMS = [
    {
        "id": "governed_work_flagship",
        "claim_id": "post_v2_governed_work_flagship.bounded_matched_local_result",
        "result": "experiments/post_v2_governed_work_flagship/results/2026-07-10-local.json",
        "doc": "docs/post_v2_governed_work_flagship.md",
        "validator": "scripts/validate_post_v2_governed_work_flagship.py",
        "chapters": ["intent-to-execution-contracts", "artifact-graphs-audit-logs-and-replay", "resource-economics-and-token-budgets"],
        "core_claims": ["intent-to-execution-contracts.core", "artifact-graphs-audit-logs-and-replay.core", "resource-economics-and-token-budgets.core"],
        "reason": "Sixteen model-generated plan/code runs provide bounded local comparative evidence for authority, effect observation, receipt/path reconciliation, residuals, rollback, quarantine, and measured cost, while zero governed releases and two failed rollbacks block broader promotion.",
        "negative_results": ["governed route released zero useful candidates", "two governed rollbacks remained inexact and quarantined", "four governed residuals were discovered and two remained open", "the prevalidation pilot was preserved as non-evidentiary after protocol defects"],
        "limitations": ["eight disposable local tasks", "one small local coder model", "internal subprocess observer only", "no deployed authorization, sandbox, verifier, rollback, or release service", "no production transfer or economics"],
        "required": ["deployed or externally reviewable governed-work traces", "broader natural workloads and models", "independent verifier-quality assessment", "production cost, throughput, rollback, and residual evidence"],
    },
    {
        "id": "routing_deliberation",
        "claim_id": "post_v2_routing_deliberation.bounded_matched_local_result",
        "result": "experiments/post_v2_routing_deliberation/results/2026-07-10-local.json",
        "doc": "docs/post_v2_routing_deliberation.md",
        "validator": "scripts/validate_post_v2_routing_deliberation.py",
        "chapters": ["routing-heads-and-specialist-cores", "governed-deliberation-and-test-time-scaling"],
        "core_claims": ["routing-heads-and-specialist-cores.core", "governed-deliberation-and-test-time-scaling.core"],
        "reason": "The frozen three-seed held-out study measures specialist routing, generalist baselines, matched operation caps, adaptive/fixed/no-deliberation arms, and extra-compute harm, while route separability and zero fallback activation block broader routing claims and deterministic verification blocks model-scale deliberation claims.",
        "negative_results": ["fallback and abstention activated zero times", "oracle, learned, and rule routing were indistinguishable on an overly separable corpus", "fixed three-step deliberation harmed 15 initially correct answers", "one adaptive case exhausted its budget without a verified candidate"],
        "limitations": ["synthetic four-family workload", "deterministic specialists and task verifier", "no language-model reasoning traces", "no trained-specialist interference or production fallback calibration", "no model-scale transfer"],
        "required": ["harder ambiguous routing workload with exercised fallback and abstention", "trained specialists and interference measurements", "language-model deliberation with independent verifier-quality assessment", "production latency, cost, safety, and transfer evidence"],
    },
    {
        "id": "update_causality",
        "claim_id": "post_v2_update_causality.bounded_real_mutation_result",
        "result": "experiments/post_v2_update_causality/results/2026-07-10-local.json",
        "doc": "docs/post_v2_update_causality.md",
        "validator": "scripts/validate_post_v2_update_causality.py",
        "chapters": ["data-engines-continual-learning-and-unlearning", "policy-optimization-and-learning-from-feedback", "open-ended-improvement-engines", "recursive-self-improvement-boundaries"],
        "core_claims": ["data-engines-continual-learning-and-unlearning.core", "policy-optimization-and-learning-from-feedback.core", "open-ended-improvement-engines.core", "recursive-self-improvement-boundaries.core"],
        "reason": "Three seeds and four arms establish real local parameter/checkpoint/output causality, best/final authority, forgetting, deletion-cohort differences, rollback identity, and descendant invalidation, while modest utility and synthetic scope block production learning, unlearning, open-ended improvement, or recursive-improvement claims.",
        "negative_results": ["challenger utility gains were modest and seed-sensitive", "bounded and regularized updates reduced retained-base accuracy on average", "best and final challenger checkpoints disagreed on 62 test decisions", "deletion-aware retraining does not prove storage erasure or verified forgetting"],
        "limitations": ["small synthetic policy network", "poisoned-cohort exclusion is not production unlearning", "no human or model feedback", "fixed stopped campaign is not open-ended", "rollback covers recorded checkpoints only", "no recursive self-proposed update"],
        "required": ["production-scale continual-learning and feedback-update traces", "verified deletion propagation across descendants and storage", "independent evaluator and privacy assessment", "deployed canary, rollback, invalidation, and monitor evidence", "open-ended or recursive campaign evidence if those claims are pursued"],
    },
]


def transition(program: dict) -> dict:
    chapter_refs = [f"chapters/{chapter}.qmd" for chapter in program["chapters"]]
    return {
        "transition_id": f"post_v2.{program['id']}.no_change",
        "claim_id": program["claim_id"],
        "claim_surface_refs": [program["doc"], *chapter_refs, "docs/post_v2_evidence_roadmap.md"],
        "claim_record_refs": [program["result"], program["validator"]],
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "scope_boundary": program["reason"],
        "evidence_roles": ["bounded_local_experiment", "matched_baseline", "negative_result_archive", "content_addressed_result", "no_core_promotion_boundary"],
        "transition_reason": program["reason"],
        "required_artifacts": program["required"],
        "artifact_refs": [program["doc"], program["result"], program["validator"]],
        "evidence_packet_refs": [*chapter_refs, "appendices/C_claim_evidence_matrix.qmd", "evidence_quality/core_claim_vectors.json"],
        "evidence_quality_before_refs": ["evidence_quality/core_claim_vectors.json"],
        "evidence_quality_after_refs": ["evidence_quality/core_claim_vectors.json"],
        "evidence_quality_dimension_deltas": {"reproducibility": "adjacent local replay added", "adversarial_strength": "adjacent bounded controls added", "validity": "still internally assessed", "transfer_distance": "still not established"},
        "source_mapping_refs": [f"appendices/C_claim_evidence_matrix.qmd#{claim}" for claim in program["core_claims"]],
        "verification_command": f"python3 {program['validator']} && python3 scripts/validate_post_v2_empirical_reconciliation.py",
        "verification_result": "pass",
        "negative_results": program["negative_results"],
        "negative_evidence_refs": [program["doc"], program["result"]],
        "downgrade_triggers": ["result validator failure", "raw artifact or checkpoint digest mismatch", "negative result erased", "core support promoted without a separate accepted upward transition", "bounded local result described as production or open-world evidence"],
        "promotion_burden": "; ".join(program["required"]),
        "limitations": program["limitations"],
        "review_status": "accepted",
        "reviewer_refs": ["Author-directed Codex post-v2 empirical cycle"],
        "reviewer_independence": "local maintainer-agent review only; no external human review requested or claimed",
        "acceptance_blockers": program["required"],
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-10---post-v2-empirical-reconciliation",
        "support_state_effect": "blocks_promotion",
        "non_claims": ["does not promote any affected chapter-core claim above argument", "does not establish production transfer, external independence, open-world safety, or ASI capability", *[f"does not promote {claim}" for claim in program["core_claims"]]],
    }


def main() -> None:
    TRANSITIONS.mkdir(parents=True, exist_ok=True)
    transition_refs = []
    decisions = []
    for program in PROGRAMS:
        path = TRANSITIONS / f"{program['id']}_no_change.json"
        path.write_text(json.dumps(transition(program), indent=2) + "\n", encoding="utf-8")
        transition_refs.append(path.relative_to(ROOT).as_posix())
        for claim_id, chapter in zip(program["core_claims"], program["chapters"]):
            decisions.append({
                "claim_id": claim_id,
                "chapter_id": chapter,
                "program_id": program["id"],
                "decision": "no_change",
                "current_support_state": "argument",
                "support_state_effect": "none",
                "result_ref": program["result"],
                "transition_ref": path.relative_to(ROOT).as_posix(),
                "basis": program["reason"],
                "remaining_burden": program["required"],
            })
    ledger = {
        "schema_version": "asi_stack.post_v2_empirical_dispositions.v0",
        "decision_set_id": "post-v2-empirical-dispositions-2026-07-10",
        "recorded_date": "2026-07-10",
        "review_status": "accepted_internal_no_external_human_review",
        "program_count": 3,
        "affected_core_claim_count": 9,
        "transition_refs": transition_refs,
        "decisions": decisions,
        "summary": {"no_change": 9, "promote": 0, "narrow": 0, "demote": 0, "refute": 0, "support_state_changes": 0},
        "non_claims": ["No chapter-core claim moves above argument.", "Internal replay and review do not establish external independence or transfer.", "A non-core transition reference cannot be counted as chapter-core promotion evidence."]
    }
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(PROGRAMS)} transition records and {len(decisions)} core no-change decisions")


if __name__ == "__main__":
    main()
