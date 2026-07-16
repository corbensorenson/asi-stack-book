# Proof-model dossier: executable-specifications-and-lean-proof-envelope

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:proofs.envelope.operational_invariant` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:proofs.envelope.failure_blocks_promotion` | terminally_dispositioned | replace_with_stronger_model |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `implemented_target_has_module_and_passing_build` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `non_operational_target_remains_planned_or_blocked` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `non_operational_target_not_implemented` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `implemented_target_missing_module_or_build_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `non_lean_artifact_cannot_claim_lean_proof` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `support_promotion_without_transition_or_boundaries_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `external_theorem_without_ids_or_boundary_rejected` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
