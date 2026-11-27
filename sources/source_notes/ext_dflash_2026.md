# DFlash: Block Diffusion for Flash Speculative Decoding

| Field | Value |
|---|---|
| Source ID | `ext_dflash_2026` |

Jian Chen, Yesheng Liang and Zhijian Liu (2026). [Primary publication](https://proceedings.mlr.press/v306/chen26bv.html). See also the [authors’ method and ablations](https://arxiv.org/html/2602.06036v2).

## Thesis

A block drafter can reduce sequential decoding when the target frequently accepts its prefixes.

## Mechanisms

Predict a candidate block in one forward pass. The target checks its tokens before the next accepted prefix is established.

## Evidence

The authors report over sixfold decoding acceleration in their tested configurations, using a lightweight drafter conditioned on target features.

## Failure Modes

ICML proceedings abstract and the authors’ arXiv v2 method and Table 6. In the depth comparison, the eight-layer drafter had longer accepted sequences and the five-layer drafter was faster. Preserving the target decoding distribution depends on the verification rule. Output correctness and service-level latency need their own measurements.

## Book Chapters Supported

- `fast-generation-architectures` — [When can the next draft begin?](https://corbensorenson.github.io/asi-stack-book/chapters/fast-generation-architectures.html#when-can-the-next-draft-begin)

## Claims To Add Or Update

Time the drafter and verifier together when choosing a drafting depth.

## Open Questions

At fixed target and hardware, which depth minimizes tail latency at the deployed batch size?
