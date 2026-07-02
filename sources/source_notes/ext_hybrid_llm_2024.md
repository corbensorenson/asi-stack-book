# Source Note: Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing

| Field | Value |
|---|---|
| Source ID | `ext_hybrid_llm_2024` |
| Source title | Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2404.14618, https://arxiv.org/abs/2404.14618 |
| Citation label | Ding et al. (2024), Hybrid LLM |
| Published / updated | 2024-04-22 / 2024-04-22 |
| DOI | 10.48550/arXiv.2404.14618 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the routing/cost-quality literature queue; router code, benchmarks, quality predictors, and experiment outputs are not imported into this repository. |

## Thesis

Hybrid LLM belongs in the routing, resource-economics, readiness-gate, and benchmark chapters as an external reference for quality-aware query routing between small and large models. It helps the ASI Stack separate route choice, query difficulty, quality targets, and cost budgets.

## Mechanisms

- Route queries to a small or large model based on predicted query difficulty.
- Dynamically tune desired quality level at test time.
- Trade quality for cost according to scenario requirements.
- Evaluate large-model call reduction while tracking response quality.

## Evidence

- The source reports fewer large-model calls without response-quality loss in its own experiments.
- This repository has not run Hybrid LLM, reproduced its quality predictor, or tested any ASI Stack router against its benchmarks.
- Use the source as external quality/cost routing vocabulary, not as local routing evidence.

## Failure Modes

- Query-difficulty predictors can fail on safety-critical, adversarial, or provenance-heavy tasks.
- Quality/cost knobs can become hidden policy controls unless recorded and governed.
- Large-model-call reductions can hide loss of verification bandwidth or residual handling.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to ground quality-aware route-choice vocabulary.
- Do not claim ASI Stack route-quality preservation, cost reduction, or difficulty prediction without local evaluation.
- Keep support state at `argument` until route records, quality predictors, benchmark traces, or accepted evidence transitions exist.

## Open Questions

- Which route-record field should capture desired quality level and who authorized it?
- How should a router refuse cheap-model routing when verification, authority, or evidence burden is high?
- What benchmark fixture would catch route policies that save cost by silently dropping hard cases?
