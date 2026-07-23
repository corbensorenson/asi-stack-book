# Source Note: vAttention

| Field | Value |
|---|---|
| Source ID | `ext_vattention_2025` |
| Source title | vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2405.04437v3 / ASPLOS 2025, https://arxiv.org/abs/2405.04437 |
| Ingestion basis | Public arXiv abstract and metadata inspected; paper, CUDA implementation, and benchmarks not reproduced locally. |

## Thesis

vAttention is the required counterpoint to treating a non-contiguous KV layout
as the universal answer. It decouples virtual and physical GPU memory while
preserving contiguous KV virtual addresses.

## Mechanisms

- Reserve contiguous virtual address space for KV state.
- Dynamically map physical GPU memory with CUDA virtual-memory APIs.
- Mitigate physical fragmentation without changing the virtual KV layout.
- Preserve compatibility with multiple attention kernels.
- Add LLM-specific mitigations for CUDA virtual-memory limitations.

## Evidence

- The source reports serving-throughput improvements over selected
  PagedAttention-based configurations.
- The result is API-, kernel-, framework-, workload-, and hardware-specific.
- No CUDA VMM, attention-kernel, fragmentation, or throughput result was run.

## Failure Modes

- Assuming OS-inspired block paging is always lower overhead.
- Ignoring kernel compatibility and virtual-memory API costs.
- Comparing one kernel/layout pair to another without matched serving policy.
- Treating lower fragmentation as model-quality evidence.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Keep contiguous-virtual and non-contiguous-block KV designs as live
  alternatives.
- Require kernel/layout/framework identity in every cache result.
- Prevent PagedAttention from becoming an unquestioned architectural default.

## Open Questions

- How do both designs behave under host or SSD spill?
- Which API and kernel combinations remain portable beyond CUDA?
- What isolation and stale-page checks are required for shared KV state?
