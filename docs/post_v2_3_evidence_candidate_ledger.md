# Post-v2.3 Evidence Candidate Adjudication

Status: complete; 21/21 candidates have accepted transition records. All 54 chapter-core claims remain at `argument`.

| Candidate | Program | Disposition | Transition | Core effect |
|---|---|---|---|---|
| `post_v2_governed_work_flagship.bounded_matched_local_result` | `post_v2` | `no_change` | `no_change` to `argument` | none |
| `post_v2_routing_deliberation.bounded_matched_local_result` | `post_v2` | `no_change` | `no_change` to `argument` | none |
| `post_v2_update_causality.bounded_real_mutation_result` | `post_v2` | `no_change` | `no_change` to `argument` | none |
| `post_v2_1.ambiguous_routing.bounded_result` | `post_v2_1` | `narrow` | `no_change` to `argument` | none |
| `post_v2_1.full_state_rollback.bounded_result` | `post_v2_1` | `narrow` | `no_change` to `argument` | none |
| `post_v2_1.full_state_update.no_change_result` | `post_v2_1` | `no_change` | `no_change` to `argument` | none |
| `post_v2_1.governed_usefulness_rollback.bounded_result` | `post_v2_1` | `narrow` | `no_change` to `argument` | none |
| `post_v2_1.real_model_deliberation.no_change_result` | `post_v2_1` | `no_change` | `no_change` to `argument` | none |
| `post_v2_1.unlearning_causality.narrow_result` | `post_v2_1` | `narrow` | `no_change` to `argument` | none |
| `qcsa.active_questions_exact_fixture_value` | `qcsa_v2_3` | `refute` | `refuted` to `refuted` | none |
| `qcsa.certificate_authority_fields_exact_value` | `qcsa_v2_3` | `promote` | `upward` to `synthetic-test-backed` | none |
| `qcsa.exact_synthetic_matched_advantage` | `qcsa_v2_3` | `refute` | `refuted` to `refuted` | none |
| `qcsa.governance_prevention_resource_tradeoff` | `qcsa_v2_3` | `narrow` | `no_change` to `argument` | none |
| `qcsa.identity_indirection_exact_migration_value` | `qcsa_v2_3` | `promote` | `upward` to `synthetic-test-backed` | none |
| `qcsa.migration_compatibility_exact_value` | `qcsa_v2_3` | `promote` | `upward` to `synthetic-test-backed` | none |
| `qcsa.open_world_or_production_transfer` | `qcsa_v2_3` | `no_change` | `no_change` to `argument` | none |
| `qcsa.plural_facets_exact_fixture_value` | `qcsa_v2_3` | `promote` | `upward` to `synthetic-test-backed` | none |
| `qcsa.reference_implementation_exact_contract_conformance` | `qcsa_v2_3` | `narrow` | `no_change` to `argument` | none |
| `qcsa.semantic_round_trip_exact_preservation` | `qcsa_v2_3` | `narrow` | `no_change` to `argument` | none |
| `qcsa.task_calibration_exact_result` | `qcsa_v2_3` | `promote` | `upward` to `synthetic-test-backed` | none |
| `qcsa.vertical_reference_exact_reversible_trace` | `qcsa_v2_3` | `narrow` | `no_change` to `argument` | none |

## Decision boundary

The five QCSA `promote` recommendations become accepted `synthetic-test-backed` transitions only for their exact non-core fixture claims. Two exact claims are refuted. Narrow and no-change rows retain `argument`. The implementation and vertical-reference rows are explicitly narrow/no-change rather than being laundered into evaluation or transfer evidence.

Every row in the JSON ledger records exact result digests, owner, comparator, cohort, cost, independence, transfer and validity limits, counterevidence, residuals, permitted changes, and prohibited inference. No external-human prepublication review was required or claimed.
