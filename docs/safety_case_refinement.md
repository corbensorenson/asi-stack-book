# Safety-case lifecycle refinement

**State:** finite authored lifecycle validated; no chapter-core support change.
**Receipt:** `experiments/safety_case_refinement/results/2026-07-15-local.json`

The refinement replaces isolated Boolean route reductions with a reachable six-stage case lifecycle: draft, scoped, evidenced, challenged, reviewed, and readiness-bound. Exact case/version, context, claim, hazard, evidence, countercase, reviewer, authority, and residual identities remain bound across each accepted event. A readiness-bound case can be invalidated only with a cause, affected-path record, and complete descendant invalidation; that event returns the case to challenge rather than silently preserving its prior status.

The independently implemented Python consumer preserves the existing eight-case assurance suite, exercises all 30 lifecycle routes, and rejects 35/35 identity, stage, replay, authority-leak, missing-field, unresolved-defeater, review-conflict, and incomplete-invalidation mutations. The full witness emits six receipts, one readiness handoff, one invalidation, zero support assignments, and zero external effects.

This is versioned record and invalidation discipline. It does not establish hazard completeness, evidence truth or adequacy, reviewer competence or independence, control effectiveness, safety, readiness, release authority, effect execution, deployed descendant invalidation, or transfer. Support-state effect is exactly `none`.
