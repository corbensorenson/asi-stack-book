# Source Note: 2024 United States Data Center Energy Usage Report

| Field | Value |
|---|---|
| Source ID | `ext_lbnl_data_center_energy_2024` |
| Source title | 2024 United States Data Center Energy Usage Report |
| Ingestion date | 2026-07-19 |
| Source version / URL | LBNL publication record and report abstract, https://energyanalysis.lbl.gov/publications/2024-lbnl-data-center-energy-usage-report |
| Citation label | Shehabi et al. (2024), United States Data Center Energy Usage Report |
| Published / updated | 2024-12-19 / 2024-12-19 |
| DOI | 10.71468/P1WC7Q |
| Review state | Preliminary structural-gap note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official LBNL metadata and abstract plus indexed report passages identifying historical electricity, scenario, infrastructure, and water accounting. The full model and source datasets were not reproduced locally. |

## Thesis

Facility-level AI capability depends on a physical data-centre system whose
energy and water demand changes with equipment, utilization, cooling, and power
supply. The report supplies a national infrastructure comparator, not a direct
measurement of a particular AI model or an ASI requirement.

## Mechanisms

- Historical US data-centre electricity estimation from prior studies and
  equipment-shipment data.
- Scenario ranges through 2028 rather than one deterministic forecast.
- Equipment and infrastructure accounting, including cooling and water in the
  full report's scope.
- Congressional/DOE reporting boundary with explicit geographic scope.

## Evidence

The reviewed record establishes the report's historical and scenario method.
It cannot isolate every AI workload and does not establish future generation,
transmission, site, cooling, water, community, or supply-chain availability.

## Failure Modes

- Mapping national data-centre totals directly to AI or one model run.
- Ignoring uncertainty ranges, utilization, embodied hardware, or indirect water.
- Treating nameplate compute or power as usable, resilient delivered capacity.
- Generalizing US facility conditions to other grids, climates, or jurisdictions.

## Book Chapters Supported

- Proposed: `physical-compute-infrastructure-energy-and-environmental-constraints`
- Existing boundaries: `resource-economics-and-token-budgets`,
  `model-weight-custody-and-hardware-roots-of-trust`,
  `ai-supply-chain-integrity-and-lifecycle-provenance`, and
  `governed-operations-incident-command-and-graceful-degradation`

## Claims To Add Or Update

- Separate model/workload energy from facility overhead, water, grid, and
  lifecycle effects.
- Keep observed, estimated, allocated, and projected resource use distinct.
- Do not infer capacity, sustainability, resilience, or support movement.

## Open Questions

- How should workload receipts reconcile with facility and utility meters?
- Which capacity, cooling, network, and grid failures must narrow authority?
- How should water, land, materials, decommissioning, and community costs enter?
