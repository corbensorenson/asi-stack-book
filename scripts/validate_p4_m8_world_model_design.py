#!/usr/bin/env python3
"""Validate the frozen Campaign 5 design without reading outcome artifacts."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from p4_m8_world_model_common import ARMS, BASE, ROOT, SEEDS, canonical_sha, load, sha


EXPECTED_EPISODES = {
    "adaptive_workshop": {"curriculum": 70, "heldout": 60, "shift_after_heldout_episode": 30},
    "service_mesh_transfer": {"curriculum": 35, "heldout": 60, "shift_after_heldout_episode": 30},
}
REQUIRED_ARTIFACTS = {
    "environment_reference_state", "agent_input", "delivered_observation", "interpretation",
    "latent_hypothesis", "prediction", "prediction_error", "intervention",
    "causal_model_revision", "belief_transition", "curriculum_stage", "observed_effect", "consolidation",
}


def validate(design: dict, environments: dict, prereg: dict) -> list[str]:
    errors: list[str] = []
    if design.get("environments") != ["adaptive_workshop", "service_mesh_transfer"]: errors.append("environment identity")
    if set(environments.get("environments", {})) != set(design.get("environments", [])): errors.append("environment bodies")
    if design.get("seeds") != list(SEEDS): errors.append("seed identity")
    if design.get("arms") != list(ARMS): errors.append("arm identity")
    if design.get("episodes") != EXPECTED_EPISODES: errors.append("episode contract")
    if set(design.get("required_artifacts", [])) != REQUIRED_ARTIFACTS: errors.append("artifact separation")
    if design.get("matched_budget", {}).get("reference_state_visible_before_terminal_effect") is not False: errors.append("reference-state boundary")
    if design.get("primary_gates", {}).get("minimum_directional_ablation_signatures") != 4: errors.append("ablation gate")
    if prereg.get("state") != "prospectively_frozen_before_any_episode_or_outcome": errors.append("freeze state")
    if prereg.get("outcome_aware_retry_allowed") is not False or prereg.get("simulator_repair_after_outcome_allowed") is not False: errors.append("one-shot rule")
    if prereg.get("design_sha256") != sha(BASE / "design.json"): errors.append("design hash")
    if prereg.get("environments_sha256") != sha(BASE / "environments.json"): errors.append("environment hash")
    if prereg.get("environment_content_sha256") != canonical_sha(environments["environments"]): errors.append("environment content hash")
    result_schema = ROOT / "schemas/p4_m8_world_model_result.schema.json"
    if not result_schema.exists() or prereg.get("result_schema_sha256") != sha(result_schema): errors.append("result schema hash")
    for name, expected in prereg.get("code_sha256", {}).items():
        path = ROOT / "scripts" / name
        if not path.exists() or sha(path) != expected: errors.append(f"code hash:{name}")
    return errors


def main() -> None:
    design, environments, prereg = load(BASE / "design.json"), load(BASE / "environments.json"), load(BASE / "preregistration.json")
    errors = validate(design, environments, prereg)
    mutations = []
    for label, mutate in (
        ("environment", lambda d, e, p: d.update(environments=["adaptive_workshop"])),
        ("seeds", lambda d, e, p: d.update(seeds=[1709])),
        ("arms", lambda d, e, p: d.update(arms=d["arms"][:-1])),
        ("episodes", lambda d, e, p: d["episodes"]["adaptive_workshop"].update(heldout=59)),
        ("artifacts", lambda d, e, p: d.update(required_artifacts=d["required_artifacts"][:-1])),
        ("leak", lambda d, e, p: d["matched_budget"].update(reference_state_visible_before_terminal_effect=True)),
        ("retry", lambda d, e, p: p.update(outcome_aware_retry_allowed=True)),
        ("code", lambda d, e, p: p["code_sha256"].update({"run_p4_m8_world_model_campaign.py": "0" * 64})),
    ):
        d, e, p = copy.deepcopy(design), copy.deepcopy(environments), copy.deepcopy(prereg)
        mutate(d, e, p); rejected = bool(validate(d, e, p)); mutations.append({"mutation": label, "rejected": rejected})
    if errors or not all(row["rejected"] for row in mutations):
        raise SystemExit(json.dumps({"errors": errors, "mutations": mutations}, indent=2))
    print(json.dumps({"valid": True, "environments": 2, "seeds": len(SEEDS), "arms": len(ARMS), "frozen_episodes": 11250, "negative_mutations_rejected": len(mutations)}, indent=2))


if __name__ == "__main__":
    main()
