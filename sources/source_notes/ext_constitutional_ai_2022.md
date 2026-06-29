# Source Note: Constitutional AI: Harmlessness from AI Feedback

| Field | Value |
|---|---|
| Source ID | `ext_constitutional_ai_2022` |
| Source title | Constitutional AI: Harmlessness from AI Feedback |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2212.08073, https://arxiv.org/abs/2212.08073 |
| Citation label | Bai et al. (2022), Constitutional AI |
| Published / updated | 2022-12-15 / 2022-12-15 |
| DOI | 10.48550/arXiv.2212.08073 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the external constitutional-AI grounding queue; paper not vendored into this repository and no training run, preference model, or RL result reproduced. |

## Thesis

This source is the direct external comparator for the book's constitutional-alignment substrate. It frames a rule or principle list as the source of feedback for training a harmless assistant, which gives the ASI Stack a concrete baseline for distinguishing constitutional principles, revision feedback, and model-behavior training from the book's broader operational-predicate layer.

## Mechanisms

- Use a list of rules or principles as the oversight surface for harmlessness training.
- Separate supervised revision from a reinforcement-learning phase using AI feedback.
- Treat constitutional principles as inputs to feedback generation rather than as an automatic proof of alignment.
- Provide a contrast between model-training constitutions and ASI Stack runtime constitutional predicates, migration records, and self-improvement gates.

## Evidence

- The source contributes external constitutional-AI framing and an experimental training method.
- This repository has not reproduced the training pipeline, imported the paper's datasets or models, evaluated harmlessness, or compared ASI Stack records to its experimental results.
- Use it as external literature for constitutional-AI positioning, not as evidence that the ASI Stack implements Constitutional AI or achieves harmlessness.

## Failure Modes

- Treating a principle list as sufficient alignment rather than as one input to training or governance.
- Confusing model-behavior training with runtime authority control, tool gating, or self-modification safety.
- Overstating harmlessness or constitutional validity without independent evaluation.

## Book Chapters Supported

- `constitutional-alignment-substrate` (Constitutional Alignment Substrate)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to compare the ASI Stack constitutional substrate with external Constitutional AI work.
- Keep the ASI Stack claim at `argument` support unless future evidence shows executable constitutional predicates surviving planning, runtime, and self-improvement pressure.
- Do not claim that constitutional-predicate fixtures reproduce Constitutional AI training results.

## Open Questions

- Which constitutional principles can become operational predicates rather than training-time prompts?
- What evidence would be needed to compare runtime constitutional gates with model-level harmlessness improvements?
- How should public, institutional, or stakeholder input alter predicate migration rules?
