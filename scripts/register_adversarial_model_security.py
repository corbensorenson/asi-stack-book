#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_adversarial_model_security.py"
ARTIFACTS = [
    "scripts/validate_adversarial_model_security.py",
    "lean/AsiStackProofs/AdversarialModelSecurity.lean",
    "tests/fixtures/proof_models/adversarial_model_security_dossier.json",
    "evidence_quality/proof_model_dossiers/adversarial-machine-learning-and-model-attack-surface.md",
    "chapters/adversarial-machine-learning-and-model-attack-surface.qmd",
    "proofs/proof_manifest.json", "proofs/proof_triage.json", "docs/book_outline.md",
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
        "input_contract": "Canonical adversarial-model-security Lean model, independent 58-axis fixture, chapter proof boundary, proof dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, assurance-substitution, disposition-scope, trace-quarantine, collision-witness, consumer-bridge, canonical-binding, and no-promotion drift.",
        "output_assertions": [
            "eight-step review reaches only Project Theseus model-security campaign eligibility",
            "58/58 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "certificate, monitoring, and recovery obligations remain non-substitutable",
            "checkpoint change, configuration change, budget widening, and expiry invalidate bounded dispositions",
            "quarantineAll covers every member of an arbitrary finite attack-trace list",
            "aggregate scores cannot recover bounded security state and local checks cannot recover composed-path reachability",
            "the adversarial-evaluation consumer receives only bounded observation fields and no support or external authority",
            "28 exact Lean declarations move no chapter support, deployment, attack, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored threat review, typed assurance separation, finite disposition checks, inductive trace quarantine, consumer refinement, and finite non-identifiability only.",
        "negative_controls": "validator_owned_58_axis_assurance_disposition_quarantine_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["weak positive control", "defense-unaware attack", "incomplete denominator", "certificate laundering", "configuration drift", "component composition", "attack authorization", "support promotion"],
        "prohibited_inference": "Does not establish robustness, exploitability, attack reachability, defense efficacy, detector competence, recovery efficacy, confidentiality, secure deployment, attack authority, transfer, SOTA, AGI, or ASI.",
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
