# Proof-model dossier: safety-cases-and-structured-assurance

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
| `lean:safety_cases.complete_case.reaches_readiness_review` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.missing_context.retains_draft` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.missing_hazard.requires_case_repair` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.stale_evidence.requires_repair` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.missing_countercase.requires_review` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.missing_independent_review.requires_review` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.unresolved_defeater.blocks_affected_release` | semantically_reviewed | retain_refinement_or_executable_bridge |
| `lean:safety_cases.case_status.cannot_authorize_release` | semantically_reviewed | retain_refinement_or_executable_bridge |

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
| `complete_case_reaches_readiness_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `missing_deployment_context_retains_draft` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `missing_hazard_model_requires_case_repair` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `stale_evidence_dependency_requires_repair` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `missing_countercase_review_requires_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `missing_independent_review_requires_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `unresolved_defeater_requires_accountable_review` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |
| `case_cannot_launder_release_authority` | derived_or_decomposed | semantically_reviewed | retain_refinement_or_executable_bridge |

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
