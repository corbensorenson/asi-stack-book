# Descriptive transcript — Context Transactions, Snapshots, Mounts, and Taint

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/context-transactions-snapshots-mounts-and-taint.html>

Video ID: `asi-video-context-transactions-snapshots-mounts-and-taint`

Lifecycle: local pilot; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:42 — Context becomes state

**Visual description.** Loose snippet cards from a store, graph, cache, and
summary initially overlap. They resolve into one transaction boundary with a
visible pre-state and a causally ordered post-state.

**Narration.** Long-lived AI systems do not merely retrieve context. They mutate durable memory through stores, branches, indexes, caches, summaries, replicas, and recovery paths. A clean-looking prompt can still come from a mixed snapshot, an uncommitted write, a stale index, a foreign branch, or a derivative whose source was revoked. This chapter treats context as accountable state. A Context Transaction binds the principal, purpose, operation, base snapshot, branch, mounts, authority, rights, isolation, durability, budget, and support ceiling to the actual pre-state and every attempted, applied, visible, replayed, recovered, or indeterminate post-state.

## 00:42–01:24 — Exact snapshot and mounts

**Visual description.** A vertical snapshot spine lists object versions,
content and index epochs, causal parents, branch, provenance, taint, leases,
caches, backups, and obligations. Beside it, separate permission gates say
read, write, derive, delete, export, train, and execute.

**Narration.** The transaction begins with an observed snapshot, not a friendly name or timestamp. It binds exact object versions, content and index epochs, causal parents, branch, mount policy, provenance, taint, leases, caches, backups, and open obligations. The request declares intended reads, writes, derivations, deletions, and revocations, but the receipt records what actually happened. Purpose-bound mounts distinguish read, write, derive, delete, share, export, train, and execute permission. No cache, summary, branch, replica, or restore route may widen that envelope.

## 01:24–02:05 — Commit lifecycle

**Visual description.** A state machine advances from requested to admitted,
prepared, applied, durable, visible, replayed, and recovered. Abort and
indeterminate branch downward. Independent observation sits beside the log.

**Narration.** Commit is a lifecycle, not a success boolean. Requested, admitted, prepared, applied, durably committed, consumer-visible, replayed, recovered, compensated, aborted, and indeterminate are different states. Content, indexes, provenance, taint, rights, derivative edges, deletion obligations, caches, and audit references commit atomically only inside the declared boundary. Conflicts, lost updates, write skew, stale indexes, retry duplicates, partial writes, and uncertain participants remain explicit. Crash recovery must return to the declared durable frontier and compare independently observed state after restart.

## 02:05–02:50 — Correction, conflict, and closure

**Visual description.** Snapshot 41 branches into B and C. A corrected source
on B derives a summary, embedding, cache entry, and route. A conflict blocks
merge. Taint labels propagate along every derivative edge. Deletion reaches
live descendants but an unreachable backup remains in a magenta residual loop.

**Narration.** Consider a source correction on branch B. A transaction reads snapshot forty-one through a purpose-bound mount, writes a corrected object, derives a summary and embedding, and invalidates an exact response cache. A concurrent branch changes the same semantic object, so silent last-writer-wins is forbidden. The transaction rebases or preserves both branches. Taint from the corrected source follows the summary, embedding, cache key, and downstream route. If deletion is later requested, closure walks live objects, indexes, caches, replicas, exports, and backups. An unreachable backup remains an owned residual; it cannot be relabeled as physical erasure or model forgetting.

## 02:50–03:32 — Cache taxonomy

**Visual description.** Three lanes compare prefix-state reuse, exact response
memoization, and semantic response reuse. The semantic lane passes through an
approximation gate and a risk policy; a receipt discloses the chosen lane.

**Narration.** Caching makes the distinction especially important. Prefix caching reuses compatible model state and still produces a new answer. Response caching returns a prior answer. An exact response key therefore closes over request, consumer, model, decoding, tools, sources, schema, locale, time, authority, purpose, policy, rights, side-effect state, verifier, and dependency versions. A semantic cache weakens the match further: similarity is only an approximate route candidate. Dynamic facts, personalized decisions, high-impact advice, security actions, rights-sensitive material, and side-effecting operations normally require fresh evaluation. Every hit discloses whether compatible prefill or a prior answer was reused.

## 03:32–04:18 — Evidence and failure ceiling

**Visual description.** Finite evidence cards show `3 valid / 6 invalid store
fixtures`, `2 valid / 4 invalid sequences`, and `78 / 78 mutations rejected`.
Concurrency, serializability, crash-safe deployed storage, complete erasure,
and useful memory remain outside a double scope boundary.

**Narration.** This design can still become transaction theater. A perfect log may describe bytes that never became durable. A database can protect records without preserving semantic identity, taint, or erasure categories. Deleting storage does not establish behavioral forgetting, influence removal, privacy protection, or removal from external descendants. The strongest current checks are finite: three valid and six invalid store fixtures, two valid and four invalid event sequences, seventy-eight rejected mutations, and one bounded historical-project lifecycle. They establish record and route consequences, not concurrency, serializability, crash-safe deployed storage, complete invalidation, or useful memory.

## 04:18–05:00 — Boundary and handoff

**Visual description.** The end card states `argument`, gives the maximum
finite POMDP inference, and places “valid transition” before a separate gate
labeled “adequate evidence.” It points to Verification Bandwidth and Context
Adequacy.

**Narration.** The core remains Design rationale at argument support and blocked after a full attempt. Its maximum inference is a bounded finite partially observed world-model result only—no open-world truth, general memory transfer, deployment, or chapter-core promotion. A valid context transaction says which state transition occurred within its declared boundary. It does not say that the context is true, sufficient, safe, or useful. The next chapter, Verification Bandwidth and Context Adequacy, asks that separate question: whether the system has enough evidence, tools, comparisons, contradiction search, and reviewer capacity to justify the claim it wants to make.

## Source and evidence boundary

The visual binds all chapter-assigned source IDs but reproduces none of their
systems or reported results. It is an explanatory derivative with zero support
effect.
