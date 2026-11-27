# BridgeKV: Large-Model Prefill and Small-Model Decoding for LLM Inference via KV Cache Translation

| Field | Value |
|---|---|
| Source ID | `ext_bridgekv_2026` |

Payman Behnam, Debopam Sanyal, Pranav Ponnusamy, Kusum Meda Ravi, Pranav Sastry, Mani Chandana Bandaru, Alind Khare, Myungjin Lee, Alexey Tumanov. [Primary paper, arXiv 2611.11761v1](https://arxiv.org/pdf/2611.11761v1).

## Thesis

Prompt processing and token generation can run on different-sized models if the decoder can consume a translated cache.

## Mechanisms

A large model processes the prompt, a learned map translates its attention cache, and a small model decodes.

## Evidence

The 8B-to-1B route measured 3.0× faster requests on one A40 relative to the larger model. The 70B-to-1B serving estimates came from simulation.

## Failure Modes

Single-A40 measurements and separate serving simulation. The smaller decoder changes the output behavior. Quality, transfer costs and request latency need comparison on the same prompt mix.

## Book Chapters Supported

- `fast-generation-architectures` — [Translate a prompt cache between models](../../chapters/fast-generation-architectures.qmd#translate-a-prompt-cache-between-models)

## Claims To Add Or Update

Distinguish the measured small-model route from the simulated large deployment when sizing a server.

## Open Questions

At what prompt length does transferring the cache erase the measured latency advantage?
