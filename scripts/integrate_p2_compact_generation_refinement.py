#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "AsiStackProofs.CompactGenerationRefinement"

TARGETS = {
    "lean:compression.cgs.operational_invariant": "Reachable residualization blocks unresolved obligations lacking record, owner, burden, provenance, cost, or fallback receipt.",
    "lean:compression.cgs.failure_blocks_promotion": "Lossy exactness is blocked and failed or mismatched verification requires executable preserved-source fallback.",
    "lean:compression.cgs.admission_route": "Nine reachable stages and 60 routes bind representation identities from source through closure.",
    "lean:compression.cgs.gvr_fixture_bridge": "Independent digest-bound GVR conformance plus reachable verification/fallback semantics replaces copied fixture facts.",
    "lean:compression.cgs.residual_storage_replay_bridge": "Independent digest-bound residual result conformance plus result-substitution and broken-chain closure guards replaces copied summaries.",
    "lean:compression.gvr.operational_invariant": "Observed reconstruction, target identity, verifier identity, and executable fallback are reachable lifecycle obligations.",
    "lean:compression.gvr.failure_blocks_promotion": "Failed verification activates preserved-source fallback or blocks progress without promotion authority.",
    "lean:representation.semantic_tree.operational_invariant": "Semantic use requires provenance identity, content, and a grounding evaluator before migration.",
    "lean:representation.semantic_tree.failure_blocks_promotion": "Hierarchy changes require migration records, reference continuity, and consumer mapping.",
}

PREFIXES = (
    "lean/AsiStackProofs/CompactGenerativeSystems.lean::",
    "lean/AsiStackProofs/GenerateVerifyRepair.lean::",
    "lean/AsiStackProofs/SemanticRepresentation.lean::",
)
RETAINED_NAMES = {
    "unresolved_obligations_without_residual_records_rejected",
    "lossy_unverified_representation_marked_exact_rejected",
    "exact_reconstruction_claim_with_mismatched_repair_rejected",
    "failed_verification_with_exactness_promotion_rejected",
    "grounded_semantic_node_without_provenance_rejected",
    "hierarchy_update_without_references_or_supersession_rejected",
}
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/CompactGenerationRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_compact_generation_refinement.py#route_cases"],
    "consumer_refs": ["docs:compact_generation_refinement", "evidence_quality:model_adequacy_dossiers/compact-generation-refinement.md"],
    "runtime_consumer_refs": [
        "scripts/validate_compact_generation_refinement.py",
        "schemas/compact_generation_refinement.schema.json",
        "experiments/compact_generation_refinement/results/2026-07-15-local.json",
        "scripts/validate_compact_gvr_slice.py",
        "scripts/validate_residual_honesty_conservation.py",
        "scripts/validate_residual_ledger_trace.py",
        "scripts/validate_residual_ledger_storage_replay.py",
    ],
    "replacement_refs": ["proof-model:compact-generation.source-to-closure-refinement.v1", "lean/AsiStackProofs/CompactGenerationRefinement.lean"],
}


def attach(record: dict) -> None:
    for key, refs in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *refs]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(c for part in structure["parts"] for c in part["chapters"] if c["id"] == "compact-generative-systems-and-residual-honesty")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.CompactGenerativeSystems; AsiStackProofs.GenerateVerifyRepair; AsiStackProofs.SemanticRepresentation; AsiStackProofs.CompactGenerationRefinement"
    chapter["minimal_implementation"] = (
        "The current minimum contains six retained finite countermodels plus a seventeen-declaration, nine-stage, sixty-route source-to-closure lifecycle; an independent consumer that rejects 51/51 non-accepting route mutations and digest-binds the five-case GVR, three-valid/five-invalid conservation, four-entry trace, and four-entry/five-invalid replay results; the exact prior Circle and residual-pressure outcomes; and no support or external effect. Twenty-six assumed projections, fixture normalizations, copied result facts, and summary bridges are retired. This is bounded local policy/conformance evidence, not useful compression, codec correctness, verifier adequacy, semantic grounding, deployed fallback, live residual detection, downstream utility, transfer, or SOTA evidence."
    )
    chapter["codex_tests"] = [row for row in chapter["codex_tests"] if not (isinstance(row, dict) and row.get("name") in {"Compact admission route", "Compact GVR fixture bridge", "Residual honesty fixture bridge", "Residual ledger trace surface bridge", "Residual ledger storage replay bridge"})]
    chapter["codex_tests"].append({
        "name": "Compact generation source-to-closure lifecycle refinement",
        "implementation_status": "implemented",
        "result_status": "passes nine stages, all sixty routes, 51/51 non-accepting mutations, four digest-bound source result families, one reachable modeled fallback, and support/effect none; no codec, semantic utility, deployed fallback, residual completeness, transfer, or support claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n", encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for record in triage["records"]:
        if record["tag"] in TARGETS:
            record["module"] = MODULE
            record["formal_target"] = TARGETS[record["tag"]]
            record["rationale"] = "Reachable nine-stage source-to-closure lifecycle, sixty routes, 51 rejecting mutations, four digest-bound bounded result families, and no support/effect authority."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")

    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    for tag in TARGETS:
        target = reviews["target_reviews"][tag]
        attach(target)
        target["semantic_role"] = "Reachable source binding, generation, verification or fallback, residual custody, publication, semantic migration, consumption, and closure lifecycle."
        target["assumptions"] = ["All representation identities, artifact/result digests, policy gates, verifier outcomes, provenance, residual, migration, consumer, and closure fields are trusted inside the finite authored model."]
        target["excluded_effects"] = ["Codec correctness, verifier correctness or real independence, obligation discovery, semantic grounding, deployed fallback, useful compression, downstream utility, total-cost advantage, reproduction, transfer, SOTA, and support are excluded."]
        target["review_rationale"] = "Replace projections, record normalizations, copied result facts, and all-true summaries with a reachable lifecycle and an independently implemented digest-bound consumer."

    baseline_ids = [key for key in reviews["theorem_reviews"] if key.startswith(PREFIXES)]
    retired = 0
    for key in baseline_ids:
        record = reviews["theorem_reviews"][key]
        attach(record)
        name = key.rsplit("::", 1)[1]
        if name not in RETAINED_NAMES:
            retired += 1
            record["review_state"] = "terminally_dispositioned"
            record["disposition"] = "replace_with_stronger_model"
            record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected an assumed policy, normalized one authored record, copied a result fact, or unfolded an authored summary now subsumed by the reachable refinement."
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n", encoding="utf-8")
    print(f"Integrated Compact Generation refinement across {len(TARGETS)} targets and {len(baseline_ids)} frozen declarations; {retired} retired and {len(RETAINED_NAMES)} retained.")


if __name__ == "__main__":
    main()
