#!/usr/bin/env python3
"""Validate the terminal P4/M7 v2 repair without erasing v1 failure."""

from __future__ import annotations

import copy

import jsonschema

from p4_m7_update_unlearning_v2_common import ARMS, CLAIM_AXES, CORPUS, FEATURES, PREREG, RAW_RUN, RESULT, ROOT, SEEDS, V1_DIAGNOSIS, file_sha, load_json


SCHEMA = ROOT / "schemas" / "p4_m7_update_unlearning_v2_result.schema.json"


def errors(result: dict) -> list[str]:
    out = []; prereg = load_json(PREREG); diagnosis = load_json(V1_DIAGNOSIS)
    if diagnosis.get("superseded_protocol_outcome") != "instrument_inadequate_unlearning_target_not_learnable": out.append("v1 failure lineage drift")
    if result.get("corpus_sha256") != file_sha(CORPUS) or result.get("preregistration_sha256") != file_sha(PREREG) or result.get("raw_run_sha256") != file_sha(RAW_RUN) or result.get("feature_artifact_sha256") != file_sha(FEATURES): out.append("v2 artifact lineage drift")
    if result.get("candidate_and_checkpoint_bytes_closed_before_axis_evaluation") is not True: out.append("v2 candidate closure drift")
    if result.get("seeds") != list(SEEDS) or result.get("arms") != list(ARMS): out.append("v2 denominator drift")
    if result.get("claim_axes") != list(CLAIM_AXES) or set(result.get("axis_dispositions", {})) != set(CLAIM_AXES): out.append("v2 axis separation drift")
    if any(row["full_state"].get("surface_count") != 24 or row["full_state"].get("rollback_exact") is not True or row["full_state"].get("rollback_sha256") != row["full_state"].get("before_sha256") for seed in result.get("seed_results", []) for row in seed.get("arms", [])): out.append("v2 full-state rollback drift")
    gates = result.get("gate_checks_before_validator_mutations", {})
    if len(gates) != 10 or not all(gates.values()): out.append("v2 terminal gate failed")
    if result.get("arm_summaries", {}).get("deletion_aware_retrain", {}).get("deletion_true_accuracy", 0) < 0.60: out.append("v2 deletion target inadequate")
    if result.get("storage_receipt", {}).get("total_storage_erasure") is not False or not result.get("storage_receipt", {}).get("retained_research_evidence"): out.append("v2 storage residual drift")
    if result.get("lineage_receipt", {}).get("external_descendant", {}).get("erasure_verified") is not False: out.append("v2 external erasure laundered")
    if result.get("protocol_outcome") != "instrument_adequate_bounded_local_axis_separation" or result.get("claim_outcome") != "claim_narrowed_after_full_attempt": out.append("v2 terminal outcome drift")
    if result.get("support_state_effect") != "none" or result.get("chapter_core_promotion_count") != 0: out.append("v2 unsupported promotion")
    for phrase in ("not language-model unlearning", "zero influence", "privacy", "complete erasure", "legal compliance", "transfer", "SOTA"):
        if phrase not in result.get("claim_ceiling", ""): out.append(f"v2 claim ceiling lost: {phrase}")
    if prereg.get("further_repair_after_v2_allowed") is not False: out.append("v2 retry ceiling drift")
    return out


def main() -> None:
    result = load_json(RESULT); jsonschema.validate(result, load_json(SCHEMA)); failures = errors(result)
    for axis in CLAIM_AXES:
        candidate = copy.deepcopy(result); candidate["axis_dispositions"].pop(axis)
        if not errors(candidate): failures.append(f"v2 axis mutation accepted: {axis}")
    for label, mutation in (
        ("erase v1 binding", lambda r: r.__setitem__("corpus_sha256", "0" * 64)),
        ("truncate state", lambda r: r["seed_results"][0]["arms"][0]["full_state"].__setitem__("surface_count", 23)),
        ("false rollback", lambda r: r["seed_results"][0]["arms"][1]["full_state"].__setitem__("rollback_exact", False)),
        ("claim total erasure", lambda r: r["storage_receipt"].__setitem__("total_storage_erasure", True)),
        ("invent external erasure", lambda r: r["lineage_receipt"]["external_descendant"].__setitem__("erasure_verified", True)),
        ("promote core", lambda r: r.__setitem__("chapter_core_promotion_count", 1)),
        ("launder LM unlearning", lambda r: r.__setitem__("claim_ceiling", "language-model unlearning proved")),
    ):
        candidate = copy.deepcopy(result); mutation(candidate)
        if not errors(candidate): failures.append(f"v2 terminal mutation accepted: {label}")
    if failures: raise SystemExit("P4/M7 v2 validation failed:\n - " + "\n - ".join(failures))
    summaries = result["arm_summaries"]; print(f"P4/M7 v2 validation passed: retrain deletion accuracy {summaries['deletion_aware_retrain']['deletion_true_accuracy']:.6f}, approximate distance effect {summaries['approximate_unlearning']['distance_reduction_fraction_vs_standard_update']:+.6f}, 15 mutations rejected, no core promotion.")


if __name__ == "__main__": main()
