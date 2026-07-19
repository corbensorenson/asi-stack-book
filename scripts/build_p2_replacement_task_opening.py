#!/usr/bin/env python3
"""Open rank-one replacement task specs after provenance/resource gates pass."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/tmp/swe-rebench-v2.parquet")
QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
PROVENANCE = ROOT / "evidence_quality/p2_replacement_provenance_preflight.json"
RESOURCE_RESULT = ROOT / "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r2/result.json"
OUT = ROOT / "evidence_quality/p2_replacement_task_opening.json"
SOURCE_SHA = "0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad"


def sha_bytes(value: bytes) -> str: return hashlib.sha256(value).hexdigest()
def sha_text(value: str) -> str: return sha_bytes(value.encode())
def sha_json(value: object) -> str: return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def diff_paths(diff: str | None) -> list[str]:
    return sorted({path for match in re.finditer(r"^diff --git a/(.+?) b/(.+)$", diff or "", re.MULTILINE) for path in match.groups()})


def load_rows(ids: set[str]) -> dict[str, dict]:
    parquet = pq.ParquetFile(SOURCE); rows = {}
    for group in range(parquet.num_row_groups):
        group_ids = parquet.read_row_group(group, columns=["instance_id"])["instance_id"].to_pylist()
        if ids.intersection(group_ids):
            for row in parquet.read_row_group(group).to_pylist():
                if row["instance_id"] in ids: rows[row["instance_id"]] = row
    if set(rows) != ids: raise SystemExit(f"source rows missing: {sorted(ids - set(rows))}")
    return rows


def main() -> None:
    if sha_bytes(SOURCE.read_bytes()) != SOURCE_SHA: raise SystemExit("source parquet digest mismatch")
    queue = json.loads(QUEUE.read_text()); provenance = json.loads(PROVENANCE.read_text()); resource = json.loads(RESOURCE_RESULT.read_text())
    if provenance["passed_candidate_count"] != 4 or resource["passed_candidate_count"] != 4: raise SystemExit("pre-opening provenance/resource gate failed")
    selected = [slot["candidates"][0] for slot in queue["slots"]]; rows = load_rows({row["instance_id"] for row in selected})
    opened = []
    for slot, candidate in zip(queue["slots"], selected):
        row = rows[candidate["instance_id"]]
        for key in ["base_commit", "repo", "language", "license", "image_name"]:
            if row[key] != candidate[key]: raise SystemExit(f"metadata drift {key}: {candidate['instance_id']}")
        if sha_text(row["problem_statement"] or "") != candidate["problem_statement_sha256"]: raise SystemExit("problem digest drift")
        if sha_text(row["patch"] or "") != candidate["solution_patch_sha256"]: raise SystemExit("solution digest drift")
        if sha_text(row["test_patch"] or "") != candidate["test_patch_sha256"]: raise SystemExit("test digest drift")
        solution_paths = diff_paths(row["patch"]); test_paths = diff_paths(row["test_patch"]); overlap = sorted(set(solution_paths) & set(test_paths))
        if overlap: raise SystemExit(f"solution/test collision: {candidate['instance_id']}: {overlap}")
        test_cmd = row["install_config"]["test_cmd"]
        compact_test_cmd = row.get("test_cmd", test_cmd)
        if not isinstance(compact_test_cmd, str) or sha_text(compact_test_cmd) != candidate["test_command_sha256"]: raise SystemExit(f"test command digest drift: {candidate['instance_id']}")
        f2p = sorted(row.get("FAIL_TO_PASS") or []); p2p = sorted(row.get("PASS_TO_PASS") or [])
        opened.append({
            "slot": slot["slot"], "rank": 1, "instance_id": candidate["instance_id"], "repo": row["repo"], "base_commit": row["base_commit"], "language": row["language"], "license": row["license"], "image_name": row["image_name"],
            "log_parser": row["install_config"]["log_parser"], "test_command": test_cmd, "test_command_sha256": candidate["test_command_sha256"],
            "problem_statement_sha256": candidate["problem_statement_sha256"], "solution_patch_sha256": candidate["solution_patch_sha256"], "test_patch_sha256": candidate["test_patch_sha256"],
            "solution_paths": solution_paths, "test_paths": test_paths, "solution_test_path_overlap": overlap,
            "fail_to_pass_count": len(f2p), "pass_to_pass_count": len(p2p), "expected_test_count": len(f2p) + len(p2p), "fail_to_pass_set_sha256": sha_json(f2p), "pass_to_pass_set_sha256": sha_json(p2p),
            "task_spec_opened": True, "execution_outcome_opened": False
        })
    output = {
        "schema_version": "asi_stack.p2_replacement_task_opening.v1", "recorded_date": "2026-07-17",
        "state": "rank_one_task_specs_opened_evaluator_calibration_pending_outcomes_unopened", "claim_id": "p2.governed_natural_repository_change_admission_joint_frontier",
        "source_parquet_sha256": SOURCE_SHA, "queue_path": "experiments/p2_governed_repository_admission/corpus/replacement_queue.json",
        "provenance_preflight_path": "evidence_quality/p2_replacement_provenance_preflight.json", "resource_result_path": "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r2/result.json",
        "opened_candidate_count": 4, "candidates": opened,
        "custody": {"rank_one_task_specs_opened": True, "problem_statement_solution_patch_test_patch_and_command_read": True, "candidate_execution_started": False, "candidate_baseline_outcome_opened": False, "candidate_gold_outcome_opened": False, "rank_greater_than_one_task_content_opened": False, "final_pool_selected": False, "final_pool_opened": False},
        "next_gate": "calibrate_independently_implemented_log_evaluator_before_any_candidate_execution",
        "support_state_effect": "none", "release_effect": "none",
        "non_claims": ["Opening a development task specification is not qualifying it.", "Expected test identities are bound by count and digest but do not establish that the image can observe them.", "No candidate execution outcome or final held-out task was opened.", "No coding, governance, safety, transfer, SOTA, release, AGI, or ASI result follows."]
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print("P2 rank-one task opening: 4 specs digest-bound; evaluator calibration pending; outcomes and final pool unopened.")


if __name__ == "__main__": main()
