# Source Note: Tree of Thoughts: Deliberate Problem Solving with Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_tree_of_thoughts_2023` |
| Source title | Tree of Thoughts: Deliberate Problem Solving with Large Language Models |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2305.10601, https://arxiv.org/abs/2305.10601 |
| Citation label | Yao et al. (2023), Tree of Thoughts |
| Published / updated | 2023-05-17 / 2023-12-03 |
| DOI | 10.48550/arXiv.2305.10601 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the planning/search literature queue; paper not vendored into this repository and no task result reproduced. |

## Thesis

Tree of Thoughts belongs in the planning chapters as an external reference for deliberative search over intermediate reasoning units. It strengthens the distinction between linear text continuation and explicit plan/search control.

## Mechanisms

- Represent intermediate reasoning units as thoughts.
- Explore multiple candidate reasoning paths.
- Evaluate and select paths during inference.
- Allow lookahead and backtracking when needed.

## Evidence

- The source reports improvements on selected planning/search tasks in its experimental setup.
- This repository has not reproduced Game of 24, creative writing, crossword tasks, prompts, or model scores.
- Use it as external context for search-control vocabulary, not as evidence for PlanForge behavior.

## Failure Modes

- Search can amplify evaluator bias or scoring artifacts.
- Branching reasoning can look systematic while still missing source grounding.
- Task-specific gains cannot be imported into execution-contract or benchmark-ratchet claims.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer: DAGs and Intelligence Arbitrage)
- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `governed-deliberation-and-test-time-scaling` (Governed Deliberation and Test-Time Scaling)

## Claims To Add Or Update

- Use this note to source external planning/search vocabulary.
- Do not claim the ASI Stack implements Tree of Thoughts or reproduces its results.
- Keep support state at `argument` until deterministic plan-graph tests or accepted transitions exist.
- Use this source to distinguish a bounded search procedure from an authority,
  correctness, safety, or deployment decision.

## Open Questions

- What is the smallest PlanForge DAG fixture that can test branch generation, scoring, and backtracking?
- Which evaluator records should prevent search from becoming benchmark gaming?
- How should failed branches become residual evidence instead of disappearing?
