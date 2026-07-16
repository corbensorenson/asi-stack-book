# Source Note: Attention Is All You Need

| Field | Value |
|---|---|
| Source ID | `ext_attention_is_all_you_need_2017` |
| Source title | Attention Is All You Need |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:1706.03762, https://arxiv.org/abs/1706.03762 |
| Ingestion basis | Primary paper abstract and architecture/evaluation sections reviewed; not vendored or reproduced. |

## Thesis

The Transformer replaces recurrence and convolution in its sequence
transduction setup with attention, enabling highly parallel training and a
strong dense-attention baseline for this chapter.

## Mechanisms

- Multi-head self-attention and cross-attention.
- Position-wise feed-forward blocks, residual connections, and normalization.
- Positional information supplied separately from recurrence.

## Evidence

The paper reports translation quality, training cost, and generalization under
its evaluated setup. This repository has not reproduced those results.

## Failure Modes

- Historical success can become architecture monoculture.
- Dense attention cost and KV-state assumptions can leak into stack contracts.
- A strong baseline is not a universal optimum.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Use a competitive Transformer as the baseline, not a straw implementation.
- Keep tokenization, positional encoding, KV state, and serving assumptions out of the ABI.

## Open Questions

- Which capabilities truly require global content-addressable communication?
- What translation cost appears when a non-attention kernel enters a Transformer-shaped stack?
