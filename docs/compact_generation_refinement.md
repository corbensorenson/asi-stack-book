# Compact generation and residual lifecycle refinement

This refinement replaces copied fixture facts and theorem-per-record admission normalizations with a reachable nine-stage lifecycle from source binding through generation, verification or executable fallback, residual custody, publication, semantic migration, consumption, and closure.

The formal model is `AsiStackProofs.CompactGenerationRefinement`. Its 60 routes bind representation, version, source, contract, generator, target, verifier, residual ledger, consumer, and result-set identities. It separates generation, verification, fallback, migration, consumption, support assignment, and external-effect counts. A fallback witness reaches closure with one modeled fallback activation and no support or external-effect authority.

`python3 scripts/validate_compact_generation_refinement.py` independently reimplements route priority, reaches all 60 routes, rejects 51/51 non-accepting mutations, recompiles the Lean module, and digest-binds four existing result families: the 5-case Compact GVR slice with 3 rejected controls, the 3-valid/5-invalid residual-conservation suite, the 4-entry repository residual trace, and the 4-entry/5-invalid storage replay.

This is finite local policy and conformance evidence only. It does not prove a useful codec, correct or independent verifier, complete residual discovery, semantic grounding, deployed fallback, downstream utility, total-cost advantage, transfer, or state of the art. The result has no support-state or external effect.
