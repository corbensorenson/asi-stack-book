# Source Note: CoilRA and MultiCoil RoPE

| Field | Value |
|---|---|
| Source ID | `coilra_multicoil_rope` |
| Source title | CoilRA and MultiCoil RoPE |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project source text; raw source text is not copied here |

## Thesis

CoilRA and MultiCoil RoPE explores cyclic/block-cyclic adapters, phase features, rotary-position structure, circulant mixers, and MLX-first benchmarks. Its disciplined claim is that cyclic or block-cyclic structure should be used only where phase, channel grouping, low-rank adaptation, positional rotation, or shift structure is real and where ordinary baselines remain the standard for quality and performance.

## Mechanisms

- Use adapter-block indices, position residues, and winding to expose finite cyclic structure and alias/load diagnostics.
- Treat circulant token mixing as circular convolution with structural shift-equivariance facts, while leaving performance to benchmarks.
- Treat RoPE relative-position invariance as a finite-circle rotation/translation law while leaving length extrapolation and accuracy to empirical tests.
- Compare dense, LoRA-style low-rank, block-cyclic, block-circulant, and circulant baselines with quality, parameter count, runtime, memory, and failure cases reported separately.
- Test MultiCoil phase features against standard RoPE, learned positions, ALiBi-style biases, recurrent memory, state-space baselines, wrong-period controls, and nonperiodic controls.

## Evidence

- The source is a proof-linked AI application paper with theorem spine, structural fixtures, and prototype program.
- It describes adapter-block, parameter-budget, circulant-mixer, block-cyclic-mixer, and MultiCoil/RoPE-style fixtures.
- It explicitly states that these fixtures are structural validation or parameter accounting, not evidence of fine-tuning, runtime, memory, quality, or downstream behavior improvements.
- No Circle sidecars, Lean builds, MLX runs, or model experiments were run from this repo as part of this note.

## Failure Modes

- Claiming CoilRA beats LoRA or dense adapters from structural bookkeeping alone.
- Optimizing for prime/coprime mathematical elegance while ignoring hardware-friendly sizes.
- Treating circulant or block-cyclic parameter counts as quality gains.
- Using phase features on nonperiodic tasks without wrong-period and learned-position controls.

## Book Chapters Supported

- `semantic-representation-and-tree-structured-models` (Semantic Representation and Tree-Structured Models)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)

## Claims To Add Or Update

- The source can support source-derived discussion of cyclic adapter/mixer contracts, phase/winding features, parameter-accounting baselines, and the empirical boundary around cyclic substrates.
- It should not be used to claim quality, speed, memory, training stability, or context-length improvements without named experiments.

## Open Questions

- Which cyclic mixer or adapter fixture should be replicated in this repo as a minimal executable schema test?
- How should ASI Stack chapters balance hardware efficiency against proof-friendly cyclic periods?
- Which resource-economics claims can be stated as parameter accounting only?

