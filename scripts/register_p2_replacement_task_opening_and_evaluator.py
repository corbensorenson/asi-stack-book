#!/usr/bin/env python3
"""Register P2 task-opening and independent-evaluator calibration validation."""

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];REGISTRY=ROOT/"validation/registry.json";SCRIPT="validate_p2_replacement_task_opening_and_evaluator.py"
ARTIFACTS=[
"evidence_quality/p2_replacement_task_opening.json","schemas/p2_replacement_task_opening.schema.json","scripts/build_p2_replacement_task_opening.py",
"scripts/p2_independent_test_log_evaluator.py","scripts/calibrate_p2_independent_test_log_evaluator.py","evidence_quality/p2_independent_test_log_evaluator_calibration.json",
"evidence_quality/p2_independent_test_log_evaluator_calibration_attempt_001.json","evidence_quality/p2_independent_test_log_evaluator_calibration_attempt_002_failed_30_of_32.json","evidence_quality/p2_independent_test_log_evaluator_calibration_attempt_003_failed_31_of_32.json",
"schemas/p2_independent_test_log_evaluator_calibration.schema.json","docs/p2_replacement_task_opening_and_evaluator_calibration.md","scripts/validate_p2_replacement_task_opening_and_evaluator.py","scripts/register_p2_replacement_task_opening_and_evaluator.py"]

def main():
 r=json.loads(REGISTRY.read_text());r["units"]=[u for u in r["units"] if u.get("script")!=SCRIPT];used={u["order"] for u in r["units"]};order=next(i for i in range(1,len(r["units"])+2) if i not in used)
 r["units"].append({"id":f"{SCRIPT}:{order}","order":order,"script":SCRIPT,"args":[],"execution_tier":"pr","validation_class":"proof_or_evidence_gate","input_contract":"Four rank-one specs opened only after provenance/image gates; exact source and expected-set digests; disjoint solution/test paths; independently implemented Cargo/Go/Maven evaluator; authored and historical calibration; failed calibration lineage; candidate outcomes and final pool closed.","input_artifacts":ARTIFACTS,"output_contract":"Require exact task identity and evaluator readiness before candidate execution while retaining every calibration defect and rejecting custody or support-state widening.","output_assertions":["four rank-one task specs","6847 expected test identities","zero solution/test path collision","independent Cargo Go and Maven grammars","12 authored and 20 historical controls","32 of 32 exact upstream and expected agreement","three failed calibration attempts retained","candidate outcomes and final pool unopened","nine mutations reject"],"claim_scope":"Development task specification and evaluator-instrument readiness only; no execution, task qualification, or claim result.","negative_controls":"validator_owned_nine_collision_denominator_execution_rank_agreement_case_outcome_final_support_mutations","negative_control_cases":["path collision","denominator drift","execution started","next rank opened","agreement loss","case shrink","outcome opened","final opened","support promotion"],"prohibited_inference":"Task opening or parser calibration does not establish task validity, coding ability, governance benefit, safety, transfer, SOTA, release, AGI, or ASI.","contract_precision":"exact","semantic_review_state":"task_identity_expected_sets_path_separation_independent_parser_calibration_failure_lineage_and_custody_reviewed"})
 for a in ARTIFACTS:
  if a not in r["required_artifacts"]:r["required_artifacts"].append(a)
 r["units"].sort(key=lambda u:u["order"]);r["summary"]={"required_artifact_count":len(r["required_artifacts"]),"unit_count":len(r["units"])};REGISTRY.write_text(json.dumps(r,indent=2)+"\n");print(f"Registered {SCRIPT}: {r['summary']['unit_count']} units, {r['summary']['required_artifact_count']} artifacts.")

if __name__=="__main__":main()
