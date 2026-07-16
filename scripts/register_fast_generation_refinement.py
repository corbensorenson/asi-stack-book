#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "validation/registry.json"
SCRIPT = "validate_fast_generation_refinement.py"
ARTIFACTS = [
    "scripts/validate_fast_generation_refinement.py",
    "schemas/fast_generation_refinement.schema.json",
    "experiments/fast_generation_refinement/results/2026-07-15-local.json",
    "docs/fast_generation_refinement.md",
    "evidence_quality/model_adequacy_dossiers/fast-generation-refinement.md",
    "lean/AsiStackProofs/FastGenerationRefinement.lean",
    "scripts/validate_generation_mode_baselines.py",
    "scripts/validate_fast_generation_task_bundle.py",
    "scripts/validate_theseus_generation_mode_import.py",
]
registry = json.loads(PATH.read_text(encoding="utf-8"))
registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
order = len(registry["units"]) + 1
registry["units"].append({
    "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
    "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
    "input_contract": "Reachable fast-generation lifecycle, three exact bounded source suites, independent route consumer, schema, receipt, and adequacy dossier.",
    "input_artifacts": ARTIFACTS,
    "output_contract": "Reject identity, context, admission, generation, verification, fallback, accounting, promotion, closure, support, and effect failures.",
    "output_assertions": ["eight reachable stages", "sixty routes", "51 rejected non-accepting mutations", "three SHA-256-bound source suites", "support and external effect none"],
    "claim_scope": "One finite authored request-to-closure policy model plus three bounded local/static source suites.",
    "negative_controls": "validator_owned_fast_generation_route_mutations",
    "negative_control_cases": ["identity, stage, evaluator, or result substitution", "failed verification without executable fallback or complete accounting", "raw-speed or support-promotion laundering"],
    "prohibited_inference": "No model speed, useful throughput, quality, verifier adequacy, deployed fallback, serving behavior, safety, transfer, SOTA, AGI, ASI, or support.",
    "contract_precision": "inherited",
    "semantic_review_state": "checked_request_to_closure_lifecycle_not_empirical_or_support_authority",
})
required = list(registry["required_artifacts"])
for artifact in ARTIFACTS:
    if artifact not in required:
        required.append(artifact)
registry["required_artifacts"] = required
registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")
