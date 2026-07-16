# Proof-model dossier: evidence-states-and-claim-discipline

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:evidence.support_state.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:evidence.support_state.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:evidence.support_state.transition_lifecycle_route` | terminally_dispositioned | replace_with_stronger_model |
| `lean:evidence.bundle.completeness_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:evidence.claim_ledger.completeness_audit_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:evidence.accepted_transition.review_audit_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:evidence.claim_state.transition_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `support_state_transition_requires_evidence` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `missing_required_evidence_blocks_promotion` | direct_or_projection | semantically_reviewed | retain_countermodel_or_negative_case |
| `no_self_promotion` | direct_or_projection | semantically_reviewed | retain_countermodel_or_negative_case |
| `unsupported_can_promote_to_argument` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `terminal_state_cannot_be_promotion_target` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `accepted_terminal_transition_requires_negative_evidence` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `accepted_downgrade_transition_requires_negative_evidence_and_trigger` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `terminal_effect_for_implies_terminal_state` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `accepted_terminal_transition_blocks_promotion_to_new_state` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `no_requested_transition_allows_no_change` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_claim_record_rejects_evidence_transition` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_scope_boundary_requests_scope_boundary` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_support_state_effect_requests_effect_record` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `mismatched_support_state_effect_blocks_transition` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `upward_transition_without_review_requests_review` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `source_derived_without_source_note_requests_required_evidence` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `synthetic_test_backed_without_test_run_requests_required_evidence` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `downward_transition_without_negative_evidence_requests_negative_evidence` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `downward_transition_without_trigger_requests_downgrade_trigger` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `terminal_refutation_with_wrong_effect_requests_terminal_effect` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `terminal_refutation_without_negative_evidence_requests_negative_evidence` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `terminal_refutation_without_changelog_requests_changelog` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `transition_without_nonclaims_preserves_nonclaim_boundary` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `complete_synthetic_test_backed_transition_accepts` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `evidence_bundle_completeness_probe_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `claim_ledger_completeness_audit_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `accepted_transition_review_audit_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `claim_state_transition_bridge_fixture_valid` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `claim_state_transition_bridge_requires_negative_evidence` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `claim_state_transition_bridge_preserves_no_live_claim_movement` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `claim_state_transition_bridge_preserves_nonclaim_boundary` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
