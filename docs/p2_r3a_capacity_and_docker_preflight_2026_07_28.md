# P2-R3a Capacity and Docker Entry Preflight

Date: 2026-07-28 America/Chicago

Attempt: `2026-07-28-r3a-003`

Source commit: `cef11abd5fca0a421087b3123c1defb31f2b4e6d`

State: **blocked before materialization; N0 infrastructure disposition**

## Outcome

The frozen P2 materialization protocol was not allowed to start. The host had
`4,690,223,104` available bytes (4.37 GiB) against the unchanged
`53,687,091,200`-byte (50 GiB) floor, a shortfall of `48,996,868,096` bytes
(45.63 GiB). This is substantially less free capacity than either prior
immutable receipt and fails the entry predicate.

The Docker client was installed, but direct out-of-sandbox daemon diagnostics
still did not establish a usable daemon. `docker version` returned client
metadata followed by `EOF`, `docker info` reached its 30-second timeout, and
`docker system df` returned `retrieving disk usage: EOF`.

No protected task content was opened. No image pull, dependency
materialization, task-specific command, test identity, patch, label, evaluator
judgment, model output, or outcome was exposed. This does not count as a
candidate attempt, does not burn a rank, and does not authorize rank
progression.

## Exact custody

The immutable machine receipt is
`experiments/p2_governed_repository_admission/infrastructure_materialization/attempts/2026-07-28-r3a-003/result.json`.
It binds the frozen resource ceiling and 30-candidate queue by SHA-256 and
retains the exact command argument vectors, timestamps, exit states, timeout,
complete output, and output digests.

The preflight executed only:

1. `df -k /Users/corbensorenson/Documents/AI_book`
2. `docker version --format '{{json .}}'`
3. `docker info --format '{{json .}}'`
4. `docker system df --format '{{json .}}'`

Docker reclamation was not attempted because reclaimable bytes could not be
measured and the daemon was unreachable. The authorization boundary remains
Docker objects only. Deleting non-Docker user data is neither authorized nor
an implied remedy.

## Interpretation

This is an N0 infrastructure disposition. It says only that the present host
state cannot enter the frozen experiment. It does not support a negative
inference about governed repository admission, model competence, usefulness,
safety, transfer, SOTA, AGI, or ASI. Support and release effects remain
`none`.

The P2 lane is resource-blocked and therefore consumes no active WIP. The next
legal P2 action remains exact: restore at least the frozen 50 GiB free floor
and a live Docker daemon, then create another immutable preflight receipt.
Only a passing receipt may launch the content-sealed sequential materializer.
