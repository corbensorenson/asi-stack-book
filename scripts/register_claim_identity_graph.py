#!/usr/bin/env python3
"""Register the accepted-transition claim identity graph validation unit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_claim_identity_graph.py"
ARTIFACTS = [
    "evidence_quality/claim_identity_graph.json",
    "schemas/claim_identity_graph.schema.json",
    "docs/claim_identity_graph_reconciliation.md",
    "scripts/build_claim_identity_graph.py",
    "scripts/validate_claim_identity_graph.py",
    "scripts/register_claim_identity_graph.py",
    "evidence_quality/claim_atom_registry.json",
    "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    used = {unit["order"] for unit in registry["units"]}
    order = next(value for value in range(1, len(registry["units"]) + 2) if value not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "All 117 transition files; the exact 115 review-accepted denominator; 3,730 activation atoms; the 15-atom post-activation addendum; and a manually adjudicated exhaustive parent table for every non-direct campaign claim.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Resolve each accepted transition through exactly one direct atom, bounded subclaim, alias, or proxy relation while preserving transition digests, scope, artifacts, non-claims, canonical owner/proposition, and zero indirect parent support movement.",
        "output_assertions": [
            "115 of 115 accepted transitions resolve",
            "25 direct atom identities",
            "61 bounded subclaims",
            "29 proxy relations",
            "zero unresolved identities",
            "zero indirect parent support movement",
            "twelve mutations reject"
        ],
        "claim_scope": "Claim identity, ownership, and maximum-inference traceability only.",
        "negative_controls": "validator_owned_twelve_identity_scope_and_support_mutations",
        "negative_control_cases": [
            "accepted transition deletion", "dangling parent", "indirect parent promotion",
            "proxy recast as atom", "claim identity rewrite", "transition digest rewrite",
            "scope boundary deletion", "non-claim deletion", "artifact denominator deletion",
            "proxy laundering enabled", "mapping promoted to evidence", "unresolved invention"
        ],
        "prohibited_inference": "Identity resolution is not claim truth, support promotion, negative-result rehabilitation, construct validity, empirical competence, reproduction, transfer, safety, SOTA, AGI, ASI, publication, or release evidence.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_non_direct_transition_scope_surface_owner_and_parent_review_with_digest_bound_regeneration"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda unit: unit["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(
        f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()
