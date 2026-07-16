#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; REGISTRY = ROOT / "validation/registry.json"; SCRIPT = "validate_virtual_context_refinement.py"
ARTIFACTS = ["scripts/validate_virtual_context_refinement.py", "schemas/virtual_context_refinement.schema.json", "experiments/virtual_context_refinement/results/2026-07-15-local.json", "docs/virtual_context_refinement.md", "evidence_quality/model_adequacy_dossiers/virtual-context-refinement.md", "lean/AsiStackProofs/VirtualContextRefinement.lean", "experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json", "scripts/validate_context_admission_adequacy.py", "experiments/context_admission_adequacy/fixtures"]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8")); value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]; order = len(value["units"]) + 1
    value["units"].append({"id": f"validate_virtual_context_refinement:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "deep", "validation_class": "proof_or_evidence_gate", "input_contract": "Reachable Lean Virtual Context model, exact eleven-scenario resolver receipt, complete eight-fixture admission inventory, independent consumer, result schema, receipt, and adequacy dossier.", "input_artifacts": ARTIFACTS, "output_contract": "Reject request/address/version/snapshot/mount substitution, expired leases, denied mounts, source/certificate mismatch, authority widening, omission and completeness laundering, taint, missing receipts, fault/materialization conflict, inventory drift, and support promotion.", "output_assertions": ["two valid and nine invalid resolver scenarios", "three valid and five invalid admission fixtures remain distinct", "four-event materialization and two-event fault traces", "fifty-five rejected mutations", "no support-state effect"], "claim_scope": "One finite sequential resolver/certificate/materialization model, eleven prior synthetic resolver scenarios, and a distinct eight-fixture admission suite only.", "negative_controls": "validator_owned_model_source_and_fixture_mutations", "negative_control_cases": ["request binding substitution", "expired or denied resolution", "certificate source or authority mismatch", "omission, overclaim, or taint", "missing receipt or fault/materialization conflict"], "prohibited_inference": "Does not establish natural-language address truth, payload meaning, summary fidelity, certificate truthfulness, deployed resolver/store behavior, concurrency, deletion enforcement, context quality, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.", "contract_precision": "inherited", "semantic_review_state": "checked_structured_virtual_context_refinement_not_natural_language_external_or_deployed"})
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8"); print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
