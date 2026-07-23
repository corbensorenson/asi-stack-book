# Source Note: ATSInfer

| Field | Value |
|---|---|
| Source ID | `ext_atsinfer_2026` |
| Source title | Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2607.10183v2, https://arxiv.org/abs/2607.10183 |
| Ingestion basis | Very recent public arXiv abstract and metadata inspected; full paper, code, and results require later review. |

## Thesis

ATSInfer is a current comparator for moving beyond coarse layer or expert
placement. It proposes tensor-granular static placement plus load-aware dynamic
transfer and asynchronous CPU-GPU coordination on consumer devices.

## Mechanisms

- Place tensors, rather than only whole layers or experts, across CPU and GPU.
- Combine static placement with dynamic transfer under changing load.
- Coordinate CPU and GPU work asynchronously.
- Treat dense and MoE models as separate evaluated cases.
- Optimize prefill and decode behavior separately.

## Evidence

- The July 2026 preprint reports prefill and decode throughput gains on
  representative consumer platforms.
- Only its public abstract and metadata were reviewed here.
- Its recency and preprint status require full-paper review, implementation
  inspection, and independent reproduction before empirical use.

## Failure Modes

- Treating a just-released abstract as settled systems evidence.
- Hidden tensor-level scheduling overhead or instability.
- Dynamic placement decisions that are not replayable.
- Failing to distinguish prefill, decode, dense, MoE, and hardware effects.

## Book Chapters Supported

- `fast-generation-architectures`
- `personal-compute-hives-and-federated-edge-intelligence`
- `resource-economics-and-token-budgets`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Add tensor granularity to the placement taxonomy.
- Require load-aware policies to emit replayable decisions and exact inputs.
- Keep ATSInfer source-reported and provisional until full review.

## Open Questions

- Is code available and sufficiently complete for reproduction?
- How does the scheduler behave under memory pressure and load shift?
- Does tensor granularity outperform competent layer/expert baselines at batch
  size one and under long-context KV pressure?
