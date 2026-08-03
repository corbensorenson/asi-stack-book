# Proof-model dossier: failure-modes-of-ungoverned-intelligence

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:failure.invariant_violation.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:failure.invariant_violation.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:failure.recurrence.escalation_route` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:failure.taxonomy.detector_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Current refinement

`AsiStackProofs.FailureRecoveryRefinement` supplies the stronger model requested
by the baseline review. Its five reachable stages preserve rejected state,
admit events only from a valid control state, require failure-class and boundary
custody before detection, open one residual while disabling modeled effects and
promotion, guard readmission through exact identity plus remediation,
independent review, current assurance and taxonomy, residual discharge, and
authority, monotonically account for incidents, recoveries, and recurrences,
and re-isolate one bounded
recurrence. `scripts/validate_failure_recovery_refinement.py` independently
encodes the transition system, checks all six lifecycle splits, and rejects 117
state-preserving mutations. The bounded model has
`support_state_effect=none`: detector truth, containment and remediation
effectiveness, deployed recovery, safety, and transfer remain Theseus or
empirical obligations.

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `failed_required_invariant_blocks_promotion` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `unbounded_authority_detected_as_governance_failure` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `authority_over_ceiling_routes_to_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `tainted_context_without_authority_grant_quarantines` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `subject_modified_evaluator_freezes_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `unverified_claim_promotion_blocks` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `no_failure_record_stays_idle` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_failure_class_requests_class` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_boundary_requests_boundary` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_receipt_requests_receipt` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_owner_requests_owner` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_containment_requests_containment` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_residual_requests_residual` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_learning_path_requests_learning_path` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_normalization_guard_requests_guard` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `recurring_failure_without_review_escalates` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `severe_irreversible_failure_without_review_escalates` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `promotion_request_without_review_blocks_promotion` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `open_escape_path_without_quarantine_quarantines` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `support_promotion_without_failure_evidence_transition_requests_transition` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `failure_record_without_nonclaim_boundary_preserves_boundary` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `complete_failure_record_closes_record` | derived_or_decomposed | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `failure_taxonomy_detector_probe_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
