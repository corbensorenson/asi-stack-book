#!/usr/bin/env python3
"""Freeze the metadata-only deterministic P2 replacement queues."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "experiments/p2_governed_repository_admission/corpus/post_snapshot_eligible_metadata.jsonl"
POOL = ROOT / "experiments/p2_governed_repository_admission/corpus/development_pool.json"
POLICY = ROOT / "evidence_quality/p2_task_qualification_and_replacement_policy.json"
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
DIAGNOSIS = ROOT / "evidence_quality/p2_gold_preflight_diagnosis.json"
OUT = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"

PERMISSIVE = {
    "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0", "ISC",
    "MIT", "MIT-0", "Unlicense",
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def eligible(row: dict, *, used_ids: set[str], used_repos: set[str]) -> bool:
    return (
        row["instance_id"] not in used_ids
        and row["repo"] not in used_repos
        and row["license"] in PERMISSIVE
        and row["quality_code_annotation"] == "A"
        and not any(row["detected_issue_annotations"].values())
        and row["difficulty_annotation"] == "easy"
        and row["num_modified_files"] in {1, 2}
        and not row["solution_test_path_overlap"]
        and row["problem_statement_present"]
        and row["solution_patch_present"]
        and row["test_patch_present"]
        and bool(row["image_name"])
    )


def compact(row: dict, *, rank: int, order_hash: str) -> dict:
    return {
        "rank": rank,
        "order_sha256": order_hash,
        "instance_id": row["instance_id"],
        "created_at_utc": row["created_at_utc"],
        "repo": row["repo"],
        "base_commit": row["base_commit"],
        "language": row["language"],
        "license": row["license"],
        "image_name": row["image_name"],
        "difficulty_annotation": row["difficulty_annotation"],
        "quality_code_annotation": row["quality_code_annotation"],
        "num_modified_files": row["num_modified_files"],
        "num_modified_lines": row["num_modified_lines"],
        "problem_statement_sha256": row["problem_statement_sha256"],
        "solution_patch_sha256": row["solution_patch_sha256"],
        "test_patch_sha256": row["test_patch_sha256"],
        "test_command_sha256": row["test_command_sha256"],
        "github_pr_url_candidate": f"https://github.com/{row['repo']}/pull/{row['instance_id'].rsplit('-', 1)[1]}",
        "public_pr_receipt_state": "unverified",
        "image_manifest_state": "unprobed",
        "task_content_opened": False,
        "gold_outcome_opened": False,
    }


def main() -> None:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    resource = json.loads(RESOURCE.read_text(encoding="utf-8"))
    diagnosis = json.loads(DIAGNOSIS.read_text(encoding="utf-8"))
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    if policy["replacement_rule"]["replacement_draw_state"] != "not_started":
        raise SystemExit("replacement policy was not in the frozen pre-draw state")
    if not resource["qualification_state"]["ceiling_frozen"] or resource["qualification_state"]["replacement_draw_started"]:
        raise SystemExit("resource ceiling not frozen before draw")
    if diagnosis["next_required_action"]["replacement_draw_started"]:
        raise SystemExit("diagnosis already reports a replacement draw")
    rows = [json.loads(line) for line in METADATA.read_text(encoding="utf-8").splitlines() if line.strip()]
    original_ids = {row["instance_id"] for row in pool["rows"]}
    original_repos = {row["repo"] for row in pool["rows"]}
    seed = policy["replacement_rule"]["seed"]
    max_per_slot = policy["replacement_rule"]["maximum_candidates_per_slot"]
    excluded = sorted(
        (row for row in diagnosis["terminal_disposition"]["task_dispositions"] if row["disposition"] == "excluded_replacement_required"),
        key=lambda row: row["instance_id"],
    )
    if len(excluded) != 4:
        raise SystemExit("replacement slot count drifted")

    language_queues: dict[str, list[dict]] = {}
    for language in sorted({row["language"] for row in excluded}):
        candidates = []
        seen_repos = set()
        for row in sorted(
            (row for row in rows if row["language"] == language and eligible(row, used_ids=original_ids, used_repos=original_repos)),
            key=lambda row: sha256((seed + "\0" + row["instance_id"]).encode()),
        ):
            if row["repo"] in seen_repos:
                continue
            seen_repos.add(row["repo"])
            candidates.append(row)
        language_queues[language] = candidates

    consumed_by_language: dict[str, int] = {language: 0 for language in language_queues}
    slots = []
    all_candidates = []
    for slot_index, exclusion in enumerate(excluded, start=1):
        language = exclusion["language"]
        start = consumed_by_language[language]
        candidates = language_queues[language][start:start + max_per_slot]
        consumed_by_language[language] += len(candidates)
        compacted = []
        for rank, row in enumerate(candidates, start=1):
            order_hash = sha256((seed + "\0" + row["instance_id"]).encode())
            compacted.append(compact(row, rank=rank, order_hash=order_hash))
        if not compacted:
            raise SystemExit(f"no deterministic replacement candidate for {exclusion['instance_id']}")
        all_candidates.extend(compacted)
        slots.append({
            "slot": slot_index,
            "replaces_instance_id": exclusion["instance_id"],
            "language": language,
            "exclusion_code": exclusion["exclusion_code"],
            "state": "queue_frozen_candidate_content_unopened",
            "queue_capacity_limit": max_per_slot,
            "candidate_count": len(compacted),
            "candidate_queue_sha256": sha256(canonical(compacted)),
            "next_candidate_rank": 1,
            "opened_candidate_count": 0,
            "qualified_replacement_instance_id": None,
            "candidates": compacted,
        })
    if len({row["instance_id"] for row in all_candidates}) != len(all_candidates):
        raise SystemExit("candidate identity reused across slots")
    if len({row["repo"] for row in all_candidates}) != len(all_candidates):
        raise SystemExit("candidate repository reused across slots")
    output = {
        "schema_version": "asi_stack.p2_replacement_queue.v1",
        "recorded_date": "2026-07-17",
        "state": "metadata_only_queue_frozen_candidate_content_unopened",
        "claim_id": diagnosis["claim_id"],
        "policy_path": "evidence_quality/p2_task_qualification_and_replacement_policy.json",
        "resource_ceiling_path": "evidence_quality/p2_resource_ceiling.json",
        "diagnosis_path": "evidence_quality/p2_gold_preflight_diagnosis.json",
        "eligible_metadata_sha256": policy["source"]["eligible_metadata_sha256"],
        "original_development_pool_sha256": policy["source"]["original_development_pool_sha256"],
        "seed": seed,
        "order_key": policy["replacement_rule"]["candidate_order_key"],
        "selection_rule": policy["replacement_rule"]["metadata_eligibility_screen"],
        "slot_count": len(slots),
        "candidate_count": len(all_candidates),
        "unique_candidate_repository_count": len({row["repo"] for row in all_candidates}),
        "slots": slots,
        "queue_sha256": sha256(canonical(slots)),
        "task_text_opened": False,
        "solution_or_test_patch_opened": False,
        "candidate_gold_outcome_opened": False,
        "replacement_qualification_started": False,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "A metadata-only deterministic queue is not a qualified replacement or a benchmark result.",
            "Candidate order does not predict task quality, model performance, governance benefit, or safety.",
            "No candidate task text, patch, test, image outcome, or gold outcome was opened during queue construction.",
            "The final held-out pool remains unselected and unopened."
        ]
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"P2 replacement queue frozen: {len(slots)} slots, {len(all_candidates)} unique repositories; "
        "candidate content and final pool unopened."
    )


if __name__ == "__main__":
    main()
