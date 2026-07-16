#!/usr/bin/env python3
"""Attach reachable Context Certificate refinement to frozen P2 lineage."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {"lean:vcm.certificates.operational_invariant","lean:vcm.certificates.failure_blocks_promotion","lean:vcm.certificates.lifecycle_admission_route"}
PREFIX = "lean/AsiStackProofs/ContextCertificates.lean::"
RETIRED = {PREFIX+"derived_context_cell_carries_bindings_and_loss_use_contracts",PREFIX+"summary_authority_cannot_exceed_source_ceiling"}
COUNTER = ["lean/AsiStackProofs/ContextCertificateRefinement.lean#countermodels","experiments/context_admission_adequacy/fixtures","experiments/context_certificate_refinement/results/2026-07-15-local.json#mutation_receipts"]
MUTATION = ["scripts/validate_context_certificate_refinement.py#mutations"]
CONSUMER = ["chapter:virtual-context-abi#formalization-hooks","docs:context_certificate_refinement","evidence_quality:model_adequacy_dossiers/context-certificate-refinement.md"]
RUNTIME = ["scripts/validate_context_certificate_refinement.py","schemas/context_certificate_refinement.schema.json","experiments/context_certificate_refinement/results/2026-07-15-local.json","schemas/semantic_page_certificate.schema.json","tests/fixtures/protocol_records/semantic_page_certificate.valid.json","scripts/validate_context_admission_adequacy.py","experiments/context_admission_adequacy/fixtures","lean/AsiStackProofs/ContextCertificateRefinement.lean"]
REPLACEMENT = ["proof-model:vcm-certificates.reachable-provenance-lifecycle-refinement.v1","lean/AsiStackProofs/ContextCertificateRefinement.lean"]

def merge(a:list[str],b:list[str])->list[str]: return list(dict.fromkeys([*a,*b]))
def attach(record:dict)->None:
    for key,vals in (("countermodel_refs",COUNTER),("mutation_refs",MUTATION),("consumer_refs",CONSUMER),("runtime_consumer_refs",RUNTIME),("replacement_refs",REPLACEMENT)): record[key]=merge(record.get(key,[]),vals)

def main()->None:
    value=json.loads(REVIEWS.read_text()); targets=value["target_reviews"]; theorems=value["theorem_reviews"]
    if TARGETS-set(targets) or RETIRED-set(theorems): raise SystemExit("missing frozen Context Certificate lineage")
    roles={
      "lean:vcm.certificates.operational_invariant":"A reachable five-event chain preserves exact source, derived representation, loss, omission, use, epoch, authority, and receipt custody before consumer admission.",
      "lean:vcm.certificates.failure_blocks_promotion":"Derived authority cannot exceed represented source authority, and support promotion requires a distinct evidence-transition receipt before admission.",
      "lean:vcm.certificates.lifecycle_admission_route":"Fifteen bounded routes are consumed alongside reachable certification/verification/admission semantics, thirteen countermodels, and 64 independent mutations."}
    for target in TARGETS:
        rec=targets[target]; attach(rec); rec["semantic_role"]=roles[target]; rec["assumptions"]=["Numeric identities, authority ranks, lifecycle epochs, declarations, policy decisions, verifier outcomes, receipts, fixture labels, and local structured records are trusted only inside the finite model."]; rec["excluded_effects"]=["Source/payload truth, transformation and omission fidelity, verifier independence, deployed enforcement, concurrent revocation, deletion propagation, natural workloads, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."]; rec["review_rationale"]="Resolve frozen certificate lineage to reachable provenance/lifecycle semantics and an independent real-schema consumer without support promotion."
    ids=[key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in ids: attach(theorems[theorem_id])
    for theorem_id in RETIRED: theorems[theorem_id]["review_rationale"]="Frozen lineage retained; the direct assumption projection is physically retired and superseded by reachable provenance/lifecycle semantics, a real-schema consumer, thirteen countermodels, and 64 mutations."
    REVIEWS.write_text(json.dumps(value,indent=2)+"\n"); print(f"Attached Context Certificate refs to {len(TARGETS)} targets and {len(ids)} theorems; {len(RETIRED)} declarations retired.")
if __name__=="__main__": main()
