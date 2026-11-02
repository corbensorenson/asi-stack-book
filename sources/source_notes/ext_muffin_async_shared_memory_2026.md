# Source Note: Muffin - A Shared Memory Buffer for Asynchronous AI Agents

| Field | Value |
|---|---|
| Source ID | `ext_muffin_async_shared_memory_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.31355v1](https://arxiv.org/html/2610.31355v1) |
| Citation | Kuo et al. (2026), Muffin |
| Published / updated | 2026-10-22 / 2026-10-22 |
| Review scope | Sections 3.1–3.2 and 4.1, 4.3–4.4; inspected workflow, visibility rule, summarizer and limitation passages. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Asynchronous exchange of selected findings can be more useful than sharing complete reasoning traces.

## Mechanisms

An orchestrator selects direct or multi-agent inference. Agents append findings with agent/step identities, read a recent window of other agents’ committed entries and keep local notes private. A summarizer uses final agent summaries.

## Evidence

Reports four-model reasoning/QA comparisons and ablations. The summarizer sometimes repairs an answer and sometimes corrupts one. Three repeats do not establish population independence.

## Failure Modes

Atomic append prevents one write conflict under its assumed model; it does not resolve contradictory content, freshness, poisoning or correlated agents. Tool use, environment interaction and long-horizon execution remain future evaluation.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

Does selective sharing retain a benefit against strong single-agent and independent-sampling baselines when delay, disagreement and complete cost are included?

## Book Chapters Supported

- `multi-agent-dynamics-collective-intelligence-and-systemic-risk`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
