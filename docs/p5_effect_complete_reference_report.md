# P5 Effect-Complete Reference: Local Multi-Process Slice

**Recorded:** 2026-07-27  
**Authority:** `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`, P5/M5  
**Result:** `experiments/effect_complete_reference/results/2026-07-27-local.json`

## What moved

The older integrated-reference artifacts checked finite routes, schema
refinement, and logical concurrency. This slice crosses the next implementation
boundary: it runs real subprocesses against one durable SQLite/WAL ledger and a
contained filesystem effect boundary. The frozen eight-case design exercises:

1. an authorized effect, independent observation, and exact restoration;
2. concurrent idempotent writers;
3. revocation against a stale cached epoch;
4. worker crash after effect but before acknowledgement;
5. compensation for an append-only effect that cannot be erased;
6. a prospectively selected checkpoint over model, optimizer, scheduler, RNG,
   cache, backup, derived-artifact, descendant, and credential state;
7. descendant-aware local deletion with separate behavioral, influence,
   privacy, and storage-erasure axes; and
8. exact-scope rejection without an effect.

All eight cases terminate with owned receipts. The fresh validator reruns the
system in a new temporary directory and requires a byte-for-byte equal result.
It therefore checks deterministic orchestration rather than trusting the
tracked summary.

## What the slice establishes

For this exact Python/SQLite/local-filesystem implementation, five named roles
coordinate through a durable ledger; two executor processes race on one
idempotency key without duplicating the effect; revoked and out-of-scope
credentials create no effect; an orphan created before worker crash is
discovered and removed; an append-only action receives compensation without
pretending its history disappeared; nine declared state classes restore
byte-exactly from authority selected before mutation; and five declared local
storage surfaces are deleted.

This is implementation evidence for the local vertical slice. It is stronger
than a record-shape fixture and weaker than deployment evidence.

## Boundaries and remaining work

This is **not a deployed AI service**. The state payloads are deterministic
bytes, not live trained-model or optimizer state. Filesystem observation is not
complete open-world effect discovery. Local deletion establishes neither
causal influence reduction nor privacy leakage reduction, and it says nothing about
copies outside the sandbox. SQLite on one host does not test network
partitions, Byzantine services, cloud credentials, real model-weight custody,
or third-party compensation.

P5 remains in progress until the same lifecycle is bound to a frozen service
with actual model and learning state, process restart and partition faults,
independently observed external effects, supply-chain and weight custody, and a
commit-bound deployment attestation. This slice changes no chapter-core support
state and grants no release authority.

## Reproduction

```bash
python3 scripts/run_p5_effect_complete_reference.py
python3 scripts/validate_p5_effect_complete_reference.py
```
