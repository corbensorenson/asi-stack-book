#!/usr/bin/env python3
"""Validate rank-one public-change, license, and image-manifest receipts."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence_quality/p2_replacement_provenance_preflight.json"
SCHEMA = ROOT / "schemas/p2_replacement_provenance_preflight.schema.json"
QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
DOC = ROOT / "docs/p2_replacement_provenance_preflight.md"


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    rows = record.get("candidates", [])
    custody = record.get("custody", {})
    if [row.get("slot") for row in rows] != [1, 2, 3, 4]: out.append("slot order drifted")
    if len({row.get("repo") for row in rows}) != 4: out.append("candidate repository reused")
    for row in rows:
        public = row.get("public_change", {})
        if row.get("base_commit") not in public.get("merge_commit_parent_shas", []): out.append(f"base is not merge parent: {row.get('instance_id')}")
        if not public.get("merged") or not public.get("github_signature_verified"): out.append(f"public merge receipt failed: {row.get('instance_id')}")
        if not row.get("license_receipt", {}).get("bound_to_base_commit"): out.append(f"license not base-bound: {row.get('instance_id')}")
        if not row.get("image_manifest", {}).get("expanded_size_unmeasured"): out.append(f"manifest preflight overclaims expanded size: {row.get('instance_id')}")
    checks = [
        (record.get("passed_candidate_count") == 4, "passed count drifted"),
        (custody.get("dataset_problem_statement_opened") is False, "problem statement opened"),
        (custody.get("dataset_solution_patch_opened") is False, "solution patch opened"),
        (custody.get("dataset_test_patch_opened") is False, "test patch opened"),
        (custody.get("test_command_opened") is False, "test command opened"),
        (custody.get("image_pulled") is False, "image pull laundered into manifest preflight"),
        (custody.get("candidate_gold_outcome_opened") is False, "gold outcome opened"),
        (custody.get("public_title_level_metadata_incidentally_visible") is True, "incidental title exposure erased"),
        (custody.get("replacement_qualification_started") is False, "qualification started prematurely"),
        (custody.get("final_pool_selected") is False and custody.get("final_pool_opened") is False, "final custody breached"),
        (record.get("support_state_effect") == "none", "preflight promoted support"),
    ]
    out.extend(message for passed, message in checks if not passed)
    if inspect_files:
        queue = json.loads(QUEUE.read_text(encoding="utf-8"))
        expected = [slot["candidates"][0] for slot in queue["slots"]]
        for row, source in zip(rows, expected):
            for key in ["instance_id", "repo", "language", "base_commit"]:
                if row.get(key) != source.get(key): out.append(f"rank-one queue mismatch {key}: {row.get('instance_id')}")
            if row.get("image_manifest", {}).get("image") != source.get("image_name"): out.append(f"image name drift: {row.get('instance_id')}")
            if row.get("license_receipt", {}).get("spdx_id") != source.get("license"): out.append(f"license drift: {row.get('instance_id')}")
        java = rows[3].get("public_change", {}) if len(rows) == 4 else {}
        if java.get("pull_api_available") is not False or java.get("receipt_mode") != "verified_github_merge_commit_fallback_pr_endpoint_unavailable": out.append("Java fallback receipt was misrepresented")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in ["Java pull endpoint returns unavailable", "expanded image sizes", "title-level metadata", "unselected and unopened"]:
            if phrase not in doc: out.append(f"preflight receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("base detached", lambda r: r["candidates"][0]["public_change"].__setitem__("merge_commit_parent_shas", ["0" * 40]))
    add("signature unverified", lambda r: r["candidates"][0]["public_change"].__setitem__("github_signature_verified", False))
    add("license unbound", lambda r: r["candidates"][0]["license_receipt"].__setitem__("bound_to_base_commit", False))
    add("wrong architecture", lambda r: r["candidates"][0]["image_manifest"].__setitem__("architecture", "arm64"))
    add("expanded size invented", lambda r: r["candidates"][0]["image_manifest"].__setitem__("expanded_size_unmeasured", False))
    add("problem opened", lambda r: r["custody"].__setitem__("dataset_problem_statement_opened", True))
    add("title exposure erased", lambda r: r["custody"].__setitem__("public_title_level_metadata_incidentally_visible", False))
    add("qualification started", lambda r: r["custody"].__setitem__("replacement_qualification_started", True))
    add("final opened", lambda r: r["custody"].__setitem__("final_pool_opened", True))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False): out.append(f"negative mutation accepted: {label}")
    if out: raise SystemExit("P2 replacement provenance preflight failed:\n - " + "\n - ".join(out))
    print("P2 replacement provenance preflight passed: 4/4 rank-one public merges, base-bound licenses, digest manifests; task content/outcomes/final pool closed; 10/10 mutations rejected.")


if __name__ == "__main__": main()
