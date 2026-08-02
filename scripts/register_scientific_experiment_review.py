#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_scientific_experiment_review.py"
ARTIFACTS = [
    "scripts/validate_scientific_experiment_review.py",
    "lean/AsiStackProofs/ScientificExperimentReview.lean",
    "tests/fixtures/proof_models/scientific_experiment_dossier.json",
    "evidence_quality/proof_model_dossiers/scientific-discovery-and-experimental-governance.md",
    "chapters/scientific-discovery-and-experimental-governance.qmd",
    "proofs/proof_manifest.json", "proofs/proof_triage.json", "docs/book_outline.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(
        i for i in range(1, len(value["units"]) + 2) if i not in used
    )
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Canonical scientific-experiment Lean review, independent 54-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, attempt, confirmation, monotonicity, receipt, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "eight-transition review reaches only Project Theseus governed experiment campaign eligibility",
            "54/54 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "finite attempt identity composes and preserves every member",
            "omitted attempts and outcome-exposed confirmatory branches reject completeness",
            "expiry, attempt gaps, and replication gaps remain rejecting under adverse changes",
            "hypothesis, protocol, instrument, data, analysis, environment, and claim-ceiling changes invalidate receipts",
            "significance cannot recover preregistration integrity and replication counts cannot recover independence",
            "missing independent replication and null results reject Evidence States and Benchmark Ratchet promotion",
            "41 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored experiment review, finite attempt custody, confirmatory integrity, adverse monotonicity, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_54_axis_identity_design_execution_analysis_replication_governance_boundary_attempt_confirmation_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["hypothesis drift", "attempt omission", "outcome exposure", "expired contract", "scope drift", "signal collision", "support promotion"],
        "prohibited_inference": "Does not establish hypothesis truth, causal identification, instrument accuracy, reproducibility, discovery, laboratory safety, deployment, support, release, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bounded_formal_model_and_two_independent_consumers_no_support_effect",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
