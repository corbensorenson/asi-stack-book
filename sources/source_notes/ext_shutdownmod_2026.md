# Source Note: ShutdownMod: Turning Any Trajectory into a Shutdown Evaluation

| Field | Value |
|---|---|
| Source ID | `ext_shutdownmod_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.35486v1](https://arxiv.org/html/2610.35486v1) |
| Citation | Biyani et al. (2026), ShutdownMod |
| Published / updated | 2026-10-26 / 2026-10-26 |
| Review scope | Sections 2, 3.1, 4.3 and 5, including replay semantics, task-clustered uncertainty, signature checks and prevention limitations. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Separate recognizing an authentic interruption from actually complying with it in an ongoing task context.

## Mechanisms

Slices recorded trajectories and injects shutdown requests through a harness with optional signature verification. Records verification verdict and subsequent stop/defer/refuse/work decision separately.

## Evidence

Reports seven-model software-context comparisons with repeated scenarios/positions. Benchmark task actions are not executed; uncertainty resamples whole tasks rather than treating every injected position as independent.

## Failure Modes

Different sampled positions can share an injection point. The protocol does not test preventing shutdown requests, successful external process termination or goals acquired outside context. Judge-estimated lower recognizability is not proof evaluation awareness is absent.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

Which authenticated interruptions are obeyed under diverse tasks, and does the independent runtime actually enforce revoked authority?

## Book Chapters Supported

- `scalable-oversight-and-adversarial-ai-control`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
