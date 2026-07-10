# Source Note: Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision

| Field | Value |
|---|---|
| Source ID | `ext_weak_to_strong_generalization_2023` |
| Source title | Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:2312.09390, https://arxiv.org/abs/2312.09390 |
| Citation label | Burns et al. (2023), Weak-to-Strong Generalization |
| Published / updated | 2023-12-14 / 2023-12-14 |
| DOI | 10.48550/arXiv.2312.09390 |
| Ingestion basis | Primary arXiv HTML paper inspected for its weak/strong supervisor setup, held-out ceiling comparison, reported task settings, and stated disanalogies. No model, supervisor, label set, training run, evaluator, or reported result was reproduced in this repository. |

## Thesis

The paper frames a present-day weak-to-strong learning experiment as an analogy
to supervising systems whose behavior outstrips a supervisor's ability to
evaluate it. It compares weak-supervisor performance, weak-to-strong student
performance, and a strong-model ground-truth ceiling under specified tasks. The
paper reports positive but incomplete weak-to-strong generalization and states
that its setup retains important disanalogies to supervising future
superhuman systems.

## Mechanisms

- Define a task, weak supervisor, strong student, held-out outcome measure, and
  a strong model trained with ground-truth labels as a ceiling for the source
  experiment.
- Separate performance recovered from the weak supervisor's own performance and
  from the strong ceiling rather than treating a student improvement as complete
  oversight.
- Study weak-model labels across specified NLP, chess, and reward-modeling
  settings, then compare auxiliary-loss, bootstrapping, and representation
  interventions within that source setup.
- Record the paper's stated limits: methods do not work consistently in all
  settings, reward-modeling recovery remains incomplete, and model-model
  experiments differ from human supervision of superhuman systems.

## Evidence

- The primary paper reports its own model-family, task, weak-label, ceiling,
  and evaluation results. It reports that naive weak supervision can exceed the
  weak supervisor in its studied settings while leaving a gap to its strong
  ceiling.
- The paper explicitly presents the work as a proof of concept rather than a
  deployment recommendation and names imitation saliency and pretraining
  leakage as remaining disanalogies.
- This repository has not trained a weak supervisor or strong student, created a
  held-out ceiling, measured calibration, audited labels, or reproduced any
  paper result. This source is a scoped experimental-design comparator only.

## Failure Modes

- A student can inherit or conceal a weak supervisor's errors while appearing to
  improve on a selected aggregate metric.
- A ceiling evaluated with ground truth available to researchers can fail to
  model the inaccessible truth conditions that motivate scalable oversight.
- Pretraining leakage or shared model-family assumptions can make a source
  experiment easier than the target oversight problem.
- A weak-to-strong score can be misread as a guarantee of honest elicitation,
  alignment, safety, or authority to deploy.

## Book Chapters Supported

- `scalable-oversight-and-adversarial-ai-control` (Scalable Oversight and Adversarial AI Control)

## Claims To Add Or Update

- Use this note for a capability-gap envelope, independent outcome-audit
  requirement, ceiling/baseline comparison, and explicit disanalogy record.
- Keep weak-supervisor quality, student behavior, and downstream authority as
  different questions.
- Do not claim local weak-to-strong generalization, reliable elicitation,
  alignment, safety, calibration, or ASI.

## Open Questions

- Which public-safe workload can compare direct review, assisted review, and
  adjudicated outcome while preserving a held-out reference and a residual
  record?
- How can an oversight record name a supervisor's capability gap and shared
  failure risks without inventing a scalar capability measurement?
- What independent review is needed before an AI-assisted oversight result can
  influence a high-risk planning or training decision?
