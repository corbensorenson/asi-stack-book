#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; REGISTRY = ROOT / "validation/registry.json"; SCRIPT = "validate_cognitive_compilation_refinement.py"
ARTIFACTS = ["scripts/validate_cognitive_compilation_refinement.py", "schemas/cognitive_compilation_refinement.schema.json", "experiments/cognitive_compilation_refinement/results/2026-07-15-local.json", "docs/cognitive_compilation_refinement.md", "evidence_quality/model_adequacy_dossiers/cognitive-compilation-refinement.md", "lean/AsiStackProofs/CognitiveCompilationRefinement.lean", "schemas/semantic_atom.schema.json", "experiments/cognitive_compilation_traces/fixtures", "experiments/cognitive_compilation_traces/results/2026-07-02-local.md"]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8")); value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]; order = len(value["units"]) + 1
    value["units"].append({"id": f"validate_cognitive_compilation_refinement:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "deep", "validation_class": "proof_or_evidence_gate", "input_contract": "Reachable Lean compilation model, semantic-atom schema, complete six-fixture inventory, prior trace receipt, result schema, receipt, and adequacy dossier.", "input_artifacts": ARTIFACTS, "output_contract": "Reject source/obligation/constraint/target substitution, authority widening, missing receipts, validation laundering, non-local or unversioned repair, open residuals, fixture drift, and support promotion.", "output_assertions": ["two accepted and four rejected fixtures", "seven reachable events", "forty-seven rejected mutations", "no support-state effect"], "claim_scope": "One finite three-obligation sequential compilation/repair model and six fixed hand-authored records only.", "negative_controls": "validator_owned_model_source_and_fixture_mutations", "negative_control_cases": ["source or obligation substitution", "authority widening", "receipt or validation loss", "global or unversioned repair", "target substitution", "residual-bearing acceptance"], "prohibited_inference": "Does not establish natural-language semantics, obligation completeness, source parsing, backend behavior, evaluator independence, compiled execution, measured locality, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.", "contract_precision": "inherited", "semantic_review_state": "checked_structured_cognitive_compilation_refinement_not_natural_language_external_or_deployed"})
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8"); print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
