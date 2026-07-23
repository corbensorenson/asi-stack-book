# Source Note: LLM in a Flash

| Field | Value |
|---|---|
| Source ID | `ext_llm_in_flash_2024` |
| Source title | LLM in a Flash: Efficient Large Language Model Inference with Limited Memory |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2312.11514v3 / ACL 2024, https://arxiv.org/abs/2312.11514 |
| Ingestion basis | Public arXiv abstract and metadata inspected; full paper and implementation not reproduced locally. |

## Thesis

The paper frames flash-backed inference as a hardware-aware data-movement
problem: reduce the bytes transferred and shape reads into larger contiguous
chunks instead of naively loading parameter fragments.

## Mechanisms

- Build an inference cost model around flash characteristics.
- Keep parameters in flash and bring them to DRAM on demand.
- Reuse previously activated neurons through windowing.
- Bundle rows and columns to increase contiguous read size.
- Combine sparsity awareness, context-adaptive loading, and hardware-aware
  layout.

## Evidence

- The source reports model-size and speed improvements against its naive loading
  baselines in CPU and GPU settings.
- These remain paper-reported results and include sparsity-aware mechanisms.
- No flash-layout, sparse-loading, accuracy, latency, or energy result was
  reproduced here.

## Failure Modes

- Treating selective neuron loading as an exact dense paging result.
- Ignoring device-specific random/sequential read behavior.
- Comparing against an intentionally naive loader instead of a strong current
  runtime.
- Omitting conversion, layout, duplicate-storage, and recovery cost.

## Book Chapters Supported

- `fast-generation-architectures`
- `personal-compute-hives-and-federated-edge-intelligence`
- `resource-economics-and-token-budgets`
- `model-weight-custody-and-hardware-roots-of-trust`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Require a hardware-specific I/O cost model.
- Measure bytes transferred and read contiguity, not only VRAM.
- Separate sparse/context-adaptive loading from exact layer streaming.

## Open Questions

- Which contemporary model families expose stable exploitable activation
  locality?
- How robust are windowing and bundling under distribution shift?
- What layout and custody rules apply to transformed flash artifacts?
