#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_content_authenticity_review.py"
ARTIFACTS = [
    "scripts/validate_content_authenticity_review.py",
    "lean/AsiStackProofs/ContentAuthenticityReview.lean",
    "tests/fixtures/proof_models/content_authenticity_envelope.json",
    "evidence_quality/proof_model_dossiers/content-authenticity-watermarking-and-synthetic-media-integrity.md",
    "chapters/content-authenticity-watermarking-and-synthetic-media-integrity.qmd",
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
        "input_contract": "Canonical authenticity-envelope Lean review, independent 42-axis fixture, chapter proof boundary, proof dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, evidence-substitution, transformation, trust-policy, signer-revocation, receipt, truth/origin collision, communication-consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "eight-transition review reaches only Project Theseus authenticity campaign eligibility",
            "42/42 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "provenance, watermark, detector, truth, origin, authorship, compliance, and support claims remain separated",
            "finite transformation accounting covers every listed transformation",
            "asset, trust-policy, transformation, signer-epoch, and expiry changes invalidate a bounded receipt",
            "unsupported preservation and unbound composite claims reject",
            "authenticity signals cannot recover semantic truth and absent signals cannot recover human origin",
            "the communication consumer rejects inherited comprehension",
            "32 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored authenticity-envelope review, evidence-role separation, finite transformation accounting, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_42_axis_evidence_transformation_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["signal laundering", "unsupported transformation", "policy drift", "signer revocation", "truth inference", "origin inference", "comprehension inheritance", "support promotion"],
        "prohibited_inference": "Does not establish signature or provenance correctness, watermark or detector robustness, semantic truth, human or synthetic origin, authorship, consent, comprehension, legal compliance, remedy efficacy, secure deployment, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bounded_formal_model_and_independent_consumer_no_support_effect",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
