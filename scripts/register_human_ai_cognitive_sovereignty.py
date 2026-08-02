#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_human_ai_cognitive_sovereignty.py"
ARTIFACTS = [
    "scripts/validate_human_ai_cognitive_sovereignty.py",
    "lean/AsiStackProofs/HumanAICognitiveSovereignty.lean",
    "tests/fixtures/proof_models/human_ai_cognitive_sovereignty_dossier.json",
    "evidence_quality/proof_model_dossiers/human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty.md",
    "chapters/human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty.qmd",
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
        "input_contract": "Canonical human-AI cognitive-sovereignty Lean review, independent 49-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, comparator, purpose, participant, denominator, monotonicity, receipt, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "eight-transition review reaches only Project Theseus low-risk coupling-study eligibility",
            "49/49 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "combined-system qualification requires both competent human-alone and AI-alone baselines",
            "purpose grants are exact and unrelated use, revocation, and expiry block authorization",
            "finite participant identity composes and every expected participant requires post-exit follow-up",
            "expiry and post-exit denominator gaps remain rejecting under adverse changes",
            "participant, protocol, device/model, purpose, observation, exit, and authority changes invalidate receipts",
            "nominal revocation cannot recover practical exit and session metrics cannot recover post-exit skill retention",
            "privacy, human-control, and Evidence States consumers reject missing coupling evidence",
            "48 exact Lean declarations move no chapter support, neural-intervention, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored human-AI coupling review, comparator and purpose discipline, finite longitudinal custody, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_49_axis_identity_comparator_authorization_data_exit_observation_boundary_participant_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["one-sided comparator", "unrelated purpose", "revoked grant", "post-exit omission", "expired contract", "scope drift", "signal collision", "support promotion"],
        "prohibited_inference": "Does not establish field truth, beneficial symbiosis, genuine consent, mental integrity, cognitive enhancement, clinical efficacy, equity, neural safety, lawful authorization, support, release, transfer, SOTA, AGI, or ASI.",
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
