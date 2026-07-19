# P2 Deterministic Replacement Queue

Date: 2026-07-17  
State: **metadata-only queue frozen; candidate content and final pool unopened**

The four N0 exclusions in the original 12-task development denominator require
same-language replacements. This receipt freezes the candidate order before any
candidate task text, patch, test command, image outcome, or gold outcome is
opened. It therefore prevents favorable replacement selection while preserving
the final held-out boundary.

The queue is derived only from the pinned post-snapshot metadata universe, the
original development-pool digest, the frozen eligibility rule, and
`sha256(seed + NUL + instance_id)` ordering. Original task identities and
repositories are excluded. A repository may appear at most once across all
slots. Invalid slots are processed in lexicographic original-instance order.

The frozen queue contains 30 unique repositories: nine Rust candidates for the
Rust slot, ten candidates for each of the two Go slots, and the sole eligible
Java repository for the Java slot. Candidate scarcity does not relax the
qualification standard. Each slot must open rank 1 first, retain every failed
attempt, proceed sequentially without outcome-aware skipping, and stop at the
first candidate that passes the complete paired gold-oracle, dual-evaluator,
repeatability, provenance, and resource gates. Failure to fill any slot leaves
the 12-task construct gate closed.

Freezing a queue is not qualifying a task and supplies no evidence about coding
ability, governance, safety, transfer, or the claim-bearing mechanism. The
final held-out pool remains unselected and unopened.

Machine record:
`experiments/p2_governed_repository_admission/corpus/replacement_queue.json`.
