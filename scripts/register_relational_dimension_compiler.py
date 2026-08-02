#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_relational_dimension_compiler.py"
ARTIFACTS = [
    "scripts/validate_relational_dimension_compiler.py",
    "lean/AsiStackProofs/RelationalDimensionCompiler.lean",
    "tests/fixtures/proof_models/relational_dimension_compiler_dossier.json",
    "evidence_quality/proof_model_dossiers/relational-dimension-compilation-and-polyadic-cognition.md",
    "chapters/relational-dimension-compilation-and-polyadic-cognition.qmd",
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
        "input_contract": "Canonical relational-dimension compiler Lean review, independent 54-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, role, candidate, denominator, descendant, monotonicity, receipt, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "eight-transition review reaches only Project Theseus relational-compiler-study eligibility",
            "54/54 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "role and candidate identities compose over append and entity remapping preserves role IDs",
            "omitted required roles and hidden candidates reject completeness",
            "descendant closure composes over append and an active dependent blocks contraction",
            "candidate overrun remains rejecting as generated count grows",
            "proposal, compiler, role, rescue, qualification, fallback, and authority changes invalidate receipts",
            "qualification metrics cannot recover role fidelity and named rescues cannot recover rescue competence",
            "substrate, routing, and Evidence States consumers reject missing compiler evidence",
            "42 exact Lean declarations move no chapter support, substrate adoption, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored relational-compiler review, typed-role and proposal custody, contraction closure, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_54_axis_identity_typing_rescue_qualification_compilation_contraction_boundary_role_candidate_descendant_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["role omission", "candidate omission", "active descendant", "expired contract", "scope drift", "signal collision", "support promotion"],
        "prohibited_inference": "Does not establish field truth, higher-order irreducibility, representational usefulness, efficiency, natural-task transfer, bounded primitive arity, safe online adaptation, support, release, transfer, SOTA, AGI, or ASI.",
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
