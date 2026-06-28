# Source Note: FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

| Field | Value |
|---|---|
| Source ID | `ext_frugalgpt_2023` |
| Source title | FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2305.05176, https://arxiv.org/abs/2305.05176 |
| Citation label | Chen et al. (2023), FrugalGPT |
| Published / updated | 2023-05-09 / 2023-05-09 |
| DOI | 10.48550/arXiv.2305.05176 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the routing/cost literature queue; code, datasets, query collections, and cost/accuracy experiments are not imported into this repository. |

## Thesis

FrugalGPT belongs in the routing, MoECOT, resource-economics, and efficiency chapters as an external reference for LLM cascades and query-specific model selection. It helps the ASI Stack discuss routing as an economic control surface rather than only a model-internal mixture-of-experts mechanism.

## Mechanisms

- Compare LLM API costs and note heterogeneous pricing structures.
- Reduce inference cost through prompt adaptation, LLM approximation, and LLM cascades.
- Learn which combinations of LLMs to use for different queries.
- Treat cost and accuracy as coupled routing objectives.

## Evidence

- The source reports cost and accuracy tradeoffs in its own experiments.
- This repository has not run FrugalGPT, imported query data, reproduced costs, or evaluated ASI Stack route decisions.
- Use the source as external task-routing vocabulary, not as evidence for efficient ASI routing.

## Failure Modes

- Routing for cost can discard verification, provenance, or authority requirements if those fields are not part of the route record.
- Cascade results can depend on specific model pricing, prompts, and datasets.
- Reported cost reductions cannot be imported into MoECOT or ASI Stack route-efficiency claims without local traces.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `moecot-runtime-and-multi-core-orchestration` (MoECOT Runtime and Multi-Core Orchestration)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)

## Claims To Add Or Update

- Use this note to compare ASI Stack routing against cost-aware LLM cascades.
- Do not claim local cost savings, accuracy gains, or route optimality without reproduced route logs and cost records.
- Keep support state at `argument` until routing traces, budget ledgers, benchmark records, or accepted evidence transitions exist.

## Open Questions

- What costed-route receipt should record prompt adaptation, fallback, and model-cascade decisions?
- How should verification and authority constraints override a cheaper route?
- Which benchmark ratchet prevents cascades from optimizing only visible accuracy?
