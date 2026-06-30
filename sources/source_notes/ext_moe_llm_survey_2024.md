# Source Note: A Survey on Mixture of Experts in Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_moe_llm_survey_2024` |
| Source title | A Survey on Mixture of Experts in Large Language Models |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2407.06204, https://arxiv.org/abs/2407.06204 |
| Citation label | Cai et al. (2024), MoE LLM Survey |
| Published / updated | 2024-06-26 / 2025-04-09 |
| DOI | 10.48550/arXiv.2407.06204 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the routing/MoE literature queue; survey not vendored into this repository and no surveyed implementation or benchmark reproduced. |

## Thesis

This survey belongs in the routing, MoECOT, resource-economics, and open-research chapters as an external map of LLM mixture-of-experts taxonomy, algorithmic design, systemic constraints, implementations, empirical evaluation patterns, and open directions. It helps the ASI Stack avoid treating one sparse model or routing method as the whole MoE design space.

## Mechanisms

- Organize MoE designs by architecture, routing, training, systems, applications, and evaluation concerns.
- Compare algorithmic and systemic choices as part of the same model-scaling design space.
- Track open-source implementations, hyperparameter configurations, and empirical-evaluation patterns.
- Record open research directions rather than reducing MoE to a single expert-router mechanism.

## Evidence

- The source is a survey of MoE literature for large language models.
- This repository has not independently checked every surveyed paper, reproduced surveyed experiments, or validated a MoECOT-to-MoE taxonomy.
- Use this source as a map for future source selection and terminology, not as direct evidence for ASI Stack routing claims.

## Failure Modes

- A survey can make coverage look complete while individual claims still need primary-source passage review.
- MoE taxonomy can be over-applied to task-level, agent-level, or governance-level routing without respecting interface differences.
- Reported empirical trends can become stale as model releases, training recipes, and serving systems change.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to plan deeper MoE source normalization and vocabulary.
- Do not use this survey alone to support novelty, performance, or implementation claims.
- Keep support state at `argument` until primary sources, local runs, route traces, or accepted evidence transitions exist.

## Open Questions

- Which MoE design axes correspond to ASI Stack task routing rather than token routing?
- What sources are needed to compare MoECOT with modular-agent orchestration rather than model-internal MoE?
- How often should external MoE survey coverage be refreshed before a major version release?
