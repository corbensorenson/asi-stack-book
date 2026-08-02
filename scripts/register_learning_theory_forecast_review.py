#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_learning_theory_forecast_review.py"
ARTIFACTS = [
    "scripts/validate_learning_theory_forecast_review.py",
    "lean/AsiStackProofs/LearningTheoryForecastReview.lean",
    "tests/fixtures/proof_models/learning_theory_forecast_dossier.json",
    "evidence_quality/proof_model_dossiers/learning-theory-generalization-and-scaling-science.md",
    "chapters/learning-theory-generalization-and-scaling-science.qmd",
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
        "input_contract": "Canonical learning-theory forecast Lean review, independent 45-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, denominator, alternative, monotonicity, receipt, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "six-transition review reaches only Project Theseus prospective forecast campaign eligibility",
            "45/45 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "finite attempt identity composes and preserves every member",
            "omitted attempts and unscored preregistered alternatives reject completeness",
            "expiry, unsupported extrapolation, and scoring shortfall remain rejecting under adverse changes",
            "population, sample, algorithm, architecture, metric, compute, and horizon changes invalidate receipts",
            "retrospective fit cannot recover prospective coverage and threshold metrics cannot recover mechanism change",
            "missing prospective holdout rejects Benchmark Ratchet promotion",
            "38 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored forecast review, finite attempt custody, adverse monotonicity, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_45_axis_identity_design_transfer_lifecycle_boundary_denominator_alternative_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["identity loss", "attempt omission", "unscored alternative", "expired contract", "scope drift", "signal collision", "support promotion"],
        "prohibited_inference": "Does not establish generalization, transfer, emergence, scaling accuracy, calibration, safety, deployment, support, release, SOTA, AGI, or ASI.",
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
