# Proof-model dossier: intent-to-execution-contracts

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:intent_execution.contracts.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:intent_execution.contracts.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |
| `lean:intent_execution.contracts.dispatch_route_envelope` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:intent_execution.handoff_trace.probe_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:command.semantic_interface.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:command.semantic_interface.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:command.semantic_interface.field_confidence_route` | semantically_reviewed | retain_load_bearing_semantic |

## Current refinement

`AsiStackProofs.IntentExecutionRefinement` now gives every event kind an exact,
exclusive payload contract, closing the prior path by which a lowering event
could carry effect, observation, delivery, residual, or rollback data. Its
thirty-seven declarations prove one-step and arbitrary-run preservation of the
vertical invariant, root-contract and authority-ceiling custody, monotone
logical time, bounded active authority, effect-attempt and observation
accounting, approval and dispatch custody, artifact and independent-verification
custody, exact delivery accounting, stopped blocking, positive residualization,
and failed-rollback quarantine. The existing ten-event witness reaches delivery;
eighteen closed countermodels reject custody substitution, stale time,
kind-invalid payloads, premature lifecycle transitions, self-verification,
inexact rollback, and quarantine without a residual.

`scripts/validate_intent_execution_vertical_refinement.py` requires the exact
thirty-seven-declaration theorem surface, rejects unproved declarations,
compiles the module, and independently checks nine executed scenarios, 89
events, six material effects, and thirty concrete source mutations. The model
trusts authored event kinds, contract and artifact identities, authority,
receipts, observations, verifier identity, rollback, and residual fields. It
proves no parser correctness, natural-language or arbitrary semantic
equivalence, authentic authority, approval-service behavior, tool-effect truth,
verifier competence, rollback efficacy, useful delivery, support transition,
deployment, reproduction, or transfer. Those behavioral and cross-component
obligations belong to Project Theseus or empirical evaluation. Chapter support
remains `argument` and `support_state_effect` remains `none`.

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `valid_command_contract_contains_required_interface_fields` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `missing_required_field_blocks_complete_command_contract` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `hidden_or_conflicting_instruction_cannot_override_explicit_constraint` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `accepted_hidden_override_violates_explicit_constraint_precedence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `inferred_authority_confidence_requires_authority_confidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_output_confidence_requires_output_confidence` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_field_confidence_allows_dispatch` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `compiled_execution_job_preserves_parent_contract_constraints` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `execution_job_without_required_approval_cannot_transition_to_running` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `missing_contract_rejects_execution_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_objective_requests_execution_clarification` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `authority_widening_blocks_execution_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `hidden_override_blocks_execution_dispatch` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `required_approval_missing_routes_to_approval` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_artifacts_request_execution_clarification` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_verification_plan_routes_to_verification` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `known_residual_records_execution_residual` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_dispatch_review_is_ready` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `intent_execution_handoff_probe_fixture_bridge` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
