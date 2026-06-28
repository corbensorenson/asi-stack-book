# Source Note: GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding

| Field | Value |
|---|---|
| Source ID | `ext_gshard_2020` |
| Source title | GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2006.16668, https://arxiv.org/abs/2006.16668 |
| Citation label | Lepikhin et al. (2020), GShard |
| Published / updated | 2020-06-30 / 2020-06-30 |
| DOI | 10.48550/arXiv.2006.16668 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the routing/MoE literature queue; paper not vendored into this repository and no distributed training result reproduced. |

## Thesis

GShard belongs in the routing, MoECOT, and resource chapters as an external systems reference for combining sparse expert routing with automatic sharding and large-scale distributed training.

## Mechanisms

- Express parallel computation patterns through annotation APIs and compiler support.
- Scale sparse MoE Transformer models across accelerator clusters.
- Combine conditional computation with automatic sharding.
- Treat routing and model quality as inseparable from communication, compiler, and hardware constraints.

## Evidence

- The source reports multilingual translation model scaling and training results in its setting.
- This repository has not reproduced the sharding system, TPU setup, model, datasets, or quality results.
- Use it as external systems context for routing and orchestration, not as evidence for MoECOT runtime claims.

## Failure Modes

- Distributed scale can hide communication and reliability costs.
- Automatic sharding can be mistaken for governance or readiness.
- Sparse model quality claims cannot be imported without reproduction and residual accounting.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `moecot-runtime-and-multi-core-orchestration` (MoECOT Runtime and Multi-Core Orchestration)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Use this note to compare MoECOT routing with sparse distributed-model systems.
- Do not claim GShard reproduction, TPU-scale training, or local routing performance.
- Keep support state at `argument` until imported artifacts or tests exist.

## Open Questions

- Which ASI Stack route record should include communication cost and sharding constraints?
- How should hardware topology enter readiness gates?
- What residual ledger captures failed sparse-expert routing?
