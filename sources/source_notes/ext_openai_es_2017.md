# Source Note: Evolution Strategies as a Scalable Alternative to Reinforcement Learning

| Field | Value |
|---|---|
| Source ID | `ext_openai_es_2017` |
| Source version / URL | <https://arxiv.org/abs/1703.03864> |
| Ingestion date | 2026-08-09 |

## Thesis

Salimans and colleagues optimize expected episodic return through parameter
perturbations and scalar fitness rather than temporal credit assignment. The
work established a practical modern baseline for large-population ES and showed
why communication can be compact when workers share seeds and return scalars.

## Mechanisms

Workers evaluate random parameter perturbations, return fitness values, and
reconstruct a population gradient estimate. Compact scalar communication can
replace transmission of full gradient tensors when workers share the parameter
identity and perturbation seeds.

## Evidence

The paper reports competitive results on studied MuJoCo and Atari tasks and
scaling beyond one thousand workers. The results are source-scoped and predate
modern foundation-model training; they do not establish universal sample or
compute efficiency.

## Failure Modes

ES moves the credit-assignment problem into a population estimator and an
episodic fitness function. It can be robust and parallel while consuming many
rollouts, and its scalar communication advantage does not erase environment,
simulation, synchronization, or energy cost.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- `learning-compute-topology-and-adaptive-process-architecture`
- `policy-optimization-and-learning-from-feedback`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Outcome-only parameter search is a real policy-learning family, not merely a
  weak approximation to policy gradients.
- Scalar communication and wall-clock parallelism must be reported beside total
  rollouts, environment cost, accelerator-hours, and energy.

## Open Questions

- Which modern model and agent regimes favor population search after total cost
  and strong gradient baselines are matched?
- How should simulator fidelity and evaluator drift enter the ES denominator?
