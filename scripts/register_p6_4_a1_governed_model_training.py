#!/usr/bin/env python3
"""Register the terminal P6.4-A1 governed-model-training validation packet."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = "scripts/register_p6_4_a1_governed_model_training.py"
UNITS = [
    {
        "script": "validate_training_run_transaction.py",
        "artifacts": ["scripts/validate_training_run_transaction.py", "schemas/training_run_transaction.schema.json", "tests/fixtures/protocol_records/training_run_transaction.valid.json", "experiments/governed_model_training_argument_exit/preregistration.json", "lean/AsiStackProofs/GovernedModelTraining.lean", "lean/AsiStackProofs.lean", "chapters/governed-model-training-distributed-optimization-and-scaling.qmd"],
        "input_contract": "One authored non-empirical training transaction, ten required state classes, seven source records, eight non-authorities, and a prospectively frozen five-arm natural campaign.",
        "output_contract": "Require topology/batch reconciliation, full attempted-run denominator, complete consistent durable checkpoint state, resume-accounting fields, validation-only checkpoint-family selection, independent unopened qualification, and 21 rejecting mutations.",
        "output_assertions": ["10 state classes", "7 sources", "8 non-authorities", "5 prospective arms", "13 fault families", "12 competence gates", "21 mutations reject", "no training/support/release effect"],
        "claim_scope": "Authored training-run record shape and finite qualification-handoff semantics only.",
        "negative_controls": "validator_owned_twenty_one_freeze_topology_batch_numeric_denominator_state_commit_resume_selection_qualification_source_and_authority_mutations",
        "prohibited_inference": "No model training, resume equivalence, distributed efficiency, fault tolerance, model quality, inventory completeness, support, readiness, release, transfer, SOTA, AGI, or ASI follows.",
    },
    {
        "script": "validate_p6_4_a1_governed_model_training_reader_integration.py",
        "artifacts": ["scripts/validate_p6_4_a1_governed_model_training_reader_integration.py", "evidence_quality/p6_4_a1_governed_model_training_reader_integration.json", "docs/p6_4_a1_governed_model_training_adjudication.md", "book_structure.json", "sources/source_inventory.json", "proofs/proof_manifest.json", "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json", "index.qmd", "appendices/B_glossary.qmd", "chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd", "chapters/integrated-reference-architecture.qmd"],
        "input_contract": "Terminal A1 decision, seven-source four-role packet, one argument chapter, two implemented targets, thirteen theorem declarations, one authored contract, one unopened natural protocol, and reconciled reader/status surfaces.",
        "output_contract": "Bind exact artifact and source-note digests, require exclusive placement and neighbor handoffs, preserve source/proof/protocol denominators, advance exactly to A2, and reject nine integration mutations.",
        "output_assertions": ["1 terminal A1 chapter", "7 source notes", "4 source roles", "2 implemented targets", "13 theorems", "60 chapters", "A2 active", "9 integration mutations reject", "support effect none"],
        "claim_scope": "A1 chapter necessity, argument-level integration, artifact custody, and no-promotion boundary only.",
        "negative_controls": "validator_owned_nine_decision_source_manifest_proof_campaign_competence_status_and_support_mutations",
        "prohibited_inference": "Reader integration and finite artifacts do not establish training integrity, exact resume, model quality, efficiency, fault tolerance, support, readiness, release, transfer, or SOTA.",
    },
]


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    path = ROOT / "validation/registry.json"
    registry = json.loads(path.read_text())
    scripts = {row["script"] for row in UNITS}
    registry["units"] = [row for row in registry["units"] if row.get("script") not in scripts]
    next_order = len(registry["units"]) + 1
    for offset, spec in enumerate(UNITS):
        unit = {key: value for key, value in spec.items() if key != "artifacts"}
        unit.update({
            "id": f"{spec['script']}:{next_order + offset}", "order": next_order + offset,
            "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
            "contract_precision": "exact_record_denominator_and_semantic_disposition_contract",
            "input_artifacts": spec["artifacts"] + [REGISTER],
        })
        registry["units"].append(unit)
    required = list(registry["required_artifacts"])
    for spec in UNITS:
        for artifact in spec["artifacts"] + [REGISTER]:
            if artifact not in required:
                required.append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["required_artifacts"] = required
    registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
    dump(path, registry)
    print(f"Registered terminal P6.4-A1 packet: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
