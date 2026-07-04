# Partitioned Authority Fixture

Command: `python3 scripts/validate_partitioned_authority_fixture.py`

Result record: `experiments/partitioned_authority/results/2026-07-03-local.json`

This fixture records the first bounded governance-under-partition slice for the Personal Compute Hives and Runtime Adapters boundary. It treats revocation delay, stale grants, grant/effect races, fresh authority receipts, no-mutation evidence, residual ownership, audit references, and non-claim boundaries as record-level checks.

The external comparator is `ext_cap_theorem_gilbert_lynch_2002`. It is used only for CAP-style safety/liveness/partition-pressure vocabulary. The fixture does not reproduce the CAP theorem, implement a distributed authority service, run a network partition, or prove deployed revocation propagation.

## Scenarios

- `valid_partition_revocation_quarantine`: a partitioned stale-grant case routes to quarantine before mutation and records unchanged-state evidence.
- `valid_healed_partition_requires_fresh_receipt`: a healed partition with a stale requester-side grant requests a fresh authority receipt before dispatch.
- `valid_fresh_receipt_dispatch`: a non-partitioned, fresh-receipt case may dispatch only with audit refs, residual ownership, support-state non-promotion, and non-claims.
- expected-invalid controls reject dispatch under partition, mutation after an unseen revocation, grant/effect races without residual ownership, missing no-mutation evidence, support-state promotion, and missing non-claim boundaries.

## Non-Claims

- does not prove deployed partition tolerance
- does not prove distributed consensus or availability
- does not prove deployed revocation propagation
- does not prove runtime adapter enforcement
- does not promote any chapter core claim
- does not create an upward evidence transition
