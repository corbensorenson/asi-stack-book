# Source Note: Prompt Cache

| Field | Value |
|---|---|
| Source ID | `ext_prompt_cache_2024` |
| Source title | Prompt Cache: Modular Attention Reuse for Low-Latency Inference |
| Ingestion date | 2026-07-23 |
| Source version / URL | MLSys 2024 paper, arXiv:2311.04934v2, https://proceedings.mlsys.org/paper_files/paper/2024/file/a66caa1703fe34705a4368c3014c1966-Paper-Conference.pdf |
| Ingestion basis | Primary conference paper inspected; no code or benchmark reproduced. |

## Thesis

Frequently reused prompt segments can be declared as prompt modules whose
attention states are precomputed and reused while a schema preserves positional
meaning.

## Mechanisms

- Schema-defined reusable prompt modules.
- Precomputed attention state stored on the inference server.
- Position assignment that keeps reused state aligned when composing prompts.
- Explicit prompt interface for selecting modules.

## Evidence

The paper reports large time-to-first-token reductions for its prototype and
workloads. Those model, hardware, quality, and latency results are
source-reported only.

## Failure Modes

- Reusing a segment under a position or composition it was not prepared for.
- Schema drift between cache creation and use.
- Counting only TTFT while omitting write, storage, transfer, and eviction.
- Treating modular reuse as arbitrary non-prefix composition.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Distinguish schema-defined modules from opportunistic exact-prefix hits.
- Bind positions and composition rules into cache identity.
- Report cache-build work and unused modules.

## Open Questions

- Which prompt-module interfaces remain valid across model and tokenizer updates?
- How should modules inherit source, rights, and invalidation dependencies?
- When is a module schema easier to govern than raw prefix caching?
