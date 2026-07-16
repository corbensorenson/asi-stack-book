# Model-adequacy dossier: Cognitive Compilation obligation refinement

## Ownership

- Chapter: `cognitive-compilation-and-semantic-ir`
- Frozen targets: `lean:cognitive_compilation.ir.operational_invariant`, `lean:cognitive_compilation.ir.failure_blocks_promotion`, `lean:cognitive_compilation.ir.semantic_lowering_route_envelope`
- Stronger model: `lean/AsiStackProofs/CognitiveCompilationRefinement.lean`
- Independent consumer: `scripts/validate_cognitive_compilation_refinement.py`
- Result: `experiments/cognitive_compilation_refinement/results/2026-07-15-local.json`
- Schema: `schemas/cognitive_compilation_refinement.schema.json`
- Support-state effect: exactly `none`

## Reachable model

The state machine moves through raw, source-bound, IR-typed, lowered, validated, repair-required, accepted, and blocked stages. The narrowed model uses one plan identity, three required obligation identities, one source-constraint identity, one target identity, an authority ceiling and approved authority, plan and ledger versions, three receipt flags, residual count, and logical time.

Source binding requires nonzero plan, obligation, and constraint identities and authority within the ceiling. IR typing preserves the complete source tuple and approved authority. Lowering preserves that tuple, binds a nonzero target, and requires declared preservation plus a lowering receipt. Validation preserves source and target, requires prior lowering custody, independently represented preservation, and a validation receipt. A material repair enters repair-required state. Repair can return to validated only when it is localized, preserves the exact affected obligation, consumes the current ledger version, increments that version by exactly one, and carries a ledger receipt. Acceptance preserves source and target, both prior receipts, zero residuals, exact authority, and declared obligation preservation.

## Consequences, countermodels, and consumer

The kernel checks accepted-transition validity, exact source/target preservation at acceptance, exact local repair and versioned-ledger custody, one seven-event repaired acceptance trace, and eight countermodels. The independent consumer implements the same contract separately and rejects 47 single-fault mutations.

The six hand-authored fixtures are consumed at their exact boundary. Two have complete obligation coverage, represented receipt identity, a passing obligation-aware target audit, same-atom observed repair scope, and a ledger reference. Four fail independently because they use whole-graph repair, omit the named lowering receipt, drop an obligation, or treat a syntactic validator pass as semantic preservation. Schema validity alone is never treated as target validity.

## Assumptions, exclusions, and adequacy verdict

Numeric identities, authority, stage, scope, receipt, validator, ledger, and fixture labels are trusted. Three obligation slots are a finite witness, not arbitrary cardinality or graph semantics. The model is sequential and deterministic. It does not inspect natural-language source or target content, calculate dependency closure, observe actual mutations, run a backend, authenticate authority, establish evaluator independence, or execute the artifact.

The model is adequate for the narrowed claim that this exact finite lowering/repair transition system preserves the represented identities and rejects the represented authority, receipt, preservation, repair-scope, ledger, target, and residual faults. It is inadequate for semantic equivalence, obligation completeness, compiler correctness, useful targets, observed locality, natural workloads, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Physically retire the two projection-only declarations while preserving frozen lineage. Retain the twelve original route branches only as bounded negative/residual/acceptance cases. Make the reachable refinement the current owner of the operational and failure targets and a stronger consumer of the route envelope. Promotion requires natural held-out source obligations, an actual backend and target class, independent source-target labels, observed repair/rebuild closure, matched strong baselines, complete cost and failure denominators, reproduction, and transfer.
