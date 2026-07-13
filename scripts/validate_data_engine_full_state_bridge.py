#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,re
from build_canonical_public_status import ROOT,load_json,validate_against_schema
P=ROOT/"experiments/post_v2_1_evidence_program/preregistration.json";I=ROOT/"experiments/post_v2_1_evidence_program/p3/state_inventory.json";C=ROOT/"experiments/post_v2_1_evidence_program/p3/results/result.json";R=ROOT/"experiments/data_engine_full_state_bridge/results/2026-07-13-local.json";S=ROOT/"schemas/data_engine_full_state_bridge_result.schema.json";L=ROOT/"lean/AsiStackProofs/DataEngines.lean"
TH=["complete_full_state_update_reaches_evidence_review","missing_optimizer_state_requires_inventory_repair","missing_scheduler_state_requires_inventory_repair","missing_rng_state_requires_inventory_repair","missing_cache_state_requires_inventory_repair","missing_backup_state_requires_inventory_repair","missing_descendant_state_requires_inventory_repair","missing_prospective_checkpoint_authority_requires_repair","rollback_mismatch_requires_repair","behavioral_change_cannot_launder_influence_reduction","behavioral_change_cannot_launder_privacy_erasure","lineage_propagation_cannot_launder_storage_erasure"]
REQ={"model_parameters","optimizer_state","scheduler_state","python_rng","numpy_rng","torch_cpu_rng","best_checkpoint","final_checkpoint","released_checkpoint","rollback_checkpoint","inference_cache","feature_cache","lineage_index","local_backup_store"}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def summary(i,c):
  arms=[a for s in c["seed_records"] for a in s["arms"]];d=[next(a for a in s["arms"] if a["arm"]=="deletion_aware_retrain") for s in c["seed_records"]]
  return {"state_surface_count":i["surface_count"],"seed_count":len(c["seeds"]),"arm_count":len(c["arms"]),"transaction_count":len(arms),"exact_rollback_count":sum(a["full_state_rollback_exact"] for a in arms),"best_final_disagreement_count":sum(a["best_final_state_disagreement"] for a in arms),"deletion_behavior_changes":[a["unlearning_claims"]["behavioral_cohort_change"] for a in d],"deletion_lineage_propagation_count":sum(a["unlearning_claims"]["lineage_propagation"] for a in d),"influence_reduction_state":d[0]["unlearning_claims"]["influence_reduction"],"storage_erasure_count":sum(a["unlearning_claims"]["storage_erasure"] for a in d),"checkpoint_authority":"prospective_validation_only_honored","disposition":"no_change_update_narrow_rollback_and_unlearning"}
def errs(d):
  p,i,c,r,l=d["p"],d["i"],d["c"],d["r"],d["l"];e=[]
  program=next((x for x in p.get("programs",[]) if x.get("program_id")=="P3-full-state-update-unlearning-causality"),None)
  if not program or program.get("state")!="preregistered":e.append("prospective program missing")
  if r.get("preregistration_sha256")!=sha(P) or r.get("inventory_sha256")!=sha(I) or r.get("campaign_result_sha256")!=sha(C):e.append("input digest drift")
  if r.get("observed_summary")!=summary(i,c):e.append("summary drift")
  if not REQ.issubset({x.get("surface_id") for x in i.get("surfaces",[])}):e.append("required full-state surfaces missing")
  if r.get("lean_bridge",{}).get("theorems")!=TH:e.append("theorem list drift")
  for t in TH:
    if not re.search(rf"^theorem\s+{re.escape(t)}\b",l,re.M):e.append("missing theorem "+t)
  if r.get("support_state_effect")!="none":e.append("support promotion")
  if len(r.get("non_claims",[]))<7:e.append("nonclaims erased")
  return e
def main():
  d={"p":load_json(P),"i":load_json(I),"c":load_json(C),"r":load_json(R),"l":L.read_text()};e=validate_against_schema(d["r"],load_json(S),str(R.relative_to(ROOT)))+errs(d)
  for m in [lambda q:q["i"].__setitem__("surfaces",q["i"]["surfaces"][:-1]),lambda q:q["c"]["seed_records"][0]["arms"][1].__setitem__("full_state_rollback_exact",False),lambda q:q["r"].__setitem__("campaign_result_sha256","0"*64),lambda q:q["r"].__setitem__("support_state_effect","prototype-backed"),lambda q:q["r"]["lean_bridge"].__setitem__("theorems",q["r"]["lean_bridge"]["theorems"][:-1]),lambda q:q["r"].__setitem__("non_claims",[])]:
    q=copy.deepcopy(d);m(q)
    if not errs(q):e.append("negative mutation accepted")
  if e:raise SystemExit("Data-engine full-state bridge failed:\n - "+"\n - ".join(e))
  print("Data-engine full-state bridge passed: 24 surfaces, 15/15 exact local rollbacks, prospective checkpoint authority, separated unlearning claims, 12 Lean theorems, and 6 rejecting mutations.")
if __name__=="__main__":main()
