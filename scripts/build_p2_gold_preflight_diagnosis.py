#!/usr/bin/env python3
"""Aggregate the immutable P2 gold-preflight and bounded-rescue lineage."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/p2_governed_repository_admission"
OUT = ROOT / "evidence_quality/p2_gold_preflight_diagnosis.json"

PATHS = {
    "read_only": BASE / "gold_preflight_attempt_001_read_only_instrument_failure/result.json",
    "pilot": BASE / "gold_preflight_attempt_002_pilot_success/result.json",
    "full": BASE / "gold_preflight/result.json",
    "abort": BASE / "gold_preflight_rescue/attempts/2026-07-17-raw-log-custody-abort/record.json",
    "rust": BASE / "gold_preflight_rescue/attempts/2026-07-17-rust-diagnostic-r1/result.json",
    "dependency": BASE / "gold_preflight_rescue/attempts/2026-07-17-dependency-diagnostic-r1/result.json",
    "java_ipv4": BASE / "gold_preflight_rescue/attempts/2026-07-17-java-ipv4-diagnostic-r1/result.json",
    "java_surefire": BASE / "gold_preflight_rescue/attempts/2026-07-17-java-surefire-diagnostic-r1/result.json",
}

QUALIFIED = [
    "apiflask__apiflask-659",
    "behat__gherkin-343",
    "dynaconf__dynaconf-1293",
    "google__yamlfmt-259",
    "keithamus__sort-package-json-361",
    "more-itertools__more-itertools-1028",
    "quantecon__quantecon.py-769",
    "true-myth__true-myth-1051",
]

EXCLUSIONS = {
    "aleph-alpha__ts-rs-422": {
        "language": "rust",
        "code": "baseline_expected_status_set_unobservable",
        "diagnosis": "The test patch produces a compile-stage failure and no named test statuses although the dataset requires 480 named failures; the human-gold arm passes 481 tests, including imports::test_def, which is absent from the stored expected set.",
        "decisive_attempt": "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-rust-diagnostic-r1/result.json",
    },
    "compose-spec__compose-go-792": {
        "language": "go",
        "code": "runtime_external_resource_required",
        "diagnosis": "TestSchema fetches json-schema.org during outcome execution, while the target baseline panic makes 59 stored fail-to-pass identities unobservable; the human-gold arm removes the target panic but the unrelated external-schema test still fails.",
        "decisive_attempt": "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-dependency-diagnostic-r1/result.json",
    },
    "gitleaks__gitleaks-1845": {
        "language": "go",
        "code": "independent_specification_review_failed",
        "diagnosis": "The target human-gold change behaves, but TestFromGit and TestFromGitStaged fail in both arms because the local Docker filesystem returns EXDEV when the fixture renames dotGit to .git; four stored pass-to-pass identities are therefore not portable to this execution environment.",
        "decisive_attempt": "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-dependency-diagnostic-r1/result.json",
    },
    "thealgorithms__java-6333": {
        "language": "java",
        "code": "dependency_materialization_failure",
        "diagnosis": "Maven reveals runtime-only dynamic dependencies sequentially: generic go-offline omitted Surefire's JUnit provider, and an explicit provider fetch still omitted junit-platform-launcher 1.13.2. The frozen bounded rescue ended rather than chasing an open-ended dependency chain.",
        "decisive_attempt": "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-java-surefire-diagnostic-r1/result.json",
    },
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def verify_log(path_text: str, expected: str) -> None:
    path = ROOT / path_text
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        observed = sha256_text(handle.read())
    if observed != expected:
        raise SystemExit(f"raw log digest mismatch: {path_text}")


def verify_log_path(path: Path, expected: str) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        observed = sha256_text(handle.read())
    if observed != expected:
        raise SystemExit(f"raw log digest mismatch: {path.relative_to(ROOT)}")
    return str(path.relative_to(ROOT))


def iter_rescue_tasks(result: dict):
    yield from result.get("rescue_results", [])


def main() -> None:
    records = {name: load(path) for name, path in PATHS.items()}
    for name, record in records.items():
        if record.get("final_pool_selected") is not False or record.get("final_pool_opened") is not False:
            raise SystemExit(f"final custody opened in {name}")
        if record.get("support_state_effect") != "none":
            raise SystemExit(f"support promotion in {name}")

    full = records["full"]
    full_by_id = {row["instance_id"]: row for row in full["tasks"]}
    original_passes = sorted(row["instance_id"] for row in full["tasks"] if row["all_runs_pass"])
    if len(original_passes) != 7:
        raise SystemExit("original fixed-denominator result drifted")
    for task in full["tasks"]:
        for run in task["runs"]:
            verify_log(run["compressed_log_path"], run["output_sha256"])

    raw_paths: set[str] = set()
    prep_paths: set[str] = set()
    arm_durations = []
    preparation_durations = []
    for task in full["tasks"]:
        for run in task["runs"]:
            raw_paths.add(run["compressed_log_path"])
            arm_durations.append(run["duration_seconds"])
    for key in ["read_only", "pilot"]:
        for task in records[key]["tasks"]:
            for run in task["runs"]:
                historical = PATHS[key].parent / "logs" / Path(run["compressed_log_path"]).name
                raw_paths.add(verify_log_path(historical, run["output_sha256"]))
                arm_durations.append(run["duration_seconds"])
    for key in ["rust", "dependency", "java_ipv4", "java_surefire"]:
        for task in iter_rescue_tasks(records[key]):
            if task.get("preparation_log"):
                verify_log(task["preparation_log"], task["preparation_log_sha256"])
                prep_paths.add(task["preparation_log"])
                preparation_durations.append(task["preparation_seconds"])
            for run in task.get("runs", []):
                if run.get("compressed_log_path"):
                    verify_log(run["compressed_log_path"], run["output_sha256"])
                    raw_paths.add(run["compressed_log_path"])
                    arm_durations.append(run["duration_seconds"])
            for run in task.get("runs", []):
                if run.get("source_log"):
                    verify_log(run["source_log"], run["source_log_sha256"])
                    raw_paths.add(run["source_log"])

    dependency = records["dependency"]
    keith = next(row for row in dependency["rescue_results"] if row["instance_id"] == "keithamus__sort-package-json-361")
    if not keith["all_runs_pass"] or any(run["upstream_parser_pass"] for run in keith["runs"] if run["arm"] == "baseline_test_patch_only"):
        raise SystemExit("independent AVA-parser rescue drifted")
    if sorted(QUALIFIED) != sorted(original_passes + ["keithamus__sort-package-json-361"]):
        raise SystemExit("qualified task set drifted")
    if set(QUALIFIED) | set(EXCLUSIONS) != set(full_by_id):
        raise SystemExit("fixed denominator is not fully dispositioned")

    lineage = []
    for name, path in PATHS.items():
        record = records[name]
        lineage.append({
            "id": name,
            "path": str(path.relative_to(ROOT)),
            "state": record.get("state"),
            "negative_inference_level": "N0" if record.get("state") != "passed" else "none",
            "claim_effect": "none",
        })
    dispositions = []
    for instance_id in sorted(QUALIFIED):
        dispositions.append({
            "instance_id": instance_id,
            "language": full_by_id[instance_id]["language"],
            "disposition": "development_gold_oracle_qualified",
            "qualification_path": (
                "independent_ava_log_rescore"
                if instance_id == "keithamus__sort-package-json-361"
                else "original_exact_paired_oracle"
            ),
            "negative_inference_level": "none",
            "claim_effect": "none",
        })
    for instance_id, exclusion in sorted(EXCLUSIONS.items()):
        dispositions.append({
            "instance_id": instance_id,
            "language": exclusion["language"],
            "disposition": "excluded_replacement_required",
            "exclusion_code": exclusion["code"],
            "diagnosis": exclusion["diagnosis"],
            "decisive_attempt": exclusion["decisive_attempt"],
            "negative_inference_level": "N0",
            "claim_effect": "none",
        })

    pull_seconds = [row["pull_seconds"] for row in full["tasks"]]
    expanded = [row["expanded_image_size_bytes"] for row in full["tasks"]]
    output = {
        "schema_version": "asi_stack.p2_gold_preflight_diagnosis.v1",
        "recorded_date": "2026-07-17",
        "state": "fixed_denominator_terminally_dispositioned_replacements_pending",
        "claim_id": full["claim_id"],
        "scope": "development_only_gold_oracle_instrument_and_construct_diagnosis",
        "original_fixed_denominator": {
            "task_count": 12,
            "exact_pass_count": 7,
            "instrument_failure_count": 5,
            "repetitions_per_arm": 2,
            "runtime_network": "none",
            "result_path": "experiments/p2_governed_repository_admission/gold_preflight/result.json"
        },
        "terminal_disposition": {
            "qualified_task_count": len(QUALIFIED),
            "excluded_n0_task_count": len(EXCLUSIONS),
            "replacement_slot_count": len(EXCLUSIONS),
            "qualified_language_count": len({full_by_id[value]["language"] for value in QUALIFIED}),
            "replacement_languages": sorted(value["language"] for value in EXCLUSIONS.values()),
            "all_original_tasks_dispositioned": True,
            "task_dispositions": dispositions,
        },
        "false_negative_findings": {
            "upstream_parser_false_reject_count": 1,
            "post_test_start_dependency_fetch_failure_count": 4,
            "compile_or_panic_expected_set_unobservable_count": 2,
            "runtime_external_resource_task_count": 1,
            "local_filesystem_semantics_incompatibility_count": 1,
            "bounded_dynamic_dependency_chain_exhaustion_count": 1,
            "idea_or_mechanism_negative_inference_count": 0,
        },
        "attempt_lineage": lineage,
        "custody_and_raw_evidence": {
            "attempt_record_count": len(lineage),
            "verified_compressed_arm_log_count": len(raw_paths),
            "verified_dependency_preparation_log_count": len(prep_paths),
            "aborted_missing_raw_log_attempt_count": 1,
            "raw_log_custody_required_after_abort": True,
            "final_pool_selected": False,
            "final_pool_opened": False,
        },
        "resource_observations": {
            "max_original_pull_seconds": round(max(pull_seconds), 6),
            "sum_original_pull_seconds": round(sum(pull_seconds), 6),
            "max_expanded_image_size_bytes": max(expanded),
            "max_observed_arm_seconds": round(max(arm_durations), 6),
            "max_dependency_preparation_seconds": round(max(preparation_durations), 6),
            "original_full_run_host_free_byte_delta": full["host_free_bytes_after"] - full["host_free_bytes_before"],
            "resource_gate_state": "pending_peak_memory_cpu_and_frozen_ceiling_before_replacement_draw",
        },
        "next_required_action": {
            "policy_path": "evidence_quality/p2_task_qualification_and_replacement_policy.json",
            "resource_ceiling_must_be_frozen_before_draw": True,
            "replacement_draw_started": False,
            "replacement_task_count_required": 4,
            "rerun_two_repetitions_after_replacement": True,
            "independent_specification_review_still_required": True,
        },
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "Development gold-oracle qualification is not a model-capability, governed-admission, safety, transfer, SOTA, release, AGI, or ASI result.",
            "The four excluded tasks are N0 instrument or construct dispositions, not failures of the book's mechanism.",
            "Eight qualified development tasks do not permit reduction of the frozen twelve-task target; four replacements are required.",
            "The final held-out pool remains unselected and unopened."
        ]
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"P2 gold diagnosis: {len(QUALIFIED)} qualified, {len(EXCLUSIONS)} N0 exclusions, "
        f"{len(raw_paths)} verified arm logs, {len(lineage)} attempts; final pool closed."
    )


if __name__ == "__main__":
    main()
