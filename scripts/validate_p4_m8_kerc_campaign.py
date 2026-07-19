#!/usr/bin/env python3
"""Validate Campaign 6 results, failures, bounded transitions, and laundering controls."""
from __future__ import annotations
import copy
import jsonschema
from p4_m8_kerc_common import BASE, ROOT, load, sha

RESULT=BASE/"results/confirmatory_result.json"; RAW=BASE/"raw/campaign_run.json"; SCHEMA=ROOT/"schemas/p4_m8_kerc_result.schema.json"
TRANSITIONS=[ROOT/"evidence_transitions/post_v2_3/kerc_protected_exact_handle_synthetic_test_backed.json",ROOT/"evidence_transitions/post_v2_3/kerc_shared_glossary_break_even_synthetic_test_backed.json",ROOT/"evidence_transitions/post_v2_3/kerc_broad_efficiency_refuted.json"]

def errors(result,raw,transitions):
 out=[]
 if result.get("preregistration_sha256")!=sha(BASE/"preregistration.json") or result.get("corpus_sha256")!=sha(BASE/"corpus.json") or result.get("raw_run_sha256")!=sha(RAW): out.append("lineage")
 if raw.get("preregistration_sha256")!=result.get("preregistration_sha256") or len(raw.get("records",[]))!=64: out.append("raw denominator")
 if result.get("denominators")!={"corpus":192,"train":128,"heldout":64,"seeds":5,"ablations":13,"attacks":20}: out.append("denominators")
 a,b,c=result.get("slice_results",{}).get("A",{}),result.get("slice_results",{}).get("B",{}),result.get("slice_results",{}).get("C",{})
 if a.get("mean_protected_object_recall")!=1.0 or b.get("semantic_intent_accuracy")!=1.0 or b.get("polarity_accuracy")!=1.0 or b.get("lossless_byte_exact_rate")!=1.0: out.append("slice A/B")
 if c.get("kernel_native_mean_accuracy")!=0.5 or c.get("best_surface_mean_accuracy")!=0.5 or c.get("simple_handle_mean_accuracy")!=0.5: out.append("native core")
 rate=result.get("rate_cost_results",{}).get("representations",{})
 if rate.get("packet",{}).get("mean_bytes")!=714.0 or result.get("rate_cost_results",{}).get("best_simple_total_description_bytes")!=73.25: out.append("whole-rate failure")
 if result.get("observed_break_even_turn")!=2 or result.get("attacks",{}).get("correct")!=19 or result.get("attacks",{}).get("false_allow")!=1: out.append("break-even/attacks")
 gate=result.get("gate_adjudication",{})
 if gate!={"broad_efficiency_gate_passed":False,"terminal_disposition":"broad_efficiency_refuted_narrow_exact_handle_and_shared_glossary_results_retained","new_chapter_gate_passed":False,"chapter_core_promotion_count":0}: out.append("adjudication")
 dispositions={x.get("claim_id"):x.get("disposition") for x in result.get("claim_dispositions",[])}
 if dispositions!={"kerc.broad_matched_total_system_efficiency":"refuted_after_full_attempt","kerc.protected_exact_handle_preservation":"promoted_at_bounded_scope","kerc.interaction_shared_glossary_break_even":"promoted_at_bounded_scope","kerc.security_or_multilingual_transfer":"blocked_after_full_attempt"}: out.append("claim dispositions")
 if result.get("support_state_effect")!="none_pending_reconciliation" or result.get("publication_authority")!="none" or result.get("release_authority")!="none": out.append("authority")
 expected={"kerc.protected_exact_handle_preservation":("upward","synthetic-test-backed"),"kerc.interaction_shared_glossary_break_even":("upward","synthetic-test-backed"),"kerc.broad_matched_total_system_efficiency":("refuted","refuted")}
 got={x.get("claim_id"):(x.get("transition_effect"),x.get("new_support_state")) for x in transitions}
 expected_support={"kerc.protected_exact_handle_preservation":"eligible_for_bounded_evidence_review","kerc.interaction_shared_glossary_break_even":"eligible_for_bounded_evidence_review","kerc.broad_matched_total_system_efficiency":"blocks_promotion"}
 if got!=expected or any(x.get("review_status")!="accepted" or x.get("transition_validity_state")!="review_accepted" or x.get("claim_id","").endswith(".core") or x.get("support_state_effect")!=expected_support.get(x.get("claim_id")) for x in transitions): out.append("transitions")
 return out

def main():
 result,raw=load(RESULT),load(RAW); transitions=[load(x) for x in TRANSITIONS]; jsonschema.validate(result,load(SCHEMA)); failures=errors(result,raw,transitions)
 mutations=[("inflate",lambda r:r["denominators"].__setitem__("heldout",65)),("launder broad",lambda r:r["gate_adjudication"].__setitem__("broad_efficiency_gate_passed",True)),("erase attack",lambda r:r["attacks"].__setitem__("false_allow",0)),("improve core",lambda r:r["slice_results"]["C"].__setitem__("kernel_native_mean_accuracy",1.0)),("shrink packet",lambda r:r["rate_cost_results"]["representations"]["packet"].__setitem__("mean_bytes",70.0)),("chapter",lambda r:r["gate_adjudication"].__setitem__("new_chapter_gate_passed",True)),("support",lambda r:r.__setitem__("support_state_effect","general"))]
 for label,mutate in mutations:
  candidate=copy.deepcopy(result); mutate(candidate)
  if not errors(candidate,raw,transitions): failures.append(f"mutation accepted:{label}")
 for label,index,mutate in [("core transition",0,lambda x:x.__setitem__("claim_id","compact-generative-systems-and-residual-honesty.core")),("support-effect laundering",1,lambda x:x.__setitem__("support_state_effect","blocks_promotion")),("unrefute",2,lambda x:x.__setitem__("new_support_state","synthetic-test-backed"))]:
  tt=copy.deepcopy(transitions); mutate(tt[index])
  if not errors(result,raw,tt): failures.append(f"mutation accepted:{label}")
 if failures: raise SystemExit("KERC campaign validation failed:\n - "+"\n - ".join(failures))
 print("P4/M8 Campaign 6 validation passed: 192 records, 64 heldout, five seeds, eight baseline families, thirteen ablations, 19/20 attacks, broad efficiency refuted, two narrow finite transitions, zero chapter-core movement, ten mutations rejected.")
if __name__=="__main__": main()
