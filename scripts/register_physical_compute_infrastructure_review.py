#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_physical_compute_infrastructure_review.py"
ARTIFACTS = [
    "scripts/validate_physical_compute_infrastructure_review.py",
    "lean/AsiStackProofs/PhysicalComputeInfrastructureReview.lean",
    "tests/fixtures/proof_models/physical_compute_infrastructure_dossier.json",
    "evidence_quality/proof_model_dossiers/physical-compute-infrastructure-energy-and-environmental-constraints.md",
    "chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd",
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
        "input_contract": "Canonical physical-compute Lean review, independent 44-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, accounting, capacity, impact, scope, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "six-transition review reaches only Project Theseus workload-capacity campaign eligibility",
            "44/44 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "finite workload demand and attributed energy compose over list append",
            "member demand, aggregate overrun, hidden backup energy, demand growth, capacity loss, and expiry remain bounded",
            "workload, site, interval, hardware, and meter changes invalidate receipts",
            "energy headlines cannot recover useful delivery and unit efficiency cannot recover total impact",
            "missing physical capacity rejects the Resource Economics required safety gate",
            "36 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored physical-infrastructure review, finite accounting, adverse monotonicity, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_44_axis_identity_capacity_impact_resilience_boundary_accounting_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["identity loss", "capacity omission", "impact omission", "hidden backup energy", "scope drift", "efficiency laundering", "support promotion"],
        "prohibited_inference": "Does not establish delivered performance, meter accuracy, sustainability, resilience, community acceptability, rebound control, deployment, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bounded_formal_model_and_independent_consumer_no_support_effect",
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
