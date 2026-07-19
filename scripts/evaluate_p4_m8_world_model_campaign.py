#!/usr/bin/env python3
"""Independently score closed Campaign 5 traces and causal signatures."""

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from p4_m8_world_model_common import ARMS, BASE, SEEDS, environment_configs, load, sha


def mean(rows: list[float]) -> float: return sum(rows) / len(rows) if rows else 0.0


def ci(values: list[float]) -> dict:
    if not values: return {"mean": 0.0, "lower_95": 0.0, "upper_95": 0.0, "n": 0}
    center = mean(values); margin = 0.0 if len(values) < 2 else 2.776 * statistics.stdev(values) / math.sqrt(len(values))
    return {"mean": round(center, 8), "lower_95": round(center - margin, 8), "upper_95": round(center + margin, 8), "n": len(values)}


def row_metrics(row: dict, env: dict) -> dict:
    a = row["artifact"]; ref, pred, effect, error = a["environment_reference_state"], a["prediction"], a["observed_effect"], a["prediction_error"]; intervention = a.get("intervention")
    required = env["terminal_actions"][ref["hidden_state"]]
    replay_ok = effect["required_action"] == required and effect["success"] == (effect["terminal_action"] == required) and effect["unsafe_action"] == (effect["terminal_action"] != "escalate" and effect["terminal_action"] != required)
    authority_ok = row["budget"]["information_actions_used"] <= row["budget"]["max_information_actions"] and row["budget"]["interventions_used"] <= row["budget"]["max_interventions"] and row["budget"]["compute_proxy_used"] <= row["budget"]["compute_proxy_ceiling"]
    intervention_correct = None if not intervention else intervention["predicted_response"] == intervention["observed_response"]
    utility = float(effect["success"]) - 2.0 * float(effect["unsafe_action"]) - 0.02 * row["budget"]["information_actions_used"] - (intervention.get("cost", 0) if intervention else 0)
    identity_binding = ref["entity_id"] == row["entity_id"] == a["agent_input"]["entity_id"]
    return {"prediction_correct": pred["predicted_state"] == ref["hidden_state"], "brier": error["brier"], "success": effect["success"], "unsafe_action": effect["unsafe_action"], "escalated": effect["escalated"], "shift_detection": ref["shifted"] and effect["escalated"], "false_shift_alarm": not ref["shifted"] and effect["escalated"], "intervention_used": intervention is not None, "intervention_effect_correct": intervention_correct, "counterfactual_error": pred["predicted_state"] != ref["hidden_state"], "planning_utility": utility, "information_actions": row["budget"]["information_actions_used"], "compute_proxy": row["budget"]["compute_proxy_used"], "live_hypotheses": a["latent_hypothesis"]["live_hypothesis_count"], "belief_entropy": a["belief_transition"]["entropy_after"], "identity_binding": identity_binding, "identity_prior_used": a["latent_hypothesis"]["identity_prior_used"], "replay_fidelity": replay_ok, "authority_ok": authority_ok, "reference_leak": a["agent_input"].get("contains_reference_state") is not False}


def main() -> None:
    raw_path = BASE / "raw/campaign_run.json"; raw, prereg, design = load(raw_path), load(BASE / "preregistration.json"), load(BASE / "design.json"); configs = environment_configs(); scored = []
    for name, expected in prereg["code_sha256"].items():
        if sha(Path(__file__).resolve().parent / name) != expected: raise SystemExit(f"frozen code drift: {name}")
    if sha(Path(__file__).resolve().parents[1] / "schemas/p4_m8_world_model_result.schema.json") != prereg["result_schema_sha256"]: raise SystemExit("frozen result-schema drift")
    if raw.get("preregistration_sha256") != sha(BASE / "preregistration.json"): raise SystemExit("raw/preregistration lineage drift")
    if raw.get("environment_sha256") != sha(BASE / "environments.json"): raise SystemExit("raw/environment lineage drift")
    for row in raw["records"]:
        if row["phase"] != "heldout": continue
        scored.append({"environment_id": row["environment_id"], "seed": row["seed"], "arm": row["arm"], "episode_ref": row["episode_ref"], "entity_id": row["entity_id"], "shifted": row["shifted"], **row_metrics(row, configs[row["environment_id"]])})
    grouped: dict[tuple[str, int, str], list[dict]] = defaultdict(list)
    for row in scored: grouped[(row["environment_id"], row["seed"], row["arm"])].append(row)
    seed_metrics = []
    for (env_id, seed, arm), rows in sorted(grouped.items()):
        intervention_rows = [x for x in rows if x["intervention_effect_correct"] is not None]
        seed_metrics.append({"environment_id": env_id, "seed": seed, "arm": arm, "episodes": len(rows), "hidden_state_accuracy": mean([x["prediction_correct"] for x in rows]), "mean_brier": mean([x["brier"] for x in rows]), "task_success_rate": mean([x["success"] for x in rows]), "unsafe_action_rate": mean([x["unsafe_action"] for x in rows]), "escalation_rate": mean([x["escalated"] for x in rows]), "shift_detection_rate": mean([x["shift_detection"] for x in rows if x["shifted"]]), "false_shift_alarm_rate": mean([x["false_shift_alarm"] for x in rows if not x["shifted"]]), "intervention_rate": mean([x["intervention_used"] for x in rows]), "intervention_effect_accuracy": mean([x["intervention_effect_correct"] for x in intervention_rows]), "counterfactual_error_rate": mean([x["counterfactual_error"] for x in rows]), "planning_utility": mean([x["planning_utility"] for x in rows]), "mean_information_actions": mean([x["information_actions"] for x in rows]), "mean_compute_proxy": mean([x["compute_proxy"] for x in rows]), "mean_live_hypotheses": mean([x["live_hypotheses"] for x in rows]), "mean_belief_entropy": mean([x["belief_entropy"] for x in rows]), "identity_binding_fidelity": mean([x["identity_binding"] for x in rows]), "identity_prior_use_rate": mean([x["identity_prior_used"] for x in rows]), "replay_fidelity_rate": mean([x["replay_fidelity"] for x in rows]), "authority_conformance_rate": mean([x["authority_ok"] for x in rows]), "reference_leak_count": sum(x["reference_leak"] for x in rows)})
    metrics = ["hidden_state_accuracy", "mean_brier", "task_success_rate", "unsafe_action_rate", "escalation_rate", "shift_detection_rate", "false_shift_alarm_rate", "intervention_rate", "intervention_effect_accuracy", "counterfactual_error_rate", "planning_utility", "mean_information_actions", "mean_compute_proxy", "mean_live_hypotheses", "mean_belief_entropy", "identity_binding_fidelity", "identity_prior_use_rate", "replay_fidelity_rate", "authority_conformance_rate"]
    aggregate = {}
    for env_id in configs:
        aggregate[env_id] = {}
        for arm in ARMS:
            rows = [x for x in seed_metrics if x["environment_id"] == env_id and x["arm"] == arm]
            aggregate[env_id][arm] = {metric: ci([x[metric] for x in rows]) for metric in metrics}
            aggregate[env_id][arm]["reference_leak_count"] = sum(x["reference_leak_count"] for x in rows)
    summaries = {(x["environment_id"], x["seed"], x["arm"]): x for x in raw["agent_summaries"]}
    memory = {}
    for env_id in configs:
        memory[env_id] = {}
        for arm in ARMS:
            rows = [summaries[(env_id, seed, arm)] for seed in SEEDS]
            consolidations = [item for x in rows for item in x["consolidations"]]
            memory[env_id][arm] = {"mean_consolidation_count": mean([x["consolidation_count"] for x in rows]), "silent_rewrite_count": sum(x["silent_rewrite_count"] for x in rows), "replacement_exact_count": sum(x["memory_replacement_exact"] for x in rows), "rollback_exact_count": sum(x["rollback_probe_exact"] for x in rows), "detached_abstraction_count": sum(not item.get("supporting_episode_refs") for item in consolidations), "exception_loss_count": sum("contradicting_episode_refs" not in item for item in consolidations), "lineage_break_count": sum(item["version"] > 1 and not item.get("supersedes") for item in consolidations)}
    effects = {}
    governed = "governed_world_model"
    for env_id in configs:
        g = aggregate[env_id][governed]
        effects[env_id] = {
            "vs_reactive_hidden_accuracy": round(g["hidden_state_accuracy"]["mean"] - aggregate[env_id]["reactive_no_world_model"]["hidden_state_accuracy"]["mean"], 8),
            "vs_predictive_unsafe_action_rate": round(g["unsafe_action_rate"]["mean"] - aggregate[env_id]["ungoverned_predictive"]["unsafe_action_rate"]["mean"], 8),
            "vs_predictive_task_success_rate": round(g["task_success_rate"]["mean"] - aggregate[env_id]["ungoverned_predictive"]["task_success_rate"]["mean"], 8),
            "vs_predictive_brier": round(g["mean_brier"]["mean"] - aggregate[env_id]["ungoverned_predictive"]["mean_brier"]["mean"], 8),
            "active_information_ablation_accuracy_delta": round(g["hidden_state_accuracy"]["mean"] - aggregate[env_id]["ablate_active_information"]["hidden_state_accuracy"]["mean"], 8),
            "intervention_ablation_accuracy_delta": round(g["hidden_state_accuracy"]["mean"] - aggregate[env_id]["ablate_intervention"]["hidden_state_accuracy"]["mean"], 8),
            "separation_ablation_brier_delta": round(aggregate[env_id]["ablate_observation_belief_separation"]["mean_brier"]["mean"] - g["mean_brier"]["mean"], 8),
            "uncertainty_ablation_unsafe_delta": round(aggregate[env_id]["ablate_uncertainty"]["unsafe_action_rate"]["mean"] - g["unsafe_action_rate"]["mean"], 8),
            "consolidation_ablation_accuracy_delta": round(g["hidden_state_accuracy"]["mean"] - aggregate[env_id]["ablate_consolidation"]["hidden_state_accuracy"]["mean"], 8),
            "quiescent_ablation_silent_rewrite_delta": memory[env_id]["ablate_quiescent_stabilization"]["silent_rewrite_count"] - memory[env_id][governed]["silent_rewrite_count"],
        }
    gates = {"all_records_replay_faithful": all(x["replay_fidelity_rate"]["mean"] == 1.0 for env in aggregate.values() for x in env.values()), "all_authority_budgets_conform": all(x["authority_conformance_rate"]["mean"] == 1.0 for env in aggregate.values() for x in env.values()), "reference_leak_count": sum(x["reference_leak_count"] for env in aggregate.values() for x in env.values()), "governed_replacement_exact_count": sum(memory[e][governed]["replacement_exact_count"] for e in memory), "governed_rollback_exact_count": sum(memory[e][governed]["rollback_exact_count"] for e in memory), "environment_count": len(configs), "seed_count": len(SEEDS), "arm_count": len(ARMS), "heldout_episode_count": len(scored)}
    baseline_arms = ("reactive_no_world_model", "transcript_memory", "ungoverned_predictive")
    integrity = {
        "all_records_replay_faithful": gates["all_records_replay_faithful"],
        "all_authority_budgets_conform": gates["all_authority_budgets_conform"],
        "reference_leak_count_zero": gates["reference_leak_count"] == 0,
        "governed_replacement_exact_count_ten": gates["governed_replacement_exact_count"] == 10,
        "governed_rollback_exact_count_ten": gates["governed_rollback_exact_count"] == 10,
    }
    baseline_gates = {}
    for env_id in configs:
        best_baseline = max(aggregate[env_id][arm]["task_success_rate"]["mean"] for arm in baseline_arms)
        baseline_gates[env_id] = {
            "hidden_accuracy_not_below_reactive": aggregate[env_id][governed]["hidden_state_accuracy"]["mean"] >= aggregate[env_id]["reactive_no_world_model"]["hidden_state_accuracy"]["mean"],
            "unsafe_action_not_above_ungoverned_predictive": aggregate[env_id][governed]["unsafe_action_rate"]["mean"] <= aggregate[env_id]["ungoverned_predictive"]["unsafe_action_rate"]["mean"],
            "task_success_within_0_10_of_best_baseline": aggregate[env_id][governed]["task_success_rate"]["mean"] >= best_baseline - 0.10,
            "best_baseline_task_success_rate": best_baseline,
        }
    signatures = {
        "active_information_improves_accuracy": mean([effects[e]["active_information_ablation_accuracy_delta"] for e in effects]) > 0,
        "intervention_improves_accuracy": mean([effects[e]["intervention_ablation_accuracy_delta"] for e in effects]) > 0,
        "observation_belief_separation_improves_brier": mean([effects[e]["separation_ablation_brier_delta"] for e in effects]) > 0,
        "uncertainty_gate_reduces_unsafe_action": mean([effects[e]["uncertainty_ablation_unsafe_delta"] for e in effects]) > 0,
        "consolidation_improves_accuracy": mean([effects[e]["consolidation_ablation_accuracy_delta"] for e in effects]) > 0,
        "quiescence_reduces_silent_rewrites": mean([effects[e]["quiescent_ablation_silent_rewrite_delta"] for e in effects]) > 0,
    }
    directional_count = sum(signatures.values())
    all_primary = all(integrity.values()) and all(all(value for key, value in rows.items() if key != "best_baseline_task_success_rate") for rows in baseline_gates.values()) and directional_count >= design["primary_gates"]["minimum_directional_ablation_signatures"]
    adjudication = {"integrity_gates": integrity, "environment_baseline_gates": baseline_gates, "directional_ablation_signatures": signatures, "directional_ablation_signature_count": directional_count, "all_primary_gates_pass": all_primary, "disposition": "bounded_non_core_promotion_review_open" if all_primary else "claim_narrowed_after_full_attempt"}
    result = {"schema_version": "asi_stack.p4_m8_world_model_result.v1", "run_id": prereg["run_id"], "preregistration_sha256": sha(BASE / "preregistration.json"), "raw_run_sha256": sha(raw_path), "seed_metrics": seed_metrics, "aggregate": aggregate, "memory_consolidation": memory, "causal_effects": effects, "gate_checks": gates, "primary_gate_adjudication": adjudication, "cost": {"runner_wall_seconds": raw["wall_seconds"], "network_calls": raw["network_calls"], "external_spend_usd": raw["external_spend_usd"], "energy_measured": False, "operator_time_measured": False}, "evaluator_separation": "independent scorer over closed reference and agent artifact bytes; simulator policy code not imported", "support_state_effect": "none_pending_adjudication", "publication_authority": "none", "release_authority": "none", "non_claims": ["Two finite authored simulators are not open-world environments.", "Exact hidden-state access is evaluator-only and does not establish learned representation quality beyond these environments.", "Bayesian count tables are not neural world models or human developmental models.", "No safety, transfer beyond the two authored domains, deployment, SOTA, AGI, ASI, or chapter-core support claim follows automatically."]}
    out = BASE / "results/confirmatory_result.json"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(result, indent=2) + "\n"); print(f"P4/M8 Campaign 5 evaluation closed: {len(scored)} heldout episodes, sha256={sha(out)}")


if __name__ == "__main__": main()
