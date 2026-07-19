#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_claim_family_bundle_coverage.py"
ARTIFACTS = [
    "scripts/validate_claim_family_bundle_coverage.py",
    "scripts/register_claim_family_bundle_coverage.py",
    "schemas/claim_family_bundle_coverage.schema.json",
    "experiments/claim_family_bundle_coverage/result.json",
    "docs/claim_family_bundle_coverage.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    order = next(candidate for candidate in range(1, len(value["units"]) + 2) if candidate not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Eight exact existing end-to-end or natural-work bundles, one for each CF-01 through CF-08 family, bound to result digests and their own rejecting validators.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Replay all selected validators, preserve 3,698 blocked atom gaps, reject five laundering mutations, and create zero new support or chapter-core movement.",
        "output_assertions": ["all eight families covered once", "all eight validators replay", "result digests remain exact", "3,698 blocked gaps remain visible", "five mutations reject"],
        "claim_scope": "Minimum P5 family-bundle breadth gate only.",
        "negative_controls": "validator_owned_five_family_bundle_mutations",
        "negative_control_cases": ["family deletion", "validator erasure", "digest rewrite", "core promotion", "blocked-gap erasure"],
        "prohibited_inference": "One bundle does not prove all family atoms, and gate coverage does not imply transfer, deployment, SOTA, publication, release, or whole-book truth.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bundle_scope_negative_controls_terminal_boundaries_and_residual_gap_preservation",
    })
    required = list(value["required_artifacts"])
    for path in ARTIFACTS:
        if path not in required:
            required.append(path)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
