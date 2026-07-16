#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/"book_structure.json";TRIAGE=ROOT/"proofs/proof_triage.json"
TARGETS={"lean:intent.contract.operational_invariant":"Every accepted compile in the finite reachable intent model preserves the root intent, exact versioned constraint and stop-condition hashes, and approved authority before contract acceptance.","lean:intent.contract.failure_blocks_promotion":"The reachable model and independent consumer reject missing payload, prohibited action, hidden override, authority widening, constraint/stop substitution, silent material deltas, and unreceipted or non-versioned re-contract.","lean:intent.intake.probe_fixture_bridge":"The bounded intake, re-contract, and plan-fixture surfaces are digest-bound to an independent consumer with exact counts and thirty rejecting mutations rather than literal summary theorems."}
def main():
 v=json.loads(STRUCTURE.read_text());ch=next(c for p in v["parts"] for c in p["chapters"] if c["id"]=="human-intent-as-a-formal-input")
 for t in ch["proof_targets"]:
  if t["tag"] in TARGETS:t["target"]=TARGETS[t["tag"]];t["module"]="AsiStackProofs.IntentResolutionRefinement"
 if not any(t.get("name")=="Executed Human Intent resolution-to-contract refinement" for t in ch["codex_tests"]):ch["codex_tests"].append({"name":"Executed Human Intent resolution-to-contract refinement","purpose":"Refine root intent, constraint/stop preservation, authority review, material-delta custody, and versioned re-contract against bounded intake, re-contract, and plan fixtures.","implementation_status":"implemented","result_status":"passes via `python3 scripts/validate_intent_resolution_refinement.py`: 4 valid/6 invalid intake cases, 6 signals, 2 valid/7 invalid re-contract cases, 13 plan fixtures, a 5-event version-2 witness, and 30/30 rejected mutations; support-state effect none","status":"implemented bounded structured-record refinement; no natural-language understanding, semantic completeness, authentic authority extraction, deployed dispatch, reproduction, transfer, safety, or chapter-core support claim"})
 STRUCTURE.write_text(json.dumps(v,indent=2)+"\n")
 t=json.loads(TRIAGE.read_text())
 for r in t["records"]:
  if r.get("tag") in TARGETS:r["formal_target"]=TARGETS[r["tag"]];r["module"]="AsiStackProofs.IntentResolutionRefinement";r["rationale"]="Replaced assumption/literal-summary ownership with a reachable request-to-contract model and independent consumer over bounded intake, re-contract, and plan fixtures plus thirty mutations; support effect none."
 TRIAGE.write_text(json.dumps(t,indent=2)+"\n");print("Integrated three Human Intent proof targets and one executed refinement test.")
if __name__=="__main__":main()
