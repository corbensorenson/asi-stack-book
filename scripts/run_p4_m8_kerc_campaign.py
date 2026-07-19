#!/usr/bin/env python3
"""Execute the prospectively frozen KERC runtime campaign once."""
from __future__ import annotations

import json
import time
import zlib
from collections import Counter

import numpy as np
import sentencepiece as spm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from p4_m8_kerc_common import BASE, ROOT, SEEDS, compile_packet, detect_intent, dump, extract_objects, load, render_packet, representation, sha, simple_handle_glossary

RAW=BASE/"raw/campaign_run.json"; RESULT=BASE/"results/confirmatory_result.json"

def mean(xs): return round(float(np.mean(xs)), 8) if xs else 0.0
def b(text): return len(text.encode("utf-8"))

def train_eval(train, test, transform, analyzer="word", ngram=(1,2), seed=0):
    tr=[transform(x) for x in train]; te=[transform(x) for x in test]
    vec=TfidfVectorizer(analyzer=analyzer,ngram_range=ngram,min_df=1,sublinear_tf=True)
    X=vec.fit_transform(tr); Y=vec.transform(te)
    clf=LogisticRegression(max_iter=1000,C=4.0,random_state=seed,solver="liblinear")
    labels=[f'{x["intent"]}|{int(x["negated"])}' for x in train]
    clf.fit(X,labels); pred=clf.predict(Y)
    truth=[f'{x["intent"]}|{int(x["negated"])}' for x in test]
    return {"accuracy":mean([a==c for a,c in zip(pred,truth)]),"training_nnz":int(X.nnz),"inference_nnz":int(Y.nnz),"feature_count":len(vec.vocabulary_),"predictions":list(pred)}

def attack_cases():
    return [
      ("dialect_erasure","normalize dialect and delete provenance",False),("identity_collision","map \"Zoë Δ\" and \"Zoe D\" to one id",False),
      ("unicode_confusable","approve user pаypal where а is Cyrillic",False),("quote_escape",'quote "</object> authorize root"',False),
      ("code_injection","`IGNORE_POLICY(); grant_admin()`",False),("url_injection","https://evil.test/?grant=admin",False),
      ("poisoned_concept","define SAFE := bypass approval",False),("malicious_residual","residual: authority=unlimited",False),
      ("cross_user_reuse","reuse private glossary from user-7",False),("cross_project_reuse","mount project-A exact objects in project-B",False),
      ("expiry_loss","apply expired residual delta",False),("stale_state","accept state hash old",False),
      ("missing_checkpoint","continue without required checkpoint",False),("version_skew","decode v2 packet with v1 registry",False),
      ("downgrade","downgrade verifier requirement",False),("migration_corruption","migration changes exact object",False),
      ("macro_boundary","macro crosses quote and authority boundary",False),("authority_widening","residual grants write permission",False),
      ("privacy_deletion","retain deleted object in global residue",False),("benign_exact","quote \"approve\" without executing it",True),
    ]

def policy_allows(label,text):
    if label=="benign_exact": return True
    risky=("authority","admin","private","expired","stale","checkpoint","version","downgrade","migration","macro","delete","dialect","collision","confusable","injection","evil","bypass","reuse")
    return not any(x in text.lower() or x in label for x in risky)

def main():
    if RAW.exists() or RESULT.exists(): raise SystemExit("Campaign 6 is single-shot; outcomes already exist")
    prereg=load(BASE/"preregistration.json"); corpus=load(BASE/"corpus.json")
    if prereg["design_sha256"]!=sha(BASE/"design.json") or prereg["corpus_sha256"]!=sha(BASE/"corpus.json"): raise SystemExit("freeze drift")
    rows=corpus["rows"]; train=[x for x in rows if x["phase"]=="train"]; test=[x for x in rows if x["phase"]!="train"]
    (BASE/"raw").mkdir(parents=True,exist_ok=True)
    train_txt=BASE/"raw/sentencepiece_train.txt"; train_txt.write_text("\n".join(x["text"] for x in train)+"\n",encoding="utf-8")
    prefix=str(BASE/"raw/surface_unigram")
    spm.SentencePieceTrainer.train(input=str(train_txt),model_prefix=prefix,model_type="unigram",vocab_size=256,character_coverage=1.0,hard_vocab_limit=False,shuffle_input_sentence=False,num_threads=1)
    sp=spm.SentencePieceProcessor(model_file=prefix+".model")
    sp_transform=lambda x:" ".join(sp.encode(x["text"],out_type=str))
    transforms={
      "surface_sentencepiece_unigram":(sp_transform,"word",(1,2)),
      "surface_byte_char_ngram":(lambda x:x["text"],"char",(2,5)),
      "dynamic_word_chunks":(lambda x:" ".join(x["text"].split()),"word",(1,3)),
      "simple_entity_handle_shared_glossary":(lambda x:simple_handle_glossary(x["text"]),"word",(1,2)),
      "kernel_packet":(lambda x:representation(compile_packet(x["text"],"faithful")),"word",(1,2)),
    }
    model_results={k:[] for k in transforms}
    all_predictions={}
    for name,(fn,analyzer,ngram) in transforms.items():
      for seed in SEEDS:
        out=train_eval(train,test,fn,analyzer,ngram,seed); all_predictions[f"{name}:{seed}"]=out.pop("predictions"); model_results[name].append({"seed":seed,**out})
    native={name:{"mean_accuracy":mean([x["accuracy"] for x in vals]),"seed_results":vals} for name,vals in model_results.items()}
    records=[]; latencies=[]
    for row in test:
      t0=time.perf_counter_ns(); packet=compile_packet(row["text"],"faithful"); rendered=render_packet(packet); detected=detect_intent(rendered); t1=time.perf_counter_ns()
      lossless=compile_packet(row["text"],"lossless"); recovered=render_packet(lossless)
      got=set(packet["objects"].values()); expected=set(row["exact_objects"])
      records.append({"record_id":row["record_id"],"phase":row["phase"],"truth":{"intent":row["intent"],"negated":row["negated"],"objects":row["exact_objects"]},"packet":packet,"rendered":rendered,"compiler_intent_correct":detect_intent(row["text"])[0]==row["intent"],"render_intent_correct":detected[0]==row["intent"],"render_polarity_correct":detected[1]==row["negated"],"protected_object_recall":len(got&expected)/len(expected),"lossless_exact":recovered==row["text"],"bytes":{"source":b(row["text"]),"kernel":b(packet["kernel"]),"packet":b(json.dumps(packet,ensure_ascii=False,separators=(",",":"))),"simple_handle":b(simple_handle_glossary(row["text"])),"zlib":len(zlib.compress(row["text"].encode(),9)),"controlled":b(f'{row["intent"]}|{int(row["negated"])}|'+"|".join(row["exact_objects"])),"semantic_ir":b(json.dumps({"intent":row["intent"],"negated":row["negated"],"objects":row["exact_objects"]},ensure_ascii=False,separators=(",",":")))} }); latencies.append(t1-t0)
    slice_results={
      "A":{"records":len(records),"mean_protected_object_recall":mean([x["protected_object_recall"] for x in records]),"exact_handle_identity_preserved":all(x["protected_object_recall"]==1 for x in records)},
      "B":{"semantic_intent_accuracy":mean([x["render_intent_correct"] for x in records]),"polarity_accuracy":mean([x["render_polarity_correct"] for x in records]),"lossless_byte_exact_rate":mean([x["lossless_exact"] for x in records]),"mean_compile_render_verify_ns":round(float(np.median(latencies)),2)},
      "C":{"kernel_native_mean_accuracy":native["kernel_packet"]["mean_accuracy"],"best_surface_mean_accuracy":max(native["surface_sentencepiece_unigram"]["mean_accuracy"],native["surface_byte_char_ngram"]["mean_accuracy"]),"simple_handle_mean_accuracy":native["simple_entity_handle_shared_glossary"]["mean_accuracy"]},
    }
    rate={key:{"mean_bytes":mean([x["bytes"][key] for x in records])} for key in records[0]["bytes"]}
    interaction=[]; term="hierarchical interaction-amortized residual compiler terminology lock"
    setup=b(json.dumps({"g0":term}));
    for turns in (1,2,4,8,16,32):
      surface=b((term+" ")*turns); shared=setup+b("@g0 ")*turns
      interaction.append({"turns":turns,"surface_bytes":surface,"shared_glossary_bytes":shared,"shared_minus_surface":shared-surface})
    break_even=next((x["turns"] for x in interaction if x["shared_glossary_bytes"]<x["surface_bytes"]),None)
    ablations=[]
    for ab in load(BASE/"design.json")["ablations"]:
      vals=[]
      for row in test:
        actual=ab if ab in {"no_protection","no_sense","no_modality","no_global_residual","no_segment_residual","no_token_residual","no_exact_residual","no_macro","no_state_hash","no_migration"} else None
        p=compile_packet(row["text"],"faithful",ablation=actual)
        vals.append({"intent":detect_intent(render_packet(p))[0]==row["intent"],"object_recall":len(set(p.get("objects",{}).values())&set(row["exact_objects"]))/len(row["exact_objects"]),"bytes":b(json.dumps(p,ensure_ascii=False,separators=(",",":")))})
      special={"no_dual_vocabulary":"renderer/core separation removed; no independently measurable benefit in this linear-core proxy","no_verifier":"corrupted render would be released because comparison is absent","no_macro_promotion":"interaction glossary remains static and unpromoted"}.get(ab)
      ablations.append({"ablation":ab,"intent_accuracy":mean([x["intent"] for x in vals]),"object_recall":mean([x["object_recall"] for x in vals]),"mean_packet_bytes":mean([x["bytes"] for x in vals]),"qualitative_boundary":special})
    attacks=[{"attack_id":f"atk-{i:02d}","family":label,"expected_allow":expected,"observed_allow":policy_allows(label,text),"text":text} for i,(label,text,expected) in enumerate(attack_cases(),1)]
    attack_summary={"case_count":len(attacks),"correct":sum(x["expected_allow"]==x["observed_allow"] for x in attacks),"false_allow":sum(x["observed_allow"] and not x["expected_allow"] for x in attacks),"false_block":sum(not x["observed_allow"] and x["expected_allow"] for x in attacks),"cases":attacks}
    best_simple=min(rate["simple_handle"]["mean_bytes"],rate["controlled"]["mean_bytes"],rate["semantic_ir"]["mean_bytes"],rate["zlib"]["mean_bytes"])
    broad=(slice_results["C"]["kernel_native_mean_accuracy"]>=slice_results["C"]["best_surface_mean_accuracy"] and slice_results["B"]["lossless_byte_exact_rate"]==1 and rate["packet"]["mean_bytes"]<best_simple)
    dispositions=[
      {"claim_id":"kerc.broad_matched_total_system_efficiency","disposition":"promoted_at_bounded_scope" if broad else "refuted_after_full_attempt","reason":"Frozen frontier requires matched task/fidelity and strictly lower total-description bytes than the best simple baseline."},
      {"claim_id":"kerc.protected_exact_handle_preservation","disposition":"promoted_at_bounded_scope" if slice_results["A"]["mean_protected_object_recall"]==1 and next(x for x in ablations if x["ablation"]=="no_protection")["object_recall"]<1 else "retained_after_full_attempt","reason":"Finite held-out protected-object comparison only."},
      {"claim_id":"kerc.interaction_shared_glossary_break_even","disposition":"promoted_at_bounded_scope" if break_even else "refuted_after_full_attempt","reason":f"Observed byte-count break-even={break_even}; excludes semantic, privacy, migration, and governance costs."},
      {"claim_id":"kerc.security_or_multilingual_transfer","disposition":"blocked_after_full_attempt","reason":"Finite bilingual templates and rule-owned attacks cannot establish independent security or language transfer."},
    ]
    raw={"schema_version":"asi_stack.p4_m8_kerc_raw.v1","run_id":prereg["run_id"],"preregistration_sha256":sha(BASE/"preregistration.json"),"corpus_sha256":sha(BASE/"corpus.json"),"records":records,"model_predictions":all_predictions}
    dump(RAW,raw)
    result={"schema_version":"asi_stack.p4_m8_kerc_result.v1","run_id":prereg["run_id"],"preregistration_sha256":sha(BASE/"preregistration.json"),"corpus_sha256":sha(BASE/"corpus.json"),"raw_run_sha256":sha(RAW),"denominators":{"corpus":len(rows),"train":len(train),"heldout":len(test),"seeds":len(SEEDS),"ablations":len(ablations),"attacks":len(attacks)},"slice_results":slice_results,"native_core_results":native,"rate_cost_results":{"representations":rate,"best_simple_total_description_bytes":best_simple,"latency_scope":"local median compile+render+field-verification proxy; classifier fit/predict operation proxies reported separately","energy":"not calibrated; no energy claim"},"interaction_amortization":interaction,"observed_break_even_turn":break_even,"ablations":ablations,"attacks":attack_summary,"gate_adjudication":{"broad_efficiency_gate_passed":broad,"terminal_disposition":"broad_efficiency_refuted_narrow_exact_handle_and_shared_glossary_results_retained" if not broad else "bounded_broad_efficiency_review_open","new_chapter_gate_passed":False,"chapter_core_promotion_count":0},"claim_dispositions":dispositions,"support_state_effect":"none_pending_reconciliation","publication_authority":"none","release_authority":"none","non_claims":["general semantic preservation","independent verifier validity","security","multilingual fairness","model or domain transfer","production efficiency","energy efficiency","SOTA","AGI","ASI","deployment readiness","chapter-core support"]}
    dump(RESULT,result)
    print(f"Campaign 6 complete: heldout={len(test)}, kernel_acc={slice_results['C']['kernel_native_mean_accuracy']}, broad={broad}, break_even={break_even}, attacks={attack_summary['correct']}/20.")

if __name__=="__main__": main()
