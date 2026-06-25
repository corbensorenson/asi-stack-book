# Source Note: Fairness in Token Delegation

| Field | Value |
|---|---|
| Source ID | `ext_dao_delegation_fairness_2025` |
| Source title | Fairness in Token Delegation: Mitigating Voting Power Concentration in DAOs |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2510.05830, https://arxiv.org/abs/2510.05830 |
| Citation label | Messias and Ide (2025), Fairness in Token Delegation |
| Published / updated | 2025-10-07 / 2026-05-07 |
| DOI | 10.48550/arXiv.2510.05830 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the artifact-steward governance queue; paper not vendored into this repository and no DAO dataset was reproduced. |

## Thesis

This paper is relevant because artifact stewards must avoid collapsing contribution, money, reputation, and governance into one capture-prone surface. DAO delegation literature supplies concrete governance risks such as voter apathy, concentrated voting power, delegation misalignment, and ranking bias.

## Mechanisms

- Analyze DAO governance participation and delegation patterns.
- Link off-chain discussion participants to on-chain addresses.
- Extract governance interests with language-model methods.
- Compare token-holder priorities against delegate behavior.
- Examine how ranking interfaces can worsen concentration.

## Evidence

- The arXiv abstract reports empirical study of delegation in DAO governance forums and identifies voter apathy, power concentration, misaligned delegation, and visibility bias as governance problems.
- This repository has not reproduced the dataset, method, address linkage, or empirical results.
- Use this source as external governance-risk literature, not as a design proof for the steward ledger.

## Failure Modes

- Delegation interfaces can concentrate authority among already-visible actors.
- Token-weighted governance can diverge from participant intent.
- AI-awarded reputation can become its own capture channel if not audited.

## Book Chapters Supported

- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use this note to support anti-capture design concerns and separated ledgers.
- Do not claim that the book's proposed governance records solve DAO capture without tests or formal models.

## Open Questions

- Which contribution-ledger fields make capture visible before it is irreversible?
- Should governance rights decay, cap, or require diverse review?
- How should fork and exit rights appear in a steward charter?
