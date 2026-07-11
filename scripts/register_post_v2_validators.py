#!/usr/bin/env python3
"""Idempotently append the seven post-v2 validators to registry authority."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"

SPECS = [
    ("validate_post_v2_governed_work_setup.py", "schema_or_structure", "Frozen governed-work corpus, amendment, pilot boundary, pinned model, plan-to-code protocol, fresh Git worktree semantics, and setup mutations.", "Reject task/attack/split drift, holdout leakage, mutable model or seeds, pilot promotion, or removal of real-worktree/plan surfaces.", "Pre-outcome protocol integrity for the realistic governed-work flagship.", "Setup validity does not establish any outcome, model quality, safety, transfer, or support movement.", ["experiments/post_v2_governed_work_flagship/tasks.json", "experiments/post_v2_evidence_program/amendments/governed_work_v1.json", "experiments/post_v2_governed_work_flagship/attempts/2026-07-10-plan-format-pilot/result.json", "schemas/post_v2_governed_work_tasks.schema.json", "schemas/post_v2_evidence_preregistration_amendment.schema.json", "scripts/run_post_v2_governed_work_flagship.py", "scripts/post_v2_governed_work_observer.py", "scripts/validate_post_v2_governed_work_setup.py"]),
    ("validate_post_v2_governed_work_flagship.py", "proof_or_evidence_gate", "Sixteen retained plan/code runs, matched baseline/governed decisions, independent observations, real Git effect replay, hashes, residuals, rollbacks, costs, dispositions, and outcome mutations.", "Reject artifact/hash drift, observer or worktree replay mismatch, erased unsafe release/residual/failed rollback, missing run, or core promotion.", "Bounded local evidence for governed work, record/reality reconciliation, and measured governance cost.", "Does not establish production transfer, external independence, open-world safety, model quality, deployed services, or chapter-core promotion.", ["experiments/post_v2_governed_work_flagship/results/2026-07-10-local.json", "experiments/post_v2_governed_work_flagship/artifacts/model_outputs", "schemas/post_v2_governed_work_result.schema.json", "docs/post_v2_governed_work_flagship.md", "scripts/validate_post_v2_governed_work_flagship.py"]),
    ("validate_post_v2_routing_deliberation_setup.py", "schema_or_structure", "Frozen 300-example balanced corpus, split isolation, route families, operation caps, comparator-only oracle, leakage boundary, runner arms, digest, and setup mutations.", "Reject example overlap, split drift, compute inflation, oracle laundering, mutable corpus, or missing registered arms.", "Pre-outcome protocol integrity for matched routing and deliberation.", "Does not establish routing quality, deliberation benefit, verifier correctness, transfer, or support movement.", ["experiments/post_v2_routing_deliberation/input/corpus.json", "schemas/post_v2_routing_deliberation_corpus.schema.json", "scripts/run_post_v2_routing_deliberation.py", "scripts/validate_post_v2_routing_deliberation_setup.py"]),
    ("validate_post_v2_routing_deliberation.py", "proof_or_evidence_gate", "Three-seed held-out routing and deliberation records, matched caps, interference, fallback/abstention, candidate histories, stops, harms, dispositions, deterministic recomputation, and mutations.", "Reject selective seeds, retry inflation, oracle laundering, fallback erasure, extra-compute-harm erasure, record/summary mismatch, or core promotion.", "Bounded synthetic evidence for routing and deliberation comparisons.", "Does not establish production routing, fallback calibration, trained-specialist interference, language-model deliberation, verifier correctness, or transfer.", ["experiments/post_v2_routing_deliberation/results/2026-07-10-local.json", "schemas/post_v2_routing_deliberation_result.schema.json", "docs/post_v2_routing_deliberation.md", "scripts/validate_post_v2_routing_deliberation.py"]),
    ("validate_post_v2_update_causality_setup.py", "schema_or_structure", "Frozen 1,200-example corpus, independent splits, base/update roles, deletion cohort, probes, seeds, arms, validation-only selection, digest, and setup mutations.", "Reject identity/split drift, deletion or probe erasure, test selection, missing no-update baseline, or mutable campaign fields.", "Pre-outcome protocol integrity for the real update-causality campaign.", "Does not establish learning quality, unlearning, feedback optimization, open-endedness, recursion, or support movement.", ["experiments/post_v2_update_causality/input/corpus.json", "schemas/post_v2_update_causality_corpus.schema.json", "scripts/run_post_v2_update_causality.py", "scripts/validate_post_v2_update_causality_setup.py"]),
    ("validate_post_v2_update_causality.py", "proof_or_evidence_gate", "Three seeds, four arms, base/best/final checkpoint bytes and tensor states, output causality, parameter deltas, forgetting, deletion, nonmember utility, rollback, invalidation, dispositions, and mutations.", "Reject checkpoint/output mismatch, no-update laundering, test-selected best substitution, erased forgetting/deletion, false rollback, invalidation erasure, or core promotion.", "Bounded local real-mutation evidence at learning, deletion, campaign, and rollback transaction boundaries.", "Does not establish production learning/unlearning, storage erasure, feedback optimization, open-ended improvement, recursive improvement, or transfer.", ["experiments/post_v2_update_causality/results/2026-07-10-local.json", "experiments/post_v2_update_causality/checkpoints", "schemas/post_v2_update_causality_result.schema.json", "docs/post_v2_update_causality.md", "scripts/validate_post_v2_update_causality.py"]),
    ("validate_post_v2_empirical_reconciliation.py", "proof_or_evidence_gate", "Three accepted non-core no-change transitions, nine core no-change decisions, nine updated chapters/vectors/Appendix C/evidence-plan rows, residuals, conditional deferrals, roadmap status, and reconciliation mutations.", "Reject missing/positive dispositions, vector laundering, residual erasure, chapter-count drift, missing transition routing, or conditional-lane closure by fixture.", "Repository-wide reconciliation of all completed post-v2 empirical results without core support movement.", "Does not add a chapter, Lean theorem, external review, production transfer, or chapter-core promotion.", ["claim_decisions/post_v2_empirical_dispositions.json", "schemas/post_v2_empirical_dispositions.schema.json", "evidence_transitions/post_v2", "docs/post_v2_empirical_reconciliation.md", "docs/post_v2_residual_ledger.md", "docs/post_v2_evidence_roadmap.md", "evidence_quality/core_claim_vectors.json", "appendices/C_claim_evidence_matrix.qmd", "docs/per_chapter_evidence_plan.md", "scripts/validate_post_v2_empirical_reconciliation.py"]),
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing_scripts = {row["script"] for row in registry["units"]}
    for script, validation_class, input_contract, output_contract, claim_scope, prohibited, artifacts in SPECS:
        if script in existing_scripts:
            continue
        order = len(registry["units"]) + 1
        registry["units"].append({
            "id": f"{script.removesuffix('.py')}:{order}",
            "order": order,
            "script": script,
            "args": [],
            "execution_tier": "deep",
            "validation_class": validation_class,
            "input_contract": input_contract,
            "output_contract": output_contract,
            "claim_scope": claim_scope,
            "negative_controls": "validator_owned",
            "prohibited_inference": prohibited,
            "input_artifacts": artifacts,
            "output_assertions": ["frozen scope", "complete registered runs", "negative outcomes retained", "no chapter-core support movement"],
            "negative_control_cases": ["scope drift", "result erasure", "false promotion", "boundary laundering"],
            "contract_precision": "class_level",
            "semantic_review_state": "internal_contract_audit_not_independent",
        })
        for artifact in artifacts:
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
        existing_scripts.add(script)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered post-v2 validators: {len(registry['units'])} units, {len(registry['required_artifacts'])} artifacts")


if __name__ == "__main__":
    main()
