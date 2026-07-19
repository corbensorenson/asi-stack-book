#!/usr/bin/env python3
"""Prospectively freeze Campaign 6 corpus, design, and executable identity."""
from __future__ import annotations

from p4_m8_kerc_common import BASE, DOMAINS, INTENTS, LANGUAGES, ROOT, SEEDS, dump, sha

EN = {
 "approve": ["Please approve", "Authorize", "You must permit", "Green-light", "Can you authorize", "Kindly approve"],
 "deny": ["Please deny", "Reject", "You must block", "Refuse", "Can you deny", "Kindly reject"],
 "schedule": ["Please schedule", "Plan", "You must book", "Schedule", "Can you plan", "Kindly book"],
 "cancel": ["Please cancel", "Abort", "You must stop", "Withdraw", "Can you cancel", "Kindly abort"],
 "compare": ["Please compare", "Contrast", "You must weigh", "Compare", "Can you contrast", "Kindly compare"],
 "calculate": ["Please calculate", "Compute", "You must derive", "Calculate", "Can you compute", "Kindly calculate"],
 "explain": ["Please explain", "Describe", "You must clarify", "Explain", "Can you describe", "Kindly clarify"],
 "quote": ["Please quote", "Repeat exactly", "You must cite", "Quote", "Can you cite", "Kindly repeat exactly"],
}
ES = {
 "approve": ["Por favor aprueba", "Autoriza", "Debe permitir", "Aprueba", "¿Puedes autorizar", "Por favor permite"],
 "deny": ["Por favor deniega", "Rechaza", "Debe bloquear", "Deniega", "¿Puedes rechazar", "Por favor bloquea"],
 "schedule": ["Por favor programa", "Planifica", "Debe agendar", "Programa", "¿Puedes planificar", "Por favor agenda"],
 "cancel": ["Por favor cancela", "Aborta", "Debe detener", "Cancela", "¿Puedes abortar", "Por favor detén"],
 "compare": ["Por favor compara", "Contrasta", "Debe comparar", "Compara", "¿Puedes contrastar", "Por favor compara"],
 "calculate": ["Por favor calcula", "Computa", "Debe calcular", "Calcula", "¿Puedes computar", "Por favor calcula"],
 "explain": ["Por favor explica", "Describe", "Debe aclarar", "Explica", "¿Puedes describir", "Por favor aclara"],
 "quote": ["Por favor cita", "Repite exactamente", "Debe citar", "Cita", "¿Puedes citar", "Por favor repite exactamente"],
}

def main() -> None:
    if (BASE / "raw/campaign_run.json").exists() or (BASE / "results/confirmatory_result.json").exists():
        raise SystemExit("Campaign 6 outcomes exist; refusing to rewrite frozen inputs")
    rows=[]
    for intent in INTENTS:
      for language in LANGUAGES:
       for domain in DOMAINS:
        for variant in range(6):
          lead=(EN if language=="en" else ES)[intent][variant]
          name='"Zoë Δ"' if domain=="research" else '"ACME-β"'
          payload=f'{name} 12.5 GB 2026-08-{variant+10:02d} https://example.org/{intent} `x_{variant}=7`'
          negated=variant==5
          neg=(" Do not reverse the requested action." if language=="en" else " No revierta la acción solicitada.") if negated else ""
          text=f"{lead} {payload}.{neg}"
          phase="train" if variant<4 else ("heldout" if variant==4 else "adversarial_heldout")
          rows.append({"record_id":f"{intent}-{language}-{domain}-{variant}","phase":phase,"intent":intent,"negated":negated,"language":language,"domain":domain,"variant":variant,"text":text,"exact_objects":[name,"12.5 GB",f"2026-08-{variant+10:02d}",f"https://example.org/{intent}",f"`x_{variant}=7`"]})
    corpus={"schema_version":"asi_stack.p4_m8_kerc_corpus.v1","rows":rows}
    dump(BASE/"corpus.json", corpus)
    design={
      "schema_version":"asi_stack.p4_m8_kerc_design.v1","run_id":"p4-m8-kerc-runtime-001","recorded_date":"2026-07-16",
      "state":"prospectively_frozen_before_outcome_execution","seeds":list(SEEDS),"record_count":len(rows),
      "split_counts":{"train":128,"heldout":32,"adversarial_heldout":32},
      "slices":{"A":"protected objects, exact handles, shared terminology","B":"sense-aware semantic/faithful/lossless compilation and deterministic round trip","C":"small Kernel-native intent core versus matched surface and simple-handle cores"},
      "baselines":["surface_sentencepiece_unigram","surface_byte_char_ngram","dynamic_word_chunks","zlib_learned_dictionary_proxy","controlled_language","semantic_ir","copy_aware_generation","simple_entity_handle_shared_glossary"],
      "native_core":{"family":"L2 logistic regression","representations":["surface_unigram","surface_byte","simple_handle_glossary","kernel_packet"],"seeds":list(SEEDS),"heldout_labels_isolated":True},
      "metrics":["intent_accuracy","polarity_accuracy","protected_object_recall","byte_exact_recovery","semantic_field_accuracy","initially_correct_corruption","encoded_bytes","total_description_bytes","compile_render_verify_latency","training_operation_proxy","inference_operation_proxy","interaction_break_even"],
      "ablations":["no_protection","no_sense","no_modality","no_global_residual","no_segment_residual","no_token_residual","no_exact_residual","no_macro","no_dual_vocabulary","no_verifier","no_state_hash","no_migration","no_macro_promotion"],
      "attack_count":20,"attack_families":["dialect_erasure","identity_collision","unicode_confusable","quote_escape","code_url_injection","poisoned_concept","malicious_residual","cross_scope_reuse","expiry_loss","state_skew","downgrade","migration_corruption","macro_boundary","authority_widening","privacy_deletion","verifier_monoculture","silent_fallback"],
      "primary_falsifier":"broad efficiency is refuted unless KERC is noninferior on heldout task and exact fidelity and strictly improves the best simple baseline on matched total-description bytes plus measured end-to-end latency; a narrower exact-handle or terminology result is retained separately",
      "chapter_gate":"existing twelve owners first; no new chapter unless a durable multi-consumer ABI, separately governed residual lifecycle, unowned invariant, and distinct reader job are all observed",
      "support_ceiling":"one authored bilingual templated corpus, deterministic compiler, small linear cores, finite attacks, and local measurements only; no general semantic truth, multilingual fairness, security, efficiency transfer, SOTA, AGI, ASI, deployment, or chapter-core support"
    }
    dump(BASE/"design.json",design)
    code=["p4_m8_kerc_common.py","build_p4_m8_kerc_campaign.py","run_p4_m8_kerc_campaign.py","validate_p4_m8_kerc_design.py"]
    prereg={"schema_version":"asi_stack.p4_m8_kerc_preregistration.v1","run_id":design["run_id"],"state":design["state"],"design_sha256":sha(BASE/"design.json"),"corpus_sha256":sha(BASE/"corpus.json"),"result_schema_sha256":sha(ROOT/"schemas/p4_m8_kerc_result.schema.json"),"code_sha256":{x:sha(ROOT/"scripts"/x) for x in code},"outcome_aware_retry_allowed":False,"heldout_label_access_during_training":False,"support_state_effect":"none_before_adjudication","publication_authority":"none","release_authority":"none"}
    dump(BASE/"preregistration.json",prereg)
    print(f"Built P4/M8 Campaign 6 freeze: {len(rows)} records, 64 heldout, 5 seeds, 13 ablations, 20 attacks.")

if __name__=="__main__": main()
