## GE1

The eight-layer DFlash drafter produced longer accepted sequences. The five-layer drafter delivered the greater speedup in the tested configuration. Accepted block length alone is insufficient as a latency proxy because proposing a longer accepted block can take more time. The comparison is a depth ablation within DFlash. [Fast Generation Architectures, paragraph beginning “DFlash’s depth ablation”](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html?view=ai) · [DFlash, Table 6](https://arxiv.org/html/2602.06036v2)

## GE2

On MATH-500 with a 1.7B drafter and Qwen3-32B, D3D reported 154 aggregate decode tokens/s at one concurrent request, a 6.1× gain over ordinary decoding. At sixteen requests it reported 864 aggregate decode tokens/s, a 2.7× gain. The figures cannot price an interactive customer’s first-token delay. That requires a time-to-first-token measurement that includes queueing at the expected concurrency. The comparison measures aggregate decode throughput. [Fast Generation Architectures, paragraph beginning “Consider a service choosing between one interactive request and a shared batch”](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html?view=ai) · [D3D, Table 2](https://arxiv.org/html/2611.06425v1)

## GE3

Unresolved. The chapter’s source notes identify `ext_bridgekv_2026` and report review of selected primary passages. I did not locate the evidence for the measured model pairing and hardware, the simulated pairing, or the larger model’s role in checking tokens. [Fast Generation Architectures, source notes](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html?view=ai)

## GE4

Unresolved. I did not locate the ByteFlow example or the Table 3 comparison, so I could not verify the split selection, the architecture and training scale, or the scope of evidence for a controller identifier.
