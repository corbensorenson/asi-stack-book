#!/usr/bin/env python3
"""Validate the P2 fixed-denominator gold-preflight diagnosis."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence_quality/p2_gold_preflight_diagnosis.json"
SCHEMA = ROOT / "schemas/p2_gold_preflight_diagnosis.schema.json"
DOC = ROOT / "docs/p2_gold_preflight_diagnosis.md"
POLICY = ROOT / "evidence_quality/p2_task_qualification_and_replacement_policy.json"
FULL = ROOT / "experiments/p2_governed_repository_admission/gold_preflight/result.json"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    terminal = record.get("terminal_disposition", {})
    dispositions = terminal.get("task_dispositions", [])
    ids = [row.get("instance_id") for row in dispositions]
    qualified = [row for row in dispositions if row.get("disposition") == "development_gold_oracle_qualified"]
    excluded = [row for row in dispositions if row.get("disposition") == "excluded_replacement_required"]
    if len(ids) != 12 or len(set(ids)) != 12:
        out.append("twelve unique original tasks are not dispositioned")
    if len(qualified) != 8 or len(excluded) != 4:
        out.append("8/4 qualified/excluded split drifted")
    if any(row.get("negative_inference_level") != "N0" or row.get("claim_effect") != "none" for row in excluded):
        out.append("excluded task was promoted above N0 or gained claim effect")
    if any(row.get("claim_effect") != "none" for row in qualified):
        out.append("development qualification gained claim effect")
    if len({row.get("exclusion_code") for row in excluded}) != 4:
        out.append("distinct exclusion diagnoses collapsed")
    findings = record.get("false_negative_findings", {})
    if findings.get("idea_or_mechanism_negative_inference_count") != 0:
        out.append("instrument failures were converted into mechanism inference")
    custody = record.get("custody_and_raw_evidence", {})
    if custody.get("final_pool_selected") is not False or custody.get("final_pool_opened") is not False:
        out.append("final pool custody opened")
    if custody.get("raw_log_custody_required_after_abort") is not True:
        out.append("raw-log correction after abort was removed")
    resource = record.get("resource_observations", {})
    if resource.get("resource_gate_state") != "pending_peak_memory_cpu_and_frozen_ceiling_before_replacement_draw":
        out.append("resource gate was prematurely passed")
    next_action = record.get("next_required_action", {})
    for key in ["resource_ceiling_must_be_frozen_before_draw", "rerun_two_repetitions_after_replacement", "independent_specification_review_still_required"]:
        if next_action.get(key) is not True:
            out.append(f"required next action weakened: {key}")
    if next_action.get("replacement_draw_started") is not True or next_action.get("replacement_task_count_required") != 4:
        out.append("replacement custody/count drifted")
    if inspect_files:
        full = json.loads(FULL.read_text(encoding="utf-8"))
        full_ids = {row["instance_id"] for row in full["tasks"]}
        if set(ids) != full_ids or full.get("passed_task_count") != 7 or full.get("task_count") != 12:
            out.append("diagnosis no longer covers the fixed original denominator")
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        if policy.get("replacement_rule", {}).get("replacement_draw_state") != "metadata_queue_frozen_candidate_content_unopened":
            out.append("replacement policy does not record the frozen metadata queue")
        for row in dispositions:
            path_text = row.get("decisive_attempt")
            if path_text and not (ROOT / path_text).is_file():
                out.append(f"decisive attempt missing: {path_text}")
        for row in record.get("attempt_lineage", []):
            path = ROOT / row.get("path", "")
            if not path.is_file() or row.get("claim_effect") != "none":
                out.append(f"attempt lineage invalid: {row.get('id')}")
        verified = 0
        for path in (ROOT / "experiments/p2_governed_repository_admission").rglob("*.log.gz"):
            try:
                with gzip.open(path, "rt", encoding="utf-8") as handle:
                    sha256_text(handle.read())
                verified += 1
            except (OSError, UnicodeError):
                out.append(f"unreadable compressed log: {path.relative_to(ROOT)}")
        if verified < custody.get("verified_compressed_arm_log_count", 0) + custody.get("verified_dependency_preparation_log_count", 0):
            out.append("retained compressed-log count is below the diagnosis receipt")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in [
            "four replacements required",
            "N0 exclusions with no claim effect",
            "smaller favorable denominator",
            "62 compressed arm logs",
            "resource gate is still open",
            "final pool remains unselected",
        ]:
            if phrase not in doc:
                out.append(f"diagnosis receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("nine qualified", lambda r: r["terminal_disposition"].__setitem__("qualified_task_count", 9))
    add("three replacements", lambda r: r["terminal_disposition"].__setitem__("replacement_slot_count", 3))
    add("exclusion promoted", lambda r: next(row for row in r["terminal_disposition"]["task_dispositions"] if row["disposition"] == "excluded_replacement_required").__setitem__("negative_inference_level", "N3"))
    add("claim effect", lambda r: next(row for row in r["terminal_disposition"]["task_dispositions"] if row["disposition"] == "excluded_replacement_required").__setitem__("claim_effect", "refutation"))
    add("mechanism negative", lambda r: r["false_negative_findings"].__setitem__("idea_or_mechanism_negative_inference_count", 1))
    add("attempt erased", lambda r: r["attempt_lineage"].pop())
    add("raw logs optional", lambda r: r["custody_and_raw_evidence"].__setitem__("raw_log_custody_required_after_abort", False))
    add("final selected", lambda r: r["custody_and_raw_evidence"].__setitem__("final_pool_selected", True))
    add("resource gate passed", lambda r: r["resource_observations"].__setitem__("resource_gate_state", "passed"))
    add("replacement draw erased", lambda r: r["next_required_action"].__setitem__("replacement_draw_started", False))
    add("single repetition", lambda r: r["next_required_action"].__setitem__("rerun_two_repetitions_after_replacement", False))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 gold-preflight diagnosis failed:\n - " + "\n - ".join(out))
    print("P2 gold-preflight diagnosis passed: 12/12 original tasks dispositioned, 8 qualified, 4 N0 replacements, 62 arm logs, 8 attempts, final pool closed; 12/12 mutations rejected.")


if __name__ == "__main__":
    main()
