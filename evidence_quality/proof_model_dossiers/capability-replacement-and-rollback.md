# Proof-model dossier: capability-replacement-and-rollback

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:replacement.transaction.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:replacement.transaction.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:replacement.transaction.route_envelope` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:replacement.transaction.trace_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:replacement.identity_sequence.invariant_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:replacement.intent_governed.bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `replacement_commit_requires_evidence_and_rollback` | direct_or_projection | semantically_reviewed | retain_reusable_lemma |
| `failed_regression_blocks_replacement_promotion` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_prior_artifact_rejects_replacement` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `authority_expansion_without_approval_routes_to_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `captured_evaluator_routes_replacement_to_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `failed_regression_routes_to_quarantine` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_rollback_receipt_requires_precheck` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `failed_rollback_dry_run_routes_to_canary_only` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `monitor_incident_requires_rollback` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_replacement_review_commits_default` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `lifecycle_missing_candidate_rejects_replacement` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_identity_mismatch_quarantines_candidate` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_authority_widening_without_governance_requests_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_stale_evidence_requires_fresh_evidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_failed_regression_floor_quarantines_candidate` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_missing_canary_scope_requires_precheck` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_failed_canary_stays_canary_only` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_missing_monitor_window_requires_precheck` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_monitor_incident_requires_rollback` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_missing_rollback_handle_requires_precheck` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_failed_rollback_dry_run_stays_canary_only` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_unowned_irreversible_effect_requires_residual_owner` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_missing_residual_owner_requires_owner` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_deprecation_without_notice_requires_notice` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_retirement_without_receipt_requires_receipt` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `lifecycle_missing_nonclaim_boundary_blocks_promotion` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_replacement_lifecycle_commits_default` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `replacement_trace_probe_fixture_valid` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `replacement_trace_probe_rejects_authority_widening` | direct_or_projection | semantically_reviewed | retain_countermodel_or_negative_case |
| `replacement_trace_probe_preserves_no_promotion_boundary` | direct_or_projection | semantically_reviewed | retain_refinement_or_executable_bridge |
| `replacement_identity_sequence_bridge_fixture_valid` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `replacement_identity_sequence_bridge_preserves_identity` | direct_or_projection | semantically_reviewed | retain_refinement_or_executable_bridge |
| `replacement_identity_sequence_bridge_blocks_default_after_failed_monitor` | direct_or_projection | semantically_reviewed | retain_countermodel_or_negative_case |
| `replacement_identity_sequence_bridge_preserves_no_promotion_boundary` | direct_or_projection | semantically_reviewed | retain_refinement_or_executable_bridge |
| `intent_governed_replacement_bridge_fixture_valid` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `intent_governed_replacement_bridge_rejects_authority_widening` | direct_or_projection | semantically_reviewed | retain_countermodel_or_negative_case |
| `intent_governed_replacement_bridge_preserves_no_promotion_boundary` | direct_or_projection | semantically_reviewed | retain_refinement_or_executable_bridge |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
