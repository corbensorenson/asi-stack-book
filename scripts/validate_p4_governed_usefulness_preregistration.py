#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "experiments" / "p4_governed_usefulness" / "preregistration.json"
ACCESS = ROOT / "experiments" / "p4_governed_usefulness" / "strong_model_access_preflight.json"
PROMPT = ROOT / "experiments" / "p4_governed_usefulness" / "strong_model_sacrificial_prompt.md"
LABELS = ROOT / "experiments" / "p4_governed_usefulness" / "sacrificial_labels.json"
CORPUS = ROOT / "experiments" / "research_foundation" / "task_corpus.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_claim_proof_and_sota_challenge_status.json"
RESULT = ROOT / "experiments" / "p4_governed_usefulness" / "results" / "strong_model_sacrificial_preflight.json"
RAW = ROOT / "experiments" / "p4_governed_usefulness" / "raw" / "strong_model_sacrificial_preflight_v1.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(value: dict[str, Any]) -> list[str]:
    out: list[str] = []
    access = load(ACCESS)
    labels = load(LABELS)
    corpus = load(CORPUS)
    status = load(STATUS)

    if value.get("schema_version") != "asi_stack.p4_governed_usefulness_preregistration.v1":
        out.append("wrong preregistration schema version")
    if value.get("state") != "terminal_instrument_inadequate_recampaign_required":
        out.append("v1 preregistration does not preserve its terminal instrument failure")
    if value.get("support_state_effect") != "none":
        out.append("preregistration invents support movement")

    foundation = value.get("foundation", {})
    if foundation.get("task_corpus_sha256") != sha(CORPUS):
        out.append("foundation corpus digest drift")
    ids = foundation.get("sacrificial_task_ids", [])
    corpus_ids = [row["task_id"] for row in corpus.get("tasks", []) if row.get("split") == "sacrificial"]
    if ids != corpus_ids or len(ids) != 6 or foundation.get("held_out_opened") is not False:
        out.append("sacrificial IDs or held-out closure drift")

    label_rows = labels.get("labels", [])
    if [row.get("task_id") for row in label_rows] != ids or "Do not place" not in labels.get("access_policy", ""):
        out.append("evaluator labels do not exactly cover or isolate sacrificial tasks")
    allowed_routes = {"block", "edit_only", "deny", "not_ready", "revoke", "quarantine", "escalate", "narrow", "release", "abstain"}
    if any(row.get("route") not in allowed_routes or not row.get("residual") for row in label_rows):
        out.append("sacrificial labels contain invalid routes or blank residuals")

    prompt = PROMPT.read_text(encoding="utf-8")
    if any(task_id not in prompt for task_id in ids) or "Return only" not in prompt or "do not reveal hidden chain-of-thought" not in prompt:
        out.append("frozen prompt omits tasks or answer/reasoning boundary")
    leaked = [row["residual"] for row in label_rows if row["residual"] in prompt]
    if leaked:
        out.append(f"frozen prompt leaks evaluator residuals: {leaked}")

    if access.get("prompt_submitted") is not True or access.get("response_observed") is not True:
        out.append("access receipt erases the completed v1 inference")
    if access.get("account_identifier_recorded") is not False or access.get("private_project_payload_observed_or_transmitted") is not False:
        out.append("access receipt violates privacy boundary")
    if access.get("authority") != "explicit_user_instruction_to_choose_and_use_chat_pro_for_the_frozen_public_safe_preflight" or access.get("support_state_effect") != "none":
        out.append("access receipt overstates authority or support")
    result = load(RESULT)
    if access.get("raw_response_sha256") != sha(RAW) or access.get("result_sha256") != sha(RESULT):
        out.append("access receipt raw/result digest drift")
    if result.get("protocol_outcome") != "instrument_inadequate_recampaign_required" or result.get("schema_admissible_task_count") != 6 or result.get("semantically_correct_admissible_task_count") != 1:
        out.append("v1 result boundary drift")
    if result.get("claim_attempt_counted") is not False or result.get("difficulty_sweep_opened") is not False or result.get("support_state_effect") != "none":
        out.append("v1 failure was laundered into a claim attempt, sweep, or support")

    preflight = value.get("instrument_preflight", {})
    if preflight.get("prompt_sha256") != sha(PROMPT) or preflight.get("labels_sha256") != sha(LABELS):
        out.append("frozen prompt or evaluator-label digest drift")
    if preflight.get("evaluator_path") != "scripts/evaluate_p4_governed_usefulness_preflight.py":
        out.append("strong-model preflight evaluator path drift")
    if preflight.get("task_count") != 6 or preflight.get("minimum_schema_admissible_task_count") != 5:
        out.append("sacrificial denominator or prospective floor drift")
    if preflight.get("minimum_schema_admissible_rate", 1) < 0.8:
        out.append("schema-admissibility floor falls below roadmap requirement")
    if preflight.get("minimum_semantically_correct_admissible_task_count") != 4 or preflight.get("maximum_evaluator_disagreement_count") != 0:
        out.append("semantic correctness or evaluator agreement gate drift")
    if preflight.get("claim_outcome") is not None or preflight.get("claim_attempt_counted") is not False:
        out.append("sacrificial preflight is laundered into a claim attempt")
    if len(preflight.get("stop_rules", [])) < 4:
        out.append("preflight lacks prospective stop rules")

    sweep = value.get("difficulty_sweep_entry_gate", {})
    confirm = value.get("confirmatory_entry_gate", {})
    if sweep.get("state") != "closed" or len(sweep.get("opens_only_if", [])) < 5:
        out.append("difficulty sweep opened before instrument adequacy")
    if confirm.get("state") != "closed" or len(confirm.get("requirements", [])) < 8:
        out.append("confirmatory campaign opened before an informative sweep")
    authorization = value.get("authorization", {})
    if authorization.get("prompt_submission_authority") != "explicit_user_instruction_to_choose_and_use_chat_pro_for_this_frozen_public_safe_preflight" or authorization.get("publication_authority") != "none" or authorization.get("release_authority") != "none":
        out.append("authorization boundary drift")

    priorities = {row.get("id"): row.get("state") for row in status.get("priorities", [])}
    milestones = {row.get("id"): row.get("state") for row in status.get("milestones", [])}
    campaign = status.get("governed_usefulness_campaign_contract", {})
    roadmap_position = (
        (status.get("current_priority") == "P4" and priorities.get("P4") == "in_progress")
        or (status.get("status") == "completed" and status.get("current_priority") is None and priorities.get("P4") == "completed")
    )
    if not roadmap_position or milestones.get("M5") != "completed" or campaign.get("confirmatory_protocol_outcome") != "bounded_local_governance_effect_supported":
        out.append("roadmap does not preserve completed M5 lineage inside active P4")
    if len(value.get("non_claims", [])) < 4:
        out.append("preregistration lacks explicit non-claims")
    return out


def main() -> None:
    value = load(PREREG)
    failures = errors(value)
    mutations: list[tuple[str, dict[str, Any]]] = []
    for label, change in (
        ("support laundering", lambda row: row.__setitem__("support_state_effect", "promotion")),
        ("held-out opening", lambda row: row["foundation"].__setitem__("held_out_opened", True)),
        ("weak floor", lambda row: row["instrument_preflight"].__setitem__("minimum_schema_admissible_rate", 0.79)),
        ("claim laundering", lambda row: row["instrument_preflight"].__setitem__("claim_attempt_counted", True)),
        ("premature confirmatory opening", lambda row: row["confirmatory_entry_gate"].__setitem__("state", "open")),
        ("submission authority rewrite", lambda row: row["authorization"].__setitem__("prompt_submission_authority", "unbounded")),
    ):
        candidate = copy.deepcopy(value)
        change(candidate)
        mutations.append((label, candidate))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P4 governed-usefulness preregistration failed:\n - " + "\n - ".join(failures))
    print(
        "P4 governed-usefulness v1 passed its lineage gate: one Chat Pro call, 6/6 schema-admissible, "
        "1/6 exact, terminal instrument_inadequate_recampaign_required, closed downstream denominators, "
        "six rejecting mutations, and no claim, publication, or release authority."
    )


if __name__ == "__main__":
    main()
