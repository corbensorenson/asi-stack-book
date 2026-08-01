#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_communication_influence_review.py"
ARTIFACTS = [
    "scripts/validate_communication_influence_review.py",
    "lean/AsiStackProofs/CommunicationInfluenceReview.lean",
    "tests/fixtures/proof_models/communication_influence_dossier.json",
    "evidence_quality/proof_model_dossiers/human-ai-communication-persuasion-and-epistemic-security.md",
    "chapters/human-ai-communication-persuasion-and-epistemic-security.qmd",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
    "docs/book_outline.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + 2) if i not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Canonical communication-influence Lean model, independent 42-axis fixture, chapter proof boundary, proof dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, exposure-monotonicity, denied-attribute noninterference, collision-witness, canonical-binding, and no-promotion drift.",
        "output_assertions": [
            "six-stage review reaches only Project Theseus benign communication-study eligibility",
            "42/42 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "expiry, audience overrun, and repetition overrun remain rejecting under adverse monotone changes",
            "typed personalization is invariant to denied attributes outside its allowed projection",
            "surface signals cannot recover the full influence state and provenance cannot recover comprehension",
            "21 exact Lean declarations move no chapter support, delivery, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored-record review, arithmetic exposure controls, typed noninterference, and finite non-identifiability only.",
        "negative_controls": "validator_owned_42_axis_monotonicity_noninterference_collision_and_binding_mutations",
        "negative_control_cases": ["missing claim custody", "denied-attribute reuse", "audience overrun", "false surface-signal sufficiency", "false provenance comprehension", "support promotion laundering"],
        "prohibited_inference": "Does not establish truth, comprehension, autonomy, persuasion efficacy, manipulation detection, correction efficacy, benefit, harm, safety, delivery authority, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact", "semantic_review_state": "checked_bounded_formal_model_and_independent_consumer_no_support_effect",
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
