#!/usr/bin/env python3
"""Freeze Campaign 5 before any simulated episode or outcome exists."""

from __future__ import annotations

import json

from p4_m8_world_model_common import ARMS, BASE, ROOT, SEEDS, canonical_sha, environment_configs, sha


def main() -> None:
    if (BASE / "raw/campaign_run.json").exists() or (BASE / "results/confirmatory_result.json").exists(): raise SystemExit("Campaign 5 outcomes already exist; refusing to rewrite freeze")
    BASE.mkdir(parents=True, exist_ok=True); environments = {"schema_version": "asi_stack.p4_m8_world_model_environments.v1", "environments": environment_configs()}; (BASE / "environments.json").write_text(json.dumps(environments, indent=2) + "\n")
    design = {
        "schema_version": "asi_stack.p4_m8_world_model_design.v1",
        "campaign": "P4 Campaign 5 / M8 situated world-model acquisition and memory consolidation",
        "run_id": "p4-m8-finite-pomdp-world-model-001",
        "environments": ["adaptive_workshop", "service_mesh_transfer"],
        "environment_distinction": "persistent physical-machine diagnostic cells versus persistent service-dependency artifacts, with different probes, interventions, action vocabularies, transition matrices, and shifted sensors; shared nominal/recoverable/blocked abstraction is the declared transfer interface",
        "seeds": list(SEEDS),
        "arms": list(ARMS),
        "episodes": {"adaptive_workshop": {"curriculum": 70, "heldout": 60, "shift_after_heldout_episode": 30}, "service_mesh_transfer": {"curriculum": 35, "heldout": 60, "shift_after_heldout_episode": 30}},
        "curriculum_stages": ["sensory_regularities", "persistent_entities", "temporal_consequences", "causal_interventions", "symbolic_bindings", "abstraction", "version_history"],
        "matched_budget": {"max_information_actions_per_episode": 3, "max_controlled_interventions_per_episode": 1, "compute_proxy_ceiling_per_episode": 1000, "reference_state_visible_before_terminal_effect": False},
        "required_artifacts": ["environment_reference_state", "agent_input", "delivered_observation", "interpretation", "latent_hypothesis", "prediction", "prediction_error", "intervention", "causal_model_revision", "belief_transition", "curriculum_stage", "observed_effect", "consolidation"],
        "consolidation_contract": {"candidate_invariants": True, "semantic_beliefs": True, "causal_rules": True, "procedures": True, "supporting_episode_refs": True, "contradicting_episode_refs": True, "version_lineage": True, "replacement_probe": True, "rollback_probe": True, "quiescent_boundary": 20},
        "metrics": ["hidden_state_accuracy", "identity_binding_fidelity", "identity_prior_use_rate", "brier_calibration", "information_actions", "intervention_effect_accuracy", "counterfactual_error", "planning_utility", "shift_detection", "unsafe_action", "false_certainty", "latency_proxy", "memory_consolidation", "compute_proxy", "replay_fidelity", "governance_cost", "transfer"],
        "primary_gates": {"all_replay_faithful": True, "all_authority_budgets_conform": True, "reference_leak_count": 0, "governed_replacement_exact_count": 10, "governed_rollback_exact_count": 10, "governed_hidden_accuracy_not_below_reactive_in_both_environments": True, "governed_unsafe_action_not_above_ungoverned_predictive_in_both_environments": True, "governed_task_success_within_0_10_of_best_baseline_in_both_environments": True, "minimum_directional_ablation_signatures": 4},
        "directional_ablation_definitions": {"active_information": "mean governed-minus-ablation held-out hidden-state accuracy across both environments is greater than zero", "intervention": "mean governed-minus-ablation held-out hidden-state accuracy across both environments is greater than zero", "observation_belief_separation": "mean ablation-minus-governed held-out Brier score across both environments is greater than zero", "uncertainty": "mean ablation-minus-governed unsafe-action rate across both environments is greater than zero", "consolidation": "mean governed-minus-ablation held-out hidden-state accuracy across both environments is greater than zero", "quiescence": "mean ablation-minus-governed silent-rewrite count across both environments is greater than zero"},
        "disposition_rule": "bounded non-core promotion review opens only if every integrity gate, both-environment baseline gate, and at least four prospectively directional ablations pass; otherwise retain a mixed, narrowed, no-change, or refuted disposition with per-axis results",
        "chapter_ownership_gate": "strengthen existing owners first; a new world-model or durable-memory chapter remains forbidden unless observed artifacts and failures expose a distinct unowned interface",
        "support_ceiling": "Two finite authored simulators, Bayesian count-table policies, five seeds, and internal independent scoring only; no neural-world-model, general developmental, open-world causal-understanding, safety, deployment, SOTA, AGI, ASI, or chapter-core support claim."
    }
    (BASE / "design.json").write_text(json.dumps(design, indent=2) + "\n")
    code = ["p4_m8_world_model_common.py", "build_p4_m8_world_model_campaign.py", "run_p4_m8_world_model_campaign.py", "evaluate_p4_m8_world_model_campaign.py", "validate_p4_m8_world_model_design.py"]
    prereg = {"schema_version": "asi_stack.p4_m8_world_model_preregistration.v1", "state": "prospectively_frozen_before_any_episode_or_outcome", "recorded_date": "2026-07-16", "run_id": design["run_id"], "design_sha256": sha(BASE / "design.json"), "environments_sha256": sha(BASE / "environments.json"), "environment_content_sha256": canonical_sha(environments["environments"]), "result_schema_sha256": sha(ROOT / "schemas/p4_m8_world_model_result.schema.json"), "code_sha256": {name: sha(ROOT / "scripts" / name) for name in code}, "outcome_aware_retry_allowed": False, "environment_reference_leakage_forbidden": True, "simulator_repair_after_outcome_allowed": False, "support_state_effect": "none_before_adjudication", "publication_authority": "none", "release_authority": "none"}
    (BASE / "preregistration.json").write_text(json.dumps(prereg, indent=2) + "\n")
    total = sum((x["curriculum"] + x["heldout"]) * len(SEEDS) * len(ARMS) for x in design["episodes"].values())
    print(f"Built P4/M8 Campaign 5: two environments, {len(SEEDS)} seeds, {len(ARMS)} arms, {total} frozen episodes.")


if __name__ == "__main__": main()
