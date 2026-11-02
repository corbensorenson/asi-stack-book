# Source Note: Memory-Centric Continual Learning for AI Agents

| Field | Value |
|---|---|
| Source ID | `ext_memory_centric_continual_learning_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.29357v1](https://arxiv.org/html/2610.29357v1) |
| Citation | Li et al. (2026), Memory-Centric Continual Learning |
| Published / updated | 2026-10-21 / 2026-10-21 |
| Review scope | Sections 2 (three axes), 3 (two loops), 4.1–4.2 (behavioral outcomes and controls), and the hypotheses introducing Section 4.3 scaling relations. Selected passages, not a complete survey/reference audit. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Evaluate persistent agent memory through later behavior rather than retrieval success alone.

## Mechanisms

Separates storage substrate, episodic/semantic/procedural asset and management policy. An inner loop changes memory; an outer loop can change the management policy. Fixed-policy memory changes do not imply policy learning.

## Evidence

Proposes retention, adaptation and transfer protocols with matched stateful/reset, full-history, static retrieval and compute controls. Its resource scaling relations are hypotheses with empirical exponents, not an established universal law.

## Failure Modes

A stored or retrieved record need not improve behavior. A bundled stateful advantage does not identify which memory mechanism helped. Surveyed systems are not independently replicated here.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

Which experience-induced gains survive delay, conflicting updates and held-out tasks under matched budgets?

## Book Chapters Supported

- `durable-semantic-memory-and-knowledge-lattices`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
