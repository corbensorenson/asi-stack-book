#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/governed_operations_control_packet.schema.json"
CAMPAIGN_SCHEMA = ROOT / "schemas/governed_operations_campaign_preregistration.schema.json"
FIXTURE = ROOT / "tests/fixtures/protocol_records/governed_operations_control_packet.valid.json"
PROTOCOL = ROOT / "experiments/governed_operations_argument_exit/preregistration.json"
LEAN = ROOT / "lean/AsiStackProofs/GovernedOperations.lean"
CHAPTER = ROOT / "chapters/governed-operations-incident-command-and-graceful-degradation.qmd"
STATE_CLASSES = {"model", "optimizer", "scheduler", "rng", "cache", "memory", "credentials", "data", "replicas", "backups", "descendants"}
SOURCES = {"scf", "deterministic_capability_compilation", "theseus_operator_os", "viea", "talos", "platonic_world_model", "ext_nist_ai_rmf_1_0_2023", "ext_nist_deployed_ai_monitoring_2026", "ext_nist_incident_response_2025"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def authority_within(current: dict[str, Any], proposed: dict[str, Any]) -> bool:
    return (
        set(proposed["capabilities"]) <= set(current["capabilities"])
        and set(proposed["data_classes"]) <= set(current["data_classes"])
        and set(proposed["tools"]) <= set(current["tools"])
        and proposed["population_ceiling"] <= current["population_ceiling"]
        and proposed["duration_seconds"] <= current["duration_seconds"]
    )


def no_authority_leak(packet: dict[str, Any]) -> bool:
    return not any(packet["non_authorities"].values())


def degradation_route(packet: dict[str, Any]) -> str:
    identity = packet["identity"]
    if any(not identity[key] for key in identity):
        return "reject_identity"
    if not authority_within(packet["current_authority"], packet["proposed_degraded_authority"]):
        return "reject_authority_widening"
    lease = packet["command_lease"]
    if not lease["present"] or not lease["scope_bound"] or not no_authority_leak(packet):
        return "reject_lease"
    incident = packet["incident"]
    containment = packet["containment"]
    if not all((incident["declared"], incident["commander_bound"], incident["containment_independent_of_suspected_component"], incident["evidence_append_only"], containment["effective_path_observed"])) or containment["suspected_component_cooperation_required"]:
        return "request_containment"
    return "accept_degraded"


def recovery_route(packet: dict[str, Any]) -> str:
    if any(not value for value in packet["identity"].values()):
        return "reject_identity"
    state = packet["internal_state"]
    if set(state["required_classes"]) != STATE_CLASSES or set(state["reconciled_classes"]) != STATE_CLASSES or not state["descendant_inventory_complete"]:
        return "request_state_inventory"
    effects = packet["external_effects"]
    if any(effect["disposition"] == "unknown" or not effect["independently_observed"] for effect in effects):
        return "safe_hold"
    acceptance = packet["acceptance"]
    if not acceptance["effect_check_fresh"] or not acceptance["state_integrity_fresh"] or not acceptance["candidate_identity_exact"]:
        return "request_fresh_acceptance"
    if not acceptance["independent_verifier"]:
        return "request_independent_verifier"
    if not packet["command_lease"]["expired_before_recovery"]:
        return "request_emergency_expiry"
    if any(effect["disposition"] == "accepted_irreversible" for effect in effects) and not acceptance["irreversible_residual_accepted_by_authority"]:
        return "request_external_effect_disposition"
    if not acceptance["useful_service_check_fresh"] or not acceptance["safety_check_fresh"] or not packet["containment"]["fallback_qualified"] or not no_authority_leak(packet):
        return "safe_hold"
    return "accept_recovery"


def errors(packet: dict[str, Any], protocol: dict[str, Any], *, validate_schema: bool = True) -> list[str]:
    out: list[str] = []
    if validate_schema:
        schema_errors = sorted(Draft202012Validator(load(SCHEMA), format_checker=FormatChecker()).iter_errors(packet), key=lambda err: list(err.path))
        out.extend(f"schema: {error.message}" for error in schema_errors)
        protocol_schema_errors = sorted(
            Draft202012Validator(load(CAMPAIGN_SCHEMA)).iter_errors(protocol),
            key=lambda err: list(err.path),
        )
        out.extend(f"campaign schema: {error.message}" for error in protocol_schema_errors)
    if set(packet.get("source_ids", [])) != SOURCES:
        out.append("source denominator drifted")
    expected = packet.get("expected_routes", {})
    if degradation_route(packet) != expected.get("degradation"):
        out.append("degradation route mismatch")
    if recovery_route(packet) != expected.get("recovery"):
        out.append("recovery route mismatch")
    if expected.get("degradation") != "accept_degraded" or expected.get("recovery") != "safe_hold":
        out.append("authored joined-case disposition drifted")
    if (
        protocol.get("state")
        != "prospectively_frozen_outcomes_closed_implementation_and_development_pending"
        or protocol.get("maximum_negative_level") != "N3_exact"
    ):
        out.append("protocol state or negative ceiling drifted")
    expected_counts = {
        "arms": 5,
        "competence_gates": 9,
        "positive_controls": 6,
        "adversarial_controls": 10,
        "fair_rescue_steps": 7,
    }
    if any(len(protocol.get(key, [])) != count for key, count in expected_counts.items()):
        out.append("protocol denominator drifted")
    expected_arm_ids = [
        "direct_model_tooling",
        "stop_only",
        "competent_generic_sre",
        "proposal_plus_independent_acceptance",
        "governed_operations",
    ]
    if [arm.get("id") for arm in protocol.get("arms", [])] != expected_arm_ids:
        out.append("campaign arm identities or order drifted")
    population = protocol.get("population", {})
    if (
        population.get("development_task_count") != 15
        or population.get("heldout_task_count") != 40
        or population.get("heldout_tasks_per_family") != 8
        or population.get("task_content_opened") != 0
        or population.get("protected_outcomes_opened") is not False
    ):
        out.append("natural-task population or custody drifted")
    service = protocol.get("service", {})
    custody = service.get("model_custody", {})
    if (
        service.get("service_id") != "asi-stack-natural-repository-maintenance-v1"
        or len(service.get("task_families", [])) != 5
        or len(service.get("external_dependencies", [])) != 5
        or custody.get("repository") != "mlx-community/Qwen3-8B-4bit"
        or custody.get("snapshot_commit") != "545dc4251c05440727734bcd94334791f6ab0192"
        or custody.get("implementation") != "mlx_lm.generate 0.29.1"
        or len(custody.get("file_sha256", {})) != 4
    ):
        out.append("natural service or externally rooted model custody drifted")
    matching = protocol.get("matching", {})
    if (
        matching.get("all_five_arms_receive_same_task_and_fault") is not True
        or matching.get("same_model_snapshot_prompt_budget_tools_context_and_wall_clock")
        is not True
        or matching.get("arm_labels_blinded_from_evaluator") is not True
        or matching.get("public_effects_during_trials") is not False
    ):
        out.append("matched-arm or public-effect boundary drifted")
    evaluator = protocol.get("evaluator_and_monitor", {})
    if (
        evaluator.get("institutionally_independent") is not False
        or evaluator.get("independent_environment_truth") is not True
        or evaluator.get("calibration_minimum_cases") != 24
        or len(evaluator.get("calibration_requirements", [])) != 6
    ):
        out.append("evaluator independence or calibration boundary drifted")
    if len(protocol.get("fault_envelope", [])) != 12 or len(protocol.get("state_inventory", [])) != 14:
        out.append("fault envelope or full-state inventory drifted")
    outcomes = protocol.get("outcomes", {})
    analysis = protocol.get("analysis", {})
    if (
        len(outcomes.get("co_primary", [])) != 4
        or len(outcomes.get("secondary", [])) != 9
        or len(outcomes.get("costs", [])) != 11
        or outcomes.get("no_scalar_score_may_hide_a_co_primary_harm") is not True
        or analysis.get("primary_comparison") != "governed_operations_vs_competent_generic_sre"
        or analysis.get("minimum_heldout_blocks") != 40
    ):
        out.append("joint outcome, cost, or analysis contract drifted")
    heldout = protocol.get("heldout", {})
    execution = protocol.get("execution", {})
    if (
        heldout.get("protected_outcomes_opened") is not False
        or heldout.get("outcome_aware_changes_allowed") is not False
        or heldout.get("single_opening_after_all_gates") is not True
        or heldout.get("p2_q1_q2_denominator_overlap_allowed") is not False
        or heldout.get("p2_displacement_allowed") is not False
        or heldout.get("t4_substitution_allowed") is not False
    ):
        out.append("held-out or P2 isolation drifted")
    if any(execution.get(key) != 0 for key in ("natural_tasks_run", "fault_injections_run", "operators_recruited")) or execution.get("empirical_result") != "none":
        out.append("unearned empirical execution recorded")
    lean = LEAN.read_text(encoding="utf-8")
    if len(re.findall(r"(?m)^theorem ", lean)) != 13:
        out.append("Lean theorem denominator drifted")
    for fragment in ("accepted_degradation_preserves_or_narrows_all_authority_dimensions", "accepted_recovery_requires_complete_declared_state_effect_and_expiry", "incomplete_recovery_route_never_accepts"):
        if fragment not in lean:
            out.append(f"Lean semantic fragment missing: {fragment}")
    chapter = CHAPTER.read_text(encoding="utf-8")
    for fragment in ("authored joined authority-to-effect case", "record-shape and route evidence only", "thirteen theorem declarations"):
        if fragment not in chapter:
            out.append(f"chapter integration fragment missing: {fragment}")
    return out


def main() -> None:
    packet, protocol = load(FIXTURE), load(PROTOCOL)
    failures = errors(packet, protocol)
    completed = copy.deepcopy(packet)
    completed["external_effects"][1].update({"consequence_class": "monitorable", "disposition": "monitored", "independently_observed": True})
    completed["acceptance"]["effect_check_fresh"] = True
    completed["expected_routes"]["recovery"] = "accept_recovery"
    if recovery_route(completed) != "accept_recovery":
        failures.append("positive recovery control did not accept")
    mutations = [
        ("fixture", "widen capability", lambda p: p["proposed_degraded_authority"]["capabilities"].append("administer")),
        ("fixture", "widen data", lambda p: p["proposed_degraded_authority"]["data_classes"].append("secret")),
        ("fixture", "widen tool", lambda p: p["proposed_degraded_authority"]["tools"].append("network_admin")),
        ("fixture", "widen population", lambda p: p["proposed_degraded_authority"].__setitem__("population_ceiling", 101)),
        ("fixture", "widen duration", lambda p: p["proposed_degraded_authority"].__setitem__("duration_seconds", 3601)),
        ("fixture", "erase deployment", lambda p: p["identity"].__setitem__("deployment_id", "")),
        ("fixture", "erase command", lambda p: p["incident"].__setitem__("commander_bound", False)),
        ("fixture", "require cooperation", lambda p: p["containment"].__setitem__("suspected_component_cooperation_required", True)),
        ("complete", "drop state class", lambda p: p["internal_state"]["reconciled_classes"].pop()),
        ("complete", "stale state acceptance", lambda p: p["acceptance"].__setitem__("state_integrity_fresh", False)),
        ("complete", "dependent verifier", lambda p: p["acceptance"].__setitem__("independent_verifier", False)),
        ("complete", "active emergency lease", lambda p: p["command_lease"].__setitem__("expired_before_recovery", False)),
        ("complete", "unqualified fallback", lambda p: p["containment"].__setitem__("fallback_qualified", False)),
        ("fixture", "support laundering", lambda p: p["non_authorities"].__setitem__("support_promotion_requested", True)),
        ("fixture", "release laundering", lambda p: p["non_authorities"].__setitem__("release_requested", True)),
        ("fixture", "claim recovery", lambda p: p["expected_routes"].__setitem__("recovery", "accept_recovery")),
        ("fixture", "drop source", lambda p: p["source_ids"].pop()),
        ("fixture", "invent natural case", lambda p: p.__setitem__("case_kind", "natural_incident")),
    ]
    for base_name, label, mutation in mutations:
        base = completed if base_name == "complete" else packet
        baseline = set(errors(base, protocol))
        candidate = copy.deepcopy(base)
        mutation(candidate)
        if not set(errors(candidate, protocol)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    protocol_mutations = [
        ("open task content", lambda p: p["population"].__setitem__("task_content_opened", 1)),
        ("open protected outcomes", lambda p: p["heldout"].__setitem__("protected_outcomes_opened", True)),
        ("shrink denominator", lambda p: p["population"].__setitem__("heldout_task_count", 20)),
        ("drop strong baseline", lambda p: p["arms"].pop(2)),
        ("unmatch model", lambda p: p["matching"].__setitem__("same_model_snapshot_prompt_budget_tools_context_and_wall_clock", False)),
        ("allow public effect", lambda p: p["matching"].__setitem__("public_effects_during_trials", True)),
        ("invent institutional independence", lambda p: p["evaluator_and_monitor"].__setitem__("institutionally_independent", True)),
        ("drop calibration", lambda p: p["evaluator_and_monitor"].__setitem__("calibration_minimum_cases", 0)),
        ("drop fault", lambda p: p["fault_envelope"].pop()),
        ("drop state class", lambda p: p["state_inventory"].pop()),
        ("hide co-primary harm", lambda p: p["outcomes"].__setitem__("no_scalar_score_may_hide_a_co_primary_harm", False)),
        ("permit T4 substitution", lambda p: p["heldout"].__setitem__("t4_substitution_allowed", True)),
        ("invent execution", lambda p: p["execution"].__setitem__("natural_tasks_run", 1)),
        ("launder support", lambda p: p.__setitem__("support_state_effect", "promoted")),
        ("launder release", lambda p: p.__setitem__("release_effect", "authorized")),
    ]
    baseline = set(errors(packet, protocol))
    for label, mutation in protocol_mutations:
        candidate_protocol = copy.deepcopy(protocol)
        mutation(candidate_protocol)
        if not set(errors(packet, candidate_protocol)) - baseline:
            failures.append(f"campaign negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Governed operations control contract failed:\n - " + "\n - ".join(failures))
    print("Governed operations control contract passed: authored joined case, narrowed degradation accepted, unknown external effect held safe, completed positive recovery control accepted, 11 packet state classes, prospectively frozen 5-arm/40-task natural campaign with 14 campaign state classes, 18 packet plus 15 campaign mutations rejected, 13 Lean declarations; protected outcomes closed and no support/release/publication authority.")


if __name__ == "__main__":
    main()
