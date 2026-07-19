# P2 Frozen Resource Ceiling

Date: 2026-07-17  
State: **v2 measurement semantics repaired and frozen before candidate outcomes; measurement gate pending**

The P2 task runner now measures actual wall time, sampled container memory, CPU
utilization, estimated CPU-seconds, process count, timeout state, image pull and
size, dependency setup, cleanup, and host free-space residuals. A passing
Apiflask task exercised the monitor without changing task selection or reopening
a failed task. Both arms retained their exact oracle pass; observed peak memory
was 75.2 MB, maximum sampled CPU was 100.51%, peak PIDs were two, and the longest
arm was 4.43 seconds.

The ceiling is grounded in that pilot plus the complete fixed-denominator run.
The original record incorrectly called Docker Engine's exact `.Size` field an
expanded image size. A pre-outcome four-image calibration proved that it tracks
registry content bytes: 1.06–1.42 GB, while Docker's virtual-size surface reports
3.89–4.87 GB. The old expanded-size pass is invalidated. The v2 contract retains
the 1.5 GB Engine-content ceiling and adds a 7 GB conservative virtual-size
upper-bound ceiling, produced by the formula frozen before the remaining three
rank-one images were measured.

Per task, acceptance now requires pull at or below 300 seconds, Engine content
at or below 1.5 GB, conservatively bounded virtual size at or below 7 GB,
dependency setup at or below 300 seconds, each arm at or below 600
seconds, peak memory at or below 6 GiB, sampled CPU at or below the six-CPU
allocation, estimated CPU use at or below 3,000 CPU-seconds, and peak PIDs at or
below 1,024. No timeout, OOM/signal kill, cleanup failure, or retained task
container/image is allowed. At least 50 GiB must be free before a task. Cleanup
must report zero images, containers, and build cache and then stabilize for up
to 60 seconds, with three five-second samples differing by at most 64 MiB,
before the residual is measured. No task may then leave more than 5 GiB of host
free-space loss, and the campaign may not leave more than 30 GiB.

The hard runtime remains six CPUs, 8 GB memory, 2,048 PIDs, a 2 GB temporary
filesystem, no network, all capabilities dropped, no-new-privileges, and a
1,200-second kill boundary. The acceptance wall ceiling is intentionally lower
than the kill boundary so a near-timeout run cannot count as healthy.

The sampled CPU-seconds value is explicitly an estimate, not exact billing or
energy measurement. Arms lasting at least three seconds require a monitor
sample; shorter arms remain bounded by hard limits and wall time but are marked
measurement-limited. Any monitor failure, environment-specific amd64 emulation
failure, task ceiling breach, 12-hour replacement-screening breach, six-hour
full requalification breach, or disk breach blocks the corpus gate. It is not a
negative result about governed admission.

The v2 ceiling is frozen, but the resource gate has not passed: the eight
retained qualified tasks and all replacements must be remeasured with this
monitor. Rank-one development task specifications are open; candidate outcomes
remain unopened. The final held-out pool remains unselected and unopened.

Machine record: `evidence_quality/p2_resource_ceiling.json`.
