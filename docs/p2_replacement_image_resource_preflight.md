# P2 Replacement Image Resource Preflight

Date: 2026-07-17  
State: **rank-one images feasible; task qualification not started**

The first attempt completed all four pull/cleanup cycles but failed while
writing the aggregate because the runner referenced a nonexistent campaign-
ceiling field. Its eight logs are retained, its measurements are not recovered,
and it is N0 with no candidate or claim effect.

A clean R2 run began with no Docker images or build cache and repeated all four
cycles. Images were pulled by immutable registry digest, inspected locally,
removed before the next candidate, and checked against the ceilings frozen
before the queue draw.

| Slot | Candidate | Pull seconds | Local image bytes | Post-cleanup host loss | Result |
|---:|---|---:|---:|---:|---|
| 1 | `mitsuhiko__minijinja-794` | 115.801 | 1,123,009,785 | 3,722,633,216 | pass |
| 2 | `google__go-github-3619` | 111.252 | 1,148,377,404 | 59,998,208 | pass |
| 3 | `go-git__go-git-1556` | 127.839 | 1,417,428,320 | 1,669,070,848 | pass |
| 4 | `jhipster__jhipster-lite-12851` | 210.994 | 1,056,326,910 | 2,126,180,352 | pass |

All pulls stayed below 300 seconds, all images stayed below 1.5 GB, every
digest/platform inspection and cleanup returned zero, and each task stayed
below the 5 GiB residual ceiling. The campaign host-space loss was 7,577,923,584
bytes, below the frozen 30 GiB campaign ceiling. The residual is material and
is retained rather than described as full disk recovery.

This passes only image-resource feasibility. Dependency materialization, paired
baseline/gold execution, exact dual-evaluator agreement, two repetitions,
runtime-network isolation, and task-level resource monitoring remain pending.
No dataset task content or candidate outcome was opened, and the final held-out
pool remains unselected and unopened.

Machine attempts:

- `experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r1/result.json`
- `experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts/2026-07-17-rank-one-r2/result.json`
