# Source Note: Automated Design of Agentic Systems

| Field | Value |
|---|---|
| Source ID | `ext_adas_2024` |
| Source title | Automated Design of Agentic Systems |
| Ingestion date | 2026-07-10 |
| Source version / URL | Preprint, https://arxiv.org/abs/2408.08435 |
| Citation label | Hu et al. (2024), Automated Design of Agentic Systems |
| Published / updated | 2024-08-15 / 2025-03-02 |
| Ingestion basis | Full ICLR 2025 paper reviewed for the ADAS search-space/search-algorithm/evaluation-function decomposition, Meta Agent Search, code-defined agents, archive growth, novelty reflection, bounded repair attempts, validation/test separation, baselines, transfer experiments, cost and safety discussion, and limitations. No architecture-search run, model call, code artifact, transfer result, or promotion decision is imported. |

## Thesis

ADAS frames automated agent design as search over a representable agent space
under an explicit search algorithm and evaluation function. Meta Agent Search
uses a foundation-model meta-agent to write code-defined agent workflows,
evaluate them on validation tasks, and grow an archive that conditions later
designs.

## Mechanisms

- Represent each agent as a `forward` function inside a small framework that
  exposes model-query and formatting primitives.
- Condition new ideas on the archive, ask the meta-agent to reflect on novelty,
  implement the design, and retry boundedly after evaluation errors.
- Store new agents with evaluation metrics and use the archive as stepping
  stones for later workflows rather than retaining only the current best.
- Separate target-domain validation used during search from held-out test
  reporting, then test selected agents across domains and model backends.

## Evidence

- The paper reports source-scoped gains across ARC and selected reading, math,
  science, and multi-task benchmarks, plus transfer tests across domains and
  models. Those results depend on its sampled tasks, prompts, model versions,
  validation selection, evaluation budget, and implementation.
- Code-space expressiveness does not imply the finite search found all useful
  agents, and held-out benchmark improvement does not establish deployment
  usefulness, safety, or robust open-world transfer.
- No source result has moved an ASI Stack support state or been reproduced.

## Failure Modes

- Optimizing an agent architecture against limited tests while discarding hidden costs or failures.
- Treating a generated design as authorized to replace an existing governed capability.
- Repeated validation feedback can overfit the search even when a distinct test
  split exists; transfer tasks remain selected benchmark distributions.
- Archive novelty can reward complexity, latency, or model-call multiplication
  unless resource and simplicity costs travel with performance.
- The meta-agent's own novelty reflection is not independent evidence that a
  design is meaningfully distinct or safe.

## Book Chapters Supported

- `recursive-self-improvement-boundaries`
- `open-ended-improvement-engines`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `integrated-reference-architecture`

## Claims To Add Or Update

- Use the three-part ADAS formulation and Meta Agent Search as an external
  design-search comparator subject to evaluation, cost, archive, review, and
  rollback controls.
- Preserve validation/test separation, model/call budget, candidate code,
  lineage, failed repairs, and transfer scope before making a bounded claim.

## Open Questions

- What selection, archive, and rollback records would be required before a design-search result can cross a governed readiness gate?
