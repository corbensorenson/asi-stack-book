#!/usr/bin/env python3
"""Validate Campaign 5 evidence, bounded promotion, and laundering controls."""

from __future__ import annotations

import copy
from collections import Counter, defaultdict

import jsonschema

from p4_m8_world_model_common import ARMS, BASE, ROOT, SEEDS, load, sha


RESULT = BASE / "results/confirmatory_result.json"
RAW = BASE / "raw/campaign_run.json"
PREREG = BASE / "preregistration.json"
SCHEMA = ROOT / "schemas/p4_m8_world_model_result.schema.json"
TRANSITION = ROOT / "evidence_transitions/post_v2_3/situated_world_model_finite_pomdp_synthetic_test_backed.json"
REQUIRED_ARTIFACTS = {
    "environment_reference_state", "agent_input", "delivered_observation", "interpretation",
    "latent_hypothesis", "prediction", "prediction_error", "intervention",
    "causal_model_revision", "belief_transition", "curriculum_stage", "observed_effect", "consolidation",
}


def mean(values: list[float]) -> float: return sum(values) / len(values) if values else 0.0


def errors(result: dict, raw: dict, transition: dict) -> list[str]:
    out: list[str] = []
    prereg = load(PREREG)
    if result.get("preregistration_sha256") != sha(PREREG) or result.get("raw_run_sha256") != sha(RAW): out.append("result lineage")
    if raw.get("preregistration_sha256") != sha(PREREG) or raw.get("environment_sha256") != prereg.get("environments_sha256"): out.append("raw lineage")
    if raw.get("record_count") != 11250 or len(raw.get("records", [])) != 11250: out.append("episode denominator")
    if len(raw.get("agent_summaries", [])) != 100: out.append("agent-summary denominator")
    refs = [row.get("episode_ref") for row in raw.get("records", [])]
    if len(set(refs)) != 11250: out.append("episode identity")

    heldout: dict[tuple[str, int, str], list[dict]] = defaultdict(list)
    recomputed: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in raw.get("records", []):
        artifact = row.get("artifact", {})
        if set(artifact) != REQUIRED_ARTIFACTS: out.append("artifact separation"); break
        ref, agent_input = artifact["environment_reference_state"], artifact["agent_input"]
        if ref.get("evaluator_only") is not True or agent_input.get("contains_reference_state") is not False: out.append("reference leak"); break
        if not (ref.get("entity_id") == row.get("entity_id") == agent_input.get("entity_id")): out.append("identity binding"); break
        budget = row.get("budget", {})
        if budget.get("information_actions_used", 10**9) > budget.get("max_information_actions", -1) or budget.get("interventions_used", 10**9) > budget.get("max_interventions", -1) or budget.get("compute_proxy_used", 10**9) > budget.get("compute_proxy_ceiling", -1): out.append("authority budget"); break
        effect, pred = artifact["observed_effect"], artifact["prediction"]
        required = effect.get("required_action")
        if effect.get("success") != (effect.get("terminal_action") == required) or effect.get("unsafe_action") != (effect.get("terminal_action") != "escalate" and effect.get("terminal_action") != required): out.append("replay fidelity"); break
        if row.get("phase") == "heldout":
            heldout[(row["environment_id"], row["seed"], row["arm"])].append(row)
            recomputed[(row["environment_id"], row["arm"])].append({"correct": pred["predicted_state"] == ref["hidden_state"], "success": effect["success"], "unsafe": effect["unsafe_action"], "brier": artifact["prediction_error"]["brier"]})
    if set(heldout) != {(e, s, a) for e in ("adaptive_workshop", "service_mesh_transfer") for s in SEEDS for a in ARMS} or any(len(rows) != 60 for rows in heldout.values()): out.append("heldout matrix")
    if sum(len(rows) for rows in heldout.values()) != 6000: out.append("heldout denominator")

    aggregate = result.get("aggregate", {})
    for (env, arm), rows in recomputed.items():
        expected = aggregate.get(env, {}).get(arm, {})
        for key, values in (("hidden_state_accuracy", [x["correct"] for x in rows]), ("task_success_rate", [x["success"] for x in rows]), ("unsafe_action_rate", [x["unsafe"] for x in rows]), ("mean_brier", [x["brier"] for x in rows])):
            if expected.get(key, {}).get("mean") != round(mean(values), 8): out.append(f"aggregate recomputation:{env}:{arm}:{key}")

    summaries = raw.get("agent_summaries", [])
    governed = [x for x in summaries if x.get("arm") == "governed_world_model"]
    if len(governed) != 10 or sum(x.get("memory_replacement_exact") is True for x in governed) != 10 or sum(x.get("rollback_probe_exact") is True for x in governed) != 10: out.append("governed replacement/rollback")
    for summary in governed:
        consolidations = summary.get("consolidations", [])
        if not consolidations or any(not x.get("supporting_episode_refs") or "contradicting_episode_refs" not in x for x in consolidations): out.append("consolidation evidence"); break
        if any(x.get("version", 0) > 1 and not x.get("supersedes") for x in consolidations): out.append("consolidation lineage"); break

    gate = result.get("gate_checks", {})
    if gate != {"all_records_replay_faithful": True, "all_authority_budgets_conform": True, "reference_leak_count": 0, "governed_replacement_exact_count": 10, "governed_rollback_exact_count": 10, "environment_count": 2, "seed_count": 5, "arm_count": 10, "heldout_episode_count": 6000}: out.append("gate receipt")
    adjudication = result.get("primary_gate_adjudication", {})
    if adjudication.get("all_primary_gates_pass") is not True or adjudication.get("disposition") != "bounded_non_core_promotion_review_open" or adjudication.get("directional_ablation_signature_count") != 6 or not all(adjudication.get("directional_ablation_signatures", {}).values()): out.append("frozen adjudication")
    if result.get("support_state_effect") != "none_pending_adjudication" or result.get("publication_authority") != "none" or result.get("release_authority") != "none": out.append("result authority")

    if transition.get("claim_id") != "situated-world-model.finite-pomdp-governed-acquisition-and-consolidation" or transition.get("new_support_state") != "synthetic-test-backed" or transition.get("support_state_effect") != "eligible_for_bounded_evidence_review": out.append("transition identity")
    if (
        transition.get("transition_validity_state") != "review_accepted"
        or transition.get("review_status") != "accepted"
        or transition.get("transition_effect") != "upward"
        or transition.get("old_support_state") != "argument"
    ): out.append("transition boundary")
    if "does not authorize publication, release" not in " ".join(transition.get("non_claims", [])).lower(): out.append("transition authority")
    nonclaims = " ".join(transition.get("non_claims", []))
    for phrase in ("neural world model", "open-world", "transfer beyond", "deployment safety", "SOTA", "AGI", "ASI", "chapter core"):
        if phrase not in nonclaims: out.append(f"transition non-claim:{phrase}")
    return out


def main() -> None:
    result, raw, transition = load(RESULT), load(RAW), load(TRANSITION)
    jsonschema.validate(result, load(SCHEMA))
    failures = errors(result, raw, transition)
    mutations = (
        ("result heldout inflation", result, lambda x: x["gate_checks"].__setitem__("heldout_episode_count", 6001)),
        ("result disposition laundering", result, lambda x: x["primary_gate_adjudication"].__setitem__("disposition", "general_world_model_proved")),
        ("result ablation inflation", result, lambda x: x["primary_gate_adjudication"].__setitem__("directional_ablation_signature_count", 5)),
        ("result aggregate rewrite", result, lambda x: x["aggregate"]["adaptive_workshop"]["governed_world_model"]["hidden_state_accuracy"].__setitem__("mean", 1.0)),
        ("transition core promotion", transition, lambda x: x.__setitem__("claim_id", "planning-as-a-control-layer.core")),
        ("transition scope inflation", transition, lambda x: x.__setitem__("new_support_state", "empirical-test-backed")),
        ("transition review erasure", transition, lambda x: x.__setitem__("review_status", "open")),
    )
    for label, source, mutate in mutations:
        candidate_result, candidate_transition = copy.deepcopy(result), copy.deepcopy(transition)
        target = candidate_result if source is result else candidate_transition
        mutate(target)
        if not errors(candidate_result, raw, candidate_transition): failures.append(f"mutation accepted:{label}")

    first = raw["records"][0]
    for label, mutate, restore in (
        ("reference leak", lambda: first["artifact"]["agent_input"].__setitem__("contains_reference_state", True), lambda: first["artifact"]["agent_input"].__setitem__("contains_reference_state", False)),
        ("identity swap", lambda: first["artifact"]["agent_input"].__setitem__("entity_id", "alien"), lambda: first["artifact"]["agent_input"].__setitem__("entity_id", first["entity_id"])),
        ("authority overflow", lambda: first["budget"].__setitem__("information_actions_used", 4), lambda: first["budget"].__setitem__("information_actions_used", len(first["artifact"]["delivered_observation"]))),
    ):
        mutate()
        if not errors(result, raw, transition): failures.append(f"mutation accepted:{label}")
        restore()
    if failures: raise SystemExit("P4/M8 Campaign 5 validation failed:\n - " + "\n - ".join(dict.fromkeys(failures)))
    print("P4/M8 Campaign 5 validation passed: 11,250 episodes, 6,000 heldout, 10/10 governed replacement/rollback, six directional signatures, 10 laundering mutations rejected, one bounded non-core promotion, zero chapter-core movement.")


if __name__ == "__main__":
    main()
