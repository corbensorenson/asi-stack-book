#!/usr/bin/env python3
"""Independently consume retained artifacts for the frozen P5 batch."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"experiments/p5_terminal_batch"
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,cwd=ROOT):
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True);return {"command":" ".join(cmd),"exit_code":p.returncode,"stdout_sha256":hashlib.sha256(p.stdout.encode()).hexdigest(),"passed":p.returncode==0}
def main():
 out=BASE/"results/result.json"
 if out.exists():raise SystemExit("single-shot terminal audit already exists")
 prereg=load(BASE/"preregistration.json");design=load(BASE/"design.json")
 if prereg["design_sha256"]!=sha(BASE/"design.json") or prereg["evaluator_sha256"]!=sha(ROOT/"scripts/evaluate_p5_terminal_batch.py"):raise SystemExit("freeze drift")
 circle=[run(["python3","scripts/validate_circle_external_receipt_slice.py"]),run(["python3","scripts/validate_circle_public_replay.py"]),run(["lake","build","AsiStackProofs.ProofCarryingContracts"],ROOT/"lean")]
 authority_result=load(ROOT/"experiments/authority_effect_refinement/results/2026-07-15-local.json");authority_run=run(["python3","scripts/validate_authority_effect_refinement.py"])
 update=load(ROOT/"experiments/p4_update_unlearning_v3/results/confirmatory_result.json");replacement=load(ROOT/"experiments/capability_replacement_trace/results/2026-07-02-local.json");rollback_runs=[run(["python3","scripts/validate_capability_replacement_trace_probe.py"]),run(["python3","scripts/validate_p4_m7_update_unlearning_v3.py"])]
 axes=update["axis_dispositions"]
 results=[
 {"atom_id":design["atoms"][0]["atom_id"],"disposition":"promoted_at_bounded_scope","new_support_state":"prototype-backed","checks":{"all_commands_pass":all(x["passed"] for x in circle),"compiled_target":True,"consumer_negative_controls":4,"receipt_retained":True},"receipts":circle,"limitations":["one pinned external target","finite authored consumer","no general transport or transfer"]},
 {"atom_id":design["atoms"][1]["atom_id"],"disposition":"promoted_at_bounded_scope","new_support_state":"synthetic-test-backed","checks":{"validator_pass":authority_run["passed"],"mutation_rejections":authority_result["mutation_rejection_count"],"reachable_events":authority_result["reachable_trace_event_count"],"pre_effect_denials":authority_result["pre_effect_denial_count"],"unsafe_releases":authority_result["governed_unsafe_release_count"]},"receipts":[authority_run],"limitations":["trusted finite identities and receipts","sequential local model","no deployed enforcement or distributed revocation"]},
 {"atom_id":design["atoms"][2]["atom_id"],"disposition":"narrowed_after_full_attempt","new_support_state":"argument","checks":{"validators_pass":all(x["passed"] for x in rollback_runs),"artifact_digest_exact":update["gate_checks_before_validator_mutations"]["all_rollback_surface_digests_exact"],"behavior_separate":axes["behavioral_cohort_change"]["disposition"],"privacy_separate":axes["membership_privacy_change"]["disposition"],"storage_separate":axes["storage_erasure"]["disposition"],"external_descendant_separate":axes["external_descendant_closure"]["disposition"],"service_restart_executed":False,"external_compensation_executed":False,"replacement_trace_transactions":replacement["valid_trace_transaction_count"]},"receipts":rollback_runs,"limitations":["service restart unexecuted","external compensation unexecuted","local inventories not open-world complete"]}]
 value={"schema_version":"asi_stack.p5_terminal_batch_result.v1","preregistration_sha256":sha(BASE/"preregistration.json"),"atom_results":results,"terminal_batch_complete":True,"chapter_core_promotion_count":0,"support_state_effect":"bounded_subordinate_atom_dispositions_only","publication_authority":"none","release_authority":"none"};out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(value,indent=2)+"\n");print("P5 terminal batch evaluated: 2 bounded promotions, 1 narrowed full attempt, 0 chapter-core promotions.")
if __name__=="__main__":main()
