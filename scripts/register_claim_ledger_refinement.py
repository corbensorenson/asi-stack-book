#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_claim_ledger_refinement.py"
ARTIFACTS = [
    "scripts/validate_claim_ledger_refinement.py",
    "schemas/claim_ledger_refinement.schema.json",
    "experiments/claim_ledger_refinement/results/2026-07-15-local.json",
    "docs/claim_ledger_refinement.md",
    "evidence_quality/model_adequacy_dossiers/claim-ledger-refinement.md",
    "lean/AsiStackProofs/ClaimLedgerRefinement.lean",
    "scripts/validate_claim_ledger_revision.py",
    "experiments/claim_ledger_revision/fixtures",
    "scripts/validate_contradiction_revision_lifecycle.py",
    "schemas/contradiction_revision_lifecycle_record.schema.json",
    "tests/fixtures/protocol_records/contradiction_revision_lifecycle_record.valid.json",
    "experiments/contradiction_revision_lifecycle/fixtures",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"validate_claim_ledger_refinement:{order}", "order": order, "script": SCRIPT,
        "args": [], "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean append-only lifecycle, exact 5/7 revision and 1/11 historical suites, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject stale identity or base, support self-approval, external-effect requests, contradictions, missing evidence-owner custody, overwritten history, incomplete dependencies or migration, event substitution, and incomplete surface acknowledgment.",
        "output_assertions": ["five valid and seven invalid revision fixtures", "one valid and eleven invalid historical lifecycle cases", "seventeen routes and five reachable stages", "twenty-nine rejected lifecycle mutations", "no support-state effect"],
        "claim_scope": "One finite authored single-claim event lifecycle plus two existing bounded synthetic suites only.",
        "negative_controls": "validator_owned_revision_event_and_lifecycle_mutations",
        "negative_control_cases": ["claim, base, version, or event substitution", "ledger support self-approval or external effect request", "open contradiction or missing evidence-owner receipt", "history, residual, dependency, migration, or surface omission", "skipped append, materialize, or acknowledgment stage"],
        "prohibited_inference": "Does not establish truth, evidence validity, reviewer competence, semantic equivalence, assumption completeness, natural claim extraction, concurrent persistence, deployed synchronization, causal usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_append_only_lifecycle_not_natural_concurrent_deployed_or_support_authority",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
