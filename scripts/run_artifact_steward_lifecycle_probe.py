#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "artifact_steward_lifecycle_probe" / "results" / "2026-07-02-local.json"
PROBE_ID = "artifact-steward-lifecycle-probe-2026-07-02-local"
RESULT_COMMAND = "python3 scripts/run_artifact_steward_lifecycle_probe.py --write-result"

FIXTURE_REFS = {
    "charter": "tests/fixtures/protocol_records/artifact_steward_charter.valid.json",
    "work_contract": "tests/fixtures/protocol_records/project_work_contract.valid.json",
    "contribution_ledger": "tests/fixtures/protocol_records/contribution_ledger_entry.valid.json",
    "treasury_policy": "tests/fixtures/protocol_records/treasury_policy_record.valid.json",
    "event_taint": "tests/fixtures/protocol_records/event_taint_record.valid.json",
    "steward_decision": "tests/fixtures/protocol_records/steward_action_decision.valid.json",
    "sunset_review": "tests/fixtures/protocol_records/sunset_review_record.valid.json",
    "federation_lease": "tests/fixtures/protocol_records/hive_federation_lease.valid.json",
}

NON_CLAIMS = [
    "This artifact steward lifecycle probe does not promote any chapter core claim above argument.",
    "This artifact steward lifecycle probe does not create a support-state transition.",
    "This artifact steward lifecycle probe does not deploy or execute a steward bot, treasury executor, event-taint workflow, governance runner, contributor-ledger service, project federation harness, release runner, or sunset protocol.",
    "This artifact steward lifecycle probe does not prove treasury safety, legal authority, governance correctness, contributor fairness, workflow-injection resistance, capture resistance, release safety, federation safety, steward autonomy, project quality, or AI safety.",
    "This artifact steward lifecycle probe uses generated public-safe fixture compositions only; it does not move funds, merge branches, publish releases, dispatch external workers, scan live repository events, or call a network service. It does not copy private source text, local paths, secrets, keys, or raw project payloads into the repository.",
]

VALID_SCENARIO_IDS = {
    "valid_clean_release_review_proposal",
    "valid_sunset_review_route",
}

EXPECTED_INVALID_IDS = {
    "invalid_tainted_event_without_review",
    "invalid_over_policy_treasury_spend",
    "invalid_contribution_governance_laundering",
    "invalid_unscoped_federation_contract",
    "invalid_release_without_gate_evidence",
    "invalid_sunset_criteria_ordinary_work",
}


def load_fixture_summary() -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    for name, rel_path in FIXTURE_REFS.items():
        path = ROOT / rel_path
        if not path.exists():
            raise SystemExit(f"Missing fixture: {rel_path}")
        payload = path.read_bytes()
        data = json.loads(payload.decode("utf-8"))
        summary[name] = {
            "ref": rel_path,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "top_level_keys": sorted(data.keys()),
        }
    return summary


def scenario_templates() -> list[dict[str, Any]]:
    separated_fields = [
        "authorship_credit",
        "review_credit",
        "evidence_credit",
        "compensation_ref",
        "reputation_signal",
        "governance_effect",
        "conflict_notes",
    ]
    base = {
        "event": {
            "taint_state": "reviewed",
            "review_completed": True,
            "untrusted_control_fields_used": False,
        },
        "treasury": {
            "spend_requested": False,
            "requested_usd": 0,
            "policy_limit_usd": 0,
            "approval_ref": "not_required",
        },
        "contribution": {
            "ledger_entry_present": True,
            "separated_fields": separated_fields,
            "collapsed_score_used_for_governance": False,
            "support_state_change_requested": False,
            "evidence_transition_record_present": False,
        },
        "federation": {
            "external_worker_requested": False,
            "scoped_contract_present": True,
            "worker_inherits_project_authority": False,
            "external_spend_requested": False,
            "approval_ref": "not_required",
            "evidence_bundle_required": True,
        },
        "release": {
            "release_candidate_requested": False,
            "tests_recorded": True,
            "evidence_recorded": True,
            "changelog_recorded": True,
            "residuals_recorded": True,
            "approval_recorded": True,
        },
        "sunset": {
            "sunset_criteria_met": False,
            "sunset_review_opened": False,
            "ordinary_work_requested": False,
        },
        "autonomy": {
            "autonomy_increase_requested": False,
            "charter_approval_present": False,
        },
    }

    def with_updates(scenario_id: str, expected_route: str, expected_valid: bool, **updates: Any) -> dict[str, Any]:
        scenario = json.loads(json.dumps(base))
        scenario["scenario_id"] = scenario_id
        scenario["expected_route"] = expected_route
        scenario["expected_valid"] = expected_valid
        for section, patch in updates.items():
            scenario[section].update(patch)
        return scenario

    return [
        with_updates(
            "valid_clean_release_review_proposal",
            "prepare_release_review",
            True,
            release={"release_candidate_requested": True},
        ),
        with_updates(
            "valid_sunset_review_route",
            "open_sunset_review",
            True,
            sunset={"sunset_criteria_met": True, "sunset_review_opened": False, "ordinary_work_requested": False},
        ),
        with_updates(
            "invalid_tainted_event_without_review",
            "quarantine_event",
            False,
            event={"taint_state": "untrusted", "review_completed": False, "untrusted_control_fields_used": True},
            release={"release_candidate_requested": True},
        ),
        with_updates(
            "invalid_over_policy_treasury_spend",
            "request_treasury_approval",
            False,
            treasury={"spend_requested": True, "requested_usd": 50, "policy_limit_usd": 0, "approval_ref": ""},
        ),
        with_updates(
            "invalid_contribution_governance_laundering",
            "reject_collapsed_governance",
            False,
            contribution={"collapsed_score_used_for_governance": True},
        ),
        with_updates(
            "invalid_unscoped_federation_contract",
            "reject_federation_authority_inheritance",
            False,
            federation={
                "external_worker_requested": True,
                "scoped_contract_present": False,
                "worker_inherits_project_authority": True,
                "evidence_bundle_required": False,
            },
        ),
        with_updates(
            "invalid_release_without_gate_evidence",
            "block_release_evidence_gate",
            False,
            release={
                "release_candidate_requested": True,
                "tests_recorded": True,
                "evidence_recorded": False,
                "changelog_recorded": True,
                "residuals_recorded": False,
                "approval_recorded": False,
            },
        ),
        with_updates(
            "invalid_sunset_criteria_ordinary_work",
            "open_sunset_review",
            False,
            sunset={"sunset_criteria_met": True, "sunset_review_opened": False, "ordinary_work_requested": True},
        ),
    ]


def all_release_evidence_recorded(scenario: dict[str, Any]) -> bool:
    release = scenario["release"]
    return all(
        bool(release[key])
        for key in ("tests_recorded", "evidence_recorded", "changelog_recorded", "residuals_recorded", "approval_recorded")
    )


def all_contribution_fields_separated(scenario: dict[str, Any]) -> bool:
    required = {
        "authorship_credit",
        "review_credit",
        "evidence_credit",
        "compensation_ref",
        "reputation_signal",
        "governance_effect",
        "conflict_notes",
    }
    return scenario["contribution"]["ledger_entry_present"] and required.issubset(
        set(scenario["contribution"]["separated_fields"])
    )


def route_scenario(scenario: dict[str, Any]) -> tuple[str, str]:
    event = scenario["event"]
    treasury = scenario["treasury"]
    contribution = scenario["contribution"]
    federation = scenario["federation"]
    release = scenario["release"]
    sunset = scenario["sunset"]
    autonomy = scenario["autonomy"]

    if event["taint_state"] == "untrusted" and not event["review_completed"]:
        return "quarantine_event", "tainted_event_without_review"
    if sunset["sunset_criteria_met"] and not sunset["sunset_review_opened"]:
        return "open_sunset_review", "sunset_criteria_met_without_open_review"
    if treasury["spend_requested"] and treasury["requested_usd"] > treasury["policy_limit_usd"] and not treasury["approval_ref"]:
        return "request_treasury_approval", "spend_exceeds_policy_without_approval"
    if not all_contribution_fields_separated(scenario):
        return "request_ledger_repair", "contribution_ledger_missing_separated_fields"
    if contribution["collapsed_score_used_for_governance"]:
        return "reject_collapsed_governance", "collapsed_contribution_score_used_for_governance"
    if contribution["support_state_change_requested"] and not contribution["evidence_transition_record_present"]:
        return "request_evidence_transition", "support_state_change_without_evidence_transition"
    if federation["external_worker_requested"] and not federation["scoped_contract_present"]:
        if federation["worker_inherits_project_authority"]:
            return "reject_federation_authority_inheritance", "federated_worker_cannot_inherit_project_authority"
        return "request_federation_contract_repair", "external_worker_missing_scoped_contract"
    if federation["external_spend_requested"] and not federation["approval_ref"]:
        return "request_treasury_approval", "federated_spend_without_approval"
    if federation["external_worker_requested"] and not federation["evidence_bundle_required"]:
        return "request_federation_evidence_bundle", "federated_worker_missing_evidence_bundle_requirement"
    if release["release_candidate_requested"] and not all_release_evidence_recorded(scenario):
        return "block_release_evidence_gate", "release_candidate_missing_required_evidence_records"
    if autonomy["autonomy_increase_requested"] and not autonomy["charter_approval_present"]:
        return "request_charter_approval", "autonomy_escalation_without_charter_approval"
    if release["release_candidate_requested"]:
        return "prepare_release_review", "release_candidate_has_required_records_but_is_not_published"
    return "ordinary_work_proposal", "ordinary_work_remains_proposal_only"


def evaluate_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    route, reason = route_scenario(scenario)
    expected_valid = bool(scenario["expected_valid"])
    protected_action_allowed = route in {"prepare_release_review", "ordinary_work_proposal"}
    release_published = False
    spend_executed = False
    external_worker_dispatched = False
    ordinary_work_allowed = route in {"prepare_release_review", "ordinary_work_proposal"} and not scenario["sunset"][
        "ordinary_work_requested"
    ]
    governance_effect_allowed = route != "reject_collapsed_governance"
    worker_authority_inherited = False
    scenario_pass = route == scenario["expected_route"] and (
        expected_valid
        or (
            not release_published
            and not spend_executed
            and not external_worker_dispatched
            and not worker_authority_inherited
            and (governance_effect_allowed or route == "reject_collapsed_governance")
        )
    )
    if scenario["scenario_id"] == "invalid_sunset_criteria_ordinary_work":
        scenario_pass = scenario_pass and not ordinary_work_allowed

    return {
        "scenario_id": scenario["scenario_id"],
        "expected_valid": expected_valid,
        "expected_route": scenario["expected_route"],
        "actual_route": route,
        "decision_reason": reason,
        "scenario_pass": scenario_pass,
        "input_summary": {
            "event_taint_state": scenario["event"]["taint_state"],
            "event_review_completed": scenario["event"]["review_completed"],
            "treasury_requested_usd": scenario["treasury"]["requested_usd"],
            "treasury_policy_limit_usd": scenario["treasury"]["policy_limit_usd"],
            "contribution_fields_separated": all_contribution_fields_separated(scenario),
            "collapsed_score_used_for_governance": scenario["contribution"]["collapsed_score_used_for_governance"],
            "external_worker_requested": scenario["federation"]["external_worker_requested"],
            "worker_inherits_project_authority_requested": scenario["federation"]["worker_inherits_project_authority"],
            "release_candidate_requested": scenario["release"]["release_candidate_requested"],
            "release_gate_complete": all_release_evidence_recorded(scenario),
            "sunset_criteria_met": scenario["sunset"]["sunset_criteria_met"],
            "sunset_review_opened": scenario["sunset"]["sunset_review_opened"],
            "ordinary_work_requested": scenario["sunset"]["ordinary_work_requested"],
        },
        "outcome": {
            "protected_action_allowed": protected_action_allowed,
            "release_published": release_published,
            "spend_executed": spend_executed,
            "external_worker_dispatched": external_worker_dispatched,
            "ordinary_work_allowed": ordinary_work_allowed,
            "governance_effect_allowed": governance_effect_allowed,
            "worker_authority_inherited": worker_authority_inherited,
            "support_state_effect": "none",
            "chapter_core_support_effect": "none",
        },
    }


def decision_digest(valid: list[dict[str, Any]], invalid: list[dict[str, Any]]) -> str:
    payload = [
        {
            "scenario_id": scenario["scenario_id"],
            "actual_route": scenario["actual_route"],
            "decision_reason": scenario["decision_reason"],
            "scenario_pass": scenario["scenario_pass"],
            "outcome": scenario["outcome"],
        }
        for scenario in valid + invalid
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_record() -> dict[str, Any]:
    fixture_summary = load_fixture_summary()
    evaluated = [evaluate_scenario(scenario) for scenario in scenario_templates()]
    valid = [scenario for scenario in evaluated if scenario["scenario_id"] in VALID_SCENARIO_IDS]
    invalid = [scenario for scenario in evaluated if scenario["scenario_id"] in EXPECTED_INVALID_IDS]
    pass_state = (
        len(valid) == 2
        and len(invalid) == 6
        and all(scenario["scenario_pass"] for scenario in evaluated)
        and all(scenario["outcome"]["support_state_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["chapter_core_support_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["release_published"] is False for scenario in evaluated)
        and all(scenario["outcome"]["spend_executed"] is False for scenario in evaluated)
        and all(scenario["outcome"]["external_worker_dispatched"] is False for scenario in evaluated)
        and all(scenario["outcome"]["worker_authority_inherited"] is False for scenario in evaluated)
    )
    return {
        "schema_version": "0.1",
        "probe_id": PROBE_ID,
        "record_kind": "artifact_steward_lifecycle_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "public_safety_boundary": "Generated public-safe steward lifecycle records only; no funds, branch, release, worker, live event, network target, private source, or external service is mutated.",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": pass_state,
        "fixture_summary": fixture_summary,
        "summary": {
            "valid_scenarios": len(valid),
            "expected_invalid_controls": len(invalid),
            "decision_digest": decision_digest(valid, invalid),
        },
        "valid_scenarios": valid,
        "expected_invalid_controls": invalid,
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a public-safe artifact steward lifecycle probe.")
    parser.add_argument("--write-result", action="store_true", help=f"write {RESULT.relative_to(ROOT)}")
    args = parser.parse_args()

    record = build_record()
    text = json.dumps(record, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(text, end="")
    if not record.get("pass"):
        sys.exit(1)


if __name__ == "__main__":
    main()
