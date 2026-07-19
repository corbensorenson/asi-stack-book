#!/usr/bin/env python3
"""Validate the prospective P2 infrastructure/content freeze boundary."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence_quality/p2_infrastructure_content_freeze_amendment.json"
SCHEMA = ROOT / "schemas/p2_infrastructure_content_freeze_amendment.schema.json"
DOC = ROOT / "docs/p2_infrastructure_materialization_and_content_freeze_amendment.md"


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    out.extend(
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(record)
    )
    setup = record.get("infrastructure_phase", {})
    boundary = record.get("protected_content_boundary", {})
    history = record.get("historical_reconciliation", {})
    capacity = record.get("current_capacity", {})
    custody = record.get("campaign_disposition_custody", {})
    checks = [
        (setup.get("protected_task_content_may_be_opened") is False, "setup may expose protected content"),
        (setup.get("bounded_attempts_per_exact_artifact_and_failure_class") == 3, "retry budget drifted"),
        (setup.get("selection_may_condition_on_pull_speed") is False, "pull-speed selection allowed"),
        (setup.get("retry_exhaustion_effect") == "block_pool_do_not_advance_rank", "setup failure burns rank"),
        (boundary.get("after_trigger_no_rerun") is True, "post-content rerun allowed"),
        (boundary.get("after_trigger_no_retry_budget_change") is True, "post-content retry budget mutable"),
        (len(boundary.get("protected_surfaces", [])) == 8, "protected-content surface incomplete"),
        (history.get("rank_4") == "content_exposed_irrevocable", "rank 4 history weakened"),
        (history.get("rank_5") == "no_content_exposed_infrastructure_retry_pending", "rank 5 not reinstated"),
        (history.get("rank_6_may_open") is False, "rank 6 may open before pool gate"),
        (capacity.get("pool_wide_materialization_demonstrated") is False, "pool readiness falsely claimed"),
        (capacity.get("slot_1_state") == "blocked_at_pool_wide_infrastructure_gate", "slot 1 state overstated"),
        (custody.get("commit_required_before_counting") is True, "commit custody optional"),
        (custody.get("validator") == "scripts/validate_evidence_git_custody.py", "custody validator drifted"),
        (record.get("support_state_effect") == "none", "support promotion requested"),
    ]
    out.extend(message for passed, message in checks if not passed)
    if inspect_files:
        for relative in record.get("immutable_history", []):
            if not (ROOT / relative).exists():
                out.append(f"missing immutable history: {relative}")
        text = DOC.read_text(encoding="utf-8")
        for phrase in ["protected task content", "at most three attempts", "does not advance the rank", "rank 6 must remain unopened", "committed before it counts"]:
            if phrase not in text:
                out.append(f"amendment prose missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("unbounded retry", lambda r: r["infrastructure_phase"].__setitem__("bounded_attempts_per_exact_artifact_and_failure_class", 999))
    add("pull-speed selection", lambda r: r["infrastructure_phase"].__setitem__("selection_may_condition_on_pull_speed", True))
    add("rank burn", lambda r: r["infrastructure_phase"].__setitem__("retry_exhaustion_effect", "advance_rank"))
    add("post-content rerun", lambda r: r["protected_content_boundary"].__setitem__("after_trigger_no_rerun", False))
    add("open rank 6", lambda r: r["historical_reconciliation"].__setitem__("rank_6_may_open", True))
    add("fake pool pass", lambda r: r["current_capacity"].__setitem__("pool_wide_materialization_demonstrated", True))
    add("custody optional", lambda r: r["campaign_disposition_custody"].__setitem__("commit_required_before_counting", False))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "empirical-test-backed"))
    for label, mutation in mutations:
        if not failures(mutation, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 infrastructure/content amendment failed:\n - " + "\n - ".join(out))
    print("P2 infrastructure/content freeze amendment passed: setup retry is bounded before content, rank 5 pending, pool blocked honestly, 8/8 mutations rejected.")


if __name__ == "__main__":
    main()
