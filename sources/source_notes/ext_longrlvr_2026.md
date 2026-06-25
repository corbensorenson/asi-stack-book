# Source Note: LongRLVR: Long-Context Reinforcement Learning Requires Verifiable Context Rewards

| Field | Value |
|---|---|
| Source ID | `ext_longrlvr_2026` |
| Source title | LongRLVR: Long-Context Reinforcement Learning Requires Verifiable Context Rewards |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2603.02146, https://arxiv.org/abs/2603.02146 |
| Citation label | Chen et al. (2026), LongRLVR |
| Published / updated | 2026-03-02 / 2026-03-02 |
| DOI | 10.48550/arXiv.2603.02146 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

LongRLVR is directly relevant to VCM policy learning: final-answer reward alone can be inadequate when the task requires finding and reasoning over externally supplied context.

## Mechanisms

- Analyze RLVR failure in long-context settings where contextual grounding matters.
- Argue for verifiable context rewards rather than relying only on final-answer correctness.
- Connect reward design to retrieval, grounding, and context-use behavior.
- Map to ASI Stack context-policy rewards and adequacy records.

## Evidence

- The source reports long-context RLVR observations. This repo has not reproduced LongRLVR or run context-grounding reward experiments.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Final-answer rewards can allow models to ignore supplied context or rely on parametric shortcuts.
- Context rewards can be gamed if citation, grounding, or retrieval checks are shallow.
- Long-context improvements must still be separated from verifier bandwidth and context adequacy.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note verifiable context rewards for VCM/context-policy updates. Do not promote VCM learning claims without local tests.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
