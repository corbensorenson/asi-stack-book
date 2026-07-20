#!/usr/bin/env python3
"""Validate the bounded governed-training transaction and rejecting controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/training_run_transaction.schema.json"
FIXTURE = ROOT / "tests/fixtures/protocol_records/training_run_transaction.valid.json"
EXPECTED_SOURCES = {
    "ext_llama3_herd_2024",
    "ext_megatron_distributed_training_2021",
    "ext_zero_optimizer_2019",
    "ext_gspmd_2021",
    "ext_datastates_llm_2024",
    "ext_pytorch_distributed_checkpoint_2026",
    "ext_mlperf_training_v6_2026",
}
EXPECTED_NON_AUTHORITIES = {
    "model_quality", "optimizer_superiority", "distributed_efficiency",
    "exact_real_resume", "fault_tolerance", "safety", "support_transition",
    "release_or_publication",
}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict) -> list[str]:
    errors: list[str] = []
    execution = record.get("execution_ledger", {})
    checkpoint = record.get("checkpoint", {})
    family = record.get("checkpoint_family", {})
    handoff = record.get("qualification_handoff", {})
    topology = record.get("topology", {})

    required = set(checkpoint.get("required_state_classes", []))
    captured = set(checkpoint.get("captured_state_classes", []))
    if required != captured:
        errors.append("captured checkpoint state must equal the prospectively required state closure")
    required_names = {"model", "optimizer", "scheduler", "rng_cpu", "rng_device", "loss_scaler", "data_cursor", "sampler", "topology", "compiler_plan"}
    if not required_names.issubset(required):
        errors.append("checkpoint state closure omits a mandatory run-state class")

    attempted = execution.get("attempted_runs", -1)
    completed = execution.get("completed_runs", -1)
    failed = execution.get("failed_runs", -1)
    if attempted != completed + failed:
        errors.append("attempted run denominator must equal completed plus failed runs")
    if execution.get("recovered_runs", 0) > execution.get("interrupted_runs", 0):
        errors.append("recovered runs cannot exceed interrupted runs")

    devices = topology.get("device_count", 0)
    product = 1
    for key in ("data_parallel", "tensor_parallel", "pipeline_parallel", "context_parallel", "expert_parallel"):
        product *= topology.get(key, 0)
    if product != devices:
        errors.append("parallelism dimensions must multiply to the declared device count")
    if topology.get("global_batch") != topology.get("microbatch") * topology.get("gradient_accumulation") * topology.get("data_parallel"):
        errors.append("global batch must reconcile microbatch, accumulation, and data-parallel degree")

    candidates = family.get("candidate_ids", [])
    selected = family.get("selected_id")
    if selected not in candidates:
        errors.append("selected checkpoint must be in the retained candidate family")
    if handoff.get("candidate_id") != selected:
        errors.append("qualification handoff must name the validation-selected checkpoint")

    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("four-role primary-source packet is incomplete or contaminated")
    if set(record.get("non_authorities", [])) != EXPECTED_NON_AUTHORITIES:
        errors.append("non-authority ceiling changed")

    if record.get("expected_route") != "accept_bounded_qualification_handoff":
        errors.append("baseline route must be bounded qualification handoff")
    return errors


def validate(record: dict, schema: dict) -> list[str]:
    errors = [f"schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(record)]
    errors.extend(semantic_errors(record))
    return errors


def main() -> None:
    schema = load(SCHEMA)
    record = load(FIXTURE)
    baseline = validate(record, schema)
    if baseline:
        raise SystemExit("Baseline training-run transaction failed:\n- " + "\n- ".join(baseline))

    mutations: list[tuple[str, callable]] = [
        ("unfrozen inputs", lambda r: r["frozen_inputs"].__setitem__("frozen_before_run", False)),
        ("topology erased", lambda r: r["topology"].__setitem__("topology_recorded", False)),
        ("device topology mismatch", lambda r: r["topology"].__setitem__("device_count", 4)),
        ("global batch drift", lambda r: r["topology"].__setitem__("global_batch", 9)),
        ("numerical policy erased", lambda r: r["numerical_policy"].__setitem__("policy_recorded", False)),
        ("failed run hidden", lambda r: r["execution_ledger"].__setitem__("failed_runs_retained", False)),
        ("denominator laundered", lambda r: r["execution_ledger"].__setitem__("attempted_runs", 2)),
        ("impossible recovery count", lambda r: r["execution_ledger"].__setitem__("recovered_runs", 2)),
        ("state class omitted", lambda r: r["checkpoint"]["captured_state_classes"].remove("rng_device")),
        ("required state laundered", lambda r: r["checkpoint"]["required_state_classes"].remove("rng_device")),
        ("torn checkpoint", lambda r: r["checkpoint"].__setitem__("logical_step_consistent", False)),
        ("async completion missing", lambda r: r["checkpoint"].__setitem__("durably_committed", False)),
        ("resume data cursor drift", lambda r: r["resume_probe"].__setitem__("data_cursor_exact", False)),
        ("resume RNG drift", lambda r: r["resume_probe"].__setitem__("rng_state_exact", False)),
        ("candidate family censored", lambda r: r["checkpoint_family"].__setitem__("all_candidates_retained", False)),
        ("test-selected checkpoint", lambda r: r["checkpoint_family"].__setitem__("selection_split", "test")),
        ("handoff identity mismatch", lambda r: r["qualification_handoff"].__setitem__("candidate_id", "checkpoint-100")),
        ("qualification opened early", lambda r: r["qualification_handoff"].__setitem__("qualification_dataset_unopened_at_selection", False)),
        ("support laundering", lambda r: r["qualification_handoff"].__setitem__("support_transition_requested", True)),
        ("source role deletion", lambda r: r["source_ids"].pop()),
        ("non-authority deletion", lambda r: r["non_authorities"].pop()),
    ]
    survivors: list[str] = []
    for name, mutate in mutations:
        changed = copy.deepcopy(record)
        mutate(changed)
        if not validate(changed, schema):
            survivors.append(name)
    if survivors:
        raise SystemExit("Training-run mutations survived:\n- " + "\n- ".join(survivors))

    inventory = {row["id"] for row in load(ROOT / "sources/source_inventory.json")}
    missing_inventory = sorted(EXPECTED_SOURCES - inventory)
    missing_notes = sorted(source for source in EXPECTED_SOURCES if not (ROOT / f"sources/source_notes/{source}.md").is_file())
    if missing_inventory or missing_notes:
        raise SystemExit(f"Source packet incomplete: inventory={missing_inventory}, notes={missing_notes}")

    print("Training-run transaction passed: complete ten-class checkpoint closure, topology/batch reconciliation, full run denominator, validation-only checkpoint-family selection, qualification separation, seven-source role packet, eight non-authorities, and 21 rejecting mutations; no training, quality, support, or release claim.")


if __name__ == "__main__":
    main()
