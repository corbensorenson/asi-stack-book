# Proof-model dossier: circle-calculus-and-proof-carrying-ai-contracts

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:circle_contracts.receipt_requires_boundary.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:circle_contracts.consumer_gate.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:circle_contracts.public_consumer_gate.fixture_bridge` | terminally_dispositioned | replace_with_stronger_model |

## Current refinement

`AsiStackProofs.ProofCarryingContracts` now exposes 28 theorem declarations.
The versioned transport model proves exact theorem, parent, consumer, support,
and effect custody across arbitrary finite event lists; zero-authority and
root/descendant revocation coherence; exact batch composition; persistent
revoked-lineage containment across arbitrary suffixes; exclusion of descendant
use after revocation; and preservation of unrelated-lineage availability. The
existing closed trace consumes a descendant, revokes its root lineage, rejects
later descendant use, and leaves the independent lineage available.

`scripts/validate_circle_contract_pack_archive.py` recompiles the exact surface,
checks the pinned nine-contract/four-policy archive, explores forty-five
reachable states through 360 transitions, checks nine revoked-lineage states
through seventy-two contained transitions, preserves all eight trace splits,
and rejects sixteen lifecycle plus fifteen semantic mutations. These are
authored finite-state and pinned-archive results. They do not establish external
theorem resolution, statement equivalence, semantic refinement, authenticated
or deployed transport, distributed invalidation, service liveness or recovery,
downstream utility, support, safety, reproduction, transfer, or ASI. Chapter
support remains `argument` and `support_state_effect` remains `none`.

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `downstream_ready_receipt_exposes_boundary_fields` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `downstream_ready_receipt_missing_boundary_field_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `contract_readiness_alone_cannot_promote_downstream_claim` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `promoted_downstream_claim_without_contract_ready_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `consumer_gate_acceptance_with_stale_or_unsupported_receipt_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `passing_replay_without_replay_artifacts_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `circle_public_consumer_gate_fixture_accepted` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `circle_public_consumer_gate_acceptance_blocks_promotion` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `circle_public_consumer_gate_promotion_overclaim_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `circle_public_consumer_gate_missing_mutation_control_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
