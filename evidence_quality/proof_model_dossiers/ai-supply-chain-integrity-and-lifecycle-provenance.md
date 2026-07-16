# Proof-model dossier: ai-supply-chain-integrity-and-lifecycle-provenance

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:ai_supply_chain.unresolved_critical_advisory.quarantines_artifact` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:ai_supply_chain.complete_requested_artifact.reaches_custody_review` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:ai_supply_chain.missing_lineage.requires_repair` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:ai_supply_chain.missing_component_inventory.requires_review` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:ai_supply_chain.missing_revocation_path.requires_repair` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:ai_supply_chain.missing_residual_owner.requires_review` | semantically_reviewed | retain_load_bearing_semantic |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `unresolved_critical_advisory_quarantines_requested_artifact` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `required_unverified_signature_quarantines_artifact` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `complete_requested_artifact_reaches_custody_review` | derived_or_decomposed | semantically_reviewed | retain_load_bearing_semantic |
| `missing_lineage_requires_repair` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_component_inventory_requires_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_revocation_path_requires_repair` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_residual_owner_requires_review` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
