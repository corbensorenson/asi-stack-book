# Source Note: The Simplex Architecture

| Field | Value |
|---|---|
| Source ID | `ext_simplex_architecture_1998` |
| Source title | The Simplex Architecture for Safe On-Line Control System Upgrades |
| Ingestion date | 2026-07-24 |
| Source version / URL | American Control Conference 1998, https://doi.org/10.1109/ACC.1998.703255 |
| Citation label | Seto et al. (1998), The Simplex Architecture |
| Published / updated | 1998-06-24 / 1998-06-24 |
| DOI | 10.1109/ACC.1998.703255 |
| Ingestion basis | Primary institutional publication record and abstract inspected; no controller, switch, monitor, or process case reproduced. |

## Thesis

An unverified advanced controller can be placed behind an independently trusted
safety controller and decision module. Safe fallback must be an operational
path with adequate switching time, not a promise attached to the advanced
controller.

## Mechanisms

- Separate advanced and baseline safety controllers.
- Monitor the plant and switch control authority before leaving the safe
  operating region.
- Permit online upgrade under a fault-tolerant architecture.

## Evidence

The source describes and demonstrates Simplex in a bounded process-control
setting. It does not validate arbitrary learned controllers or the ASI Stack.

## Failure Modes

- Shared defects between monitor and advanced controller.
- Late or oscillatory switching.
- A fallback controller that is unavailable, unsafe, or too weak for the
  current state.
- An operating-region proof that does not match the plant.

## Book Chapters Supported

- `embodied-agency-real-time-control-and-physical-safety`
- `capability-replacement-and-rollback`

## Claims To Add Or Update

- The physical layer needs independent stop and fallback authority.
- Replacement and rollback must preserve real-time plant safety, not only
  software state.

## Open Questions

- Which controller and state-estimator components require separate trust roots?
- What receipt proves the fallback was reachable before the safety margin
  expired?
