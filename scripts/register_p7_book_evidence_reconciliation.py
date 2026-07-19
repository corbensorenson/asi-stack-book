#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/"validation/registry.json";SCRIPT="validate_p7_book_evidence_reconciliation.py"
ART=["scripts/reconcile_p7_chapter_evidence.py","scripts/build_p7_book_evidence_reconciliation.py","scripts/validate_p7_book_evidence_reconciliation.py","scripts/register_p7_book_evidence_reconciliation.py","schemas/p7_book_evidence_reconciliation.schema.json","experiments/p7_book_evidence_reconciliation/result.json","docs/p7_book_evidence_reconciliation.md","sources/source_notes/ext_gated_deltanet2_2026.md"]
def main():
 v=json.loads(R.read_text());v["units"]=[x for x in v["units"] if x.get("script")!=SCRIPT];used={x["order"] for x in v["units"]};o=next(i for i in range(1,len(v["units"])+2) if i not in used)
 v["units"].append({"id":f"{SCRIPT}:{o}","order":o,"script":SCRIPT,"args":[],"execution_tier":"pr","validation_class":"proof_or_evidence_gate","input_contract":"One exact reconciliation packet per live chapter, canonical atom/family/P6 results, current source correction, five generated appendices, and regenerated reader projection.","input_artifacts":ART,"output_contract":"Preserve 55 chapter packets, 3,698 blocked gaps, current Gated DeltaNet-2/P6 boundaries, reader projection, five appendices, and zero core movement.","output_assertions":["55 exact chapter packets","3,745 atom denominator and 3,698 blocked gaps","five appendices digest-bound","reader projection replays","five mutations reject"],"claim_scope":"Book and evidence reconciliation only.","negative_controls":"validator_owned_five_p7_laundering_mutations","negative_control_cases":["chapter deletion","digest rewrite","packet erasure","gap erasure","core promotion"],"prohibited_inference":"Packet, appendix, vector, reader, or render coverage does not prove chapter truth, external reproduction, transfer, SOTA, reader approval, publication, or release.","contract_precision":"exact","semantic_review_state":"checked_chapter_specific_atom_dispositions_family_boundaries_current_source_and_reader_projection"})
 req=list(v["required_artifacts"])
 for p in ART:
  if p not in req:req.append(p)
 v["units"].sort(key=lambda x:x["order"]);v["required_artifacts"]=req;v["summary"]={"required_artifact_count":len(req),"unit_count":len(v["units"])};R.write_text(json.dumps(v,indent=2)+"\n");print(f"Registered {SCRIPT}: {len(v['units'])} units, {len(req)} artifacts.")
if __name__=="__main__":main()
