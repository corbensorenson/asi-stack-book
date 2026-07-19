#!/usr/bin/env python3
"""Validate the P2 natural development-corpus preflight and custody boundary."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "evidence_quality/p2_development_corpus_preflight.json"
SCHEMA = ROOT / "schemas/p2_development_corpus_preflight.schema.json"
POOL = ROOT / "experiments/p2_governed_repository_admission/corpus/development_pool.json"
METADATA = ROOT / "experiments/p2_governed_repository_admission/corpus/post_snapshot_eligible_metadata.jsonl"
IMAGES = ROOT / "experiments/p2_governed_repository_admission/corpus/image_manifest_receipts.json"
DOC = ROOT / "docs/p2_development_corpus_preflight.md"
INVENTORY = ROOT / "sources/source_inventory.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def failures(bundle: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    summary, pool, images = bundle["summary"], bundle["pool"], bundle["images"]
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(summary):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    rows = pool.get("rows", [])
    ids = [row.get("instance_id") for row in rows]
    if len(rows) != 12 or len(set(ids)) != 12:
        out.append("development pool must contain 12 unique tasks")
    if len({row.get("repo") for row in rows}) != 12 or len({row.get("language") for row in rows}) != 7:
        out.append("development repository/language diversity drifted")
    forbidden = {"problem_statement", "patch", "test_patch", "test_cmd", "FAIL_TO_PASS", "PASS_TO_PASS"}
    if any(forbidden & set(row) for row in rows):
        out.append("development record leaked task text, patch, tests, or outcomes")
    if any(row.get("role") != "development_only_not_final" for row in rows):
        out.append("development-only role drifted")
    if pool.get("final_pool_selected") is not False or pool.get("final_pool_opened") is not False:
        out.append("final pool was selected or opened")
    expected_pool_sha = sha256_bytes(canonical_json(rows))
    if summary.get("development_pool", {}).get("pool_sha256") != expected_pool_sha:
        out.append("development pool digest drifted")
    receipts = images.get("receipts", [])
    if images.get("image_count") != 12 or images.get("all_available") is not True:
        out.append("all twelve development manifests must resolve")
    if {row.get("instance_id") for row in receipts} != set(ids):
        out.append("image receipt/task identity mismatch")
    for row in receipts:
        if row.get("platform") != {"architecture": "amd64", "os": "linux"}:
            out.append("unexpected image platform")
        if row.get("manifest_digest", "").removeprefix("sha256:") != row.get("raw_manifest_sha256"):
            out.append("manifest digest/raw receipt mismatch")
    if images.get("final_pool_selected") is not False or images.get("final_pool_opened") is not False:
        out.append("image probe widened to final pool")
    if summary.get("preflight_effect", {}).get("support_state_effect") != "none":
        out.append("corpus preflight cannot promote support")
    if inspect_files:
        text = METADATA.read_bytes()
        lines = [json.loads(line) for line in text.splitlines() if line.strip()]
        if len(lines) != 1117 or len({row["instance_id"] for row in lines}) != 1117:
            out.append("eligible metadata denominator drifted")
        if sha256_bytes(text) != summary.get("eligible_universe", {}).get("metadata_sha256"):
            out.append("eligible metadata digest drifted")
        if any(forbidden & set(row) for row in lines):
            out.append("eligible metadata leaked task text, patch, tests, or outcomes")
        inventory = {row["id"] for row in json.loads(INVENTORY.read_text(encoding="utf-8"))}
        if "ext_swe_rebench_v2_2026" not in inventory:
            out.append("SWE-rebench V2 source missing from inventory")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in [
            "qualified for development only; final denominator unselected and closed",
            "1,117 tasks", "532 repositories", "seven languages",
            "does not prove contamination absence", "gold",
            "creates no benchmark result",
        ]:
            if phrase not in doc:
                out.append(f"preflight receipt missing boundary: {phrase}")
    return out


def main() -> None:
    bundle = {
        "summary": json.loads(SUMMARY.read_text(encoding="utf-8")),
        "pool": json.loads(POOL.read_text(encoding="utf-8")),
        "images": json.loads(IMAGES.read_text(encoding="utf-8")),
    }
    out = failures(bundle)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(bundle); edit(candidate); mutations.append((label, candidate))
    add("eligible denominator drift", lambda b: b["summary"]["eligible_universe"].__setitem__("row_count", 1116))
    add("license screen erased", lambda b: b["summary"]["development_pool"].__setitem__("all_permissive_license", False))
    add("task content leaked", lambda b: b["pool"]["rows"][0].__setitem__("problem_statement", "hidden"))
    add("final selected", lambda b: b["pool"].__setitem__("final_pool_selected", True))
    add("final opened", lambda b: b["pool"].__setitem__("final_pool_opened", True))
    add("image missing", lambda b: b["images"].__setitem__("all_available", False))
    add("image identity drift", lambda b: b["images"]["receipts"][0].__setitem__("instance_id", "other"))
    add("manifest digest drift", lambda b: b["images"]["receipts"][0].__setitem__("raw_manifest_sha256", "0" * 64))
    add("contamination overclaim", lambda b: b["summary"]["contamination_boundary"].__setitem__("claim", "proven_absent"))
    add("support promotion", lambda b: b["summary"]["preflight_effect"].__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 development-corpus preflight failed:\n - " + "\n - ".join(out))
    print("P2 development-corpus preflight passed: 1,117 post-snapshot tasks; 12-repository, 7-language development pool; 12 manifests; final pool closed; 10/10 mutations rejected.")


if __name__ == "__main__":
    main()
