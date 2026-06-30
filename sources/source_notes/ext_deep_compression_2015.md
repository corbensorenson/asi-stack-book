# Source Note: Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding

| Field | Value |
|---|---|
| Source ID | `ext_deep_compression_2015` |
| Source title | Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1510.00149, https://arxiv.org/abs/1510.00149 |
| Citation label | Han et al. (2015), Deep Compression |
| Published / updated | 2015-10-01 / 2016-02-15 |
| DOI | 10.48550/arXiv.1510.00149 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the compression/representation literature queue; paper not vendored into this repository and no compression result reproduced. |

## Thesis

Deep Compression belongs in the compression and resource chapters as an external baseline for model-compression pipelines. It helps the ASI Stack distinguish compression mechanism, utility preservation, hardware effect, and benchmark reproduction.

## Mechanisms

- Prune network connections.
- Apply trained quantization and weight sharing.
- Use Huffman coding for additional storage reduction.
- Retrain after pruning and quantization to preserve task performance in the source setting.

## Evidence

- The source reports storage, speed, and energy improvements for specific neural networks and benchmarks.
- This repository has not reproduced the compression pipeline, datasets, models, hardware measurements, or accuracy results.
- Use it as external compression context, not as evidence that ASI Stack compression preserves utility.

## Failure Modes

- Compression ratio can hide lost utility or shifted cost.
- Hardware-specific speed and energy gains cannot be generalized without measurement.
- Preserved accuracy on one task does not prove residual honesty for another artifact.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)

## Claims To Add Or Update

- Use this note to source pruning/quantization/coding as external compression mechanisms.
- Do not claim local compression ratio, speedup, energy gain, or utility preservation.
- Keep support state at `argument` until local compression receipts and tests exist.

## Open Questions

- Which artifact-compression fixture should first measure utility preservation?
- How should compression receipts separate ratio, accuracy, speed, and energy?
- What residual ledger records utility lost after compression?
