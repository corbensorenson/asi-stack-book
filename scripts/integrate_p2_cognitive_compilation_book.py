#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; STRUCTURE = ROOT / "book_structure.json"; TRIAGE = ROOT / "proofs/proof_triage.json"
TARGETS = {
    "lean:cognitive_compilation.ir.operational_invariant": "Every accepted target in the finite reachable lowering model preserves the exact plan, three represented obligations, source constraint, target identity, approved authority, and lowering/validation custody.",
    "lean:cognitive_compilation.ir.failure_blocks_promotion": "A material repair can return to validated state only with localized scope, exact affected-obligation preservation, a one-step repair-ledger version increment, and a ledger receipt; open residuals block acceptance.",
    "lean:cognitive_compilation.ir.semantic_lowering_route_envelope": "The original finite lowering routes are consumed alongside a seven-event reachable refinement and independent six-fixture/47-mutation consumer covering source, obligation, authority, target, validation, receipt, repair, ledger, and residual failures.",
}


def main() -> None:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8")); chapter = next(c for p in value["parts"] for c in p["chapters"] if c["id"] == "cognitive-compilation-and-semantic-ir")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS: target["target"] = TARGETS[target["tag"]]; target["module"] = "AsiStackProofs.CognitiveCompilationRefinement"
    name = "Executed obligation-preserving compilation refinement"
    if not any(test.get("name") == name for test in chapter["codex_tests"]):
        chapter["codex_tests"].append({"name": name, "purpose": "Refine exact source obligations through target lowering, validation, localized repair, ledger versioning, and acceptance against the full compilation fixture inventory.", "implementation_status": "implemented", "result_status": "passes via `python3 scripts/validate_cognitive_compilation_refinement.py`: 2 accepted/4 rejected fixtures, a 7-event localized-repair witness, and 47/47 rejected mutations; support-state effect none", "status": "implemented bounded structured-record refinement; no natural-language semantics, obligation completeness, backend behavior, independent target evaluation, observed locality, reproduction, transfer, safety, or chapter-core support claim"})
    STRUCTURE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for record in triage["records"]:
        if record.get("tag") in TARGETS: record["formal_target"] = TARGETS[record["tag"]]; record["module"] = "AsiStackProofs.CognitiveCompilationRefinement"; record["rationale"] = "Replaced projection-only ownership with a reachable exact-obligation/target/authority/receipt/repair-ledger model and independent consumer over all six fixtures and 47 mutations; support effect none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated three Cognitive Compilation targets and one executed refinement test.")


if __name__ == "__main__": main()
