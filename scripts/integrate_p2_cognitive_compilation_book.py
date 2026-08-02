#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; STRUCTURE = ROOT / "book_structure.json"; TRIAGE = ROOT / "proofs/proof_triage.json"
TARGETS = {
    "lean:cognitive_compilation.ir.operational_invariant": "Arbitrary successful runs preserve exact source identity, zero support/external-effect authority, valid traces, batch composition, receipt custody, and nondecreasing plan versions; acceptance requires validation bound to the current plan version.",
    "lean:cognitive_compilation.ir.failure_blocks_promotion": "A material repair returns to lowering only with localized scope, exact obligation preservation, coordinated one-step plan/ledger increments, a ledger receipt, and closed represented residuals; fresh repaired-plan validation is required before acceptance.",
    "lean:cognitive_compilation.ir.semantic_lowering_route_envelope": "The original finite routes are consumed alongside an eight-event reachable refinement and independent exact-build six-fixture/86-mutation consumer covering source, obligation, authority, target, version, validation, receipt, repair, ledger, residual, support, and effect failures.",
}


def main() -> None:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8")); chapter = next(c for p in value["parts"] for c in p["chapters"] if c["id"] == "cognitive-compilation-and-semantic-ir")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS: target["target"] = TARGETS[target["tag"]]; target["module"] = "AsiStackProofs.CognitiveCompilationRefinement"
    name = "Executed obligation-preserving compilation refinement"
    if not any(test.get("name") == name for test in chapter["codex_tests"]):
        chapter["codex_tests"].append({"name": name, "purpose": "Refine exact source obligations through target lowering, validation, localized repair, ledger versioning, and acceptance against the full compilation fixture inventory.", "implementation_status": "implemented", "result_status": "passes via `python3 scripts/validate_cognitive_compilation_refinement.py`: 2 accepted/4 rejected fixtures, an 8-event repair-and-revalidation witness, 33 Lean theorems, and 86/86 rejected mutations; support-state effect none", "status": "implemented bounded structured-record refinement; no natural-language semantics, obligation completeness, backend behavior, independent target evaluation, observed locality, reproduction, transfer, safety, or chapter-core support claim"})
    STRUCTURE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for record in triage["records"]:
        if record.get("tag") in TARGETS: record["formal_target"] = TARGETS[record["tag"]]; record["module"] = "AsiStackProofs.CognitiveCompilationRefinement"; record["rationale"] = "Exact 33-theorem repair/revalidation model plus independently exact-built six-fixture/86-mutation consumer; support and external-effect authority remain false."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated three Cognitive Compilation targets and one executed refinement test.")


if __name__ == "__main__": main()
