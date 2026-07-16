#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_command_semantic_refinement.py"
ARTIFACTS = [
    "scripts/validate_command_semantic_refinement.py",
    "schemas/command_semantic_refinement.schema.json",
    "experiments/command_semantic_refinement/results/2026-07-15-local.json",
    "docs/command_semantic_refinement.md",
    "evidence_quality/model_adequacy_dossiers/command-semantic-refinement.md",
    "lean/AsiStackProofs/CommandSemanticRefinement.lean",
    "schemas/command_contract.schema.json",
    "experiments/plan_execution_contracts/fixtures",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json",
    "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"validate_command_semantic_refinement:{order}", "order": order,
        "script": SCRIPT, "args": [], "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The reachable Lean command model, command schema, complete plan fixture inventory, prior handoff and vertical results, schema, receipt, and adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject slot/provenance/confidence, lineage/time, precedence, authority, blocker, approval, planning-validation, dispatch-receipt, fixture-classification, source-drift, and support-promotion failures.",
        "output_assertions": ["thirteen schema-valid command fixtures", "five command-interface violations", "two correct command-interface blocks", "six command-interface-admissible records without whole-fixture acceptance", "five reachable events", "thirty-eight rejected mutations", "no support-state effect"],
        "claim_scope": "One finite structured command-boundary model, fixed synthetic fixtures, and digest-bound prior local results only.",
        "negative_controls": "validator_owned_model_source_and_classification_mutations",
        "negative_control_cases": ["missing, inferred, or substituted slots", "hidden provenance or applied override", "inferred or widened authority", "missing approval or receipts", "open blockers", "interface-to-whole-fixture laundering"],
        "prohibited_inference": "Does not establish natural-language semantic preservation, calibrated confidence, authentic authority extraction, prompt-injection containment, deployed dispatch/effects, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_command_semantic_refinement_not_natural_language_external_or_deployed",
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
