#!/usr/bin/env python3
"""Run the frozen finite situated-world-model and consolidation campaign."""

from __future__ import annotations

import copy
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path

from p4_m8_world_model_common import ARMS, BASE, SEEDS, STATES, canonical_sha, entropy, environment_configs, load, normalize, rng_for, sample, sha


CURRICULUM = ("sensory_regularities", "persistent_entities", "temporal_consequences", "causal_interventions", "symbolic_bindings", "abstraction", "version_history")


class Agent:
    def __init__(self, arm: str, env: dict, seed: int):
        self.arm, self.env, self.seed = arm, env, seed
        self.counts: dict[str, dict[str, Counter]] = {p: {s: Counter({o: 1 for o in rows[s]}) for s in STATES} for p, rows in env["probes"].items()}
        responses = env["intervention"]["responses"]
        self.intervention_counts = {s: Counter({o: 1 for o in responses[s]}) for s in STATES}
        self.history: list[dict] = []; self.entity_history: dict[str, list[str]] = defaultdict(list); self.consolidations: list[dict] = []
        self.last_rules: dict[str, dict[str, str]] = {}; self.silent_rewrites = 0; self.rollback_snapshots: list[dict] = []

    def likelihood(self, probe: str, state: str, observation: str) -> float:
        counts = self.counts[probe][state]; return counts[observation] / sum(counts.values())

    def response_likelihood(self, state: str, response: str) -> float:
        counts = self.intervention_counts[state]; return counts[response] / sum(counts.values())

    def update_belief(self, belief: dict[str, float], probe: str, observation: str, separate: bool = True) -> dict[str, float]:
        prior = belief if separate else {s: 1 / len(STATES) for s in STATES}
        return normalize({s: prior[s] * self.likelihood(probe, s, observation) for s in STATES})

    def probe_score(self, probe: str) -> float:
        outcomes = self.env["probes"][probe][STATES[0]].keys(); score = 0.0
        for outcome in outcomes:
            values = [self.likelihood(probe, state, outcome) for state in STATES]
            score += max(values) - min(values)
        return score

    def choose_probes(self) -> list[str]:
        probes = list(self.env["probes"])
        if self.arm in {"reactive_no_world_model", "transcript_memory", "ablate_active_information"}: return probes[:2]
        return sorted(probes, key=lambda p: (-self.probe_score(p), p))[:2]

    def transcript_belief(self, observations: list[dict]) -> dict[str, float]:
        signature = tuple((row["probe"], row["value"]) for row in observations); exact = [x["revealed_state"] for x in self.history if x.get("signature") == signature]
        if not exact:
            partial = [x["revealed_state"] for x in self.history if any(item in x.get("signature", ()) for item in signature)]
            exact = partial
        counts = Counter(exact)
        return normalize({s: counts[s] + 1 for s in STATES})

    def consolidate(self, episode_ref: str, stage: str, quiescent: bool) -> dict | None:
        if self.arm == "ablate_consolidation": return None
        rules = {}
        for probe in self.env["probes"]:
            rules[probe] = {}
            outcomes = self.env["probes"][probe][STATES[0]].keys()
            for outcome in outcomes:
                rules[probe][outcome] = max(STATES, key=lambda s: self.likelihood(probe, s, outcome))
        changed = rules != self.last_rules
        if not quiescent and changed and self.last_rules: self.silent_rewrites += 1
        version = len(self.consolidations) + 1
        record = {"consolidation_id": f"{self.env['environment_id']}:{self.seed}:{self.arm}:c{version}", "version": version, "stage": stage, "quiescent": quiescent, "candidate_invariants": rules, "semantic_beliefs": {"states": list(STATES), "entity_count": len(self.entity_history)}, "causal_rules": {"intervention": self.env["intervention"]["action"], "response_mode_by_state": {s: self.intervention_counts[s].most_common(1)[0][0] for s in STATES}}, "procedures": {s: self.env["terminal_actions"][s] for s in STATES}, "supporting_episode_refs": [x["episode_ref"] for x in self.history[-20:]], "contradicting_episode_refs": [x["episode_ref"] for x in self.history[-20:] if not x["prediction_correct"]], "supersedes": self.consolidations[-1]["consolidation_id"] if self.consolidations else None, "rollback_snapshot_version": len(self.rollback_snapshots) + 1}
        self.rollback_snapshots.append({"version": len(self.rollback_snapshots) + 1, "counts": copy.deepcopy(self.counts), "intervention_counts": copy.deepcopy(self.intervention_counts), "last_rules": copy.deepcopy(self.last_rules)}); self.consolidations.append(record); self.last_rules = rules
        return record

    def learn(self, probe_rows: list[dict], intervention: dict | None, state: str, episode: int, episode_ref: str, stage: str, prediction_correct: bool) -> dict | None:
        signature = tuple((x["probe"], x["value"]) for x in probe_rows); self.history.append({"episode_ref": episode_ref, "signature": signature, "revealed_state": state, "prediction_correct": prediction_correct}); self.entity_history[episode_ref.split(":")[-1]].append(state)
        if self.arm != "reactive_no_world_model":
            for row in probe_rows: self.counts[row["probe"]][state][row["value"]] += 1
            if intervention: self.intervention_counts[state][intervention["observed_response"]] += 1
        if self.arm == "ablate_consolidation" and episode > 0 and episode % 20 == 0:
            # Loss of cross-stage semantic consolidation: retain the transcript but reset the predictive tables.
            self.counts = {p: {s: Counter({o: 1 for o in rows[s]}) for s in STATES} for p, rows in self.env["probes"].items()}
            return None
        if self.arm == "ablate_quiescent_stabilization": return self.consolidate(episode_ref, stage, quiescent=False)
        if episode > 0 and episode % 20 == 0: return self.consolidate(episode_ref, stage, quiescent=True)
        return None


def hidden_sequence(env: dict, seed: int, count: int) -> list[tuple[str, str]]:
    current = {entity: sample({s: 1 / 3 for s in STATES}, rng_for(seed, env["environment_id"], entity, "initial")) for entity in env["entities"]}; rows = []
    for episode in range(count):
        entity = env["entities"][episode % len(env["entities"])]; state = sample(env["transition"][current[entity]], rng_for(seed, env["environment_id"], episode, entity, "transition")); current[entity] = state; rows.append((entity, state))
    return rows


def observe(env: dict, seed: int, episode: int, state: str, probe: str, shifted: bool, step: int) -> str:
    table = env.get("shifted_probes", {}).get(probe, env["probes"][probe]) if shifted else env["probes"][probe]
    return sample(table[state], rng_for(seed, env["environment_id"], episode, probe, step, "observation"))


def run_episode(agent: Agent, env: dict, seed: int, episode: int, entity: str, hidden_state: str, phase: str, shifted: bool, stage: str) -> dict:
    episode_ref = f"{env['environment_id']}:{seed}:{agent.arm}:{episode}:{entity}"
    identity_history = agent.entity_history.get(entity, [])
    if identity_history and agent.arm not in {"reactive_no_world_model", "transcript_memory"}:
        identity_counts = Counter(identity_history[-12:])
        belief = normalize({state: identity_counts[state] + 1 for state in STATES})
    else:
        belief = {s: 1 / 3 for s in STATES}
    prior = dict(belief); probes = agent.choose_probes(); probe_rows = []
    for step, probe in enumerate(probes):
        value = observe(env, seed, episode, hidden_state, probe, shifted, step); probe_rows.append({"observation_id": f"{episode_ref}:obs:{step}", "probe": probe, "value": value, "delivered_version": 1})
        if agent.arm == "reactive_no_world_model": belief = agent.update_belief({s: 1 / 3 for s in STATES}, probe, value, separate=False); break
        if agent.arm == "transcript_memory": belief = agent.transcript_belief(probe_rows)
        else: belief = agent.update_belief(belief, probe, value, separate=agent.arm != "ablate_observation_belief_separation")
    intervention = None; intervention_allowed = agent.arm in {"governed_world_model", "ablate_active_information", "ablate_observation_belief_separation", "ablate_uncertainty", "ablate_consolidation", "ablate_quiescent_stabilization"} and agent.arm != "ablate_intervention"
    if intervention_allowed and entropy(belief) > 0.55:
        prediction = max(env["intervention"]["responses"][max(belief, key=belief.get)], key=env["intervention"]["responses"][max(belief, key=belief.get)].get)
        response = sample(env["intervention"]["responses"][hidden_state], rng_for(seed, env["environment_id"], episode, "intervention")); intervention = {"intervention_id": f"{episode_ref}:intervention", "action": env["intervention"]["action"], "authority": env["intervention"]["authority"], "predicted_response": prediction, "observed_response": response, "cost": env["intervention"]["cost"]}
        belief = normalize({s: belief[s] * agent.response_likelihood(s, response) for s in STATES})
    predicted_state = max(belief, key=belief.get); confidence = belief[predicted_state]
    expected_obs_probability = 1.0
    if probe_rows:
        last = probe_rows[-1]; expected_obs_probability = sum(belief[s] * agent.likelihood(last["probe"], s, last["value"]) for s in STATES)
    governed = agent.arm in {"governed_world_model", "ablate_active_information", "ablate_intervention", "ablate_observation_belief_separation", "ablate_uncertainty", "ablate_consolidation", "ablate_quiescent_stabilization"}
    uncertainty_gate = governed and agent.arm != "ablate_uncertainty" and confidence < 0.62
    shift_gate = governed and expected_obs_probability < 0.14
    terminal_action = "escalate" if uncertainty_gate or shift_gate else env["terminal_actions"][predicted_state]
    prediction_correct = predicted_state == hidden_state
    observed_effect = {"required_action": env["terminal_actions"][hidden_state], "terminal_action": terminal_action, "success": terminal_action == env["terminal_actions"][hidden_state], "unsafe_action": terminal_action != "escalate" and terminal_action != env["terminal_actions"][hidden_state], "escalated": terminal_action == "escalate", "revealed_state_after_effect": hidden_state}
    consolidation = agent.learn(probe_rows, intervention, hidden_state, episode, episode_ref, stage, prediction_correct)
    artifact = {"environment_reference_state": {"artifact_id": f"{episode_ref}:reference", "evaluator_only": True, "hidden_state": hidden_state, "entity_id": entity, "shifted": shifted}, "agent_input": {"artifact_id": f"{episode_ref}:input", "entity_id": entity, "phase": phase, "observation_refs": [x["observation_id"] for x in probe_rows], "contains_reference_state": False}, "delivered_observation": probe_rows, "interpretation": {"artifact_id": f"{episode_ref}:interpretation", "observation_values": [{"probe": x["probe"], "value": x["value"]} for x in probe_rows]}, "latent_hypothesis": {"artifact_id": f"{episode_ref}:hypotheses", "prior": prior, "posterior": belief, "live_hypothesis_count": sum(v > 0.05 for v in belief.values()), "identity_history_count": len(identity_history), "identity_prior_used": bool(identity_history and agent.arm not in {"reactive_no_world_model", "transcript_memory"})}, "prediction": {"artifact_id": f"{episode_ref}:prediction", "predicted_state": predicted_state, "confidence": confidence, "terminal_action": terminal_action}, "prediction_error": {"artifact_id": f"{episode_ref}:prediction-error", "state_error": not prediction_correct, "brier": sum((belief[s] - (1 if s == hidden_state else 0)) ** 2 for s in STATES)}, "intervention": intervention, "causal_model_revision": {"artifact_id": f"{episode_ref}:causal-revision", "updated_after_effect_only": True, "intervention_observed": intervention is not None}, "belief_transition": {"artifact_id": f"{episode_ref}:belief-transition", "prior": prior, "posterior": belief, "entropy_before": entropy(prior), "entropy_after": entropy(belief)}, "curriculum_stage": {"artifact_id": f"{episode_ref}:stage", "stage": stage}, "observed_effect": {"artifact_id": f"{episode_ref}:effect", **observed_effect}, "consolidation": consolidation}
    return {"episode_ref": episode_ref, "environment_id": env["environment_id"], "seed": seed, "arm": agent.arm, "episode": episode, "phase": phase, "entity_id": entity, "shifted": shifted, "artifact": artifact, "budget": {"max_information_actions": 3, "information_actions_used": len(probe_rows), "max_interventions": 1, "interventions_used": int(intervention is not None), "compute_proxy_ceiling": 1000, "compute_proxy_used": 80 + 25 * len(probe_rows) + 40 * int(intervention is not None)}, "support_state_effect": "none_pending_adjudication"}


def main() -> None:
    prereg = load(BASE / "preregistration.json"); design = load(BASE / "design.json"); out = BASE / "raw/campaign_run.json"
    if out.exists(): raise SystemExit(f"one-shot result already exists: {out}")
    if sha(BASE / "design.json") != prereg["design_sha256"] or sha(BASE / "environments.json") != prereg["environments_sha256"]: raise SystemExit("frozen design drift")
    for name, expected in prereg["code_sha256"].items():
        if sha(Path(__file__).resolve().parent / name) != expected: raise SystemExit(f"frozen code drift: {name}")
    if sha(Path(__file__).resolve().parents[1] / "schemas/p4_m8_world_model_result.schema.json") != prereg["result_schema_sha256"]: raise SystemExit("frozen result-schema drift")
    configs = environment_configs(); records = []; agent_summaries = []; started = time.perf_counter()
    for env_index, env_id in enumerate(("adaptive_workshop", "service_mesh_transfer")):
        env = configs[env_id]; train_count = design["episodes"][env_id]["curriculum"]; heldout_count = design["episodes"][env_id]["heldout"]; total = train_count + heldout_count; sequences = {seed: hidden_sequence(env, seed, total) for seed in SEEDS}
        for seed in SEEDS:
            for arm in ARMS:
                agent = Agent(arm, env, seed)
                for episode, (entity, state) in enumerate(sequences[seed]):
                    phase = "curriculum" if episode < train_count else "heldout"; within = episode if phase == "curriculum" else episode - train_count; shifted = phase == "heldout" and within >= design["episodes"][env_id]["shift_after_heldout_episode"]
                    stage = CURRICULUM[min(len(CURRICULUM) - 1, int(episode / max(1, train_count / len(CURRICULUM))))] if phase == "curriculum" else "heldout_shift" if shifted else "heldout_pre_shift"
                    records.append(run_episode(agent, env, seed, episode, entity, state, phase, shifted, stage))
                current_state = {"counts": {p: {s: dict(c) for s, c in rows.items()} for p, rows in agent.counts.items()}, "intervention_counts": {s: dict(c) for s, c in agent.intervention_counts.items()}, "last_rules": agent.last_rules}
                replacement_state = json.loads(json.dumps(current_state, sort_keys=True))
                replacement_exact = canonical_sha(current_state) == canonical_sha(replacement_state)
                rollback_exact = False
                rollback_target_version = None
                if agent.rollback_snapshots:
                    snapshot = agent.rollback_snapshots[-1]
                    rollback_target_version = snapshot["version"]
                    snapshot_state = {"counts": {p: {s: dict(c) for s, c in rows.items()} for p, rows in snapshot["counts"].items()}, "intervention_counts": {s: dict(c) for s, c in snapshot["intervention_counts"].items()}, "last_rules": snapshot["last_rules"]}
                    mutated = copy.deepcopy(current_state); first_probe = next(iter(mutated["counts"])); first_state = next(iter(mutated["counts"][first_probe])); first_obs = next(iter(mutated["counts"][first_probe][first_state])); mutated["counts"][first_probe][first_state][first_obs] += 999
                    restored = json.loads(json.dumps(snapshot_state, sort_keys=True))
                    rollback_exact = canonical_sha(mutated) != canonical_sha(restored) and canonical_sha(restored) == canonical_sha(snapshot_state)
                agent_summaries.append({"environment_id": env_id, "seed": seed, "arm": arm, "consolidation_count": len(agent.consolidations), "silent_rewrite_count": agent.silent_rewrites, "rollback_snapshot_count": len(agent.rollback_snapshots), "memory_replacement_exact": replacement_exact, "rollback_probe_exact": rollback_exact, "rollback_target_version": rollback_target_version, "final_state_sha256": canonical_sha(current_state), "replacement_state_sha256": canonical_sha(replacement_state), "consolidations": agent.consolidations})
                print(f"P4/M8 Campaign 5 {env_id} seed={seed} arm={arm} closed", flush=True)
    result = {"schema_version": "asi_stack.p4_m8_world_model_raw.v1", "run_id": prereg["run_id"], "preregistration_sha256": sha(BASE / "preregistration.json"), "environment_sha256": sha(BASE / "environments.json"), "record_count": len(records), "records": records, "agent_summaries": agent_summaries, "wall_seconds": round(time.perf_counter() - started, 6), "network_calls": 0, "external_spend_usd": 0, "reference_state_excluded_from_agent_input": True, "support_state_effect": "none_pending_adjudication", "publication_authority": "none", "release_authority": "none"}
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(result, separators=(",", ":"), default=lambda x: dict(x)) + "\n"); print(f"P4/M8 Campaign 5 raw run closed: {len(records)} episodes, sha256={sha(out)}")


if __name__ == "__main__": main()
