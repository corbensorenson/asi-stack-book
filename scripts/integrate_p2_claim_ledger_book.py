#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
MODULE = "AsiStackProofs.ClaimLedgerRefinement"
TARGETS = {
    "lean:claims.ledger.operational_invariant": "Every accepted step and arbitrary successful run preserve durable claim identity, zero external effects, and exact ledger-version/append-count balance; an authorized append advances both counters exactly once.",
    "lean:claims.ledger.failure_blocks_promotion": "Stale bases, ledger self-approval, digest or same-digest payload substitution, open contradictions, missing evidence-owner receipts, and incomplete custody block append or exact acknowledgment.",
    "lean:claims.ledger.revision_lifecycle_route": "A reachable propose-append-materialize-acknowledge lifecycle binds the full pending proposal, exact versions, history, dependencies, ontology migration, residuals, and surface receipts; successful event batches compose and acknowledged states are terminal.",
    "lean:claims.ledger.semantic_assumption_fixture_bridge": "An independent consumer compiles the exact 27-declaration surface, covers 22 route cases, consumes the exact 5/7 revision suite and 1/11 five-project lifecycle, and rejects 34 mutations without support movement.",
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
            "result_status": "passes via `python3 scripts/validate_claim_ledger_refinement.py`: exact 27-declaration Lean surface, 5/7 revision fixtures, 1/11 five-project lifecycle, 22 route cases, 5 stages, and 34/34 rejected mutations; support effect none",
            "status": "bounded authored lifecycle; no claim extraction, semantic-equivalence engine, evidence-quality judgment, concurrent store, natural surface repair, usefulness, causality, reproduction, transfer, or core-support claim",
        })
    chapter["minimal_implementation"] = (
        "Five valid and seven expected-invalid claim-revision fixtures; one bounded five-project contradiction lifecycle with eleven rejecting mutations; four retained bounded legacy lemmas; and a stronger 27-declaration append-only Claim Ledger refinement whose independent consumer covers twenty-two route cases, five reachable stages, and thirty-four rejected mutations. The refinement binds exact claim, ledger, head, semantic, ontology, support-view, history, non-overwrite, dependency, migration, residual, surface, and full pending-proposal state; every successful event list preserves identity, zero external effects, and exact ledger-version/append-count balance, event batches compose, and acknowledged states are terminal. An authored upward support record requires an evidence-owner receipt, and the ledger cannot self-approve support or commit an external effect. This remains finite structured-record evidence, not a claim extractor, semantic-equivalence engine, deployed concurrent store, natural multi-surface repair system, evidence-quality judgment, or chapter-core result."
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
