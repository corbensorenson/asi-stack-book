# Forward-transfer factorial follow-up

Protocol dated 2026-11-20. This CPU-only follow-up asks whether descriptive
selection, library representation, or their interaction explains a local
retrieval advantage. The first pilot compared a query-aware whole-program arm
with a query-blind routine arm. This study crosses the two decisions. It uses
fresh five-bit maps and a new historical corpus. Differences across the two
studies also reflect different cases, budgets, and task width.

## Fixed interventions

For each historical group, the whole entry is its first archive program by ID.
The routine is its most frequent adjacent two-operation subsequence, breaking
ties lexically. The archive supplies two programs per group. Both
representations use the same six groups and their combined description
terms. The query-aware policy ranks groups by token Jaccard similarity and
breaks ties by group ID. The query-blind policy ranks the same groups using
SHA-256 of task ID and group ID and never reads the description. Each
library arm gets exactly two distinct operators. The no-library arm gets
only the same seven primitives.

Evaluate every task twice, once with a descriptive query and once with
neutral wording. In each case cross forward and reversed primitive order
with forward and reversed library order. The no-library arm is repeated in
the same design cells and supplies a paired comparator. These deliberate
changes measure ordering and description sensitivity. Repeated cells are
not independent tasks.

## Budgets, checking, and scoring

The first resource regime permits 96 candidate proposals. The second permits
1,450 executed primitive steps across screening and full verification. When
the next screen or full check would exceed its cap, stop the deterministic
queue. Queue insertion and retrieval work are counted separately. All arms
share the same screening inputs, expanded-program deduplication, search
order within a condition, and independent exhaustive bit-string interpreter.
Check all 32 inputs for candidates that match the visible examples. Count
all steps in those checks. Save false matches, checked prefixes, selected
operators, expanded solutions, and every exhausted or failed case.

Validate known good and bad programs, completeness of library arms, and
disjoint historical and later truth vectors before opening results. The
adverse family uses operations outside the expected strengths of the library.
An exhausted budget gives no proof that its target is unreachable. A
calibration failure invalidates outcome reporting.

Report exact paired counts by budget and description, signed differences by
task family, and how often a success depends on ordering. Summarize the
query-aware benefit separately for each representation and the representation
benefit separately for each selection rule. The sign may differ. Report
proposal counts, expanded screening and verification work, indexing and
retrieval effort and optional measured CPU separately. This fixed collection
does not estimate a natural workload probability or general model advantage.
Advance a specific reuse assumption only if its paired evidence is favorable
under both resource regimes and no adverse tradeoff overturns it.

## Calibration amendment

The first lock at commit `2dc1d19b` stopped before any paired search. The
target vector for `b22` was equivalent to historical programs `h22` and
`h28`. The vector for `d21` matched `h30`. The other four calibration
checks passed. Replace the duplicated targets with the flagged and
twice-rotated variants now specified in the oracle. Keep both task IDs and
family assignments. This amendment changes neither search nor prior
definitions and precedes opening any outcomes. Retain the failed gate as
an instrument preparation event.
