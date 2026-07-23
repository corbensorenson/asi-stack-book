# Source Note: SpecOffload

| Field | Value |
|---|---|
| Source ID | `ext_specoffload_2025` |
| Source title | SpecOffload: Unlocking Latent GPU Capacity for LLM Inference on Resource-Constrained Devices |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2505.10259v3, https://arxiv.org/abs/2505.10259 |
| Ingestion basis | Public arXiv abstract and metadata inspected; code and reported results not reproduced locally. |

## Thesis

SpecOffload composes weight offloading with speculative decoding by using
otherwise underutilized GPU capacity for a draft model and interleaving target
and draft execution.

## Mechanisms

- Offload target-model weights under a small GPU-memory budget.
- Place and execute a draft model in latent GPU capacity.
- Interleave target and draft model work.
- Plan tensor placement and speculative-decoding parameters jointly.
- Use target verification to accept or reject drafted tokens.

## Evidence

- The paper reports GPU-utilization and inference-throughput gains against its
  selected baseline.
- The result remains source-reported and combines several mechanisms.
- No planner, draft model, acceptance trace, offload pipeline, quality result,
  or throughput result was reproduced.

## Failure Modes

- Calling the method speculative paging when it is speculative decoding
  composed with offloading.
- Crediting offload, draft placement, or scheduling alone for a compound gain.
- Weak draft-model or baseline tuning creating false negatives.
- Ignoring rejection, recovery, and verifier cost.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Add the method as a composition arm, not as evidence for predictive page
  fetch.
- Require acceptance-rate, verifier, placement, and I/O ablations.
- Record draft and target state as separate physical-memory objects.

## Open Questions

- Which component creates the gain under different bandwidth regimes?
- When does a draft model crowd out useful target-model cache?
- How should rollback and cache consistency work after rejected drafts?
