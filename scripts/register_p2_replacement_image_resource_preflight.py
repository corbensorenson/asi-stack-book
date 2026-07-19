#!/usr/bin/env python3
"""Register P2 rank-one image resource preflight validation."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_replacement_image_resource_preflight.py"
ARTIFACTS = [
    "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r1/result.json",
    "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r2/result.json",
    "evidence_quality/p2_resource_ceiling.json", "evidence_quality/p2_replacement_provenance_preflight.json",
    "schemas/p2_replacement_image_resource_preflight.schema.json", "docs/p2_replacement_image_resource_preflight.md",
    "scripts/run_p2_replacement_image_resource_preflight.py", "scripts/validate_p2_replacement_image_resource_preflight.py", "scripts/register_p2_replacement_image_resource_preflight.py"
]

def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")); registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}; order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Frozen rank-one provenance and resource ceilings; clean uncached digest pulls; local size/platform inspection; sequential cleanup; raw logs; per-task and campaign residuals; failed-recorder attempt retained as N0.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Qualify only image-resource feasibility while rejecting cache-contaminated, over-ceiling, digest-mismatched, cleanup-defective, custody-breaching, or claim-promoting records.",
        "output_assertions": ["failed R1 retained as N0", "R1 measurements not recovered", "four clean R2 digest pulls", "pull and image ceilings pass", "Linux amd64 inspection passes", "cleanup and task residual gates pass", "campaign residual gate passes", "raw log digests verify", "task content outcomes and final pool closed", "twelve mutations reject"],
        "claim_scope": "Rank-one image resource feasibility only; dependency, oracle, dual-evaluator, repeatability, task, mechanism, and final evidence gates remain pending.",
        "negative_controls": "validator_owned_twelve_timeout_wall_size_digest_cleanup_residual_arithmetic_gate_content_qualification_final_support_mutations",
        "negative_control_cases": ["pull timeout", "pull over ceiling", "size over ceiling", "wrong digest", "cleanup failure", "task residual over ceiling", "campaign arithmetic drift", "gate removed", "task content opened", "qualification started", "final opened", "support promotion"],
        "prohibited_inference": "Image feasibility does not establish task validity, coding ability, governance benefit, safety, transfer, SOTA, release, AGI, or ASI.",
        "contract_precision": "exact", "semantic_review_state": "failed_attempt_custody_digest_pull_expanded_size_platform_cleanup_residual_and_nonpromotion_reviewed"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]: registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"]); registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8"); print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")

if __name__ == "__main__": main()
