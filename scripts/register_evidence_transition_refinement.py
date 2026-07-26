#!/usr/bin/env python3
"""Register the projection-aware evidence-transition refinement validator."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "validation/registry.json"
SCRIPT = "validate_evidence_transition_refinement.py"
ARTIFACTS = [
    "scripts/validate_evidence_transition_refinement.py",
    "schemas/evidence_transition_refinement.schema.json",
    "experiments/evidence_transition_refinement/results/2026-07-26-local.json",
    "chapters/evidence-states-and-claim-discipline.qmd",
    "lean/AsiStackProofs/EvidenceTransitionRefinement.lean",
    "lean/AsiStackProofs/EvidenceStates.lean",
    "lean/AsiStackProofs/ClaimLedgerRefinement.lean",
]

registry = json.loads(PATH.read_text())
registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
order = len(registry["units"]) + 1
registry["units"].append(
    {
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": (
            "Projection-aware six-stage evidence-transition lifecycle, independent "
            "route consumer, result schema, bounded result, chapter interpretation, "
            "foundational support-state facts, and exact claim-ledger handoff boundary."
        ),
        "input_artifacts": ARTIFACTS,
        "output_contract": (
            "Reject atom, projection, state-category, event, target-evidence, adverse-"
            "transition, review, decision, handoff, acknowledgment, inheritance, support, "
            "and external-effect failures while reaching every declared route."
        ),
        "output_assertions": [
            "six reachable stages",
            "35 declared and reached routes",
            "35 rejecting mutation cases",
            "three exact claim projections",
            "eight non-aggregating evidence dimensions",
            "support, inheritance, and external effect none",
        ],
        "claim_scope": (
            "One finite authored evidence-transition policy and independent local route "
            "consumer; repository audits retain their own historical scopes."
        ),
        "negative_controls": "validator_owned_evidence_transition_route_mutations",
        "negative_control_cases": [
            "atom, proposition, obligation, predicate, state, or event substitution",
            "missing target evidence, adverse-transition burden, review, dissent, limitations, residuals, changelog, handoff, or acknowledgment",
            "support assignment, inherited parent or descendant movement, or external-effect laundering",
        ],
        "prohibited_inference": (
            "No evidence truth, semantic projection equivalence, reviewer independence, "
            "live support decision, release readiness, deployment, capability, safety, "
            "SOTA, AGI, ASI, inherited movement, or external effect."
        ),
        "contract_precision": "inherited",
        "semantic_review_state": (
            "checked_projection_aware_reachable_transition_control_not_evidence_truth_or_support_authority"
        ),
    }
)
required = list(registry["required_artifacts"])
for artifact in ARTIFACTS:
    if artifact not in required:
        required.append(artifact)
registry["required_artifacts"] = required
registry["summary"] = {
    "required_artifact_count": len(required),
    "unit_count": len(registry["units"]),
}
PATH.write_text(json.dumps(registry, indent=2) + "\n")
print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")
