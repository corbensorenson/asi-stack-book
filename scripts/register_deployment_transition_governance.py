#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_deployment_transition_governance.py"
ARTIFACTS = [
    "scripts/validate_deployment_transition_governance.py",
    "lean/AsiStackProofs/DeploymentTransitionGovernance.lean",
    "tests/fixtures/proof_models/deployment_transition_dossier.json",
    "evidence_quality/proof_model_dossiers/ai-deployment-transition-distribution-and-human-agency.md",
    "chapters/ai-deployment-transition-distribution-and-human-agency.qmd",
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
        "input_contract": "Canonical deployment-transition Lean review, independent 54-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, cohort, denominator, remedy, monotonicity, receipt, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "eight-transition review reaches only Project Theseus governed transition-study eligibility",
            "54/54 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "finite cohort identity and fully-remedied predicates compose over append",
            "omitted cohorts and unremedied harmed cohorts reject transition acceptance",
            "positive aggregate gain cannot erase the modeled harmed-cohort obligation",
            "expiry, denominator gaps, and remedy gaps remain rejecting under adverse changes",
            "deployment, baseline, contract, denominator, observation, remedy, and authority changes invalidate receipts",
            "aggregate signals cannot recover harmed-cohort status and approval counts cannot recover practical refusal",
            "accountability, readiness, and Evidence States consumers reject missing transition evidence",
            "44 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored deployment-transition review, finite cohort and remedy custody, adverse monotonicity, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_54_axis_identity_design_accounting_agency_capacity_remedy_boundary_cohort_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["cohort omission", "unremedied burden", "expired contract", "scope drift", "aggregate collision", "agency collision", "support promotion"],
        "prohibited_inference": "Does not establish field truth, causal deployment effect, job change, welfare, fairness, meaningful agency, lawful remedy, service continuity, deployment readiness, support, release, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bounded_formal_model_and_three_existing_consumers_no_support_effect",
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
