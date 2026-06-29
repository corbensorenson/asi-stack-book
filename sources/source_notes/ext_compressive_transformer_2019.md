# Source Note: Compressive Transformers for Long-Range Sequence Modelling

| Field | Value |
|---|---|
| Source ID | `ext_compressive_transformer_2019` |
| Source title | Compressive Transformers for Long-Range Sequence Modelling |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:1911.05507, https://arxiv.org/abs/1911.05507 |
| Citation label | Rae et al. (2019), Compressive Transformers |
| Published / updated | 2019-11-13 / 2019-11-13 |
| DOI | 10.48550/arXiv.1911.05507 |
| Ingestion basis | Public arXiv abstract and metadata inspected for cyclic-memory external positioning; paper not vendored into this repository and no model or benchmark reproduced. |

## Thesis

Compressive Transformers are an external memory-compression comparator for long-range sequence modeling. They help position Coil memory against established attempts to retain or compress past sequence state while keeping ASI Stack structural-contract claims separate from reproduced performance.

## Mechanisms

- Maintain memories of past activations.
- Compress older memories for longer-range sequence access.
- Evaluate long-range language and sequence tasks under a memory-compression architecture.
- Treat memory compression as a separate claim from retrieval quality, authority, freshness, and fallback policy.

## Evidence

- The source reports long-range sequence results, language-modeling benchmarks, and memory-mechanism experiments under its own setup.
- This repository has not reproduced Compressive Transformer training, benchmarks, compression behavior, or downstream task performance.
- Use this source to compare compressed-memory baselines with cyclic-memory contracts and residual/fallback accounting.

## Failure Modes

- Compression can hide residual information loss.
- Long-range memory access can be mistaken for governed context adequacy.
- Benchmark results may not transfer across data, architecture, model size, or evaluation protocol.
- Compression-memory claims need separate stale-read, fallback, and downstream utility checks.

## Book Chapters Supported

- `coil-attention-cyclic-memory-and-recurrence-contracts` (Coil Attention, Cyclic Memory, and Recurrence Contracts)

## Claims To Add Or Update

- Use Compressive Transformers as a source-noted external compressed-memory baseline.
- Keep Coil memory positioned as a structural admission and non-claim layer, not a reproduced long-range memory result.
- Require local compression, stale-read, and utility tests before any stronger memory claim.

## Open Questions

- Should cyclic-memory records include a compressed-memory fallback or comparison field?
- Which residual fields best capture lossy compressed memory in a governed context packet?
- What workload would expose the difference between structural freshness and useful compressed recall?
