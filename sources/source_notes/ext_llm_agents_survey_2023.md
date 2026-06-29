# Source Note: Survey on LLM-based Autonomous Agents

| Field | Value |
|---|---|
| Source ID | `ext_llm_agents_survey_2023` |
| Source title | A Survey on Large Language Model based Autonomous Agents |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2308.11432, https://arxiv.org/abs/2308.11432 |
| Citation label | Wang et al. (2023), Survey on LLM-based Autonomous Agents |
| Published / updated | 2023-08-22 / 2024-09-22 |
| DOI | 10.48550/arXiv.2308.11432 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the opener external-positioning queue; survey not vendored into this repository and no surveyed agent system reproduced. |

## Thesis

The LLM-agent survey is an external comparator for decomposing language-model agents into architecture components such as profile, memory, planning, and action. It helps position the ASI Stack opener against current agent-system language while keeping the ASI Stack's governance and evidence machinery distinct.

## Mechanisms

- Treat an autonomous agent as more than raw model inference.
- Organize agent systems around profile, memory, planning, and action components.
- Survey application domains, benchmarks, and challenges for LLM-based agents.
- Make agent architecture a systems question rather than only a model-size question.

## Evidence

- The source surveys agent architectures and component patterns in the LLM-agent literature.
- This repository has not reproduced any surveyed benchmark, implemented a surveyed agent system, or validated ASI Stack behavior against the survey's taxonomy.
- Use this source as adjacent architecture vocabulary, not support-state evidence.

## Failure Modes

- Agent-component taxonomies can omit authority, evidence, rollback, or human-governance boundaries.
- Memory and planning modules can appear systematic while remaining unverified or unaudited.
- Benchmarks for agents can overstate deployment readiness or safety.
- Survey taxonomy can be mistaken for evidence that a specific architecture works.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model` (ASI Is a Stack, Not a Model)

## Claims To Add Or Update

- Use the survey to position the opener against established LLM-agent decomposition into memory, planning, and action components.
- Emphasize that the ASI Stack is stricter than generic agent architecture because it requires authority ceilings, evidence states, typed artifacts, and rollback paths.
- Do not claim reproduction of surveyed systems or benchmarks.

## Open Questions

- Which survey component categories align cleanly with the ASI Stack parts, and which need stricter governance fields?
- Which agent benchmark could serve as a future evidence lane without encouraging benchmark overclaim?
- How should surveyed memory/planning/action failures map to ASI Stack residual records?
