#!/usr/bin/env python3
"""Attach reachable Cognitive Compilation refinement to frozen P2 lineage."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {"lean:cognitive_compilation.ir.operational_invariant", "lean:cognitive_compilation.ir.failure_blocks_promotion", "lean:cognitive_compilation.ir.semantic_lowering_route_envelope"}
PREFIX = "lean/AsiStackProofs/CognitiveCompilation.lean::"
RETIRED = {PREFIX + "compiled_artifact_preserves_all_required_ir_obligations", PREFIX + "repair_invalidating_existing_obligation_requires_ledger_update"}
COUNTER = ["lean/AsiStackProofs/CognitiveCompilationRefinement.lean#countermodels", "experiments/cognitive_compilation_traces/fixtures", "experiments/cognitive_compilation_refinement/results/2026-07-15-local.json#fixture_receipts"]
MUTATION = ["scripts/validate_cognitive_compilation_refinement.py#mutations"]
CONSUMER = ["chapter:cognitive-compilation-and-semantic-ir#formalization-hooks", "docs:cognitive_compilation_refinement", "evidence_quality:model_adequacy_dossiers/cognitive-compilation-refinement.md"]
RUNTIME = ["scripts/validate_cognitive_compilation_refinement.py", "schemas/cognitive_compilation_refinement.schema.json", "experiments/cognitive_compilation_refinement/results/2026-07-15-local.json", "schemas/semantic_atom.schema.json", "experiments/cognitive_compilation_traces/fixtures", "experiments/cognitive_compilation_traces/results/2026-07-02-local.md", "lean/AsiStackProofs/CognitiveCompilationRefinement.lean"]
REPLACEMENT = ["proof-model:cognitive-compilation.reachable-obligation-refinement.v1", "lean/AsiStackProofs/CognitiveCompilationRefinement.lean"]


def merge(left: list[str], right: list[str]) -> list[str]: return list(dict.fromkeys([*left, *right]))
def attach(record: dict) -> None:
    for key, values in (("countermodel_refs", COUNTER), ("mutation_refs", MUTATION), ("consumer_refs", CONSUMER), ("runtime_consumer_refs", RUNTIME), ("replacement_refs", REPLACEMENT)):
        record[key] = merge(record.get(key, []), values)


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8")); targets = value["target_reviews"]; theorems = value["theorem_reviews"]
    if TARGETS - set(targets) or RETIRED - set(theorems): raise SystemExit("missing frozen Cognitive Compilation lineage")
    roles = {
        "lean:cognitive_compilation.ir.operational_invariant": "A reachable seven-event lowering and localized-repair path preserves exact plan, obligation, source-constraint, target, authority, version, receipt, and residual custody before acceptance.",
        "lean:cognitive_compilation.ir.failure_blocks_promotion": "Countermodels and 47 mutations reject obligation or target substitution, authority widening, missing receipts, validation laundering, global or unversioned repair, and residual-bearing acceptance.",
        "lean:cognitive_compilation.ir.semantic_lowering_route_envelope": "Twelve bounded priority branches remain, now consumed alongside a reachable refinement and independent classification of all six trace fixtures.",
    }
    for target in TARGETS:
        record = targets[target]; attach(record); record["semantic_role"] = roles[target]
        record["assumptions"] = ["Numeric identities, authority, scope, validator, receipt, ledger, fixture labels, and local structured records are trusted only inside the finite model."]
        record["excluded_effects"] = ["Natural-language source/target semantics, obligation completeness, backend behavior, evaluator independence, observed repair locality, natural workloads, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."]
        record["review_rationale"] = "Resolve frozen Cognitive Compilation lineage to a reachable exact-obligation/target/authority/receipt/repair-ledger model and independent consumer without support promotion."
    theorem_ids = [key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in theorem_ids: attach(theorems[theorem_id])
    for theorem_id in RETIRED: theorems[theorem_id]["review_rationale"] = "Frozen lineage retained; the assumption-projection declaration is physically retired and superseded by the reachable model, independent fixture consumer, countermodels, and 47 mutations."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Attached Cognitive Compilation refs to {len(TARGETS)} targets and {len(theorem_ids)} theorems; {len(RETIRED)} declarations retired.")


if __name__ == "__main__": main()
