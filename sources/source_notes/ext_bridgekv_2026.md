# BridgeKV: Large-Model Prefill and Small-Model Decoding for LLM Inference via KV Cache Translation

Payman Behnam, Debopam Sanyal, Pranav Ponnusamy, Kusum Meda Ravi, Pranav Sastry, Mani Chandana Bandaru, Alind Khare, Myungjin Lee, Alexey Tumanov. [Primary paper, arXiv 2611.11761v1](https://arxiv.org/pdf/2611.11761v1).

## Mechanism and evidence

A large model processes the prompt, a learned map translates its attention cache, and a small model decodes.

The 8B-to-1B route measured 3.0× faster requests on one A40 relative to the larger model. The 70B-to-1B serving estimates came from simulation.

## Reviewed passage and limits

Single-A40 measurements and separate serving simulation. The smaller decoder changes the output behavior. Quality, transfer costs and request latency need comparison on the same prompt mix.

## Book Chapters Supported

- `fast-generation-architectures`
