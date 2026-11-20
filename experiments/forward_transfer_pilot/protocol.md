# Forward-transfer pilot on finite word transformations

Protocol date 2026-11-20. The author paper proposes evaluating the marginal
contribution of a reusable routine on later task lineages. This pilot tests
a narrow CPU-only encoding of that idea. The tasks transform four-bit words.

## Prospective design

Earlier programs and task descriptions are in `history.json`. Three later
families of independently specified word maps and one deliberately adverse
family are in `heldout.py`. Their input decisions are frozen before running
the study. Held-out task IDs and family names have no overlap with training
lineages. The harness rejects a held-out map whose full output vector exactly
matches an earlier program or another held-out map. These are authored
finite functions and source groups, so lineage separation is by fixture
construction. There is no random sample from natural program synthesis.

The three arms share primitive semantics, breadth-first search, queue order,
example locations, full-domain verifier, and a cap of 96 proposed programs per
task. No-library starts with the seven primitive operators. Ordinary retrieval
selects up to two complete earlier programs using token-set Jaccard similarity
over the task descriptions. The routine arm selects up to two adjacent
two-operator subsequences from earlier programs. A subsequence must occur in
at least two historical lineages. Rank by repeated occurrences, then lexical
order. Both reuse arms may compose their two supplied operators with
primitives. A prior exact solution and an extracted routine both occupy one
grammar operator. Log expanded primitive length separately from search cost.
The library is frozen across test tasks. No arm adds test results to it.

Search sees the same eight input-output pairs in every arm. The independent
checker implements the seven word transformations with bit strings and checks
all sixteen inputs against reference functions written as formulas. A
candidate that passes the visible examples but fails the full check is
recorded and search continues. Report verified, budget-exhausted, and
counterexample outcomes for every task. Verify a known good and known bad
candidate before running the study. A failed calibration or lineage audit
invalidates the result.

Report per-arm and per-case candidate attempts, expanded primitive evaluations
on visible examples, full-check calls and expanded primitive evaluations in the
checker, setup work (historical programs indexed, adjacent patterns examined,
retrieval similarities scored) and expanded solution length. Log process CPU
time for setup, retrieval, proposal generation and screening, and full
verification separately as machine-dependent diagnostics. Report paired
outcomes by family with all failed cases and equal-budget limits visible. The
cap matches candidate search opportunities. Extra setup and verification work
are measured rather than silently treated as free. The diagnostic CPU timer
charges all search work including queue management and bookkeeping.

A result in which the routine arm verifies more held-out tasks than both
comparators supports a benefit only for this corpus, search and budget.
A tie leaves a cheaper route preferable on this denominator. Cross-family
losses or higher full-check burden narrow the admission claim. This is an
internal synthetic pilot. It supplies neither a production adoption measure
nor evidence about scaling or general program-synthesis performance.
