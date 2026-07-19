#!/usr/bin/env python3
"""Build the P2 development-corpus custody and qualification receipt.

This script reads a pinned SWE-rebench V2 parquet object, retains only compact
metadata and content digests, and never vendors problem statements, solution
patches, test patches, source trees, or a final held-out denominator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "experiments/p2_governed_repository_admission/corpus"
SUMMARY = ROOT / "evidence_quality/p2_development_corpus_preflight.json"
METADATA = OUT_DIR / "post_snapshot_eligible_metadata.jsonl"
DEV_POOL = OUT_DIR / "development_pool.json"

SOURCE_URL = "https://huggingface.co/datasets/nebius/SWE-rebench-V2"
SOURCE_REVISION = "475dd5e8703bb5fb22dd3c60b5d038b019eba1e0"
SOURCE_PARQUET_SHA256 = "0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad"
CUTOFF = "2025-04-28 21:51:20"
MODEL_SNAPSHOT = "545dc4251c05440727734bcd94334791f6ab0192"
PERMISSIVE = {
    "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0", "ISC",
    "MIT", "MIT-0", "Unlicense",
}

DEV_IDS = [
    "aleph-alpha__ts-rs-422",
    "apiflask__apiflask-659",
    "behat__gherkin-343",
    "compose-spec__compose-go-792",
    "dynaconf__dynaconf-1293",
    "gitleaks__gitleaks-1845",
    "google__yamlfmt-259",
    "keithamus__sort-package-json-361",
    "more-itertools__more-itertools-1028",
    "quantecon__quantecon.py-769",
    "thealgorithms__java-6333",
    "true-myth__true-myth-1051",
]

SOURCE_RECEIPTS = {
    "aleph-alpha__ts-rs-422": ("https://github.com/Aleph-Alpha/ts-rs/pull/422", "2025-07-07T11:47:53Z", "2025-07-08T11:28:29Z", "f63dd5fbc402a5d29ded86266f47d8e8fa585472"),
    "apiflask__apiflask-659": ("https://github.com/apiflask/apiflask/pull/659", "2025-05-04T00:55:59Z", "2025-05-04T03:52:38Z", "adf18204180c630363c961aed07c5283785351e7"),
    "behat__gherkin-343": ("https://github.com/Behat/Gherkin/pull/343", "2025-05-22T16:46:59Z", "2025-05-22T21:41:34Z", "70108518c71c3a760157a591dea2aacf50e893d4"),
    "compose-spec__compose-go-792": ("https://github.com/compose-spec/compose-go/pull/792", "2025-05-20T11:32:07Z", "2025-05-20T12:05:51Z", "a6c896cdf0d93008cf78ba1a61b9d72bf3a6e236"),
    "dynaconf__dynaconf-1293": ("https://github.com/dynaconf/dynaconf/pull/1293", "2025-05-06T11:32:03Z", "2025-05-06T15:26:39Z", "82a3f61d1798a0048a2af76d5ea747d116765b62"),
    "gitleaks__gitleaks-1845": ("https://github.com/gitleaks/gitleaks/pull/1845", "2025-04-30T12:57:35Z", "2025-04-30T13:29:57Z", "d1c77598da5353c83c46d8a62be0d376a1b63bbb"),
    "google__yamlfmt-259": ("https://github.com/google/yamlfmt/pull/259", "2025-06-18T18:25:31Z", "2025-06-19T12:57:15Z", "1e2fd2c379fddce1682340a3b87178b73a4447fc"),
    "keithamus__sort-package-json-361": ("https://github.com/keithamus/sort-package-json/pull/361", "2025-05-08T13:30:24Z", "2025-05-08T13:47:39Z", "aa6774ad937feb83178c8bc981f08305e1d22b5c"),
    "more-itertools__more-itertools-1028": ("https://github.com/more-itertools/more-itertools/pull/1028", "2025-07-14T00:35:41Z", "2025-07-14T13:50:03Z", "7de169f7ad39eb1f95f8358225476e6f1a59d3d7"),
    "quantecon__quantecon.py-769": ("https://github.com/QuantEcon/QuantEcon.py/pull/769", "2025-06-22T13:14:57Z", "2025-07-06T06:56:15Z", "f3db957647ec0c28d8329ac6c8b34384e3eb07f1"),
    "thealgorithms__java-6333": ("https://github.com/TheAlgorithms/Java/pull/6333", "2025-07-01T13:00:00Z", "2025-07-02T12:51:56Z", "712ada5102be82b4807b0737ad70cfc0bca37935"),
    "true-myth__true-myth-1051": ("https://github.com/true-myth/true-myth/pull/1051", "2025-05-17T05:33:55Z", "2025-05-21T01:34:57Z", "918382841ed5d4ec3bd7ce6c666daa0c26fd36df"),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def diff_paths(diff: str | None) -> list[str]:
    paths: set[str] = set()
    for match in re.finditer(r"^diff --git a/(.+?) b/(.+)$", diff or "", re.MULTILINE):
        paths.update(match.groups())
    return sorted(paths)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def compact_row(row: dict) -> dict:
    solution_paths = diff_paths(row["patch"])
    test_paths = diff_paths(row["test_patch"])
    return {
        "instance_id": row["instance_id"],
        "created_at_utc": row["created_at"].replace(" ", "T") + "Z",
        "repo": row["repo"],
        "base_commit": row["base_commit"],
        "language": row["language"],
        "license": row["license"],
        "image_name": row["image_name"],
        "difficulty_annotation": row["difficulty"],
        "quality_code_annotation": row["code"],
        "detected_issue_annotations": row["detected_issues"],
        "pr_categories": row["pr_categories"] or [],
        "num_modified_files": row["num_modified_files"],
        "num_modified_lines": row["num_modified_lines"],
        "solution_paths": solution_paths,
        "test_paths": test_paths,
        "solution_test_path_overlap": sorted(set(solution_paths) & set(test_paths)),
        "problem_statement_present": bool((row["problem_statement"] or "").strip()),
        "solution_patch_present": bool((row["patch"] or "").strip()),
        "test_patch_present": bool((row["test_patch"] or "").strip()),
        "problem_statement_sha256": sha256_bytes((row["problem_statement"] or "").encode()),
        "solution_patch_sha256": sha256_bytes((row["patch"] or "").encode()),
        "test_patch_sha256": sha256_bytes((row["test_patch"] or "").encode()),
        "test_command_sha256": sha256_bytes((row["test_cmd"] or "").encode()),
        "dataset_pr_url_present": bool(row["pr_url"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-parquet", type=Path, required=True)
    args = parser.parse_args()
    source = args.source_parquet.resolve()
    observed_source_sha = sha256_file(source)
    if observed_source_sha != SOURCE_PARQUET_SHA256:
        raise SystemExit(f"source parquet digest mismatch: {observed_source_sha}")

    columns = [
        "instance_id", "created_at", "repo", "base_commit", "language",
        "license", "image_name", "problem_statement", "patch", "test_patch",
        "meta.num_modified_files", "meta.num_modified_lines",
        "meta.llm_metadata.difficulty", "meta.llm_metadata.code",
        "meta.llm_metadata.detected_issues",
        "meta.llm_metadata.pr_categories", "meta.pr_url",
        "install_config.test_cmd",
    ]
    all_rows = pq.read_table(source, columns=columns).to_pylist()
    eligible = sorted(
        (compact_row(row) for row in all_rows if row["created_at"] > CUTOFF),
        key=lambda row: row["instance_id"],
    )
    if len(eligible) != 1117:
        raise SystemExit(f"eligible denominator drifted: {len(eligible)}")

    by_id = {row["instance_id"]: row for row in eligible}
    if set(DEV_IDS) - set(by_id):
        raise SystemExit(f"development IDs missing: {sorted(set(DEV_IDS) - set(by_id))}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata_text = "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in eligible)
    METADATA.write_text(metadata_text, encoding="utf-8")
    pool_rows = []
    for instance_id in DEV_IDS:
        row = by_id[instance_id]
        url, created, merged, merge_commit = SOURCE_RECEIPTS[instance_id]
        if created != row["created_at_utc"]:
            raise SystemExit(f"GitHub creation timestamp mismatch: {instance_id}")
        pool_rows.append({
            **row,
            "github_pr_url": url,
            "github_created_at_utc": created,
            "github_merged_at_utc": merged,
            "github_merge_commit": merge_commit,
            "source_receipt_observed_date": "2026-07-17",
            "role": "development_only_not_final",
        })

    dev_pool = {
        "schema_version": "asi_stack.p2_development_pool.v1",
        "recorded_date": "2026-07-17",
        "selection_state": "development_pool_selected_final_pool_unselected",
        "selection_rule": "metadata-only convenience sample before task-text inspection: distinct repositories; seven languages; permissive SPDX licenses; post-model-snapshot merged PRs; dataset quality code A; easy annotation; one or two modified files; separate solution/test paths; accessible public PR and container manifest",
        "task_text_inspected_for_selection": False,
        "gold_patch_or_test_outcome_used_for_selection": False,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "rows": pool_rows,
    }
    DEV_POOL.write_text(json.dumps(dev_pool, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    license_counts = Counter(row["license"] or "null" for row in eligible)
    language_counts = Counter(row["language"] for row in eligible)
    difficulty_counts = Counter(row["difficulty_annotation"] or "null" for row in eligible)
    permissive_rows = [row for row in eligible if row["license"] in PERMISSIVE]
    summary = {
        "schema_version": "asi_stack.p2_development_corpus_preflight.v1",
        "recorded_date": "2026-07-17",
        "state": "natural_corpus_candidate_qualified_for_development_only",
        "claim_id": "p2.governed_natural_repository_change_admission_joint_frontier",
        "source": {
            "source_id": "ext_swe_rebench_v2_2026",
            "dataset_url": SOURCE_URL,
            "dataset_revision": SOURCE_REVISION,
            "parquet_sha256": observed_source_sha,
            "dataset_license": "CC-BY-4.0 with per-repository license obligations",
            "raw_parquet_retention": "transient_local_preflight_only_not_vendored",
        },
        "contamination_boundary": {
            "candidate_model_snapshot": MODEL_SNAPSHOT,
            "candidate_model_snapshot_last_modified_utc": CUTOFF.replace(" ", "T") + "Z",
            "filter": f"created_at > {CUTOFF} UTC",
            "claim": "reduced_by_post_snapshot_filter_not_eliminated_or_proven_absent",
        },
        "eligible_universe": {
            "row_count": len(eligible),
            "repository_count": len({row["repo"] for row in eligible}),
            "language_count": len(language_counts),
            "language_counts": dict(sorted(language_counts.items())),
            "license_counts": dict(sorted(license_counts.items())),
            "difficulty_counts": dict(sorted(difficulty_counts.items())),
            "permissive_license_row_count": len(permissive_rows),
            "missing_problem_statement_count": sum(not row["problem_statement_present"] for row in eligible),
            "solution_test_path_overlap_count": sum(bool(row["solution_test_path_overlap"]) for row in eligible),
            "duplicate_repo_base_commit_count": len(eligible) - len({(row["repo"], row["base_commit"]) for row in eligible}),
            "metadata_sha256": sha256_bytes(metadata_text.encode()),
            "metadata_path": str(METADATA.relative_to(ROOT)),
        },
        "development_pool": {
            "row_count": len(pool_rows),
            "repository_count": len({row["repo"] for row in pool_rows}),
            "language_count": len({row["language"] for row in pool_rows}),
            "languages": sorted({row["language"] for row in pool_rows}),
            "all_permissive_license": all(row["license"] in PERMISSIVE for row in pool_rows),
            "all_quality_code_a": all(row["quality_code_annotation"] == "A" for row in pool_rows),
            "all_diagnostic_flags_false": all(not any(row["detected_issue_annotations"].values()) for row in pool_rows),
            "all_solution_test_paths_disjoint": all(not row["solution_test_path_overlap"] for row in pool_rows),
            "all_github_created_post_snapshot": all(row["github_created_at_utc"] > CUTOFF.replace(" ", "T") + "Z" for row in pool_rows),
            "all_github_merged": all(bool(row["github_merged_at_utc"]) for row in pool_rows),
            "pool_sha256": sha256_bytes(canonical_json(pool_rows)),
            "pool_path": str(DEV_POOL.relative_to(ROOT)),
        },
        "known_dataset_limitations": [
            "automated construction and LLM-based quality annotations do not replace local construct validation",
            "the paper's diagnostic study covers 300 tasks in five languages rather than every released task",
            "tests can impose implicit naming requirements, couple unrelated regressions, or depend on external resources",
            "repository image names can be missing or mismatched; manifest availability and gold execution are separate gates",
            "amd64-only images require measured emulation on the local arm64 host",
            "test-based correctness does not observe authority, residual, rollback, or governance cost",
        ],
        "required_before_construct_pass": [
            "all 12 development image manifests resolve by digest",
            "all 12 qualified or same-language deterministically replaced tasks reproduce fail-to-pass and pass-to-pass behavior under network-off outcome execution",
            "candidate patch application rejects any edit to test-patch paths before test-patch application",
            "independent task/specification review finds no hidden naming or external-context requirement",
            "development tasks and injected candidates expose useful-safe, unsafe-admission, false-blocking, abstention, rollback, and residual opportunities",
            "final tasks remain unselected and unopened until all competence gates pass",
        ],
        "preflight_effect": {
            "construct_gate": "pending_four_replacements_dual_evaluator_and_independent_task_review",
            "resource_gate": "pending_peak_memory_cpu_and_frozen_ceiling_before_replacement_draw",
            "final_heldout_gate": "closed",
            "support_state_effect": "none",
            "release_effect": "none",
        },
        "non_claims": [
            "Development-corpus qualification is not a benchmark result or competence-qualified empirical transition.",
            "Dataset annotations are screening signals, not independent evaluator truth.",
            "A resolvable image manifest is not a successful gold execution.",
            "The 12 development tasks are not the final held-out denominator.",
            "No coding ability, governance benefit, safety, transfer, reproduction, SOTA, AGI, or ASI claim follows.",
        ],
    }
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"P2 corpus preflight wrote {len(eligible)} eligible metadata rows and "
        f"{len(pool_rows)} development-only tasks; final pool remains unselected."
    )


if __name__ == "__main__":
    main()
