# Source Note: Hybrid Reasoning Agents

| Field | Value |
|---|---|
| Source ID | `ext_hybrid_reasoning_agents_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.18861v1](https://arxiv.org/html/2610.18861v1) |
| Citation | Zou et al. (2026), Hybrid Reasoning Agents |
| Published / updated | 2026-10-13 / 2026-10-13 |
| Review scope | Sections 3.1–3.2, 4.1–4.2, 5.1–5.2, 6.3 and 8; selected mechanisms and auditability setup, not an independent proof or model audit. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Interleave continuous latent computation with text-based tool interaction in one generation process.

## Mechanisms

A residual HybridLink maps hidden states back to input embeddings. Entry/exit anchors switch mode; accumulated KV state carries the hybrid trajectory across turns. HybridSFT and HybridRL train coordination and mode choices; replay retains recorded latent inputs.

## Evidence

Reports task, token, generation-step and latency comparisons. External auditability tests use visible traces on mathematics; nearest-embedding pseudo-text is a separate readout of latent steps.

## Failure Modes

Readable projection is not complete causal reasoning recovery, adversarial monitor reliability or confidentiality. A text-only transcript cannot reconstruct the full latent/KV state. Token savings do not by themselves measure complete execution cost.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

How well do monitors detect strategic failures after latent computation, and which state must be retained for bounded replay?

## Book Chapters Supported

- `governed-deliberation-and-test-time-scaling`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
