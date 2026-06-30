# Source Note: RULER: What's the Real Context Size of Your Long-Context Language Models?

| Field | Value |
|---|---|
| Source ID | `ext_ruler_2024` |
| Source title | RULER: What's the Real Context Size of Your Long-Context Language Models? |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2404.06654, https://arxiv.org/abs/2404.06654 |
| Citation label | Hsieh et al. (2024), RULER |
| Published / updated | 2024-04-09 / 2024-08-06 |
| DOI | 10.48550/arXiv.2404.06654 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the long-context evaluation queue; paper not vendored into this repository and no RULER tasks or model evaluations reproduced. |

## Thesis

RULER belongs in the verification-bandwidth, VCM, context-transaction, and benchmark-ratchet chapters as an external warning that nominal context size and simple retrieval tests can overstate real usable context. It supports the book's need for harder context adequacy tasks without becoming local evidence.

## Mechanisms

- Expand beyond vanilla needle-in-a-haystack retrieval with configurable task length and complexity.
- Include multiple needle variants, multi-hop tracing, and aggregation tasks.
- Evaluate long-context models against tasks intended to stress context use as length and complexity increase.
- Compare claimed context windows against measured task performance in the source setting.

## Evidence

- The source reports synthetic benchmark design and model-evaluation results for long-context stress testing.
- This repository has not run RULER, imported tasks, evaluated any model, or built a VCM/RULER adapter.
- Use this source as external pressure on context-size claims, not as evidence that ASI Stack context systems pass long-context stress tests.

## Failure Modes

- Needle-in-a-haystack success can be mistaken for broad context understanding.
- Context-size marketing can hide degradation as task complexity or input length increases.
- Synthetic tasks can expose failure but still need mapping to real evidence workflows before supporting claim adequacy.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to sharpen the distinction between context window, retrieval success, and context adequacy.
- Do not claim local RULER reproduction, model performance, or VCM stress-test success.
- Keep support state at `argument` until tasks, adapter traces, model runs, and evidence transitions are recorded.

## Open Questions

- Which RULER task families best map to ASI Stack evidence-use failures?
- How should context adequacy records represent multi-hop tracing and aggregation failures?
- What benchmark ratchet prevents a passing simple retrieval task from hiding broader context-use degradation?
