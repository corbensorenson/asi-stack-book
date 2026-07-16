# Model-adequacy dossier: safety-case refinement

## Decision

Adequate for one finite authored safety-case record lifecycle with identity custody, typed failure routes, explicit readiness handoff, and descendant-aware invalidation. Inadequate for assurance-argument truth, hazard completeness, causal safety, reviewer independence, release execution, or deployed invalidation.

## Reachable model

Six reachable stages and six events preserve exact case/version, context, claim, hazard, evidence, countercase, reviewer, authority, and residual identity. Thirty routes cover wrong-stage, substitution, replay, authority leakage, missing scope/hazard/argument fields, absent or stale evidence, missing assumptions or countercase work, unresolved defeaters, missing or conflicted review, missing acceptance/residual/authority records, authority laundering, and incomplete affected-path or descendant invalidation.

The readiness route is a handoff only. The invalidation route returns a readiness-bound case to the challenged stage; it cannot preserve the old readiness status while changing the evidence lineage.

## Countermodels and consumer

The Lean module proves state preservation on rejection, one-receipt advancement, zero support/external-effect assignment, six concrete countermodels, and a complete lifecycle/invalidation witness. The independently implemented Python consumer reruns the inherited eight-case suite, covers all 30 routes, and rejects 35/35 binding, lifecycle, replay, authority, defeater, review, and invalidation mutations.

## Assumptions, exclusions, and adequacy verdict

The model trusts authored identifiers, booleans, digests, reviewer and authority labels, affected paths, and the assertion that descendant invalidation is complete. It does not prove that a claim is meaningful, hazards are complete, evidence is true or causally relevant, reviewers are competent or independent, controls work, residual owners can act, invalidation reached a live consumer, or a system is safe. It executes no release or external effect and assigns no support state. Support-state effect: exactly `none`.
