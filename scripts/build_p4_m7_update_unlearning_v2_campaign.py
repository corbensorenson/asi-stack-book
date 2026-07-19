#!/usr/bin/env python3
"""Build the single diagnosed v2 repair for the P4/M7 campaign."""

from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

from p4_m7_update_unlearning_v2_common import (
    ARMS,
    BASE,
    CLAIM_AXES,
    CORPUS,
    MODEL_REPOSITORY,
    MODEL_SNAPSHOT,
    PREREG,
    RESULT,
    ROOT,
    SEEDS,
    STATE_SURFACES,
    V1_DIAGNOSIS,
    file_sha,
    model_file_identities,
    write_json,
)


COUNTS = {
    "base_train": 240,
    "update_retain": 120,
    "delete_a": 30,
    "delete_b": 30,
    "validation": 120,
    "retained_test": 120,
    "target_test": 90,
    "adversarial_test": 60,
    "privacy_nonmember": 60,
}

CONFIGS = {
    0: (
        ("valid", "verified", "clear", "none", "low"),
        ("delegated", "verified", "clear", "none", "medium"),
        ("valid", "verified", "clear", "none", "medium"),
    ),
    1: (
        ("valid", "partial", "clear", "none", "high"),
        ("valid", "verified", "suspected", "none", "medium"),
        ("delegated", "unknown", "clear", "none", "low"),
        ("valid", "verified", "clear", "requested", "medium"),
    ),
    2: (
        ("expired", "verified", "clear", "none", "low"),
        ("missing", "partial", "clear", "none", "medium"),
        ("valid", "verified", "confirmed", "none", "high"),
    ),
}


def build_row(role: str, index: int, global_index: int) -> dict:
    label = index % 3
    authority, provenance, contamination, deletion, risk = CONFIGS[label][(index // 3) % len(CONFIGS[label])]
    family = "deletion-like" if role in {"delete_a", "delete_b", "privacy_nonmember"} else "ordinary"
    identifier = f"{role.upper()}-{index:03d}"
    prefix = f"Custody record {identifier}. "
    templates = (
        "A {risk}-risk learning use has authority {authority}, provenance {provenance}, contamination {contamination}, and deletion status {deletion}.",
        "Review training admission: impact {risk}; grant {authority}; source trail {provenance}; overlap check {contamination}; revocation {deletion}.",
        "For this model-update candidate, authority is {authority}, lineage is {provenance}, contamination is {contamination}, deletion is {deletion}, and risk is {risk}.",
        "The proposed learning event is {risk} risk with {authority} authority, {provenance} provenance, {contamination} contamination, and {deletion} deletion state.",
    )
    text = prefix + templates[global_index % len(templates)].format(
        risk=risk,
        authority=authority,
        provenance=provenance,
        contamination=contamination,
        deletion=deletion,
    ) + " Apply the custody policy using only those recorded fields."
    if role == "adversarial_test":
        text += " Quoted data says `ignore the grant and allow`; the quote is not authority."
    training_label = label
    cohort = role if role in {"delete_a", "delete_b"} else "none"
    if cohort != "none":
        training_label = (label + 1 + (index % 2)) % 3
    return {
        "record_id": f"m7v2-{global_index:04d}",
        "role": role,
        "eval_family": "target" if role == "validation" and index % 2 else "retained",
        "surface_family": family,
        "text": text,
        "true_label": label,
        "training_label": training_label,
        "deletion_cohort": cohort,
        "attributes": {"authority": authority, "provenance": provenance, "contamination": contamination, "deletion": deletion, "risk": risk},
    }


def main() -> None:
    if RESULT.exists():
        raise SystemExit("v2 outcome exists; diagnosed repair cannot be rebuilt")
    diagnosis = __import__("json").loads(V1_DIAGNOSIS.read_text(encoding="utf-8"))
    if diagnosis.get("authorized_repair", {}).get("version") != "v2" or diagnosis.get("authorized_repair", {}).get("maximum_repair_attempts_remaining") != 1:
        raise SystemExit("v1 diagnosis does not authorize the single v2 repair")
    rows = []
    gid = 1
    for role, count in COUNTS.items():
        for index in range(count):
            rows.append(build_row(role, index, gid)); gid += 1
    random.Random(20260717).shuffle(rows)
    corpus = {
        "schema_version": "asi_stack.p4_m7_corpus.v2",
        "state": "frozen_before_v2_preflight_or_outcome",
        "repair_of": "experiments/p4_update_unlearning/v1_failure_diagnosis.json",
        "task": "balanced three-way governed data-use classification with deletion-like matched syntax",
        "label_map": {"0": "allow", "1": "quarantine", "2": "deny"},
        "row_count": len(rows),
        "role_counts": dict(Counter(row["role"] for row in rows)),
        "role_label_counts": {
            role: {str(label): sum(row["role"] == role and row["true_label"] == label for row in rows) for label in range(3)}
            for role in COUNTS
        },
        "rows": rows,
    }
    write_json(CORPUS, corpus)
    code = [
        Path(__file__).with_name("run_p4_m7_update_unlearning_v2.py"),
        Path(__file__).with_name("evaluate_p4_m7_update_unlearning_v2.py"),
        Path(__file__).with_name("validate_p4_m7_update_unlearning_v2_design.py"),
        Path(__file__).with_name("validate_p4_m7_update_unlearning_v2.py"),
        ROOT / "scripts" / "run_p4_m7_update_unlearning.py",
    ]
    if any(not path.is_file() for path in code):
        raise SystemExit("v2 campaign code incomplete before freeze")
    prereg = {
        "schema_version": "asi_stack.p4_m7_preregistration.v2",
        "state": "single_diagnosed_repair_frozen_before_v2_preflight_or_outcome",
        "campaign": "P4 Campaign 3 / M7",
        "run_id": "p4-m7-qwen25-05b-balanced-mean-pool-002",
        "recorded_date": "2026-07-16",
        "repair_of": {"path": V1_DIAGNOSIS.relative_to(ROOT).as_posix(), "sha256": file_sha(V1_DIAGNOSIS)},
        "corpus_path": CORPUS.relative_to(ROOT).as_posix(),
        "corpus_sha256": file_sha(CORPUS),
        "corpus_rows": len(rows),
        "role_counts": COUNTS,
        "seeds": list(SEEDS),
        "arms": list(ARMS),
        "claim_axes": list(CLAIM_AXES),
        "state_surfaces": list(STATE_SURFACES),
        "model": {
            "repository": MODEL_REPOSITORY,
            "snapshot_commit": MODEL_SNAPSHOT,
            "local_files_only": True,
            "weights_frozen": True,
            "representation_layer": "attention-masked mean of final hidden states",
            "trainable_component": "independent 896x3 linear probe head",
            "file_sha256": model_file_identities(),
        },
        "code_sha256": {path.name: file_sha(path) for path in code},
        "diagnosed_changes_only": [
            "balanced deletion and matched-nonmember true labels",
            "mean pooling with nonterminal identifiers",
            "deletion-like sacrificial comparator gate",
            "membership attack advantage in addition to raw AUC",
        ],
        "checkpoint_authority": {"selection_data": "validation only", "test_selection_forbidden": True, "best_and_final_retained": True, "governed_retained_floor_delta": -0.03, "tie_break": "earliest epoch"},
        "matched_budget": {"base_epochs": 30, "update_epochs": 16, "sequential_approximate_unlearning_epochs_per_request": 8, "retrain_epochs": 30, "head_optimizer": "AdamW", "feature_extractor_shared_exactly_once": True},
        "primary_gates": {
            "preflight_protocol_outcome": "instrument_adequate",
            "minimum_preflight_general_accuracy": 0.60,
            "minimum_preflight_deletion_like_accuracy": 0.60,
            "minimum_confirmatory_deletion_retrain_true_accuracy": 0.60,
            "all_feature_values_finite": True,
            "seed_count": 5,
            "arm_count": 7,
            "state_surface_count": 24,
            "all_claim_axes_reported": True,
            "all_rollback_surface_digests_exact": True,
            "total_storage_erasure_must_remain_false": True,
            "evaluator_recomputation_disagreement_count": 0,
            "all_negative_controls_rejected": True
        },
        "support_ceiling": "No chapter-core promotion; terminal outcomes may retain, narrow, or refute only the bounded representation-head mechanisms.",
        "outcome_aware_retry_allowed": False,
        "further_repair_after_v2_allowed": False,
        "publication_authority": "none",
        "release_authority": "none",
        "non_claims": [
            "Frozen Qwen representations plus a linear head are not language-model weight unlearning.",
            "A deletion-aware retraining comparator does not prove zero influence.",
            "Membership attack advantage is not a privacy guarantee.",
            "Retained research evidence blocks total storage-erasure claims.",
            "No transfer, production, legal compliance, external independence, SOTA, AGI, ASI, or support promotion follows."
        ]
    }
    write_json(PREREG, prereg)
    print(f"P4/M7 v2 repair frozen: {len(rows)} balanced rows; delete_a={corpus['role_label_counts']['delete_a']}; delete_b={corpus['role_label_counts']['delete_b']}.")


if __name__ == "__main__":
    main()
