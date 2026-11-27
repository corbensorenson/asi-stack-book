# Coordinated Mixed-Precision KV Cache Quantization for Efficient LLM-based Multi-agent Systems

| Field | Value |
|---|---|
| Source ID | `ext_comixkv_2026` |

Weizhong Huang, Jinchao Zhang, Xiawu Zheng. [Primary paper, arXiv 2611.10096v1](https://arxiv.org/html/2611.10096v1).

## Thesis

The value of cache precision depends on which agent and layer consume the available memory.

## Mechanisms

Allocate cache precision jointly across agents and layers as new cache blocks are quantized.

## Evidence

Peak cache memory fell from 14.64 to 9.94 GiB in the reported Qwen3-32B setting, while total GPU peak fell from 79.26 to 74.43 GiB.

## Failure Modes

Figure 4, Qwen3-32B cost comparison. New allocations apply to newly quantized blocks. Aggregate accuracy and memory depend on the agents, workload and model.

## Book Chapters Supported

- `resource-economics-and-token-budgets` — [Which memory saving can fund another job?](../../chapters/resource-economics-and-token-budgets.qmd#which-memory-saving-can-fund-another-job)

## Claims To Add Or Update

Use peak device memory as the capacity measure when deciding whether the next agent fits.

## Open Questions

Do the savings persist for a long-lived agent whose older cache blocks retain their original precision?
