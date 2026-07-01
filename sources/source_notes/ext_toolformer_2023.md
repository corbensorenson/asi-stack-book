# Source Note: Toolformer: Language Models Can Teach Themselves to Use Tools

| Field | Value |
|---|---|
| Source ID | `ext_toolformer_2023` |
| Source title | Toolformer: Language Models Can Teach Themselves to Use Tools |
| Ingestion date | 2026-07-01 |
| Source version / URL | arXiv:2302.04761, https://arxiv.org/abs/2302.04761 |
| Citation label | Schick et al. (2023), Toolformer |
| Published / updated | 2023-02-09 / 2023-02-09 |
| DOI | 10.48550/arXiv.2302.04761 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the procedural-memory and tool-use comparator queue; paper, code, training data, API traces, and evaluations are not imported into this repository. |

## Thesis

Toolformer belongs in the procedural-memory, runtime-adapter, and policy-optimization comparison set as an external learned-tool-use reference. It helps the ASI Stack distinguish learning when to call tools from governing whether a learned tool invocation is allowed, recorded, replayed, and eligible for evidence use.

## Mechanisms

- Train a language model to decide which external APIs to call, when to call them, what arguments to pass, and how to incorporate API results.
- Use a small number of demonstrations for each API to create self-supervised tool-use data.
- Incorporate APIs such as calculation, question answering, search, translation, and calendar lookup.
- Preserve general language-modeling ability while improving selected downstream tasks in the source setting.

## Evidence

- The source reports zero-shot improvements in its own downstream task setup.
- This repository has not trained Toolformer, imported its training pipeline, replayed API-call traces, reproduced any scores, or evaluated ASI Stack tool routing against Toolformer.
- Use this source for learned-tool-use vocabulary and prior-art positioning, not as evidence that Procedural Memory, Runtime Adapters, or Policy Optimization work.

## Failure Modes

- Learned API use can improve task behavior while leaving authority, approval, sandbox, and receipt boundaries implicit.
- A model may learn when a tool is useful without preserving proof that the tool result is trustworthy, replayable, or claim-relevant.
- API-call training data can encode overbroad tool-use habits if negative examples, residuals, and non-claims are not preserved.

## Book Chapters Supported

- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use Toolformer to compare ASI Stack procedural memory against learned external-tool-use approaches.
- Keep the ASI Stack distinction clear: tool-use skill is not the same as governed permission, replay, regression preservation, or support-state promotion.
- Do not claim local Toolformer reproduction, API-call training, downstream-task improvement, model-quality result, or tool-safety result.

## Open Questions

- Which procedural-memory record should preserve the demonstrations, generated calls, accepted calls, rejected calls, and tool-result residuals?
- How should runtime-adapter receipts constrain a learned tool-use policy before it becomes routable?
- What negative control would show that a learned tool-use habit improves utility without widening authority or laundering evidence?
