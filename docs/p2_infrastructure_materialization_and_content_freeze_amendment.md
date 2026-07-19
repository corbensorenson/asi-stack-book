# P2 Infrastructure Materialization and Content-Freeze Amendment

Date: 2026-07-18  
State: **prospectively frozen; pool-wide infrastructure gate blocked; protected task content remains the no-rerun boundary**

## Decision

The original replacement policy applied irreversibility too early. A failed
image pull, dependency fetch, emulation startup, resource sampler, or cleanup
probe that occurs before protected task content opens cannot create
outcome-awareness about the task. Treating that event as a burned rank buys no
experimental integrity and can select the surviving corpus for local
infrastructure weather.

This amendment therefore separates two clocks:

1. **Infrastructure materialization clock.** Exact image digests, dependency
   snapshots, architecture/emulation state, resource instrumentation, cleanup,
   and disk recovery are prepared without reading protected task content.
   Failures may receive at most three attempts per exact artifact and failure
   class. Every attempt, timeout, byte count, cleanup result, and digest is
   retained. Retry ceilings and success predicates are frozen before the first
   attempt and cannot change in response to task or candidate outcomes.
2. **Protected-content clock.** The irreversible boundary begins with the first
   read, decode, application, or evaluator exposure of any problem statement,
   solution patch, test patch, test identity, expected status, task-specific
   command, baseline outcome, or gold outcome. From that event onward, the
   candidate is one-shot. No rerun, retry-budget change, candidate skip, or
   favorable replacement is permitted.

The whole 30-candidate frozen metadata queue must have infrastructure receipts
before any still-unopened rank is activated. A setup failure that exhausts its
bounded attempts blocks the pool; it does not advance the rank. Selection may
not condition on pull speed. Infrastructure cost remains part of the resource
bill and may define a separately stated deployment population, but it is not a
negative result about governed repository admission.

## Historical reconciliation

Historical records are not rewritten. Rank 4 opened task-specific material and
therefore remains irrevocable under the stronger boundary. Rank 5 opened no
protected content or outcome. Its 300-second pull timeout remains a valid N0
setup observation, but its instruction to advance to rank 6 is superseded.
Rank 5 returns to `infrastructure_retry_pending`; rank 6 must remain unopened.

The local host currently has about 60 GiB free and zero retained Docker images.
That is not enough evidence to assert that all 30 images and dependency
snapshots can coexist under the frozen resource ceiling. P2 slot 1 is therefore
blocked at the pool-wide infrastructure gate rather than falsely reported as
executed. The unblock trigger is an exact storage/runtime plan that can retain
or reproducibly mount every frozen infrastructure artifact without reading task
content, followed by a passing pool manifest and monitor soak test.

## Campaign custody rule

Every terminal campaign disposition must be committed before it counts. The
release-tier validator `scripts/validate_evidence_git_custody.py` rejects a
modified, staged, or untracked file under `evidence_transitions/`,
`evidence_quality/`, or `release_records/`. A clean commit proves durability,
not scientific validity.

Machine record:
`evidence_quality/p2_infrastructure_content_freeze_amendment.json`.
