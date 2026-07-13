#!/usr/bin/env python3
"""Write the content-addressed pre-outcome QCSA evaluation setup freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "roadmap_records/qcsa_evaluation_setup_freeze.json"
FILES = [
    "experiments/qcsa_reference/test_plan.json",
    "experiments/qcsa_reference/budgets.json",
    "experiments/qcsa_reference/corpus/inputs.json",
    "experiments/qcsa_reference/corpus/labels.json",
    "experiments/qcsa_reference/corpus/manifest.json",
    "experiments/qcsa_reference/qcsa_ref/evaluation.py",
    "scripts/build_qcsa_evaluation_corpus.py",
    "scripts/validate_qcsa_evaluation_corpus.py",
    "scripts/run_qcsa_evaluation_predictions.py",
    "scripts/qcsa_evaluation_observer.py",
    "scripts/qcsa_independent_evaluator.py",
    "schemas/qcsa_evaluation_corpus_manifest.schema.json",
    "schemas/qcsa_evaluation_setup_freeze.schema.json"
]


def main() -> None:
    record = {
        "schema_version": "asi_stack.qcsa_evaluation_setup_freeze.v0",
        "freeze_id": "qcsa-evaluation-setup-2026-07-13",
        "state": "frozen_pending_commit_and_hosted_attestation",
        "parent_implementation_commit": "2aeb2cf92ebc2de54864c6f47439548986d5b18a",
        "outcome_access": "sealed_pending_setup_commit_attestation",
        "systems": [
            "qcsa",
            "direct_inference_or_retrieval_without_semantic_address",
            "flat_lexical_retrieval_matched_corpus_and_budget",
            "flat_embedding_proxy_retrieval_matched_corpus_and_budget",
            "one_fixed_hierarchy",
            "random_tree",
            "frequency_derived_tree",
            "direct_clarification_without_adaptive_question_policy",
            "qcsa_without_plural_facets",
            "qcsa_without_active_questions",
            "qcsa_without_identity_address_indirection",
            "qcsa_without_certificate_residual_authority_fields",
            "qcsa_without_migration_compatibility"
        ],
        "baselines": [
            "direct_inference_or_retrieval_without_semantic_address",
            "flat_lexical_retrieval_matched_corpus_and_budget",
            "flat_embedding_proxy_retrieval_matched_corpus_and_budget",
            "one_fixed_hierarchy",
            "random_tree",
            "frequency_derived_tree",
            "direct_clarification_without_adaptive_question_policy"
        ],
        "ablations": [
            "qcsa_without_plural_facets",
            "qcsa_without_active_questions",
            "qcsa_without_identity_address_indirection",
            "qcsa_without_certificate_residual_authority_fields",
            "qcsa_without_migration_compatibility"
        ],
        "seeds": [11, 29, 47],
        "held_out_case_count": 60,
        "bootstrap_resamples": 10000,
        "files": [{"path": path, "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()} for path in FILES],
        "runner_label_isolation": "runner reads public inputs, interaction tokens, plan, budget, systems, and execution authorization; it never reads evaluator labels",
        "observer_independence": "observer reads predictions and evaluator labels but imports no candidate, baseline, atlas, or round-trip implementation",
        "decision_policy": "frozen thresholds, per-family results, 10000-resample paired intervals, and Pareto frontiers; no blended score",
        "support_state_effect": "none",
        "non_claims": [
            "Freezing methods and labels is not an evaluation outcome.",
            "The workload is synthetic, bounded, public-safe, and not an open-world or natural-task benchmark.",
            "Internal evaluator separation is not external replication or a safety guarantee."
        ]
    }
    OUT.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote QCSA evaluation setup freeze with {len(FILES)} content-addressed files.")


if __name__ == "__main__":
    main()
