## BC1

The preservation packet carries six records:

1. **Authority-bearing IR** records the principal, domain, operation, and mutation boundary that survive lowering.
2. **Ambiguity ledger** tracks resolved, deferred, and unresolved meanings and their consequences for strict compilation.
3. **Field lineage** maps every source field through the IR to the target and records how it changed or whether it was lost.
4. **Pass/failure bundle** retains the pass input and output, the semantic validator that ran, and earlier failures.
5. **Preservation obligations** bind source requirements to stable IR nodes, target fields, and validators.
6. **Repair receipt** records the declared repair scope, actual changes, and observed blast radius.

An unresolved or deferred ambiguity blocks or escalates a strict route when the meaning matters to that route. A missing authority limit breaks the required source-to-IR-to-target lineage and the strict route cannot accept the lowering as preserving the contract. Passes may carry or narrow the source grant. Acceptance depends on validation of the relevant target field. The packet makes preservation inspectable and exposes failures, with semantic adequacy still subject to the validator's coverage. [§35.7.1, Authority-bearing IR and contract preservation](https://corbensorenson.github.io/asi-stack-book/chapters/cognitive-compilation-and-semantic-ir.html#authority-bearing-ir-and-contract-preservation)

## BC2

Use three separate denominators based on the starting state:

- **Initially correct** measures corruption, when deliberation replaces a correct candidate with a wrong one.
- **Initially incorrect** measures repair, when extra compute produces a candidate that passes an independent criterion.
- **Unresolved** measures honesty, when the controller abstains or escrows the residual.

Count an initially correct answer released through a bypass of its required independent check as an **unsafe handoff**. Its correctness does not qualify it as a successful release. The comparison applies matched authority with the same execution requirements across arms. [§64.13, Deliberation measurement contract](https://corbensorenson.github.io/asi-stack-book/chapters/governed-deliberation-and-test-time-scaling.html#deliberation-measurement-contract)

## BC3

Equal-downstream-budget testing fixes the downstream budget, freezes the reusable library, and treats its construction as sunk. It asks whether reuse helps under those conditions. Equal-total-budget testing charges construction and maintenance to the candidate and asks whether the full system is preferable. The decision depends on the task volume or time horizon over which cumulative savings, if any, exceed fixed and continuing costs. The evidence I could read specifies this comparison and the reporting requirement. Whether the source measured the break-even point remains unresolved in the available excerpt. [§66.8.3, Price reuse over its break-even horizon](https://corbensorenson.github.io/asi-stack-book/chapters/resource-economics-and-token-budgets.html#price-reuse-over-its-break-even-horizon)

## BC4

Lower joules per token reduces energy intensity. Lower unit cost can also drive enough additional demand or utilization to raise total burden, and burdens can shift beyond the measured workload. A short window can capture the initial saving and miss the rebound. After an efficiency change the book would track utilization, model size, demand, cost, and shifted work long enough to detect rebound, with marginal and total impacts reported separately. A revision preserves the prior estimate and explains every denominator change. The cited external estimates and scenarios provide methodological grounding, with validation of project meters and rebound estimates still open. [§67.8.7, Metering, allocation, uncertainty, and rebound](https://corbensorenson.github.io/asi-stack-book/chapters/physical-compute-infrastructure-energy-and-environmental-constraints.html#metering-allocation-uncertainty-and-rebound)
