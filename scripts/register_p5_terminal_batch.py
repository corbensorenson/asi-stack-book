#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"validation/registry.json";SCRIPT="validate_p5_terminal_batch.py"
ART=["scripts/build_p5_terminal_batch.py","scripts/evaluate_p5_terminal_batch.py","scripts/validate_p5_terminal_batch.py","schemas/p5_terminal_batch_result.schema.json","experiments/p5_terminal_batch/design.json","experiments/p5_terminal_batch/preregistration.json","experiments/p5_terminal_batch/results/result.json","docs/p5_mandatory_terminal_batch.md"]
def main():
 v=json.loads(P.read_text());v["units"]=[x for x in v["units"] if x.get("script")!=SCRIPT];used={x["order"] for x in v["units"]};order=next(i for i in range(1,len(v["units"])+2) if i not in used)
 v["units"].append({"id":f"{SCRIPT}:{order}","order":order,"script":SCRIPT,"args":[],"execution_tier":"pr","validation_class":"proof_or_evidence_gate","input_contract":"Prospectively frozen mandatory P5 three-atom terminal batch.","input_artifacts":ART,"output_contract":"Preserve two bounded subordinate promotions, one full-attempt narrowing, missing service restart and compensation, and zero chapter-core movement.","output_assertions":["three exact atoms","two bounded promotions","one narrowing at argument","four mutations reject","zero chapter-core movement"],"claim_scope":"One pinned Circle target, one finite authority model, and bounded local replacement/update records.","negative_controls":"validator_owned_four_terminal_batch_mutations","negative_control_cases":["chapter-core promotion","rollback laundering","compensation rewrite","authority mutation erasure"],"prohibited_inference":"No general transport, deployed authority, effect-complete rollback, transfer, SOTA, AGI, ASI, publication, or release.","contract_precision":"exact","semantic_review_state":"checked_three_atom_terminal_dispositions"})
 req=list(v["required_artifacts"])
 for x in ART:
  if x not in req:req.append(x)
 v["units"].sort(key=lambda x:x["order"]);v["required_artifacts"]=req;v["summary"]={"required_artifact_count":len(req),"unit_count":len(v["units"])};P.write_text(json.dumps(v,indent=2)+"\n");print(f"Registered {SCRIPT}: {len(v['units'])} units.")
if __name__=="__main__":main()
