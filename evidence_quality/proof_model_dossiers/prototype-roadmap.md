# Proof-model dossier: prototype-roadmap

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:roadmap.phases.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:roadmap.phases.failure_blocks_promotion` | semantically_reviewed | retain_countermodel_or_negative_case |
| `lean:roadmap.phases.fixture_gate_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `roadmap_phase_unlock_requires_passing_acceptance_gates` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `phase_milestone_cannot_promote_claim_without_evidence_artifacts` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `accepted_phase_claim_promotion_requires_evidence_artifacts` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `missing_source_matrix_rejects_phase_route` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `self_improvement_without_independent_evaluator_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `failed_acceptance_gates_keep_phase_research_only` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `support_promotion_without_evidence_transition_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `accepted_non_promoting_phase_integrates` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_non_claim_boundary_rejects_prototype_fixture_bridge` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_prototype_phase_gate_fixture_bridge_accepts` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `accepted_prototype_phase_gate_fixture_bridge_preserves_non_claims` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
