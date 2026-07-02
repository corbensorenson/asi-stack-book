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
RESULT = ROOT / "experiments" / "intent_recontract_probe" / "results" / "2026-07-02-local.json"
PROBE_ID = "intent-recontract-probe-2026-07-02-local"
RESULT_COMMAND = "python3 scripts/run_intent_recontract_probe.py --write-result"

TRIGGER_FIELDS = [
    "allowed_means",
    "authority_ceiling",
    "affected_parties",
    "evidence_bar",
    "publication_surface",
    "source_boundary",
    "stop_conditions",
    "support_state_effect",
]

NON_CLAIMS = [
    "This intent re-contract trigger probe does not promote any chapter core claim above argument.",
    "This intent re-contract trigger probe does not create a support-state transition.",
    "This intent re-contract trigger probe does not prove natural-language intent understanding, deployed parser quality, deployed authority extraction, prompt-injection containment, runtime dispatch, approval-service behavior, user satisfaction, or AI safety.",
    "This intent re-contract trigger probe uses generated public-safe contract and downstream-delta records only; it does not read private source text, call a network service, dispatch jobs, publish artifacts, or infer user intent from private conversation history.",
]

VALID_SCENARIO_IDS = {
    "valid_no_material_delta_continue",
    "valid_publication_surface_delta_recontracts",
}

EXPECTED_INVALID_IDS = {
    "invalid_authority_delta_without_recontract",
    "invalid_private_source_delta_without_recontract",
    "invalid_stop_condition_erasure_without_recontract",
    "invalid_evidence_bar_weakening_without_recontract",
    "invalid_affected_party_widening_without_recontract",
    "invalid_means_expansion_without_recontract",
    "invalid_support_state_promotion_without_recontract",
}


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def base_contract() -> dict[str, Any]:
    return {
        "contract_id": "intent-contract://recontract-probe/base-public-book-edit",
        "request_summary": "Improve a public-safe book chapter inside tracked repository files.",
        "allowed_means": ["edit_tracked_public_book_files", "run_local_validators"],
        "authority_ceiling": "local_public_book_edit_only",
        "affected_parties": ["book_maintainer"],
        "evidence_bar": "validation_output_and_no_support_promotion",
        "publication_surface": "draft_branch_only",
        "source_boundary": "public_safe_source_notes_only",
        "stop_conditions": ["stop_if_validation_fails", "stop_before_private_source_publication"],
        "support_state_effect": "none",
        "recontract_triggers": TRIGGER_FIELDS,
        "non_claims": [
            "synthetic intent contract only",
            "does not authorize runtime dispatch",
        ],
    }


def scenario_templates() -> list[dict[str, Any]]:
    def template(scenario_id: str, expected_route: str, expected_valid: bool) -> dict[str, Any]:
        return {
            "scenario_id": scenario_id,
            "expected_route": expected_route,
            "expected_valid": expected_valid,
            "accepted_contract": base_contract(),
            "downstream_delta": {},
            "recontract_record_present": False,
        }

    scenarios = [
        template("valid_no_material_delta_continue", "continue_under_existing_contract", True),
        template("valid_publication_surface_delta_recontracts", "require_recontract", True),
        template("invalid_authority_delta_without_recontract", "block_delta_until_recontract", False),
        template("invalid_private_source_delta_without_recontract", "block_delta_until_recontract", False),
        template("invalid_stop_condition_erasure_without_recontract", "block_delta_until_recontract", False),
        template("invalid_evidence_bar_weakening_without_recontract", "block_delta_until_recontract", False),
        template("invalid_affected_party_widening_without_recontract", "block_delta_until_recontract", False),
        template("invalid_means_expansion_without_recontract", "block_delta_until_recontract", False),
        template("invalid_support_state_promotion_without_recontract", "block_delta_until_recontract", False),
    ]
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        delta: dict[str, Any] = {}
        if sid == "valid_publication_surface_delta_recontracts":
            delta["publication_surface"] = "push_to_main_and_public_site"
            scenario["recontract_record_present"] = True
        elif sid == "invalid_authority_delta_without_recontract":
            delta["authority_ceiling"] = "repo_push_and_publish"
        elif sid == "invalid_private_source_delta_without_recontract":
            delta["source_boundary"] = "include_private_google_doc_raw_text"
        elif sid == "invalid_stop_condition_erasure_without_recontract":
            delta["stop_conditions"] = ["continue_even_if_validation_fails"]
        elif sid == "invalid_evidence_bar_weakening_without_recontract":
            delta["evidence_bar"] = "model_says_it_looks_good"
        elif sid == "invalid_affected_party_widening_without_recontract":
            delta["affected_parties"] = ["book_maintainer", "external_reviewers", "public_readers"]
        elif sid == "invalid_means_expansion_without_recontract":
            delta["allowed_means"] = [
                "edit_tracked_public_book_files",
                "run_local_validators",
                "install_external_service",
            ]
        elif sid == "invalid_support_state_promotion_without_recontract":
            delta["support_state_effect"] = "promote_chapter_core_claim"
        scenario["downstream_delta"] = delta
    return scenarios


def changed_trigger_fields(contract: dict[str, Any], delta: dict[str, Any]) -> list[str]:
    changed = []
    for field in TRIGGER_FIELDS:
        if field in delta and delta[field] != contract[field]:
            changed.append(field)
    return changed


def risky_delta_reasons(delta: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if delta.get("authority_ceiling") in {"repo_push_and_publish", "unbounded", "external_effects"}:
        reasons.append("authority_widening")
    if "private" in str(delta.get("source_boundary", "")).lower():
        reasons.append("private_source_boundary_change")
    if "continue_even_if_validation_fails" in [str(item) for item in delta.get("stop_conditions", [])]:
        reasons.append("stop_condition_erasure")
    if delta.get("evidence_bar") == "model_says_it_looks_good":
        reasons.append("evidence_bar_weakening")
    if "external_reviewers" in [str(item) for item in delta.get("affected_parties", [])]:
        reasons.append("affected_party_widening")
    if "install_external_service" in [str(item) for item in delta.get("allowed_means", [])]:
        reasons.append("means_expansion")
    if delta.get("support_state_effect") == "promote_chapter_core_claim":
        reasons.append("support_state_promotion_attempt")
    return reasons


def route_scenario(scenario: dict[str, Any]) -> tuple[str, str, list[str], list[str]]:
    contract = scenario["accepted_contract"]
    delta = scenario["downstream_delta"]
    changed = changed_trigger_fields(contract, delta)
    risky = risky_delta_reasons(delta)
    if not changed:
        return "continue_under_existing_contract", "no_material_recontract_trigger", changed, risky
    if scenario["recontract_record_present"]:
        return "require_recontract", "material_delta_has_recontract_record", changed, risky
    return "block_delta_until_recontract", "material_delta_without_recontract_record", changed, risky


def evaluate_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    route, reason, changed, risky = route_scenario(scenario)
    expected_valid = bool(scenario["expected_valid"])
    dispatch_allowed = route == "continue_under_existing_contract"
    recontract_required = route in {"require_recontract", "block_delta_until_recontract"}
    blocked_before_dispatch = route == "block_delta_until_recontract"
    support_state_effect = "none"
    scenario_pass = (
        route == scenario["expected_route"]
        and (not expected_valid or (scenario["recontract_record_present"] if route == "require_recontract" else True))
        and (blocked_before_dispatch if not expected_valid else True)
        and support_state_effect == "none"
    )
    return {
        "scenario_id": scenario["scenario_id"],
        "expected_valid": expected_valid,
        "expected_route": scenario["expected_route"],
        "actual_route": route,
        "decision_reason": reason,
        "scenario_pass": scenario_pass,
        "input_summary": {
            "accepted_contract_sha256": canonical_sha(scenario["accepted_contract"]),
            "downstream_delta": scenario["downstream_delta"],
            "changed_trigger_fields": changed,
            "risky_delta_reasons": risky,
            "recontract_record_present": scenario["recontract_record_present"],
        },
        "outcome": {
            "dispatch_allowed": dispatch_allowed,
            "recontract_required": recontract_required,
            "blocked_before_dispatch": blocked_before_dispatch,
            "private_source_read": False,
            "network_used": False,
            "job_dispatched": False,
            "publication_performed": False,
            "support_state_effect": support_state_effect,
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
    return canonical_sha(payload)


def build_record() -> dict[str, Any]:
    evaluated = [evaluate_scenario(scenario) for scenario in scenario_templates()]
    valid = [scenario for scenario in evaluated if scenario["scenario_id"] in VALID_SCENARIO_IDS]
    invalid = [scenario for scenario in evaluated if scenario["scenario_id"] in EXPECTED_INVALID_IDS]
    pass_state = (
        len(valid) == 2
        and len(invalid) == 7
        and all(scenario["scenario_pass"] for scenario in evaluated)
        and all(scenario["outcome"]["support_state_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["chapter_core_support_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["private_source_read"] is False for scenario in evaluated)
        and all(scenario["outcome"]["network_used"] is False for scenario in evaluated)
        and all(scenario["outcome"]["job_dispatched"] is False for scenario in evaluated)
        and all(scenario["outcome"]["publication_performed"] is False for scenario in evaluated)
    )
    return {
        "schema_version": "0.1",
        "probe_id": PROBE_ID,
        "record_kind": "intent_recontract_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "public_safety_boundary": "Generated public-safe intent contracts and downstream-delta records only; no private source text, network target, job dispatch, publication, or external service is used.",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": pass_state,
        "trigger_fields": TRIGGER_FIELDS,
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
    parser = argparse.ArgumentParser(description="Run a public-safe intent re-contract trigger probe.")
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
