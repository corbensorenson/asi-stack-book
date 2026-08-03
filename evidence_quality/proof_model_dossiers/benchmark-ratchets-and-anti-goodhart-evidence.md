# Proof-model dossier: benchmark-ratchets-and-anti-goodhart-evidence

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:benchmarks.ratchet.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:benchmarks.ratchet.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:benchmarks.ratchet.fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Current refinement

`AsiStackProofs.BenchmarkRatchets` now exposes 29 theorem declarations. The
refined finite model proves exact custody and stage/outcome coherence across
arbitrary runs, one receipt per accepted event, exact trace composition, clean,
saturated, and contaminated witnesses, and quarantine persistence across an
arbitrary suffix. A same-aggregate-pass-count witness has opposite promotion
admissibility, ruling out any exact classifier that observes only that count.

`scripts/validate_benchmark_fixture_bridge.py` recompiles the exact surface,
explores 19 reachable states through 114 transitions, checks 12 quarantine
suffixes, and rejects 15 lifecycle plus 11 semantic mutations. These are
authored finite-state results. They do not establish construct validity, target
capacity, benchmark quality, contamination detection, hidden-holdout integrity,
model or policy capability, regression quality, anti-Goodhart effectiveness,
support, safety, deployment, reproduction, transfer, or ASI. Chapter support
remains `argument` and `support_state_effect` remains `none`.

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `capability_promotion_requires_benchmark_evidence_and_preserved_regressions` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `saturated_benchmark_alone_cannot_promote_higher_readiness` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `accepted_readiness_promotion_requires_transfer_negative_and_regression_records` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `accepted_saturated_floor_requires_regression_records` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `contaminated_review_cannot_promote_readiness` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `benchmark_antigoodhart_fixture_bridge_valid` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `benchmark_antigoodhart_fixture_bridge_has_expected_controls` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `benchmark_antigoodhart_fixture_bridge_preserves_no_support_promotion` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
