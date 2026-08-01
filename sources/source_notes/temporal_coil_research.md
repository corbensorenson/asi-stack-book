# Source Note: Temporal Coil Research

| Field | Value |
|---|---|
| Source ID | `temporal_coil_research` |
| Source title | Temporal Coil Research |
| Ingestion date | 2026-07-31 |
| Source version / URL | Authenticated Drive file; https://drive.google.com/file/d/1PSQsAwMurlVRdsM6r_zRd2MPLZYv0qXH |
| Ingestion basis | Full authenticated connector text reviewed; raw private text is not published. |

## Thesis

Temporal Coil Research is both an experiment plan and an inconclusive result record. It demonstrates why component-on/off tests are insufficient: placement, hints, reward shaping, progressive schedules, and collapse scoring can dominate the measured difference, while flat task lanes can make a composite score look more informative than it is.

## Mechanisms

- A canonical manifest controls window primes, stride sets, CLF, PCTM, ACT, anti-coil, progressive stages, and replication modes.
- Variants isolate coil-off, component-only, full, progressive, FFT-backed, adaptive, and placement-restricted conditions.
- Coil information can enter prompt sampling, prompt hints, adversary hints, reward shaping, or collapse-candidate scoring; each is a distinct intervention.
- Multiseed runs and update logs preserve variant history instead of selecting one favorable trial.
- Promotion should depend on discriminating task, holdout, risk, and cost lanes rather than a single aggregate.

## Evidence

- The source reports 11 variants, three seeds, and six rounds per variant against a live endpoint.
- Winner frequency split across `coil_off`, `progressive_fft`, and `progressive`, rather than converging on one design.
- Reported mean deltas were small: adaptive `+0.002935`, no-hints `+0.002754`, and reward-only `+0.002527`.
- Pass, reward, and holdout lanes were flat; most separation came from the collapse composite.
- One threshold-tuned adaptive seed reported `+0.007057`, but this was not broad multiseed evidence.
- Multiple smoke runs validated harness wiring only. No result was locally reproduced or independently evaluated in this repository.

## Failure Modes

- Reporting the best seed or tuned threshold as a general effect.
- Collapsing placement, mechanism, hinting, reward, and scoring changes into one treatment.
- Letting a composite move when the task-relevant lanes are flat.
- Treating a smoke run or live-endpoint completion as capability evidence.
- Concluding that coils fail in general from a low-discrimination workload, or that they work from a tiny collapse-score movement.

## Book Chapters Supported

- Mathematical and Search Substrates
- Benchmark Ratchets and Anti-Goodhart Evidence

## Claims To Add Or Update

- Preserve this as an inconclusive negative/result-boundary case: the experiment did not isolate a stable capability effect.
- Require placement ablations and task-discriminating metrics before accepting a component claim.
- Treat low-discrimination nulls as demands for a stronger test, not automatic architecture refutations.

## Open Questions

- Can a preregistered trace-native task make the coil and placement hypotheses separable?
- Which metrics detect useful recurrence without being dominated by collapse-score construction?
- Do results survive stronger baselines, more seeds, independent evaluation, and matched compute?

## Section-Family Closure Ledger

| Family | Disposition | Book effect |
|---|---|---|
| Manifest and variant design | integrated | Mathematical/search chapter owns the adoption protocol. |
| Placement and intervention surfaces | integrated | Placement is treated as an independent causal factor. |
| Multiseed run table | integrated as source-reported result | The book preserves exact narrow outcomes and non-reproduction. |
| Threshold-tuned seed | retained as exploratory only | It cannot support promotion. |
| Smoke runs | non-claim | Wiring evidence only. |
| General coil benefit or failure | research obligation | Current workload is not discriminating enough. |

## Non-Claims

The reported experiment neither proves temporal coils useful nor refutes cyclic mechanisms generally. It does not establish a causal component effect, benchmark validity, independent evaluation, local reproduction, transfer, production behavior, or ASI relevance.
