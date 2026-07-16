#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "validation/registry.json"
SCRIPT = "validate_compact_generation_refinement.py"
ARTIFACTS = [
    "scripts/validate_compact_generation_refinement.py",
    "schemas/compact_generation_refinement.schema.json",
    "experiments/compact_generation_refinement/results/2026-07-15-local.json",
    "docs/compact_generation_refinement.md",
    "evidence_quality/model_adequacy_dossiers/compact-generation-refinement.md",
    "lean/AsiStackProofs/CompactGenerationRefinement.lean",
    "scripts/validate_compact_gvr_slice.py",
    "scripts/validate_residual_honesty_conservation.py",
    "scripts/validate_residual_ledger_trace.py",
    "scripts/validate_residual_ledger_storage_replay.py",
]
registry = json.loads(PATH.read_text(encoding="utf-8"))
registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
order = len(registry["units"]) + 1
registry["units"].append({
    "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
    "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
    "input_contract": "Reachable compact-generation lifecycle, four exact bounded result families, independent route consumer, schema, receipt, and adequacy dossier.",
    "input_artifacts": ARTIFACTS,
    "output_contract": "Reject identity, source, rights, generation, verification, fallback, residual, result, migration, consumer, replay, closure, support, and effect failures.",
    "output_assertions": ["nine reachable stages", "sixty routes", "51 rejected non-accepting mutations", "four SHA-256-bound result families", "support and external effect none"],
    "claim_scope": "One finite authored source-to-closure policy model plus four bounded local result families.",
    "negative_controls": "validator_owned_compact_generation_route_mutations",
    "negative_control_cases": ["identity or result substitution", "lossy exactness or failed verification without executable fallback", "residual, migration, consumer, chain, support, or effect gap"],
    "prohibited_inference": "No useful compression, codec correctness, verifier adequacy, semantic grounding, deployed fallback, residual completeness, safety, transfer, SOTA, AGI, ASI, or support.",
    "contract_precision": "inherited",
    "semantic_review_state": "checked_source_to_closure_lifecycle_not_empirical_or_support_authority",
})
required = list(registry["required_artifacts"])
for artifact in ARTIFACTS:
    if artifact not in required:
        required.append(artifact)
registry["required_artifacts"] = required
registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")
