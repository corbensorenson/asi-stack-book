# Proof-model dossier: readiness-gates-residual-escrow-and-quarantine

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:readiness.gates.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:readiness.gates.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:readiness.gates.lifecycle_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `promoted_decision_requires_all_required_gates` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `promoted_decision_with_failed_required_gates_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `quarantined_module_cannot_be_selected_for_ordinary_route` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `accepted_stronger_transition_missing_required_record_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `quarantined_target_ordinary_or_unbacked_diagnostic_route_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `stale_gate_reuse_without_rerun_or_residual_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `readiness_lifecycle_transition_must_be_forward_or_terminal` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `retired_readiness_state_cannot_transition` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `allowed_readiness_transition_requires_core_records` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `qualified_readiness_requires_regression_floor` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `default_readiness_requires_regression_authority_and_route` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `default_readiness_without_regression_floor_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `default_readiness_without_authority_scope_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `quarantine_transition_blocks_ordinary_and_requires_fallback` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `quarantined_lifecycle_transition_with_ordinary_route_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `supersession_requires_record_and_residual_escrow` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `supersession_without_record_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `retirement_requires_receipt_and_residual_escrow` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `retirement_without_receipt_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `readiness_lifecycle_probe_fixture_bridge` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
