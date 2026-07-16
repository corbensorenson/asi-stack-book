#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
MODULE = "AsiStackProofs.ClaimLedgerRefinement"
TARGETS = {
    "lean:claims.ledger.operational_invariant": "An accepted ledger step preserves durable claim identity and cannot commit an external effect; an authorized append advances ledger version and append count exactly once.",
    "lean:claims.ledger.failure_blocks_promotion": "Stale bases, ledger self-approval, event substitution, open contradictions, missing evidence-owner receipts, and incomplete custody block append or exact acknowledgment.",
    "lean:claims.ledger.revision_lifecycle_route": "A reachable propose-append-materialize-acknowledge lifecycle binds exact versions, history, dependencies, ontology migration, residuals, and surface receipts.",
    "lean:claims.ledger.semantic_assumption_fixture_bridge": "An independent consumer covers seventeen routes, consumes the exact 5/7 revision suite and 1/11 five-project lifecycle, and rejects 29 mutations without support movement.",
}


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(ch for part in structure["parts"] for ch in part["chapters"] if ch["id"] == "claim-ledgers-and-belief-revision")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    name = "Append-only Claim Ledger and evidence-owner refinement"
    if not any(isinstance(row, dict) and row.get("name") == name for row in chapter["codex_tests"]):
        chapter["codex_tests"].append({
            "name": name,
            "purpose": "Replace checklist acceptance and support-authority ambiguity with exact version binding, append-only history, evidence-owner handoff, materialization, and surface acknowledgment.",
            "implementation_status": "implemented",
            "result_status": "passes via `python3 scripts/validate_claim_ledger_refinement.py`: exact 5/7 revision fixtures, 1/11 five-project lifecycle, 17 routes, 5 stages, and 29/29 rejected mutations; support effect none",
            "status": "bounded authored lifecycle; no claim extraction, semantic-equivalence engine, evidence-quality judgment, concurrent store, natural surface repair, usefulness, causality, reproduction, transfer, or core-support claim",
        })
    chapter["minimal_implementation"] = (
        "Five valid and seven expected-invalid claim-revision fixtures; one bounded five-project contradiction lifecycle with eleven rejecting mutations; four retained bounded legacy lemmas; and a stronger append-only Claim Ledger refinement whose independent consumer covers seventeen routes, five reachable stages, and twenty-nine rejected mutations. The refinement binds exact claim, ledger, head, semantic, ontology, support-view, history, non-overwrite, dependency, migration, residual, and surface state; an authored upward support record requires an evidence-owner receipt, and the ledger cannot self-approve support or commit an external effect. This remains finite structured-record evidence, not a claim extractor, semantic-equivalence engine, deployed concurrent store, natural multi-surface repair system, evidence-quality judgment, or chapter-core result."
    )
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    for record in triage["records"]:
        if record.get("tag") in TARGETS:
            record["module"] = MODULE
            record["formal_target"] = TARGETS[record["tag"]]
            record["rationale"] = "Reachable append-only lifecycle plus independent exact-suite consumer; the ledger records an evidence-owner decision, cannot authorize support, and has support effect none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")
    print("Integrated four Claim Ledger refinement targets and executable receipt.")


if __name__ == "__main__": main()
