#!/usr/bin/env python3
"""Attach the grant-to-effect refinement to frozen Authority P2 lineage."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {
    "lean:authority.ceiling.operational_invariant",
    "lean:authority.ceiling.failure_blocks_promotion",
    "lean:authority.lifecycle.admission_route",
    "lean:authority.revocation.trace_surface_bridge",
}
RETIRED = "lean/AsiStackProofs/Authority.lean::valid_authority_decision_has_audit_and_nonclaims"
PREFIX = "lean/AsiStackProofs/Authority.lean::"
COUNTERMODELS = [
    "lean/AsiStackProofs/AuthorityEffectRefinement.lean#countermodels",
    "experiments/authority_transitions/fixtures",
    "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json#expected_invalid_controls",
    "experiments/authority_revocation_trace/results/2026-07-03-local.json#trace_entries",
]
MUTATIONS = ["scripts/validate_authority_effect_refinement.py#mutation_cases"]
CONSUMERS = [
    "chapter:system-boundaries-and-authority#formalization-hooks",
    "docs:authority_effect_refinement",
    "evidence_quality:model_adequacy_dossiers/authority-effect-refinement.md",
]
RUNTIME = [
    "scripts/validate_authority_effect_refinement.py",
    "schemas/authority_effect_refinement.schema.json",
    "experiments/authority_effect_refinement/results/2026-07-15-local.json",
    "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    "experiments/authority_revocation_trace/results/2026-07-03-local.json",
    "experiments/governed_repository_change_slice/results/2026-07-10-local.json",
    "lean/AsiStackProofs/AuthorityEffectRefinement.lean",
]
REPLACEMENTS = [
    "proof-model:authority.reachable-grant-effect-refinement.v1",
    "lean/AsiStackProofs/AuthorityEffectRefinement.lean",
]


def merged(old: list[str], new: list[str]) -> list[str]:
    return list(dict.fromkeys([*old, *new]))


def attach(review: dict[str, object]) -> None:
    for key, values in (("countermodel_refs", COUNTERMODELS), ("mutation_refs", MUTATIONS), ("consumer_refs", CONSUMERS), ("runtime_consumer_refs", RUNTIME), ("replacement_refs", REPLACEMENTS)):
        review[key] = merged(review.get(key, []), values)  # type: ignore[arg-type]


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8"))
    targets = value["target_reviews"]
    theorems = value["theorem_reviews"]
    missing = sorted(TARGETS - set(targets))
    if missing or RETIRED not in theorems:
        raise SystemExit(f"Missing targets={missing}; retired theorem present={RETIRED in theorems}")
    roles = {
        "lean:authority.ceiling.operational_invariant": "Reachable issuance, approval, dispatch, effect, observation, revocation, and rollback preserve exact grant binding and prevent authority amplification across caller ceiling, epoch, expiry, and one-shot use.",
        "lean:authority.ceiling.failure_blocks_promotion": "Lean countermodels and 38 executable mutations reject widening, confused-deputy substitution, stale or expired grants, missing receipts, post-revocation dispatch, effect without dispatch, and one-shot reuse.",
        "lean:authority.lifecycle.admission_route": "Finite lifecycle routes remain local diagnostic branches; the reachable refinement supplies transition consequences and consumes six decision fixtures plus executed denial/effect paths.",
        "lean:authority.revocation.trace_surface_bridge": "The five-entry revocation surface remains lineage evidence and is digest-bound to a reachable model that clears approval/dispatch custody, increments the epoch, and rejects later dispatch.",
    }
    for target_id in TARGETS:
        review = targets[target_id]
        attach(review)
        review["semantic_role"] = roles[target_id]
        review["assumptions"] = ["Grant identities, principals, operations, targets, receipts, epochs, expiry, observations, and expected fixture dispositions are authoritative only within the declared finite local records."]
        review["excluded_effects"] = ["Natural-language authority extraction, identity and receipt authenticity, wise issuance, concurrency, complete observation, deployed enforcement, production security, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."]
        review["review_rationale"] = "Resolve frozen Authority lineage to the reachable grant-to-effect model and independent executed-evidence consumer without support promotion."
    authority_theorems = [theorem_id for theorem_id in theorems if theorem_id.startswith(PREFIX)]
    for theorem_id in authority_theorems:
        attach(theorems[theorem_id])
    theorems[RETIRED]["review_rationale"] = "Frozen lineage retained, but the projection-only theorem is physically retired and superseded by the reachable grant-to-effect model, concrete consumer, countermodels, and 38 rejecting mutations."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Attached authority-effect refs to {len(TARGETS)} targets and {len(authority_theorems)} frozen theorems; one projection physically retired.")


if __name__ == "__main__":
    main()
