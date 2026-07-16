# Proof-model dossier: security-kernel-and-digital-scifs

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:security.scif.operational_invariant` | terminally_dispositioned | replace_with_stronger_model |
| `lean:security.scif.failure_blocks_promotion` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:security.scif.route_envelope` | semantically_reviewed | retain_load_bearing_semantic |
| `lean:security.scif.commit_probe_bridge` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `secret_substitution_requires_authorized_boundary` | direct_or_projection | terminally_dispositioned | retire_projection_or_assumption_restatement |
| `insufficient_clearance_blocks_protected_scif_entry` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_handle_denies_authority_use` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `revocation_request_revokes_handle` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `inactive_lease_denies_authority_use` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_approval_requests_approval` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `unauthorized_boundary_denies_authority_use` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_secret_substitution_permission_denies_authority_use` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `insufficient_clearance_denies_authority_use` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `prompt_injection_records_leak_residual` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `missing_required_scif_routes_to_scif_spawn` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `unsanitized_output_routes_to_sanitization` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `residual_risk_records_leak_residual` | derived_or_decomposed | semantically_reviewed | retain_countermodel_or_negative_case |
| `clean_authorized_use_is_allowed` | derived_or_decomposed | semantically_reviewed | retain_reusable_lemma |
| `scif_commit_secret_output_blocks_commit` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_handle_output_blocks_commit` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_missing_zeroize_blocks_commit` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_overbroad_context_blocks_commit` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_inactive_approval_blocks_commit` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_missing_residual_blocks_commit` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_prompt_injection_routes_to_sanitized_refusal` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `scif_commit_clean_sanitized_output_commits_summary` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
