#!/usr/bin/env python3
"""Register validation for the P2 natural development-corpus preflight."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_development_corpus_preflight.py"
ARTIFACTS = [
    "evidence_quality/p2_development_corpus_preflight.json",
    "schemas/p2_development_corpus_preflight.schema.json",
    "docs/p2_development_corpus_preflight.md",
    "experiments/p2_governed_repository_admission/corpus/post_snapshot_eligible_metadata.jsonl",
    "experiments/p2_governed_repository_admission/corpus/development_pool.json",
    "experiments/p2_governed_repository_admission/corpus/image_manifest_receipts.json",
    "sources/source_inventory.json",
    "sources/source_notes/ext_swe_rebench_v2_2026.md",
    "scripts/build_p2_development_corpus_preflight.py",
    "scripts/probe_p2_development_images.py",
    "scripts/validate_p2_development_corpus_preflight.py",
    "scripts/register_p2_development_corpus_preflight.py",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Pinned SWE-rebench V2 parquet identity; post-model-snapshot metadata universe; public merged-PR, license, diagnostic, path-separation, and image-manifest screens; development-only task pool; final-heldout closure.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Qualify a compact natural corpus for development only while rejecting task-content leakage, denominator drift, inaccessible images, contamination overclaim, premature final selection/opening, or support promotion.",
        "output_assertions": ["1117 eligible post-snapshot rows", "532 repositories and 20 languages", "12 distinct development repositories", "7 development languages", "12 image manifests", "no task text or patches vendored", "final pool unselected and closed", "ten mutations reject"],
        "claim_scope": "Corpus acquisition and development preflight only; no construct pass, benchmark result, empirical transition, support movement, or final heldout opening.",
        "negative_controls": "validator_owned_ten_corpus_custody_content_image_contamination_and_support_mutations",
        "negative_control_cases": ["denominator drift", "license failure", "task leak", "final selection", "final opening", "image missing", "image identity drift", "manifest digest drift", "contamination overclaim", "support promotion"],
        "prohibited_inference": "Development qualification does not establish gold execution, construct validity, evaluator competence, model capability, governance benefit, safety, transfer, reproduction, SOTA, release, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "source_revision_cutoff_rights_provenance_task_custody_path_collision_image_and_false_negative_boundaries_reviewed",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()
