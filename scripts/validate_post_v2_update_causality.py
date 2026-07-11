#!/usr/bin/env python3
"""Validate checkpoint/output causality for the post-v2 update campaign."""
from __future__ import annotations

import copy
import hashlib

from build_canonical_public_status import ROOT, load_json, validate_against_schema
from run_post_v2_update_causality import CORPUS, PolicyNet, accuracy, canonical_sha, evaluate_checkpoint, load_state, predictions, state_sha


RESULT = ROOT / "experiments/post_v2_update_causality/results/2026-07-10-local.json"
SCHEMA = ROOT / "schemas/post_v2_update_causality_result.schema.json"
DOC = ROOT / "docs/post_v2_update_causality.md"
ARMS = {"no_update", "bounded_finetune", "regularized_challenger", "deletion_aware_retrain"}


def semantic_errors(result: dict, replay: bool = True) -> list[str]:
    errors: list[str] = []
    corpus = load_json(CORPUS)
    if result.get("corpus_sha256") != corpus.get("corpus_sha256"):
        errors.append("result does not bind the frozen corpus")
    payload = copy.deepcopy(result); claimed = payload.pop("bundle_sha256", None)
    if claimed != canonical_sha(payload):
        errors.append("result bundle digest mismatch")
    seeds = result.get("seed_records", [])
    if [row.get("seed") for row in seeds] != [17, 29, 43]:
        errors.append("seed records must preserve 17, 29, and 43")
    examples = corpus["examples"]
    rows = {
        "base_train": [row for row in examples if row["train_role"] == "base_train"],
        "update": [row for row in examples if row["train_role"] == "update"],
        "deletion": [row for row in examples if row["deletion_cohort"]],
        "validation": [row for row in examples if row["split"] == "validation"],
        "test": [row for row in examples if row["split"] == "test"],
        "probes": [row for row in examples if row["fixed_probe"]],
    }
    total_best_final_disagreement = 0
    for seed_row in seeds:
        base = seed_row.get("base_checkpoint", {})
        base_path = ROOT / str(base.get("path", ""))
        if not base_path.is_file() or hashlib.sha256(base_path.read_bytes()).hexdigest() != base.get("file_sha256"):
            errors.append(f"seed {seed_row.get('seed')}: base checkpoint byte digest mismatch")
            continue
        base_state = load_state(base_path)
        if state_sha(base_state) != base.get("state_sha256"):
            errors.append(f"seed {seed_row.get('seed')}: base tensor-state digest mismatch")
        base_model = PolicyNet(); base_model.load_state_dict(base_state)
        base_predictions = {name: predictions(base_model, values) for name, values in rows.items()}
        if round(accuracy(base_predictions["test"], rows["test"]), 8) != base.get("test_accuracy"):
            errors.append(f"seed {seed_row.get('seed')}: base output/checkpoint mismatch")
        arm_rows = seed_row.get("arms", [])
        if {row.get("arm") for row in arm_rows} != ARMS:
            errors.append(f"seed {seed_row.get('seed')}: arm set is missing or extra")
        for arm in arm_rows:
            history = arm.get("history", [])
            expected_best = 0 if not history else max(history, key=lambda row: (row["validation_accuracy"], -row["epoch"]))["epoch"]
            if arm.get("best_epoch_selected_by_validation") != expected_best:
                errors.append(f"seed {seed_row.get('seed')} {arm.get('arm')}: best checkpoint not selected by validation")
            for checkpoint_name in ("best_checkpoint", "final_checkpoint"):
                checkpoint = arm.get(checkpoint_name, {})
                path = ROOT / str(checkpoint.get("path", ""))
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != checkpoint.get("file_sha256"):
                    errors.append(f"seed {seed_row.get('seed')} {arm.get('arm')} {checkpoint_name}: byte digest mismatch")
                    continue
                if replay:
                    fresh = evaluate_checkpoint(path, rows, base_state, base_predictions)
                    if fresh != checkpoint.get("metrics"):
                        errors.append(f"seed {seed_row.get('seed')} {arm.get('arm')} {checkpoint_name}: checkpoint/output metrics mismatch")
            final_delta = arm.get("final_checkpoint", {}).get("metrics", {}).get("parameter_delta_l2")
            if arm.get("arm") == "no_update":
                if final_delta != 0.0 or arm.get("actual_parameter_mutation") is not False:
                    errors.append(f"seed {seed_row.get('seed')}: no-update arm was represented as mutation")
            elif not isinstance(final_delta, (int, float)) or final_delta <= 0 or arm.get("actual_parameter_mutation") is not True:
                errors.append(f"seed {seed_row.get('seed')} {arm.get('arm')}: real parameter mutation missing")
            metrics = arm.get("final_checkpoint", {}).get("metrics", {})
            for field in ("retained_base_accuracy", "deletion_cohort_changes", "deletion_true_accuracy", "deletion_training_label_accuracy", "nonmember_test_utility"):
                if field not in metrics:
                    errors.append(f"seed {seed_row.get('seed')} {arm.get('arm')}: required negative/causal metric missing: {field}")
            if arm.get("arm") != "no_update":
                total_best_final_disagreement += arm.get("best_final_test_disagreement", 0)
        rollback = seed_row.get("rollback", {})
        if rollback.get("state_sha256") != base.get("state_sha256") or rollback.get("exact") is not True or rollback.get("descendant_arms_invalidated") != 3:
            errors.append(f"seed {seed_row.get('seed')}: rollback or descendant invalidation mismatch")
    if total_best_final_disagreement != 62:
        errors.append(f"best/final disagreement total expected 62, got {total_best_final_disagreement}")
    if any(row.get("disposition") != "no_change" for row in result.get("claim_dispositions", [])) or result.get("support_state_effect") != "none":
        errors.append("campaign cannot silently change a chapter-core support state")
    return errors


def main() -> None:
    missing = [path.relative_to(ROOT).as_posix() for path in (RESULT, SCHEMA, DOC, CORPUS) if not path.is_file()]
    if missing:
        raise SystemExit("missing update-causality result artifacts: " + ", ".join(missing))
    result = load_json(RESULT)
    errors = validate_against_schema(result, load_json(SCHEMA), RESULT.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(result))
    doc = DOC.read_text(encoding="utf-8")
    for phrase in ("zero parameter delta", "| Bounded fine-tune | 0.7792 | 41 | 9", "disagreed on 30 test", "mean true-label accuracy\n0.8222", "invalidated nine", "All four affected core claims receive `no_change`"):
        if phrase not in doc:
            errors.append(f"readable update report missing result boundary: {phrase}")
    mutations = []
    digest = copy.deepcopy(result); digest["bundle_sha256"] = "0" * 64; mutations.append(digest)
    no_update = copy.deepcopy(result); no_update["seed_records"][0]["arms"][0]["actual_parameter_mutation"] = True; mutations.append(no_update)
    best = copy.deepcopy(result); best["seed_records"][0]["arms"][1]["best_epoch_selected_by_validation"] = 12; mutations.append(best)
    forgetting = copy.deepcopy(result); forgetting["seed_records"][0]["arms"][1]["final_checkpoint"]["metrics"].pop("retained_base_accuracy"); mutations.append(forgetting)
    deletion = copy.deepcopy(result); deletion["seed_records"][0]["arms"][3]["final_checkpoint"]["metrics"].pop("deletion_cohort_changes"); mutations.append(deletion)
    rollback = copy.deepcopy(result); rollback["seed_records"][0]["rollback"]["exact"] = False; mutations.append(rollback)
    descendant = copy.deepcopy(result); descendant["seed_records"][0]["rollback"]["descendant_arms_invalidated"] = 0; mutations.append(descendant)
    promote = copy.deepcopy(result); promote["claim_dispositions"][0]["disposition"] = "promote"; mutations.append(promote)
    for mutation in mutations:
        if not semantic_errors(mutation, replay=False):
            errors.append("an update-causality outcome mutation was accepted")
    if errors:
        raise SystemExit("Update-causality validation failed:\n - " + "\n - ".join(errors))
    print("Update-causality validation passed: 3 seeds x 4 arms, real parameter mutations, 24 best/final checkpoint replays plus 3 bases, validation-only selection, 62 best/final test disagreements, deletion/forgetting/nonmember metrics, 3 exact rollbacks, 9 invalidated descendant arms, 4 no-change dispositions, and 8 rejecting mutations.")


if __name__ == "__main__":
    main()
