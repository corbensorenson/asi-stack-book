# Source Note: Titans

| Field | Value |
|---|---|
| Source ID | `ext_titans_2025` |
| Source title | Titans: Learning to Memorize at Test Time |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2501.00663, https://arxiv.org/abs/2501.00663 |
| Ingestion basis | Primary preprint abstract and memory/evaluation sections reviewed; no reproduction. |

## Thesis

Titans introduces neural long-term memory updated at test time and combines it
with sequence-processing architectures for long-context tasks.

## Mechanisms

- Surprise-sensitive neural memory updates.
- Persistent, short-term, and attention-linked memory variants.
- Test-time memorization within sequence modeling.

## Evidence

The source reports long-context and language-model results. No local Titans
model, memory update, or benchmark has run.

## Failure Modes

- Learned memory can confuse storage with faithful recall.
- Online writes create privacy, poisoning, revocation, and rollback obligations.
- Reported context length can conceal retrieval failures and update cost.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Separate neural memory from exact durable records and receipts.
- Measure state custody, rollback, poisoning, and total update cost.

## Open Questions

- Can mutable memory be selectively revoked or influence-unlearned?
- Which exact records must accompany neural-memory checkpoints?
