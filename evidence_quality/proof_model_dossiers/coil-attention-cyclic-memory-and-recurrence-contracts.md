# Proof-model dossier: coil-attention-cyclic-memory-and-recurrence-contracts

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:coil_memory.alias_boundary.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:coil_attention.coverage_not_quality.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |

## Current refinement

`AsiStackProofs.CoilAttentionMemory` now exposes 34 theorem declarations. The
finite model proves that residue-only addressing is non-injective while the
complete residue-plus-winding encoding round-trips and is injective. Across
arbitrary finite event lists it preserves memory, request, address, budget,
support, and effect custody; recurrence-budget safety; zero support/effect
authority; freshness-stage coherence; and monotone recurrence depth. Trace
composition holds, every suffix after stale detection excludes fresh validation
and consumption, and closure absorbs every later event.

`scripts/validate_cyclic_memory_contracts.py` recompiles the exact surface and
independently checks sixteen complete-address round trips, two dropped-coordinate
collision controls, forty reachable states through 320 transitions, twenty-four
stale-suffix states through 192 contained transitions, all eight composition
splits, three mismatch/fallback paths, eleven rejecting event mutations, and
seventeen semantic mutations. These are authored finite-state results. They do
not establish deployed cache truth or isolation, freshness-report truth,
sparse-attention coverage, recurrence utility, retrieval or reasoning quality,
long-context behavior, resource benefit, support, safety, deployment,
reproduction, transfer, or ASI. Chapter support remains `argument` and
`support_state_effect` remains `none`.

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `cyclic_memory_claim_records_residue_and_winding_or_visible_alias_residual` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `reused_cyclic_slot_without_winding_or_residual_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `sparse_coverage_or_freshness_alone_cannot_promote_retrieval_quality` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `structure_only_retrieval_quality_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `recurrence_without_budget_exit_or_fallback_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `stale_read_admitted_as_fresh_without_residual_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
