#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_proof_carrying_claims_refinement.py"
ARTIFACTS = [
    "scripts/validate_proof_carrying_claims_refinement.py",
    "schemas/proof_carrying_claims_refinement.schema.json",
    "experiments/proof_carrying_claims_refinement/results/2026-07-15-local.json",
    "docs/proof_carrying_claims_refinement.md",
    "evidence_quality/model_adequacy_dossiers/proof-carrying-claims-refinement.md",
    "lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean",
    "scripts/validate_proof_carrying_claims.py",
    "schemas/proof_carrying_claim.schema.json",
    "experiments/proof_carrying_claims/fixtures",
    "scripts/validate_adversarial_review_dossier_probe.py",
    "experiments/adversarial_review_dossier/results/2026-07-02-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean target-to-writeback lifecycle, exact 3/5 proof-carrying and 2/7 adversarial-dossier suites, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject target/artifact/verifier/result substitution, authority leakage, missing interpretation/scope/trusted-base/execution/attempt/dossier/dissent/limitation/residual/owner custody, unverified pass, negative promotion, and mismatch without tribunal.",
        "output_assertions": ["three valid and five invalid proof-carrying fixtures", "two valid and seven invalid adversarial-dossier cases", "twenty-three routes and six reachable stages", "thirty-six rejected lifecycle mutations", "no support-state effect"],
        "claim_scope": "One finite authored target-specific verification lifecycle plus two existing bounded synthetic suites only.",
        "negative_controls": "validator_owned_target_artifact_verifier_adjudication_writeback_mutations",
        "negative_control_cases": ["target, artifact, verifier, result, or event substitution", "missing semantic or trusted-base custody", "passed verifier without artifacts or semantic review", "negative promotion or mismatch without tribunal", "missing independent dossier, dissent, limitation, residual, or owner handoff", "support assignment or external effect authority leak"],
        "prohibited_inference": "Does not establish semantic equivalence, artifact truth, proof/source/verifier soundness, reviewer competence, claim truth, evidence adequacy, support, action, useful advantage, causality, safety, deployment, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_target_to_writeback_lifecycle_not_semantic_sound_natural_deployed_or_support_authority",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
