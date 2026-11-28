## GE1

DFlash’s eight-layer drafter produced longer accepted sequences. Its five-layer drafter delivered the greater speedup. In that depth ablation, the two rankings diverged because proposing a block also takes time. The deployment team should measure latency directly for its serving configuration and use accepted block length as a diagnostic.

Source: [Fast Generation Architectures, DFlash depth-ablation paragraph](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html?view=ai), citing [DFlash, Table 6](https://arxiv.org/html/2602.06036v2). Source note `ext_dflash_2026`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`.

## GE2

On MATH-500, with a 1.7B drafter and Qwen3-32B target, one request yielded 154 aggregate decode tokens/s and a 6.1× gain over ordinary decoding. Sixteen concurrent requests yielded 864 aggregate decode tokens/s and a 2.7× gain. These figures cannot price first-token delay for an interactive customer. The relevant measurement is request-level time to first token, including queueing, at the expected concurrency.

Source: [Fast Generation Architectures, D3D interactive-versus-shared-batch paragraph](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html?view=ai), citing [D3D, Table 2](https://arxiv.org/html/2611.06425v1). Source note `ext_d3d_2026`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`.

## GE3

BridgeKV measured 3.0× faster requests with an 8B prefill model and 1B decoder on one A40, relative to serving with the larger model. The 70B-to-1B serving estimates came from simulation. The large model processes the prompt, a learned map translates its KV cache, and the 1B model decodes. The larger model does not recheck each output token, and the smaller decoder can change output behavior.

Source: [Fast Generation Architectures, BridgeKV measured-speedup paragraph and comparator entry](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html?view=ai), citing [BridgeKV](https://arxiv.org/pdf/2611.11761v1). Source note `ext_bridgekv_2026`. Book revision `d5d8c2f7c11985af1a7f9a4393f0771745610639`.

## GE4

A budget of two distinct boundary positions can retain at most two of three distinct useful internal splits, so at least one split must be omitted and its neighboring spans remain joined. I could not locate the ByteFlow worked example or Table 3 within the open limit. I could not verify which split is omitted, the architecture and training scale of the comparison, or what the evidence establishes for a controller identifier.
