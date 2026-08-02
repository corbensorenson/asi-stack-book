# Cognitive Compilation obligation-refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/CognitiveCompilationRefinement.lean` replaces two assumption-projection declarations with a reachable source-plan-to-target model. State carries exact abstract identities for the plan, three obligations, source constraint, target artifact, authority ceiling and approved authority, plan and repair-ledger versions, lowering/validation/repair receipts, residual count, stage, and logical time.

The eight-event witness binds the source, types the IR, lowers a target, validates it, detects an obligation-invalidating residual, applies a localized obligation-preserving repair with coordinated plan- and ledger-version increments, revalidates the repaired plan version, and accepts the exact target. The 33-theorem refinement proves arbitrary-run source identity, zero support/external-effect authority, valid traces, batch composition, receipt custody, and nondecreasing plan versions. Repair returns to lowering with zero represented residual; acceptance requires validation bound to the current plan version. Eight named closed countermodels retain the original obligation, authority, receipt, validation, repair, version, target, and residual boundaries.

`python3 scripts/validate_cognitive_compilation_refinement.py` independently reimplements the transition relation and recompiles the exact Lean surface. It validates the semantic-atom records, accepts exactly the two intended fixtures, rejects the four expected-invalid fixtures, digest-binds the prior trace receipt, accepts the eight-event witness, and rejects 86 of 86 mutations across source identity, obligation identity, constraints, authority, target identity, plan and ledger versions, receipts, fresh validation, repair scope, residuals, support, effects, and time.

## Exact boundary

This is finite structured-record evidence. Numeric identities establish equality only, not semantic equivalence or obligation completeness. Fixture labels, authority, scope, validator, receipt, and ledger fields remain trusted. The packet does not provide a natural-language source parser, target backend, independent semantic evaluator, actual target-content inspection, compiled execution, measured repair locality, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. It creates no effect, evidence transition, support transition, or release transition.
