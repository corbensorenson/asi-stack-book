# Proof-model dossier: context-transactions-snapshots-mounts-and-taint

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:vcm.transactions.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:vcm.transactions.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:vcm.transactions.memory_store_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:vcm.transactions.sequence_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `snapshot_read_sees_committed_event_in_declared_view` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `tainted_source_taints_derivative_without_declassification` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `untainted_derivative_from_tainted_source_requires_declassification` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `open_deletion_without_closure_or_declassification_blocks_materialization` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `ready_open_deletion_without_closure_routes_to_deletion_block` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_snapshot_rejects_context_transaction` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `stale_snapshot_rejects_context_transaction` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `source_branch_mismatch_rejects_context_transaction` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `target_branch_mismatch_rejects_context_transaction` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `mount_fault_without_repair_rejects_context_transaction` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `tainted_transaction_without_declassification_routes_to_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `deleted_cell_without_closure_blocks_materialization_route` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `committed_read_without_visible_read_set_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_replay_boundary_requests_replay_boundary` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `support_promotion_without_transition_requests_evidence_transition` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_non_claim_boundary_requests_non_claim_boundary` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_context_transaction_admits_committed_read` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `current_memory_store_harness_summary_accepted` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `accepted_memory_store_harness_summary_requires_invalid_controls` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `memory_store_harness_summary_with_support_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `current_context_transaction_sequence_summary_accepted` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `accepted_context_transaction_sequence_summary_requires_order` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `context_transaction_sequence_with_support_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
