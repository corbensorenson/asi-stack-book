# DFlash: Block Diffusion for Flash Speculative Decoding

Jian Chen, Yesheng Liang and Zhijian Liu (2026). [Primary publication](https://proceedings.mlr.press/v306/chen26bv.html). See also the [authors’ method and ablations](https://arxiv.org/html/2602.06036v2).

## Mechanism and evidence

Predict a candidate block in one forward pass. The target checks its tokens before the next accepted prefix is established.

The authors report over sixfold decoding acceleration in their tested configurations, using a lightweight drafter conditioned on target features.

## Review scope and open question

ICML proceedings abstract and the authors’ arXiv v2 method and Table 6. In the depth comparison, the eight-layer drafter had longer accepted sequences and the five-layer drafter was faster. Preserving the target decoding distribution depends on the verification rule. Output correctness and service-level latency need their own measurements.

## Book Chapters Supported

- `fast-generation-architectures`
