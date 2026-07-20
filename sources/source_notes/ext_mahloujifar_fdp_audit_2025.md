# Source Note: Auditing f-Differential Privacy in One Run

| Field | Value |
|---|---|
| Source ID | `ext_mahloujifar_fdp_audit_2025` |
| Source title | Auditing f-Differential Privacy in One Run |
| Ingestion date | 2026-07-19 |
| Source version / URL | ICML 2025, https://proceedings.mlr.press/v267/mahloujifar25a.html |
| Citation label | Mahloujifar, Melis, and Chaudhuri (2025), Auditing f-Differential Privacy in One Run |
| Published / updated | 2025-07 / 2025-07 |
| DOI | none |
| Review state | Paper-body and official proceedings page reviewed. |
| Ingestion basis | One-run construction, f-DP hypothesis/estimates, experiments, assumptions, and limitations. Code was not run. |

## Thesis

One-run empirical auditing can use randomized example inclusion and an assumed
f-DP curve to detect some implementation flaws and obtain bounded empirical estimates.

## Mechanisms

- Randomize target inclusion, derive membership observations, and compare them
  with a hypothesized f-DP tradeoff curve.

## Evidence

The paper reports tighter estimates in studied settings. An empirical audit is a
lower-bound/flaw detector under its assumptions, not proof that privacy holds.

## Failure Modes

- Treating failure to violate as certification, weak membership signals,
  broken inclusion randomization, outcome-aware tuning, or lost denominators.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Pair formal accounting with independent empirical auditing and preserve every
  randomized inclusion in the denominator.

## Open Questions

- Which f-DP hypothesis and attack fit the selected workload?
- How should audit cost and audit-created privacy loss be accounted?
