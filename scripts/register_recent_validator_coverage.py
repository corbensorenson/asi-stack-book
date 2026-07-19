#!/usr/bin/env python3
"""Register recent tracked design and failure-lineage validators."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
UNITS = {
    "validate_p4_governed_usefulness_local_instrument.py": [
        "scripts/validate_p4_governed_usefulness_local_instrument.py",
        "scripts/run_p4_governed_usefulness_local_instrument_v9.py",
        "experiments/p4_governed_usefulness/local_instrument_preregistration_v9.json",
        "experiments/p4_governed_usefulness/local_instrument_tasks_v9.json",
        "experiments/p4_governed_usefulness/local_instrument_labels_v9.json",
        "experiments/p4_governed_usefulness/raw/local_instrument_qualification_v9_qwen3_8b.json",
        "experiments/p4_governed_usefulness/results/local_instrument_qualification_v9.json",
    ],
    "validate_p4_m7_update_unlearning.py": [
        "scripts/validate_p4_m7_update_unlearning.py",
        "scripts/p4_m7_update_unlearning_common.py",
        "schemas/p4_m7_update_unlearning_result.schema.json",
        "experiments/p4_update_unlearning/preregistration.json",
        "experiments/p4_update_unlearning/corpus.json",
        "experiments/p4_update_unlearning/raw/features.pt",
        "experiments/p4_update_unlearning/raw/training_run.json",
        "experiments/p4_update_unlearning/results/preflight_result.json",
        "experiments/p4_update_unlearning/results/confirmatory_result.json",
    ],
    "validate_p4_m7_update_unlearning_design.py": [
        "scripts/validate_p4_m7_update_unlearning_design.py",
        "scripts/p4_m7_update_unlearning_common.py",
        "experiments/p4_update_unlearning/preregistration.json",
        "experiments/p4_update_unlearning/corpus.json",
        "experiments/p4_update_unlearning/results/preflight_result.json",
    ],
    "validate_p4_m7_update_unlearning_failure_lineage.py": [
        "scripts/validate_p4_m7_update_unlearning_failure_lineage.py",
        "experiments/p4_update_unlearning/v1_failure_diagnosis.json",
        "experiments/p4_update_unlearning_v2/preflight_failure_diagnosis.json",
        "experiments/p4_update_unlearning_v3/preregistration.json",
    ],
    "validate_p4_m7_update_unlearning_v3_design.py": [
        "scripts/validate_p4_m7_update_unlearning_v3_design.py",
        "scripts/p4_m7_update_unlearning_v3_common.py",
        "experiments/p4_update_unlearning_v2/corpus.json",
        "experiments/p4_update_unlearning_v3/preregistration.json",
        "experiments/p4_update_unlearning_v3/results/preflight_result.json",
        "experiments/p4_update_unlearning/v1_failure_diagnosis.json",
        "experiments/p4_update_unlearning_v2/preflight_failure_diagnosis.json",
    ],
    "validate_p4_m8_world_model_design.py": [
        "scripts/validate_p4_m8_world_model_design.py",
        "scripts/p4_m8_world_model_common.py",
        "schemas/p4_m8_world_model_result.schema.json",
        "experiments/p4_situated_world_model/environments.json",
        "experiments/p4_situated_world_model/design.json",
        "experiments/p4_situated_world_model/preregistration.json",
    ],
    "validate_reflexive_dispatch_trace.py": [
        "scripts/validate_reflexive_dispatch_trace.py",
        "tests/fixtures/protocol_records/reflexive_dispatch_trace_record.valid.json",
        "book_structure.json",
    ],
}


def main() -> None:
    value = json.loads(REGISTRY.read_text()); required = list(value["required_artifacts"])
    existing_order = {x.get("script"): x.get("order") for x in value["units"]}
    value["units"] = [x for x in value["units"] if x.get("script") not in UNITS]
    used = {x["order"] for x in value["units"]}
    for script, artifacts in UNITS.items():
        preferred = existing_order.get(script)
        order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + len(UNITS) + 2) if i not in used)
        used.add(order)
        value["units"].append({"id": f"{script}:{order}", "order": order, "script": script, "args": [], "execution_tier": "pr", "validation_class": "proof_or_evidence_gate", "input_contract": "Tracked prospective design, failure-lineage, source-interface, or instrument-qualification artifacts for a recently completed roadmap campaign.", "input_artifacts": artifacts, "output_contract": "Preserve exact frozen identities, failure boundaries, rejecting mutations, and zero unsupported chapter-core or release movement.", "output_assertions": ["validator executes from the authoritative registry", "frozen design or failure lineage remains exact", "rejecting controls remain effective", "no unsupported chapter-core or release authority is inferred"], "claim_scope": "Exact tracked design, failure-lineage, instrument, or dispatch-interface contract only.", "negative_controls": "validator_owned_mutations", "negative_control_cases": ["identity drift", "denominator drift", "failure erasure", "support laundering"], "prohibited_inference": "Does not establish natural-task usefulness, transfer, deployment, SOTA, AGI, ASI, publication, release, or chapter-core support.", "contract_precision": "exact", "semantic_review_state": "checked_recent_validator_coverage"})
        for artifact in artifacts:
            if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda x: x["order"]); value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}; REGISTRY.write_text(json.dumps(value, indent=2) + "\n"); print(f"Registered {len(UNITS)} recent validators: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
