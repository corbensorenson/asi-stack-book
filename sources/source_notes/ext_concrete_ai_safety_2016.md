# Source Note: Concrete Problems in AI Safety

| Field | Value |
|---|---|
| Source ID | `ext_concrete_ai_safety_2016` |
| Source title | Concrete Problems in AI Safety |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1606.06565, https://arxiv.org/abs/1606.06565 |
| Citation label | Amodei et al. (2016), Concrete Problems in AI Safety |
| Published / updated | 2016-06-21 / 2016-07-25 |
| DOI | 10.48550/arXiv.1606.06565 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the alignment/control literature queue; paper not vendored into this repository and no experiments reproduced. |

## Thesis

This source belongs in the book as the external accident-risk baseline for practical AI safety. It frames safety work around concrete failure classes rather than broad assurances, which matches the ASI Stack emphasis on explicit failure modes, residuals, and evidence boundaries.

## Mechanisms

- Treat unintended side effects, reward hacking, scalable oversight, safe exploration, and distributional shift as separate problem families.
- Connect safety failures to objective design, training signal quality, supervision limits, environment interaction, and deployment shift.
- Emphasize empirically testable problem formulations rather than a single global alignment proof.
- Motivate benchmark ratchets that preserve negative results instead of smoothing failures into a general performance score.

## Evidence

- The source contributes external taxonomy and research framing.
- This repository has not reproduced any experiment, environment, benchmark, or mitigation result from the paper.
- Use it as literature context for failure-class vocabulary and test-design pressure, not as evidence that any ASI Stack mechanism solves those problems.

## Failure Modes

- A taxonomy can become a checklist that hides new failure modes.
- Reward-hacking and distribution-shift examples can be overgeneralized to untested ASI Stack components.
- Safety benchmark results from the source setting cannot be imported without reproduction artifacts.

## Book Chapters Supported

- `failure-modes-of-ungoverned-intelligence` (Failure Modes of Ungoverned Intelligence)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to ground the book's practical failure taxonomy against external literature.
- Keep all ASI Stack claim support at `argument` unless a later accepted evidence transition, reproduction, or narrower source-derived review justifies movement.
- Record failed or inconclusive local tests if any future harness attempts these failure classes.

## Open Questions

- Which ASI Stack harness should first instantiate side-effect, reward-hacking, or distribution-shift checks?
- Which failure classes need separate residual ledgers rather than one benchmark score?
- What source-derived claim, if any, can be scoped narrowly enough for future promotion?
