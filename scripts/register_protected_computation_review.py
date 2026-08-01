#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_protected_computation_review.py"
ARTIFACTS = [
    "scripts/validate_protected_computation_review.py",
    "lean/AsiStackProofs/ProtectedComputationReview.lean",
    "tests/fixtures/proof_models/protected_computation_dossier.json",
    "evidence_quality/proof_model_dossiers/confidential-and-verifiable-ai-computation.md",
    "chapters/confidential-and-verifiable-ai-computation.qmd",
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
        "input_contract": "Canonical protected-computation Lean review, independent 48-axis fixture, chapter proof boundary, proof dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, evidence-substitution, freshness, leakage, fallback, collision, privacy-consumer, canonical-binding, and no-promotion drift.",
        "output_assertions": [
            "eight-step review reaches only Project Theseus protected-computation campaign eligibility",
            "48/48 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "attestation, relation-proof, confidentiality, semantics, authorization, and end-to-end privacy claims remain separated",
            "artifact, verifier-policy, evidence-epoch, and expiry changes invalidate a bounded receipt",
            "finite leakage accounting covers every listed channel and an overrun is monotone under adverse change",
            "unprotected fallback requires separate authorization and consumer-visible disclosure",
            "evidence signals cannot recover semantic authority and component guarantees cannot recover end-to-end privacy",
            "the privacy consumer rejects purpose and authority inheritance",
            "31 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored protected-execution review, evidence-role separation, finite leakage and receipt checks, fallback policy, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_48_axis_evidence_freshness_leakage_fallback_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["stale evidence", "policy drift", "leakage overrun", "semantic laundering", "silent downgrade", "privacy authorization laundering", "support promotion"],
        "prohibited_inference": "Does not establish cryptographic soundness, attestation validity, hardware trust, side-channel resistance, leakage bounds in practice, semantic correctness, authorization, privacy, fallback efficacy, acceptable cost, secure deployment, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bounded_formal_model_and_independent_consumer_no_support_effect",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {
        "required_artifact_count": len(required), "unit_count": len(value["units"]),
    }
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
