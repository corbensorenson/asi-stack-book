# Proof-model dossier: labor-os-and-typed-jobs

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:jobs.lifecycle.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:jobs.lifecycle.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:jobs.lifecycle.execution_route_envelope` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:jobs.lifecycle.delivery_probe_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:jobs.lifecycle.durable_lifecycle_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `recorded_valid_job_transition_uses_declared_lifecycle_relation` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `job_requiring_approval_cannot_run_without_approval` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_job_rejects_job_execution` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `unlocked_contract_requests_job_contract` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `invalid_lifecycle_blocks_job_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_approval_requires_job_approval` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_permissions_block_job_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `observed_failure_records_job_failure` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `known_job_residual_records_residual` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `delivered_unverified_output_routes_to_adjudication` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `delivered_verified_output_is_evidence_ready` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `dispatch_without_scheduler_slot_routes_to_scheduler` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `dispatch_with_scheduler_slot_runs_job` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `complete_retirement_review_retires_job` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `typed_job_delivery_probe_fixture_bridge` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `durable_retry_without_idempotency_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_retry_authority_widening_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_retry_permission_overreach_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_expired_lease_dispatch_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_evidence_ready_missing_completion_receipt_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_evidence_ready_missing_replay_ref_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_blocked_without_residual_owner_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_missing_non_claim_boundary_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_support_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `durable_retry_complete_trace_accepted` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `durable_expired_lease_blocked_trace_accepted` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `typed_job_durable_lifecycle_probe_fixture_bridge` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
