# Proof-model dossier: artifact-steward-agents-and-living-project-governance

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:artifact_stewards.work_contract.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:artifact_stewards.treasury_boundary.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:artifact_stewards.release_gate.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:artifact_stewards.sunset_review.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:artifact_stewards.lifecycle_route.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:artifact_stewards.contribution_ledger.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:artifact_stewards.federation_contract.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `dispatched_steward_contract_records_required_boundary` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `protected_steward_action_without_approval_cannot_execute` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `stewarded_release_publication_requires_test_evidence_changelog_residual_and_approval_records` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `sunset_criteria_block_ordinary_work_until_review_opened` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `tainted_event_without_review_routes_to_quarantine` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `sunset_criteria_without_open_review_routes_to_sunset_review` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `autonomy_escalation_without_charter_approval_routes_to_approval` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `treasury_spend_outside_policy_routes_to_approval` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_authorship_credit_routes_to_ledger_repair` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `collapsed_contribution_score_cannot_drive_governance_effect` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `support_state_change_without_transition_requests_evidence_transition` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `separated_contribution_ledger_without_support_change_accepts` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `federation_without_work_contract_requests_contract` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `federated_worker_cannot_inherit_project_authority` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `external_federation_spend_without_approval_routes_to_approval` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `complete_scoped_federation_dispatches` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
