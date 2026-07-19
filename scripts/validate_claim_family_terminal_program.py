#!/usr/bin/env python3
import copy,json
from collections import Counter
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"experiments/claim_family_terminal_coverage/results/result.json"
PREREG=ROOT/"experiments/claim_family_terminal_coverage/preregistration.json";PREFLIGHT=ROOT/"experiments/claim_family_terminal_coverage/preflight_receipt.json";REPAIR=ROOT/"experiments/claim_family_terminal_coverage/results/schema_repair_receipt.json"
def load(p):return json.loads(p.read_text())
def errors(r):
 out=[];rows=r.get("dispositions",[])
 if len(rows)!=3745 or len({x.get("atom_id") for x in rows})!=3745:out.append("atom coverage")
 if {x.get("family_id") for x in rows}!={f"CF-{i:02d}" for i in range(1,9)}:out.append("family coverage")
 allowed={"promoted_at_bounded_scope","retained_after_full_attempt","narrowed_after_full_attempt","refuted_after_full_attempt","deprecated_after_full_attempt","blocked_after_full_attempt"}
 if any(x.get("terminal_disposition") not in allowed for x in rows):out.append("nonterminal")
 if any(x["terminal_disposition"]=="blocked_after_full_attempt" and not x.get("missing_or_unproved_lanes") for x in rows):out.append("unexplained block")
 if any(x["terminal_disposition"]=="promoted_at_bounded_scope" and not x.get("accepted_transition_ref") for x in rows):out.append("unsupported promotion")
 if any(x.get("role")=="core" and x.get("terminal_disposition")=="promoted_at_bounded_scope" for x in rows) or r.get("chapter_core_promotion_count")!=0:out.append("core promotion")
 if len(r.get("attempt_receipts",[]))!=3 or any(x.get("exit_code")!=0 for x in r["attempt_receipts"]):out.append("attempt receipts")
 return out
def preflight_errors():
 out=[];prereg=load(PREREG);receipt=load(PREFLIGHT)
 expected=prereg.get("input_sha256",{});observed=receipt.get("input_sha256",{})
 if receipt.get("state")!="passed_before_outcome_generation" or receipt.get("all_frozen_inputs_match") is not True or receipt.get("outcome_file_present_at_check") is not False:out.append("preflight state")
 if set(observed)!=set(expected):out.append("preflight input coverage")
 for path,digest in expected.items():
  row=observed.get(path,{})
  if row!={"expected":digest,"observed":digest,"match":True}:out.append("preflight digest:"+path)
 if receipt.get("support_state_effect")!="none" or receipt.get("publication_authority")!="none" or receipt.get("release_authority")!="none":out.append("preflight authority")
 return out
def repair_errors(r):
 out=[];receipt=load(REPAIR);ids={"asi-is-a-stack-not-a-model.problem.001","asi-is-a-stack-not-a-model.mechanism.003"}
 if receipt.get("original_result_sha256")!="a52421af219a07fadce3a76c4700e37a3c62df263ba1e91aca826a131da02450" or receipt.get("outcome_aware_retry_performed") is not False:out.append("schema repair lineage")
 if {x.get("atom_id") for x in receipt.get("repairs",[])}!=ids or any(x.get("old_terminal_disposition")!="nonmaterial_context" or x.get("new_terminal_disposition")!="blocked_after_full_attempt" or x.get("unchanged_missing_or_unproved_lanes")!=["normative"] for x in receipt.get("repairs",[])):out.append("schema repair scope")
 rows={x.get("atom_id"):x for x in r.get("dispositions",[]) }
 if any(rows.get(atom_id,{}).get("terminal_disposition")!="blocked_after_full_attempt" or rows.get(atom_id,{}).get("missing_or_unproved_lanes")!=["normative"] for atom_id in ids):out.append("schema repair application")
 return out
def main():
 r=load(P);jsonschema.validate(r,load(ROOT/"schemas/claim_family_terminal_coverage.schema.json"));fail=preflight_errors()+repair_errors(r)+errors(r)
 for label,mut in [("drop",lambda x:x["dispositions"].pop()),("core",lambda x:x.__setitem__("chapter_core_promotion_count",1)),("fake promote",lambda x:x["dispositions"][0].update({"terminal_disposition":"promoted_at_bounded_scope","accepted_transition_ref":None})),("erase gap",lambda x:next(y for y in x["dispositions"] if y["terminal_disposition"]=="blocked_after_full_attempt").__setitem__("missing_or_unproved_lanes",[]))]:
  c=copy.deepcopy(r);mut(c)
  if not errors(c):fail.append("mutation accepted:"+label)
 if fail:raise SystemExit("Claim-family terminal coverage failed:\n - "+"\n - ".join(fail))
 print("Claim-family terminal coverage passed: 3,745/3,745 atoms across CF-01..CF-08, every block names missing lanes, promotions require accepted transitions, four mutations rejected, zero chapter-core movement.")
if __name__=="__main__":main()
