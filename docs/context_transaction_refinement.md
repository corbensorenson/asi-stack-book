# Context Transaction reachable-refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`AsiStackProofs.ContextTransactionRefinement` replaces six assumption, copied-result, or field-projection declarations with reachable snapshot-bind, write-stage, commit, read, derive, and materialize semantics. State preserves exact transaction, snapshot, epoch, branch, mount, cell, version, authority, taint, declassification, deletion, replay, audit, receipt, and logical-time custody.

The six-event witness commits version 1 and reads that exact visible version before deriving and materializing. Lean proves accepted reads preserve snapshot/branch/mount/cell/version and replay custody; an accepted untainted derivation from a tainted source requires declassification authority and receipt; accepted materialization preserves the exact transaction tuple and seven prior receipt classes. Fifteen named countermodels reject missing or stale snapshots, branch/mount substitution, unauthorized mount, uncommitted or skipped-version writes, invisible or stale reads, missing replay, taint laundering, false declassification, open deletion, missing materialization receipt, and support promotion without an evidence transition.

`python3 scripts/validate_context_transaction_refinement.py` independently reimplements the transition relation, consumes the exact three-valid/six-invalid store suite and two-valid/four-invalid sequence suite, accepts the witness, and rejects 78 of 78 mutations.

## Exact boundary

This is finite sequential structured-record evidence. Numeric identities, policies, taint/deletion facts, authority epochs, and receipts remain trusted. It does not establish serializability, linearizability, distributed isolation, crash recovery, replay determinism, deployed storage, deletion erasure, side-channel safety, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.
