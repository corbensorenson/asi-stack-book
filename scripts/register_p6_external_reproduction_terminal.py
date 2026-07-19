#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"validation/registry.json"
SCRIPT="validate_p6_external_reproduction_terminal.py"
ARTIFACTS=[
    "scripts/validate_p6_external_reproduction_terminal.py",
    "scripts/register_p6_external_reproduction_terminal.py",
    "schemas/p6_external_reproduction_terminal.schema.json",
    "experiments/p6_external_reproduction/comparator_ledger.json",
    "experiments/p6_external_reproduction/hardware_access_preflight.json",
    "experiments/p6_external_reproduction/onecell_defeat_prediction.json",
    "experiments/p6_external_reproduction/results/terminal_result.json",
    "docs/p6_external_reproduction_and_sota_challenge.md",
]
def main():
    value=json.loads(REGISTRY.read_text());value["units"]=[row for row in value["units"] if row.get("script")!=SCRIPT]
    used={row["order"] for row in value["units"]};order=next(i for i in range(1,len(value["units"])+2) if i not in used)
    value["units"].append({"id":f"{SCRIPT}:{order}","order":order,"script":SCRIPT,"args":[],"execution_tier":"pr","validation_class":"proof_or_evidence_gate","input_contract":"Dated primary/official comparator ledger, host-access preflight, frozen OneCell defeat prediction, and exact seven-atom P6 terminal record before any outcome-bearing ASI Stack comparison.","input_artifacts":ARTIFACTS,"output_contract":"Preserve five strongest/current comparator blockers, seven blocked-after-full-attempt dispositions, zero external reproductions or SOTA support, and six rejecting mutations.","output_assertions":["five current comparator records","seven exact claim atoms","all dispositions blocked after full attempt","zero outcome runs/reproductions/SOTA/core movement","six mutations reject"],"claim_scope":"Replaceable cognitive substrates, heterogeneous architecture tournament, OneCell, total-system KISS, and architectural-RSI external reproduction envelope.","negative_controls":"validator_owned_six_p6_laundering_mutations","negative_control_cases":["invented reproduction","invented SOTA","atom deletion","disposition widening","digest rewrite","core promotion"],"prohibited_inference":"The blocker record is not a reproduction, comparison, null result, refutation, competitive result, Pareto result, deployment, publication, release, AGI, or ASI claim.","contract_precision":"exact","semantic_review_state":"checked_current_comparator_displacement_access_blockers_defeat_prediction_and_zero_outcome_boundary"})
    required=list(value["required_artifacts"])
    for path in ARTIFACTS:
        if path not in required: required.append(path)
    value["units"].sort(key=lambda row:row["order"]);value["required_artifacts"]=required;value["summary"]={"required_artifact_count":len(required),"unit_count":len(value["units"])}
    REGISTRY.write_text(json.dumps(value,indent=2)+"\n");print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")
if __name__=="__main__":main()
