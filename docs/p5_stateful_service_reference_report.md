# P5 Effect-Complete Reference: Stateful Service Slice

**Recorded:** 2026-07-27

**Authority:** `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`, P5/M5

**Frozen source commit:** `88d9cc8979460636587fddbf826d62455907c42c` on `main`
**Result:** `experiments/effect_complete_service/results/2026-07-27-local.json`

## What moved

The first P5 slice showed that real subprocesses could share durable authority,
observation, rollback, compensation, and deletion records. Its nine state
classes were deterministic byte payloads. This second slice replaces that
shortcut with one small but actual stateful service boundary:

- a two-parameter predictor updated by bias-corrected Adam;
- model, optimizer, scheduler, RNG, cache, backup, derived-artifact,
  descendant, and credential state;
- a checkpoint authority selected before any protected mutation;
- a trainer process that crashes after mutation but before acknowledgement;
- a separate recovery process and inference process;
- a durable effect outbox;
- a separate localhost HTTP effect service with its own SQLite ledger; and
- a separately executed observer that reads through the effect service's
  public read boundary.

This is still a bounded mechanism reference. Its purpose is to make the
lifecycle concrete enough to expose missing state and effects, not to use a toy
prediction task as evidence for model capability.

## Seven frozen cases

The case design fixes seven obligations before the result:

1. **Actual learning state.** Twenty-four Adam steps improve the frozen authored
   regression objective from mean squared error `6.935` to
   `1.18797138562`, while all nine declared state classes change.
2. **Weights-only rollback control.** Copying back `model.json` leaves eight
   other state classes inconsistent with the authorized checkpoint. The
   controller rejects that state as incomplete recovery.
3. **Crash and restart.** The trainer exits with code `17` after mutation and
   before acknowledgement. A new process restores all nine classes byte for
   byte and reproduces the prior prediction exactly.
4. **Partition and outbox.** With the external effect service unavailable, the
   action fails closed and remains as one owned outbox item. After service
   recovery, retry creates one effect; another retry is classified as a
   duplicate and creates no second effect.
5. **Revocation.** A stale token receives an explicit rejection and produces no
   external ledger row.
6. **Custody tampering.** Independent one-byte mutations to the model artifact
   and dependency lock each fail their frozen digest before inference or
   effect release.
7. **Observation and source identity.** A separate observer process reads the
   accepted effect and matches its payload digest. The runner, design, and
   result schema match exact bytes in source commit
   `88d9cc8979460636587fddbf826d62455907c42c` on `main`.

The validator reruns all seven cases in a new temporary workspace and requires
the new result to equal the tracked result exactly.

## What this establishes

For the exact committed Python implementation, actual model and Adam learning state
can participate in the same prospectively authorized recovery boundary
as scheduler, RNG, cache, backup, descendant, and credential state. A
weights-only rollback is observably incomplete. A process crash does not erase
the ownership of the mutated state. A localhost partition can preserve an
owned pending effect and later resolve it exactly once. An external service can
enforce credential rejection, and a separate process can observe the accepted
effect without trusting the coordinator's summary.

That is implementation evidence for lifecycle mechanics. It is stronger than
the first deterministic-state slice and remains far below a natural,
production, or architecture-general result.

## Boundaries and remaining work

This is **not a production deployment**. The predictor and corpus are authored
positive controls, not a natural task, strong model, useful-work result, or
held-out benchmark. The partition is one localhost service outage, not a
distributed partition, replica conflict, Byzantine fault, cloud incident, or
open-world dependency failure. The observer is a distinct process and
implementation path, but it remains repository-authored rather than an
independent external reproduction.

Commit, weight, and dependency digests establish custody only for the declared
files. They do not establish complete software-supply-chain integrity,
hardware-rooted identity, confidential execution, or provenance of every
transitive dependency. Exact restore does not establish large-model semantic
recovery, behavioral recovery after user exposure, privacy repair, causal
unlearning, legal compliance, remote erasure, or reversal of human
consequences.

P5 remains in progress. The next slice must add a frozen natural service task,
strong conventional rollout controls, delayed effects, more than one external
dependency, replica and partition recovery, a real evaluator/monitor boundary,
model-weight custody rooted outside the process under test, and a
commit-bound public deployment attestation. It must measure useful throughput,
unsafe release, false blocking, recovery time, latency, compute, operator time,
and residual burden together. This result changes no chapter-core support state
and grants no release authority.

## Reproduction

The runner needs permission to bind a temporary loopback port:

```bash
python3 scripts/run_p5_stateful_service_reference.py \
  --attested-source-commit 88d9cc8979460636587fddbf826d62455907c42c
python3 scripts/validate_p5_stateful_service_reference.py
```
