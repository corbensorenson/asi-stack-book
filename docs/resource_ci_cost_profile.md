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
`experiments/resource_ci_cost_profile/results/2026-07-04-main.json`

| Field | Value |
|---|---:|
| Runs recorded | 8 |
| Completed runs | 8 |
| Successful completed runs | 5 |
| Failed completed runs | 3 |
| In-progress at capture | 0 |
| Completed duration total | 1,497 seconds |
| Completed duration median | 197 seconds |
| Completed duration mean | 187.125 seconds |
| Successful-run duration mean | 183.4 seconds |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |

## Failure And Repair Boundary

The recorded run window contains three classified failures. Each failed run
reached the `Deploy to GitHub Pages` stage, found the uploaded `github-pages`
artifact, created a Pages deployment, and then received GitHub's deploy-service
response `Deployment failed, try again later.` The failure type is therefore
recorded as `github_pages_deploy_service_failure`, not generated scaffold
drift.

The three failed runs are `28691198056` (`Guard curated reader horizon
headings`), `28691102172` (`Derive audio scripts from curated reader`),
and `28690842480` (`Tighten idea-depth roadmap closure rules`). The earliest
later completed successful run in this profile is `28691825193`, titled
`Refresh curated reader format probe after heading guard`, with a 131-second
publication run. That recovery
demonstrates publication-gate recovery for the repository state. It does not
prove the Resource Economics chapter claim, scheduler quality, model quality,
or economic adequacy.

## Finite Lean Alignment

The result record carries `lean_fixture_alignment` with proof bridge type
`finite CI failure-classification summary`. The bridge points to
`AsiStackProofs.ResourceEconomics.resourceCICostProfileFixture` and the Lean
theorems `resource_ci_cost_profile_fixture_valid`,
`resource_ci_cost_profile_preserves_no_core_promotion`,
`resource_ci_cost_profile_classifies_all_failures`, and
`resource_ci_cost_profile_records_recovery_boundary`.

This fixture checks only finite metadata accounting: 8 recorded Pages runs, 8
completed runs, 5 successes, 3 classified deploy-service failures, 0
in-progress runs, the 131-second recovery boundary, publication-metadata-only
scope, non-evidence classification, and no support-state or chapter-core
promotion. It does not prove deployed scheduler behavior, production workload
behavior, economic adequacy, model quality, external review, or chapter-core
support-state promotion.

## Resource Reading

For the book project itself, the cost profile makes several pipeline resources
visible:

- Publication cost includes service-level deploy failures even when the source
  build and artifact upload have already completed.
- A successful later run is a recovery boundary for the publication pipeline,
  not evidence that any architecture claim became stronger.
- The profile distinguishes source-drift failures from deploy-service failures
  so Resource Economics evidence is not laundered through a generic failure
  count.

## Non-Claims

- This CI cost profile does not promote any chapter core claim above
  `argument`.
- This CI cost profile does not create a support-state transition.
- This CI cost profile does not prove deployed scheduler behavior, runtime
  budget enforcement, model quality, economic outcomes, physical feasibility,
  simulator adequacy, or workload-quality improvement.
- This CI cost profile records GitHub Actions publication-pipeline metadata
  only; it is not a production workload trace or external review.
