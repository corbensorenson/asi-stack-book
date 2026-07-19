#!/usr/bin/env python3
"""Validate terminal P4/M7 v3 evidence and negative controls."""

from __future__ import annotations

import copy

import jsonschema

from p4_m7_update_unlearning_v3_common import ARMS, CLAIM_AXES, CORPUS, FEATURES, PREREG, RAW_RUN, RESULT, ROOT, SEEDS, V1_DIAGNOSIS, V2_DIAGNOSIS, file_sha, load_json


SCHEMA = ROOT / "schemas/p4_m7_update_unlearning_v3_result.schema.json"


def errors(result: dict) -> list[str]:
    out = []; prereg = load_json(PREREG)
    if load_json(V1_DIAGNOSIS).get("superseded_protocol_outcome") != "instrument_inadequate_unlearning_target_not_learnable" or load_json(V2_DIAGNOSIS).get("protocol_outcome") != "instrument_inadequate_preflight": out.append("failure lineage drift")
    if result.get("corpus_sha256") != file_sha(CORPUS) or result.get("preregistration_sha256") != file_sha(PREREG) or result.get("raw_run_sha256") != file_sha(RAW_RUN) or result.get("feature_artifact_sha256") != file_sha(FEATURES): out.append("v3 artifact lineage drift")
    if result.get("failure_lineage_preserved") is not True or result.get("candidate_and_checkpoint_bytes_closed_before_axis_evaluation") is not True: out.append("v3 closure lineage drift")
    if result.get("seeds") != list(SEEDS) or result.get("arms") != list(ARMS) or result.get("claim_axes") != list(CLAIM_AXES) or set(result.get("axis_dispositions", {})) != set(CLAIM_AXES): out.append("v3 denominator/axis drift")
    if any(row["full_state"].get("surface_count") != 24 or row["full_state"].get("rollback_exact") is not True or row["full_state"].get("rollback_sha256") != row["full_state"].get("before_sha256") for seed in result.get("seed_results", []) for row in seed.get("arms", [])): out.append("v3 rollback drift")
    gates = result.get("gate_checks_before_validator_mutations", {})
    if len(gates) != 10 or not all(gates.values()): out.append("v3 terminal gate failed")
    if result.get("arm_summaries", {}).get("deletion_aware_retrain", {}).get("deletion_true_accuracy", 0) < 0.8: out.append("v3 target inadequacy")
    if result.get("storage_receipt", {}).get("total_storage_erasure") is not False or not result.get("storage_receipt", {}).get("retained_research_evidence"): out.append("v3 storage residual drift")
    if result.get("lineage_receipt", {}).get("external_descendant", {}).get("erasure_verified") is not False: out.append("v3 external erasure laundering")
    if result.get("protocol_outcome") != "instrument_adequate_bounded_local_axis_separation" or result.get("claim_outcome") != "claim_narrowed_after_full_attempt": out.append("v3 terminal outcome drift")
    if result.get("support_state_effect") != "none" or result.get("chapter_core_promotion_count") != 0: out.append("v3 unsupported promotion")
    for phrase in ("not language-model unlearning", "zero influence", "privacy", "complete erasure", "legal compliance", "transfer", "SOTA"):
        if phrase not in result.get("claim_ceiling", ""): out.append(f"v3 claim ceiling lost: {phrase}")
    if prereg.get("further_instrument_repair_allowed") is not False: out.append("v3 retry ceiling drift")
    return out


def main() -> None:
    result = load_json(RESULT); jsonschema.validate(result, load_json(SCHEMA)); failures = errors(result)
    for axis in CLAIM_AXES:
        candidate = copy.deepcopy(result); candidate["axis_dispositions"].pop(axis)
        if not errors(candidate): failures.append(f"v3 axis mutation accepted: {axis}")
    for label, mutation in (
        ("erase lineage", lambda r: r.__setitem__("failure_lineage_preserved", False)),
        ("truncate state", lambda r: r["seed_results"][0]["arms"][0]["full_state"].__setitem__("surface_count", 23)),
        ("false rollback", lambda r: r["seed_results"][0]["arms"][1]["full_state"].__setitem__("rollback_exact", False)),
        ("claim total erasure", lambda r: r["storage_receipt"].__setitem__("total_storage_erasure", True)),
        ("invent external erasure", lambda r: r["lineage_receipt"]["external_descendant"].__setitem__("erasure_verified", True)),
        ("promote core", lambda r: r.__setitem__("chapter_core_promotion_count", 1)),
        ("launder LM", lambda r: r.__setitem__("claim_ceiling", "language-model unlearning proved")),
    ):
        candidate = copy.deepcopy(result); mutation(candidate)
        if not errors(candidate): failures.append(f"v3 mutation accepted: {label}")
    if failures: raise SystemExit("P4/M7 v3 validation failed:\n - " + "\n - ".join(failures))
    summary = result["arm_summaries"]; print(f"P4/M7 v3 validation passed: deletion retrain {summary['deletion_aware_retrain']['deletion_true_accuracy']:.6f}, approximate distance {summary['approximate_unlearning']['distance_reduction_fraction_vs_standard_update']:+.6f}, 15 mutations rejected, no promotion.")


if __name__ == "__main__": main()
