# Source Note: Machine Unlearning

| Field | Value |
|---|---|
| Source ID | `ext_bourtoule_machine_unlearning_2021` |
| Source title | Machine Unlearning |
| Ingestion date | 2026-07-10 |
| Source version / URL | 42nd IEEE Symposium on Security and Privacy (2021), pp. 141-159; primary author manuscript, https://arxiv.org/abs/1912.03817; DOI https://doi.org/10.1109/SP40001.2021.00019 |
| Citation label | Bourtoule et al. (2021), Machine Unlearning |
| Published / updated | 2021-05-24 / 2021-05-24 |
| DOI | 10.1109/SP40001.2021.00019 |
| Ingestion basis | Primary proceedings metadata and primary-paper passages on definitions, SISA design, evaluation, and limitations reviewed; neither code nor checkpoints were run or imported. |

## Thesis

Bourtoule et al. frame machine unlearning as removing a specified training
point's influence without always retraining from scratch. Their SISA approach
pre-structures training through sharding, isolation, slicing, and aggregation
so a deletion can restart only the affected constituent-model path.

## Mechanisms

- Partition a dataset into disjoint shards; train constituent models in
  isolation so a point's influence is bounded to its shard.
- Partition each shard into ordered slices and save intermediate model states;
  a deletion can restart before the slice containing the deleted point.
- Aggregate constituent-model outputs at inference rather than mixing training
  gradients across shards.
- Measure unlearning as a trade-off among retraining time, storage, accuracy,
  deletion-request distribution, and model/task complexity.

## Evidence

- The paper defines and evaluates SISA on multiple datasets and reports
  retraining-time and accuracy trade-offs in its own experimental settings.
- Its reported gains and accuracy effects are conditional on its datasets,
  request regime, partitioning, architectures, and aggregation choices.
- This repository has not run SISA, reproduced a deletion request, verified
  removal from model parameters, or measured utility, privacy, or cost.

## Failure Modes

- Deletion capability is not equivalent to privacy, and data removal does not
  by itself show that all derived representations or downstream artifacts have
  been removed.
- More sharding can improve bounded deletion cost while degrading accuracy,
  especially for complex tasks or many deletion requests.
- SISA depends on training-time structure and saved states; it is not a generic
  after-the-fact proof that an arbitrary model has forgotten a datum.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and
  Learning from Feedback)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and
  Cognitive Loop Closure)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and
  Anti-Goodhart Evidence)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and
  Bibliography Plan)

## Claims To Add Or Update

- Treat an update-data receipt as incomplete unless it records provenance,
  affected artifact/version, deletion or retention request, method, evaluation,
  remaining derived-artifact scope, and unresolved residuals.
- Do not equate a request, a routing decision, or a SISA-style retraining path
  with verified parametric deletion, privacy compliance, or an LLM unlearning
  result.
- Route a future Data Engines, Continual Learning, and Unlearning chapter
  through an explicit deletion-verification boundary rather than a generic
  "forget" command.

## Open Questions

- What evidence would verify deletion across checkpoints, adapters, caches,
  retrieval stores, distilled models, and published artifacts?
- Which deletion requests should require full retraining rather than a bounded
  localized method?
- How should a governed data engine represent the accuracy, latency, and
  residual-information cost of a deletion decision?
