# Proof-model dossier: runtime-adapters-tool-permissions-and-human-approval

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:runtime.adapters.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:runtime.adapters.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:runtime.adapters.effect_replay_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:runtime.adapters.adversarial_boundary_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:runtime.adapters.revocation_route_bridge` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:runtime.adapters.human_oversight_degradation_fixture_bridge` | terminally_dispositioned | replace_with_stronger_model |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `valid_invocation_has_required_permission` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `invocation_without_parent_permission_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `high_impact_adapter_without_approval_is_rejected` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `high_impact_adapter_without_approval_cannot_be_unrejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `valid_leased_invocation_has_active_scoped_sandbox` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `mismatched_effect_lease_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `expired_effect_lease_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `unsandboxed_effect_lease_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `high_impact_rollback_required_without_handle_is_rejected` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `rollback_required_without_handle_cannot_be_unrejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `high_impact_without_scoped_approval_routes_to_approval` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `parent_authority_ceiling_blocks_adapter_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lease_authority_ceiling_blocks_adapter_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `confused_deputy_attempt_rejected_by_adapter_route` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `sandbox_escape_attempt_rejected_by_adapter_route` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_effect_receipt_blocks_adapter_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_runtime_adapter_review_dispatches` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `missing_permission_no_mutation_denies_before_effect` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_permission_without_no_mutation_evidence_requests_evidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `expired_approval_no_mutation_denies_before_effect` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `rollback_required_without_exact_rollback_requests_rollback_evidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_effect_receipt_requests_effect_receipt` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `support_effect_or_repo_write_preserves_no_promotion_boundary` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_runtime_effect_replay_accepts` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_confused_deputy_parent_mismatch_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_missing_permission_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_parent_authority_ceiling_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_lease_authority_ceiling_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_scoped_approval_mismatch_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_expired_approval_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_sandbox_escape_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_secret_materialization_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_missing_rollback_handle_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_missing_effect_receipt_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_missing_audit_refs_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_support_promotion_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_missing_non_claim_boundary_rejected` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_low_impact_dispatch_accepted` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `adapter_adversarial_high_impact_dispatch_accepted` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `revoked_approval_with_no_mutation_evidence_denies_before_effect` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revoked_approval_without_no_mutation_evidence_requests_evidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revoked_lease_with_no_mutation_evidence_denies_before_effect` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revoked_lease_without_no_mutation_evidence_requests_evidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revoked_authority_receipt_with_no_mutation_denies_before_effect` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revoked_authority_receipt_without_no_mutation_requests_evidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revocation_route_missing_receipt_requests_effect_receipt` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_revocation_route_dispatches` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `runtime_adapter_adversarial_boundary_probe_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `human_oversight_degradation_fixture_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
