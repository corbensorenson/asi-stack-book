# AISI Frontier AI Trends Report 2025

| Field | Value |
|---|---|
| Source ID | `ext_aisi_frontier_ai_trends_2025` |

## Source identity

- Source ID: `ext_aisi_frontier_ai_trends_2025`
- Publisher: UK AI Security Institute
- Public source: <https://www.aisi.gov.uk/research/aisi-frontier-ai-trends-report-2025>
- Reviewed: 2026-07-24

## Thesis

The report synthesizes the institute's frontier-model evaluations across
offensive cyber, dual-use chemistry and biology, autonomous systems, and
societal impacts. It demonstrates the value of repeated cross-model measurement
with explicit domain methods rather than one generic safety score.

## Mechanisms

- trend measurement over model generations;
- domain-specific tasks and scaffolds;
- separation of narrow tasks from longer-horizon environments;
- explicit limits on what an evaluation suite observes;
- public reporting of capability changes relevant to national security and
  public safety.

## Evidence

The results are institute-reported and bounded to the evaluated models,
versions, scaffolds, tasks, and dates. Public summaries cannot expose every
sensitive item. The report is not a complete threat census, proof of realized
harm, or local reproduction.

## Failure Modes

- static tasks becoming stale;
- scoring changes mistaken for capability changes;
- short tasks extrapolated to long-horizon operations;
- sensitive details omitted without a usable uncertainty statement;
- broad claims made from one domain or model family.

## Book Chapters Supported

- Primary: `dangerous-capability-domains-and-misuse-uplift`
- Supporting: `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Dangerous-capability trend claims must remain domain-, model-, scaffold-,
  horizon-, evaluator-, and date-specific.
- A repeated evaluation series can expose movement while still leaving
  real-world uplift and harm unproved.

## Open Questions

- How should trend breaks be distinguished from scaffold improvements?
- What public evidence can support scrutiny without releasing harmful detail?
- How can evaluation coverage keep pace with agentic and distributed use?
