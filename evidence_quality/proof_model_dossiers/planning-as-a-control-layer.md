# Proof-model dossier: planning-as-a-control-layer

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:planning.control_layer.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:planning.control_layer.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:planning.control_layer.plan_graph_admission_route` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:planning.scheduler_state.probe_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:planning.runtime_replan.delta_audit_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:planforge.dag.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:planforge.dag.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `dispatchable_plan_graph_is_index_acyclic_and_ordered` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `dispatchable_plan_graph_orders_member_edges` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `dependency_precedence_blocks_self_dependency` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `failed_quality_predicate_routes_to_escalation_or_residual` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `plan_node_inherits_authority_without_governance_lowering` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `unsatisfied_required_constraints_block_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `valid_dispatchable_plan_has_required_gates` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `valid_dispatchable_plan_has_receipt_and_no_blocked_nodes` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `valid_dispatchable_plan_preserves_parent_authority` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `valid_blocked_plan_has_no_dispatch_receipt` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `valid_replanned_plan_preserves_control_residuals` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `valid_plan_control_record_preserves_non_claim_boundary` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `valid_dispatchable_plan_routes_to_allow_dispatch` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `missing_command_contract_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `incomplete_decomposition_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `cyclic_plan_graph_blocks_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `unordered_dependencies_block_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `authority_escalation_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_context_demand_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_adequacy_contract_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_verification_plan_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_dispatch_gate_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_dispatch_receipt_blocks_plan_graph_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `replanning_without_authority_preservation_blocks_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_residual_register_blocks_new_plan_admission` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_new_plan_graph_routes_to_admissible` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `complete_replanned_graph_routes_to_admissible` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `planning_scheduler_state_probe_fixture_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `runtime_replan_delta_authority_widening_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `runtime_replan_delta_stop_erasure_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `runtime_replan_delta_blocked_authority_dispatch_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `runtime_replan_delta_complete_audit_accepted` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `planning_runtime_replan_delta_audit_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
