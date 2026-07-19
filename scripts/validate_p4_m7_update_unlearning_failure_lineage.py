#!/usr/bin/env python3
"""Validate the two expected M7 instrument failures without treating them as errors."""

from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1_PREREG = ROOT / "experiments/p4_update_unlearning/preregistration.json"
V1_RESULT = ROOT / "experiments/p4_update_unlearning/results/confirmatory_result.json"
V1_DIAGNOSIS = ROOT / "experiments/p4_update_unlearning/v1_failure_diagnosis.json"
V2_PREREG = ROOT / "experiments/p4_update_unlearning_v2/preregistration.json"
V2_PREFLIGHT = ROOT / "experiments/p4_update_unlearning_v2/results/preflight_result.json"
V2_DIAGNOSIS = ROOT / "experiments/p4_update_unlearning_v2/preflight_failure_diagnosis.json"
V2_CONFIRMATORY = ROOT / "experiments/p4_update_unlearning_v2/results/confirmatory_result.json"
V3_PREREG = ROOT / "experiments/p4_update_unlearning_v3/preregistration.json"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_values(values: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    v1_prereg = values["v1_prereg"]
    v1_result = values["v1_result"]
    v1 = values["v1_diagnosis"]
    v2_prereg = values["v2_prereg"]
    v2_preflight = values["v2_preflight"]
    v2 = values["v2_diagnosis"]
    v3 = values["v3_prereg"]

    if v1.get("superseded_protocol_outcome") != "instrument_inadequate_unlearning_target_not_learnable":
        errors.append("v1 target-adequacy failure was erased")
    if v1.get("claim_outcome") != "not_applicable_instrument_failure":
        errors.append("v1 was laundered into a claim outcome")
    if v1.get("result_sha256") != digest(V1_RESULT):
        errors.append("v1 diagnosis no longer binds the preserved result bytes")
    if v1.get("preregistration_sha256") != digest(V1_PREREG):
        errors.append("v1 diagnosis no longer binds the preserved preregistration")
    class_counts = v1.get("failure_evidence", {}).get("deletion_cohort_class_counts", {})
    if class_counts != {"allow": 60, "quarantine": 0, "deny": 0}:
        errors.append("v1 single-class deletion-cohort failure changed")
    arm_accuracy = v1.get("failure_evidence", {}).get("mean_deletion_true_accuracy_by_arm", {})
    if len(arm_accuracy) != 7 or any(value != 0.0 for value in arm_accuracy.values()):
        errors.append("v1 seven-arm zero deletion-accuracy failure changed")
    if v1_result.get("run_id") != v1_prereg.get("run_id"):
        errors.append("v1 result/preregistration run identity mismatch")
    if v1.get("support_state_effect") != "none":
        errors.append("v1 instrument failure changed support state")

    if v2.get("protocol_outcome") != "instrument_inadequate_preflight":
        errors.append("v2 failed-preflight outcome was erased")
    if v2.get("claim_outcome") != "not_applicable_instrument_only":
        errors.append("v2 was laundered into a claim attempt")
    if v2.get("heldout_opened") is not False or V2_CONFIRMATORY.exists():
        errors.append("v2 held-out denominator must remain unopened")
    if v2.get("preregistration_sha256") != digest(V2_PREREG):
        errors.append("v2 diagnosis no longer binds the preserved preregistration")
    if v2.get("preflight_result_sha256") != digest(V2_PREFLIGHT):
        errors.append("v2 diagnosis no longer binds the preserved preflight")
    observed = v2.get("observed", {})
    expected_observed = {
        "general_validation_accuracy": 0.43333333,
        "deletion_like_validation_accuracy": 0.33333333,
        "frozen_floor_each": 0.6,
    }
    if observed != expected_observed:
        errors.append("v2 prospectively failed accuracy record changed")
    if v2_preflight.get("protocol_outcome") != "instrument_inadequate":
        errors.append("v2 raw preflight is no longer instrument-inadequate")
    repair_of = v2_prereg.get("repair_of", {})
    if repair_of != {
        "path": str(V1_DIAGNOSIS.relative_to(ROOT)),
        "sha256": digest(V1_DIAGNOSIS),
    }:
        errors.append("v2 no longer binds the exact v1 diagnosis as its repair parent")
    if v2.get("support_state_effect") != "none":
        errors.append("v2 instrument failure changed support state")

    lineage = {
        row.get("path"): row.get("sha256")
        for row in v3.get("failure_lineage", [])
        if isinstance(row, dict)
    }
    expected_lineage = {
        str(V1_DIAGNOSIS.relative_to(ROOT)): digest(V1_DIAGNOSIS),
        str(V2_DIAGNOSIS.relative_to(ROOT)): digest(V2_DIAGNOSIS),
    }
    if lineage != expected_lineage:
        errors.append("v3 preregistration no longer closes over both exact failure diagnoses")
    if v3.get("further_instrument_repair_allowed") is not False:
        errors.append("v3 terminal-instrument boundary was reopened")
    if v3.get("outcome_aware_retry_allowed") is not False:
        errors.append("v3 outcome-aware retry was enabled")
    return errors


def main() -> None:
    paths = [V1_PREREG, V1_RESULT, V1_DIAGNOSIS, V2_PREREG, V2_PREFLIGHT, V2_DIAGNOSIS, V3_PREREG]
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.exists()]
    if missing:
        print("P4/M7 failure-lineage validation failed:\n - missing " + "\n - missing ".join(missing))
        sys.exit(1)
    values = {
        "v1_prereg": load(V1_PREREG),
        "v1_result": load(V1_RESULT),
        "v1_diagnosis": load(V1_DIAGNOSIS),
        "v2_prereg": load(V2_PREREG),
        "v2_preflight": load(V2_PREFLIGHT),
        "v2_diagnosis": load(V2_DIAGNOSIS),
        "v3_prereg": load(V3_PREREG),
    }
    errors = validate_values(values)
    mutations = [
        ("v1 target laundering", lambda x: x["v1_diagnosis"].update(superseded_protocol_outcome="instrument_adequate")),
        ("v1 support promotion", lambda x: x["v1_diagnosis"].update(support_state_effect="promotion")),
        ("v2 held-out laundering", lambda x: x["v2_diagnosis"].update(heldout_opened=True)),
        ("v2 accuracy rewriting", lambda x: x["v2_diagnosis"]["observed"].update(general_validation_accuracy=0.8)),
        ("failure-lineage erasure", lambda x: x["v3_prereg"].update(failure_lineage=[])),
        ("outcome-aware retry", lambda x: x["v3_prereg"].update(outcome_aware_retry_allowed=True)),
    ]
    rejected = 0
    for name, mutate in mutations:
        candidate = deepcopy(values)
        mutate(candidate)
        if validate_values(candidate):
            rejected += 1
        else:
            errors.append(f"negative control accepted: {name}")
    if errors:
        print("P4/M7 failure-lineage validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(f"P4/M7 failure lineage passed: two expected failures preserved, {rejected}/6 mutations rejected.")


if __name__ == "__main__":
    main()
