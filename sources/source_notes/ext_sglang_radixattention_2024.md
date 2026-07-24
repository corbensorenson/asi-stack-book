# Source Note: SGLang and RadixAttention

| Field | Value |
|---|---|
| Source ID | `ext_sglang_radixattention_2024` |
| Source title | SGLang: Efficient Execution of Structured Language Model Programs |
| Ingestion date | 2026-07-23 |
| Source version / URL | NeurIPS 2024 paper and arXiv:2312.07104v2, https://papers.nips.cc/paper_files/paper/2024/hash/724be4472168f31ba1c9ac630f15dec8-Abstract-Conference.html |
| Ingestion basis | Primary conference paper inspected; no code or benchmark reproduced. |

## Thesis

Structured multi-call language-model programs expose shared prefixes across
requests and branches. A radix-tree KV cache plus cache-aware scheduling can
reuse that structure across a workload rather than optimizing each call alone.

## Mechanisms

- RadixAttention stores reusable KV state in a radix tree over token sequences.
- Cache-aware scheduling favors requests with shared prefixes.
- Reference counting and eviction manage shared state.
- Frontend structure exposes generation, branching, and parallelism to the runtime.

## Evidence

The paper reports workload throughput gains and gives a bounded scheduling
argument under stated cache assumptions. Those results and assumptions have not
been reproduced here.

## Failure Modes

- A scheduling theorem can stop applying when request arrivals, memory limits,
  fairness, deadlines, or cache costs differ.
- Prefix-favoring order can starve unrelated or urgent work.
- Shared state can cross tenant or authority boundaries.
- Throughput can improve while tail latency or useful outcomes worsen.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Treat cache-aware scheduling as a workload policy, not a local lookup detail.
- Measure fairness, tails, admission, and eviction alongside aggregate throughput.
- Preserve the exact assumptions of any scheduling optimality statement.

## Open Questions

- What fairness and deadline constraints should override prefix locality?
- How should reusable branches be partitioned across workers and tenants?
- When does cache-aware batching hurt interactive traffic?
