# Model-adequacy dossier: Context Transaction reachable refinement

## Ownership

- Chapter: `context-transactions-snapshots-mounts-and-taint`
- Frozen targets: all four `lean:vcm.transactions.*` targets
- Stronger model: `lean/AsiStackProofs/ContextTransactionRefinement.lean`
- Independent consumer: `scripts/validate_context_transaction_refinement.py`
- Result: `experiments/context_transaction_refinement/results/2026-07-15-local.json`
- Support-state effect: exactly `none`

## Reachable model

The model orders snapshot binding, branch/mount-scoped staging, one-step versioned commit, exact visible read, taint/deletion-governed derivation, and receipt-bound materialization. It carries transaction, snapshot, epoch, branch, mount, cell, authority, committed/visible version, taint, declassification, deletion, replay, audit, evidence-transition, and materialization state.

## Consequences, countermodels, and consumer

Three general consequences establish exact read custody, declassification necessity for represented taint removal, and full receipt custody at materialization. One six-event witness and fifteen countermodels are kernel checked. The independent consumer rejects 78 mutations and consumes both existing fixture families at exactly 3/6 store and 2/4 sequence outcomes. The original validators now require the reachable model rather than copied Lean fixture constants.

## Assumptions, exclusions, and adequacy verdict

Identifiers, policy outcomes, taint/deletion facts, epochs, and receipts are trusted; the model is single-cell, sequential, and deterministic. It is adequate for the exact represented ordering and custody claims. It is inadequate for concurrent serializability or linearizability, distributed clocks/partitions, crash recovery, replay determinism, authentic policy or declassification, actual erasure, deployed storage, side channels, natural workloads, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Retire two assumption bridges, two copied current-result theorems, and two field projections with frozen lineage. Retain the genuine taint/deletion contradictions, priority routes, and non-promotion countermodels as bounded lemmas. Promotion requires an executable concurrent store, prospective isolation model, crash/retry schedules, observed deletion and taint propagation, independent replay, natural workloads, matched baselines, reproduction, and transfer.
