#!/usr/bin/env python3
"""Register prospective P2 frontier selection validation."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_frontier_selection.py"
ARTIFACTS = [
    "evidence_quality/p2_frontier_selection.json",
    "schemas/p2_frontier_selection.schema.json",
    "docs/p2_frontier_selection.md",
    "scripts/validate_p2_frontier_selection.py",
    "scripts/register_p2_frontier_selection.py",
    "evidence_quality/claim_atom_registry.json",
    "docs/claim_bearing_experiment_competence_standard.md",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [u for u in registry["units"] if u.get("script") != SCRIPT]
    used = {u["order"] for u in registry["units"]}
    order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Five prospectively compared high-value frontier candidates; exact weighted criteria and fatal gates; a canonical subclaim identity; natural non-authored corpus and rights plan; local model, hardware, and resource snapshot; seven pending competence gates; and a closed final-heldout gate.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Select exactly one highest-value feasible P2 subclaim before outcomes, bind its scope and maximum inference, and reject score drift, fatal-blocker selection, invented identity, false competence, premature heldout opening, or support promotion.",
        "output_assertions": ["five candidates compared", "one highest-scoring non-fatally-blocked subclaim selected", "canonical parent exists", "seven competence gates pending", "final heldout gate closed", "no support or release effect", "eight mutations reject"],
        "claim_scope": "Prospective P2 selection and custody only; no experiment result or support movement.",
        "negative_controls": "validator_owned_eight_selection_score_identity_competence_heldout_and_support_mutations",
        "negative_control_cases": ["weight drift", "lower scorer selection", "fatal selected", "missing parent", "false evaluator pass", "heldout opened", "denominator opened", "support promotion"],
        "prohibited_inference": "Selection does not establish implementation, construct, evaluator, sensitivity, rescue, resource, corpus, model, reproduction, transfer, safety, SOTA, AGI, ASI, publication, deployment, or release competence.",
        "contract_precision": "exact",
        "semantic_review_state": "candidate_value_feasibility_claim_identity_scope_corpus_custody_model_resource_and_heldout_reviewed",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda u: u["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()
