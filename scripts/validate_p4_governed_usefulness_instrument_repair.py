#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V1_RESULT = ROOT / "experiments" / "p4_governed_usefulness" / "results" / "strong_model_sacrificial_preflight.json"
V1_RAW = ROOT / "experiments" / "p4_governed_usefulness" / "raw" / "strong_model_sacrificial_preflight_v1.json"
DIAGNOSIS = ROOT / "experiments" / "p4_governed_usefulness" / "v1_failure_diagnosis.json"
V2_PREREG = ROOT / "experiments" / "p4_governed_usefulness" / "preregistration_v2.json"
V2_PROMPT = ROOT / "experiments" / "p4_governed_usefulness" / "strong_model_sacrificial_prompt_v2.md"
V2_LABELS = ROOT / "experiments" / "p4_governed_usefulness" / "sacrificial_labels_v2.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(value: dict[str, Any]) -> list[str]:
    out: list[str] = []
    result = load(V1_RESULT)
    diagnosis = load(DIAGNOSIS)
    labels = load(V2_LABELS)
    if result.get("protocol_outcome") != "instrument_inadequate_recampaign_required" or result.get("claim_attempt_counted") is not False:
        out.append("v1 instrument failure or non-claim boundary was rewritten")
    if result.get("schema_admissible_task_count") != 6 or result.get("semantically_correct_admissible_task_count") != 1:
        out.append("v1 observed denominator was rewritten")
    parent = value.get("repair_parent", {})
    for key, path in (("v1_result_sha256", V1_RESULT), ("v1_raw_response_sha256", V1_RAW), ("v1_diagnosis_sha256", DIAGNOSIS)):
        if parent.get(key) != sha(path):
            out.append(f"v2 repair parent digest drift: {key}")
    if parent.get("retrospective_rescore_allowed") is not False or diagnosis.get("retrospective_rescore_allowed") is not False:
        out.append("v1 retrospective rescore was permitted")
    if value.get("state") != "authorized_before_v2_strong_model_submission" or value.get("protocol_id") != "p4-gu-instrument-preflight-v2":
        out.append("v2 repair is not prospectively frozen under a new identity")
    instrument = value.get("instrument", {})
    if instrument.get("prompt_sha256") != sha(V2_PROMPT) or instrument.get("labels_sha256") != sha(V2_LABELS):
        out.append("v2 prompt or labels digest drift")
    if instrument.get("task_count") != 6 or instrument.get("minimum_schema_admissible_task_count") != 5 or instrument.get("minimum_semantically_correct_admissible_task_count") != 5:
        out.append("v2 denominator or pass floor drift")
    if instrument.get("route_detail_scored") is not False or instrument.get("brief_reason_scored") is not False:
        out.append("v2 reintroduced free-text exact-match scoring")
    if len(instrument.get("canonical_decision_classes", [])) != 6 or len(instrument.get("canonical_residual_classes", [])) != 7:
        out.append("v2 canonical taxonomy drift")
    if instrument.get("maximum_evaluator_disagreement_count") != 0 or instrument.get("candidate_artifact_closes_before_labels_load") is not True:
        out.append("v2 evaluation isolation or agreement gate drift")
    label_rows = labels.get("labels", [])
    if len(label_rows) != 6 or {row.get("task_id") for row in label_rows} != {"gw-sac-01","gw-sac-02","gl-sac-01","gl-sac-02","ac-sac-01","ac-sac-02"}:
        out.append("v2 labels do not exactly cover the sacrificial tasks")
    prompt = V2_PROMPT.read_text(encoding="utf-8")
    if any(row["task_id"] not in prompt for row in label_rows) or "hidden chain-of-thought" not in prompt:
        out.append("v2 prompt task or reasoning boundary drift")
    if value.get("state") != "authorized_before_v2_strong_model_submission":
        out.append("v2 preregistration must record authorization before submission")
    if value.get("authorization", {}).get("prompt_submission_authority") != "explicit_user_authority_2026-07-16_run_v2_in_chat_pro":
        out.append("v2 submission authority does not match the user's explicit instruction")
    if value.get("difficulty_sweep_state") != "closed" or value.get("confirmatory_denominator_state") != "closed":
        out.append("v2 repair prematurely opened an outcome denominator")
    if value.get("claim_outcome") is not None or value.get("claim_attempt_counted") is not False or value.get("support_state_effect") != "none":
        out.append("v2 repair was laundered into claim support")
    return out


def main() -> None:
    value = load(V2_PREREG)
    failures = errors(value)
    mutations: list[tuple[str, dict[str, Any]]] = []
    for label, change in (
        ("retrospective rescore", lambda row: row["repair_parent"].__setitem__("retrospective_rescore_allowed", True)),
        ("same protocol identity", lambda row: row.__setitem__("protocol_id", "p4-gu-instrument-preflight-v1")),
        ("weak semantic floor", lambda row: row["instrument"].__setitem__("minimum_semantically_correct_admissible_task_count", 4)),
        ("free-text route scoring", lambda row: row["instrument"].__setitem__("route_detail_scored", True)),
        ("premature sweep", lambda row: row.__setitem__("difficulty_sweep_state", "open")),
        ("invented authority", lambda row: row["authorization"].__setitem__("prompt_submission_authority", "granted")),
    ):
        candidate = copy.deepcopy(value)
        change(candidate)
        mutations.append((label, candidate))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4 instrument repair validation failed:\n - " + "\n - ".join(failures))
    print("P4 instrument repair passed: immutable 6/6-admissible 1/6-exact v1 failure, new canonical v2 protocol, 5/6 floors, closed downstream denominators, six rejecting mutations, and no rescore or support effect.")


if __name__ == "__main__":
    main()
