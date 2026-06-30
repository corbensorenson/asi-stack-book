# Source Note: Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity

| Field | Value |
|---|---|
| Source ID | `ext_switch_transformer_2021` |
| Source title | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2101.03961, https://arxiv.org/abs/2101.03961 |
| Citation label | Fedus et al. (2021), Switch Transformers |
| Published / updated | 2021-01-11 / 2022-06-16 |
| DOI | 10.48550/arXiv.2101.03961 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the routing/MoE literature queue; paper not vendored into this repository and no model result reproduced. |

## Thesis

Switch Transformers belongs in the routing and resource chapters as an external reference for simplifying MoE routing and exposing the practical constraints of sparse activation: communication, stability, precision, and speed claims.

## Mechanisms

- Route each token or example to a simplified expert choice.
- Keep computational cost bounded while increasing parameter count.
- Address communication cost and training instability in sparse expert models.
- Report pretraining speed and multilingual transfer results in the source setting.

## Evidence

- The source reports sparse-model scale and speed results.
- This repository has not reproduced training, data, precision behavior, routing stability, or benchmarks.
- Use it as external literature for routing design and cost accounting, not as evidence that ASI Stack routes are efficient.

## Failure Modes

- Sparse activation can become a scale story without route-quality evidence.
- Instability and communication overhead can erase theoretical efficiency.
- Speed claims can be over-read into intelligence or governance claims.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to source sparse routing and simplified expert-selection vocabulary.
- Do not claim local Switch Transformer reproduction or sparse-router performance.
- Keep support state at `argument` until routing harnesses or accepted evidence transitions exist.

## Open Questions

- What test separates route efficiency from route adequacy?
- Which cost ledger should include communication overhead and precision constraints?
- How should sparse-router regressions be preserved?
