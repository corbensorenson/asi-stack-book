# Proof-model dossier: governed-operations-incident-command-and-graceful-degradation

This dossier records the chapter's bounded formal model, consumers, and exact
nonclaims. It is a proof-accounting surface, not operational evidence or a
support transition.

## Targets

| Target | Semantic role | Current disposition |
|---|---|---|
| `lean:operations.degradation_never_widens_authority` | Five-dimensional degraded-authority ceiling | Retain as a finite static invariant |
| `lean:operations.recovery_requires_complete_state` | Declared state/effect/review/expiry recovery gate | Retain as a finite static invariant |
| `lean:operations.incident_lifecycle_refines_static_contracts` | Reachable incident lifecycle and refinement into both static predicates | Retain as a bounded lifecycle refinement |

## Current model

`AsiStackProofs.GovernedOperations` contains the original degradation and
recovery predicates. `AsiStackProofs.GovernedOperationsRefinement` adds eight
reachable stages from normal service through detection, command, containment,
degradation, reconciliation, review, and restoration. Accepted degradation and
restoration are proved to refine the original predicates. Rejected events
preserve exact state; accepted detection disables modeled effects; restoration
requires emergency-authority expiry; and one bounded recurrence returns the
system to incident control. Neither transition execution nor theorem checking
changes support or external-authority counters.

The independently encoded canonical consumer is
`scripts/validate_governed_operations_control_contract.py`. It accepts seven
ordered transitions, checks bounded recurrence, and rejects 44 lifecycle
mutations with exact state preservation, in addition to the existing 18 packet
and 15 campaign mutations.

## Exact boundary

The model assumes that incident observation, containment observation, the
declared state inventory, effect enumeration and disposition, residual
acceptance, verifier independence, fallback qualification, and authority
records are truthful and complete. It does not establish detector quality,
inventory completeness, effect reversibility, fallback usefulness, operator
performance, distributed recovery, bounded harm, operational resilience,
safety, transfer, deployment readiness, release authority, AGI, or ASI.

Those claims remain assigned to the frozen natural campaign and Project
Theseus runtime traces. The formal increment has `support_state_effect=none`.
