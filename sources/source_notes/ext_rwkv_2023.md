# Source Note: RWKV

| Field | Value |
|---|---|
| Source ID | `ext_rwkv_2023` |
| Source title | RWKV: Reinventing RNNs for the Transformer Era |
| Ingestion date | 2026-07-15 |
| Source version / URL | Findings of EMNLP 2023, https://aclanthology.org/2023.findings-emnlp.936/ |
| Ingestion basis | Primary paper abstract and model/evaluation sections reviewed; no reproduction. |

## Thesis

RWKV combines parallelizable training with recurrent inference to provide a
language-model architecture outside ordinary dense-attention serving.

## Mechanisms

- Time-mixing and channel-mixing recurrence.
- Parallel training form and constant-state recurrent inference form.
- Language-model scaling and evaluation.

## Evidence

The source reports benchmark, memory, and inference behavior. The repository has
not trained or served RWKV.

## Failure Modes

- Constant inference state can erase exact long-range information.
- Parallel and recurrent forms can diverge numerically or operationally.
- Model quality and ecosystem maturity may outweigh state-size advantages.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Test training/inference equivalence and state carry explicitly.
- Include recurrent serving as a first-class ABI cost/state pattern.

## Open Questions

- Which state-tracking tasks reveal recurrent compression failures?
- How should recurrent state be revoked, transferred, and restored?
