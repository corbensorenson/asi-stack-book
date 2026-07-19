#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_claim_family_terminal_program.py"
ARTIFACTS = [
    "scripts/build_claim_family_terminal_program.py",
    "scripts/evaluate_claim_family_terminal_program.py",
    "scripts/validate_claim_family_terminal_program.py",
    "scripts/register_claim_family_terminal_program.py",
    "schemas/claim_family_terminal_coverage.schema.json",
    "experiments/claim_family_terminal_coverage/design.json",
    "experiments/claim_family_terminal_coverage/preregistration.json",
    "experiments/claim_family_terminal_coverage/preflight_receipt.json",
    "experiments/claim_family_terminal_coverage/results/result.json",
    "experiments/claim_family_terminal_coverage/results/schema_repair_receipt.json",
    "docs/claim_family_terminal_coverage.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(
        candidate for candidate in range(1, len(value["units"]) + 2) if candidate not in used
    )
    value["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "One prospectively frozen, single-shot terminal disposition audit over all 3,745 CF-01 through CF-08 claim atoms, including explicit preflight and conservative schema-repair lineage.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Preserve 3,698 exact blocked gaps, 36 retained states, nine narrowings, two previously accepted bounded promotions, and zero chapter-core movement.",
        "output_assertions": [
            "3,745 unique atoms and all eight families remain exact",
            "every block retains at least one named missing lane",
            "every bounded promotion resolves to an accepted transition",
            "single-shot preflight and two-record conservative repair lineage remain exact",
            "four laundering mutations reject and no chapter core moves",
        ],
        "claim_scope": "Repository-local terminal disposition coverage for the frozen activation registry and accepted 15-atom addendum.",
        "negative_controls": "validator_owned_four_terminal_coverage_mutations",
        "negative_control_cases": [
            "denominator loss",
            "chapter-core promotion",
            "unsupported promotion",
            "missing-lane erasure",
        ],
        "prohibited_inference": "Coverage is not proof of truth, empirical success, causal identification, transfer, deployment, SOTA, AGI, ASI, publication, release, or completion of the family natural-work bundle gate.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_terminal_dispositions_missing_lanes_and_no_promotion_boundary",
    })
    required = list(value["required_artifacts"])
    for path in ARTIFACTS:
        if path not in required:
            required.append(path)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(value["units"]),
    }
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
