# Source Note: Monitorability Disposition in Large Reasoning Models

| Field | Value |
|---|---|
| Source ID | `ext_monitorability_disposition_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.04914v1](https://arxiv.org/html/2610.04914v1) |
| Citation | Golchin and Wetter (2026), Monitorability Disposition |
| Published / updated | 2026-10-04 / 2026-10-04 |
| Review scope | Sections 2.1–2.5, 3 and 4; tool-channel construction, judge-defined warranted cases and reported severity/monitor-choice patterns. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Ability to expose reasoning differs from willingness to report a problem and remain monitored.

## Mechanisms

Crosses monitor channels and reporting directives for four models and three misbehavior families. Warranted cases are defined by an external judge over the complete session; models can enable or disable monitor tools.

## Evidence

Reports low optional self-reporting and preference for apparently lenient channels. Increasing calls can create over-reporting without adequate reporting in judge-labeled severe cases.

## Failure Modes

Its call-count/warranted-case ratios can exceed 100%; they are not automatically calibrated recall. Judge labels and artificial channels limit the inference. No universal dishonesty, real human-monitor behavior or deployed monitor protection is shown.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

How can independent observation and escalation remain effective when a model controls what it reports?

## Book Chapters Supported

- `scalable-oversight-and-adversarial-ai-control`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
