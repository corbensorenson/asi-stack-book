# Proof-model dossier: asi-is-a-stack-not-a-model

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:stack.layer_boundaries.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:stack.layer_boundaries.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:stack.layer_contract.admission_lifecycle_route` | terminally_dispositioned | replace_with_stronger_model |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `layer_without_external_authority_requires_authorized_handoff` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `valid_stack_trace_rejects_unauthorized_external_handoff` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `handoff_exceeding_caller_ceiling_rejected` | direct_or_projection | semantically_reviewed | retain_countermodel_or_negative_case |
| `no_layer_contract_request_stays_idle` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_layer_identity_requests_identity` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_lifecycle_state_requests_lifecycle` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_owner_requests_owner` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_responsibility_requests_responsibility` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_input_artifacts_requests_input_artifacts` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_output_artifacts_requests_output_artifacts` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_authority_ceiling_requests_ceiling` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_handoff_protocol_requests_protocol` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_invariant_requests_invariant` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_failure_mode_requests_failure_mode` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_evidence_gate_requests_evidence_gate` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `possible_external_action_without_authority_or_handoff_blocks_contract` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_source_mapping_requests_mapping` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `missing_support_state_effect_requests_boundary` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `promotion_request_without_stack_evidence_transition_requests_transition` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `layer_contract_without_nonclaim_boundary_preserves_boundary` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `complete_layer_contract_admission_allows_contract` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
