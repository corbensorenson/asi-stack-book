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
RESULT = ROOT / "experiments" / "vcm_resolver_certificate_probe" / "results" / "2026-07-02-local.json"
PROBE_ID = "vcm-resolver-certificate-probe-2026-07-02-local"
RESULT_COMMAND = "python3 scripts/run_vcm_resolver_certificate_probe.py --write-result"

NON_CLAIMS = [
    "This VCM resolver/certificate probe does not promote any chapter core claim above argument.",
    "This VCM resolver/certificate probe does not create a support-state transition.",
    "This VCM resolver/certificate probe does not prove deployed resolver correctness, memory-store behavior, planner-guided context compilation, open-domain summary fidelity, certificate truthfulness, transaction isolation, deletion enforcement, model-facing context quality, contradiction-rate improvement, distractor resistance, VCM-Bench performance, leak prevention, or AI safety.",
    "This VCM resolver/certificate probe uses generated public-safe source-cell facts only; it does not read private source text, copy raw source payloads, call a network service, run a model, access a live memory store, or materialize real user data.",
]

VALID_SCENARIO_IDS = {
    "valid_resolver_materialization_receipt",
    "valid_mandatory_miss_typed_fault",
}

EXPECTED_INVALID_IDS = {
    "invalid_address_mismatch_materialization_denied",
    "invalid_version_mismatch_materialization_denied",
    "invalid_snapshot_mismatch_materialization_denied",
    "invalid_mount_policy_denied",
    "invalid_lease_expired_reuse_blocked",
    "invalid_certificate_source_binding_mismatch_denied",
    "invalid_certificate_authority_escalation_denied",
    "invalid_certificate_truthfulness_overclaim_denied",
    "invalid_summary_fidelity_omission_denied",
}

AUTHORITY_RANK = {
    "public_read": 1,
    "public_transform": 2,
    "tracked_file_write": 3,
    "restricted_source": 4,
    "secret": 5,
}


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def source_cell() -> dict[str, Any]:
    facts = {
        "stable_address": "Context objects must carry stable address, version, and snapshot bindings.",
        "authority_boundary": "Summaries and derived cells cannot raise source authority ceilings.",
        "fault_contract": "Mandatory context misses must emit typed faults instead of best-effort packets.",
    }
    return {
        "cell_id": "cell://vcm-probe/source/vcm-public-static-abi",
        "semantic_address": "vcm://book/source-notes/vcm_public/static-abi",
        "version": "source-note-2026-06-24",
        "snapshot_id": "snapshot://vcm-probe/public-safe-001",
        "mount": "public-safe-source-note",
        "authority_ceiling": "public_read",
        "facts": facts,
        "facts_sha256": canonical_sha(facts),
        "non_claims": [
            "synthetic source-cell facts only",
            "not a quotation from private source text",
        ],
    }


def base_catalog() -> dict[str, Any]:
    cell = source_cell()
    return {
        "allowed_mounts": ["public-safe-source-note"],
        "bindings": [
            {
                "semantic_address": cell["semantic_address"],
                "version": cell["version"],
                "snapshot_id": cell["snapshot_id"],
                "mount": cell["mount"],
                "source_cell_id": cell["cell_id"],
                "source_facts_sha256": cell["facts_sha256"],
            }
        ],
    }


def base_request() -> dict[str, Any]:
    cell = source_cell()
    return {
        "request_id": "context-request://vcm-probe/static-abi-001",
        "semantic_address": cell["semantic_address"],
        "version": cell["version"],
        "snapshot_id": cell["snapshot_id"],
        "mount": cell["mount"],
        "mandatory": True,
        "requested_use": "chapter_drafting",
        "lease_state": "active",
        "certificate_required": True,
    }


def base_derived_cell() -> dict[str, Any]:
    cell = source_cell()
    included = ["stable_address", "authority_boundary"]
    omitted = sorted(set(cell["facts"]) - set(included))
    return {
        "cell_id": "cell://vcm-probe/derived/static-abi-summary",
        "source_cell_id": cell["cell_id"],
        "source_bindings": [cell["cell_id"]],
        "representation_kind": "lossy_summary",
        "included_fact_keys": included,
        "omitted_fact_keys": omitted,
        "authority_ceiling": "public_read",
        "derived_facts_sha256": canonical_sha({key: cell["facts"][key] for key in included}),
    }


def base_certificate() -> dict[str, Any]:
    cell = source_cell()
    derived = base_derived_cell()
    return {
        "certificate_id": "certificate://vcm-probe/static-abi-summary",
        "source_bindings": [cell["cell_id"]],
        "derived_cell_id": derived["cell_id"],
        "representation_claim": "lossy_summary_with_declared_omissions",
        "source_facts_sha256": cell["facts_sha256"],
        "derived_facts_sha256": derived["derived_facts_sha256"],
        "omissions": derived["omitted_fact_keys"],
        "loss_contract": "lossy summary may omit declared facts and cannot be used as an exact quotation or support-state promotion artifact",
        "permitted_uses": ["chapter_drafting", "source_queue_routing"],
        "authority_ceiling": "public_read",
        "certificate_fresh": True,
        "revocation_state": "active",
    }


def scenario_templates() -> list[dict[str, Any]]:
    def template(scenario_id: str, expected_route: str, expected_valid: bool) -> dict[str, Any]:
        return {
            "scenario_id": scenario_id,
            "expected_route": expected_route,
            "expected_valid": expected_valid,
            "catalog": base_catalog(),
            "request": base_request(),
            "source_cell": source_cell(),
            "derived_cell": base_derived_cell(),
            "certificate": base_certificate(),
        }

    scenarios = [
        template("valid_resolver_materialization_receipt", "materialize_context", True),
        template("valid_mandatory_miss_typed_fault", "issue_typed_fault", True),
        template("invalid_address_mismatch_materialization_denied", "issue_typed_fault", False),
        template("invalid_version_mismatch_materialization_denied", "issue_typed_fault", False),
        template("invalid_snapshot_mismatch_materialization_denied", "issue_typed_fault", False),
        template("invalid_mount_policy_denied", "deny_mount_policy", False),
        template("invalid_lease_expired_reuse_blocked", "deny_expired_lease", False),
        template("invalid_certificate_source_binding_mismatch_denied", "reject_source_binding_mismatch", False),
        template("invalid_certificate_authority_escalation_denied", "reject_authority_escalation", False),
        template("invalid_certificate_truthfulness_overclaim_denied", "reject_truthfulness_overclaim", False),
        template("invalid_summary_fidelity_omission_denied", "reject_undeclared_omission", False),
    ]

    for scenario in scenarios:
        sid = scenario["scenario_id"]
        if sid == "valid_mandatory_miss_typed_fault":
            scenario["request"]["semantic_address"] = "vcm://book/source-notes/missing"
        elif sid == "invalid_address_mismatch_materialization_denied":
            scenario["request"]["semantic_address"] = "vcm://book/source-notes/other"
        elif sid == "invalid_version_mismatch_materialization_denied":
            scenario["request"]["version"] = "stale-version"
        elif sid == "invalid_snapshot_mismatch_materialization_denied":
            scenario["request"]["snapshot_id"] = "snapshot://vcm-probe/stale"
        elif sid == "invalid_mount_policy_denied":
            scenario["request"]["mount"] = "restricted-private-cache"
        elif sid == "invalid_lease_expired_reuse_blocked":
            scenario["request"]["lease_state"] = "expired"
        elif sid == "invalid_certificate_source_binding_mismatch_denied":
            scenario["certificate"]["source_bindings"] = ["cell://vcm-probe/source/other"]
        elif sid == "invalid_certificate_authority_escalation_denied":
            scenario["derived_cell"]["authority_ceiling"] = "tracked_file_write"
            scenario["certificate"]["authority_ceiling"] = "tracked_file_write"
        elif sid == "invalid_certificate_truthfulness_overclaim_denied":
            scenario["certificate"]["representation_claim"] = "exact_quote_complete"
        elif sid == "invalid_summary_fidelity_omission_denied":
            scenario["certificate"]["omissions"] = []
    return scenarios


def binding_matches(request: dict[str, Any], binding: dict[str, Any]) -> bool:
    return (
        request["semantic_address"] == binding["semantic_address"]
        and request["version"] == binding["version"]
        and request["snapshot_id"] == binding["snapshot_id"]
        and request["mount"] == binding["mount"]
    )


def resolver_route(scenario: dict[str, Any]) -> tuple[str, str]:
    request = scenario["request"]
    catalog = scenario["catalog"]
    if request["mount"] not in catalog["allowed_mounts"]:
        return "deny_mount_policy", "mount_not_permitted_for_request"
    if request["lease_state"] != "active":
        return "deny_expired_lease", "context_lease_not_active"
    if not any(binding_matches(request, binding) for binding in catalog["bindings"]):
        if request["mandatory"]:
            return "issue_typed_fault", "mandatory_context_reference_not_found"
        return "request_context", "optional_context_reference_not_found"
    if request["certificate_required"] and not scenario.get("certificate"):
        return "require_certificate", "certificate_required_for_materialization"
    return "resolver_ok", "address_version_snapshot_mount_resolved"


def certificate_route(scenario: dict[str, Any]) -> tuple[str, str]:
    source = scenario["source_cell"]
    derived = scenario["derived_cell"]
    certificate = scenario["certificate"]
    if set(certificate["source_bindings"]) != set(derived["source_bindings"]):
        return "reject_source_binding_mismatch", "certificate_bindings_do_not_match_derived_cell"
    if source["cell_id"] not in certificate["source_bindings"]:
        return "reject_source_binding_mismatch", "source_cell_missing_from_certificate"
    if certificate["source_facts_sha256"] != source["facts_sha256"]:
        return "reject_source_binding_mismatch", "source_facts_digest_mismatch"
    omitted = set(derived["omitted_fact_keys"])
    if not omitted.issubset(set(certificate["omissions"])):
        return "reject_undeclared_omission", "derived_cell_omissions_not_declared"
    source_rank = AUTHORITY_RANK[source["authority_ceiling"]]
    derived_rank = AUTHORITY_RANK[derived["authority_ceiling"]]
    certificate_rank = AUTHORITY_RANK[certificate["authority_ceiling"]]
    if derived_rank > source_rank or certificate_rank > source_rank:
        return "reject_authority_escalation", "derived_or_certificate_authority_exceeds_source"
    if certificate["representation_claim"] == "exact_quote_complete" and (
        derived["representation_kind"] != "exact_excerpt" or derived["omitted_fact_keys"]
    ):
        return "reject_truthfulness_overclaim", "certificate_claims_exact_complete_representation_for_lossy_cell"
    if scenario["request"]["requested_use"] not in certificate["permitted_uses"]:
        return "reject_consumer_policy", "requested_use_outside_certificate_policy"
    if not certificate["certificate_fresh"] or certificate["revocation_state"] != "active":
        return "require_certificate_refresh", "certificate_not_fresh_or_active"
    return "certificate_ok", "paired_source_derived_cell_certificate_consistent"


def evaluate_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    resolver, resolver_reason = resolver_route(scenario)
    if resolver != "resolver_ok":
        route, reason = resolver, resolver_reason
    else:
        certificate, certificate_reason = certificate_route(scenario)
        route = "materialize_context" if certificate == "certificate_ok" else certificate
        reason = "resolver_and_certificate_accepted" if certificate == "certificate_ok" else certificate_reason

    materialization_emitted = route == "materialize_context"
    typed_fault_emitted = route == "issue_typed_fault"
    support_state_effect = "none"
    expected_valid = bool(scenario["expected_valid"])
    scenario_pass = (
        route == scenario["expected_route"]
        and (materialization_emitted is True if route == "materialize_context" else True)
        and (not materialization_emitted if not expected_valid else True)
    )
    if scenario["scenario_id"] == "valid_mandatory_miss_typed_fault":
        scenario_pass = scenario_pass and typed_fault_emitted and not materialization_emitted

    return {
        "scenario_id": scenario["scenario_id"],
        "expected_valid": expected_valid,
        "expected_route": scenario["expected_route"],
        "actual_route": route,
        "decision_reason": reason,
        "scenario_pass": scenario_pass,
        "input_summary": {
            "semantic_address": scenario["request"]["semantic_address"],
            "version": scenario["request"]["version"],
            "snapshot_id": scenario["request"]["snapshot_id"],
            "mount": scenario["request"]["mount"],
            "mandatory": scenario["request"]["mandatory"],
            "lease_state": scenario["request"]["lease_state"],
            "source_facts_sha256": scenario["source_cell"]["facts_sha256"],
            "derived_facts_sha256": scenario["derived_cell"]["derived_facts_sha256"],
            "certificate_claim": scenario["certificate"]["representation_claim"],
            "certificate_omissions": scenario["certificate"]["omissions"],
            "source_authority_ceiling": scenario["source_cell"]["authority_ceiling"],
            "derived_authority_ceiling": scenario["derived_cell"]["authority_ceiling"],
            "certificate_authority_ceiling": scenario["certificate"]["authority_ceiling"],
        },
        "outcome": {
            "materialization_emitted": materialization_emitted,
            "typed_fault_emitted": typed_fault_emitted,
            "model_called": False,
            "network_used": False,
            "private_source_read": False,
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
        and len(invalid) == 9
        and all(scenario["scenario_pass"] for scenario in evaluated)
        and all(scenario["outcome"]["support_state_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["chapter_core_support_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["model_called"] is False for scenario in evaluated)
        and all(scenario["outcome"]["network_used"] is False for scenario in evaluated)
        and all(scenario["outcome"]["private_source_read"] is False for scenario in evaluated)
    )
    return {
        "schema_version": "0.1",
        "probe_id": PROBE_ID,
        "record_kind": "vcm_resolver_certificate_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "public_safety_boundary": "Generated public-safe source-cell facts and derived-cell metadata only; no private source text, live memory store, model call, network target, or real user data is read or materialized.",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": pass_state,
        "synthetic_source_cell": {
            "cell_id": source_cell()["cell_id"],
            "facts_sha256": source_cell()["facts_sha256"],
            "fact_keys": sorted(source_cell()["facts"]),
            "non_claims": source_cell()["non_claims"],
        },
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
    parser = argparse.ArgumentParser(description="Run a public-safe VCM resolver/certificate conformance probe.")
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
