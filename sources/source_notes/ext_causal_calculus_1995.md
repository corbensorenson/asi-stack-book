# Source Note: A Causal Calculus for Statistical Research

| Field | Value |
|---|---|
| Source ID | `ext_causal_calculus_1995` |
| Source title | A Causal Calculus for Statistical Research |
| Source version / URL | <https://proceedings.mlr.press/r0/pearl95a.html> |
| Ingestion date | 2026-07-24 |

## Thesis

Pearl gives formal semantics and rules for identifying interventional
quantities from observational distributions under a structural causal model.
The central distinction is between observing a variable and intervening on it.

## Mechanisms

- causal directed graphs and intervention operators;
- graphical conditions for adding, deleting, or exchanging observations and
  actions;
- identification of interventional distributions from observational data;
- explicit query, population, assumptions, and adjustment structure.

## Evidence

The paper supplies formal results relative to a stated causal model. It does
not discover the true graph from arbitrary data, validate the variables,
guarantee positivity or invariance, or make a counterfactual reliable by syntax
alone.

## Failure Modes

- confounding hidden by an incorrect graph;
- selection bias, measurement error, or positivity failure;
- causal direction inferred from association alone;
- transport to a changed population without a transport argument;
- a formally identified query paired with an invalid estimator or ontology.

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`

## Claims To Add Or Update

- Every causal world-model claim should bind a query, graph version,
  intervention, population, identification derivation, assumptions, estimator,
  uncertainty, transport target, and falsification tests.
- Causal discovery proposals and identified causal effects remain distinct.

## Open Questions

- How should learned representations map to stable causal variables?
- Which interventions are ethical and feasible for validation?
- How should causal assumptions expire under policy-induced distribution shift?
