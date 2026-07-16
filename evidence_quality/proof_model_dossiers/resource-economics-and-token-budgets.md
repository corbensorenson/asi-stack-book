# Proof-model dossier: resource-economics-and-token-budgets

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:resources.budgets.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:resources.budgets.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:resources.costed_route.fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:resources.workflow_trace.trace_property_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:resources.capacity_smoothing.reviewer_trace_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:resources.serving_memory.separation_guard` | terminally_dispositioned | replace_with_stronger_model |
| `lean:resources.flagship.aggregate_invariant` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:resources.ci_failure_classification.fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:resource.governance_tax.tradeoff_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:simulation.fidelity.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:simulation.fidelity.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:resource.simulation_fidelity.theseus_receipt_suite.fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:resource.simulation_fidelity.theseus_rlds_minari_trace_export.fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `task_budget_cannot_disable_required_safety_or_verification_gates` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `required_safety_gate_disabled_rejects_budget_gate_preservation` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `high_risk_task_with_insufficient_verification_budget_is_not_dispatched` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `high_risk_insufficient_budget_dispatch_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `aggregate_serving_throughput_requires_single_request_boundary` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `serving_memory_throughput_quality_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `costed_route_fixture_selected_is_eligible` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `cheap_unverified_transform_rejected_by_fixture` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `hidden_residual_auto_merge_rejected_by_fixture` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `selected_route_is_lowest_cost_eligible_in_fixture` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `costed_route_fixture_trace_selects_lowest_eligible_route` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `resource_workflow_trace_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_preserves_high_risk_ordering` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_residualizes_displaced_costs` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_rejects_physical_feasibility_overclaim` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_rejects_latency_only_selection` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_rejects_capacity_budget_overrun` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_has_no_support_promotion` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_workflow_trace_fixture_events_roll_up_to_summary` | unknown_or_mixed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `resource_workflow_trace_fixture_events_keep_high_risk_first` | unknown_or_mixed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `resource_workflow_trace_fixture_events_preserve_guard_flags` | unknown_or_mixed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `capacity_smoothing_reviewer_trace_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `capacity_smoothing_reviewer_trace_preserves_review_capacity` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `capacity_smoothing_reviewer_trace_preserves_protected_review_overhead` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `capacity_smoothing_reviewer_trace_residualizes_displaced_review_costs` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `capacity_smoothing_reviewer_trace_has_no_support_promotion` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `blocked_protected_review_rejects_low_risk_review_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `high_risk_review_without_protected_overhead_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `blocked_protected_review_requires_displaced_cost_residual` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `resource_load_smoothing_workload_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_load_smoothing_workload_reduces_overrun` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_load_smoothing_workload_rejects_review_erasure` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_load_smoothing_workload_residualizes_deferrals` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_load_smoothing_workload_has_no_support_promotion` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `resource_flagship_lane_aggregate_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_flagship_lane_aggregate_preserves_no_core_promotion` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_flagship_lane_aggregate_carries_transition_accounting` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_ci_cost_profile_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_ci_cost_profile_preserves_no_core_promotion` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_ci_cost_profile_classifies_all_failures` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_ci_cost_profile_records_recovery_boundary` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_governance_tax_tradeoff_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_governance_tax_tradeoff_shows_governance_can_pay` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_governance_tax_tradeoff_allows_low_risk_shortcut` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `resource_governance_tax_tradeoff_preserves_no_promotion_boundary` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `simulation_claim_used_as_evidence_includes_scope_fidelity_and_bounds` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `evidence_use_without_scope_declaration_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `promoted_experiment_result_cannot_exceed_declared_fidelity_support` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `promoted_result_above_declared_fidelity_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_simulation_fidelity_receipt_suite_import_fixture_valid` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `theseus_simulation_fidelity_receipt_suite_import_core_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_simulation_fidelity_receipt_suite_import_physical_feasibility_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_simulation_fidelity_receipt_suite_import_benchmark_transfer_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_simulation_fidelity_receipt_suite_import_native_kv_parity_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_rlds_minari_trace_export_import_fixture_valid` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `theseus_rlds_minari_trace_export_import_core_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_rlds_minari_trace_export_import_dataset_quality_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `theseus_rlds_minari_trace_export_import_replay_success_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
