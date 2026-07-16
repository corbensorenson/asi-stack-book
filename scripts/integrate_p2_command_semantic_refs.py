#!/usr/bin/env python3
"""Attach the reachable Command refinement to frozen P2 lineage."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {
    "lean:command.semantic_interface.operational_invariant",
    "lean:command.semantic_interface.failure_blocks_promotion",
    "lean:command.semantic_interface.field_confidence_route",
}
PREFIX = "lean/AsiStackProofs/CommandContracts.lean::"
RETIRED = {PREFIX + name for name in [
    "valid_command_contract_contains_required_interface_fields",
    "hidden_or_conflicting_instruction_cannot_override_explicit_constraint",
]}
COUNTER = [
    "lean/AsiStackProofs/CommandSemanticRefinement.lean#countermodels",
    "experiments/plan_execution_contracts/fixtures",
    "experiments/command_semantic_refinement/results/2026-07-15-local.json#fixture_receipts",
]
MUTATION = ["scripts/validate_command_semantic_refinement.py#mutated_traces"]
CONSUMER = [
    "chapter:intent-to-execution-contracts#formalization-hooks",
    "docs:command_semantic_refinement",
    "evidence_quality:model_adequacy_dossiers/command-semantic-refinement.md",
]
RUNTIME = [
    "scripts/validate_command_semantic_refinement.py",
    "schemas/command_semantic_refinement.schema.json",
    "experiments/command_semantic_refinement/results/2026-07-15-local.json",
    "schemas/command_contract.schema.json",
    "experiments/plan_execution_contracts/fixtures",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json",
    "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json",
    "lean/AsiStackProofs/CommandSemanticRefinement.lean",
]
REPLACEMENT = [
    "proof-model:command.reachable-semantic-interface-refinement.v1",
    "lean/AsiStackProofs/CommandSemanticRefinement.lean",
]


def merge(left: list[str], right: list[str]) -> list[str]:
    return list(dict.fromkeys([*left, *right]))


def attach(record: dict) -> None:
    for key, values in (
        ("countermodel_refs", COUNTER), ("mutation_refs", MUTATION),
        ("consumer_refs", CONSUMER), ("runtime_consumer_refs", RUNTIME),
        ("replacement_refs", REPLACEMENT),
    ):
        record[key] = merge(record.get(key, []), values)


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8"))
    target_reviews = value["target_reviews"]
    theorem_reviews = value["theorem_reviews"]
    if TARGETS - set(target_reviews) or RETIRED - set(theorem_reviews):
        raise SystemExit("missing frozen Command lineage")
    roles = {
        "lean:command.semantic_interface.operational_invariant": "A reachable five-stage command path binds and preserves exact objective, constraint, output, verification, failure, and authority slots with typed provenance/confidence before dispatch.",
        "lean:command.semantic_interface.failure_blocks_promotion": "Countermodels and 38 mutations reject missing or substituted slots, hidden provenance or override, authority inference/widening, blockers, and missing approval/validation/dispatch receipts.",
        "lean:command.semantic_interface.field_confidence_route": "Dispatch eligibility and stricter authority eligibility are explicit transition preconditions rather than standalone positive-route normalization.",
    }
    for target_id in TARGETS:
        record = target_reviews[target_id]
        attach(record)
        record["semantic_role"] = roles[target_id]
        record["assumptions"] = ["Slot hashes, provenance/confidence labels, authority, approvals, receipts, fixture classifications, and bounded local records are trusted only inside the declared finite model."]
        record["excluded_effects"] = ["Natural-language semantics, calibrated extraction, prompt-injection containment, authentic authority, deployed dispatch/effects, concurrency, natural workloads, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."]
        record["review_rationale"] = "Resolve frozen Command lineage to a reachable exact-slot/provenance/confidence/authority/receipt model and independent local-record consumer without support promotion."
    theorem_ids = [key for key in theorem_reviews if key.startswith(PREFIX)]
    for theorem_id in theorem_ids:
        attach(theorem_reviews[theorem_id])
    for theorem_id in RETIRED:
        theorem_reviews[theorem_id]["review_rationale"] = "Frozen lineage retained; the projection-only declaration is physically retired and superseded by the reachable model, consumer, countermodels, and 38 mutations."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Attached command-semantic refs to {len(TARGETS)} targets and {len(theorem_ids)} theorems; {len(RETIRED)} declarations retired.")


if __name__ == "__main__":
    main()
