# Source Note: GSPMD: General and Scalable Parallelization for ML Computation Graphs

| Field | Value |
|---|---|
| Source ID | `ext_gspmd_2021` |
| Source title | GSPMD: General and Scalable Parallelization for ML Computation Graphs |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2105.04663v3, https://arxiv.org/abs/2105.04663 |
| Citation label | Xu et al. (2021), GSPMD |
| Published / updated | 2021-05-10 / 2021-12-14 |
| DOI | 10.48550/arXiv.2105.04663 |
| Ingestion basis | Primary paper reviewed, especially Sections 1, 3, 5, 6, and 7; no compiler, TPU run, or result reproduced. |

## Thesis

Parallelism can be represented as tensor sharding over a device mesh and
completed by a compiler, allowing data, model, optimizer-state, spatial, expert,
and pipeline patterns to compose through one representation.

## Mechanisms

- SPMD partitioning from limited user annotations.
- Per-operator sharding completion and resharding insertion.
- Nested device meshes and mixed parallelism patterns.
- Compiler-mediated alternative to hand-authored topology composition.

## Evidence

The paper reports 50--62% compute utilization on up to 2,048 TPUv3 cores for
models up to one trillion parameters and presents multiple workload studies.
These are source-reported results, not local evidence.

## Failure Modes

- Treating automatic completion as proof that the selected topology is optimal
  or semantically equivalent.
- Omitting compiler version, annotations, inferred shardings, inserted
  collectives, and resharding costs from run identity.
- Comparing compiler and manual approaches without matched hardware, model,
  quality target, and tuning opportunity.
- Assuming regular operator coverage transfers to new architecture families.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- Boundary context: `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat topology compilers and their inferred plans as versioned run inputs.
- Preserve the manual-versus-compiler design alternative and measure
  communication, memory, quality, tuning burden, and failures jointly.

## Open Questions

- How can an inferred sharding plan be independently replayed and compared?
- Which compiler changes invalidate a prior training-run qualification?
