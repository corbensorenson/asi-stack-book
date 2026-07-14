# Source Note: Faithfulness as Information Flow

| Field | Value |
|---|---|
| Source ID | `ext_faithfulness_information_flow_2026` |
| Source title | Faithfulness as Information Flow: Evaluating and Training Faithful Chain-of-Thought Reasoning |
| Ingestion date | 2026-07-14 |
| Source version / URL | arXiv:2605.24286v1, https://arxiv.org/abs/2605.24286 |
| Citation label | Jia, Benton, and Easley (2026), Faithfulness as Information Flow |
| Published / updated | 2026-05-22 / 2026-05-22 |
| DOI | 10.48550/arXiv.2605.24286 |
| Ingestion basis | Primary arXiv HTML passages reviewed at Abstract and Sections 1, 3, 4, 6.3, and Limitations; code and models were not run locally. |

## Thesis

A visible chain of thought is useful for monitoring only when answer-relevant
information actually flows through it. The paper separates three properties:
the trace can contain enough information to predict the answer (sufficiency),
capture the answer-relevant prompt information rather than leave a shortcut
(completeness), and causally affect the answer (necessity). A transcript alone
cannot establish the last property.

## Mechanisms

- Treat prompt-to-answer shortcuts as a distinct path that can bypass a
  plausible trace (Sections 1 and 3; HTML lines 76-139).
- Evaluate sufficiency, completeness, and necessity with separate entropy,
  structural-mask, and gradient diagnostics (Section 4; HTML lines 140-183).
- Stress the trace with counterfactual edits or interventions; necessity is
  interventional rather than readable from prose alone (Section 3; HTML
  lines 130-139).
- Test whether reward-hacking behavior is visible in the trace instead of
  accepting visible-test reward as adequate evidence (Section 6.3; HTML
  lines 244-252).

## Evidence

The paper reports bounded experiments on hinted arithmetic, reward-hackable
code repair, and DAPO-Math under injected wrong hints. It supplies a primary
causal-faithfulness comparator and training intervention family. This
repository did not reproduce the models, metrics, or interventions.

## Failure Modes

- A trace can be sufficient but not necessary: a plausible post-hoc rationale.
- Completeness can hold degenerately when outputs carry little information.
- KL diagnostics can be confounded in low-entropy regimes.
- Reference-model measurements characterize an observer/model pair rather than
  prove the generating model's internal causal reliance.
- Making reward hacking visible is not the same as eliminating it.

## Book Chapters Supported

- `artifact-graphs-audit-logs-and-replay`
- `adversarial-evaluation-sandbagging-and-training-time-deception`
- `governed-deliberation-and-test-time-scaling`
- `policy-optimization-and-learning-from-feedback`

## Claims To Add Or Update

- Keep private reasoning, reported rationale, action trace, receipt,
  monitorability evidence, and authoritative effect as separate objects.
- Require trace/action inconsistency and hidden-computation controls.
- Never use a chain of thought as execution permission or authoritative receipt.
- Preserve all affected chapter-core support states at `argument`.

## Open Questions

- Which trace perturbations remain meaningful across tool-using and
  multi-agent routes?
- How should an evaluator distinguish a faithful but unsafe rationale from an
  unfaithful but harmless one?
- What evidence can be retained without exposing sensitive private reasoning?
