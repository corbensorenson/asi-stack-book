# Proof-model dossier: circle-calculus-and-proof-carrying-ai-contracts

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:circle_contracts.receipt_requires_boundary.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:circle_contracts.consumer_gate.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:circle_contracts.public_consumer_gate.fixture_bridge` | terminally_dispositioned | replace_with_stronger_model |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `downstream_ready_receipt_exposes_boundary_fields` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `downstream_ready_receipt_missing_boundary_field_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `contract_readiness_alone_cannot_promote_downstream_claim` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `promoted_downstream_claim_without_contract_ready_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `consumer_gate_acceptance_with_stale_or_unsupported_receipt_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `passing_replay_without_replay_artifacts_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `circle_public_consumer_gate_fixture_accepted` | direct_or_projection | terminally_dispositioned | replace_with_stronger_model |
| `circle_public_consumer_gate_acceptance_blocks_promotion` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `circle_public_consumer_gate_promotion_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `circle_public_consumer_gate_missing_mutation_control_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
