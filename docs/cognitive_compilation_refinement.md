# Cognitive Compilation obligation-refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/CognitiveCompilationRefinement.lean` replaces two assumption-projection declarations with a reachable source-plan-to-target model. State carries exact abstract identities for the plan, three obligations, source constraint, target artifact, authority ceiling and approved authority, plan and repair-ledger versions, lowering/validation/repair receipts, residual count, stage, and logical time.

The seven-event witness binds the source, types the IR, lowers a target, validates it, detects an obligation-invalidating repair, applies a localized obligation-preserving repair with a ledger-version increment, and accepts the exact target. Lean proves that accepted target transitions preserve the plan, three obligations, constraint, and target identity, and that accepted repairs require local scope, exact before/after obligation identity, a one-step ledger increment, and a repair receipt. Eight named countermodels reject obligation substitution, authority widening, missing lowering receipt, validator/preservation laundering, global repair, unversioned repair, target substitution, and residual-bearing acceptance.

`python3 scripts/validate_cognitive_compilation_refinement.py` independently reimplements the transition relation. It validates the semantic-atom records, accepts exactly the two intended fixtures, rejects the four expected-invalid fixtures, digest-binds the prior trace receipt, accepts the seven-event witness, and rejects 47 of 47 mutations across source identity, obligation identity, constraints, authority, target identity, receipts, validation, repair scope, ledger custody, residuals, and time.

## Exact boundary

This is finite structured-record evidence. Numeric identities establish equality only, not semantic equivalence or obligation completeness. Fixture labels, authority, scope, validator, receipt, and ledger fields remain trusted. The packet does not provide a natural-language source parser, target backend, independent semantic evaluator, actual target-content inspection, compiled execution, measured repair locality, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. It creates no effect, evidence transition, support transition, or release transition.
