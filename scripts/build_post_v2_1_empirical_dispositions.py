#!/usr/bin/env python3
"""Build post-v2.1 non-core transitions and chapter-core no-change decisions."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSITION_ROOT = ROOT / "evidence_transitions/post_v2_1"
LEDGER = ROOT / "claim_decisions/post_v2_1_empirical_dispositions.json"
RESULT = "experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json"
RESULT_DOC = "docs/post_v2_1_empirical_results.md"
VALIDATOR = "scripts/validate_post_v2_1_outcomes.py"


TRANSITIONS = [
    {
        "id": "governed_usefulness_rollback",
        "claim": "post_v2_1.governed_usefulness_rollback.bounded_result",
        "empirical_disposition": "narrow",
        "chapters": [
            "intent-to-execution-contracts", "runtime-adapters-tool-permissions-and-human-approval",
            "artifact-graphs-audit-logs-and-replay", "capability-replacement-and-rollback",
            "readiness-gates-residual-escrow-and-quarantine", "security-kernel-and-digital-scifs",
            "resource-economics-and-token-budgets",
        ],
        "reason": "Governance reduced registered primary unsafe releases from 24/36 to 0/36, but useful release remained 2/36 and attack-control exact rollback was 32/36, below both registered usefulness and rollback thresholds.",
        "negative": ["only two of 36 held-out candidates were correct", "governed useful-release rate was 0.0556", "four of 36 attack-control rollbacks remained inexact"],
        "limitations": ["finite synthetic public-safe repository-task corpus", "one locally hosted four-bit model", "internal observer implementation", "no external effects or production service"],
        "burden": ["useful governed throughput at the registered frontier", "effect-complete rollback beyond the local inventory", "independently assessed verifier quality", "production transfer and governance-cost evidence"],
    },
    {
        "id": "ambiguous_routing",
        "claim": "post_v2_1.ambiguous_routing.bounded_result",
        "empirical_disposition": "narrow",
        "chapters": ["routing-heads-and-specialist-cores", "readiness-gates-residual-escrow-and-quarantine", "verification-bandwidth-and-context-adequacy"],
        "reason": "The learned router selected 59/60 correct routes and exercised fallback, abstention, and clarification, but all 360 generated substantive candidates were wrong and the apparent selective-utility gain came entirely from correct non-answer actions.",
        "negative": ["zero of 360 substantive candidate evaluations were correct", "learned answer correctness consisted only of abstention, clarification, and fallback decisions", "one bounded synthetic finite set cannot establish transfer"],
        "limitations": ["synthetic six-action workload", "single model and seed", "internal deterministic criterion evaluator", "no trained-specialist interference or deployment"],
        "burden": ["nonzero substantive answer utility", "independently assessed evaluator validity", "multiple models, seeds, and natural workloads", "production routing safety, latency, cost, and transfer"],
    },
    {
        "id": "real_model_deliberation",
        "claim": "post_v2_1.real_model_deliberation.no_change_result",
        "empirical_disposition": "no_change",
        "chapters": ["governed-deliberation-and-test-time-scaling", "verification-bandwidth-and-context-adequacy"],
        "reason": "All five deliberation arms ended at 0/60 correct; adaptive stopping exhausted five candidates on every request, so utility did not improve and corruption reduction was not estimable on an initially-correct case.",
        "negative": ["no deliberation arm produced one correct final answer", "adaptive stopping never stopped before budget exhaustion", "the fifteen historical harms remain regression logic rather than new held-out evidence"],
        "limitations": ["single small model", "zero initially-correct held-out candidates", "internal evaluator", "no production latency or transfer"],
        "burden": ["a workload with correct and incorrect initial candidates", "adaptive benefit at a matched real budget", "replicated corruption reduction", "independently assessed evaluator and production transfer"],
    },
    {
        "id": "full_state_update",
        "claim": "post_v2_1.full_state_update.no_change_result",
        "empirical_disposition": "no_change",
        "chapters": ["data-engines-continual-learning-and-unlearning", "policy-optimization-and-learning-from-feedback", "open-ended-improvement-engines", "recursive-self-improvement-boundaries"],
        "reason": "Prospective checkpoint authority was honored and retained-task bounds held for eligible challengers, but zero of nine challenger seed-arms reached the registered 0.05 target-utility gain.",
        "negative": ["zero of nine eligible challenger seed-arms met the target-gain threshold", "gains were small and seed-sensitive", "authorized-data comparators crossed the safety bound and remained ineligible"],
        "limitations": ["small synthetic policy network", "three seeds", "fixed twelve-epoch campaign", "no feedback-learning, open-ended, recursive, or deployed update loop"],
        "burden": ["replicated target gain at the retained-task bound", "production-scale update and monitoring traces", "independent validity assessment", "separate evidence for feedback learning, open-endedness, or recursion if claimed"],
    },
    {
        "id": "unlearning_causality",
        "claim": "post_v2_1.unlearning_causality.narrow_result",
        "empirical_disposition": "narrow",
        "chapters": ["data-engines-continual-learning-and-unlearning", "artifact-graphs-audit-logs-and-replay"],
        "reason": "Deletion-aware retraining produced behavioral cohort changes of 4, 0, and 1 and propagated lineage invalidation, while influence reduction remained a confidence proxy and storage erasure remained false at every seed.",
        "negative": ["one seed had zero behavioral deletion-cohort changes", "influence removal was not established", "the immutable source corpus remained stored"],
        "limitations": ["synthetic deletion cohort", "behavioral proxy only", "no privacy audit", "no legal or physical storage-erasure transaction"],
        "burden": ["causal influence-removal evidence", "privacy and member/nonmember assessment", "descendant-wide propagation receipts", "verified storage and backup erasure where claimed"],
    },
    {
        "id": "full_state_rollback",
        "claim": "post_v2_1.full_state_rollback.bounded_result",
        "empirical_disposition": "narrow",
        "chapters": ["capability-replacement-and-rollback", "artifact-graphs-audit-logs-and-replay"],
        "reason": "All fifteen seed-arm transactions restored all 24 declared model, optimizer, scheduler, RNG, cache, checkpoint, backup, and descendant surfaces exactly, but the scope was one local synthetic campaign with no external system effects.",
        "negative": ["rollback identity is bounded to the declared local inventory", "no production cache, remote backup, service, or external effect was exercised", "exact local bytes do not prove semantic or production recovery"],
        "limitations": ["local disposable state trees", "single implementation", "no remote or production effect", "no independent operator"],
        "burden": ["replication across heterogeneous runtimes", "external effect and remote backup recovery", "production recovery objectives and monitoring", "independent replay"],
    },
]


def transition(row: dict) -> dict:
    chapters = [f"chapters/{chapter}.qmd" for chapter in row["chapters"]]
    core_claims = [f"{chapter}.core" for chapter in row["chapters"]]
    return {
        "transition_id": f"post_v2_1.{row['id']}.{row['empirical_disposition']}",
        "claim_id": row["claim"],
        "claim_surface_refs": [RESULT_DOC, *chapters, "docs/post_v2_1_residual_and_transfer_roadmap.md"],
        "claim_record_refs": [RESULT, VALIDATOR],
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "scope_boundary": row["reason"],
        "evidence_roles": ["bounded_local_experiment", "content_addressed_raw_results", "negative_result_archive", "exact_replay_validator", "no_core_promotion_boundary"],
        "transition_reason": row["reason"],
        "required_artifacts": row["burden"],
        "artifact_refs": [RESULT_DOC, RESULT, VALIDATOR],
        "evidence_packet_refs": [*chapters, "appendices/C_claim_evidence_matrix.qmd", "evidence_quality/core_claim_vectors.json"],
        "evidence_quality_before_refs": ["evidence_quality/core_claim_vectors.json"],
        "evidence_quality_after_refs": ["evidence_quality/core_claim_vectors.json"],
        "evidence_quality_dimension_deltas": {"reproducibility": "exact local replay added", "adversarial_strength": "registered controls retained", "validity": "internally assessed only", "transfer_distance": "not established"},
        "source_mapping_refs": [f"appendices/C_claim_evidence_matrix.qmd#{claim}" for claim in core_claims],
        "verification_command": "python3 scripts/validate_post_v2_1_outcomes.py && python3 scripts/validate_post_v2_1_empirical_reconciliation.py",
        "verification_result": "pass",
        "negative_results": row["negative"],
        "negative_evidence_refs": [RESULT_DOC, RESULT],
        "downgrade_triggers": ["raw bundle or artifact replay failure", "negative outcome erasure", "scope or transfer laundering", "core support promotion without a distinct accepted upward transition"],
        "promotion_burden": "; ".join(row["burden"]),
        "limitations": row["limitations"],
        "review_status": "accepted",
        "reviewer_refs": ["Author-directed Codex post-v2.1 empirical cycle"],
        "reviewer_independence": "local maintainer-agent review only; no external human review requested or claimed",
        "acceptance_blockers": row["burden"],
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-11---post-v2-1-empirical-reconciliation",
        "support_state_effect": "blocks_promotion",
        "non_claims": ["does not promote any affected chapter-core claim above argument", "does not establish population validity, production transfer, external independence, open-world safety, or ASI capability", *[f"does not promote {claim}" for claim in core_claims]],
    }


def main() -> None:
    TRANSITION_ROOT.mkdir(parents=True, exist_ok=True)
    transition_refs = {}
    for row in TRANSITIONS:
        path = TRANSITION_ROOT / f"{row['id']}_{row['empirical_disposition']}.json"
        path.write_text(json.dumps(transition(row), indent=2) + "\n", encoding="utf-8")
        transition_refs[row["id"]] = path.relative_to(ROOT).as_posix()
    chapter_rows: dict[str, list[dict]] = {}
    for row in TRANSITIONS:
        for chapter in row["chapters"]:
            chapter_rows.setdefault(chapter, []).append(row)
    decisions = []
    for chapter in sorted(chapter_rows):
        owners = chapter_rows[chapter]
        decisions.append({
            "claim_id": f"{chapter}.core",
            "chapter_id": chapter,
            "program_components": [row["id"] for row in owners],
            "empirical_dispositions": [row["empirical_disposition"] for row in owners],
            "core_decision": "no_change",
            "current_support_state": "argument",
            "support_state_effect": "none",
            "result_ref": RESULT,
            "transition_refs": [transition_refs[row["id"]] for row in owners],
            "basis": " ".join(row["reason"] for row in owners),
            "remaining_burden": sorted({item for row in owners for item in row["burden"]}),
        })
    ledger = {
        "schema_version": "asi_stack.post_v2_1_empirical_dispositions.v0",
        "decision_set_id": "post-v2-1-empirical-dispositions-2026-07-11",
        "recorded_date": "2026-07-11",
        "review_status": "accepted_internal_no_external_human_review",
        "program_count": 3,
        "component_disposition_count": len(TRANSITIONS),
        "affected_core_claim_count": len(decisions),
        "transition_refs": [transition_refs[row["id"]] for row in TRANSITIONS],
        "decisions": decisions,
        "summary": {"no_change": len(decisions), "promote": 0, "narrow_core": 0, "demote": 0, "refute": 0, "support_state_changes": 0},
        "non_claims": ["No chapter-core claim moves above argument.", "Empirical hypothesis narrowing and bounded non-core findings are not chapter-core promotion.", "Internal replay and review do not establish external independence or production transfer.", "A transition reference cannot be counted as support movement without an accepted upward transition."],
    }
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(TRANSITIONS)} transitions and {len(decisions)} chapter-core no-change decisions")


if __name__ == "__main__":
    main()
