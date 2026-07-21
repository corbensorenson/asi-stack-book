#!/usr/bin/env python3
"""Validate the authored optimizer-policy identity fixture and negative controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/optimizer_policy_card.schema.json"
FIXTURE = ROOT / "tests/fixtures/protocol_records/optimizer_policy_card.valid.json"
EXPECTED_SOURCES = {"ext_adamw_2019", "ext_muon_scalable_2025", "ext_muon_spectral_norm_2026"}
EXPECTED_DIMENSIONS = {
    "progress", "final_behavior", "resources", "stability",
    "tuning", "transfer", "recovery", "governance_cost",
}
EXPECTED_NON_AUTHORITIES = {
    "optimizer_superiority", "model_quality", "scale_transfer", "safety",
    "support_transition", "release_or_publication",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict) -> list[str]:
    errors: list[str] = []
    groups = record.get("parameter_groups", [])
    primary = [g for g in groups if g.get("role") == "primary"]
    fallback = [g for g in groups if g.get("role") == "fallback"]
    if len(primary) != 1 or primary[0].get("optimizer_family") != "muon":
        errors.append("authored Muon card requires one explicit Muon primary group")
    if len(fallback) != 1 or fallback[0].get("optimizer_family") != "adamw":
        errors.append("authored Muon card requires one explicit AdamW fallback group")
    if len({g.get("group_id") for g in groups}) != len(groups):
        errors.append("parameter group identities must be unique")

    state = set(record.get("state_classes", []))
    required_state = {
        "muon_momentum", "fallback_first_moment", "fallback_second_moment",
        "optimizer_step", "parameter_group_routing", "schedule_state",
        "approximation_configuration",
    }
    if not required_state.issubset(state):
        errors.append("optimizer state closure omits primary, fallback, routing, schedule, or approximation state")

    approximation = record.get("approximation", {})
    if approximation.get("method") != "newton_schulz" or approximation.get("iterations", 0) < 1:
        errors.append("authored Muon card must identify a nonempty Newton-Schulz approximation")
    if not approximation.get("coefficient_digest", "").startswith("sha256:"):
        errors.append("orthogonalization coefficients are not content-bound")

    transfer = record.get("parameterization", {}).get("transfer_axes_claimed", [])
    if "none" in transfer and len(transfer) != 1:
        errors.append("no-transfer declaration cannot be mixed with claimed transfer axes")

    if set(record.get("evaluation_dimensions", [])) != EXPECTED_DIMENSIONS:
        errors.append("joint optimizer evaluation dimensions are incomplete")
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("optimizer policy source packet drifted")
    if set(record.get("non_authorities", [])) != EXPECTED_NON_AUTHORITIES:
        errors.append("optimizer policy non-authority ceiling drifted")
    return errors


def validate(record: dict, schema: dict) -> list[str]:
    errors = [f"schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(record)]
    errors.extend(semantic_errors(record))
    return errors


def main() -> None:
    schema = load(SCHEMA)
    record = load(FIXTURE)
    baseline = validate(record, schema)
    if baseline:
        raise SystemExit("Optimizer policy baseline failed:\n- " + "\n- ".join(baseline))

    mutations: list[tuple[str, callable]] = [
        ("implementation identity erased", lambda r: r["implementation"].__setitem__("version_or_commit", "")),
        ("primary family substituted", lambda r: r["parameter_groups"][0].__setitem__("optimizer_family", "adamw")),
        ("fallback family substituted", lambda r: r["parameter_groups"][1].__setitem__("optimizer_family", "lion")),
        ("parameter routing erased", lambda r: r["checkpoint_contract"].__setitem__("parameter_routing_required", False)),
        ("fallback state omitted", lambda r: r["state_classes"].remove("fallback_second_moment")),
        ("schedule state omitted", lambda r: r["checkpoint_contract"].__setitem__("schedule_state_required", False)),
        ("approximation identity omitted", lambda r: r["checkpoint_contract"].__setitem__("approximation_configuration_required", False)),
        ("zero orthogonalization iterations", lambda r: r["approximation"].__setitem__("iterations", 0)),
        ("coefficient binding erased", lambda r: r["approximation"].__setitem__("coefficient_digest", "unbound")),
        ("communication accounting erased", lambda r: r["distributed_semantics"].__setitem__("communication_accounted", False)),
        ("unmatched tuning", lambda r: r["tuning_and_rescue"].__setitem__("matched_or_priced_against_baselines", False)),
        ("single-seed comparison", lambda r: r["tuning_and_rescue"].__setitem__("minimum_seed_count", 1)),
        ("post-outcome rescue", lambda r: r["tuning_and_rescue"].__setitem__("rescue_frozen_before_final", False)),
        ("positive controls removed", lambda r: r["tuning_and_rescue"].__setitem__("positive_controls_required", False)),
        ("evaluation dimension removed", lambda r: r["evaluation_dimensions"].pop()),
        ("transfer laundering", lambda r: r["parameterization"].__setitem__("transfer_axes_claimed", ["none", "architecture"])),
        ("source removed", lambda r: r["source_ids"].pop()),
        ("superiority authority invented", lambda r: r["non_authorities"].remove("optimizer_superiority")),
    ]
    survivors: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(record)
        mutate(candidate)
        if not validate(candidate, schema):
            survivors.append(name)
    if survivors:
        raise SystemExit("Optimizer policy mutations survived:\n- " + "\n- ".join(survivors))

    inventory = {row["id"] for row in load(ROOT / "sources/source_inventory.json")}
    missing_inventory = sorted(EXPECTED_SOURCES - inventory)
    missing_notes = sorted(s for s in EXPECTED_SOURCES if not (ROOT / f"sources/source_notes/{s}.md").is_file())
    if missing_inventory or missing_notes:
        raise SystemExit(f"Optimizer source packet incomplete: inventory={missing_inventory}, notes={missing_notes}")

    print(
        "Optimizer Policy Card passed: explicit Muon primary and AdamW fallback, "
        "seven state classes, content-bound Newton-Schulz approximation, matched "
        "three-seed tuning/rescue contract, eight joint evaluation dimensions, "
        "and 18/18 mutations rejected; authored identity fixture only, no optimizer result."
    )


if __name__ == "__main__":
    main()
