#!/usr/bin/env python3
"""Freeze the mandatory three-atom P5 batch before its audit execution."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"experiments/p5_terminal_batch"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+"\n")
def main():
 if (BASE/"results/result.json").exists():raise SystemExit("terminal-batch outcome exists")
 design={"schema_version":"asi_stack.p5_terminal_batch_design.v1","state":"frozen_before_terminal_audit","recorded_date":"2026-07-16","atoms":[
 {"atom_id":"circle-calculus-and-proof-carrying-ai-contracts.mechanism.003","falsifier":"named target fails to compile or command, environment, result, proof boundary, and consumer-rejecting controls are absent","ceiling":"one pinned Circle rope target and finite consumer path only"},
 {"atom_id":"system-boundaries-and-authority.invariant.001","falsifier":"any finite reachable mutation widens declared principal, operation, target, ceiling, epoch, expiry, remaining-use, approval, or dispatch authority without an explicit grant","ceiling":"finite trusted-input authority model only"},
 {"atom_id":"capability-replacement-and-rollback.invariant.011","falsifier":"the evidence collapses artifact/digest, behavior, privacy, storage, descendant, service, or compensation outcomes into one rollback-success bit","ceiling":"bounded local replacement and unlearning records; service restart and external compensation unexecuted"}],"allowed_terminal_dispositions":["promoted_at_bounded_scope","retained_after_full_attempt","narrowed_after_full_attempt","refuted_after_full_attempt","deprecated_after_full_attempt","blocked_after_full_attempt"],"outcome_aware_retry_allowed":False,"chapter_core_promotion_allowed":False}
 dump(BASE/"design.json",design)
 prereg={"schema_version":"asi_stack.p5_terminal_batch_preregistration.v1","state":"frozen_before_terminal_audit","design_sha256":sha(BASE/"design.json"),"evaluator_sha256":sha(ROOT/"scripts/evaluate_p5_terminal_batch.py"),"schema_sha256":sha(ROOT/"schemas/p5_terminal_batch_result.schema.json"),"outcome_aware_retry_allowed":False,"publication_authority":"none","release_authority":"none"};dump(BASE/"preregistration.json",prereg);print("P5 mandatory terminal batch frozen: 3 atoms, no outcome-aware retry.")
if __name__=="__main__":main()
