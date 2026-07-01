# Resource CI Cost Profile

Date: 2026-07-01

This record captures GitHub Actions publication-pipeline metadata for the
living book as a Resource Economics accountability trace. It uses actual Pages
workflow run metadata to show pipeline elapsed time, failure cost, and recovery
boundary for recent publication runs.

This is GitHub Actions publication-pipeline metadata only. It is not a
production workload trace, deployed scheduler result, live model-quality result,
economic-optimality result, physical-feasibility review, simulator-adequacy
result, or external review.

## Command

```bash
python3 scripts/build_resource_ci_cost_profile.py --write-result
python3 scripts/validate_resource_ci_cost_profile.py
```

The builder uses `gh run list` for recent `Publish Quarto site` runs on
`main` and `gh run view <failed-run-id> --log-failed` for failed-run excerpts.
The validator checks the recorded timestamps, durations, metrics, failure
classification, repair boundary, source commands, and non-claims offline.

## Result Record

Result record:
`experiments/resource_ci_cost_profile/results/2026-07-01-main.json`

| Field | Value |
|---|---:|
| Runs recorded | 8 |
| Completed runs | 7 |
| Successful completed runs | 6 |
| Failed completed runs | 1 |
| In-progress at capture | 1 |
| Completed duration total | 1,533 seconds |
| Completed duration median | 213 seconds |
| Completed duration mean | 219.0 seconds |
| Successful-run duration mean | 251.833 seconds |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |

## Failure And Repair Boundary

The recorded failed run is `28521511292`, titled `Add Resource Economics
workflow trace`. The failure stage was `Check generated scaffold`, and the
failure type is recorded as generated scaffold drift: the workflow ran
`python3 scripts/sync_scaffold.py` followed by `git diff --exit-code`, then
detected generated Appendix E drift around the Resource workflow trace harness
row.

The next completed successful run in the profile is `28522244545`, titled
`Bridge resource workflow trace to Lean`, with a 356-second publication run.
That repair event demonstrates publication-gate recovery for the repository
state. It does not prove the Resource Economics chapter claim, scheduler
quality, model quality, or economic adequacy.

## Resource Reading

For the book project itself, the cost profile makes several pipeline resources
visible:

- Generated surfaces have to be updated through their source of truth; direct
  edits create fast CI failures.
- The failure was cheap in wall-clock time, but it displaced reviewer and
  maintainer attention until the manifest source was corrected.
- The next successful publication run carried the real recovery cost, including
  full validation and render time.

## Non-Claims

- This CI cost profile does not promote any chapter core claim above
  `argument`.
- This CI cost profile does not create a support-state transition.
- This CI cost profile does not prove deployed scheduler behavior, runtime
  budget enforcement, model quality, economic outcomes, physical feasibility,
  simulator adequacy, or workload-quality improvement.
- This CI cost profile records GitHub Actions publication-pipeline metadata
  only; it is not a production workload trace or external review.
