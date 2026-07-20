# Source Note: MLPerf Training v6.0

| Field | Value |
|---|---|
| Source ID | `ext_mlperf_training_v6_2026` |
| Source title | MLPerf Training v6.0 |
| Ingestion date | 2026-07-19 |
| Source version / URL | v6.0 benchmark page and official rules/results links, https://mlcommons.org/benchmarks/training/ |
| Citation label | MLCommons (2026), MLPerf Training v6.0 |
| Published / updated | 2026-06-16 / 2026-07-19 retrieval date |
| Ingestion basis | Official MLCommons benchmark page reviewed for targets, divisions, repetitions, variance, system metadata, and result governance; no submission or benchmark reproduction performed. |

## Thesis

Training-system performance requires a fixed workload and quality target,
declared system/software metadata, multiple measured runs, and rules about what
may change. Time-to-quality is different from peak throughput, single-step
speed, eventual convergence, or model merit.

## Mechanisms

- Dataset-plus-quality-target benchmark definitions.
- Closed and Open divisions with different change allowances.
- Repeated runs and aggregation rules intended to expose runtime variance.
- System, processor, accelerator, software, code, availability, and optional
  power metadata.
- Public result correction and invalidation through a change log.

## Evidence

MLPerf publishes audited benchmark results and current v6.0 workload records.
This repository has not run or submitted MLPerf Training. The source supplies a
measurement comparator, not evidence for any ASI Stack training claim.

## Failure Modes

- Reporting throughput without reaching a fixed quality target.
- Selecting the best run while hiding repeats, failures, and tuning cost.
- Comparing Open and Closed submissions as if their allowed changes matched.
- Treating one benchmark suite as complete model, safety, or transfer evidence.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- Boundary context: `benchmark-ratchets-and-anti-goodhart-evidence` and
  `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Measure time-to-declared-quality, variance, failures, tuning opportunity,
  system identity, energy where available, and complete run denominators.
- Keep qualification quality, training integrity, and systems efficiency as
  separate claim axes.

## Open Questions

- Which natural training workloads are tractable enough for independent
  replay while still exposing topology and recovery defects?
- How should governance and operator burden join time-to-quality accounting?
