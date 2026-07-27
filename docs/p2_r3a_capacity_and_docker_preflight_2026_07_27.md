# P2-R3a Capacity and Docker Entry Preflight

Date: 2026-07-27 America/Chicago

Attempt: `2026-07-27-r3a-002`

Source commit: `2aae71bf83909298f4c5ebd5c6a819f687ba772e`

State: **blocked before materialization; N0 infrastructure disposition**

## Outcome

The frozen P2 materialization protocol was not allowed to start. The host had
`25,627,230,208` available bytes (23.87 GiB) against the exact
`53,687,091,200`-byte (50 GiB) floor, a shortfall of `28,059,860,992` bytes
(26.13 GiB). This is an improvement over the 2026-07-26 receipt, but it does
not satisfy the frozen gate.

The Docker client was installed, but direct daemon diagnostics did not
establish a reachable daemon. `docker version` returned `EOF`, `docker info`
reached its 30-second diagnostic timeout, and `docker system df` returned
`retrieving disk usage: EOF`. The result therefore confirms an actual daemon
failure rather than inheriting the earlier sandbox-local socket observation.

No protected task content was opened. No image pull, dependency
materialization, task-specific command, test identity, patch, label, evaluator
judgment, model output, or outcome was exposed. This does not count as a
candidate attempt, does not burn a rank, and does not authorize rank
progression.

## Exact custody

The immutable machine receipt is
`experiments/p2_governed_repository_admission/infrastructure_materialization/attempts/2026-07-27-r3a-002/result.json`.
It binds the frozen resource ceiling and 30-candidate queue by SHA-256, records
the exact command argument vectors, timestamps, exit codes, timeouts, complete
standard output and error, and output digests, and preserves the measured disk
arithmetic.

The preflight executed only:

1. `df -k /Users/corbensorenson/Documents/AI_book`
2. `docker version --format '{{json .}}'`
3. `docker info --format '{{json .}}'`
4. `docker system df --format '{{json .}}'`

Docker reclamation was not attempted because reclaimable bytes could not be
measured and the daemon was not reachable. The authorization boundary remains
Docker objects only. Deleting non-Docker user data is neither authorized nor
an implied remedy.

## Interpretation

This is an N0 infrastructure disposition. It says only that this host state
could not enter the frozen experiment. It says nothing about governed
repository admission, model competence, usefulness, safety, transfer, SOTA,
AGI, or ASI. The support and release effects are both `none`.

The next legal empirical action is to restore at least the frozen 50 GiB free
floor and a live Docker daemon, then create a new immutable preflight receipt.
Only a passing entry receipt may launch the content-sealed sequential
materializer. The materialization and replacement-qualification result remains
open; this receipt closes only the exact 2026-07-27 entry attempt.
