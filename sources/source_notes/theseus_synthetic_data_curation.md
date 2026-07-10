# Source Note: Theseus Synthetic Data Curation

| Field | Value |
|---|---|
| Source ID | `theseus_synthetic_data_curation` |
| Source title | Theseus Synthetic Data Curation |
| Ingestion date | 2026-07-10 |
| Source version / URL | local-project:Theseus-Hive@09ecbd8cff4a:docs/SYNTHETIC_DATA_CURATION.md; pinned local project source |
| Citation label | Project Theseus, Synthetic Data Curation (pinned local source) |
| Published / updated | 2026-05-12 / 2026-05-12 |
| DOI | none recorded |
| Ingestion basis | Pinned local-project documentation, policy, and source-reported curator result reviewed; no Theseus command, generated dataset, or training evaluation was rerun from this repository. |

## Thesis

The Theseus synthetic-data lane treats synthetic examples as a capped,
residual-targeted training intervention rather than a bulk self-training source.
It uses provenance, leakage, quality, diversity, ratio, and downstream
promotion gates to make the data path inspectable and rejectable.

## Mechanisms

- Start from residual escrow and select high-residual rule or term families.
- Generate local template and feature-preserving mutation candidates, then
  reject overlaps with training, evaluation, holdout, and bridge exclusions.
- Require source/provenance records, quality and diversity checks, per-rule
  caps, a real-data seed, and a bounded synthetic-data ratio.
- Keep external teacher material in a separately governed, verifier-gated,
  training-time-only path; prohibit runtime serving of teacher output.
- Require public/private comparator, regression, residual-delta, runtime, and
  synthetic-governance gates before candidate promotion.

## Evidence

- The pinned local source describes a concrete policy and names its scripts,
  generated artifacts, and gate reports.
- The pinned curator report is source-reported context for one local BabyLM/
  BLIMP-style blend and its own declared checks; it is not independently
  replayed, current-system, model-quality, or general synthetic-data evidence.
- This repository has not executed `synthetic_data_curator.py`, inspected
  generated rows, verified the report's digests, rerun a comparator, or imported
  any Theseus dataset.

## Failure Modes

- A capped synthetic ratio and exact-overlap checks do not rule out semantic
  leakage, provenance error, hidden distribution shift, or benchmark gaming.
- Better training score can coexist with worse heldout calibration, regression,
  or residual state; the source routes that case to blocked promotion.
- The data engine's local policy cannot establish that its ratio is optimal,
  that synthetic data is generally safe, or that external teacher generation is
  harmless.

## Book Chapters Supported

- `data-engines-continual-learning-and-unlearning` (Data Engines, Continual
  Learning, and Unlearning)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and
  Learning from Feedback)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and
  Cognitive Loop Closure)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and
  Anti-Goodhart Evidence)
- `project-theseus-as-report-first-implementation-reference` (Project Theseus
  as Report-First Implementation Reference)

## Claims To Add Or Update

- Use Theseus as a source-reported prototype pattern for a data-admission
  receipt: origin, license, provenance, generation policy, target residual,
  split exclusions, quality checks, ratio, result reference, and residual.
- Preserve the boundary between source-reported gate state and a reproduced
  data-engine result.
- Do not claim data quality, model improvement, leakage absence, or general
  efficacy without an ASI Stack consumer replay and a scoped evidence decision.

## Open Questions

- What public-safe fixture can test data-admission routing without exposing
  training rows or benchmark answers?
- Which semantic-overlap and distributional checks are required beyond exact
  overlap before a data packet may be admitted?
- How should unlearning, deletion, and source revocation propagate through
  synthetic descendants and procedural-memory artifacts?
