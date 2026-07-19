#!/usr/bin/env python3
"""Register the P2 replacement provenance preflight validator."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_replacement_provenance_preflight.py"
ARTIFACTS = [
    "evidence_quality/p2_replacement_provenance_preflight.json",
    "schemas/p2_replacement_provenance_preflight.schema.json",
    "docs/p2_replacement_provenance_preflight.md",
    "scripts/validate_p2_replacement_provenance_preflight.py",
    "scripts/register_p2_replacement_provenance_preflight.py",
    "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
]

def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Rank one from each frozen replacement slot; public merge and exact base-parent receipt; license file at base; image manifest digest/platform receipt; no dataset task content, image pull, candidate outcome, or final-pool access.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Admit only provenance-complete rank-one candidates to resource measurement while preserving exact fallback disclosure and pre-outcome custody.",
        "output_assertions": ["four rank-one candidates", "public merged-change receipt", "base commit is merge parent", "GitHub merge signature verified", "license blob bound to base", "Linux amd64 image digest resolves", "compressed layers not represented as expanded size", "incidental title exposure disclosed", "task content outcomes and final pool unopened", "ten mutations reject"],
        "claim_scope": "Replacement provenance and manifest feasibility only; no task qualification or claim-bearing result.",
        "negative_controls": "validator_owned_ten_base_signature_license_architecture_size_content_disclosure_qualification_final_support_mutations",
        "negative_control_cases": ["base detached", "signature unverified", "license unbound", "wrong architecture", "expanded size invented", "problem opened", "title exposure erased", "qualification started", "final opened", "support promotion"],
        "prohibited_inference": "A public change, license, or image manifest does not establish task validity, coding ability, governance benefit, safety, transfer, SOTA, release, AGI, or ASI.",
        "contract_precision": "exact", "semantic_review_state": "rank_one_public_change_base_license_manifest_fallback_disclosure_and_custody_reviewed"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]: registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")

if __name__ == "__main__": main()
