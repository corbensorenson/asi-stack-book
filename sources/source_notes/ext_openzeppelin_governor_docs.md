# Source Note: OpenZeppelin Contracts - Governance

| Field | Value |
|---|---|
| Source ID | `ext_openzeppelin_governor_docs` |
| Source title | OpenZeppelin Contracts: Governance |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://docs.openzeppelin.com/contracts/5.x/api/governance |
| Citation label | OpenZeppelin Contracts Docs, Governance |
| Published / updated | unknown / unknown |
| Ingestion basis | Official public documentation inspected for the artifact-steward external literature queue; no contract was deployed or audited from this repository. |

## Thesis

OpenZeppelin Governor is relevant as a concrete governance machinery reference: proposals, votes, quorum, timelocks, and guardian-style controls can inform steward governance boundaries, but they do not automatically solve project legitimacy or capture risk.

## Mechanisms

- Provide modular Governor contracts for on-chain voting protocols.
- Use votes modules to define voting power and quorum.
- Use counting modules to define voting options and vote counting behavior.
- Use timelock extensions to delay execution through queue and execute steps.
- Provide settings and guardian-style extensions for proposal lifecycle controls.

## Evidence

- The official docs describe Governor core contracts, voting modules, quorum modules, timelock extensions, proposal settings, and guardian cancellation patterns.
- This repository has not deployed, audited, or simulated any OpenZeppelin governance contract.
- Use this source for governance-design vocabulary, not as proof that a steward treasury is safe or legal.

## Failure Modes

- On-chain voting can confuse token ownership with project legitimacy.
- Timelocks and guardians can be misconfigured or captured.
- Legal, tax, and fiduciary questions remain outside the contract interface.

## Book Chapters Supported

- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use this note to ground proposal/vote/quorum/timelock/guardian vocabulary in the steward chapter.
- Keep treasury and governance claims at `argument` until policy models and legal review exist.

## Open Questions

- Which steward actions should require timelock, maintainer approval, or guardian veto?
- How should non-transferable reputation interact with formal voting systems?
- Which governance actions must remain off-chain and human-approved?
