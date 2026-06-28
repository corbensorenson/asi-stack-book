# Source Note: Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer

| Field | Value |
|---|---|
| Source ID | `ext_sparse_moe_2017` |
| Source title | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1701.06538, https://arxiv.org/abs/1701.06538 |
| Citation label | Shazeer et al. (2017), Sparsely-Gated Mixture-of-Experts |
| Published / updated | 2017-01-23 / 2017-01-23 |
| DOI | 10.48550/arXiv.1701.06538 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the routing/MoE literature queue; paper not vendored into this repository and no model or benchmark reproduced. |

## Thesis

This source belongs in the routing and MoECOT chapters as the external origin point for sparsely gated expert layers at large scale. It grounds the book's routing claims in conditional computation without importing the paper's benchmark results as local evidence.

## Mechanisms

- Use conditional computation so only a sparse subset of experts is active per example.
- Route examples through a trainable gating network.
- Increase parameter capacity without proportional compute increase.
- Surface load-balancing, routing overhead, and distributed-training constraints.

## Evidence

- The source reports large-capacity MoE models and language/translation benchmark results in its experimental setting.
- This repository has not reproduced the models, routing code, datasets, cluster setup, or benchmark results.
- Use it as external literature for routing vocabulary and MoE design pressure, not as evidence that ASI Stack routing works.

## Failure Modes

- Expert capacity can be confused with effective intelligence or reliability.
- Gating can collapse, overload experts, or hide routing failures.
- Benchmark gains do not prove governance, readiness, or residual accounting.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `moecot-runtime-and-multi-core-orchestration` (MoECOT Runtime and Multi-Core Orchestration)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)

## Claims To Add Or Update

- Use this note to ground MoE and conditional-computation vocabulary.
- Do not claim local MoE implementation, routing improvement, or reproduced benchmark results.
- Keep support state at `argument` until local routing artifacts, tests, or accepted evidence transitions exist.

## Open Questions

- Which routing fixture should first test expert load, fallback, and residual accounting?
- How should a route ledger record failed or overloaded experts?
- What benchmark boundary separates capacity from governed usefulness?
