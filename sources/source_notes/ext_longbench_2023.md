# Source Note: LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding

| Field | Value |
|---|---|
| Source ID | `ext_longbench_2023` |
| Source title | LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2308.14508, https://arxiv.org/abs/2308.14508 |
| Citation label | Bai et al. (2023), LongBench |
| Published / updated | 2023-08-28 / 2024-06-19 |
| DOI | 10.48550/arXiv.2308.14508 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the long-context evaluation queue; paper not vendored into this repository and no LongBench tasks or model evaluations reproduced. |

## Thesis

LongBench belongs in the context and benchmark chapters as an external benchmark reference for long-context understanding across multiple task categories. It helps the ASI Stack distinguish available context length from task-sensitive context understanding, retrieval/compression tradeoffs, and reproducible evaluation design.

## Mechanisms

- Package long-context tasks across single-document QA, multi-document QA, summarization, few-shot learning, synthetic tasks, and code completion.
- Cover English and Chinese datasets under a unified benchmark format.
- Compare models and long-context techniques within the source paper's evaluation setting.
- Treat retrieval and compression as context techniques whose value depends on the task and model being evaluated.

## Evidence

- The source reports benchmark design, dataset coverage, model comparisons, and observed long-context limitations in its own evaluations.
- This repository has not imported LongBench, run any LongBench task, reproduced model comparisons, or validated a VCM benchmark adapter.
- Use this source as external evaluation vocabulary, not as a local benchmark result.

## Failure Modes

- A high nominal context window can still fail task-specific long-context understanding.
- Benchmark coverage can be mistaken for source adequacy if provenance, taint, or claim-specific evidence use is not tested.
- Automatic evaluation can miss failure modes that matter for governed evidence use or reader-facing claims.

## Book Chapters Supported

- `virtual-context-abi` (Virtual Context ABI)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `semantic-pages-context-cells-and-certificates` (Semantic Pages, Context Cells, and Certificates)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to frame long-context benchmark coverage and task diversity.
- Do not claim any ASI Stack model, VCM adapter, or context protocol has passed LongBench.
- Keep support state at `argument` until a public-safe benchmark run or accepted evidence transition exists.

## Open Questions

- Which LongBench task types map cleanly to VCM adequacy states?
- What adapter would preserve source provenance and taint while running long-context benchmarks?
- How should benchmark ratchets prevent one long-context score from becoming a broad context-adequacy claim?
