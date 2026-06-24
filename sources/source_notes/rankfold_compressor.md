# Source Note: RankFold Compressor

| Field | Value |
|---|---|
| Source ID | `rankfold_compressor` |
| Source title | rankFold compressor |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/11jw0DAAuUvw75Q_1AiwTiUGcd-y_IywB9qdEka9_MfI |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/rankfold_compressor.txt`; raw text is not published. |

## Thesis

RankFold Compressor explores low-rank vector-pair representation, adaptive matrix/tensor compression, shape optimization, entropy-aware coding, and recursive cascades. It is an earlier or adjacent compression source for the RankFold/NeuralFold artifact-compression chapter.

## Mechanisms

- Reshape arbitrary data into matrices or tensors for low-rank treatment.
- Use vector-pair or factorized representations with adaptive rank.
- Combine normalization, entropy coding, and shape optimization.
- Prefer near-square shapes when they reduce parameter count under suitable assumptions.
- Apply recursive cascades to reduce residual entropy.
- Add correctness, determinism, metric reporting, CLI, and extension plans in later sections.

## Evidence

- The cache contains multiple versions and broad mathematical claims.
- The repository has not implemented the compressor, reproduced ratios, or validated lossless reconstruction.
- Use the more specific `rankfold_neuralfold` note for the mature archive-stack framing and this note for lineage and mathematical variants.

## Failure Modes

- Calling a representation lossless without an exact reconstruction contract.
- Hiding overhead in shape metadata, ranks, seeds, or residuals.
- Assuming low-rank structure where artifact data is high entropy.
- Optimizing continuous reconstruction while ignoring discrete serialization.
- Reporting compression without baselines, corpus, and decoder determinism.

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)

## Claims To Add Or Update

- Use this source as a lineage source for low-rank/tensor compression concepts.
- Do not use it alone to support compression-performance claims.

## Open Questions

- Should the book separate exact compression, lossy representation, and archival containers more sharply?
- Which RankFold claims can be tested with a tiny public matrix corpus?
