#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p4_m8_world_model_campaign.py"
ARTIFACTS = [
    "scripts/p4_m8_world_model_common.py",
    "scripts/build_p4_m8_world_model_campaign.py",
    "scripts/validate_p4_m8_world_model_design.py",
    "scripts/run_p4_m8_world_model_campaign.py",
    "scripts/evaluate_p4_m8_world_model_campaign.py",
    "scripts/validate_p4_m8_world_model_campaign.py",
    "schemas/p4_m8_world_model_result.schema.json",
    "experiments/p4_situated_world_model/environments.json",
    "experiments/p4_situated_world_model/design.json",
    "experiments/p4_situated_world_model/preregistration.json",
    "experiments/p4_situated_world_model/raw/campaign_run.json",
    "experiments/p4_situated_world_model/results/confirmatory_result.json",
    "evidence_transitions/post_v2_3/situated_world_model_finite_pomdp_synthetic_test_backed.json",
    "docs/p4_situated_world_model_campaign.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text()); existing = next((x for x in value["units"] if x.get("script") == SCRIPT), None); value["units"] = [x for x in value["units"] if x.get("script") != SCRIPT]; used = {x["order"] for x in value["units"]}; preferred = existing.get("order") if existing else None; order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + 2) if i not in used)
    value["units"].append({"id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate", "input_contract": "One prospectively frozen 11,250-episode situated-world-model and consolidation campaign over two authored partially observable environments, five seeds, ten arms, six causal ablations, and 6,000 held-out episodes.", "input_artifacts": ARTIFACTS, "output_contract": "Recompute the central held-out metrics; preserve exact reference exclusion, identity binding, authority, replay, consolidation lineage, replacement, rollback, heterogeneous effects, bounded non-core promotion, and zero chapter-core movement.", "output_assertions": ["11,250 episode and 6,000 heldout denominators remain exact", "all 100 environment-seed-arm cells remain present", "all governed replacement and rollback receipts remain exact", "six aggregate directional ablation signatures and heterogeneous active-information effect remain visible", "ten laundering mutations are rejected", "only the finite non-core claim is synthetic-test-backed and no chapter core moves"], "claim_scope": "Two finite authored simulators and one Bayesian count-table governed interface only.", "negative_controls": "validator_owned_ten_world_model_laundering_mutations", "negative_control_cases": ["heldout inflation", "disposition laundering", "ablation inflation", "aggregate rewrite", "chapter-core promotion", "new-chapter invention", "release authority", "reference leak", "identity swap", "authority overflow"], "prohibited_inference": "Does not establish a neural world model, learned latent representation, natural-task planning, open-world object permanence, general causal understanding, reliable shift detection, simulator adequacy, sim-to-real transfer, deployment safety, SOTA, AGI, ASI, publication, release, or chapter-core support.", "contract_precision": "exact", "semantic_review_state": "checked_bounded_finite_promotion_and_scope_ceiling"})
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda x: x["order"]); value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}; REGISTRY.write_text(json.dumps(value, indent=2) + "\n"); print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
