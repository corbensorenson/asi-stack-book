# Explore, Then Commit: Measurement-Efficient Scientific Law Discovery with Language Models

| Field | Value |
|---|---|
| Source ID | `ext_explore_then_commit_2026` |

Kautik Mandve, Dileepa Fernando. [Primary paper, arXiv 2610.07620v1](https://arxiv.org/html/2610.07620v1).

## Thesis

The observations available to a scientific analyst depend on the policy that selected the measurements.

## Mechanisms

Choose a discriminating probe, freeze the observations, and evaluate a fresh analyst's law and forecast.

## Evidence

Across 576 NewtonBench trials, the interpreter-enabled configuration on medium GPT-4.1-mini tasks averaged 8.6 measurements versus 22.5 for the comparison.

## Failure Modes

NewtonBench trials and coverage-sensitive analysis. The simulations are noiseless, batch limits differed, symbolic gains varied, and random acquisition was competitive with disagreement scoring.

## Book Chapters Supported

- `scientific-discovery-and-experimental-governance` — [Spend one measurement to separate two laws](../../chapters/scientific-discovery-and-experimental-governance.qmd#spend-one-measurement-to-separate-two-laws)

## Claims To Add Or Update

Match acquisition budgets and retain random acquisition when attributing forecast gains to active probing.

## Open Questions

With noisy measurements and identical batch caps, which strategy recovers a better law on held-out systems?
