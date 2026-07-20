#!/usr/bin/env python3
"""Validate the bounded privacy lifecycle transaction and rejecting controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path
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


def main() -> None:
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
    print("Information lifecycle transaction passed: purpose/authority, minimization, 12-surface flow, derivatives, privacy evaluation, rights receipts, nine sources, ten non-authorities, and 26 rejecting mutations; no personal-data, privacy, compliance, support, or release claim.")


if __name__ == "__main__":
    main()
