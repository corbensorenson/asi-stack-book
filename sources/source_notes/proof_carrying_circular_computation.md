# Source Note: Proof-Carrying Circular Computation

| Field | Value |
|---|---|
| Source ID | `proof_carrying_circular_computation` |
| Source title | Proof-Carrying Circular Computation |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project source text; raw source text is not copied here |

## Thesis

Proof-Carrying Circular Computation starts a compute track for certified cyclic, circulant, and orbit-structured computations that can later lower to specialized backends. The long-term target is a CoilIR-style optimizer: recognize cyclic structure, attach Lean-proved rewrite or address transformations, select a backend, and validate performance with benchmarks.

## Mechanisms

- Use a cyclic-address primitive `index mod size` for positive circular buffer sizes.
- Prove basic address-safety facts: bounded address, wraparound after one pass, multi-pass wraparound, idempotent normalization, and zero anchor.
- Treat stride coverage as the non-trivial structural rule: a stride visits every cell exactly when it is coprime to the size.
- Require each backend to have both a proof side, where rewrites preserve finite address or algebraic structure, and a benchmark side, where the backend beats a relevant baseline on a specified workload.
- Candidate backends include direct cyclic loops, FFT convolution, NTT convolution, circulant/block-circulant routines, coiled memory layouts, ring-buffer kernels, and geometric kernels where the workload warrants them.

## Evidence

- The source is a polished draft with a proved cyclic-address seed.
- It identifies Lean theorem ids, Python examples, theorem/dictionary manifest links, and future backend program requirements.
- The source explicitly says the current address theorems are elementary bookkeeping and that performance is an empirical benchmark question.
- No Circle sidecar examples, Lean builds, or backend benchmarks were run from this repo as part of this note.

## Failure Modes

- Treating address-safety proofs as performance evidence.
- Selecting specialized cyclic backends without proving rewrite legality and benchmarking against dense/direct/standard-library baselines.
- Ignoring off-by-one, overflow, or idempotence errors in circular address lowering.
- Overstating elementary modular-index facts as deep compute acceleration.

## Book Chapters Supported

- `mathematical-and-search-substrates` (Mathematical and Search Substrates)
- `circle-calculus-and-proof-carrying-ai-contracts` (Circle Calculus and Proof-Carrying AI Contracts)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)

## Claims To Add Or Update

- The source can support source-derived discussion of proof-carrying cyclic address transformations and the separation between legal rewrites and benchmarked backend speedups.
- It should not be used to claim performance improvements without named benchmark artifacts.

## Open Questions

- Which cyclic address facts should be mirrored in ASI Stack Lean proofs?
- Should CoilIR remain an external Circle roadmap item or become an ASI Stack substrate appendix?
- What minimal benchmark would be adequate before any circular-compute performance claim is promoted?

