# Generation and compression

Book revision 552fb37f379249f6a726b98cbbbd06384710c55c.

## GE1

The eight-layer DFlash drafter produced longer accepted sequences. The five-layer drafter produced the greater speedup in the tested depth ablation. Accepted block length alone cannot establish latency or rank deployments: a deeper drafter can spend more time proposing the longer blocks. Compare measured latency at matched deployment conditions. [Fast Generation Architectures, the paragraph beginning “DFlash’s depth ablation”](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html) reports the comparison from [DFlash Table 6](https://arxiv.org/html/2602.06036v2), source ID `ext_dflash_2026`.

## GE2

D3D with a 1.7B drafter and Qwen3-32B on MATH-500 reported **154 aggregate decode tokens/s and 6.1×** versus ordinary decoding at one concurrent request, and **864 aggregate decode tokens/s and 2.7×** at sixteen. Those aggregate decode figures cannot price an interactive customer’s first-token delay. That requires an arrival-to-first-token measurement, including queueing, at the customer’s expected concurrency. [Fast Generation Architectures, the paragraph beginning “Consider a service choosing between one interactive request and a shared batch”](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html) gives the figures and the measurement boundary for [D3D Table 2](https://arxiv.org/html/2611.06425v1), source ID `ext_d3d_2026`.

## GE3

BridgeKV measured **3.0× faster requests** for 8B prefill and 1B decoding on **one NVIDIA A40**, relative to serving the larger model. Its **70B-to-1B** serving estimates were simulated. The larger model processes the prompt, a learned map translates its KV cache, and the smaller model performs decoding without a per-token recheck by the prefill model. The route can change output behavior, so the measured speedup carries no target-output preservation guarantee. [Fast Generation Architectures, the paragraph beginning “The 8B-to-1B route” and the BridgeKV comparator entry](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html) summarize the [BridgeKV paper](https://arxiv.org/pdf/2611.11761v1), source ID `ext_bridgekv_2026`.

## GE4

If each desired internal split occupies one boundary position, a budget of two can retain at most two of three useful splits. At least one useful split is omitted, so at least two intended neighboring pieces stay joined. I could not locate the ByteFlow example or Table 3 in the inspected bundle routes. The comparison’s architecture and training scale, and the precise evidence boundary for the controller identifier, remain unresolved.
