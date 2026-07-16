# Proof-model dossier: model-weight-custody-and-hardware-roots-of-trust

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:model_weight_custody.required.invalid_attestation_blocks_load` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:model_weight_custody.lifecycle.complete_observed_load` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:model_weight_custody.lifecycle.missing_lineage` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:model_weight_custody.lifecycle.stale_attestation` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:model_weight_custody.lifecycle.undisclosed_verifier_dependencies` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:model_weight_custody.lifecycle.unobserved_load` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:model_weight_custody.lifecycle.release_authority_laundering` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:model_weight_custody.lifecycle.irreversible_distribution_record` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `required_invalid_attestation_blocks_requested_load` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_lineage_requires_custody_repair` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_observed_load_is_bounded` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `missing_lineage_blocks_lifecycle` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `stale_attestation_requires_refresh` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `undisclosed_verifier_dependencies_require_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `unobserved_load_requires_observation` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `distribution_cannot_launder_load_authority` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `acknowledged_distribution_records_irreversibility` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
