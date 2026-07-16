# Proof-model dossier: artifact-graphs-audit-logs-and-replay

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:artifacts.graph.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:artifacts.graph.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:artifacts.graph.replay_packet_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.record_reality_sequence_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.receipt_faithfulness_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.receipt_repository_audit_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.receipt_repository_challenge_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.live_attestation_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.randomized_attestation_audit_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:artifacts.graph.epistemic_tcb_fixture_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `produced_artifact_records_parent_job_and_context_refs` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `produced_artifact_missing_trace_refs_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_required_provenance_blocks_promoted_claim_support` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `incomplete_or_blocked_provenance_blocks_promoted_claim_support` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `replay_grade_below_requirement_blocks_sufficiency` | direct_or_projection | semantically_reviewed | retain_load_bearing_semantic |
| `missing_artifact_rejects_artifact_graph_route` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `produced_artifact_without_parent_requires_parent_job` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `produced_artifact_without_source_refs_requires_source_refs` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `produced_artifact_without_context_refs_requires_context_refs` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_context_transaction_refs_requires_transaction_refs` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_semantic_certificate_refs_requires_certificate_refs` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_tool_refs_require_tool_refs` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_claim_links_requires_claim_links` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_test_links_requires_test_links` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_audit_events_require_audit_events` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_replay_metadata_requires_metadata` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `insufficient_replay_grade_requires_upgrade` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_replay_limits_require_replay_limits` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_evidence_gate_requires_evidence_gate` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `stale_certificate_blocks_artifact_reuse` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `promotion_without_permission_blocks_artifact_promotion` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_non_claim_boundary_requires_boundary` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_artifact_graph_route_admits_artifact` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `complete_promoted_artifact_route_admits_artifact` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `replay_packet_parent_job_mismatch_requires_parent_match` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `replay_packet_missing_audit_chain_requires_audit_chain` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `byte_exact_replay_missing_observed_artifact_requires_observation` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `stale_certificate_in_replay_packet_requires_active_certificate` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `support_review_without_replay_validated_transaction_requires_validation` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `partial_replay_promotion_request_blocks_packet_promotion` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `partial_replay_record_only_blocks_promotion_without_rejecting_record` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `complete_byte_exact_replay_packet_admits_bounded_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `complete_support_review_packet_admits_bounded_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `stale_certificate_sequence_event_blocks_bounded_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `incomplete_replay_sequence_event_blocks_bounded_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `fresh_byte_exact_sequence_event_restores_bounded_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `artifact_record_reality_sequence_fixture_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `receipt_faithfulness_adversarial_fixture_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `receipt_repository_audit_fixture_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `receipt_repository_challenge_fixture_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `artifact_live_attestation_probe_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `artifact_randomized_attestation_audit_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |
| `epistemic_tcb_fixture_bridge` | derived_or_decomposed | terminally_dispositioned | replace_with_stronger_model |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
