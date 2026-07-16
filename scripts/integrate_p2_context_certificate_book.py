#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; STRUCTURE=ROOT/"book_structure.json"; TRIAGE=ROOT/"proofs/proof_triage.json"
TARGETS={
 "lean:vcm.certificates.operational_invariant":"Every accepted consumer admission in the finite reachable certificate model preserves the exact represented source, derived representation, loss contract, omission ledger, permitted use, lifecycle epoch, authority, and receipt custody.",
 "lean:vcm.certificates.failure_blocks_promotion":"Derived authority cannot exceed represented source authority, and a support-promotion request cannot be admitted without a distinct evidence-transition receipt.",
 "lean:vcm.certificates.lifecycle_admission_route":"The original fifteen lifecycle routes are consumed alongside a five-event reachable refinement and independent 12-certificate/8-scenario/64-mutation consumer."}
def main()->None:
    value=json.loads(STRUCTURE.read_text()); chapter=next(c for p in value["parts"] for c in p["chapters"] if c["id"]=="virtual-context-abi")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS: target["target"]=TARGETS[target["tag"]]; target["module"]="AsiStackProofs.ContextCertificateRefinement"
    name="Executed certificate provenance/lifecycle refinement"
    if not any(t.get("name")==name for t in chapter["codex_tests"]): chapter["codex_tests"].append({"name":name,"purpose":"Refine source binding, derivation, loss/omission/use contracts, verification, deletion closure, lifecycle epoch, authority, evidence-transition, and consumer admission against the real certificate fixture inventory.","implementation_status":"implemented","result_status":"passes via `python3 scripts/validate_context_certificate_refinement.py`: 12 schema-valid certificate projections across 8 scenarios remain distinct from the 3-valid/5-invalid admission result, one 5-event witness, and 64/64 rejected mutations; support-state effect none","status":"implemented bounded structured-record refinement; no source/payload truth, transformation fidelity, verifier independence, deployed enforcement, concurrent revocation, deletion propagation, reproduction, transfer, safety, or chapter-core support claim"})
    STRUCTURE.write_text(json.dumps(value,indent=2)+"\n")
    triage=json.loads(TRIAGE.read_text())
    for rec in triage["records"]:
        if rec.get("tag") in TARGETS: rec["formal_target"]=TARGETS[rec["tag"]]; rec["module"]="AsiStackProofs.ContextCertificateRefinement"; rec["rationale"]="Replaced projection ownership with reachable provenance/lifecycle semantics and an independent real-schema 12-certificate/8-scenario/64-mutation consumer; support effect none."
    TRIAGE.write_text(json.dumps(triage,indent=2)+"\n"); print("Integrated three Context Certificate targets and one executed refinement test.")
if __name__=="__main__": main()
