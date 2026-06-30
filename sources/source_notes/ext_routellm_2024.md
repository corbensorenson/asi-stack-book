# Source Note: RouteLLM: Learning to Route LLMs with Preference Data

| Field | Value |
|---|---|
| Source ID | `ext_routellm_2024` |
| Source title | RouteLLM: Learning to Route LLMs with Preference Data |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2406.18665, https://arxiv.org/abs/2406.18665 |
| Citation label | Ong et al. (2024), RouteLLM |
| Published / updated | 2024-06-26 / 2025-02-23 |
| DOI | 10.48550/arXiv.2406.18665 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the learned-routing literature queue; router models, preference data, benchmarks, and transfer experiments are not imported into this repository. |

## Thesis

RouteLLM belongs in the routing, MoECOT, resource-economics, and policy-optimization chapters as an external reference for learned routers that choose between stronger and weaker LLMs. It helps the ASI Stack frame routing policy as a learned control surface that must still be governed by support, authority, budget, and residual records.

## Mechanisms

- Train router models using human preference data and data augmentation.
- Dynamically select between stronger and weaker LLMs at inference time.
- Optimize cost-quality tradeoffs.
- Evaluate transfer when the strong and weak model pair changes.

## Evidence

- The source reports cost reductions and transfer behavior in its own benchmark setting.
- This repository has not trained RouteLLM, imported preference data, reproduced benchmarks, or tested router transfer.
- Use the source as external learned-router vocabulary, not as evidence for MoECOT or ASI Stack routing quality.

## Failure Modes

- Preference-data routing can inherit preference bias or benchmark artifacts.
- Transfer across model pairs can fail when task, safety, or provenance requirements change.
- Learned route policies can optimize cost-quality scores while ignoring authority, rollback, or evidence obligations.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to compare ASI Stack routing policy with learned LLM router models.
- Do not claim learned routing, preference-transfer, cost reductions, or quality preservation for ASI Stack without local artifacts.
- Keep support state at `argument` until route-policy training records, benchmark traces, transfer tests, or accepted evidence transitions exist.

## Open Questions

- What policy-update record should govern a learned route policy before deployment?
- Which residual ledger fields reveal when a cheap route failed silently?
- How should route transfer be blocked when model-pair changes alter authority or evidence boundaries?
