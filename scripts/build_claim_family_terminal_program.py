#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"experiments/claim_family_terminal_coverage"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+"\n")
def main():
 if (BASE/"results/result.json").exists():raise SystemExit("coverage outcome exists")
 design={"schema_version":"asi_stack.claim_family_terminal_design.v1","state":"frozen_before_repository_wide_attempt","recorded_date":"2026-07-16","activation_atom_count":3730,"post_activation_addendum_atom_count":15,"total_atom_count":3745,"families":[f"CF-{i:02d}" for i in range(1,9)],"attempt":{"pr_registry":True,"deep_registry":True,"full_lean_build":True,"accepted_transition_replay":True,"semantic_review_consumption":True,"per_atom_lane_audit":True},"disposition_rule":"Preserve an exact accepted transition or prior terminal disposition. Otherwise retain_after_full_attempt only when every atom-required lane has an auditable local route; use blocked_after_full_attempt with exact missing lanes when it does not. Never infer support from validation, theorem, source, or coverage counts.","outcome_aware_retry_allowed":False,"chapter_core_promotion_allowed":False}
 dump(BASE/"design.json",design); files=["evidence_quality/claim_atom_registry.json","evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json","roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json","validation/registry.json","proofs/proof_manifest.json","scripts/evaluate_claim_family_terminal_program.py","schemas/claim_family_terminal_coverage.schema.json"]
 prereg={"schema_version":"asi_stack.claim_family_terminal_preregistration.v1","state":design["state"],"design_sha256":sha(BASE/"design.json"),"input_sha256":{x:sha(ROOT/x) for x in files},"outcome_aware_retry_allowed":False,"publication_authority":"none","release_authority":"none"};dump(BASE/"preregistration.json",prereg);print("Claim-family terminal program frozen: 3,745 atoms across CF-01..CF-08.")
if __name__=="__main__":main()
