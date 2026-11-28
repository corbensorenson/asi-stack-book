## GE1

The eight-layer DFlash drafter produced longer accepted sequences. The five-layer drafter gave the greater speedup in the tested configuration. Accepted block length alone is an insufficient latency proxy because a longer block can take more time to propose. Measure latency directly on the intended serving configuration. [Fast Generation Architectures §63.8.1, depth ablation citing DFlash Table 6](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html#when-can-the-next-draft-begin)

## GE2

On MATH-500, the 1.7B D3D drafter with Qwen3-32B achieved 154 aggregate decode tokens/s at one concurrent request, 6.1× ordinary decoding, and 864 tokens/s at sixteen concurrent requests, 2.7× ordinary decoding. These figures cannot price an interactive customer’s first-token delay. That requires measuring time to first token at the expected concurrency, including queueing. [Fast Generation Architectures §63.8.1, MATH-500 comparison citing D3D Table 2](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html#when-can-the-next-draft-begin)

## GE3

BridgeKV measured a 3.0× request speedup on one A40 with an 8B prefill model and a 1B decoder, relative to running the larger model. The 70B-to-1B serving figures came from simulation. The large model supplies the prompt cache for translation, and the small decoder generates the output without a per-token check by the large model. [Fast Generation Architectures §63.8.2, BridgeKV measured and simulated routes](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html#translate-a-prompt-cache-between-models)

## GE4

With two boundary positions and three useful internal splits, ByteFlow selects two based on the input and drops the lower-ranked split. Table 3 compares chunking rules within the same 0.6B architecture trained on the reported 50B-token scale and averages three runs. Its bits-per-byte and downstream scores leave open whether the exact controller identifier can be recovered after chunking on the intended workload, especially if a dropped split marks it. [Replaceable Cognitive Substrates §55.11.3, boundary example and ByteFlow Table 3](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#a-fixed-budget-for-learned-byte-boundaries)
