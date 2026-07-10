# Source Note: DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

| Field | Value |
|---|---|
| Source ID | `ext_deepseek_r1_2025` |
| Source title | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2501.12948, https://arxiv.org/abs/2501.12948 |
| Citation label | DeepSeek-AI et al. (2025), DeepSeek-R1 |
| Published / updated | 2025-01-22 / 2026-01-04 |
| DOI | 10.1038/s41586-025-09422-z |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

DeepSeek-R1 belongs in the policy chapter as a reasoning-RL reference: reinforcement learning can shape long-form reasoning behavior, but that does not make reward, reasoning length, or benchmark gain equivalent to governed truth.

## Mechanisms

- Use reinforcement learning to incentivize reasoning behavior in large language models.
- Reduce dependence on extensive human-annotated demonstrations in the source framing.
- Evaluate reasoning capability through the paper's benchmark/reporting setup.
- Expose the need to separate reasoning behavior, reward design, benchmark transfer, and governance rights.

## Evidence

- The source reports reasoning-RL results and has a journal reference in the primary arXiv metadata. This repo has not reproduced DeepSeek-R1 training, evaluation, or model behavior.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Reasoning-length or benchmark rewards can produce overthinking, brittle traces, or hidden reward hacking.
- Reported model performance cannot be imported as local evidence without artifacts, commands, and reproduction boundaries.
- RL-shaped reasoning behavior does not prove truthfulness, corrigibility, authority compliance, or source grounding.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `governed-deliberation-and-test-time-scaling` (Governed Deliberation and Test-Time Scaling)

## Claims To Add Or Update

- Use this note to source-note reasoning-RL as an external method family. Do not use it to claim local reasoning-model capability.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.
- Treat reported self-reflection and verification behavior as source-setting
  reasoning-RL context, not as an independent verifier or local deliberation
  result.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
