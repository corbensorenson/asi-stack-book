# Source Note: Frontier AI Regulation: Managing Emerging Risks to Public Safety

| Field | Value |
|---|---|
| Source ID | `ext_frontier_ai_regulation_2023` |
| Source title | Frontier AI Regulation: Managing Emerging Risks to Public Safety |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2307.03718, https://arxiv.org/abs/2307.03718 |
| Citation label | Anderljung et al. (2023), Frontier AI Regulation |
| Published / updated | 2023-07-06 / 2023-11-07 |
| DOI | 10.48550/arXiv.2307.03718 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the governance/evals literature queue; paper not vendored into this repository and no compliance process reproduced. |

## Thesis

This source belongs in the governance and release chapters as an external policy reference for frontier-model risk management. It helps the book connect internal readiness gates to public-safety controls without claiming regulatory compliance.

## Mechanisms

- Discuss standard setting, registration/reporting, and compliance mechanisms for frontier AI.
- Emphasize pre-deployment risk assessment and external scrutiny.
- Include post-deployment monitoring as part of ongoing risk management.
- Motivate release records that distinguish internal validation, external review, and deployment authority.

## Evidence

- The source contributes external governance and policy framing.
- This repository has not implemented a regulatory compliance regime, external audit, or deployment-monitoring system.
- Use it as comparison material for governance surfaces, not as evidence of compliance or safety.

## Failure Modes

- Confusing a book release or local validation run with regulatory compliance.
- Treating standards as static while frontier risk practices evolve.
- Omitting post-deployment monitoring and incident response from release planning.

## Book Chapters Supported

- `system-boundaries-and-authority` (System Boundaries and Authority)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `living-book-methodology` (Living Book Methodology)

## Claims To Add Or Update

- Use this note to frame release and readiness gates against external frontier-governance literature.
- Do not claim the ASI Stack is compliant with any specific law, standard, or regulator.
- Record external-review and release-artifact status separately from local render or validator status.

## Open Questions

- Which release records should distinguish internal review from external scrutiny?
- What public-safety residuals should be visible before any major version release?
- How should the book track changes in frontier-governance literature over time?
