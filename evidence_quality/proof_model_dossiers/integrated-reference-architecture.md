# Proof-model dossier: integrated-reference-architecture

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:reference_architecture.trace.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:reference_architecture.trace.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:reference_architecture.governed_trace.four_invariants` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `governed_fixture_authority_monotone` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `authority_widening_negative_rejected` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `governed_fixture_revocation_before_effect` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `effect_at_revocation_time_negative_rejected` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `governed_fixture_evidence_integrity` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `unrecorded_promotion_negative_rejected` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `governed_fixture_residual_conserved` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `erased_open_residual_negative_rejected` | unknown_or_mixed | terminally_dispositioned | replace_with_stronger_model |
| `governed_repository_trace_four_invariants` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `end_to_end_trace_contains_required_artifacts_for_layer_handoff` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `trace_with_missing_governance_gate_cannot_be_marked_valid` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `trace_missing_parent_artifacts_routes_to_parentage_repair` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `trace_missing_authority_deltas_routes_to_authority_repair` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `trace_missing_residual_deltas_routes_to_residual_preservation` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `trace_missing_required_governance_gate_blocks_trace` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `trace_missing_validation_command_requires_validation` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
