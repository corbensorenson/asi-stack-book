# Source Note: RankFold + NeuralFold

| Field | Value |
|---|---|
| Source ID | `rankfold_neuralfold` |
| Source title | RankFold + NeuralFold |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1-9wujZDobutPQbAml3H3QqYvdt9GIk55bxJiaPeSUhg |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/rankfold_neuralfold.txt`; raw text is not published. |

## Thesis

RankFold + NeuralFold proposes a tensor-centric archival stack for heterogeneous ML and scientific artifacts. RankFold optimizes low-rank residual transforms against actual coding cost, while NeuralFold converts arbitrary artifacts into weight-like tensors that can be stored through a common compression backend.

## Mechanisms

- Optimize per artifact rather than relying on one global learned compressor.
- Align transforms with the residual coder and bit cost, not only reconstruction error.
- Convert arbitrary files, images, logs, simulations, or directories into implicit or predictive tensor representations.
- Use WORM archival assumptions so expensive encoding can be amortized over long-term storage.
- Preserve determinism, reproducibility, decode correctness, fuzz tests, and integration tests as design obligations.
- Keep artifact manifests, codec parameters, and reconstruction checks attached to archives.

## Evidence

- The source is an architecture and implementation-plan paper with pseudocode, testing strategy, milestones, and interface discussion.
- It does not provide local compression benchmarks, implementation artifacts, or reproducible ratios in this repository.
- Use it for compression architecture and artifact-backend design, not for measured performance claims.

## Failure Modes

- Optimizing reconstruction error while ignoring actual encoded residual cost.
- Treating arbitrary-artifact-to-tensor conversion as lossless without a reconstruction contract.
- Hiding encoder cost in a setting where write-once amortization does not apply.
- Losing deterministic decode through floating-point, platform, or dependency differences.
- Publishing compression ratios without manifest, baseline, and verification details.

## Book Chapters Supported

- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `simulation-fidelity-and-physical-constraints` (Simulation Fidelity and Physical Constraints)

## Claims To Add Or Update

- Use this source to connect artifact compression, deterministic reconstruction, and ML-system storage economics.
- Keep compression-ratio and universality claims as research goals until a benchmark harness exists.

## Open Questions

- Should Appendix E include a toy deterministic archive manifest?
- Which artifacts in this repo are suitable for a first RankFold-style experiment?
