# Independent verifier reproduction report

Choose one check and identify the exact run. The standalone ZIP replays
`verifier-paired` at evidence commit
`21a8b4eab72edd9593f5de9c982fecaf51f639d8`. Record the result digest and,
when used, the standalone ZIP digest displayed on the study page.
Use the `verifier-floor-cache` run for the absolute floor, provenance
controls and equal-memoization comparison.

| Check | What to send |
|---|---|
| Exact rerun | Give the command, environment, expected and observed digests, and earliest differing case if any. |
| Independent reanalysis | Give your scoring definition, the paired rows it uses, your calculation or executable script, and the resulting decision. |
| Changed assumption | Give the changed input or policy rule, the reason, the new protocol, and the exact comparable and incomparable outcomes. |

## Report

- Report ID and revision. Use a new revision for a correction and identify which report it supersedes.
- Study, run, commit, artifact digest, and the relevant case link.
- Check type, date, environment, and command or method.
- Observed result with counts, exclusions, and the first discrepancy.
- What inference you think should change and why.
- Independence, relevant conflicts, and optional attribution. Say explicitly which text and artifacts may be made public. Keep private material out of public evidence.

The author can add a cleared report to the study history with the reported
result and a separate disposition. Record whether the result was confirmed,
narrowed, disputed, or left unresolved, and cite the exact artifact and
decision. A changed-assumption check belongs beside the original run with
its scope visible. Record an external check only after it happens.

For a cleared public report, the author adds an entry to
`independent_reports` in [the research history manifest](../../products/research_studies.json).
Use a stable `id`, integer `revision`, `run`, and kind of `rerun`,
`reanalysis` or `changed-assumption`. Pin the public `artifact` path to
its `source_commit` and record `artifact_sha256`. Add `reported_result`, author `decision`, and
`disposition`. Set `permission` to `public` only with explicit clearance.
