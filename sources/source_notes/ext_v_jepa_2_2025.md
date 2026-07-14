# Source Note: V-JEPA 2

| Field | Value |
|---|---|
| Source ID | `ext_v_jepa_2_2025` |
| Source title | V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning |
| Ingestion date | 2026-07-14 |
| Source version / URL | arXiv:2506.09985, https://arxiv.org/abs/2506.09985 |
| Citation label | Assran et al. (2025), V-JEPA 2 |
| Published / updated | 2025-06-11 / 2026-04-26 |
| DOI | 10.48550/arXiv.2506.09985 |
| Ingestion basis | Primary arXiv HTML Abstract, architecture, planning, results, and limitations passages reviewed; checkpoints, robot data, and code were not run locally. |

## Thesis

V-JEPA 2 is a concrete latent-prediction and model-predictive-control
comparator. It separates action-free video pretraining from a smaller
action-conditioned predictor, then evaluates candidate action sequences in
representation space and replans toward image goals.

## Mechanisms

- Pretrain a visual encoder and predictor without action labels.
- Adapt a small action-conditioned predictor for robot planning.
- Predict future representations instead of reconstructing pixels or tokens.
- Use model-predictive control to score action sequences and repeatedly replan
  from new observations (Abstract and Sections 1-3; HTML lines 128-175).

## Evidence

The paper reports video understanding, prediction, and limited zero-shot robot
planning results. It provides a primary empirical architecture comparator and
an adoption test for the book. The repository has not reproduced any model,
benchmark, robot experiment, or timing result.

## Failure Modes

- Camera-position sensitivity required manual selection in reported settings.
- Autoregressive prediction accumulates error.
- Candidate-action search grows exponentially with horizon and dimension.
- Image-goal planning assumes suitable visual goals and representations.
- Representation-level prediction does not prove causal or interventional
  understanding, safe control, or sim-to-real transfer (limitations, HTML
  lines 383-396).

## Book Chapters Supported

- `mathematical-and-search-substrates`
- `planning-as-a-control-layer`
- `data-engines-continual-learning-and-unlearning`
- `integrated-reference-architecture`

## Claims To Add Or Update

- Add predictive-state identity, predictor version, horizon, action-space,
  observation provenance, error ledger, and replanning trigger to the planning
  contract.
- Keep structural, benchmark, causal, control, and transfer claims separate.
- Adopt a latent world model only after matched task, cost, calibration,
  intervention, and sim-to-real tests.

## Open Questions

- What representation-space residuals should block physical action?
- How should a world-model checkpoint inherit deletion and provenance duties?
- Which comparator separates predictive state quality from controller quality?
