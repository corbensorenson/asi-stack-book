#!/usr/bin/env python3
"""Register the executed Authority grant-to-effect refinement."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_authority_effect_refinement.py"
ARTIFACTS = [
    "scripts/validate_authority_effect_refinement.py",
    "schemas/authority_effect_refinement.schema.json",
    "experiments/authority_effect_refinement/results/2026-07-15-local.json",
    "docs/authority_effect_refinement.md",
    "evidence_quality/model_adequacy_dossiers/authority-effect-refinement.md",
    "lean/AsiStackProofs/AuthorityEffectRefinement.lean",
    "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    "experiments/authority_revocation_trace/results/2026-07-03-local.json",
    "experiments/governed_repository_change_slice/results/2026-07-10-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"validate_authority_effect_refinement:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The reachable Lean grant-to-effect model, authority decision fixtures, executed runtime effect/denial result, revocation trace, governed repository result, schema, receipt, and adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject authority amplification, exact-binding substitution, stale/expired/revoked grants, receipt bypass, effect without dispatch, nonindependent observation, inexact rollback, one-shot reuse, source drift, and support promotion.",
        "output_assertions": ["six authority fixtures", "six reachable witness events", "one executed local effect", "one independent observation", "one exact rollback", "two pre-effect denials", "five revocation entries", "nine governed scenarios", "thirty-eight rejected mutations", "no support-state effect"],
        "claim_scope": "One finite numeric-identity model and fixed local executed evidence surfaces only.",
        "negative_controls": "validator_owned_model_and_source_semantic_mutations",
        "negative_control_cases": ["grant identity or binding substitution", "authority widening", "stale epoch or expiry", "missing approval/dispatch/effect receipt", "post-revocation dispatch", "nonindependent observation", "inexact rollback", "one-shot reuse"],
        "prohibited_inference": "The finite local refinement does not establish natural-language authority extraction, authentic identity or receipts, wise issuance, concurrent revocation, complete effects, deployed enforcement, production security, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_finite_grant_effect_refinement_not_authentic_concurrent_external_or_deployed",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
