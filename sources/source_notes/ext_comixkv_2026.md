# Coordinated Mixed-Precision KV Cache Quantization for Efficient LLM-based Multi-agent Systems

Weizhong Huang, Jinchao Zhang, Xiawu Zheng. [Primary paper, arXiv 2611.10096v1](https://arxiv.org/html/2611.10096v1).

## Mechanism and evidence

Allocate cache precision jointly across agents and layers as new cache blocks are quantized.

Peak cache memory fell from 14.64 to 9.94 GiB in the reported Qwen3-32B setting, while total GPU peak fell from 79.26 to 74.43 GiB.

## Reviewed passage and limits

Figure 4, Qwen3-32B cost comparison. New allocations apply to newly quantized blocks. Aggregate accuracy and memory depend on the agents, workload and model.

## Book Chapters Supported

- `resource-economics-and-token-budgets`
