#!/usr/bin/env python3
"""Validate prospective P4/M7 freeze and optional sacrificial qualification."""

from __future__ import annotations

import copy
from collections import Counter

from p4_m7_update_unlearning_common import (
    ARMS,
    CLAIM_AXES,
    CORPUS,
    MODEL_REPOSITORY,
    MODEL_SNAPSHOT,
    PREFLIGHT,
    PREREG,
    SEEDS,
    STATE_SURFACES,
    file_sha,
    load_json,
    model_file_identities,
)


EXPECTED_COUNTS = {
    "base_train": 240,
    "update_retain": 120,
    "delete_a": 30,
    "delete_b": 30,
    "validation": 120,
    "retained_test": 120,
    "target_test": 80,
    "adversarial_test": 60,
    "privacy_nonmember": 60,
}


def errors(prereg: dict, corpus: dict) -> list[str]:
    out: list[str] = []
    rows = corpus.get("rows", [])
    if prereg.get("state") != "prospectively_frozen_before_preflight_feature_extraction_or_any_outcome":
        out.append("prospective freeze state drift")
    if prereg.get("corpus_sha256") != file_sha(CORPUS) or prereg.get("corpus_rows") != 860:
        out.append("frozen corpus identity drift")
    if corpus.get("state") != "frozen_before_any_model_feature_extraction_or_training" or corpus.get("row_count") != 860:
        out.append("corpus freeze or denominator drift")
    if Counter(row.get("role") for row in rows) != Counter(EXPECTED_COUNTS):
        out.append("role denominator drift")
    if len({row.get("record_id") for row in rows}) != 860:
        out.append("record identity collision")
    if prereg.get("seeds") != list(SEEDS) or prereg.get("arms") != list(ARMS):
        out.append("seed or arm freeze drift")
    if prereg.get("claim_axes") != list(CLAIM_AXES) or prereg.get("state_surfaces") != list(STATE_SURFACES):
        out.append("claim-axis or state-surface freeze drift")
    if len(CLAIM_AXES) != 8 or len(STATE_SURFACES) != 24:
        out.append("canonical axis/surface count drift")
    model = prereg.get("model", {})
    if model.get("repository") != MODEL_REPOSITORY or model.get("snapshot_commit") != MODEL_SNAPSHOT or model.get("weights_frozen") is not True:
        out.append("model identity or frozen-weight boundary drift")
    if model.get("file_sha256") != model_file_identities():
        out.append("local model snapshot bytes drift")
    if any(row.get("true_label") not in {0, 1, 2} or row.get("training_label") not in {0, 1, 2} for row in rows):
        out.append("label domain drift")
    deletion = [row for row in rows if row.get("deletion_cohort") in {"delete_a", "delete_b"}]
    if len(deletion) != 60 or any(row["true_label"] == row["training_label"] for row in deletion):
        out.append("deletion cohort or poisoned-label contrast drift")
    if any(row["true_label"] != row["training_label"] for row in rows if row.get("deletion_cohort") == "none"):
        out.append("nondeletion label poisoning drift")
    if prereg.get("outcome_aware_retry_allowed") is not False or prereg.get("support_ceiling", "").startswith("No chapter-core promotion") is not True:
        out.append("retry or support ceiling drift")
    gates = prereg.get("primary_gates", {})
    if gates.get("seed_count") != 5 or gates.get("arm_count") != 7 or gates.get("state_surface_count") != 24:
        out.append("primary denominator gate drift")
    if gates.get("total_storage_erasure_must_remain_false") is not True or gates.get("evaluator_recomputation_disagreement_count") != 0:
        out.append("erasure or evaluator gate drift")
    return out


def main() -> None:
    prereg = load_json(PREREG); corpus = load_json(CORPUS)
    failures = errors(prereg, corpus)
    mutations = []
    for label, mutation in (
        ("drop arm", lambda p, c: p["arms"].pop()),
        ("drop seed", lambda p, c: p["seeds"].pop()),
        ("merge privacy and storage", lambda p, c: p["claim_axes"].remove("membership_privacy_change")),
        ("truncate state", lambda p, c: p["state_surfaces"].pop()),
        ("unfreeze weights", lambda p, c: p["model"].__setitem__("weights_frozen", False)),
        ("poison retained label", lambda p, c: c["rows"][next(i for i, row in enumerate(c["rows"]) if row["role"] == "base_train")].__setitem__("training_label", 9)),
        ("permit retry", lambda p, c: p.__setitem__("outcome_aware_retry_allowed", True)),
        ("launder erasure", lambda p, c: p["primary_gates"].__setitem__("total_storage_erasure_must_remain_false", False)),
    ):
        candidate_p = copy.deepcopy(prereg); candidate_c = copy.deepcopy(corpus); mutation(candidate_p, candidate_c)
        if not errors(candidate_p, candidate_c):
            failures.append(f"design mutation accepted: {label}")
        mutations.append(label)
    preflight_state = "not_run"
    if PREFLIGHT.exists():
        preflight = load_json(PREFLIGHT)
        preflight_state = preflight.get("protocol_outcome", "missing")
        if preflight_state != "instrument_adequate" or preflight.get("heldout_opened") is not True:
            failures.append("sacrificial instrument did not qualify")
        if preflight.get("validation_accuracy", 0.0) < prereg["primary_gates"]["minimum_preflight_validation_accuracy"]:
            failures.append("preflight validation floor failed")
        if not all(preflight.get("negative_controls", {}).values()) or len(preflight.get("negative_controls", {})) != 5:
            failures.append("preflight negative controls drift")
    if failures:
        raise SystemExit("P4/M7 design validation failed:\n - " + "\n - ".join(failures))
    print(f"P4/M7 design passed: 860 rows, 5 seeds, 7 arms, 8 separate claim axes, 24 full-state surfaces, 8 design mutations rejected, preflight={preflight_state}.")


if __name__ == "__main__":
    main()
