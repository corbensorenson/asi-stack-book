# Source Note: Recursive Language Models

| Field | Value |
|---|---|
| Source ID | `ext_recursive_language_models_2025` |
| Review date | 2026-11-02 |
| Primary version | [2512.24601v3](https://arxiv.org/html/2512.24601v3) |
| Citation | Zhang, Kraska and Khattab (2026 revision), Recursive Language Models |
| Published / updated | 2025-12-31 / 2026-05-11 |
| Review scope | Section 2 algorithms and distinctions, Section 3 task/baseline scope, Section 7 limitations. This is the May 11 v3 revision, not a new October publication. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Treat long input as an external object that a model can inspect and recursively process with code.

## Mechanisms

A persistent REPL holds the prompt and intermediate values. The root receives bounded metadata and writes code that invokes submodels on programmatically selected material; outputs can be assembled in variables.

## Evidence

Reports long-context comparisons and preliminary post-training of an 8B model. The method is an inference scaffold, not a new attention kernel or a proof of unbounded effective context.

## Failure Modes

Subcalls can explode in cost; guardrails and natural long-context tasks remain open. Stored input does not establish complete coverage, faithful summaries or permission to execute generated code.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

Which tasks justify decomposition rather than direct/full-context processing after counting all calls, sandboxing and verification?

## Book Chapters Supported

- `governed-deliberation-and-test-time-scaling`

- `virtual-context-abi` — Connect externalized prompt inspection and recursive subcalls to materialization, snapshot and omission boundaries; Governed Deliberation retains ownership of compute allocation.

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
