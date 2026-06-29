# Source Note: Circle AI Architectures

| Field | Value |
|---|---|
| Source ID | `circle_ai_architectures` |
| Source title | Circle AI Architectures |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project source text; raw source text is not copied here |

## Thesis

Circle AI Architectures states a disciplined Circle AI thesis: cyclic or coil structure may help only where the model, data, or computation already has real phase, recurrence, rotation, sparse cyclic mixing, circular memory, harmonic transforms, or geometry-aware structure. The contribution is to make the phase/coil/proof interface systematic, not to claim that circles improve every neural network.

## Mechanisms

- Separate finite-indexing bookkeeping theorems from genuinely ML-relevant structural guarantees.
- Treat phase channels, period closure, zero anchors, and normalization laws as useful but elementary infrastructure.
- Identify stronger structural targets: strided-attention coverage from orbit/gcd theory, RoPE relative position from rotation composition, and circulant shift-equivariance.
- Propose MLX/Mac-compatible prototypes around phase features, recurrence schedules, sparse cyclic mixing, circular memory banks, harmonic/circulant layers, and spherical/quaternion models when the data warrants them.
- Require ordinary baselines, wrong-period controls, scalar controls, learned-position controls, and negative results.

## Evidence

- The source is a polished paper draft for Circle's AI architecture program.
- It provides theorem/benchmark scaffolding and explicit guardrails.
- It describes exploratory benchmark fixtures but does not treat them as model-quality evidence.
- This source note itself did not run sidecar tests, Lean builds, MLX experiments, or benchmark fixtures from the ASI Stack repo. A later bounded external receipt slice is recorded separately in `docs/circle_external_receipt_slice.md` for one local rope-position contract replay; it does not support broad cyclic-architecture or model-quality claims.

## Failure Modes

- Claiming general AI improvement from cyclic structure.
- Treating elementary modulo-indexing theorems as evidence that a model improves.
- Omitting ordinary baselines or negative controls.
- Forcing circle structure onto nonperiodic or nongeometric tasks.

## Book Chapters Supported

- `semantic-representation-and-tree-structured-models` (Semantic Representation and Tree-Structured Models)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)
- `circle-calculus-and-proof-carrying-ai-contracts` (Circle Calculus and Proof-Carrying AI Contracts)
- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)

## Claims To Add Or Update

- The source can support source-derived discussion of when cyclic structure is an appropriate representation substrate and how to keep proof infrastructure separate from model-quality claims.
- It should not be used to claim universal performance improvement or broad architectural superiority.

## Open Questions

- Which ASI Stack chapters should mention Circle only as optional substrate rather than core architecture?
- Which negative controls should become required for cyclic-substrate experiments?
- Which structural guarantees are worth restating as ASI Stack proof targets?
