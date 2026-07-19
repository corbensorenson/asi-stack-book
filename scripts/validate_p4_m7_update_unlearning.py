#!/usr/bin/env python3
"""Validate terminal P4/M7 evidence, axis separation, and claim ceiling."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import jsonschema
import torch

from p4_m7_update_unlearning_common import (
    ARMS,
    CLAIM_AXES,
    CORPUS,
    FEATURES,
    PREFLIGHT,
    PREREG,
    RAW_RUN,
    RESULT,
    ROOT,
    SEEDS,
    STATE_SURFACES,
    file_sha,
    load_json,
    state_sha,
)


SCHEMA = ROOT / "schemas" / "p4_m7_update_unlearning_result.schema.json"


def errors(result: dict[str, Any]) -> list[str]:
    out: list[str] = []
    prereg = load_json(PREREG); preflight = load_json(PREFLIGHT); raw = load_json(RAW_RUN)
    if result.get("corpus_sha256") != file_sha(CORPUS) or result.get("preregistration_sha256") != file_sha(PREREG) or result.get("raw_run_sha256") != file_sha(RAW_RUN):
        out.append("frozen lineage digest drift")
    if result.get("feature_artifact_sha256") != file_sha(FEATURES):
        out.append("feature artifact digest drift")
    if result.get("candidate_and_checkpoint_bytes_closed_before_axis_evaluation") is not True:
        out.append("candidate closure drift")
    if preflight.get("protocol_outcome") != "instrument_adequate" or preflight.get("heldout_opened") is not True:
        out.append("instrument qualification drift")
    if result.get("seeds") != list(SEEDS) or result.get("arms") != list(ARMS):
        out.append("seed or arm denominator drift")
    if result.get("claim_axes") != list(CLAIM_AXES) or set(result.get("axis_dispositions", {})) != set(CLAIM_AXES):
        out.append("claim-axis separation drift")
    seed_results = result.get("seed_results", [])
    if len(seed_results) != 5 or any([row.get("arm") for row in seed.get("arms", [])] != list(ARMS) for seed in seed_results):
        out.append("per-seed arm coverage drift")
    if any(row.get("full_state", {}).get("surface_count") != 24 for seed in seed_results for row in seed.get("arms", [])):
        out.append("full-state inventory truncation")
    if any(row.get("full_state", {}).get("rollback_exact") is not True or row["full_state"].get("rollback_sha256") != row["full_state"].get("before_sha256") for seed in seed_results for row in seed.get("arms", [])):
        out.append("rollback exactness drift")
    for seed in raw.get("seed_records", []):
        for arm in seed.get("arms", []):
            state = torch.load(ROOT / arm["best_checkpoint"]["path"], map_location="cpu", weights_only=True)
            if state_sha(state) != arm["best_checkpoint"]["state_sha256"]:
                out.append(f"checkpoint tensor identity drift: {seed['seed']} {arm['arm']}")
    gates = result.get("gate_checks_before_validator_mutations", {})
    if len(gates) != 9 or not all(gates.values()):
        out.append("frozen terminal gate failed")
    storage = result.get("storage_receipt", {})
    if storage.get("bounded_operational_derived_store_erasure") is not True or storage.get("total_storage_erasure") is not False:
        out.append("partial storage boundary drift")
    if not all(storage.get("physical_absence_after_request", {}).values()) or storage.get("logical_index_references_after_request") != 0:
        out.append("declared local deletion observation drift")
    if storage.get("remote_backup", {}).get("erasure_acknowledged") is not False or not storage.get("retained_research_evidence"):
        out.append("remote or retained-evidence residual erased")
    lineage = result.get("lineage_receipt", {})
    if lineage.get("local_descendant_invalidation_count") != 5 or any(row.get("physical_erasure") is not False for row in lineage.get("descendants", [])):
        out.append("descendant invalidation/erasure distinction drift")
    if lineage.get("external_descendant", {}).get("erasure_verified") is not False:
        out.append("external descendant closure laundered")
    if result.get("protocol_outcome") != "instrument_adequate_bounded_local_axis_separation" or result.get("claim_outcome") != "support_retained_with_bounded_noncore_axis_result":
        out.append("terminal disposition drift")
    if result.get("support_state_effect") != "none" or result.get("chapter_core_promotion_count") != 0:
        out.append("unsupported core promotion")
    ceiling = result.get("claim_ceiling", "")
    for phrase in ("not language-model unlearning", "privacy", "complete erasure", "legal compliance", "transfer", "SOTA"):
        if phrase not in ceiling:
            out.append(f"claim ceiling lost: {phrase}")
    if result.get("evaluator_recomputation_disagreement_count") != 0:
        out.append("evaluator disagreement drift")
    if prereg.get("support_ceiling", "").startswith("No chapter-core promotion") is not True:
        out.append("preregistered support ceiling drift")
    return out


def main() -> None:
    result = load_json(RESULT)
    jsonschema.validate(result, load_json(SCHEMA))
    failures = errors(result)
    mutations = []
    for axis in CLAIM_AXES:
        candidate = copy.deepcopy(result); candidate["axis_dispositions"].pop(axis)
        if not errors(candidate):
            failures.append(f"axis deletion mutation accepted: {axis}")
        mutations.append(axis)
    for label, mutation in (
        ("truncate state", lambda r: r["seed_results"][0]["arms"][0]["full_state"].__setitem__("surface_count", 23)),
        ("false rollback", lambda r: r["seed_results"][0]["arms"][1]["full_state"].__setitem__("rollback_exact", False)),
        ("claim total erasure", lambda r: r["storage_receipt"].__setitem__("total_storage_erasure", True)),
        ("erase retained evidence", lambda r: r["storage_receipt"].__setitem__("retained_research_evidence", [])),
        ("invent remote ack", lambda r: r["storage_receipt"]["remote_backup"].__setitem__("erasure_acknowledged", True)),
        ("invent descendant erasure", lambda r: r["lineage_receipt"]["external_descendant"].__setitem__("erasure_verified", True)),
        ("promote core", lambda r: r.__setitem__("chapter_core_promotion_count", 1)),
        ("launder LM unlearning", lambda r: r.__setitem__("claim_ceiling", "language-model unlearning established")),
    ):
        candidate = copy.deepcopy(result); mutation(candidate)
        if not errors(candidate):
            failures.append(f"terminal mutation accepted: {label}")
        mutations.append(label)
    if failures:
        raise SystemExit("P4/M7 validation failed:\n - " + "\n - ".join(failures))
    approx = result["arm_summaries"]["approximate_unlearning"]
    print(
        "P4/M7 validation passed: 5 seeds x 7 arms, 24/24 surfaces with exact local rollback, "
        f"8 distinct claim axes, approximate distance reduction {approx['distance_reduction_fraction_vs_standard_update']:.6f}, "
        f"membership AUC {approx['membership_attack_auc']:.6f}, 16 negative mutations rejected, and no core promotion."
    )


if __name__ == "__main__":
    main()
