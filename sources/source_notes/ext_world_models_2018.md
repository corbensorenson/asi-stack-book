# Source Note: World Models

| Field | Value |
|---|---|
| Source ID | `ext_world_models_2018` |
| Source title | World Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:1803.10122, https://arxiv.org/abs/1803.10122 |
| Citation label | Ha and Schmidhuber (2018), World Models |
| Published / updated | 2018-03-27 / 2018-03-27 |
| DOI | 10.48550/arXiv.1803.10122 |
| Ingestion basis | Primary arXiv abstract and architecture description inspected; training, dream rollouts, and transfer results were not reproduced. |

## Thesis

World Models demonstrates the architectural separation of learned compact
environment state, temporal prediction, and a small controller, including
policy training inside generated rollouts. For the book, the important lesson
is also the hazard: internally coherent imagined trajectories are not reality.

## Mechanisms

- Encode observations into a compact latent representation.
- Predict temporal evolution in latent state.
- Train a compact controller against the learned dynamics.
- Transfer a policy learned in imagined rollouts back to the environment.

## Evidence

The paper reports bounded reinforcement-learning results in simulated domains.
No result has been reproduced here, and the paper does not establish safe
real-world grounding or causal adequacy.

## Failure Modes

- The controller can exploit model error or dream artifacts.
- Prediction quality can be uneven in action-relevant regions.
- Latent compression can discard rare but safety-critical state.
- Simulated success can fail under environment shift.

## Book Chapters Supported

- Proposed: `governed-world-models-and-reality-grounding`
- Existing boundary owners: `planning-as-a-control-layer`,
  `mathematical-and-search-substrates`

## Claims To Add Or Update

- Distinguish observation, belief state, prediction, imagined branch, and
  observed effect in the artifact graph.
- Require model-error and sim-to-real residuals before action authority.
- Test for planner exploitation of model error, not only prediction loss.

## Open Questions

- Which error budget must block action or force re-observation?
- How should rare-event uncertainty survive latent compression?
- What intervention distinguishes useful dynamics from correlational replay?
