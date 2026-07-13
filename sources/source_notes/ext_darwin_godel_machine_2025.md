# Source Note: Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents

| Field | Value |
|---|---|
| Source ID | `ext_darwin_godel_machine_2025` |
| Source title | Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents |
| Ingestion date | 2026-07-10 |
| Source version / URL | Preprint, https://arxiv.org/abs/2505.22954 |
| Citation label | Zhang et al. (2025), Darwin Godel Machine |
| Published / updated | 2025-05-29 / 2026-03-12 |
| Ingestion basis | Full ICLR 2026 paper reviewed for archive-based parent selection, self-modifying coding-agent repositories, benchmark evaluation, compile/edit eligibility, open-ended and no-self-improvement baselines, branching lineage, transfer, compute cost, sandbox and network limits, rollback/audit framing, safety discussion, and stated limitations. No code evolution run, model call, sandbox, benchmark result, or agent was imported. |

## Thesis

Darwin Gödel Machine is an empirical, archive-based coding-agent
self-modification system. It samples a parent, uses a foundation model to
modify that agent's own repository, evaluates the child on coding benchmarks,
and keeps eligible variants in a branching archive whose lower-scoring stepping
stones may later produce stronger descendants.

## Mechanisms

- Select parents approximately by performance and underexplored branching,
  then record child code and evaluation lineage rather than overwriting a
  single current agent.
- Admit only children that compile and retain basic codebase-editing ability;
  the paper discards failures outside that eligibility boundary.
- Compare the full system with a fixed modifier lacking iterative
  self-improvement and with a latest-version path lacking archive-based
  open-ended exploration.
- Run agents inside isolated sandboxes with time/resource limits, restricted
  network and host access, and self-modification bounded to the agent codebase
  and harnesses; retain an auditable archive for rollback and analysis.

## Evidence

- The paper reports source-scoped improvements on SWE-bench and Polyglot, model
  transfer checks, and ablation evidence for self-improvement and archive-based
  exploration. Those results rely on coding benchmarks as a proxy for coding
  and future self-modification ability.
- A run reportedly takes roughly two weeks and substantial API cost, and the
  discovered systems remain below closed-source state of the art in the stated
  comparison.
- Benchmark gains do not establish monotonic general improvement, safety,
  preserved authority, local reproduction, or permission to self-modify.

## Failure Modes

- Selecting changes against a narrow benchmark and misreading the result as broadly beneficial.
- Giving an improving system standing authority beyond its evaluated and reversible boundary.
- The archive discards children that fail compile/edit eligibility, so a
  governed archive needs retained failure receipts rather than survivorship by
  construction.
- Optimization can amplify vulnerabilities or opaque logic when benchmarks omit
  robustness, interpretability, security, or wider social objectives.
- Sandboxing and post-hoc audit narrow execution risk but do not independently
  establish that each modification is beneficial or aligned.

## Book Chapters Supported

- `recursive-self-improvement-boundaries`
- `open-ended-improvement-engines`
- `readiness-gates-residual-escrow-and-quarantine`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Use as a comparator for branching archive lineage, empirical selection,
  stepping stones, self-modification under a fixed exploration process,
  sandbox/resource boundaries, and rollback/audit records.
- Preserve the paper's benchmark-proxy assumption, discarded-child boundary,
  costs, fixed exploration controller, and undeployed status.

## Open Questions

- Which source details define the sandbox, evaluator, and archive boundaries needed for a faithful controlled comparison?
