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
 p=packet();return {k:p[k] for k in ["artifactDigest","consumerDigest","useDigest","policyDigest","rightsDigest","codecDigest","decoderDigest","evidenceDigest","resultDigest"]}|{"lastEventDigest":last}

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

def build(errors:list[str])->dict[str,Any]:
 rows=cases();text=LEAN.read_text();body=re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq",text,re.S).group("body");declared=set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)",body));reached={x["actual_route"] for x in rows};negative=[x for x in rows if not x["accepted"]]
 for x in rows:
  if x["actual_route"]!=x["expected_route"]:errors.append(f"{x['case_id']}: {x['actual_route']} != {x['expected_route']}")
 if (len(declared),len(reached),len(rows),len(negative))!=(53,53,53,44):errors.append(f"route coverage drifted: {len(declared)}/{len(reached)}/{len(rows)}/{len(negative)}")
 return {"schema_version":"asi_stack.artifact_compression_refinement.result.v1","result_id":"2026-07-15-artifact-compression-refinement","recorded_date":"2026-07-15","command":COMMAND,"model":{"lean_module":rel(LEAN),"stage_count":8,"route_count":len(declared),"reached_route_count":len(reached),"route_case_count":len(rows),"rejected_mutation_count":len(negative),"fallback_route_reached":"routeToFallback" in reached,"exact_use_route_reached":"acceptConsumption" in reached,"support_assignment_count":0,"external_effect_count":0},"source_result_refinement":source_results(errors),"route_cases":rows,"lean_verification":run(["lake","env","lean","AsiStackProofs/ArtifactCompressionRefinement.lean"],ROOT/"lean"),"support_state_effect":"none","external_effect":"none","residuals":["Finite authored lifecycle only; no NeuralFold encode was run by this refinement.","The fresh replay used RAW0, made the artifact larger, and supplies one exact roundtrip plus one corrupt-byte rejection.","The three NEURAL0 records are historical metadata observations over one decoded artifact, not a fresh encode or independent reproduction.","Probe validity, decoder correctness, utility, rare-case preservation, security, rights, costs, fallback execution, and recovery remain unmeasured gates."],"non_claims":["no codec correctness, useful compression, downstream utility, deployed fallback, safety, transfer, SOTA, AGI, ASI, or support claim","no inference from archive ratio, digest agreement, route coverage, or green validators to semantic preservation","no support assignment or external effect"]}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument("--write-result",action="store_true");args=a.parse_args();errors=[];result=build(errors);jsonschema.validate(result,load(SCHEMA));serialized=json.dumps(result,indent=2)+"\n"
 if args.write_result:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f"{rel(RESULT)} stale; run {COMMAND} --write-result")
 if errors:print("Artifact compression refinement failed:\n - "+"\n - ".join(errors));sys.exit(1)
 print("Artifact compression refinement passed: 8 stages, 53 routes, 44/44 mutations rejected; exact fixture, RAW0 replay, NEURAL0 metadata, and two no-change decisions digest-bound; support/effect none.")
if __name__=="__main__":main()
