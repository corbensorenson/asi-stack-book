# Source Note: Mixture-of-Experts with Expert Choice Routing

| Field | Value |
|---|---|
| Source ID | `ext_expert_choice_routing_2022` |
| Source title | Mixture-of-Experts with Expert Choice Routing |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2202.09368, https://arxiv.org/abs/2202.09368 |
| Citation label | Zhou et al. (2022), Expert Choice Routing |
| Published / updated | 2022-02-18 / 2022-10-14 |
| DOI | 10.48550/arXiv.2202.09368 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the routing/MoE literature queue; paper not vendored into this repository and no pretraining or task result reproduced. |

## Thesis

Expert Choice Routing belongs in the routing, MoECOT, resource-economics, and readiness-gate chapters as an external reference for routing strategy as a first-class performance and load-balancing mechanism. It gives the ASI Stack a concrete comparison point for token/expert assignment direction and capacity constraints without implying that MoECOT implements expert-choice routing.

## Mechanisms

- Change the routing direction so experts select tokens rather than only letting tokens select experts.
- Fix expert bucket capacity while allowing tokens to be routed to a variable number of experts.
- Address load imbalance and undertraining or overspecialization of experts as routing failure modes.
- Report training-convergence and downstream-task results in the source paper's own setting.

## Evidence

- The source reports a routing method and paper-scope comparisons against prior MoE routing strategies.
- This repository has not trained an MoE, reproduced routing experiments, imported code, or measured MoECOT routing behavior.
- Use this source for external routing vocabulary and failure modes, not as local evidence for specialist-core routing quality.

## Failure Modes

- Load-balancing objectives can conflict with competence, safety, cost, or authority constraints.
- A routing strategy can improve training metrics while hiding expert specialization collapse or unsafe route choices.
- Source-reported convergence and benchmark results cannot justify ASI Stack route promotion without reproduction and scoped artifacts.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `moecot-runtime-and-multi-core-orchestration` (MoECOT Runtime and Multi-Core Orchestration)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)

## Claims To Add Or Update

- Use this note to ground external expert-routing and load-balancing vocabulary.
- Do not claim local expert-choice routing, MoE training, convergence improvement, or benchmark reproduction.
- Keep support state at `argument` until route traces, training/evaluation runs, or accepted evidence transitions exist.

## Open Questions

- Which ASI Stack route records should carry load, capacity, competence, cost, and authority fields together?
- What fixture would expose load-balancing wins that violate readiness or authority gates?
- How should residual escrow record an expert-route failure caused by load pressure?
