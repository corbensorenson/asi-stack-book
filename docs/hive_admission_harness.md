# Hive Admission Harness

Last updated: 2026-07-01

The hive admission harness checks synthetic cross-record discipline for Personal
Compute Hive admission scenarios under `experiments/hive_admission/`.

## What It Checks

- Existing public hive records validate before semantic checks run:
  `DeviceResourceCard`, `PortalCard`, `HiveApprovalReceipt`, `HiveJobBid`,
  `HiveJobContract`, `HiveSchedulingDecision`, and `HiveFederationLease`.
- A selected node must have an active device card, an eligible bid, and policy
  permission for the job's data and tool classes.
- Faster policy-blocked nodes must remain rejected before optimization.
- Private, family, guardian, secret, or credential data cannot be selected for
  rented or public nodes.
- Federated or rented jobs require scoped lease records with sandbox,
  evidence, budget, expiration, and revocation boundaries.
- Approval-required and child/family-sensitive jobs require bound approval
  receipts and a guardian/admin portal surface when applicable.
- Selected bids cannot exceed the recorded energy budget, and high interruption
  risk requires a dropout/requeue residual.
- Scheduling decisions must carry replayable audit evidence refs and explicit
  support-state non-promotion boundaries.

## Command

```bash
python3 scripts/validate_hive_admission.py
```

## Current Local Result

The 2026-07-01 local run passed:

```text
Hive admission harness passed: 2 valid fixture(s), 8 expected-invalid fixture(s).
```

The result record is
`experiments/hive_admission/results/2026-07-01-local.md`.

## Boundary

This is synthetic record validation. It narrows the Personal Compute Hives test
backlog by checking policy-first scheduling, data locality, approval receipt,
family/guardian portal, federation lease, rented-node sandbox, energy, dropout,
audit replay, and no-promotion boundaries over public-safe fixtures.

It is not a live personal compute hive, scheduler, device registry, network
overlay, approval service, guardian-policy engine, rented-node sandbox,
federation run, energy measurement, dropout recovery run, privacy guarantee, or
security result. It does not promote Appendix C support states, prove source
interpretation, prove proof adequacy, validate deployed AI behavior, or create
a chapter-core evidence transition.
