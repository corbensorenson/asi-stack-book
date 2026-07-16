# Source Note: TRM ARC-AGI Critical Analysis

| Field | Value |
|---|---|
| Source ID | `ext_trm_arc_agi_analysis_2025` |
| Source title | Tiny Recursive Models on ARC-AGI-1: Inductive Biases, Identity Conditioning, and Test-Time Compute |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2512.11847v2, https://arxiv.org/abs/2512.11847 |
| Ingestion basis | Primary technical note abstract and behavioral-analysis claims reviewed; not independently reproduced. |

## Thesis

The analyzed TRM checkpoint's ARC-AGI-1 performance depends materially on
test-time augmentation and voting, correct puzzle identity, and relatively
shallow effective recursion rather than establishing deep generic recursive reasoning.

## Mechanisms

- Single-pass versus 1000-sample voting comparison.
- Puzzle-identity removal and randomization.
- Per-recursion trajectory analysis and saturation measurement.

## Evidence

The note reports about an eleven-point Pass@1 contribution from the 1000-sample
voting pipeline, zero accuracy under blank or random puzzle identity, and most
accuracy appearing at the first recursion step. These are source-reported
findings, not local results.

## Failure Modes

- A technical-note audit may depend on one checkpoint and evaluation implementation.
- Identity removal can change the task as well as reveal a shortcut.
- Shallow effective recursion in one setting does not refute every recursive architecture.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Count test-time samples and voting in total-system KISS accounting.
- Measure marginal utility by recursion step and remove identity shortcuts prospectively.

## Open Questions

- Which recurrent gains survive canonical single-pass inference and unseen task identities?
- Can recursion policies generalize their stopping and depth allocation?
