#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p4_m8_residual_verifier_terminal.py"
ARTIFACTS = [
    "scripts/p4_m8_residual_verifier_common.py",
    "scripts/build_p4_m8_residual_verifier_campaign.py",
    "scripts/run_p4_m8_residual_verifier.py",
    "scripts/evaluate_p4_m8_residual_verifier.py",
    "experiments/p4_residual_verifier_capacity/preregistration.json",
    "experiments/p4_residual_verifier_capacity/raw/preflight_generation.json",
    "experiments/p4_residual_verifier_capacity/results/preflight_result.json",
    "experiments/p4_residual_verifier_capacity/v1_preflight_failure_diagnosis.json",
    "scripts/p4_m8_residual_verifier_v2_common.py",
    "scripts/build_p4_m8_residual_verifier_v2_campaign.py",
    "scripts/run_p4_m8_residual_verifier_v2.py",
    "scripts/evaluate_p4_m8_residual_verifier_v2.py",
    "experiments/p4_residual_verifier_capacity_v2/preregistration.json",
    "experiments/p4_residual_verifier_capacity_v2/raw/preflight_generation.json",
    "experiments/p4_residual_verifier_capacity_v2/results/preflight_result.json",
    "experiments/p4_residual_verifier_capacity_v2/v2_preflight_failure_diagnosis.json",
    "scripts/p4_m8_residual_verifier_v3_common.py",
    "scripts/build_p4_m8_residual_verifier_v3_campaign.py",
    "scripts/run_p4_m8_residual_verifier_v3.py",
    "scripts/evaluate_p4_m8_residual_verifier_v3.py",
    "scripts/validate_p4_m8_residual_verifier_terminal.py",
    "experiments/p4_residual_verifier_capacity_v3/preregistration.json",
    "experiments/p4_residual_verifier_capacity_v3/raw/preflight_generation.json",
    "experiments/p4_residual_verifier_capacity_v3/results/preflight_result.json",
    "experiments/p4_residual_verifier_capacity_v3/v3_terminal_preflight_failure_diagnosis.json",
    "evidence_transitions/post_v2_3/residual_verifier_terminal_instrument_failure.json",
    "docs/p4_residual_verifier_capacity_campaign.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text()); existing = next((x for x in value["units"] if x.get("script") == SCRIPT), None); value["units"] = [x for x in value["units"] if x.get("script") != SCRIPT]; used = {x["order"] for x in value["units"]}; preferred = existing.get("order") if existing else None; order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + 2) if i not in used)
    value["units"].append({"id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate", "input_contract": "Three prospectively versioned sacrificial residual-honesty/verifier-capacity instruments over eighteen tasks and 36 exact local Qwen3-8B calls, with all heldout generation and result paths absent.", "input_artifacts": ARTIFACTS, "output_contract": "Preserve all three instrument failures, exact byte bindings, terminal no-repair boundary, diagnostic sacrificial values, sealed heldout denominator, no claim attempt, and zero support promotion.", "output_assertions": ["v1 route/clean-control failure remains visible", "v2 label-bearing exemplar failure remains visible", "v3 extraction-interface failure remains terminal", "all heldout paths remain absent", "six laundering mutations are rejected", "support remains blocks_promotion with zero chapter-core movement"], "claim_scope": "Instrument qualification history only; no heldout residual-honesty or verifier-capacity result.", "negative_controls": "validator_owned_six_terminal_failure_mutations", "negative_control_cases": ["v1 failure erasure", "v2 heldout laundering", "v3 repair reopening", "schema inflation", "qualification laundering", "support promotion"], "prohibited_inference": "Does not establish residual honesty, verifier competence, useful throughput, safety, transfer, deployment, SOTA, AGI, ASI, publication, release, or chapter-core support.", "contract_precision": "exact", "semantic_review_state": "checked_terminal_instrument_failure_and_sealed_heldout"})
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda x: x["order"]); value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}; REGISTRY.write_text(json.dumps(value, indent=2) + "\n"); print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
