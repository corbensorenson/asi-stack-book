#!/usr/bin/env python3
"""Validate P2 rank-one image resource preflight and failed-attempt custody."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r1/result.json"
R2 = ROOT / "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r2/result.json"
SCHEMA = ROOT / "schemas/p2_replacement_image_resource_preflight.schema.json"
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
PROVENANCE = ROOT / "evidence_quality/p2_replacement_provenance_preflight.json"
DOC = ROOT / "docs/p2_replacement_image_resource_preflight.md"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record): out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    rows = record.get("candidates", [])
    if [row.get("slot") for row in rows] != [1, 2, 3, 4]: out.append("slot order drifted")
    if record.get("campaign_post_cleanup_host_free_byte_loss") != max(0, record.get("campaign_host_free_before_bytes", 0) - record.get("campaign_host_free_after_bytes", 0)): out.append("campaign residual arithmetic drifted")
    for row in rows:
        digest = row.get("manifest_digest", "")
        if row.get("immutable_ref", "").split("@")[-1] != digest: out.append(f"immutable ref digest mismatch: {row.get('instance_id')}")
        if not any(item.endswith(digest) for item in row.get("repo_digests", [])): out.append(f"inspected repo digest mismatch: {row.get('instance_id')}")
        gates = row.get("gates", {})
        if set(gates) != {"pull_exit_zero", "pull_within_seconds", "pull_not_timed_out", "inspect_exit_zero", "manifest_digest_present", "linux_amd64", "expanded_size_within_bytes", "cleanup_exit_zero", "post_cleanup_loss_within_bytes"}: out.append(f"gate set drifted: {row.get('instance_id')}")
        if not all(gates.values()) or not row.get("resource_gate_pass"): out.append(f"resource gate did not pass: {row.get('instance_id')}")
    checks = [
        (record.get("passed_candidate_count") == len(rows) == 4, "pass denominator drifted"),
        (record.get("failed_candidate_count") == 0, "failure count drifted"),
        (record.get("campaign_residual_gate_pass") is True, "campaign residual gate failed"),
        (record.get("task_content_opened") is False, "task content opened"),
        (record.get("candidate_outcome_opened") is False, "candidate outcome opened"),
        (record.get("replacement_qualification_started") is False, "qualification started"),
        (record.get("final_pool_selected") is False and record.get("final_pool_opened") is False, "final custody breached"),
        (record.get("support_state_effect") == "none", "resource preflight promoted support"),
    ]
    out.extend(message for passed, message in checks if not passed)
    if inspect_files:
        resource = json.loads(RESOURCE.read_text(encoding="utf-8")); ceilings = resource["task_acceptance_ceilings"]
        provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        for row, source in zip(rows, provenance["candidates"]):
            if row.get("instance_id") != source.get("instance_id") or row.get("image") != source["image_manifest"]["image"] or row.get("manifest_digest") != source["image_manifest"]["digest"]: out.append(f"provenance candidate drift: {row.get('instance_id')}")
            if row.get("pull_wall_seconds", 10**9) > ceilings["image_pull_seconds"]: out.append(f"pull ceiling breached: {row.get('instance_id')}")
            if row.get("expanded_image_size_bytes", 10**30) > ceilings["expanded_image_bytes"]: out.append(f"size ceiling breached: {row.get('instance_id')}")
            if row.get("post_cleanup_host_free_byte_loss", 10**30) > ceilings["maximum_post_cleanup_host_free_byte_loss"]: out.append(f"task residual breached: {row.get('instance_id')}")
            for kind in ["pull", "cleanup"]:
                path = ROOT / row.get(f"{kind}_log_path", "")
                if not path.is_file() or file_digest(path) != row.get(f"{kind}_log_sha256"): out.append(f"raw {kind} log custody failed: {row.get('instance_id')}")
        if record.get("campaign_post_cleanup_host_free_byte_loss", 10**30) > resource["campaign_ceilings"]["maximum_cumulative_host_free_byte_loss"]: out.append("campaign residual ceiling breached")
        r1 = json.loads(R1.read_text(encoding="utf-8"))
        if r1.get("state") != "aborted_instrument_failure_after_all_pull_cleanup_cycles" or r1.get("negative_inference_level") != "N0" or r1.get("claim_effect") != "none" or r1.get("measurement_recovery_allowed") is not False: out.append("R1 instrument failure disposition drifted")
        if r1.get("raw_log_count") != 8 or len(r1.get("raw_logs", [])) != 8: out.append("R1 raw-log denominator drifted")
        for receipt in r1.get("raw_logs", []):
            path = ROOT / receipt.get("path", "")
            if not path.is_file() or file_digest(path) != receipt.get("sha256"): out.append(f"R1 raw log custody failed: {receipt.get('path')}")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in ["N0 with no candidate or claim effect", "clean R2 run", "7,577,923,584", "passes only image-resource feasibility", "unselected and unopened"]:
            if phrase not in doc: out.append(f"resource receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(R2.read_text(encoding="utf-8")); out = failures(record)
    mutations = []
    def add(label, edit): candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("pull timeout", lambda r: r["candidates"][0].__setitem__("pull_timeout", True))
    add("pull over ceiling", lambda r: r["candidates"][0].__setitem__("pull_wall_seconds", 301))
    add("size over ceiling", lambda r: r["candidates"][0].__setitem__("expanded_image_size_bytes", 1500000001))
    add("wrong digest", lambda r: r["candidates"][0].__setitem__("manifest_digest", "sha256:" + "0" * 64))
    add("cleanup failure", lambda r: r["candidates"][0].__setitem__("cleanup_exit_code", 1))
    add("task residual over ceiling", lambda r: r["candidates"][0].__setitem__("post_cleanup_host_free_byte_loss", 5368709121))
    add("campaign arithmetic drift", lambda r: r.__setitem__("campaign_post_cleanup_host_free_byte_loss", 0))
    add("gate removed", lambda r: r["candidates"][0]["gates"].pop("linux_amd64"))
    add("task content opened", lambda r: r.__setitem__("task_content_opened", True))
    add("qualification started", lambda r: r.__setitem__("replacement_qualification_started", True))
    add("final opened", lambda r: r.__setitem__("final_pool_opened", True))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False): out.append(f"negative mutation accepted: {label}")
    if out: raise SystemExit("P2 replacement image resource preflight failed:\n - " + "\n - ".join(out))
    print("P2 replacement image resource preflight passed: R1 retained N0, R2 4/4 digest pulls/sizes/cleanup/residuals passed, task content/final pool closed; 12/12 mutations rejected.")


if __name__ == "__main__": main()
