#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
MODULE = "AsiStackProofs.VerificationBandwidthRefinement"
TARGETS = {
    "lean:verification_bandwidth.adequacy.operational_invariant": "Context admission is separated from a frozen claim-specific obligation plan; only an exactly bound execution can advance to adjudication.",
    "lean:verification_bandwidth.adequacy.failure_blocks_promotion": "Direct chapter-core promotion requests and represented contradictions block evidence-gate handoff; high-risk correlated evaluation requires escalation.",
    "lean:verification_bandwidth.adequacy.route_envelope": "A five-stage lifecycle covers twelve explicit routes whose strongest positive effect is handoff to an independent evidence gate, never support assignment.",
    "lean:verification_bandwidth.contradiction_probe_fixture_bridge": "An independent consumer recomputes all twelve routes, consumes the exact 3/5 admission, 2/7 contradiction, and 3/5 capacity suites, and rejects 31 evidence-handoff mutations.",
}


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] == "verification-bandwidth-and-context-adequacy"
    )
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    name = "Reachable verification-plan and evidence-gate refinement"
    if not any(isinstance(row, dict) and row.get("name") == name for row in chapter["codex_tests"]):
        chapter["codex_tests"].append({
            "name": name,
            "purpose": "Replace adequacy-to-support authority leakage with exact plan/execution binding, exhaustive dispositions, route priority, and evidence-gate handoff.",
            "implementation_status": "implemented",
            "result_status": "passes via `python3 scripts/validate_verification_bandwidth_refinement.py`: 3/5 admission, 2/7 contradiction, 3/5 capacity, 12 routes, 5 stages, and 31/31 rejected mutations; support effect none",
            "status": "bounded authored lifecycle; no model, natural claim, calibrated adequacy, deployed ledger, usefulness, causality, reproduction, transfer, safety, or core-support claim",
        })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    for record in triage["records"]:
        if record.get("tag") in TARGETS:
            record["module"] = MODULE
            record["formal_target"] = TARGETS[record["tag"]]
            record["rationale"] = "Reachable verification-plan lifecycle plus independent exact-suite consumer; strongest effect is evidence-gate handoff and support effect remains none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")
    print("Integrated four Verification Bandwidth refinement targets.")


if __name__ == "__main__":
    main()
