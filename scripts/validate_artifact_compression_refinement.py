#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/"lean/AsiStackProofs/ArtifactCompressionRefinement.lean"
SCHEMA=ROOT/"schemas/artifact_compression_refinement.schema.json"
RESULT=ROOT/"experiments/artifact_compression_refinement/results/2026-07-15-local.json"
FIXTURE=ROOT/"tests/fixtures/protocol_records/compressed_artifact_record.valid.json"
FIXTURE_SCHEMA=ROOT/"schemas/compressed_artifact_record.schema.json"
PROBE=ROOT/"experiments/rankfold_public_safe_probe/results/2026-07-02-local.json"
IMPORT=ROOT/"experiments/rankfold_artifact_import/results/2026-07-02-local.json"
DECISION_PROBE=ROOT/"evidence_transitions/v1_x_measured/rankfold_public_safe_replay_probe_no_change.json"
DECISION_IMPORT=ROOT/"evidence_transitions/v1_x_measured/rankfold_artifact_import_no_change.json"
COMMAND="python3 scripts/validate_artifact_compression_refinement.py"
KINDS={"registered":"bindArtifact","encoded":"recordEncoding","verified":"verifyReconstruction","probed":"probeConsumer","fallbackReady":"prepareFallback","admitted":"admitUse","consumed":"recordConsumption","closed":"close"}
ACCEPTED={"acceptEncoding","acceptVerification","acceptProbe","routeToFallback","acceptFallbackPrep","acceptAdmission","acceptConsumption","acceptClosure","acceptClosed"}
STAGES=tuple(KINDS)
LIVE_STAGES=STAGES[:-1]
NEXT_STAGE=dict(zip(STAGES[:-1],STAGES[1:]))
IDENTITY_KEYS=("artifactDigest","consumerDigest","useDigest","policyDigest","rightsDigest","codecDigest","decoderDigest","evidenceDigest","resultDigest")
THEOREMS=(
 "accepted_step_is_accepted","accepted_step_applies_event","apply_event_preserves_full_identity",
 "accepted_step_preserves_full_identity","accepted_step_preserves_non_authority",
 "accepted_step_adds_exactly_one_receipt","accepted_step_advances_stage",
 "apply_event_fallback_count_monotone","accepted_step_fallback_count_monotone",
 "accepted_run_preserves_full_identity","accepted_run_preserves_support",
 "accepted_run_preserves_external_effect","accepted_run_accounts_exact_receipts",
 "accepted_run_fallback_count_monotone","accepted_run_has_accepted_trace","artifact_run_append",
 "closed_state_accepts_no_event","exact_lifecycle_reaches_closed_with_receipts",
 "failed_probe_lifecycle_reaches_closed_with_one_fallback",
 "complete_packet_has_no_support_or_effect_authority","failed_probe_with_fallback_routes_to_fallback",
 "failed_probe_without_fallback_requests_artifact","exact_replay_without_readiness_blocks_use",
 "raw_ratio_cannot_promote_admitted_artifact","missing_evidence_transition_blocks_consumption",
 "exact_use_lifecycle_routes_to_closed","failed_probe_lifecycle_has_executable_fallback_without_support")

def load(p:Path)->Any:return json.loads(p.read_text())
def rel(p:Path)->str:return str(p.relative_to(ROOT))
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd:list[str],cwd:Path=ROOT)->dict[str,Any]:
 p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {"command":" ".join(cmd),"exit_code":0,"output_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()}

def packet()->dict[str,Any]:
 p={"artifactDigest":5001,"consumerDigest":5002,"useDigest":5003,"policyDigest":5004,"rightsDigest":5005,"codecDigest":5006,"decoderDigest":5007,"evidenceDigest":5008,"resultDigest":5009,"eventDigest":101}
 for k in ["fullArtifact","manifest","useEnvelope","accessPattern","consumer","rights","codecIdentity","decoderIdentity","platform","byteAccounting","residual","artifactDigestRecord","decoderDeterminism","exactReplayReady","integrity","adversarialMutation","verificationReceipt","taskProbeRequired","taskProbePassed","fallbackArtifact","utilityEvidence","rareCaseCoverage","securityAndRights","fallbackTrigger","fallbackExecuted","recoveryReceipt","costAccounting","qualifiedUse","evidenceTransition","nonClaims","consumerAck","observedOutcome","fallbackOutcome","residualClosure","descendants","resultDigestBound","cleanup"]:p[k]=True
 for k in ["exactReplayRequired","rawRatioPromotion","supportPromotionRequested","externalEffectRequested"]:p[k]=False
 return p

def state(stage:str,last:int=0)->dict[str,Any]:
 p=packet();return {k:p[k] for k in IDENTITY_KEYS}|{"stage":stage,"lastEventDigest":last,"receiptCount":0,"fallbackCount":0,"supportAssigned":False,"externalEffectCommitted":False}

def route(stage:str,kind:str,p:dict[str,Any],s:dict[str,Any])->str:
 if kind!=KINDS[stage]:return "rejectWrongStage"
 if any(p[k]!=s[k] for k in ["artifactDigest","consumerDigest","useDigest"]):return "rejectIdentitySubstitution"
 if any(p[k]!=s[k] for k in ["policyDigest","rightsDigest"]):return "rejectPolicySubstitution"
 if any(p[k]!=s[k] for k in ["codecDigest","decoderDigest"]):return "rejectDecoderSubstitution"
 if any(p[k]!=s[k] for k in ["evidenceDigest","resultDigest"]):return "rejectEvidenceSubstitution"
 if p["eventDigest"]==s["lastEventDigest"]:return "rejectEventReplay"
 if p["supportPromotionRequested"] or p["externalEffectRequested"]:return "rejectAuthorityLeak"
 simple={
 "registered":[("fullArtifact","requestFullArtifact"),("manifest","requestManifest"),("useEnvelope","requestUseEnvelope"),("accessPattern","requestAccessPattern"),("consumer","requestConsumer"),("rights","requestRights")],
 "encoded":[("codecIdentity","requestCodecIdentity"),("decoderIdentity","requestDecoderIdentity"),("platform","requestPlatform"),("byteAccounting","requestByteAccounting"),("residual","requestResidual"),("artifactDigestRecord","requestArtifactDigest")],
 "verified":[("decoderDeterminism","requestDecoderDeterminism"),("integrity","requestIntegrity"),("adversarialMutation","requestAdversarialMutation"),("verificationReceipt","requestVerificationReceipt")],
 "fallbackReady":[("fallbackTrigger","requestFallbackTrigger"),("fallbackExecuted","requestFallbackExecution"),("recoveryReceipt","requestRecoveryReceipt"),("costAccounting","requestCostAccounting")],
 "consumed":[("consumerAck","requestConsumerAck"),("observedOutcome","requestObservedOutcome"),("fallbackOutcome","requestFallbackOutcome"),("residualClosure","requestResidualClosure")],
 "closed":[("descendants","requestDescendants"),("resultDigestBound","requestResultDigest"),("cleanup","requestCleanup")]}
 accepts={"registered":"acceptEncoding","encoded":"acceptVerification","verified":"acceptProbe","fallbackReady":"acceptAdmission","consumed":"acceptClosure","closed":"acceptClosed"}
 if stage in simple:
  if stage=="verified" and p["exactReplayRequired"] and not p["exactReplayReady"]:return "blockExactReplay"
  for field,out in simple[stage]:
   if not p[field]:return out
  return accepts[stage]
 if stage=="probed":
  if not p["taskProbeRequired"]:return "requestTaskProbe"
  if not p["taskProbePassed"]:return "routeToFallback" if p["fallbackArtifact"] else "requestFallbackArtifact"
  for field,out in [("utilityEvidence","requestUtilityEvidence"),("rareCaseCoverage","requestRareCaseCoverage"),("securityAndRights","requestSecurityAndRights")]:
   if not p[field]:return out
  return "acceptFallbackPrep"
 if stage=="admitted":
  if not p["qualifiedUse"]:return "blockUnqualifiedUse"
  if p["rawRatioPromotion"]:return "blockRawRatioPromotion"
  if not p["evidenceTransition"]:return "requestEvidenceTransition"
  if not p["nonClaims"]:return "requestNonClaims"
  return "acceptConsumption"
 raise AssertionError(stage)

def step(s:dict[str,Any],kind:str,p:dict[str,Any])->dict[str,Any]|None:
 if s["stage"]=="closed":return None
 selected=route(s["stage"],kind,p,s)
 if selected not in ACCEPTED:return None
 out=dict(s);out["stage"]=NEXT_STAGE[s["stage"]];out["lastEventDigest"]=p["eventDigest"];out["receiptCount"]+=1
 if selected=="routeToFallback":out["fallbackCount"]+=1
 return out

def lifecycle_events(fallback:bool=False)->list[tuple[str,dict[str,Any]]]:
 rows=[]
 for index,stage_name in enumerate(LIVE_STAGES,start=1):
  p=packet();p["eventDigest"]=100+index
  if fallback and stage_name=="probed":p["taskProbePassed"]=False
  rows.append((KINDS[stage_name],p))
 return rows

def run_states(initial:dict[str,Any],events:list[tuple[str,dict[str,Any]]])->list[dict[str,Any]]|None:
 states=[dict(initial)];current=dict(initial)
 for kind,p in events:
  nxt=step(current,kind,p)
  if nxt is None:return None
  states.append(nxt);current=nxt
 return states

def cases()->list[dict[str,Any]]:
 rows=[]
 def add(cid,stage,expected,mutation=None,kind=None,last=0):
  p=packet();p.update(mutation or {});actual=route(stage,kind or KINDS[stage],p,state(stage,last));rows.append({"case_id":cid,"stage":stage,"expected_route":expected,"actual_route":actual,"accepted":actual in ACCEPTED})
 add("wrong-stage","registered","rejectWrongStage",kind="recordEncoding")
 for cid,key,out in [("identity-substitution","artifactDigest","rejectIdentitySubstitution"),("policy-substitution","policyDigest","rejectPolicySubstitution"),("decoder-substitution","decoderDigest","rejectDecoderSubstitution"),("evidence-substitution","evidenceDigest","rejectEvidenceSubstitution")]:add(cid,"registered",out,{key:999})
 add("event-replay","registered","rejectEventReplay",last=101);add("authority-leak","registered","rejectAuthorityLeak",{"supportPromotionRequested":True})
 simple={"registered":[("fullArtifact","requestFullArtifact"),("manifest","requestManifest"),("useEnvelope","requestUseEnvelope"),("accessPattern","requestAccessPattern"),("consumer","requestConsumer"),("rights","requestRights")],"encoded":[("codecIdentity","requestCodecIdentity"),("decoderIdentity","requestDecoderIdentity"),("platform","requestPlatform"),("byteAccounting","requestByteAccounting"),("residual","requestResidual"),("artifactDigestRecord","requestArtifactDigest")],"verified":[("decoderDeterminism","requestDecoderDeterminism"),("integrity","requestIntegrity"),("adversarialMutation","requestAdversarialMutation"),("verificationReceipt","requestVerificationReceipt")],"fallbackReady":[("fallbackTrigger","requestFallbackTrigger"),("fallbackExecuted","requestFallbackExecution"),("recoveryReceipt","requestRecoveryReceipt"),("costAccounting","requestCostAccounting")],"consumed":[("consumerAck","requestConsumerAck"),("observedOutcome","requestObservedOutcome"),("fallbackOutcome","requestFallbackOutcome"),("residualClosure","requestResidualClosure")],"closed":[("descendants","requestDescendants"),("resultDigestBound","requestResultDigest"),("cleanup","requestCleanup")]}
 accepts={"registered":"acceptEncoding","encoded":"acceptVerification","verified":"acceptProbe","fallbackReady":"acceptAdmission","consumed":"acceptClosure","closed":"acceptClosed"}
 for stage,pairs in simple.items():
  for field,out in pairs:add(f"{stage}-{field}",stage,out,{field:False})
  if stage=="verified":add("verified-exact-replay",stage,"blockExactReplay",{"exactReplayRequired":True,"exactReplayReady":False})
  add(f"{stage}-accepted",stage,accepts[stage])
 add("probed-missing-probe","probed","requestTaskProbe",{"taskProbeRequired":False});add("probed-fallback","probed","routeToFallback",{"taskProbePassed":False});add("probed-no-fallback","probed","requestFallbackArtifact",{"taskProbePassed":False,"fallbackArtifact":False})
 for field,out in [("utilityEvidence","requestUtilityEvidence"),("rareCaseCoverage","requestRareCaseCoverage"),("securityAndRights","requestSecurityAndRights")]:add(f"probed-{field}","probed",out,{field:False})
 add("probed-accepted","probed","acceptFallbackPrep")
 add("admitted-unqualified","admitted","blockUnqualifiedUse",{"qualifiedUse":False});add("admitted-ratio","admitted","blockRawRatioPromotion",{"rawRatioPromotion":True});add("admitted-transition","admitted","requestEvidenceTransition",{"evidenceTransition":False});add("admitted-nonclaims","admitted","requestNonClaims",{"nonClaims":False});add("admitted-accepted","admitted","acceptConsumption")
 return rows

def source_results(errors:list[str])->dict[str,Any]:
 f=load(FIXTURE);jsonschema.validate(f,load(FIXTURE_SCHEMA));p=load(PROBE);i=load(IMPORT);dp=load(DECISION_PROBE);di=load(DECISION_IMPORT)
 counts={"fixture_field_count":len(f),"fixture_non_claim_count":len(f["non_claims"]),"probe_input_bytes":p["input"]["bytes"],"probe_archive_bytes":p["roundtrip"]["archive_file_bytes"],"probe_command_count":len(p["commands"]),"probe_corrupt_rejection_count":int(p["negative_control"]["rejected"]),"probe_roundtrip_exact_count":int(p["roundtrip"]["roundtrip_exact"]),"probe_compression_advantage_count":int(p["roundtrip"]["compression_advantage_observed"]),"import_observation_count":len(i["observations"]),"import_decoded_bytes":i["reference_decoded_artifact"]["decoded_file_bytes"],"import_best_ratio":i["summary"]["best_observed_decoded_to_archive_ratio"],"no_change_decision_count":sum(x["transition_effect"]=="no_change" for x in [dp,di])}
 expected={"fixture_field_count":22,"fixture_non_claim_count":3,"probe_input_bytes":3936,"probe_archive_bytes":4434,"probe_command_count":5,"probe_corrupt_rejection_count":1,"probe_roundtrip_exact_count":1,"probe_compression_advantage_count":0,"import_observation_count":3,"import_decoded_bytes":100000000,"import_best_ratio":2.76634019,"no_change_decision_count":2}
 if counts!=expected:errors.append(f"source counts drifted: {counts}")
 paths=[FIXTURE,PROBE,IMPORT,DECISION_PROBE,DECISION_IMPORT]
 return {"counts":counts,"sha256":{rel(x):sha(x) for x in paths},"validator_runs":[run(["python3","scripts/validate_protocol_examples.py"]),run(["python3","scripts/validate_rankfold_public_safe_probe.py"]),run(["python3","scripts/validate_rankfold_artifact_import.py"])]}

def lifecycle_checks(errors:list[str])->dict[str,Any]:
 initial=state("registered")
 exact_events=lifecycle_events(False);fallback_events=lifecycle_events(True)
 exact_states=run_states(initial,exact_events);fallback_states=run_states(initial,fallback_events)
 if exact_states is None or fallback_states is None:errors.append("canonical lifecycle failed");return {}
 exact_final=exact_states[-1];fallback_final=fallback_states[-1]
 expected_base={"stage":"closed","receiptCount":7,"supportAssigned":False,"externalEffectCommitted":False}
 for key,value in expected_base.items():
  if exact_final.get(key)!=value or fallback_final.get(key)!=value:errors.append(f"terminal witness drifted: {key}")
 if exact_final["fallbackCount"]!=0 or fallback_final["fallbackCount"]!=1:errors.append("fallback witness count drifted")
 split_checks=0
 for split in range(len(fallback_events)+1):
  prefix=run_states(initial,fallback_events[:split])
  if prefix is None:errors.append(f"trace prefix {split} failed");continue
  suffix=run_states(prefix[-1],fallback_events[split:])
  if suffix is None or suffix[-1]!=fallback_final:errors.append(f"trace composition split {split} failed")
  split_checks+=1
 identity_checks=sum(all(s[k]==initial[k] for k in IDENTITY_KEYS) for s in fallback_states)
 nonauthority_checks=sum(not s["supportAssigned"] and not s["externalEffectCommitted"] for s in fallback_states)
 fallback_monotonicity_checks=sum(a["fallbackCount"]<=b["fallbackCount"] for a,b in zip(fallback_states,fallback_states[1:]))
 terminal_rejections=sum(step(fallback_final,kind,{**packet(),"eventDigest":900+i}) is None for i,kind in enumerate(KINDS.values()))
 return {"exact_states":exact_states,"fallback_states":fallback_states,"trace_event_count":len(fallback_events),"trace_composition_split_count":split_checks,"identity_preservation_check_count":identity_checks,"non_authority_preservation_check_count":nonauthority_checks,"fallback_monotonicity_check_count":fallback_monotonicity_checks,"terminal_rejection_count":terminal_rejections,"exact_final":exact_final,"fallback_final":fallback_final}

def mutation_checks()->list[dict[str,Any]]:
 receipts=[]
 for row in cases():
  if not row["accepted"]:receipts.append({"mutation_id":f"route:{row['case_id']}","rejected":True})
 for stage_index,stage_name in enumerate(LIVE_STAGES):
  for key in IDENTITY_KEYS:
   p=packet();p["eventDigest"]=200+stage_index;p[key]=999999
   receipts.append({"mutation_id":f"identity:{stage_name}:{key}","rejected":step(state(stage_name),KINDS[stage_name],p) is None})
  wrong_kind=KINDS[LIVE_STAGES[(stage_index+1)%len(LIVE_STAGES)]]
  p=packet();p["eventDigest"]=300+stage_index
  receipts.append({"mutation_id":f"wrong-kind:{stage_name}","rejected":step(state(stage_name),wrong_kind,p) is None})
  p=packet();p["eventDigest"]=400+stage_index
  receipts.append({"mutation_id":f"replay:{stage_name}","rejected":step(state(stage_name,last=p["eventDigest"]),KINDS[stage_name],p) is None})
  p=packet();p["eventDigest"]=500+stage_index;p["supportPromotionRequested"]=True
  receipts.append({"mutation_id":f"support:{stage_name}","rejected":step(state(stage_name),KINDS[stage_name],p) is None})
  p=packet();p["eventDigest"]=600+stage_index;p["externalEffectRequested"]=True
  receipts.append({"mutation_id":f"effect:{stage_name}","rejected":step(state(stage_name),KINDS[stage_name],p) is None})
 closed=state("closed")
 for index,kind in enumerate(KINDS.values()):
  p=packet();p["eventDigest"]=700+index
  receipts.append({"mutation_id":f"terminal:{kind}","rejected":step(closed,kind,p) is None})
 return receipts

def build(errors:list[str])->dict[str,Any]:
 rows=cases();text=LEAN.read_text();body=re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq",text,re.S).group("body");declared=set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)",body));reached={x["actual_route"] for x in rows};negative=[x for x in rows if not x["accepted"]]
 theorem_surface=tuple(re.findall(r"^theorem\s+([A-Za-z0-9_]+)",text,re.M));checks=lifecycle_checks(errors);mutations=mutation_checks()
 for x in rows:
  if x["actual_route"]!=x["expected_route"]:errors.append(f"{x['case_id']}: {x['actual_route']} != {x['expected_route']}")
 if (len(declared),len(reached),len(rows),len(negative))!=(53,53,53,44):errors.append(f"route coverage drifted: {len(declared)}/{len(reached)}/{len(rows)}/{len(negative)}")
 if theorem_surface!=THEOREMS:errors.append(f"theorem surface drifted: {theorem_surface}")
 if re.search(r"\b(sorry|axiom)\b",text):errors.append("Lean placeholder detected")
 if len(mutations)!=143 or not all(x["rejected"] for x in mutations):errors.append(f"mutation coverage drifted: {sum(x['rejected'] for x in mutations)}/{len(mutations)}")
 expected_checks={"trace_event_count":7,"trace_composition_split_count":8,"identity_preservation_check_count":8,"non_authority_preservation_check_count":8,"fallback_monotonicity_check_count":7,"terminal_rejection_count":8}
 for key,value in expected_checks.items():
  if checks.get(key)!=value:errors.append(f"lifecycle check drifted: {key}")
 model={"lean_module":rel(LEAN),"stage_count":8,"lean_theorem_count":len(theorem_surface),"lean_theorem_surface":list(theorem_surface),"route_count":len(declared),"reached_route_count":len(reached),"route_case_count":len(rows),**expected_checks,"identity_field_count":len(IDENTITY_KEYS),"mutation_count":len(mutations),"rejected_mutation_count":sum(x["rejected"] for x in mutations),"fallback_route_reached":"routeToFallback" in reached,"exact_use_route_reached":"acceptConsumption" in reached,"support_assignment_count":0,"external_effect_count":0}
 witnesses={"exact_use":{"terminal_stage":checks.get("exact_final",{}).get("stage"),"receipt_count":checks.get("exact_final",{}).get("receiptCount"),"fallback_count":checks.get("exact_final",{}).get("fallbackCount"),"support_assigned":checks.get("exact_final",{}).get("supportAssigned"),"external_effect_committed":checks.get("exact_final",{}).get("externalEffectCommitted")},"failed_probe_fallback":{"terminal_stage":checks.get("fallback_final",{}).get("stage"),"receipt_count":checks.get("fallback_final",{}).get("receiptCount"),"fallback_count":checks.get("fallback_final",{}).get("fallbackCount"),"support_assigned":checks.get("fallback_final",{}).get("supportAssigned"),"external_effect_committed":checks.get("fallback_final",{}).get("externalEffectCommitted")}}
 return {"schema_version":"asi_stack.artifact_compression_refinement.result.v2","result_id":"2026-07-15-artifact-compression-refinement","recorded_date":"2026-07-15","command":COMMAND,"model":model,"source_result_refinement":source_results(errors),"route_cases":rows,"mutation_receipts":mutations,"witnesses":witnesses,"lean_verification":run(["lake","env","lean","AsiStackProofs/ArtifactCompressionRefinement.lean"],ROOT/"lean"),"support_state_effect":"none","external_effect":"none","residuals":["Finite authored lifecycle only; no NeuralFold encode was run by this refinement.","The fresh replay used RAW0, made the artifact larger, and supplies one exact roundtrip plus one corrupt-byte rejection.","The three NEURAL0 records are historical metadata observations over one decoded artifact, not a fresh encode or independent reproduction.","Probe validity, decoder correctness, utility, rare-case preservation, security, rights, costs, fallback execution, and recovery remain unmeasured gates."],"non_claims":["no codec correctness, useful compression, downstream utility, deployed fallback, safety, transfer, SOTA, AGI, ASI, or support claim","no inference from archive ratio, digest agreement, route coverage, or green validators to semantic preservation","no support assignment or external effect"]}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument("--write-result",action="store_true");args=a.parse_args();errors=[];result=build(errors);jsonschema.validate(result,load(SCHEMA));serialized=json.dumps(result,indent=2)+"\n"
 if args.write_result:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f"{rel(RESULT)} stale; run {COMMAND} --write-result")
 if errors:print("Artifact compression refinement failed:\n - "+"\n - ".join(errors));sys.exit(1)
 print("Artifact compression refinement passed: 27 Lean theorems, 8 stages, 8 trace splits, 53 routes, 143/143 mutations rejected; exact fixture, RAW0 replay, NEURAL0 metadata, and two no-change decisions digest-bound; support/effect none.")
if __name__=="__main__":main()
