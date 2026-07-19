#!/usr/bin/env python3
"""Freeze the terminal, substantively changed P4/M7 v3 instrument."""

from __future__ import annotations

from pathlib import Path

from p4_m7_update_unlearning_v3_common import ARMS, CLAIM_AXES, CORPUS, FUSED_SIZE, MODEL_REPOSITORY, MODEL_SNAPSHOT, PREREG, RESULT, ROOT, SEEDS, STATE_SURFACES, STRUCTURED_FIELDS, STRUCTURED_SIZE, V1_DIAGNOSIS, V2_DIAGNOSIS, file_sha, load_json, model_file_identities, write_json


def main() -> None:
    if RESULT.exists(): raise SystemExit("v3 outcome exists; terminal instrument cannot be rebuilt")
    v2 = load_json(V2_DIAGNOSIS)
    if v2.get("terminal_instrument_change", {}).get("version") != "v3" or v2.get("terminal_instrument_change", {}).get("further_preflight_repair_allowed") is not False: raise SystemExit("v2 diagnosis does not bind terminal v3")
    code = [Path(__file__).with_name(name) for name in ("run_p4_m7_update_unlearning_v3.py", "evaluate_p4_m7_update_unlearning_v3.py", "validate_p4_m7_update_unlearning_v3_design.py", "validate_p4_m7_update_unlearning_v3.py")]
    if any(not path.is_file() for path in code): raise SystemExit("v3 code incomplete before freeze")
    prereg = {
        "schema_version": "asi_stack.p4_m7_preregistration.v3",
        "state": "terminal_instrument_frozen_before_preflight_or_heldout_outcome",
        "campaign": "P4 Campaign 3 / M7",
        "run_id": "p4-m7-qwen25-05b-structured-fusion-003",
        "recorded_date": "2026-07-16",
        "failure_lineage": [{"path": V1_DIAGNOSIS.relative_to(ROOT).as_posix(), "sha256": file_sha(V1_DIAGNOSIS)}, {"path": V2_DIAGNOSIS.relative_to(ROOT).as_posix(), "sha256": file_sha(V2_DIAGNOSIS)}],
        "corpus_path": CORPUS.relative_to(ROOT).as_posix(),
        "corpus_sha256": file_sha(CORPUS),
        "corpus_rows": 870,
        "seeds": list(SEEDS),
        "arms": list(ARMS),
        "claim_axes": list(CLAIM_AXES),
        "state_surfaces": list(STATE_SURFACES),
        "model": {"repository": MODEL_REPOSITORY, "snapshot_commit": MODEL_SNAPSHOT, "local_files_only": True, "weights_frozen": True, "transformer_representation": "per-row L2-normalized attention-masked final-hidden-state mean", "structured_fields": {key: list(values) for key, values in STRUCTURED_FIELDS.items()}, "structured_size": STRUCTURED_SIZE, "structured_scale": 2.0, "fused_size": FUSED_SIZE, "trainable_component": "912x32x3 nonlinear fusion head", "file_sha256": model_file_identities()},
        "code_sha256": {path.name: file_sha(path) for path in code},
        "preflight_ablation": ["transformer_only_linear", "structured_only_nonlinear", "fused_nonlinear"],
        "checkpoint_authority": {"selection_data": "validation only", "test_selection_forbidden": True, "best_and_final_retained": True, "governed_retained_floor_delta": -0.03, "tie_break": "earliest epoch"},
        "matched_budget": {"base_epochs": 60, "update_epochs": 24, "sequential_approximate_unlearning_epochs_per_request": 12, "retrain_epochs": 60, "head_optimizer": "AdamW", "shared_frozen_transformer_features": True},
        "primary_gates": {"preflight_protocol_outcome": "instrument_adequate", "minimum_preflight_fused_general_accuracy": 0.8, "minimum_preflight_fused_deletion_like_accuracy": 0.8, "minimum_confirmatory_deletion_retrain_true_accuracy": 0.8, "all_feature_values_finite": True, "seed_count": 5, "arm_count": 7, "state_surface_count": 24, "all_claim_axes_reported": True, "all_rollback_surface_digests_exact": True, "total_storage_erasure_must_remain_false": True, "evaluator_recomputation_disagreement_count": 0, "all_negative_controls_rejected": True},
        "support_ceiling": "No chapter-core promotion. The terminal attempt may narrow or refute bounded fusion-head update/unlearning mechanisms only.",
        "outcome_aware_retry_allowed": False,
        "further_instrument_repair_allowed": False,
        "publication_authority": "none",
        "release_authority": "none",
        "non_claims": ["The deterministic structured vector exposes fields already present in each custody record; it is not hidden-label access.", "Frozen Qwen features plus a fusion head are not language-model weight unlearning.", "Deletion-aware retraining does not prove zero influence.", "Membership attack advantage is not a privacy guarantee.", "Retained research evidence blocks total storage erasure.", "No transfer, production, legal compliance, external independence, SOTA, AGI, ASI, or support promotion follows."]
    }
    write_json(PREREG, prereg); print(f"P4/M7 terminal v3 frozen: corpus={prereg['corpus_sha256'][:12]}, fused_size={FUSED_SIZE}, 5 seeds x 7 arms.")


if __name__ == "__main__": main()
