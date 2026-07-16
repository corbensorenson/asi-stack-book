#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
TARGETS = {
    "lean:command.semantic_interface.operational_invariant": "Every accepted transition in the finite reachable command model binds or preserves exact objective, constraint, output-contract, verification, failure-behavior, and authority slots with explicit provenance/confidence before planning validation and dispatch.",
    "lean:command.semantic_interface.failure_blocks_promotion": "The reachable model and independent consumer reject missing or substituted fields, hidden-instruction provenance, applied override, inferred or widened authority, open blockers, and missing approval, planning-validation, or dispatch receipts.",
    "lean:command.semantic_interface.field_confidence_route": "General command fields require dispatch-eligible provenance/confidence while authority requires the stricter confirmed-or-policy-imposed confidence route before an approved dispatch can be reached.",
}


def main() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(chapter for part in structure["parts"] for chapter in part["chapters"] if chapter["id"] == "intent-to-execution-contracts")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["target"] = TARGETS[target["tag"]]
            target["module"] = "AsiStackProofs.CommandSemanticRefinement"
    name = "Executed command semantic-interface refinement"
    if not any(test.get("name") == name for test in chapter["codex_tests"]):
        chapter["codex_tests"].append({
            "name": name,
            "purpose": "Refine exact semantic-slot identity, provenance/confidence eligibility, explicit precedence, authority ceiling, planning validation, blockers, approvals, and dispatch receipts against the complete command-fixture inventory and prior vertical evidence.",
            "implementation_status": "implemented",
            "result_status": "passes via `python3 scripts/validate_command_semantic_refinement.py`: 13 schema-valid command fixtures classified as 5 interface violations, 2 correct blocks, and 6 interface-admissible records; one 5-event witness; 38/38 rejected mutations; nine-trace handoff and nine-scenario/89-event vertical results digest-bound; support-state effect none",
            "status": "implemented bounded structured-record refinement; interface admissibility is not whole-fixture acceptance; no natural-language semantics, calibrated extraction, authentic authority, prompt-injection containment, deployed dispatch, reproduction, transfer, safety, or chapter-core support claim",
        })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n", encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for record in triage["records"]:
        if record.get("tag") in TARGETS:
            record["formal_target"] = TARGETS[record["tag"]]
            record["module"] = "AsiStackProofs.CommandSemanticRefinement"
            record["rationale"] = "Replaced projection-only ownership with a reachable exact-slot/provenance/confidence/authority/receipt model and an independent consumer over all 13 command fixtures, prior handoff/vertical results, and 38 mutations; support effect none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated three Command proof targets and one executed refinement test.")


if __name__ == "__main__":
    main()
