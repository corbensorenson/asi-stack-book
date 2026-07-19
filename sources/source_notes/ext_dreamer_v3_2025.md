# Source Note: Mastering diverse control tasks through world models

| Field | Value |
|---|---|
| Source ID | `ext_dreamer_v3_2025` |
| Source title | Mastering diverse control tasks through world models |
| Ingestion date | 2026-07-19 |
| Source version / URL | Nature 640, 647-653, https://www.nature.com/articles/s41586-025-08744-2 |
| Citation label | Hafner et al. (2025), Mastering diverse control tasks through world models |
| Published / updated | 2025-04-02 / 2025-04-02 |
| DOI | 10.1038/s41586-025-08744-2 |
| Ingestion basis | Primary open-access article abstract, architecture, evaluation scope, and limitations context inspected; code and reported task suite were not run locally. |

## Thesis

DreamerV3 learns an environment model, imagines action-conditioned futures,
and trains actor and critic components on those trajectories with one robust
configuration across many domains. It is a modern comparator for predictive
state as a reusable substrate, not proof that imagined outcomes remain grounded
under consequential deployment.

## Mechanisms

- Encode sensory input into discrete predictive state.
- Learn recurrent action-conditioned dynamics and reward predictions.
- Train actor and critic on imagined trajectories replayed from experience.
- Stabilize heterogeneous domains through normalization, balancing, and
  transformed losses.

## Evidence

The paper reports results across more than 150 control tasks and multiple
domains. The repository has not reproduced these results and imports no claim
about local model quality, transfer, or safety.

## Failure Modes

- Actor and critic can optimize shared world-model errors.
- Fixed hyperparameters do not imply fixed reliability across deployments.
- Aggregate task breadth can hide rare-event or tail-risk failures.
- Environment interaction and imagined learning can form self-confirming loops.

## Book Chapters Supported

- Proposed: `governed-world-models-and-reality-grounding`
- Existing boundary owners: `planning-as-a-control-layer`,
  `policy-optimization-and-learning-from-feedback`

## Claims To Add Or Update

- Keep world-model, policy, critic, observation, and evaluator identities
  independently versioned.
- Require disagreement and external-observation tests, not only imagined return.
- Measure task utility, grounding error, action risk, and governance cost jointly.

## Open Questions

- How should correlated world-model/critic error be detected?
- What independent observer can falsify a self-confirming rollout?
- Which error ledger is sufficient for safe degraded operation?
