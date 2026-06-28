# Source Note: Mixtral of Experts

| Field | Value |
|---|---|
| Source ID | `ext_mixtral_2024` |
| Source title | Mixtral of Experts |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2401.04088, https://arxiv.org/abs/2401.04088 |
| Citation label | Jiang et al. (2024), Mixtral of Experts |
| Published / updated | 2024-01-08 / 2024-01-08 |
| DOI | 10.48550/arXiv.2401.04088 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the routing/MoE literature queue; paper not vendored into this repository and no model, benchmark, or inference result reproduced. |

## Thesis

Mixtral belongs in the routing, MoECOT, fast-generation, and resource-economics chapters as an external sparse-LLM example where each token activates only a subset of available experts. It helps the ASI Stack distinguish total parameter count, active parameter count, router selection, inference cost, and benchmark claims.

## Mechanisms

- Use sparse mixture-of-experts layers in a language model.
- Route each token to a subset of experts at each layer.
- Separate available parameters from active parameters during inference.
- Report source-scope model release, context-length, benchmark, and instruction-tuned results.

## Evidence

- The source reports a sparse MoE model and benchmark comparisons in the authors' setting.
- This repository has not downloaded Mixtral weights, run inference, reproduced benchmarks, measured active-parameter cost, or inspected router traces.
- Use this source as external sparse-LLM routing context, not as evidence for ASI Stack routing, MoECOT, or useful-solution-per-second claims.

## Failure Modes

- Active-parameter accounting can be mistaken for end-to-end efficiency without measuring memory, batching, routing overhead, and quality.
- Benchmark comparisons can hide prompt differences, contamination, serving constraints, or domain-specific failure modes.
- Token-level expert routing does not by itself provide authority, readiness, provenance, or rollback controls.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `moecot-runtime-and-multi-core-orchestration` (MoECOT Runtime and Multi-Core Orchestration)
- `fast-generation-architectures` (Fast Generation Architectures)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)

## Claims To Add Or Update

- Use this note to ground sparse LLM routing and active-parameter accounting.
- Do not claim local Mixtral inference, benchmark reproduction, route trace inspection, or speed-quality evidence.
- Keep support state at `argument` until a local model run, route measurement, or accepted evidence transition exists.

## Open Questions

- Which ASI Stack resource ledger fields distinguish total parameters, active parameters, router overhead, and output quality?
- What benchmark ratchet would compare sparse and dense routes without overfitting to public scores?
- How should MoECOT route receipts represent token-level routing versus task-level specialist selection?
