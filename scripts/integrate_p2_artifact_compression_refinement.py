#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STRUCTURE=ROOT/"book_structure.json";TRIAGE=ROOT/"proofs/proof_triage.json";REVIEWS=ROOT/"proofs/proof_rationalization_reviews.json"
MODULE="AsiStackProofs.ArtifactCompressionRefinement"
TARGETS={
"lean:compression.artifacts.operational_invariant":"A reachable artifact-to-consumption lifecycle requires full-source custody, exact identities, reconstruction checks, consumer probes, executable fallback, observed outcomes, and closure before a qualified use can complete.",
"lean:compression.artifacts.failure_blocks_promotion":"Failed probes route to fallback, exact-replay gaps block use, raw ratios cannot promote support, and missing evidence transitions block consumption.",
"lean:compression.artifacts.admission_lifecycle_route":"Eight stages and 53 independently consumed routes govern registration, encoding, verification, probing, fallback, admission, observed consumption, and closure without support or external-effect authority."}
PREFIX="lean/AsiStackProofs/ArtifactCompression.lean::"
RETAINED={"invalid_compressed_artifact_use_without_probe_or_fallback_rejected","promotion_candidate_missing_residual_or_fallback_rejected"}
REFS={"countermodel_refs":["lean/AsiStackProofs/ArtifactCompressionRefinement.lean#countermodels"],"mutation_refs":["scripts/validate_artifact_compression_refinement.py#route_cases"],"consumer_refs":["docs:artifact_compression_refinement","evidence_quality:model_adequacy_dossiers/artifact-compression-refinement.md"],"runtime_consumer_refs":["scripts/validate_artifact_compression_refinement.py","schemas/artifact_compression_refinement.schema.json","experiments/artifact_compression_refinement/results/2026-07-15-local.json","scripts/validate_rankfold_public_safe_probe.py","scripts/validate_rankfold_artifact_import.py","tests/fixtures/protocol_records/compressed_artifact_record.valid.json"],"replacement_refs":["proof-model:artifact-compression.request-to-closure-refinement.v1","lean/AsiStackProofs/ArtifactCompressionRefinement.lean"]}
def attach(r:dict)->None:
 for k,v in REFS.items():r[k]=list(dict.fromkeys([*r.get(k,[]),*v]))
def main()->None:
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s["parts"] for c in p["chapters"] if c["id"]=="rankfold-neuralfold-and-artifact-compression")
 for t in c["proof_targets"]:
  t["module"]=MODULE;t["target"]=TARGETS[t["tag"]]
 c["lean_module"]="AsiStackProofs.ArtifactCompression; AsiStackProofs.ArtifactCompressionRefinement"
 c["minimal_implementation"]="Two retained finite probe/fallback and metadata countermodels plus an eight-declaration, eight-stage, 53-route artifact-to-consumption lifecycle; an independent consumer rejects 44/44 non-accepting mutations and digest-binds the exact compressed-artifact fixture, RAW0 replay, NEURAL0 metadata import, and two no-change decisions. One failed-probe route reaches fallback preparation, one qualified-use witness reaches closure, and support/effect authority remains none. Seventeen projections and theorem-per-record consequences are retired. This is bounded policy/conformance and artifact-identity evidence, not codec correctness, NeuralFold reproduction, useful compression, semantic preservation, downstream utility, deployed fallback, transfer, or SOTA evidence."
 c["codex_tests"]=[x for x in c["codex_tests"] if not(isinstance(x,dict) and x.get("name")=="Artifact compression admission lifecycle route")]
 c["codex_tests"].append({"name":"Artifact compression request-to-closure refinement","implementation_status":"implemented","result_status":"passes eight stages, all 53 routes, 44/44 non-accepting mutations, exact fixture/RAW0/NEURAL0/no-change artifact binding, fallback and qualified-use witnesses, support/effect none; no codec-correctness, useful-compression, utility, deployment, transfer, or support claim"})
 STRUCTURE.write_text(json.dumps(s,indent=2)+"\n")
 tri=json.loads(TRIAGE.read_text())
 for r in tri["records"]:
  if r["tag"] in TARGETS:r["module"]=MODULE;r["formal_target"]=TARGETS[r["tag"]];r["rationale"]="Reachable eight-stage artifact-to-consumption lifecycle, 53 routes, 44 rejecting mutations, exact bounded artifacts, and no support/effect authority."
 TRIAGE.write_text(json.dumps(tri,indent=2)+"\n")
 rev=json.loads(REVIEWS.read_text())
 for tag in TARGETS:
  r=rev["target_reviews"][tag];attach(r);r["semantic_role"]="Reachable full-source, encoding, reconstruction, probe, fallback, admission, consumption, residual, and closure lifecycle.";r["assumptions"]=["All identities, codec/decoder facts, verification, probe, utility, rights, fallback, cost, outcome, and closure fields are trusted inside the finite authored model."];r["excluded_effects"]=["Codec correctness, NeuralFold reproduction, semantic preservation, utility, security, rights adequacy, cost benefit, deployment, transfer, SOTA, and support are excluded."];r["review_rationale"]="Replace direct implications and theorem-per-record route cases with a reachable lifecycle and independently implemented digest-bound consumer."
 ids=[k for k in rev["theorem_reviews"] if k.startswith(PREFIX)];retired=0
 for k in ids:
  r=rev["theorem_reviews"][k];attach(r)
  if k.rsplit("::",1)[1] not in RETAINED:retired+=1;r["review_state"]="terminally_dispositioned";r["disposition"]="replace_with_stronger_model";r["review_rationale"]="Frozen lineage retained; declaration physically retired because the direct projection or flat route consequence is subsumed by reachable identity, reconstruction, probe, fallback, outcome, closure, support, and effect semantics."
 REVIEWS.write_text(json.dumps(rev,indent=2)+"\n")
 print(f"Integrated Artifact Compression refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations; {retired} retired and {len(RETAINED)} retained.")
if __name__=="__main__":main()
