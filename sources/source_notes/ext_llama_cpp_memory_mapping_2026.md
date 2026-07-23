# Source Note: llama.cpp Memory Mapping and Offload Controls

| Field | Value |
|---|---|
| Source ID | `ext_llama_cpp_memory_mapping_2026` |
| Source title | llama.cpp CLI Memory Mapping, Tensor Placement, and KV Offload Controls |
| Ingestion date | 2026-07-23 |
| Source version / URL | Current official CLI documentation inspected 2026-07-23, https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md |
| Ingestion basis | Official implementation documentation inspected; no local build, model load, or performance run. |

## Thesis

llama.cpp exposes a practical consumer-inference baseline where memory mapping,
DirectIO, host locking, GPU-layer placement, tensor overrides, MoE CPU
placement, KV offload, and KV data type are separate controls.

## Mechanisms

- Memory-map model files or select alternative load modes.
- Use DirectIO where supported.
- Select the number of GPU-resident layers and tensor split behavior.
- Keep some or all MoE weights on the CPU.
- Enable or disable KV offload and choose KV-cache data types.
- Report internal timing when enabled.

## Evidence

- The official CLI documentation establishes the available control surface.
- It explicitly notes pageout and load-time tradeoffs for memory mapping.
- No local llama.cpp build, model, quality test, offload comparison, page-fault
  trace, or throughput measurement was performed.

## Failure Modes

- Comparing configurations without pinning model format, quantization, load
  mode, GPU-layer count, KV type, context, batch, and thermal state.
- Attributing operating-system page-cache behavior to the model architecture.
- Treating memory mapping, KV offload, and weight offload as one mechanism.
- Ignoring that deprecated flags may map to newer load-mode semantics.

## Book Chapters Supported

- `fast-generation-architectures`
- `personal-compute-hives-and-federated-edge-intelligence`
- `resource-economics-and-token-budgets`
- `model-weight-custody-and-hardware-roots-of-trust`

## Claims To Add Or Update

- Use llama.cpp as a current consumer-runtime baseline with an exact CLI/config
  receipt.
- Separate operating-system paging from application-managed model/KV paging.
- Treat quantization and placement as independent experimental factors.

## Open Questions

- Which stable commit and model format should a future comparison pin?
- How can page faults and actual storage reads be captured portably?
- Which DirectIO and mmap combinations are competent on each filesystem?
