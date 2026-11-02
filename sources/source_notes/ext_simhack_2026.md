# Source Note: SimHack: Predicting the onset of detectable reward hacking before RL training

| Field | Value |
|---|---|
| Source ID | `ext_simhack_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.28707v1](https://arxiv.org/html/2610.28707v1) |
| Citation | Deng, Bie and Ponomareva (2026), SimHack |
| Published / updated | 2026-10-20 / 2026-10-20 |
| Review scope | Sections 3.1–3.2, 4.1 and 7; recipe-level prediction rather than a direct behavior monitor. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Models behavior-state transitions from reference RL runs to forecast the distribution of detectable hacking onset under candidate training recipes. Useful for prospective curriculum-risk comparisons.

## Mechanisms

Fit prompt-level behavioral dynamics from reference RL histories, then simulate correct/hacking/other behavior under target curricula, rollout counts, learning rates and model scales.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

Reference/target splits support recipe-level prediction in two Qwen3 scales and two loophole suites. Detectable-onset prediction depends on retained detectors and is not a live internal-state monitor. No study, code or proof was independently reproduced here.

## Failure Modes

Requires reference training data and detectors. Qwen3-0.6B/4B and two loophole suites bound the evidence; delayed detectable onset is not absence of hidden hacking or a general prevention guarantee.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
