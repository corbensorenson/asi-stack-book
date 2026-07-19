#!/usr/bin/env python3
import hashlib,json,subprocess
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"experiments/claim_family_terminal_coverage"
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,cwd=ROOT):
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True);return {"command":" ".join(cmd),"exit_code":p.returncode,"stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest(),"stderr_sha256":hashlib.sha256(p.stderr.encode()).hexdigest()}
def transitions():
 out={}
 for p in (ROOT/"evidence_transitions").rglob("*.json"):
  try:r=load(p)
  except Exception:continue
  if r.get("review_status")=="accepted":out[r.get("claim_id")]=r
 return out
def main():
 out=BASE/"results/result.json"
 if out.exists():raise SystemExit("single-shot family attempt already exists")
 pre=load(BASE/"preregistration.json")
 if pre["design_sha256"]!=sha(BASE/"design.json") or pre["input_sha256"]["scripts/evaluate_claim_family_terminal_program.py"]!=sha(ROOT/"scripts/evaluate_claim_family_terminal_program.py"):raise SystemExit("freeze drift")
 receipts=[run(["python3","scripts/run_validation_registry.py","--tier","pr"]),run(["python3","scripts/run_validation_registry.py","--tier","deep"]),run(["lake","build"],ROOT/"lean")]
 if any(x["exit_code"] for x in receipts):raise SystemExit("repository-wide attempt failed before adjudication")
 reg=load(ROOT/"evidence_quality/claim_atom_registry.json"); add=load(ROOT/"evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json"); status=load(ROOT/"roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"); trans=transitions(); fam={x["chapter_id"]:x["family_id"] for x in status["chapter_claim_program"]}; rows=[]
 for a in reg["atoms"]:
  aid=a["atom_id"]; t=trans.get(aid); required=[x["lane"] for x in a.get("required_lanes",[])]; attempted=set(["source-synthesis"] if a.get("review_state")=="semantically_reviewed" else [])
  if a.get("evidence_refs",{}).get("proof_targets"):attempted.add("formal")
  if a.get("evidence_refs",{}).get("test_specs"):attempted.add("executable")
  if a.get("reproduction",{}).get("command"):attempted.update(x for x in required if x in {"formal","executable","empirical","causal"})
  missing=sorted(set(required)-attempted)
  if t and t.get("transition_effect")=="upward":disp="promoted_at_bounded_scope"
  elif t and t.get("transition_effect")=="refuted":disp="refuted_after_full_attempt"
  elif t and t.get("transition_effect")=="no_change" and "narrow" in (t.get("transition_id","")+t.get("transition_reason","")).lower():disp="narrowed_after_full_attempt"
  elif a.get("terminal_disposition"):disp=a["terminal_disposition"]
  elif not missing:disp="retained_after_full_attempt"
  else:disp="blocked_after_full_attempt"
  rows.append({"atom_id":aid,"chapter_id":a["chapter_id"],"family_id":fam[a["chapter_id"]],"role":a["role"],"support_state":a["support_state"],"terminal_disposition":disp,"required_lanes":required,"attempted_local_lanes":sorted(attempted),"missing_or_unproved_lanes":missing,"accepted_transition_ref":t.get("transition_id") if t else None,"ceiling":"No support movement beyond an exact preaccepted transition; registry/Lean success is structural and finite only."})
 for a in add["atoms"]:
  t=trans.get(a["id"]);disp="promoted_at_bounded_scope" if t and t.get("transition_effect")=="upward" else "blocked_after_full_attempt"
  rows.append({"atom_id":a["id"],"chapter_id":add["chapter_id"],"family_id":"CF-06","role":a["type"],"support_state":a["support_state"],"terminal_disposition":disp,"required_lanes":["executable","empirical","causal","transfer"],"attempted_local_lanes":["source-synthesis","executable"],"missing_or_unproved_lanes":["empirical","causal","transfer"],"accepted_transition_ref":t.get("transition_id") if t else None,"ceiling":"No heterogeneous-kernel, transfer, architectural-RSI, or chapter-core claim."})
 sums=defaultdict(Counter)
 for r in rows:sums[r["family_id"]][r["terminal_disposition"]]+=1;sums[r["family_id"]]["atom_count"]+=1
 value={"schema_version":"asi_stack.claim_family_terminal_coverage.v1","preregistration_sha256":sha(BASE/"preregistration.json"),"attempt_receipts":receipts,"atom_count":len(rows),"family_summaries":{k:dict(v) for k,v in sorted(sums.items())},"dispositions":rows,"all_atoms_terminal":len(rows)==3745 and all(r["terminal_disposition"] for r in rows),"chapter_core_promotion_count":0,"support_state_effect":"preserve_only_preaccepted_transitions","publication_authority":"none","release_authority":"none","non_claims":["coverage does not prove atom truth","green validators do not establish empirical or causal claims","Lean build does not establish runtime refinement or transfer","blocked dispositions are retained evidence gaps, not failures erased as success"]};out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(value,indent=2)+"\n");print("Claim-family attempt complete:",len(rows),"terminal dispositions",dict(Counter(r["terminal_disposition"] for r in rows)))
if __name__=="__main__":main()
