# Artifact GitHub Pages CI Attestation

Status: bounded external CI-service attestation for one GitHub Pages workflow
run. It is not independent external human review, not deployed attestation
behavior, not open-world receipt faithfulness, not release approval, and not
support-state promotion.

The tracked result is validated by:

```bash
python3 scripts/validate_artifact_github_pages_ci_attestation.py
```

The local capture command for the current result was:

```bash
python3 scripts/validate_artifact_github_pages_ci_attestation.py --write-result --run-id 28733145259
```

The generated result is:

`experiments/artifact_github_pages_ci_attestation/results/2026-07-05-local.json`

The accepted no-promotion decision is:

`evidence_transitions/v1_x_measured/artifact_github_pages_ci_attestation_no_change.json`

Result id:

`artifact-github-pages-ci-attestation-2026-07-05`

## What Is Checked

The validator checks a tracked GitHub Actions run record captured from
`gh run view`. The captured run is the `Publish Quarto site` workflow for the
`main` branch. It records the run URL, run id, event, head commit, job set, and
required build-step statuses.

The bounded observation routes are:

- GitHub Actions run API reports the workflow as completed successfully.
- GitHub Actions jobs API reports the expected `build` and `deploy` jobs.
- The build job reports successful required steps for scaffold check, book
  validation, Lean build, HTML render, live Human view validation, browser Human
  view smoke test, and Pages artifact upload.

## Boundary

This is useful record-reality evidence because it moves beyond a local replay
or local filesystem digest. An externally hosted CI service reports that the
repository's public publication workflow passed for a specific commit.

It remains bounded. GitHub Actions success is not independent external human
review. It does not prove source interpretation, verifier correctness, deployed
attestation behavior, open-world receipt faithfulness, model quality,
benchmark quality, safety, ASI capability, or reader release approval. It also
attests only the recorded commit, not future commits.

The no-promotion record keeps this lane at `argument` and records
`blocks_promotion` until externally reviewable attestation/audit traces,
independent verifier-quality review, broader trap/challenge execution outside
the producing component, provenance-completeness review, and independent review
exist.
