# Source Note: Gated DeltaNet-2

| Field | Value |
|---|---|
| Source ID | `ext_gated_deltanet2_2026` |
| Source title | Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention |
| Ingestion date | 2026-07-16 |
| Source version / URL | arXiv:2605.22791v1, https://arxiv.org/abs/2605.22791; official implementation, https://github.com/NVlabs/GatedDeltaNet-2, revision `95709fc250357c2dd109361c353192f2aa5913f9` observed 2026-07-16 |
| Ingestion basis | Primary preprint abstract/comparison envelope and official implementation identity reviewed; no checkpoint, training, inference, benchmark, hardware, ablation, or transfer result reproduced. |

## Thesis

Gated DeltaNet-2 separates the erase and write operations that earlier gated
delta-rule memories coupled through a shared scalar. The paper presents this as
a more expressive recurrent/linear-attention update with an efficient chunkwise
algorithm.

## Mechanisms

- Channel-wise erase and write gates instead of one coupled scalar update.
- A fast-weight interpretation and chunkwise algorithm with channel-wise decay.
- Recurrent and hybrid configurations evaluated against Mamba-2, Gated
  DeltaNet, KDA, and Mamba-3 variants.

## Evidence

The preprint reports that a 1.3B-parameter model trained on 100B FineWeb-Edu
tokens produces the strongest overall aggregate in its declared language-
modeling, commonsense, retrieval, and RULER comparison envelope. This makes it
the dated reported recurrent comparator for that envelope at the P6 refresh.
It does not establish a universal architecture frontier.

The ASI Stack repository did not reproduce the checkpoint, training, seed
variation, hardware behavior, retrieval results, recurrent state behavior,
hybrid comparison, or transfer. The available Apple M1 host has no CUDA path,
and no cloud-compute authority was granted.

## Failure Modes

- **Frontier laundering:** the paper's exact comparison is described as global
  SOTA across model scales, data, modalities, workloads, or hardware.
- **Source-result laundering:** an author-reported aggregate becomes local
  evidence without checkpoint and harness reproduction.
- **State-cost erasure:** fixed-size recurrent memory is credited without
  migration, checkpoint, numerical, rollback, and failure accounting.
- **Hardware erasure:** optimized CUDA/Triton behavior is generalized to edge,
  CPU, or Apple hardware without measurement.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Update the dated architecture taxonomy so Mamba-3 is a current mechanism
  comparator rather than the newest claimed recurrent frontier.
- Require Gated DeltaNet-2 in the strongest-comparator ledger for the paper's
  exact envelope.
- Keep independently reproduced quality, state, hardware, total-cost, and
  transfer gates before any architecture qualification.

## Open Questions

- Do the reported gains survive independently reproduced matched seeds and
  equal total-lifecycle cost?
- How do separate erase/write gates affect state migration, numerical drift,
  poisoning recovery, and rollback?
- Do recurrent and hybrid gains transfer across modalities and non-CUDA
  hardware?
