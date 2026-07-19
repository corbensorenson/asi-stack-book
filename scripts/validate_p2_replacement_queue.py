#!/usr/bin/env python3
"""Validate the frozen metadata-only P2 replacement queues."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
SCHEMA = ROOT / "schemas/p2_replacement_queue.schema.json"
METADATA = ROOT / "experiments/p2_governed_repository_admission/corpus/post_snapshot_eligible_metadata.jsonl"
POOL = ROOT / "experiments/p2_governed_repository_admission/corpus/development_pool.json"
POLICY = ROOT / "evidence_quality/p2_task_qualification_and_replacement_policy.json"
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
DIAGNOSIS = ROOT / "evidence_quality/p2_gold_preflight_diagnosis.json"
DOC = ROOT / "docs/p2_replacement_queue.md"
PERMISSIVE = {"Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0", "ISC", "MIT", "MIT-0", "Unlicense"}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def eligible(row: dict, original_ids: set[str], original_repos: set[str]) -> bool:
    return (
        row["instance_id"] not in original_ids
        and row["repo"] not in original_repos
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


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    slots = record.get("slots", [])
    candidates = [candidate for slot in slots for candidate in slot.get("candidates", [])]
    checks = [
        (record.get("slot_count") == len(slots) == 4, "replacement slot count drifted"),
        (record.get("candidate_count") == len(candidates) == 30, "candidate count drifted"),
        (len({row.get("instance_id") for row in candidates}) == len(candidates), "candidate identity reused"),
        (len({row.get("repo") for row in candidates}) == len(candidates), "candidate repository reused"),
        (record.get("unique_candidate_repository_count") == len(candidates), "unique repository receipt drifted"),
        (record.get("queue_sha256") == digest(canonical(slots)), "aggregate queue digest mismatch"),
        (not record.get("task_text_opened"), "task text was opened during metadata draw"),
        (not record.get("solution_or_test_patch_opened"), "patch content was opened during metadata draw"),
        (not record.get("candidate_gold_outcome_opened"), "candidate gold outcome was opened"),
        (not record.get("replacement_qualification_started"), "qualification was started inside queue freeze"),
        (not record.get("final_pool_selected") and not record.get("final_pool_opened"), "final custody boundary breached"),
        (record.get("support_state_effect") == "none", "queue gained claim support effect"),
    ]
    out.extend(message for passed, message in checks if not passed)
    expected_slots = [
        (1, "aleph-alpha__ts-rs-422", "rust", 9),
        (2, "compose-spec__compose-go-792", "go", 10),
        (3, "gitleaks__gitleaks-1845", "go", 10),
        (4, "thealgorithms__java-6333", "java", 1),
    ]
    for slot, expected in zip(slots, expected_slots):
        number, replaced, language, count = expected
        if (slot.get("slot"), slot.get("replaces_instance_id"), slot.get("language"), slot.get("candidate_count")) != expected:
            out.append(f"slot {number} identity/language/count drifted")
        rows = slot.get("candidates", [])
        if slot.get("candidate_queue_sha256") != digest(canonical(rows)):
            out.append(f"slot {number} queue digest mismatch")
        for rank, row in enumerate(rows, start=1):
            if row.get("rank") != rank:
                out.append(f"slot {number} candidate rank sequence drifted")
            expected_order = digest((record.get("seed", "") + "\0" + row.get("instance_id", "")).encode())
            if row.get("order_sha256") != expected_order:
                out.append(f"slot {number} order hash mismatch: {row.get('instance_id')}")
            if row.get("language") != language:
                out.append(f"slot {number} cross-language candidate")
            if row.get("task_content_opened") or row.get("gold_outcome_opened"):
                out.append(f"slot {number} candidate custody breached")
    if inspect_files:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        resource = json.loads(RESOURCE.read_text(encoding="utf-8"))
        diagnosis = json.loads(DIAGNOSIS.read_text(encoding="utf-8"))
        pool = json.loads(POOL.read_text(encoding="utf-8"))
        if record.get("seed") != policy["replacement_rule"]["seed"]:
            out.append("queue seed drifted from frozen policy")
        if not resource["qualification_state"]["ceiling_frozen"]:
            out.append("resource ceiling was not frozen")
        if record.get("eligible_metadata_sha256") != policy["source"]["eligible_metadata_sha256"]:
            out.append("eligible metadata digest drifted")
        if record.get("original_development_pool_sha256") != policy["source"]["original_development_pool_sha256"]:
            out.append("original pool digest drifted")
        excluded = sorted(
            (row for row in diagnosis["terminal_disposition"]["task_dispositions"] if row["disposition"] == "excluded_replacement_required"),
            key=lambda row: row["instance_id"],
        )
        if [slot.get("replaces_instance_id") for slot in slots] != [row["instance_id"] for row in excluded]:
            out.append("invalid-slot order drifted from diagnosis")
        rows = [json.loads(line) for line in METADATA.read_text(encoding="utf-8").splitlines() if line.strip()]
        original_ids = {row["instance_id"] for row in pool["rows"]}
        original_repos = {row["repo"] for row in pool["rows"]}
        by_language: dict[str, list[dict]] = {}
        for language in {slot["language"] for slot in slots}:
            seen: set[str] = set()
            ordered = []
            for row in sorted(
                (row for row in rows if row["language"] == language and eligible(row, original_ids, original_repos)),
                key=lambda row: digest((record["seed"] + "\0" + row["instance_id"]).encode()),
            ):
                if row["repo"] not in seen:
                    seen.add(row["repo"]); ordered.append(row)
            by_language[language] = ordered
        consumed = {language: 0 for language in by_language}
        for slot in slots:
            language = slot["language"]
            start = consumed[language]
            expected = by_language[language][start:start + 10]
            consumed[language] += len(expected)
            if [row["instance_id"] for row in slot["candidates"]] != [row["instance_id"] for row in expected]:
                out.append(f"slot {slot['slot']} is not the deterministic metadata queue")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in ["candidate content and final pool unopened", "without outcome-aware skipping", "is not qualifying a task", "final held-out pool remains unselected and unopened"]:
            if phrase not in doc:
                out.append(f"queue receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("slot order swap", lambda r: r["slots"].__setitem__(slice(0, 2), [r["slots"][1], r["slots"][0]]))
    add("seed drift", lambda r: r.__setitem__("seed", r["seed"] + "x"))
    add("content opened", lambda r: r.__setitem__("task_text_opened", True))
    add("candidate skipped", lambda r: r["slots"][0].__setitem__("next_candidate_rank", 2))
    add("duplicate repo", lambda r: r["slots"][1]["candidates"][0].__setitem__("repo", r["slots"][0]["candidates"][0]["repo"]))
    add("cross language", lambda r: r["slots"][0]["candidates"][0].__setitem__("language", "go"))
    add("queue digest drift", lambda r: r.__setitem__("queue_sha256", "0" * 64))
    add("slot digest drift", lambda r: r["slots"][0].__setitem__("candidate_queue_sha256", "0" * 64))
    add("gold opened", lambda r: r["slots"][0]["candidates"][0].__setitem__("gold_outcome_opened", True))
    add("final selected", lambda r: r.__setitem__("final_pool_selected", True))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    add("candidate removed", lambda r: r["slots"][0]["candidates"].pop(0))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 replacement queue failed:\n - " + "\n - ".join(out))
    print("P2 replacement queue passed: 4 slots, 30 deterministic unique repositories, metadata-only custody, final pool closed; 12/12 mutations rejected.")


if __name__ == "__main__":
    main()
