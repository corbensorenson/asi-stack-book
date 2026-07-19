# Source Note: Energy and AI

| Field | Value |
|---|---|
| Source ID | `ext_iea_energy_and_ai_2025` |
| Source title | Energy and AI |
| Ingestion date | 2026-07-19 |
| Source version / URL | IEA 2025 report page and 2026 update pointers, https://www.iea.org/reports/energy-and-ai |
| Citation label | International Energy Agency (2025), Energy and AI |
| Published / updated | 2025-04-10 / update page inspected 2026-07-19 |
| Review state | Preliminary structural-gap note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official methodology summary, energy-demand, supply, security, emissions, affordability, and scenario passages inspected. Underlying datasets and every chapter of the full report were not independently audited or reproduced. |

## Thesis

AI compute is inseparable from data-centre, grid, generation, location, cooling,
and affordability constraints. The IEA's scenario structure is a useful
comparator for treating physical capacity and environmental externalities as
uncertain lifecycle records rather than an abstract token price.

## Mechanisms

- Global and regional data-centre electricity-demand scenarios.
- Separation of accelerated servers, conventional servers, other IT equipment,
  and cooling/infrastructure demand.
- Energy-supply, grid, location, efficiency, emissions, security, and
  affordability analysis.
- Base, higher-demand, constrained, and efficiency-sensitive cases.

## Evidence

The report uses IEA datasets, modelling, and consultations and publishes
scenario projections. Projections are not measurements of this book's stack,
and global shares can hide severe local grid, water, land, or affordability
constraints.

## Failure Modes

- Presenting one scenario as a forecast or physical capacity guarantee.
- Equating energy efficiency with lower total demand after rebound.
- Hiding local grid, cooling, water, emissions, or community effects in a global total.
- Treating purchased energy attributes as proof of physical or temporal supply.

## Book Chapters Supported

- Proposed: `physical-compute-infrastructure-energy-and-environmental-constraints`
- Existing boundaries: `resource-economics-and-token-budgets`,
  `personal-compute-hives-and-federated-edge-intelligence`,
  `ai-supply-chain-integrity-and-lifecycle-provenance`, and the proposed
  `governed-model-training-distributed-optimization-and-scaling`

## Claims To Add Or Update

- Bind compute demand to location, time, hardware, network, grid, generation,
  cooling, water, emissions, price, resilience, and affected-party records.
- Preserve scenario uncertainty and local constraints.
- Do not claim environmental benefit, capacity, transfer, or support movement.

## Open Questions

- Which workload-level measurements can reconcile with facility and grid records?
- How should rebound, marginal generation, congestion, and embodied materials be counted?
- What safe degraded modes exist when physical capacity or cooling is constrained?
