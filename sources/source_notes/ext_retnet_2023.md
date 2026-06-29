# Source Note: Retentive Network: A Successor to Transformer for Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_retnet_2023` |
| Source title | Retentive Network: A Successor to Transformer for Large Language Models |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2307.08621, https://arxiv.org/abs/2307.08621 |
| Citation label | Sun et al. (2023), Retentive Network |
| Published / updated | 2023-07-17 / 2023-08-09 |
| DOI | 10.48550/arXiv.2307.08621 |
| Ingestion basis | Public arXiv abstract and metadata inspected for recurrence and cyclic-substrate external positioning; paper not vendored into this repository and no model or benchmark reproduced. |

## Thesis

RetNet is an external comparator for the attention-recurrence boundary. It belongs in Coil memory and cyclic-mixer positioning because it explicitly relates recurrence, attention, recurrent inference, and chunkwise computation, but it does not validate local Coil, CoilRA, or cyclic-substrate claims.

## Mechanisms

- Derive a connection between recurrence and attention.
- Use a retention mechanism for sequence modeling.
- Support parallel, recurrent, and chunkwise recurrent computation modes.
- Treat inference, memory, latency, and sequence-length behavior as empirical claims rather than structural facts alone.

## Evidence

- The source reports language-modeling, scaling, inference, latency, memory, and long-sequence claims under its evaluated setup.
- This repository has not reproduced RetNet training, inference, memory, latency, quality, or long-sequence results.
- Use this source as an external comparator for recurrence/attention tradeoffs and for keeping computation-mode claims separate from Coil structural receipts.

## Failure Modes

- Recurrent inference efficiency can be mistaken for governed recurrence contracts.
- Chunkwise recurrent structure does not prove retrieval adequacy or reasoning quality.
- Reported deployment economics depend on implementation, hardware, model scale, and workload.
- A recurrence-attention bridge does not establish cyclic mixer quality, parameter efficiency, or context-length improvement.

## Book Chapters Supported

- `coil-attention-cyclic-memory-and-recurrence-contracts` (Coil Attention, Cyclic Memory, and Recurrence Contracts)
- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)

## Claims To Add Or Update

- Use RetNet as a source-noted external comparator for recurrence/attention tradeoffs.
- Keep ASI Stack Coil contracts framed as structural guardrails and admission records, not as reproduced recurrence-model results.
- Require workload, baseline, metric, and negative-control records before routing cyclic or recurrent substrates as adopted mechanisms.

## Open Questions

- Should recurrence-mode selection live in generation-mode records, substrate-adoption records, or cyclic-memory contracts?
- What negative controls distinguish useful recurrence from overthinking or stale-state reuse?
- Which RetNet-style recurrent or chunkwise baseline would be fair for a first Coil memory experiment?
