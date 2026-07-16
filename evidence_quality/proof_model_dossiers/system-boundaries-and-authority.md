# Proof-model dossier: system-boundaries-and-authority

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:authority.ceiling.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:authority.ceiling.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:authority.lifecycle.admission_route` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:authority.revocation.trace_surface_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `valid_transition_without_grant_preserves_ceiling` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_grant_blocks_over_ceiling_execution` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `valid_authority_decision_has_audit_and_nonclaims` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `valid_allow_decision_has_effect_receipt` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `valid_allow_decision_preserves_caller_ceiling` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `valid_allow_decision_target_within_active_ceiling` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `valid_deny_decision_has_no_effect_receipt` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `valid_escalation_routes_to_review` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `no_authority_request_stays_idle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_principal_requests_principal` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_operation_requests_operation` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_permission_class_requests_permission_class` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_caller_ceiling_requests_caller_ceiling` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_target_requirement_requests_target_requirement` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_delegation_chain_requests_delegation_chain` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_grant_requests_grant_record` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `inactive_grant_denies_authority_lifecycle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `expired_grant_denies_authority_lifecycle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revoked_grant_denies_authority_lifecycle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `scope_mismatch_denies_authority_lifecycle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `grant_ceiling_gap_denies_authority_lifecycle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `required_approval_gap_requests_approval` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_effect_receipt_requests_effect_receipt` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_denial_receipt_requests_denial_receipt` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_audit_refs_requests_audit_refs` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `promotion_request_without_evidence_transition_requests_transition` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `authority_lifecycle_without_nonclaim_boundary_preserves_boundary` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_authority_lifecycle_admits_record` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `authority_revocation_trace_surface_bridge` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
