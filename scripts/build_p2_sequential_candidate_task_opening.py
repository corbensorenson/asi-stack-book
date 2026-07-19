#!/usr/bin/env python3
"""Open one sequential replacement task only after provenance and image gates pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/tmp/swe-rebench-v2.parquet")
SOURCE_SHA = "0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad"
QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def sha_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def diff_paths(diff: str | None) -> list[str]:
    return sorted({path for match in re.finditer(r"^diff --git a/(.+?) b/(.+)$", diff or "", re.MULTILINE) for path in match.groups()})


def load_row(instance_id: str) -> dict:
    parquet = pq.ParquetFile(SOURCE)
    for group in range(parquet.num_row_groups):
        ids = parquet.read_row_group(group, columns=["instance_id"])["instance_id"].to_pylist()
        if instance_id in ids:
            for row in parquet.read_row_group(group).to_pylist():
                if row["instance_id"] == instance_id:
                    return row
    raise SystemExit(f"source row missing: {instance_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--image-result", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = ROOT / args.output
    if output.exists():
        raise SystemExit(f"immutable opening record exists: {output}")
    if sha_file(SOURCE) != SOURCE_SHA:
        raise SystemExit("source parquet digest drift")

    provenance = json.loads((ROOT / args.provenance).read_text())
    image_result = json.loads((ROOT / args.image_result).read_text())
    queue = json.loads(QUEUE.read_text())
    candidate = provenance["candidate"]
    if provenance["state"] != "passed_before_task_content_opened" or image_result["state"] != "passed":
        raise SystemExit("provenance/image gate did not pass")
    if image_result["instance_id"] != candidate["instance_id"] or image_result["manifest_digest"] != candidate["image_manifest"]["digest"]:
        raise SystemExit("provenance/image identity drift")
    queued = queue["slots"][candidate["slot"] - 1]["candidates"][candidate["rank"] - 1]
    if queued["instance_id"] != candidate["instance_id"]:
        raise SystemExit("candidate is not at the declared frozen queue position")

    row = load_row(candidate["instance_id"])
    for key in ("repo", "base_commit", "language", "license", "image_name"):
        if row[key] != queued[key]:
            raise SystemExit(f"source/queue drift: {key}")
    for source_key, digest_key in (("problem_statement", "problem_statement_sha256"), ("patch", "solution_patch_sha256"), ("test_patch", "test_patch_sha256")):
        if sha_text(row[source_key] or "") != queued[digest_key]:
            raise SystemExit(f"source/queue digest drift: {source_key}")
    compact_command = row.get("test_cmd", row["install_config"]["test_cmd"])
    if not isinstance(compact_command, str) or sha_text(compact_command) != queued["test_command_sha256"]:
        raise SystemExit("source/queue test-command digest drift")

    solution_paths = diff_paths(row["patch"])
    test_paths = diff_paths(row["test_patch"])
    overlap = sorted(set(solution_paths) & set(test_paths))
    fail_to_pass = sorted(row.get("FAIL_TO_PASS") or [])
    pass_to_pass = sorted(row.get("PASS_TO_PASS") or [])
    record = {
        "schema_version": "asi_stack.p2_sequential_candidate_task_opening.v1",
        "recorded_date": "2026-07-17",
        "state": "task_spec_opened_outcome_unopened",
        "claim_id": provenance["claim_id"],
        "source_parquet_sha256": SOURCE_SHA,
        "queue_path": "experiments/p2_governed_repository_admission/corpus/replacement_queue.json",
        "provenance_path": args.provenance,
        "image_result_path": args.image_result,
        "candidate": {
            "slot": candidate["slot"],
            "rank": candidate["rank"],
            "instance_id": row["instance_id"],
            "repo": row["repo"],
            "base_commit": row["base_commit"],
            "language": row["language"],
            "license": row["license"],
            "image_name": row["image_name"],
            "image_manifest_digest": candidate["image_manifest"]["digest"],
            "log_parser": row["install_config"]["log_parser"],
            "test_command": row["install_config"]["test_cmd"],
            "test_command_sha256": queued["test_command_sha256"],
            "problem_statement_sha256": queued["problem_statement_sha256"],
            "solution_patch_sha256": queued["solution_patch_sha256"],
            "test_patch_sha256": queued["test_patch_sha256"],
            "solution_paths": solution_paths,
            "test_paths": test_paths,
            "solution_test_path_overlap": overlap,
            "fail_to_pass_count": len(fail_to_pass),
            "pass_to_pass_count": len(pass_to_pass),
            "expected_test_count": len(fail_to_pass) + len(pass_to_pass),
            "fail_to_pass_set_sha256": sha_json(fail_to_pass),
            "pass_to_pass_set_sha256": sha_json(pass_to_pass),
        },
        "opening_gates": {
            "source_queue_digests_match": True,
            "solution_test_path_disjoint": not overlap,
            "independent_evaluator_calibrated_before_opening": True,
            "task_spec_opened": True,
            "candidate_execution_started": False,
            "candidate_outcome_opened": False,
            "final_pool_selected": False,
            "final_pool_opened": False
        },
        "next_gate": "execute the unchanged offline dependency qualification; if packaging fails, use only the prospectively frozen checksum-snapshot rescue",
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "Opening a development task specification does not qualify the task.",
            "Expected test identities are bound by count and digest but have not yet been observed.",
            "No execution outcome or held-out task was opened.",
            "No mechanism support or refutation follows from task opening."
        ]
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"{candidate['instance_id']}: task spec opened; {record['candidate']['expected_test_count']} expected identities; outcome unopened.")


if __name__ == "__main__":
    main()
