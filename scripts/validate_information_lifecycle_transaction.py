#!/usr/bin/env python3
"""Validate the bounded privacy lifecycle transaction and rejecting controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import subprocess
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/information_lifecycle_transaction.schema.json"
FIXTURE = ROOT / "tests/fixtures/protocol_records/information_lifecycle_transaction.valid.json"
EXPECTED_SOURCES = {
    "ext_nist_privacy_framework_2020", "ext_eu_gdpr_2016", "ext_w3c_dpv_2024",
    "ext_abadi_dpsgd_2016", "ext_algospec_purpose_limitation_2024",
    "ext_carlini_training_data_extraction_2021", "ext_choquette_choo_label_only_mia_2021",
    "ext_nist_differential_privacy_2025", "ext_mahloujifar_fdp_audit_2025",
}
EXPECTED_NON_AUTHORITIES = {"legal_compliance", "valid_consent", "lawful_basis", "privacy_guarantee", "attack_absence", "complete_lineage", "total_erasure", "behavioral_forgetting", "influence_removal", "support_or_release"}
REQUIRED_SURFACES = {"input", "context", "memory", "training", "inference", "output", "audit", "sharing", "cache", "backup", "checkpoint", "derivative"}
REQUIRED_ATTACKS = {"extraction", "confidence-membership", "label-only-membership", "linkage", "cross-user-memory"}
LEAN = ROOT / "lean/AsiStackProofs/PrivacyInformationFlow.lean"
ROUTE_THEOREMS = {
    "accepted_requires_purpose_and_authority",
    "accepted_requires_flow_and_privacy_evaluation",
    "accepted_separates_outcomes_and_refuses_compliance",
    "purpose_drift_rejects",
    "hidden_unknown_copies_request_flow_map",
    "label_attack_incompetence_rejects_privacy_evaluation",
    "missing_recipient_notice_requests_rights_work",
    "conflated_behavior_and_storage_quarantines",
    "compliance_laundering_quarantines",
    "release_laundering_quarantines",
    "complete_authored_record_accepts_bounded_receipt",
}
LIFECYCLE_THEOREMS = {
    "accepted_information_step_is_valid",
    "accepted_information_step_applies_event",
    "apply_information_event_preserves_identity",
    "accepted_information_step_preserves_non_authority",
    "accepted_information_step_preserves_known_copy_inventory",
    "rejected_information_step_preserves_exact_state",
    "accepted_information_step_adds_one_receipt",
    "accepted_information_step_respects_authority_ceiling",
    "successful_information_run_preserves_identity",
    "successful_information_run_preserves_non_authority",
    "successful_information_run_preserves_known_copy_inventory",
    "successful_information_run_respects_authority_ceiling",
    "successful_information_run_has_valid_trace",
    "information_run_composes",
    "active_information_use_cannot_record_deletion",
    "accepted_activation_requires_rights_disposition",
    "accepted_revocation_zeros_information_authority",
    "accepted_deletion_records_only_known_copy_disposition",
    "deletion_recorded_information_state_rejects_every_event",
    "deletion_recorded_information_state_has_no_nonempty_run",
    "complete_information_prefix_reaches_exact_revoked_state",
    "complete_information_run_reaches_bounded_deletion_record",
    "information_same_count_copy_substitution_is_rejected",
    "information_duplicate_known_copy_inventory_is_rejected",
    "information_copy_disposition_count_summary_collides",
    "information_exact_inventory_separates_count_collision",
    "no_exact_copy_deletion_classifier_from_count_only",
}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict) -> list[str]:
    errors: list[str] = []
    categories = set(record.get("minimization", {}).get("data_categories", []))
    necessary = set(record.get("minimization", {}).get("necessary_categories", []))
    if not categories or categories != necessary:
        errors.append("admitted data categories must equal the necessity decision")
    flow = record.get("flow_graph", {})
    required, mapped = set(flow.get("required_surfaces", [])), set(flow.get("mapped_surfaces", []))
    if required != mapped or not REQUIRED_SURFACES.issubset(required):
        errors.append("required lifecycle surfaces must be completely mapped")
    evaluation = record.get("privacy_evaluation", {})
    if set(evaluation.get("attack_families", [])) != REQUIRED_ATTACKS:
        errors.append("competent attack family packet drifted")
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("four-role source packet is incomplete or contaminated")
    if set(record.get("non_authorities", [])) != EXPECTED_NON_AUTHORITIES:
        errors.append("non-authority ceiling changed")
    receipt = record.get("rights_receipt", {})
    if receipt.get("legal_compliance_claimed") is not False:
        errors.append("rights receipt cannot claim legal compliance")
    if record.get("expected_route") != "accept_bounded_rights_receipt_without_compliance_claim":
        errors.append("baseline route must remain a bounded receipt")
    return errors


def validate(record: dict, schema: dict) -> list[str]:
    out = [f"schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(record)]
    return out + semantic_errors(record)


def validate_lean_surface() -> None:
    text = LEAN.read_text(encoding="utf-8")
    theorems = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", text, re.MULTILINE))
    expected = ROUTE_THEOREMS | LIFECYCLE_THEOREMS
    if theorems != expected:
        raise SystemExit(
            "Privacy Lean theorem surface drifted: "
            f"missing={sorted(expected - theorems)}, extra={sorted(theorems - expected)}."
        )
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/PrivacyInformationFlow.lean"],
        cwd=ROOT / "lean",
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise SystemExit("Privacy Lean recompilation failed:\n" + completed.stdout + completed.stderr)


def lifecycle_step(state: dict, event: dict) -> dict | None:
    identity = ("subject_id", "dataset_id", "purpose_lease_id", "jurisdiction_id")
    if any(event[field] != state[field] for field in identity):
        return None
    if event["known_copy_ids"] != state["known_copy_ids"]:
        return None
    if len(state["known_copy_ids"]) != len(set(state["known_copy_ids"])):
        return None
    if state["known_copies"] != len(state["known_copy_ids"]):
        return None
    if event["requested_authority"] > state["authority_ceiling"]:
        return None
    if event["legal_compliance_claimed"] or event["total_erasure_claimed"]:
        return None
    if event["support_requested"] or event["external_effect_authority_requested"]:
        return None
    if not event["residual_owner"]:
        return None
    transition = (state["stage"], event["kind"])
    if transition == ("collected", "bind_purpose"):
        valid = event["purpose_matches"] and event["authority_recorded"] and event["lease_active"]
        next_stage = "purpose_bound"
    elif transition == ("purpose_bound", "record_minimization"):
        valid = event["less_data_alternative_tested"]
        next_stage = "minimized"
    elif transition == ("minimized", "map_flows"):
        valid = (
            event["mapped_surfaces"] == event["required_surfaces"]
            and event["unknown_copies_recorded"]
            and event["derivative_obligations_propagated"]
        )
        next_stage = "flows_mapped"
    elif transition == ("flows_mapped", "evaluate_privacy"):
        valid = event["independent_evaluator"] and event["positive_controls_pass"] and event["attack_denominator_complete"]
        next_stage = "privacy_evaluated"
    elif transition == ("privacy_evaluated", "disposition_rights"):
        valid = (
            event["rights_identity_verified"]
            and event["exceptions_reviewed"]
            and event["recipient_notifications_complete"]
            and event["derivative_dispositions_complete"]
        )
        next_stage = "rights_dispositioned"
    elif transition == ("rights_dispositioned", "activate_use"):
        valid = event["outcomes_separated"]
        next_stage = "active"
    elif transition == ("active", "revoke_purpose"):
        valid = True
        next_stage = "revoked"
    elif transition == ("revoked", "record_deletion"):
        valid = (
            event["outcomes_separated"]
            and event["disposed_copies"] == state["known_copies"]
            and event["requested_disposed_copy_ids"] == state["known_copy_ids"]
        )
        next_stage = "deletion_recorded"
    else:
        return None
    if not valid:
        return None
    next_state = copy.deepcopy(state)
    next_state["stage"] = next_stage
    next_state["receipts"] += 1
    if event["kind"] == "activate_use":
        next_state["active_authority"] = event["requested_authority"]
    if event["kind"] == "revoke_purpose":
        next_state["active_authority"] = 0
    if event["kind"] == "record_deletion":
        next_state["disposed_copies"] = event["disposed_copies"]
        next_state["disposed_copy_ids"] = copy.deepcopy(event["requested_disposed_copy_ids"])
    return next_state


def process_lifecycle_event(state: dict, event: dict) -> tuple[dict, bool]:
    next_state = lifecycle_step(state, event)
    return (copy.deepcopy(state), False) if next_state is None else (next_state, True)


def validate_lifecycle_consumer() -> int:
    initial = {
        "stage": "collected",
        "subject_id": 10,
        "dataset_id": 20,
        "purpose_lease_id": 30,
        "jurisdiction_id": 40,
        "authority_ceiling": 3,
        "active_authority": 0,
        "known_copies": 4,
        "disposed_copies": 0,
        "known_copy_ids": [53, 59, 61, 67],
        "disposed_copy_ids": [],
        "receipts": 0,
        "support_count": 0,
        "external_effect_authority_count": 0,
    }

    def event(kind: str, **changes: object) -> dict:
        value = {
            "kind": kind,
            "subject_id": 10,
            "dataset_id": 20,
            "purpose_lease_id": 30,
            "jurisdiction_id": 40,
            "known_copy_ids": [53, 59, 61, 67],
            "requested_disposed_copy_ids": [53, 59, 61, 67],
            "requested_authority": 2,
            "purpose_matches": True,
            "authority_recorded": True,
            "lease_active": True,
            "less_data_alternative_tested": True,
            "required_surfaces": 12,
            "mapped_surfaces": 12,
            "unknown_copies_recorded": True,
            "derivative_obligations_propagated": True,
            "independent_evaluator": True,
            "positive_controls_pass": True,
            "attack_denominator_complete": True,
            "rights_identity_verified": True,
            "exceptions_reviewed": True,
            "recipient_notifications_complete": True,
            "derivative_dispositions_complete": True,
            "outcomes_separated": True,
            "residual_owner": True,
            "disposed_copies": 4,
            "legal_compliance_claimed": False,
            "total_erasure_claimed": False,
            "support_requested": False,
            "external_effect_authority_requested": False,
        }
        value.update(changes)
        return value

    events = [
        event("bind_purpose"),
        event("record_minimization"),
        event("map_flows"),
        event("evaluate_privacy"),
        event("disposition_rights"),
        event("activate_use"),
        event("revoke_purpose"),
        event("record_deletion"),
    ]
    states = [copy.deepcopy(initial)]
    for item in events:
        next_state = lifecycle_step(states[-1], item)
        if next_state is None:
            raise SystemExit("Independent privacy lifecycle did not close.")
        states.append(next_state)
    final = states[-1]
    identity = ("subject_id", "dataset_id", "purpose_lease_id", "jurisdiction_id", "authority_ceiling", "known_copies", "known_copy_ids")
    if any(final[field] != initial[field] for field in identity):
        raise SystemExit("Independent privacy lifecycle changed transaction identity.")
    if final["stage"] != "deletion_recorded" or final["active_authority"] != 0:
        raise SystemExit("Independent privacy lifecycle did not close authority before deletion recording.")
    if final["disposed_copies"] != final["known_copies"] or final["receipts"] != 8:
        raise SystemExit("Independent privacy lifecycle lost bounded copy or receipt accounting.")
    if final["disposed_copy_ids"] != final["known_copy_ids"]:
        raise SystemExit("Independent privacy lifecycle lost exact known-copy disposition identity.")
    if final["support_count"] != 0 or final["external_effect_authority_count"] != 0:
        raise SystemExit("Independent privacy lifecycle assigned support or external-effect authority.")

    controls = [
        (states[0], event("bind_purpose", purpose_matches=False)),
        (states[0], event("bind_purpose", dataset_id=21)),
        (states[0], event("bind_purpose", requested_authority=4)),
        (states[0], event("bind_purpose", support_requested=True)),
        (states[0], event("bind_purpose", legal_compliance_claimed=True)),
        (states[2], event("map_flows", mapped_surfaces=11)),
        (states[3], event("evaluate_privacy", independent_evaluator=False)),
        (states[4], event("disposition_rights", recipient_notifications_complete=False)),
        (states[5], event("record_deletion")),
        (states[7], event("record_deletion", disposed_copies=3)),
        (states[7], event("record_deletion", total_erasure_claimed=True)),
        (states[6], event("revoke_purpose", known_copy_ids=[53, 59, 61, 71])),
        (states[7], event("record_deletion", requested_disposed_copy_ids=[53, 59, 61, 71])),
        (
            {**states[7], "known_copy_ids": [53, 53, 61, 67]},
            event(
                "record_deletion",
                known_copy_ids=[53, 53, 61, 67],
                requested_disposed_copy_ids=[53, 53, 61, 67],
            ),
        ),
    ]
    for state, item in controls:
        processed, accepted = process_lifecycle_event(state, item)
        if accepted or processed != state:
            raise SystemExit("Independent privacy lifecycle accepted or mutated a rejecting control.")

    from itertools import permutations

    canonical = initial["known_copy_ids"]
    permutations_checked = 0
    accepted_permutations = 0
    for ordering in permutations(canonical):
        permutations_checked += 1
        candidate = lifecycle_step(
            states[7],
            event("record_deletion", requested_disposed_copy_ids=list(ordering)),
        )
        if candidate is not None:
            accepted_permutations += 1
            if list(ordering) != canonical:
                raise SystemExit("Independent privacy lifecycle accepted reordered copy identity.")
    if permutations_checked != 24 or accepted_permutations != 1:
        raise SystemExit("Independent privacy copy-inventory permutation denominator drifted.")

    valid_deletion = event("record_deletion")
    substituted = event("record_deletion", requested_disposed_copy_ids=[53, 59, 61, 71])
    if valid_deletion["disposed_copies"] != substituted["disposed_copies"]:
        raise SystemExit("Independent privacy count-collision witness lost equal count.")
    if valid_deletion["requested_disposed_copy_ids"] == substituted["requested_disposed_copy_ids"]:
        raise SystemExit("Independent privacy count-collision witness lost identity separation.")
    if lifecycle_step(states[7], valid_deletion) is None or lifecycle_step(states[7], substituted) is not None:
        raise SystemExit("Exact copy identity did not separate the count collision.")

    event_kinds = (
        "bind_purpose", "record_minimization", "map_flows", "evaluate_privacy",
        "disposition_rights", "activate_use", "revoke_purpose", "record_deletion",
    )
    if any(lifecycle_step(final, event(kind)) is not None for kind in event_kinds):
        raise SystemExit("Independent deletion-recorded state accepted a terminal event.")
    return len(controls), permutations_checked, len(event_kinds)


def main() -> None:
    validate_lean_surface()
    lifecycle_controls, inventory_permutations, terminal_event_kinds = validate_lifecycle_consumer()
    schema, record = load(SCHEMA), load(FIXTURE)
    baseline = validate(record, schema)
    if baseline:
        raise SystemExit("Baseline information lifecycle transaction failed:\n- " + "\n- ".join(baseline))
    mutations = [
        ("subject erased", lambda r: r["affected_parties"]["subject_records"].clear()),
        ("purpose inactive", lambda r: r["purpose_lease"].__setitem__("active", False)),
        ("purpose incompatible", lambda r: r["purpose_lease"].__setitem__("compatible_with_collection_purpose", False)),
        ("authority erased", lambda r: r["purpose_lease"].__setitem__("claimed_authority", "")),
        ("recipient erased", lambda r: r["purpose_lease"]["recipients"].clear()),
        ("minimization untested", lambda r: r["minimization"].__setitem__("less_data_alternative_tested", False)),
        ("necessary category drift", lambda r: r["minimization"]["necessary_categories"].append("extra")),
        ("flow omitted", lambda r: r["flow_graph"]["mapped_surfaces"].remove("backup")),
        ("unknown copies hidden", lambda r: r["flow_graph"].__setitem__("unknown_copies_recorded", False)),
        ("cross-user boundary unverified", lambda r: r["flow_graph"].__setitem__("cross_user_boundary_verified", False)),
        ("derivative obligation dropped", lambda r: r["flow_graph"].__setitem__("obligations_propagated", False)),
        ("privacy unit erased", lambda r: r["privacy_evaluation"].__setitem__("privacy_unit", "")),
        ("adjacency erased", lambda r: r["privacy_evaluation"].__setitem__("adjacency_relation", "")),
        ("budget unrecorded", lambda r: r["privacy_evaluation"].__setitem__("budget_recorded", False)),
        ("label-only attack omitted", lambda r: r["privacy_evaluation"]["attack_families"].remove("label-only-membership")),
        ("positive control failed", lambda r: r["privacy_evaluation"].__setitem__("positive_controls_passed", False)),
        ("evaluator dependent", lambda r: r["privacy_evaluation"].__setitem__("independent_evaluator", False)),
        ("attack denominator censored", lambda r: r["privacy_evaluation"].__setitem__("all_attempts_retained", False)),
        ("identity unverified", lambda r: r["rights_request"].__setitem__("identity_verified_proportionately", False)),
        ("exceptions skipped", lambda r: r["rights_request"].__setitem__("exceptions_reviewed", False)),
        ("recipient notification missing", lambda r: r["rights_receipt"].__setitem__("recipient_notifications_complete", False)),
        ("derivative disposition missing", lambda r: r["rights_receipt"].__setitem__("known_derivative_dispositions_complete", False)),
        ("compliance laundering", lambda r: r["rights_receipt"].__setitem__("legal_compliance_claimed", True)),
        ("residual owner erased", lambda r: r["rights_receipt"].__setitem__("residual_owner", "")),
        ("source role deletion", lambda r: r["source_ids"].pop()),
        ("non-authority deletion", lambda r: r["non_authorities"].pop()),
    ]
    survivors = []
    for name, mutate in mutations:
        changed = copy.deepcopy(record); mutate(changed)
        if not validate(changed, schema): survivors.append(name)
    if survivors:
        raise SystemExit("Privacy lifecycle mutations survived:\n- " + "\n- ".join(survivors))
    inventory = {row["id"] for row in load(ROOT / "sources/source_inventory.json")}
    missing = sorted(EXPECTED_SOURCES - inventory)
    notes = sorted(source for source in EXPECTED_SOURCES if not (ROOT / f"sources/source_notes/{source}.md").is_file())
    if missing or notes:
        raise SystemExit(f"Source packet incomplete: inventory={missing}, notes={notes}")
    print(
        "Information lifecycle transaction passed: exact 38-theorem Lean surface recompiled; "
        "purpose/authority, minimization, 12-surface flow, derivatives, privacy evaluation, "
        f"rights receipts, nine sources, ten non-authorities, 26 fixture mutations, and {lifecycle_controls} "
        f"lifecycle controls with exact state preservation, {inventory_permutations} known-copy inventory "
        f"permutations, and {terminal_event_kinds} deletion-recorded event kinds; no personal-data, "
        "privacy, compliance, total-erasure, support, or release claim."
    )


if __name__ == "__main__":
    main()
