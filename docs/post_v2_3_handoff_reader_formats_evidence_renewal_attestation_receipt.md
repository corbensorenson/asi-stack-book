# Post-v2.3 Handoff, Reader Formats, and Evidence Renewal Attestation Receipt

Recorded: 2026-07-14

Substantive source commit:
`f93a4d8fa51ac7cafa0db180d7360ee1fb2c498c`

Remote branch: `origin/main`

## Tested-artifact chain

- Build workflow run:
  `https://github.com/corbensorenson/asi-stack-book/actions/runs/29321815315`
- Build job: `87048657771`, conclusion `success`.
- Deep registry, Lean, clean Quarto render, canonical status, Human-view checks,
  browser smoke, and commit-bound artifact upload all passed.
- Deploy workflow run:
  `https://github.com/corbensorenson/asi-stack-book/actions/runs/29322094443`
- Deploy job: `87049548872`, conclusion `success`.
- The deploy job downloaded and verified the commit-bound tested artifact and
  uploaded it to Pages without rebuilding.
- Deployed-site attestation job: `87049614796`, conclusion `success`.
- The attestation crawled the deployed public status and 54-chapter graph.

## Boundary

This receipt proves the mutable Pages deployment chain for the named commit.
It does not create a tag, immutable archive, public reader release, rights
grant, support-state transition, external-human review, safety result, AGI
claim, or ASI claim. `v2.3.0` remains the latest immutable public living-book
release.
