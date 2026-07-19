#!/usr/bin/env python3
"""Validate the frozen P2 resource ceiling and measurement pilot."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence_quality/p2_resource_ceiling.json"
SCHEMA = ROOT / "schemas/p2_resource_ceiling.schema.json"
DOC = ROOT / "docs/p2_resource_ceiling.md"
DIAGNOSIS = ROOT / "evidence_quality/p2_gold_preflight_diagnosis.json"


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    host = record.get("host_receipt", {})
    hard = record.get("per_container_hard_limits", {})
    task = record.get("task_acceptance_ceilings", {})
    campaign = record.get("campaign_ceilings", {})
    measure = record.get("measurement_contract", {})
    basis = record.get("empirical_basis", {})
    state = record.get("qualification_state", {})
    checks = [
        (host.get("docker_memory_bytes", 0) > hard.get("memory_bytes", 10**30), "container memory hard limit exceeds Docker allocation"),
        (host.get("docker_cpu_count", 0) >= hard.get("cpus", 10**9), "container CPU allocation exceeds Docker CPUs"),
        (task.get("peak_memory_bytes", 10**30) < hard.get("memory_bytes", 0), "accepted peak memory lacks hard-limit headroom"),
        (task.get("arm_wall_seconds", 10**30) < hard.get("arm_timeout_seconds", 0), "accepted wall time is not below kill timeout"),
        (task.get("peak_pids", 10**30) < hard.get("pids", 0), "accepted PIDs lack hard-limit headroom"),
        (task.get("max_cpu_percent") <= hard.get("cpus", 0) * 100, "CPU ceiling exceeds allocation"),
        (task.get("minimum_host_free_bytes_before_task", 0) > task.get("maximum_post_cleanup_host_free_byte_loss", 10**30), "disk reserve is not larger than task residual"),
        (task.get("timeout_allowed") is False, "timeout allowed"),
        (task.get("oom_or_signal_kill_allowed") is False, "OOM or signal kill allowed"),
        (task.get("cleanup_nonzero_allowed") is False, "cleanup failure allowed"),
        (campaign.get("minimum_qualified_task_count") == 12, "denominator shrank below twelve"),
        (campaign.get("denominator_reduction_allowed") is False, "denominator reduction allowed"),
        (campaign.get("resource_exhaustion_effect") == "corpus_gate_blocked_not_claim_failure", "resource exhaustion gained claim effect"),
        (measure.get("monitor_failure_effect") == "resource_gate_failure", "monitor failure no longer fails closed"),
        (measure.get("cpu_seconds_semantics") == "sampled_estimate_not_exact_billing_measure", "sampled CPU was overclaimed as exact"),
        (measure.get("raw_arm_logs_required") is True, "raw logs not required"),
        (measure.get("cleanup_and_host_free_space_receipts_required") is True, "cleanup/disk receipts not required"),
        (basis.get("resource_pilot_exact_oracle_pass") is True, "resource pilot oracle did not pass"),
        (basis.get("resource_pilot_min_sample_count", 0) >= 1, "resource pilot collected no samples"),
        (state.get("ceiling_frozen") is True, "ceiling is not frozen"),
        (state.get("replacement_draw_started") is True, "frozen metadata replacement draw is not recorded"),
        (state.get("resource_gate_passed") is False, "resource gate passed before all tasks were measured"),
    ]
    out.extend(message for passed, message in checks if not passed)
    if task.get("image_pull_seconds", 0) <= basis.get("original_max_pull_seconds", 10**30):
        out.append("pull ceiling has no headroom over observation")
    if task.get("engine_content_size_bytes", 0) <= basis.get("max_rank_one_engine_content_size_bytes", 10**30):
        out.append("Engine content ceiling has no headroom over observation")
    if task.get("virtual_size_conservative_upper_bound_bytes", 0) <= basis.get("max_rank_one_virtual_size_conservative_upper_bound_bytes", 10**30):
        out.append("virtual-size ceiling has no headroom over observation")
    if task.get("cleanup_stabilization_timeout_seconds") != 60 or task.get("cleanup_stabilization_required_consecutive_samples") != 3:
        out.append("cleanup stabilization contract drifted")
    if task.get("arm_wall_seconds", 0) <= basis.get("observed_max_arm_seconds", 10**30):
        out.append("arm ceiling has no headroom over observation")
    if task.get("dependency_materialization_seconds", 0) <= basis.get("observed_max_dependency_materialization_seconds", 10**30):
        out.append("dependency ceiling has no headroom over observation")
    if inspect_files:
        diagnosis = json.loads(DIAGNOSIS.read_text(encoding="utf-8"))
        observed = diagnosis["resource_observations"]
        mappings = {
            "original_sum_pull_seconds": "sum_original_pull_seconds",
            "original_max_pull_seconds": "max_original_pull_seconds",
            "original_max_engine_content_size_bytes": "max_expanded_image_size_bytes",
            "observed_max_arm_seconds": "max_observed_arm_seconds",
            "observed_max_dependency_materialization_seconds": "max_dependency_preparation_seconds",
        }
        for local, source in mappings.items():
            if basis.get(local) != observed.get(source):
                out.append(f"empirical resource basis drifted: {local}")
        pilot_path = ROOT / basis.get("resource_pilot_path", "")
        if not pilot_path.is_file():
            out.append("resource pilot result missing")
        else:
            pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
            runs = pilot["tasks"][0]["runs"]
            if not all(run.get("pass") for run in runs):
                out.append("resource pilot exact oracle failed")
            if min(run.get("resource_monitor", {}).get("sample_count", 0) for run in runs) != basis.get("resource_pilot_min_sample_count"):
                out.append("resource pilot sample count drifted")
            if max(run["resource_monitor"]["peak_memory_bytes"] for run in runs) != basis.get("resource_pilot_peak_memory_bytes"):
                out.append("resource pilot peak memory drifted")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in [
            "v2 measurement semantics repaired",
            "old expanded-size pass is invalidated",
            "resource gate has not passed",
            "sampled CPU-seconds value is explicitly an estimate",
            "blocks the corpus gate",
            "candidate outcomes",
            "final held-out pool remains unselected and unopened",
        ]:
            if phrase not in doc:
                out.append(f"resource receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("memory over Docker", lambda r: r["per_container_hard_limits"].__setitem__("memory_bytes", 9000000000))
    add("no memory headroom", lambda r: r["task_acceptance_ceilings"].__setitem__("peak_memory_bytes", 8000000000))
    add("virtual size ceiling erased", lambda r: r["task_acceptance_ceilings"].__setitem__("virtual_size_conservative_upper_bound_bytes", 0))
    add("cleanup stabilization erased", lambda r: r["task_acceptance_ceilings"].__setitem__("cleanup_stabilization_timeout_seconds", 0))
    add("wall equals kill", lambda r: r["task_acceptance_ceilings"].__setitem__("arm_wall_seconds", 1200))
    add("timeout allowed", lambda r: r["task_acceptance_ceilings"].__setitem__("timeout_allowed", True))
    add("cleanup allowed", lambda r: r["task_acceptance_ceilings"].__setitem__("cleanup_nonzero_allowed", True))
    add("denominator shrink", lambda r: r["campaign_ceilings"].__setitem__("minimum_qualified_task_count", 8))
    add("resource refutation", lambda r: r["campaign_ceilings"].__setitem__("resource_exhaustion_effect", "claim_failure"))
    add("monitor ignored", lambda r: r["measurement_contract"].__setitem__("monitor_failure_effect", "ignore"))
    add("exact CPU overclaim", lambda r: r["measurement_contract"].__setitem__("cpu_seconds_semantics", "exact_energy_measure"))
    add("replacement draw erased", lambda r: r["qualification_state"].__setitem__("replacement_draw_started", False))
    add("premature pass", lambda r: r["qualification_state"].__setitem__("resource_gate_passed", True))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 resource ceiling failed:\n - " + "\n - ".join(out))
    print("P2 resource ceiling passed: v2 content/virtual-size semantics and stabilized cleanup frozen before candidate outcomes, 12-task denominator retained, final pool closed; 14/14 mutations rejected.")


if __name__ == "__main__":
    main()
