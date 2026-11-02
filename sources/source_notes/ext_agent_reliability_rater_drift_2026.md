# Source Note: Reliability of AI Agents: Rater Effects, Drift, and the Return to an Evaluation Program

| Field | Value |
|---|---|
| Source ID | `ext_agent_reliability_rater_drift_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.07003v1](https://arxiv.org/html/2610.07003v1) |
| Citation | Zhang and Esposito (2026), Reliability of AI Agents |
| Published / updated | 2026-10-04 / 2026-10-04 |
| Review scope | Sections 3.1–3.4, 4 measurement interpretation and Section 6.5/7 limitations. Selected deployment/estimand passages, not independent access to recordings. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Longitudinal agent evaluation has to separate agent changes from changes in the measurement process.

## Mechanisms

Uses overlapping reviewers, reviewer-adjusted batch estimates, change logs and a separate support-ticket series. Interview date and reviewer sign-off date have different evidentiary meanings.

## Evidence

An observational study of 2,611 production interviews reports substantial rater effects and a different adjusted trend. The authors explicitly do not identify the causal effect of the evaluation program.

## Failure Modes

No randomized evaluation-intensity intervention; sampling mix and unlogged/vendor changes remain concerns. The estimated roughly five-week uncertainty horizon is model- and deployment-specific, not a universal review deadline. Candidate fairness and hiring validity are not established by the reliability rubric.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

Can evaluation retain comparable task/rater anchors while model, user population and operational reporting all change?

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
