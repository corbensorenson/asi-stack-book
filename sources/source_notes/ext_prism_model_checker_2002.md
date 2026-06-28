# Source Note: PRISM: Probabilistic Symbolic Model Checker

| Field | Value |
|---|---|
| Source ID | `ext_prism_model_checker_2002` |
| Source title | PRISM: Probabilistic Symbolic Model Checker |
| Ingestion date | 2026-06-28 |
| Source version / URL | PRISM project paper PDF, https://www.prismmodelchecker.org/papers/tools02.pdf |
| Citation label | Kwiatkowska et al. (2002), PRISM |
| Published / updated | 2002 /  |
| DOI | 10.1007/3-540-46002-0_42 |
| Ingestion basis | PRISM project site and linked tool-paper PDF endpoint inspected for the probabilistic model-checking queue; PRISM models, properties, case studies, and tool runs are not imported into this repository. |

## Thesis

PRISM belongs in the proof-envelope, readiness-gate, benchmark, and reference-architecture chapters as an external reference for probabilistic model checking. It gives the ASI Stack vocabulary for model, property, state-space, probability, reward, and strategy-analysis boundaries where uncertainty cannot be reduced to a Boolean proof.

## Mechanisms

- Model probabilistic systems with a symbolic model checker.
- Analyze probabilistic properties over models rather than relying on informal arguments.
- Support property-analysis workflows suitable for systems with stochastic behavior or reliability concerns.
- Connect tool runs, models, and properties as separate evidence artifacts.

## Evidence

- The source is a primary PRISM tool paper/project source for probabilistic model-checking vocabulary.
- This repository has not built PRISM models, run PRISM, imported properties, or checked ASI Stack protocols probabilistically.
- Use this source as external model-checking vocabulary, not as evidence for any ASI Stack safety or benchmark claim.

## Failure Modes

- A model-checking result only applies to the model and properties actually encoded.
- Probabilistic assumptions can hide deployment mismatch if environment distributions are guessed.
- Tool-based certainty can be laundered into broader runtime claims when the abstraction boundary is not recorded.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Use this note to ground probabilistic model-checking vocabulary for future readiness, benchmark, and runtime-assurance artifacts.
- Do not claim PRISM verification or probabilistic safety evidence without local model/property/tool-run records.
- Keep support state at `argument` until model-checking artifacts or accepted evidence transitions exist.

## Open Questions

- Which ASI Stack readiness-gate record is small enough to model as a probabilistic transition system?
- What property format should preserve model, assumption, property, solver version, and result boundary?
- How should benchmark ratchets distinguish stochastic reliability from benchmark-score improvement?
