#!/usr/bin/env python3
"""Validate the pre-outcome QCSA reference implementation freeze."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "roadmap_records/qcsa_reference_implementation_freeze.json"
FREEZE_SCHEMA = ROOT / "schemas/qcsa_reference_freeze.schema.json"
ADR = ROOT / "docs/qcsa_reference_architecture_decision.md"
MANIFEST = ROOT / "experiments/qcsa_reference/package_manifest.json"
MANIFEST_SCHEMA = ROOT / "schemas/qcsa_reference_package_manifest.schema.json"
BUDGET = ROOT / "experiments/qcsa_reference/budgets.json"
BUDGET_SCHEMA = ROOT / "schemas/qcsa_reference_budget.schema.json"
PLAN = ROOT / "experiments/qcsa_reference/test_plan.json"
PLAN_SCHEMA = ROOT / "schemas/qcsa_reference_test_plan.schema.json"
VALID = ROOT / "experiments/qcsa_reference/fixtures/envelope_examples.valid.json"
INVALID = ROOT / "experiments/qcsa_reference/fixtures/envelope_examples.expected_invalid.json"
ARTIFACT_SCHEMA = ROOT / "schemas/qcsa_reference_artifact.schema.json"

LANES = [f"QI-{index:02d}" for index in range(1, 13)]
FAMILIES = {
    "polysemy_and_same_name_identity",
    "paraphrase_and_cross_language_reference",
    "compositional_roles_negation_modality_quantity_time",
    "evidence_conflict_and_proposition_revision",
    "route_ambiguity_with_authority_differences",
    "migration_merge_split_stale_address_compatibility",
}
BASELINES = {
    "direct_inference_or_retrieval_without_semantic_address",
    "flat_lexical_retrieval_matched_corpus_and_budget",
    "flat_embedding_proxy_retrieval_matched_corpus_and_budget",
    "one_fixed_hierarchy",
    "random_tree",
    "frequency_derived_tree",
    "direct_clarification_without_adaptive_question_policy",
}
ABLATIONS = {
    "qcsa_without_plural_facets",
    "qcsa_without_active_questions",
    "qcsa_without_identity_address_indirection",
    "qcsa_without_certificate_residual_authority_fields",
    "qcsa_without_migration_compatibility",
}
ADAPTERS = {"retrieval", "model", "sensor", "specialist", "authority", "tool", "verification"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(value: dict, schema_path: Path) -> list[str]:
    schema = load(schema_path)
    return [error.message for error in Draft202012Validator(schema).iter_errors(value)]


def semantic_errors(data: dict) -> list[str]:
    errors: list[str] = []
    freeze = data["freeze"]
    manifest = data["manifest"]
    budget = data["budget"]
    plan = data["plan"]
    valid = data["valid"]
    invalid = data["invalid"]
    adr = data["adr"]

    for label, value, schema in [
        ("freeze", freeze, FREEZE_SCHEMA),
        ("manifest", manifest, MANIFEST_SCHEMA),
        ("budget", budget, BUDGET_SCHEMA),
        ("plan", plan, PLAN_SCHEMA),
    ]:
        for message in schema_errors(value, schema):
            errors.append(f"{label} schema: {message}")

    if freeze.get("lane_ids") != LANES:
        errors.append("freeze must bind QI-01 through QI-12 in order")
    lanes = manifest.get("lanes", [])
    if [row.get("id") for row in lanes] != LANES:
        errors.append("package manifest must bind QI-01 through QI-12 in order")
    if manifest.get("implementation_order") != LANES:
        errors.append("implementation order must be QI-01 through QI-12")
    if {row.get("state") for row in lanes} != {"frozen_unimplemented"}:
        errors.append("freeze may not represent a lane as implemented")
    if set(manifest.get("adapter_interfaces", [])) != ADAPTERS:
        errors.append("adapter boundary set drifted")
    if any(len(row.get("required_payload_fields", [])) != len(set(row.get("required_payload_fields", []))) for row in lanes):
        errors.append("lane payload contracts contain duplicate fields")

    artifacts = valid.get("artifacts", [])
    if [row.get("lane_id") for row in artifacts] != LANES:
        errors.append("valid fixture bundle must contain one ordered artifact per lane")
    for row in artifacts:
        for message in schema_errors(row, ARTIFACT_SCHEMA):
            errors.append(f"{row.get('lane_id')} artifact schema: {message}")
        lane = next((item for item in lanes if item.get("id") == row.get("lane_id")), {})
        if row.get("owner_chapters") != lane.get("owner_chapters"):
            errors.append(f"{row.get('lane_id')}: fixture owner drift")
        if row.get("payload", {}).get("frozen_required_fields") != lane.get("required_payload_fields"):
            errors.append(f"{row.get('lane_id')}: fixture payload contract drift")
        artifact_id = row.get("artifact_id", "")
        if any(token in artifact_id for token in ["bank", "dog", "finance", "label", "answer"]):
            errors.append(f"{row.get('lane_id')}: label-bearing fixture identifier")
    cases = invalid.get("cases", [])
    if [row.get("lane_id") for row in cases] != LANES or len({row.get("mutation") for row in cases}) != 12:
        errors.append("expected-invalid fixture must bind twelve distinct lane mutations")

    corpus = plan.get("corpus", {})
    if set(corpus.get("families", [])) != FAMILIES:
        errors.append("six-family corpus contract drifted")
    if (corpus.get("train_cases"), corpus.get("development_cases"), corpus.get("held_out_cases")) != (72, 48, 60):
        errors.append("72/48/60 split drifted")
    if set(plan.get("baselines", [])) != BASELINES:
        errors.append("matched baseline set drifted")
    if set(plan.get("ablations", [])) != ABLATIONS:
        errors.append("ablation set drifted")
    if plan.get("seeds") != [11, 29, 47]:
        errors.append("seed set drifted")
    evaluator = plan.get("evaluator_separation", {})
    if evaluator.get("candidate_path") == evaluator.get("independent_evaluator_path") or not evaluator.get("shared_candidate_code_forbidden"):
        errors.append("independent evaluator boundary collapsed")
    rules = plan.get("decision_rules", {})
    for key in ["advantage_gate", "resource_gate", "calibration_gate", "semantic_preservation_gate", "authority_gate", "migration_gate", "narrowing_gate", "statistics"]:
        if not rules.get(key):
            errors.append(f"missing frozen decision rule: {key}")
    if budget.get("service_spend_usd_max") != 0 or budget.get("network_calls_max") != 0:
        errors.append("zero-service/network freeze drifted")
    if budget.get("corpus_case_count") != 180 or budget.get("held_out_case_count") != 60 or budget.get("seed_count") != 3:
        errors.append("budget and corpus counts disagree")
    if freeze.get("outcome_access") != "unopened" or "outcomes_unopened" not in plan.get("state", ""):
        errors.append("freeze improperly opens outcomes")

    for phrase in [
        "Identity:",
        "Evidence:",
        "Address and route:",
        "Effect authority:",
        "No function may infer authority",
        "No address migration may silently retarget",
        "standard-library Python package",
    ]:
        if phrase not in adr:
            errors.append(f"architecture decision missing boundary: {phrase}")
    if freeze.get("support_state_effect") != "none" or manifest.get("support_state_effect") != "none":
        errors.append("freeze changes support state")
    return errors


def negative_controls(base: dict) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict]] = []

    missing_lane = copy.deepcopy(base)
    missing_lane["manifest"]["lanes"] = missing_lane["manifest"]["lanes"][:-1]
    mutations.append(("missing lane", missing_lane))

    label_leak = copy.deepcopy(base)
    label_leak["valid"]["artifacts"][0]["artifact_id"] = "qa:bank_finance"
    mutations.append(("label-bearing identifier", label_leak))

    opened = copy.deepcopy(base)
    opened["freeze"]["outcome_access"] = "opened"
    mutations.append(("outcomes opened", opened))

    budget_drift = copy.deepcopy(base)
    budget_drift["budget"]["held_out_case_count"] = 30
    mutations.append(("held-out budget drift", budget_drift))

    evaluator_collapse = copy.deepcopy(base)
    evaluator_collapse["plan"]["evaluator_separation"]["independent_evaluator_path"] = evaluator_collapse["plan"]["evaluator_separation"]["candidate_path"]
    mutations.append(("evaluator self-confirmation", evaluator_collapse))

    authority_missing = copy.deepcopy(base)
    authority_missing["manifest"]["adapter_interfaces"].remove("authority")
    mutations.append(("authority adapter erased", authority_missing))

    implemented_claim = copy.deepcopy(base)
    implemented_claim["manifest"]["lanes"][0]["state"] = "implemented"
    mutations.append(("premature implementation claim", implemented_claim))

    payload_drift = copy.deepcopy(base)
    payload_drift["valid"]["artifacts"][6]["payload"]["frozen_required_fields"].remove("rollback_identity")
    mutations.append(("migration rollback field erased", payload_drift))

    no_invalid = copy.deepcopy(base)
    no_invalid["invalid"]["cases"] = []
    mutations.append(("negative fixtures erased", no_invalid))

    support_promotion = copy.deepcopy(base)
    support_promotion["freeze"]["support_state_effect"] = "prototype-backed"
    mutations.append(("support promotion", support_promotion))

    for label, mutation in mutations:
        if not semantic_errors(mutation):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = [FREEZE, FREEZE_SCHEMA, ADR, MANIFEST, MANIFEST_SCHEMA, BUDGET, BUDGET_SCHEMA, PLAN, PLAN_SCHEMA, VALID, INVALID, ARTIFACT_SCHEMA]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA freeze artifacts: " + ", ".join(missing))
    base = {
        "freeze": load(FREEZE),
        "manifest": load(MANIFEST),
        "budget": load(BUDGET),
        "plan": load(PLAN),
        "valid": load(VALID),
        "invalid": load(INVALID),
        "adr": ADR.read_text(encoding="utf-8"),
    }
    errors = semantic_errors(base)
    errors.extend(negative_controls(base))
    if errors:
        raise SystemExit("\n".join(f"- {error}" for error in errors))
    print("QCSA implementation freeze passed: 12 frozen unimplemented lanes, 6 families, 180 cases with 60 held out, 7 matched baselines, 5 ablations, 3 seeds, zero network/service budget, separated evaluator, and 10 rejecting mutations; outcomes remain unopened.")


if __name__ == "__main__":
    main()
