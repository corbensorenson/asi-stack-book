# Command semantic-interface refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/CommandSemanticRefinement.lean` replaces the projection-only command-completeness and precedence declarations with a reachable command-boundary model. The model carries an exact root intent and command version; objective, constraint, output-contract, verification, failure-behavior, and authority slots; per-slot provenance and confidence; authority ceiling and approved authority; precedence, planning-validation, approval, dispatch, block, and logical-time custody.

Lean checks that every accepted step satisfies the transition relation, planning validation preserves all six slots and the approved authority, and dispatch requires prior planning validation plus matching authority, approval, and dispatch receipts. A five-event witness reaches `dispatchReady`. Named countermodels reject missing output, hidden-instruction provenance, an applied hidden override, inferred authority, authority widening, constraint substitution, planning without its receipt, and dispatch without its receipt.

`python3 scripts/validate_command_semantic_refinement.py` independently reimplements the transition system. It schema-validates all 13 command records, classifies five command-interface violations, two correct command-interface blocks, and six command-interface-admissible records, binds the nine-trace handoff and nine-scenario/89-event vertical execution results by digest, accepts the five-event witness, and rejects 38 of 38 mutations.

The six interface-admissible records are not treated as whole-fixture successes. Five deliberately fail at downstream ownership boundaries—approval, contract lineage, DAG acyclicity, dispatch receipt, or requirement preservation—and one is the valid linear fixture. This separation prevents command validation from laundering failures owned by other layers.

## Exact boundary

This is finite structured-record evidence. Hash equality is not semantic equivalence. Provenance, confidence, authority, approval, validation, and dispatch labels are trusted inputs, not authenticated extractions. The packet does not establish natural-language parsing, semantic completeness, prompt-injection resistance, deployed dispatch, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. No effect, support transition, evidence transition, or release transition is created.
