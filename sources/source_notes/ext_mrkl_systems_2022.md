# Source Note: MRKL Systems

| Field | Value |
|---|---|
| Source ID | `ext_mrkl_systems_2022` |
| Source title | MRKL Systems: A Modular, Neuro-Symbolic Architecture That Combines Large Language Models, External Knowledge Sources and Discrete Reasoning |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2205.00445, https://arxiv.org/abs/2205.00445 |
| Citation label | Karpas et al. (2022), MRKL Systems |
| Published / updated | 2022-05-01 / 2022-05-01 |
| DOI | 10.48550/arXiv.2205.00445 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the opener external-positioning queue; paper not vendored into this repository and no MRKL system reproduced. |

## Thesis

MRKL Systems are an external comparator for modular architectures that combine language models with expert modules, external knowledge sources, and discrete reasoning components. They help position the ASI Stack opener against adjacent work that treats a model as one component inside a routed architecture rather than as the whole system.

## Mechanisms

- Combine neural language-model behavior with symbolic, calculator, retrieval, or expert modules.
- Route subtasks to specialized components instead of forcing a single model to solve every task internally.
- Use external knowledge and discrete reasoning machinery alongside LLM generation.
- Treat orchestration and module selection as architecture questions.

## Evidence

- The source proposes and evaluates a modular neuro-symbolic architecture under its own setup.
- This repository has not implemented MRKL routing, reproduced MRKL tasks, evaluated expert-module selection, or compared ASI Stack routing against MRKL.
- Use this source as a modular-architecture comparator, not as evidence that the ASI Stack works.

## Failure Modes

- Modular routing can hide authority, evidence, or residual ownership if the route record is not explicit.
- Expert modules can be overtrusted when their validity domain is unclear.
- A model-plus-tools architecture can still lack governance, claim ledgers, rollback, or support-state discipline.
- Routing success on one task family does not establish whole-stack safety or ASI capability.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model` (ASI Is a Stack, Not a Model)

## Claims To Add Or Update

- Use MRKL Systems to show that model-plus-module decomposition is established adjacent architecture vocabulary.
- Keep the ASI Stack distinction clear: it adds governance, authority ceilings, evidence states, rollback, and recursive-improvement boundaries beyond modular tool routing.
- Do not claim local MRKL reproduction or external validation of the ASI Stack.

## Open Questions

- Which ASI Stack route record fields would be needed to compare against MRKL-style module routing?
- Should future routing evidence use MRKL-style baselines for narrow tasks?
- What negative control would show that a routed module improved adequacy without widening authority?
