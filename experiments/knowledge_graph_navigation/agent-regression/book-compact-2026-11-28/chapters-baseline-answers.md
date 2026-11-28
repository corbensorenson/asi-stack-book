# BC1

The minimum preservation packet carries six coupled records:

1. Authority-bearing IR records the principal, domain, operation, and mutation boundary that survive lowering.
2. The ambiguity ledger records resolved, deferred, and unresolved meanings. A resolution requires a reference.
3. Field lineage traces each source field through semantic IR to the target, recording normalization, splitting, merging, paraphrase, or loss.
4. The pass/failure bundle identifies each pass’s inputs and outputs, the semantic validator it ran, and the failures it retains.
5. Preservation obligations bind source requirements to stable IR nodes, target fields, and validators.
6. The repair receipt records the declared repair scope, actual mutations, and observed blast radius.

A strict route must block or escalate when unresolved or deferred ambiguity affects its interpretation. If lowering drops an authority limit, its field has no preserved source-to-target path, so it fails preservation and cannot be accepted. A pass may carry or narrow granted authority. It cannot create execution or mutation authority or assign a new target owner. This is a design and validation requirement. The section acknowledges that validators can share the compiler’s mistaken interpretation and miss semantic failures. [Chapter 35, §35.7.1, Authority-bearing IR and contract preservation](https://corbensorenson.github.io/asi-stack-book/chapters/cognitive-compilation-and-semantic-ir.html#authority-bearing-ir-and-contract-preservation)

# BC2

- For initially correct requests, use the initially correct cohort as the denominator and measure corruption, meaning a correct candidate is replaced by a wrong one.
- For initially incorrect requests, use the initially incorrect cohort as the denominator and measure repair, meaning extra inference produces a candidate that passes an independent criterion.
- For unresolved requests, use the unresolved cohort as the denominator and measure whether the controller abstains or escrows the residual.

An initially correct answer that bypasses a required independent check counts as an unsafe handoff and earns no successful-release credit. The comparison holds execution authority fixed across deliberation policies and records candidate correctness separately from governance outcomes. These are measurement rules for the comparison. [Chapter 64, §64.13, Deliberation measurement contract](https://corbensorenson.github.io/asi-stack-book/chapters/governed-deliberation-and-test-time-scaling.html#deliberation-measurement-contract)

# BC3

Unresolved within the reading allowance. I located the resource-economics chapter but could not reach its break-even reuse section to verify what the equal-downstream-budget comparison treats as fixed or sunk, what decision the equal-total-budget comparison changes, or whether the source measured the break-even point.

# BC4

Unresolved within the reading allowance. I could not verify Chapter 67’s explanation of the rebound, the measures it calls for tracking after the change, or its rule for a revised denominator.
